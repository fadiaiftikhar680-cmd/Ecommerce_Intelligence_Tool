"""
backend/models.py
SQLAlchemy Database Models for E-Commerce Intelligence SaaS Platform.
Stores events, winning products, store inventory, COD assessments, and pricing scenarios.
"""

from datetime import datetime
import json
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text
from backend.database import Base


class EventModel(Base):
    __tablename__ = "events"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_ur = Column(String(255), nullable=True)
    hijri_date = Column(String(100), nullable=True)
    start_date = Column(String(30), nullable=False)
    end_date = Column(String(30), nullable=False)
    demand_spike_pct = Column(Integer, default=100)
    peak_window = Column(String(150), nullable=True)
    sourcing_cutoff = Column(String(30), nullable=True)
    courier_cutoff = Column(String(30), nullable=True)
    status = Column(String(100), default="Upcoming Planning")
    days_remaining = Column(Integer, default=30)
    description = Column(Text, nullable=True)
    top_categories_json = Column(Text, default="[]")
    recommended_lead_time_days = Column(Integer, default=30)
    historical_gmv_index = Column(Integer, default=80)
    courier_notes = Column(Text, nullable=True)
    seller_checklist_json = Column(Text, default="[]")
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_ur": self.name_ur,
            "hijri_date": self.hijri_date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "demand_spike_pct": self.demand_spike_pct,
            "peak_window": self.peak_window,
            "sourcing_cutoff": self.sourcing_cutoff,
            "courier_cutoff": self.courier_cutoff,
            "status": self.status,
            "days_remaining": self.days_remaining,
            "description": self.description,
            "top_categories": json.loads(self.top_categories_json) if self.top_categories_json else [],
            "recommended_lead_time_days": self.recommended_lead_time_days,
            "historical_gmv_index": self.historical_gmv_index,
            "courier_notes": self.courier_notes,
            "seller_checklist": json.loads(self.seller_checklist_json) if self.seller_checklist_json else [],
            "is_custom": self.is_custom
        }


class ProductModel(Base):
    __tablename__ = "winning_products"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_ur = Column(String(255), nullable=True)
    event_id = Column(String(64), index=True, nullable=True)
    category = Column(String(100), index=True, nullable=False)
    sourcing_hub = Column(String(255), nullable=True)
    sourcing_hub_city = Column(String(100), nullable=True)
    sourcing_cost = Column(Float, nullable=False)
    suggested_retail_price = Column(Float, nullable=False)
    profit_margin_delivered_pct = Column(Float, default=0.0)
    opportunity_score = Column(Integer, default=80)
    return_risk_default = Column(String(50), default="Medium (22%)")
    target_audience = Column(String(255), nullable=True)
    recommended_courier = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    seasonal_velocity = Column(String(100), nullable=True)
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def wholesale_hub(self):
        return self.sourcing_hub or "N/A"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_ur": self.name_ur,
            "event_id": self.event_id,
            "category": self.category,
            "wholesale_hub": self.wholesale_hub,
            "sourcing_hub": self.sourcing_hub,
            "sourcing_hub_city": self.sourcing_hub_city,
            "sourcing_cost": self.sourcing_cost,
            "suggested_retail_price": self.suggested_retail_price,
            "profit_margin_delivered_pct": self.profit_margin_delivered_pct,
            "opportunity_score": self.opportunity_score,
            "return_risk_default": self.return_risk_default,
            "target_audience": self.target_audience,
            "recommended_courier": self.recommended_courier,
            "description": self.description,
            "seasonal_velocity": self.seasonal_velocity,
            "is_custom": self.is_custom,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class StoreInventoryModel(Base):
    __tablename__ = "store_inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    stock = Column(Integer, default=0)
    unit_cost = Column(Float, default=0.0)
    selling_price = Column(Float, default=0.0)
    monthly_velocity = Column(Integer, default=0)
    status = Column(String(100), default="Healthy / Star Item")
    event_affinity = Column(String(100), nullable=True)
    days_of_inventory = Column(Integer, default=30)
    action_recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "title": self.title,
            "category": self.category,
            "stock": self.stock,
            "unit_cost": self.unit_cost,
            "selling_price": self.selling_price,
            "monthly_velocity": self.monthly_velocity,
            "status": self.status,
            "event_affinity": self.event_affinity,
            "days_of_inventory": self.days_of_inventory,
            "action_recommendation": self.action_recommendation
        }


class RiskAssessmentModel(Base):
    __tablename__ = "cod_risk_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_ref = Column(String(64), index=True, nullable=True)
    city = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    order_value = Column(Float, nullable=False)
    customer_type = Column(String(100), nullable=False)
    address_type = Column(String(100), nullable=False)
    courier = Column(String(100), nullable=False)
    predicted_rto_pct = Column(Float, nullable=False)
    risk_tier = Column(String(50), nullable=False)
    action_code = Column(String(100), nullable=False)
    action_label = Column(String(255), nullable=False)
    expected_reverse_loss_pkr = Column(Float, default=0.0)
    whatsapp_message = Column(Text, nullable=True)
    assessed_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "order_ref": self.order_ref,
            "city": self.city,
            "category": self.category,
            "order_value": self.order_value,
            "customer_type": self.customer_type,
            "address_type": self.address_type,
            "courier": self.courier,
            "predicted_rto_pct": self.predicted_rto_pct,
            "risk_tier": self.risk_tier,
            "action_code": self.action_code,
            "action_label": self.action_label,
            "expected_reverse_loss_pkr": self.expected_reverse_loss_pkr,
            "whatsapp_message": self.whatsapp_message,
            "assessed_at": self.assessed_at.isoformat() if self.assessed_at else None
        }


class SavedPricingModel(Base):
    __tablename__ = "saved_pricing_scenarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_name = Column(String(150), nullable=False)
    sourcing_cost = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    ad_cac = Column(Float, nullable=False)
    courier_fee = Column(Float, nullable=False)
    packaging_cost = Column(Float, nullable=False)
    return_rate_pct = Column(Float, nullable=False)
    return_courier_charge = Column(Float, nullable=False)
    discount_pct = Column(Float, default=0.0)
    net_profit_per_order = Column(Float, nullable=False)
    net_margin_pct = Column(Float, nullable=False)
    breakeven_roas = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "scenario_name": self.scenario_name,
            "sourcing_cost": self.sourcing_cost,
            "selling_price": self.selling_price,
            "ad_cac": self.ad_cac,
            "courier_fee": self.courier_fee,
            "packaging_cost": self.packaging_cost,
            "return_rate_pct": self.return_rate_pct,
            "return_courier_charge": self.return_courier_charge,
            "discount_pct": self.discount_pct,
            "net_profit_per_order": self.net_profit_per_order,
            "net_margin_pct": self.net_margin_pct,
            "breakeven_roas": self.breakeven_roas,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
