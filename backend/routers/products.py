"""
backend/routers/products.py
Winning Products Catalog API Endpoints (CRUD & Opportunity Ranking).
"""

import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ProductModel
from backend.schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Winning Products"])


@router.get("", response_model=List[dict])
def get_winning_products(
    event_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_opportunity: int = Query(0),
    sort_by: str = Query("Opportunity Score (High to Low)"),
    db: Session = Depends(get_db)
):
    """Filter and rank winning products for upcoming Pakistani shopping events."""
    query = db.query(ProductModel)

    if event_id and event_id != "All Events":
        query = query.filter(ProductModel.event_id == event_id)

    if category and category != "All Categories":
        query = query.filter(ProductModel.category == category)

    if min_opportunity > 0:
        query = query.filter(ProductModel.opportunity_score >= min_opportunity)

    products = [p.to_dict() for p in query.all()]

    if sort_by == "Opportunity Score (High to Low)":
        products.sort(key=lambda x: x["opportunity_score"], reverse=True)
    elif sort_by == "Wholesale Price (Low to High)":
        products.sort(key=lambda x: x["sourcing_cost"])
    elif sort_by == "Retail Price (High to Low)":
        products.sort(key=lambda x: x["suggested_retail_price"], reverse=True)
    elif sort_by == "Profit Margin %":
        products.sort(key=lambda x: x["profit_margin_delivered_pct"], reverse=True)

    return products


@router.get("/categories")
def get_product_categories(db: Session = Depends(get_db)):
    """Return all unique product categories in the platform."""
    cats = db.query(ProductModel.category).distinct().all()
    categories_list = sorted([c[0] for c in cats if c[0]])
    return ["All Categories"] + categories_list


@router.get("/{product_id}")
def get_product_by_id(product_id: str, db: Session = Depends(get_db)):
    """Retrieve details for a single winning product."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.to_dict()


@router.post("", status_code=201)
def create_winning_product(prod_in: ProductCreate, db: Session = Depends(get_db)):
    """Add a new winning product to the database."""
    product_id = f"custom-prod-{uuid.uuid4().hex[:8]}"

    # Auto-calculate margin if not provided
    margin = prod_in.profit_margin_delivered_pct
    if not margin and prod_in.suggested_retail_price > 0:
        margin = round(((prod_in.suggested_retail_price - prod_in.sourcing_cost) / prod_in.suggested_retail_price) * 100, 1)

    new_prod = ProductModel(
        id=product_id,
        name=prod_in.name,
        name_ur=prod_in.name_ur,
        event_id=prod_in.event_id,
        category=prod_in.category,
        sourcing_hub=prod_in.sourcing_hub,
        sourcing_hub_city=prod_in.sourcing_hub_city,
        sourcing_cost=prod_in.sourcing_cost,
        suggested_retail_price=prod_in.suggested_retail_price,
        profit_margin_delivered_pct=margin,
        opportunity_score=prod_in.opportunity_score,
        return_risk_default=prod_in.return_risk_default,
        target_audience=prod_in.target_audience,
        recommended_courier=prod_in.recommended_courier,
        description=prod_in.description,
        seasonal_velocity=prod_in.seasonal_velocity,
        is_custom=True
    )
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod.to_dict()


@router.delete("/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """Delete a custom product."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"status": "success", "message": f"Product {product_id} deleted successfully"}
