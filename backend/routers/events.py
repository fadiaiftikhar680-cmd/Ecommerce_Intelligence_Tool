"""
backend/routers/events.py
Event Calendar and Demand Alerts API Endpoints (CRUD operations).
"""

import json
import uuid
from datetime import date, datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import EventModel
from backend.schemas import EventCreate, EventResponse
from backend.auth import require_admin_api_key

router = APIRouter(prefix="/events", tags=["Event Intelligence"])


def _recalculate_days(event_dict: dict) -> dict:
    """Dynamically recalculate days_remaining from today so it's always current."""
    try:
        start = datetime.strptime(event_dict["start_date"], "%Y-%m-%d").date()
        end = datetime.strptime(event_dict["end_date"], "%Y-%m-%d").date()
        delta = (start - date.today()).days
        event_dict["days_remaining"] = max(0, delta)
        if start <= date.today() <= end:
            event_dict["event_phase"] = "Current"
        elif start > date.today():
            event_dict["event_phase"] = "Upcoming"
        else:
            event_dict["event_phase"] = "Past"
    except Exception:
        pass
    return event_dict


@router.get("", response_model=List[dict])
def get_all_events(
    status_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve all synchronized Hijri-Gregorian events with optional filtering.
    Only returns CURRENT and UPCOMING events (today or future start dates).
    Days remaining is recalculated dynamically on every request.
    """
    today = date.today()
    all_events = db.query(EventModel).all()

    # Filter: only show events that haven't fully ended yet
    active_and_future = []
    for e in all_events:
        try:
            end_d = datetime.strptime(e.end_date, "%Y-%m-%d").date()
            if end_d >= today:
                active_and_future.append(e)
        except Exception:
            active_and_future.append(e)  # keep if parse fails (e.g. "Rolling daily")

    if status_filter and status_filter != "All":
        active_and_future = [e for e in active_and_future if status_filter.lower() in e.status.lower()]

    # Sort: currently active events first, then by start_date ascending
    def sort_key(e):
        try:
            sd = datetime.strptime(e.start_date, "%Y-%m-%d").date()
            ed = datetime.strptime(e.end_date, "%Y-%m-%d").date()
            if sd <= today <= ed:
                return (0, sd)
            elif sd > today:
                return (1, sd)
            else:
                return (2, sd)
        except Exception:
            return (1, date.max)

    active_and_future.sort(key=sort_key)

    return [_recalculate_days(e.to_dict()) for e in active_and_future]



@router.get("/{event_id}")
def get_event_by_id(event_id: str, db: Session = Depends(get_db)):
    """Retrieve specific event by its ID."""
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.to_dict()


@router.post("", status_code=201, dependencies=[Depends(require_admin_api_key)])
def create_custom_event(event_in: EventCreate, db: Session = Depends(get_db)):
    """Create a new custom seller event / flash sale campaign."""
    event_id = f"custom-{uuid.uuid4().hex[:8]}"
    new_event = EventModel(
        id=event_id,
        name=event_in.name,
        name_ur=event_in.name_ur,
        hijri_date=event_in.hijri_date,
        start_date=event_in.start_date,
        end_date=event_in.end_date,
        demand_spike_pct=event_in.demand_spike_pct,
        peak_window=event_in.peak_window,
        sourcing_cutoff=event_in.sourcing_cutoff,
        courier_cutoff=event_in.courier_cutoff,
        status=event_in.status,
        days_remaining=event_in.days_remaining,
        description=event_in.description,
        top_categories_json=json.dumps(event_in.top_categories),
        recommended_lead_time_days=event_in.recommended_lead_time_days,
        historical_gmv_index=event_in.historical_gmv_index,
        courier_notes=event_in.courier_notes,
        seller_checklist_json=json.dumps(event_in.seller_checklist),
        is_custom=True
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event.to_dict()


@router.delete("/{event_id}", dependencies=[Depends(require_admin_api_key)])
def delete_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a custom event."""
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not event.is_custom:
        raise HTTPException(status_code=403, detail="Built-in events cannot be deleted.")
    db.delete(event)
    db.commit()
    return {"status": "success", "message": f"Event {event_id} deleted successfully"}
