"""
backend/routers/pricing.py
Smart Price & Margin Protector calculation and scenario persistence endpoints.
Simulates COD reverse shipping freight loss and break-even ROAS for Pakistani merchants.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import SavedPricingModel
from backend.schemas import PricingCalculationRequest, PricingCalculationResponse, SavedScenarioCreate

router = APIRouter(prefix="/pricing", tags=["Price & Margin Protector"])


def run_margin_simulation(req: PricingCalculationRequest) -> dict:
    """Core mathematical engine for Pakistani COD margin & return loss simulation."""
    discounted_price = req.selling_price * (1.0 - (req.discount_pct / 100.0))
    delivered_orders = max(0.0, 100.0 - req.return_rate_pct)
    returned_orders = float(req.return_rate_pct)

    # Revenue from delivered orders
    total_revenue = delivered_orders * discounted_price

    # Costs across 100 placed orders
    cogs_delivered = delivered_orders * req.sourcing_cost
    packaging_total = 100.0 * req.packaging_cost
    ad_spend_total = 100.0 * req.ad_cac
    outbound_shipping = 100.0 * req.courier_fee
    reverse_shipping = returned_orders * req.return_courier_charge

    total_costs = cogs_delivered + packaging_total + ad_spend_total + outbound_shipping + reverse_shipping
    net_profit_total = total_revenue - total_costs
    net_profit_per_order = net_profit_total / 100.0
    net_margin_pct = (net_profit_total / total_revenue * 100.0) if total_revenue > 0 else 0.0

    # Ideal scenario without returns
    ideal_profit_per_order = discounted_price - (req.sourcing_cost + req.packaging_cost + req.ad_cac + req.courier_fee)
    ideal_margin_pct = (ideal_profit_per_order / discounted_price * 100.0) if discounted_price > 0 else 0.0
    rto_profit_drag = ideal_profit_per_order - net_profit_per_order

    # Break-even ROAS
    breakeven_roas = (req.selling_price / (req.selling_price - req.sourcing_cost - req.courier_fee - req.packaging_cost)) if (req.selling_price - req.sourcing_cost - req.courier_fee - req.packaging_cost) > 0 else 9.99
    actual_roas = (total_revenue / ad_spend_total) if ad_spend_total > 0 else 0.0

    # Maximum discount before net profit hits 0
    max_discount = 0.0
    for disc in range(0, 70):
        test_price = req.selling_price * (1.0 - disc / 100.0)
        test_rev = delivered_orders * test_price
        if (test_rev - total_costs) <= 0:
            max_discount = max(0.0, disc - 1.0)
            break
        max_discount = float(disc)

    if net_margin_pct >= 25.0:
        verdict = "HEALTHY & HIGHLY PROFITABLE"
        verdict_color = "#10B981"
    elif net_margin_pct >= 12.0:
        verdict = "MODERATE SAFE MARGIN"
        verdict_color = "#38BDF8"
    elif net_margin_pct > 0.0:
        verdict = "THIN MARGIN (HIGH RISK OF LOSS ON RETURNS)"
        verdict_color = "#F59E0B"
    else:
        verdict = "LOSS-MAKING UNIT ECONOMICS (DO NOT LAUNCH)"
        verdict_color = "#EF4444"

    break_even_selling_price = (total_costs / delivered_orders) if delivered_orders > 0 else req.selling_price
    rto_penalty_per_order = max(0.0, abs(rto_profit_drag))
    breakdown = {
        "cogs": req.sourcing_cost,
        "ad_spend": req.ad_cac,
        "outbound_shipping": req.courier_fee,
        "packaging": req.packaging_cost,
        "reverse_shipping_drag": rto_penalty_per_order,
    }

    response = {
        "discounted_price": round(discounted_price, 0),
        "total_revenue_per_100": round(total_revenue, 0),
        "total_costs_per_100": round(total_costs, 0),
        "net_profit_per_100": round(net_profit_total, 0),
        "net_profit_per_order": round(net_profit_per_order, 1),
        "net_margin_pct": round(net_margin_pct, 1),
        "ideal_profit_per_order": round(ideal_profit_per_order, 1),
        "ideal_margin_pct": round(ideal_margin_pct, 1),
        "rto_profit_drag_per_order": round(rto_profit_drag, 1),
        "cogs_total": round(cogs_delivered, 0),
        "packaging_total": round(packaging_total, 0),
        "ad_spend_total": round(ad_spend_total, 0),
        "outbound_shipping_total": round(outbound_shipping, 0),
        "reverse_shipping_total": round(reverse_shipping, 0),
        "breakeven_roas": round(breakeven_roas, 2),
        "actual_simulated_roas": round(actual_roas, 2),
        "max_safe_discount_pct": round(max_discount, 0),
        "breakeven_selling_price": round(break_even_selling_price, 0),
        "delivered_orders_per_100": int(delivered_orders),
        "returned_orders_per_100": int(returned_orders),
        "rto_loss_penalty_per_order": round(rto_penalty_per_order, 1),
        "breakdown": breakdown,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "status": verdict,
        "status_color": verdict_color,
        "max_allowable_discount_pct": round(max_discount, 0),
    }
    return response


@router.post("/calculate", response_model=PricingCalculationResponse)
def calculate_margin_and_pricing(req: PricingCalculationRequest):
    """Calculates safe selling price, blended net margin, break-even ROAS, and reverse freight drag."""
    return run_margin_simulation(req)


@router.post("/save", status_code=201)
def save_pricing_scenario(scenario_in: SavedScenarioCreate, db: Session = Depends(get_db)):
    """Save a tested pricing scenario to database."""
    calc = run_margin_simulation(scenario_in)
    saved = SavedPricingModel(
        scenario_name=scenario_in.scenario_name,
        sourcing_cost=scenario_in.sourcing_cost,
        selling_price=scenario_in.selling_price,
        ad_cac=scenario_in.ad_cac,
        courier_fee=scenario_in.courier_fee,
        packaging_cost=scenario_in.packaging_cost,
        return_rate_pct=scenario_in.return_rate_pct,
        return_courier_charge=scenario_in.return_courier_charge,
        discount_pct=scenario_in.discount_pct,
        net_profit_per_order=calc["net_profit_per_order"],
        net_margin_pct=calc["net_margin_pct"],
        breakeven_roas=calc["breakeven_roas"]
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved.to_dict()


@router.get("/saved", response_model=List[dict])
def get_saved_scenarios(db: Session = Depends(get_db)):
    """Retrieve all previously saved pricing scenarios."""
    scenarios = db.query(SavedPricingModel).order_by(SavedPricingModel.created_at.desc()).all()
    return [s.to_dict() for s in scenarios]


@router.delete("/saved/{scenario_id}")
def delete_saved_scenario(scenario_id: int, db: Session = Depends(get_db)):
    """Delete a saved pricing scenario."""
    scenario = db.query(SavedPricingModel).filter(SavedPricingModel.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    db.delete(scenario)
    db.commit()
    return {"status": "success", "message": f"Scenario {scenario_id} deleted"}
