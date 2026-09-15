"""
backend/schemas.py
Pydantic Request and Response Schemas for FastAPI REST API endpoints.
Ensures strong typing, data validation, and automated Swagger/OpenAPI documentation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# EVENT SCHEMAS
# -----------------------------------------------------------------------------
class EventCreate(BaseModel):
    name: str = Field(..., example="Summer Clearance Gala")
    name_ur: Optional[str] = Field(None, example="سمر کلیئرنس گالا")
    hijri_date: Optional[str] = Field(None, example="Safar 1449 AH")
    start_date: str = Field(..., example="2026-07-01")
    end_date: str = Field(..., example="2026-07-15")
    demand_spike_pct: int = Field(120, ge=0, le=1000, example=150)
    peak_window: Optional[str] = Field(None, example="1st to 10th July")
    sourcing_cutoff: Optional[str] = Field(None, example="2026-06-15")
    courier_cutoff: Optional[str] = Field(None, example="2026-07-12")
    status: str = Field("Upcoming Planning", example="Active Sourcing")
    days_remaining: int = Field(30, ge=0, example=25)
    description: Optional[str] = Field(None)
    top_categories: List[str] = Field(default_factory=list)
    recommended_lead_time_days: int = Field(30, ge=0, example=30)
    historical_gmv_index: int = Field(75, ge=0, le=100, example=85)
    courier_notes: Optional[str] = Field(None)
    seller_checklist: List[str] = Field(default_factory=list)


class EventResponse(EventCreate):
    id: str
    is_custom: bool = False


# -----------------------------------------------------------------------------
# PRODUCT SCHEMAS
# -----------------------------------------------------------------------------
class ProductCreate(BaseModel):
    name: str = Field(..., example="Premium Khunja Chiffon Dupatta 3-Piece")
    name_ur: Optional[str] = Field(None, example="پریمیم شیفون ڈوپٹہ سوٹ")
    event_id: Optional[str] = Field("eid-ul-fitr-2026", example="eid-ul-fitr-2026")
    category: str = Field(..., example="Women's Festive Pret & Lawn")
    wholesale_hub: Optional[str] = Field(None, example="Shah Alam Market & Faisalabad")
    sourcing_hub: Optional[str] = Field("Shah Alam Market & Faisalabad", example="Shah Alam Market, Lahore")
    sourcing_hub_city: Optional[str] = Field("Lahore", example="Lahore")
    sourcing_cost: float = Field(..., gt=0, example=1200.0)
    suggested_retail_price: float = Field(..., gt=0, example=3450.0)
    profit_margin_delivered_pct: Optional[float] = Field(42.5, ge=0, le=100, example=42.5)
    opportunity_score: int = Field(85, ge=0, le=100, example=92)
    return_risk_default: str = Field("Medium (22%)", example="Low (14%)")
    target_audience: Optional[str] = Field(None, example="Women aged 22-45")
    recommended_courier: Optional[str] = Field("Trax / PostEx", example="PostEx")
    description: Optional[str] = Field(None)
    seasonal_velocity: Optional[str] = Field("Peak (Ramadan-Eid)", example="Peak")


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    name_ur: Optional[str] = None
    category: Optional[str] = None
    sourcing_cost: Optional[float] = None
    suggested_retail_price: Optional[float] = None
    opportunity_score: Optional[int] = None
    return_risk_default: Optional[str] = None


class ProductResponse(ProductCreate):
    id: str
    is_custom: bool = False
    created_at: Optional[str] = None


# -----------------------------------------------------------------------------
# STORE INVENTORY SCHEMAS
# -----------------------------------------------------------------------------
class InventoryCreate(BaseModel):
    sku: str = Field(..., example="EID-SUIT-009")
    title: str = Field(..., example="Embroidered Lawn Kurti")
    category: str = Field(..., example="Apparel & Footwear (Size Risk)")
    stock: int = Field(..., ge=0, example=150)
    unit_cost: float = Field(..., ge=0, example=850.0)
    selling_price: float = Field(..., ge=0, example=2200.0)
    monthly_velocity: int = Field(40, ge=0, example=45)
    status: Optional[str] = Field("Healthy / Star Item", example="Healthy / Star Item")
    event_affinity: Optional[str] = Field("Eid-ul-Fitr", example="Eid-ul-Fitr")
    days_of_inventory: Optional[int] = Field(35, ge=0, example=35)
    action_recommendation: Optional[str] = Field(None)


class InventoryUpdate(BaseModel):
    stock: Optional[int] = Field(None, ge=0)
    selling_price: Optional[float] = Field(None, ge=0)
    status: Optional[str] = None
    action_recommendation: Optional[str] = None


class InventoryResponse(InventoryCreate):
    id: int


# -----------------------------------------------------------------------------
# COD RISK PREDICTION SCHEMAS
# -----------------------------------------------------------------------------
class RiskPredictionRequest(BaseModel):
    city: str = Field(..., example="Hyderabad")
    category: str = Field(..., example="Apparel & Footwear (Size Risk)")
    order_value: float = Field(..., gt=0, example=3450.0)
    customer_type: str = Field(..., example="First-Time Buyer (Cold Traffic / Ad Click)")
    address_type: str = Field(..., example="Moderate (Area/Mohalla mentioned, No house #)")
    courier: str = Field(..., example="PostEx COD")
    order_ref: Optional[str] = Field(None, example="ORD-PK-8831")


class RiskPredictionResponse(BaseModel):
    city: str
    city_tier: str
    benchmark_city_rto_pct: float
    predicted_rto_pct: float
    risk_tier: str
    action_code: str
    action_label: str
    color: str
    expected_reverse_loss_pkr: float
    courier_freight_standard: float
    courier_reverse_tariff: float
    whatsapp_message: str
    order_ref: Optional[str] = None


# -----------------------------------------------------------------------------
# GEMINI INSIGHT SCHEMAS
# -----------------------------------------------------------------------------
class GeminiInsightRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=4000)
    context: Optional[Dict[str, Any]] = Field(default=None)


class GeminiInsightResponse(BaseModel):
    answer: str
    model: str


# -----------------------------------------------------------------------------
# PRICING SIMULATION SCHEMAS
# -----------------------------------------------------------------------------
class PricingCalculationRequest(BaseModel):
    sourcing_cost: float = Field(..., ge=0, example=1400.0)
    selling_price: float = Field(..., gt=0, example=3400.0)
    ad_cac: float = Field(..., ge=0, example=650.0)
    courier_fee: float = Field(..., ge=0, example=220.0)
    packaging_cost: float = Field(..., ge=0, example=70.0)
    return_rate_pct: float = Field(..., ge=0, le=100, example=22.0)
    return_courier_charge: float = Field(..., ge=0, example=160.0)
    discount_pct: float = Field(0.0, ge=0, lt=100, example=10.0)


class PricingCalculationResponse(BaseModel):
    discounted_price: float
    total_revenue_per_100: float
    total_costs_per_100: float
    net_profit_per_100: float
    net_profit_per_order: float
    net_margin_pct: float
    ideal_profit_per_order: float
    ideal_margin_pct: float
    rto_profit_drag_per_order: float
    cogs_total: float
    packaging_total: float
    ad_spend_total: float
    outbound_shipping_total: float
    reverse_shipping_total: float
    breakeven_roas: float
    actual_simulated_roas: float
    max_safe_discount_pct: float
    breakeven_selling_price: float
    delivered_orders_per_100: int
    returned_orders_per_100: int
    rto_loss_penalty_per_order: float
    breakdown: Dict[str, float]
    verdict: str
    verdict_color: str
    status: str
    status_color: str
    max_allowable_discount_pct: float


class SavedScenarioCreate(PricingCalculationRequest):
    scenario_name: str = Field(..., example="Eid Stitched Lawn Kurti Campaign")
