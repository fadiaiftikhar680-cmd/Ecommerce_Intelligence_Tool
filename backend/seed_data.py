"""
backend/seed_data.py
Seeds initial Pakistani e-commerce records into SQLite database on initial application setup.
"""

import json
from sqlalchemy.orm import Session
from backend.models import EventModel, ProductModel, StoreInventoryModel
from backend.database import SessionLocal, engine, Base
from mock.data import EVENTS_DATA, WINNING_PRODUCTS_DATA, SAMPLE_STORE_INVENTORY


def seed_initial_data(db: Session = None):
    """Checks if tables are populated; if not, inserts initial Pakistan market datasets."""
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        # 1. Seed Events
        if db.query(EventModel).count() == 0:
            for ev in EVENTS_DATA:
                event_obj = EventModel(
                    id=ev["id"],
                    name=ev["name"],
                    name_ur=ev.get("name_ur"),
                    hijri_date=ev.get("hijri_date"),
                    start_date=ev["start_date"],
                    end_date=ev["end_date"],
                    demand_spike_pct=ev.get("demand_spike_pct", 100),
                    peak_window=ev.get("peak_window"),
                    sourcing_cutoff=ev.get("sourcing_cutoff"),
                    courier_cutoff=ev.get("courier_cutoff"),
                    status=ev.get("status", "Upcoming Planning"),
                    days_remaining=ev.get("days_remaining", 30),
                    description=ev.get("description"),
                    top_categories_json=json.dumps(ev.get("top_categories", [])),
                    recommended_lead_time_days=ev.get("recommended_lead_time_days", 30),
                    historical_gmv_index=ev.get("historical_gmv_index", 80),
                    courier_notes=ev.get("courier_notes"),
                    seller_checklist_json=json.dumps(ev.get("seller_checklist", [])),
                    is_custom=False
                )
                db.add(event_obj)
            db.commit()

        # 2. Seed Winning Products
        existing_products = {p.id: p for p in db.query(ProductModel).all()}
        for prod in WINNING_PRODUCTS_DATA:
            hub_value = prod.get("wholesale_hub") or prod.get("sourcing_hub")
            product_obj = existing_products.get(prod["id"])
            if product_obj is None:
                product_obj = ProductModel(
                    id=prod["id"],
                    name=prod["name"],
                    name_ur=prod.get("name_ur"),
                    event_id=prod.get("event_id"),
                    category=prod.get("category"),
                    sourcing_hub=hub_value,
                    sourcing_hub_city=prod.get("sourcing_hub_city"),
                    sourcing_cost=prod.get("sourcing_cost", 0.0),
                    suggested_retail_price=prod.get("suggested_retail_price", 0.0),
                    profit_margin_delivered_pct=prod.get("profit_margin_delivered_pct", 0.0),
                    opportunity_score=prod.get("opportunity_score", 80),
                    return_risk_default=prod.get("return_risk_default", "Medium (22%)"),
                    target_audience=prod.get("target_audience"),
                    recommended_courier=prod.get("recommended_courier"),
                    description=prod.get("description"),
                    seasonal_velocity=prod.get("seasonal_velocity"),
                    is_custom=False
                )
                db.add(product_obj)
            else:
                product_obj.name = prod["name"]
                product_obj.name_ur = prod.get("name_ur")
                product_obj.event_id = prod.get("event_id")
                product_obj.category = prod.get("category")
                product_obj.sourcing_hub = hub_value
                product_obj.sourcing_hub_city = prod.get("sourcing_hub_city")
                product_obj.sourcing_cost = prod.get("sourcing_cost", 0.0)
                product_obj.suggested_retail_price = prod.get("suggested_retail_price", 0.0)
                product_obj.profit_margin_delivered_pct = prod.get("profit_margin_delivered_pct", 0.0)
                product_obj.opportunity_score = prod.get("opportunity_score", 80)
                product_obj.return_risk_default = prod.get("return_risk_default", "Medium (22%)")
                product_obj.target_audience = prod.get("target_audience")
                product_obj.recommended_courier = prod.get("recommended_courier")
                product_obj.description = prod.get("description")
                product_obj.seasonal_velocity = prod.get("seasonal_velocity")
        db.commit()

        # 3. Seed Store Inventory
        if db.query(StoreInventoryModel).count() == 0:
            for item in SAMPLE_STORE_INVENTORY:
                inv_obj = StoreInventoryModel(
                    sku=item["sku"],
                    title=item["title"],
                    category=item["category"],
                    stock=item["stock"],
                    unit_cost=item["unit_cost"],
                    selling_price=item["selling_price"],
                    monthly_velocity=int(item.get("monthly_velocity", item.get("daily_sales_velocity", 1.0) * 30)),
                    status=item.get("status", "Healthy / Star Item"),
                    event_affinity=item.get("event_affinity", item.get("event_relevance")),
                    days_of_inventory=int(item.get("days_of_inventory", item.get("days_of_supply", 30))),
                    action_recommendation=item.get("action_recommendation", "Monitor sales velocity against event peaks")
                )
                db.add(inv_obj)
            db.commit()

    finally:
        if own_session:
            db.close()


if __name__ == "__main__":
    print("Seeding database...")
    seed_initial_data()
    print("Database seeded successfully.")
