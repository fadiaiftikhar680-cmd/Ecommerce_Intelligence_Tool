"""
backend/routers/cod_risk.py
COD Return (RTO) Risk Predictor API powered by Scikit-learn Machine Learning Model.
Logs assessments to SQLite database and generates automated WhatsApp verification scripts.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import RiskAssessmentModel
from backend.schemas import RiskPredictionRequest, RiskPredictionResponse
from backend.ml_model import ml_service
from mock.data import CITY_COD_TIERS, COURIER_BENCHMARKS

router = APIRouter(prefix="/cod-risk", tags=["COD Return Risk Predictor"])


@router.post("/predict", response_model=RiskPredictionResponse)
def predict_cod_return_risk(req: RiskPredictionRequest, db: Session = Depends(get_db)):
    """
    Predicts Cash on Delivery (COD) Return-to-Origin (RTO) probability using trained ML pipeline,
    computes estimated reverse courier freight loss, generates tailored WhatsApp template,
    and automatically logs the assessment to the database.
    """
    prediction = ml_service.predict_risk(
        city=req.city,
        category=req.category,
        order_value=req.order_value,
        customer_type=req.customer_type,
        address_type=req.address_type,
        courier=req.courier,
        order_ref=req.order_ref
    )

    # Persist assessment record in SQLite database
    assessment_record = RiskAssessmentModel(
        order_ref=req.order_ref or "Manual Assessment",
        city=req.city,
        category=req.category,
        order_value=req.order_value,
        customer_type=req.customer_type,
        address_type=req.address_type,
        courier=req.courier,
        predicted_rto_pct=prediction["predicted_rto_pct"],
        risk_tier=prediction["risk_tier"],
        action_code=prediction["action_code"],
        action_label=prediction["action_label"],
        expected_reverse_loss_pkr=prediction["expected_reverse_loss_pkr"],
        whatsapp_message=prediction["whatsapp_message"]
    )
    db.add(assessment_record)
    db.commit()
    db.refresh(assessment_record)

    return prediction


@router.get("/history", response_model=List[dict])
def get_assessment_history(limit: int = Query(20, le=100), db: Session = Depends(get_db)):
    """Retrieve historical COD risk predictions logged in the system."""
    records = db.query(RiskAssessmentModel).order_by(RiskAssessmentModel.assessed_at.desc()).limit(limit).all()
    return [r.to_dict() for r in records]


@router.get("/city-benchmarks")
def get_city_benchmarks():
    """Retrieve Pakistan city tiers, SLAs, and average RTO rates."""
    rows = []
    for city, data in CITY_COD_TIERS.items():
        rows.append({
            "City": city,
            "Tier": f"Tier {data['tier']}",
            "Zone": data["zone"],
            "Average COD RTO %": data["avg_rto_pct"],
            "Avg Delivery Days": data["avg_delivery_days"],
            "Coverage Quality": data["courier_coverage"]
        })
    return rows


@router.get("/couriers")
def get_couriers():
    """Retrieve Pakistani logistics partner tariffs and performance benchmarks."""
    return [{"name": k, **v} for k, v in COURIER_BENCHMARKS.items()]
