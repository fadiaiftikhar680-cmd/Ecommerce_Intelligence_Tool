"""
backend/routers/overview.py
Market overview and primary dashboard KPI metrics.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import EventModel, ProductModel, StoreInventoryModel, RiskAssessmentModel
from mock.data import CITY_COD_TIERS

router = APIRouter(prefix="/overview", tags=["Market Overview"])


@router.get("")
def get_market_overview(db: Session = Depends(get_db)):
    """Fetch high-level market overview and macro metrics from the database."""
    events = db.query(EventModel).order_by(EventModel.days_remaining.asc()).all()
    next_event = events[0].to_dict() if events else None

    products = db.query(ProductModel).all()
    total_products = len(products)
    avg_opportunity = sum(p.opportunity_score for p in products) / max(total_products, 1)

    all_cities = list(CITY_COD_TIERS.values())
    avg_market_rto = sum(c["avg_rto_pct"] for c in all_cities) / len(all_cities)

    inventory = db.query(StoreInventoryModel).all()
    total_skus = len(inventory)
    total_inventory_value = sum(item.stock * item.unit_cost for item in inventory)

    total_assessments = db.query(RiskAssessmentModel).count()

    return {
        "status": "success",
        "next_event": next_event,
        "total_winning_products": total_products,
        "avg_opportunity_score": round(avg_opportunity, 1),
        "benchmark_market_rto_pct": round(avg_market_rto, 1),
        "active_season": "Pre-Ramadan & Eid Festive Buildup",
        "demand_multiplier_peak": "3.2x",
        "urgent_actions_count": 3,
        "total_skus_tracked": total_skus,
        "total_inventory_value_pkr": round(total_inventory_value, 0),
        "total_assessments_logged": total_assessments,
        "database_engine": "SQLite / SQLAlchemy ORM"
    }
