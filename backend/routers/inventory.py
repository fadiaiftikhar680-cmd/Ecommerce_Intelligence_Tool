"""
backend/routers/inventory.py
Store Inventory Predictor & Dead Stock Liquidation API Endpoints (CRUD operations).
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import StoreInventoryModel
from backend.schemas import InventoryCreate, InventoryUpdate, InventoryResponse

router = APIRouter(prefix="/inventory", tags=["Store Inventory Predictor"])


@router.get("", response_model=List[dict])
def get_store_inventory(db: Session = Depends(get_db)):
    """Retrieve full seller inventory from database with stock health indicators."""
    items = db.query(StoreInventoryModel).all()
    return [i.to_dict() for i in items]


@router.post("", status_code=201)
def add_inventory_sku(sku_in: InventoryCreate, db: Session = Depends(get_db)):
    """Add a new product SKU into the seller inventory."""
    existing = db.query(StoreInventoryModel).filter(StoreInventoryModel.sku == sku_in.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"SKU {sku_in.sku} already exists in database")

    # Compute days of inventory
    daily_vel = sku_in.monthly_velocity / 30.0 if sku_in.monthly_velocity > 0 else 0.1
    days_inv = int(sku_in.stock / daily_vel)

    # Determine status
    if days_inv <= 14:
        status = "Stockout Imminent"
        recommendation = "Reorder immediately before supplier cutoff date."
    elif days_inv >= 90:
        status = "Dead Stock / Slow Mover"
        recommendation = "Bundle with festive fast-seller or run flash discount clearance."
    else:
        status = "Healthy / Star Item"
        recommendation = "Maintain current replenishment cadence."

    new_item = StoreInventoryModel(
        sku=sku_in.sku,
        title=sku_in.title,
        category=sku_in.category,
        stock=sku_in.stock,
        unit_cost=sku_in.unit_cost,
        selling_price=sku_in.selling_price,
        monthly_velocity=sku_in.monthly_velocity,
        status=status,
        event_affinity=sku_in.event_affinity,
        days_of_inventory=days_inv,
        action_recommendation=recommendation
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item.to_dict()


@router.put("/{sku}")
def update_inventory_sku(sku: str, update_in: InventoryUpdate, db: Session = Depends(get_db)):
    """Update stock count or status for an existing SKU."""
    item = db.query(StoreInventoryModel).filter(StoreInventoryModel.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="SKU not found")

    if update_in.stock is not None:
        item.stock = update_in.stock
        daily_vel = item.monthly_velocity / 30.0 if item.monthly_velocity > 0 else 0.1
        item.days_of_inventory = int(item.stock / daily_vel)
        if item.days_of_inventory <= 14:
            item.status = "Stockout Imminent"
        elif item.days_of_inventory >= 90:
            item.status = "Dead Stock / Slow Mover"
        else:
            item.status = "Healthy / Star Item"

    if update_in.selling_price is not None:
        item.selling_price = update_in.selling_price
    if update_in.status is not None:
        item.status = update_in.status
    if update_in.action_recommendation is not None:
        item.action_recommendation = update_in.action_recommendation

    db.commit()
    db.refresh(item)
    return item.to_dict()


@router.delete("/{sku}")
def delete_inventory_sku(sku: str, db: Session = Depends(get_db)):
    """Delete an inventory SKU."""
    item = db.query(StoreInventoryModel).filter(StoreInventoryModel.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="SKU not found")
    db.delete(item)
    db.commit()
    return {"status": "success", "message": f"SKU {sku} removed"}


@router.get("/dead-stock-analysis")
def get_dead_stock_liquidation_plan(db: Session = Depends(get_db)):
    """Generates an automated liquidation and discount strategy for slow-moving inventory."""
    items = db.query(StoreInventoryModel).all()
    dead_items = [i for i in items if "dead" in i.status.lower() or "slow" in i.status.lower()]

    total_dead_units = sum(i.stock for i in dead_items)
    total_locked_capital = sum(i.stock * i.unit_cost for i in dead_items)
    salvage_at_cost = total_locked_capital

    recommendations = []
    for item in dead_items:
        break_even_price = item.unit_cost * 1.08  # +8% handling
        flash_discount_pct = round(((item.selling_price - break_even_price) / item.selling_price) * 100, 0)
        recommendations.append({
            "sku": item.sku,
            "title": item.title,
            "units_locked": item.stock,
            "capital_locked_pkr": item.stock * item.unit_cost,
            "original_selling_price": item.selling_price,
            "recommended_flash_price": round(break_even_price, 0),
            "max_clearance_discount_pct": f"{int(flash_discount_pct)}%",
            "liquidation_strategy": "Bundle as free promotional gift or 1+1 Ramadan Clearance deal."
        })

    return {
        "dead_sku_count": len(dead_items),
        "total_units_locked": total_dead_units,
        "total_capital_locked_pkr": total_locked_capital,
        "salvage_at_cost_pkr": salvage_at_cost,
        "liquidation_plan": recommendations
    }
