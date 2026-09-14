"""
backend/routers/overview.py
Market overview and primary dashboard KPI metrics.
"""

from datetime import date, datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import EventModel, ProductModel, StoreInventoryModel, RiskAssessmentModel
from mock.data import CITY_COD_TIERS

router = APIRouter(prefix="/overview", tags=["Market Overview"])


def _days_left(date_str: str) -> int:
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return max(0, (target - date.today()).days)
    except Exception:
        return 0


@router.get("")
def get_market_overview(db: Session = Depends(get_db)):
    """Fetch high-level market overview and macro metrics from the database."""
    today = date.today()
    all_events = db.query(EventModel).all()

    # Recalculate days and classify events
    live_events = []
    upcoming_events = []

    for e in all_events:
        try:
            sd = datetime.strptime(e.start_date, "%Y-%m-%d").date()
            ed = datetime.strptime(e.end_date, "%Y-%m-%d").date()
            days = max(0, (sd - today).days)
            ev_dict = e.to_dict()
            ev_dict["days_remaining"] = days
            if sd <= today <= ed:
                live_events.append((sd, ev_dict))
            elif sd > today:
                upcoming_events.append((sd, ev_dict))
        except Exception:
            pass

    # Sort upcoming by start date
    upcoming_events.sort(key=lambda x: x[0])
    live_events.sort(key=lambda x: x[0])

    # next_event = first upcoming (not currently live)
    next_event = upcoming_events[0][1] if upcoming_events else (live_events[0][1] if live_events else None)

    # Top 3 upcoming events for homepage panel
    top_upcoming = [ev for _, ev in upcoming_events[:3]]

    # Currently live event (if any)
    current_live = live_events[0][1] if live_events else None
    seasonal_candidates = [ev for _, ev in live_events + upcoming_events]
    peak_event = max(
        seasonal_candidates,
        key=lambda ev: ev.get("demand_spike_pct", 0),
        default=None
    )

    products = db.query(ProductModel).all()
    total_products = len(products)
    avg_opportunity = sum(p.opportunity_score for p in products) / max(total_products, 1)

    all_cities = list(CITY_COD_TIERS.values())
    avg_market_rto = sum(c["avg_rto_pct"] for c in all_cities) / len(all_cities)

    inventory = db.query(StoreInventoryModel).all()
    total_skus = len(inventory)
    total_inventory_value = sum(item.stock * item.unit_cost for item in inventory)

    total_assessments = db.query(RiskAssessmentModel).count()

    # Determine active season label
    if current_live:
        season_label = f"🟢 LIVE: {current_live['name']}"
    elif next_event:
        season_label = f"⏳ Upcoming: {next_event['name']}"
    else:
        season_label = "Pakistan E-Commerce Season"

    return {
        "status": "success",
        "next_event": next_event,
        "current_live_event": current_live,
        "top_upcoming_events": top_upcoming,
        "total_winning_products": total_products,
        "avg_opportunity_score": round(avg_opportunity, 1),
        "benchmark_market_rto_pct": round(avg_market_rto, 1),
        "active_season": season_label,
        "seasonal_sale": {
            "current_event": current_live,
            "next_event": upcoming_events[0][1] if upcoming_events else None,
            "peak_event": peak_event,
        },
        "demand_multiplier_peak": (
            f"+{peak_event.get('demand_spike_pct', 0)}%" if peak_event else "N/A"
        ),
        "urgent_actions_count": 3,
        "total_skus_tracked": total_skus,
        "total_inventory_value_pkr": round(total_inventory_value, 0),
        "total_assessments_logged": total_assessments,
        "database_engine": "SQLite / SQLAlchemy ORM"
    }
