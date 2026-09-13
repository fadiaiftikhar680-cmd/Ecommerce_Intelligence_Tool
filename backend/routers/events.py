"""
backend/routers/events.py
Event Calendar and Demand Alerts API Endpoints (CRUD operations).
"""

import json
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import EventModel
from backend.schemas import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["Event Intelligence"])


@router.get("", response_model=List[dict])
def get_all_events(
    status_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve all synchronized Hijri-Gregorian events with optional filtering."""
    query = db.query(EventModel).order_by(EventModel.days_remaining.asc())
    events = query.all()

    if status_filter and status_filter != "All":
        events = [e for e in events if status_filter.lower() in e.status.lower()]

    return [e.to_dict() for e in events]


@router.get("/{event_id}")
def get_event_by_id(event_id: str, db: Session = Depends(get_db)):
    """Retrieve specific event by its ID."""
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.to_dict()


@router.post("", status_code=201)
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


@router.delete("/{event_id}")
def delete_event(event_id: str, db: Session = Depends(get_db)):
    """Delete a custom event."""
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"status": "success", "message": f"Event {event_id} deleted successfully"}
