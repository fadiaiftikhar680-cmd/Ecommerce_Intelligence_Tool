"""
utils/api_client.py
Service Client Layer (Layer 2) — Abstracted Service Interface for Streamlit Frontend.

Dual-Mode Architecture:
1. Live REST API Mode: Communicates with FastAPI backend (Layer 3) at http://127.0.0.1:8000/api.
2. Resilient Offline Mode: If the FastAPI server is starting up or offline, seamlessly falls back
   to local computation & database fixtures with zero UI disruption.
"""

import os
from datetime import date, datetime
from typing import List, Dict, Any, Optional
import requests
import pandas as pd
from mock.data import (
    EVENTS_DATA,
    WINNING_PRODUCTS_DATA,
    CITY_COD_TIERS,
    COURIER_BENCHMARKS,
    SAMPLE_STORE_INVENTORY,
    MONTHLY_DEMAND_CURVE
)
from backend.ml_model import ml_service

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/health"
TIMEOUT_SEC = 1.5


class ApiClient:
    """Service client providing market intelligence, pricing calculations, and COD risk models."""

    @staticmethod
    def _normalize_product(product: Dict[str, Any]) -> Dict[str, Any]:
        """Keep live database products compatible with the richer mock catalog UI."""
        normalized = dict(product)
        normalized.setdefault("wholesale_hub", normalized.get("sourcing_hub") or "N/A")
        normalized.setdefault("demand_trend", normalized.get("seasonal_velocity") or "Market trend unavailable")
        normalized.setdefault("search_volume_pk", "N/A")
        normalized.setdefault("competition_level", "Not assessed")
        normalized.setdefault("selling_points", [normalized.get("description") or "Review product positioning before launch."])
        return normalized

    @staticmethod
    def check_backend_health() -> Dict[str, Any]:
        """Check whether the FastAPI Layer 3 backend is online."""
        try:
            resp = requests.get(BACKEND_HEALTH_URL, timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "is_online": True,
                    "service": data.get("service", "FastAPI"),
                    "version": data.get("version", "2.0.0"),
                    "database": data.get("database", "SQLite (Active)"),
                    "ml_model": data.get("ml_model", "RandomForest (Loaded)")
                }
        except Exception:
            pass
        return {
            "is_online": False,
            "service": "Local High-Performance Engine (Fallback)",
            "version": "1.0-embedded",
            "database": "SQLite / Local Fixtures",
            "ml_model": "Embedded Scikit-learn Pipeline"
        }

    # -------------------------------------------------------------------------
    # 1. OVERVIEW & KPIS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_market_overview() -> Dict[str, Any]:
        """Fetch high-level overview metrics for the primary dashboard."""
        try:
            resp = requests.get(f"{API_BASE_URL}/overview", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Fallback local calculation using the same current/upcoming date rules as the API.
        today = date.today()
        current_events = []
        upcoming_events = []
        for raw_event in EVENTS_DATA:
            try:
                event = dict(raw_event)
                start = datetime.strptime(event["start_date"], "%Y-%m-%d").date()
                end = datetime.strptime(event["end_date"], "%Y-%m-%d").date()
                if end < today:
                    continue
                event["days_remaining"] = max(0, (start - today).days)
                if start <= today <= end:
                    current_events.append(event)
                else:
                    upcoming_events.append(event)
            except (KeyError, TypeError, ValueError):
                continue

        current_events.sort(key=lambda event: event["start_date"])
        upcoming_events.sort(key=lambda event: event["start_date"])
        current_live = current_events[0] if current_events else None
        next_event = upcoming_events[0] if upcoming_events else None
        seasonal_candidates = current_events + upcoming_events
        peak_event = max(
            seasonal_candidates,
            key=lambda event: event.get("demand_spike_pct", 0),
            default=None
        )
        total_products = len(WINNING_PRODUCTS_DATA)
        avg_opportunity = sum(p["opportunity_score"] for p in WINNING_PRODUCTS_DATA) / max(total_products, 1)
        all_cities = list(CITY_COD_TIERS.values())
        avg_market_rto = sum(c["avg_rto_pct"] for c in all_cities) / len(all_cities)

        return {
            "status": "success",
            "next_event": next_event,
            "current_live_event": current_live,
            "top_upcoming_events": upcoming_events[:3],
            "total_winning_products": total_products,
            "avg_opportunity_score": round(avg_opportunity, 1),
            "benchmark_market_rto_pct": round(avg_market_rto, 1),
            "active_season": (
                f"LIVE: {current_live['name']}" if current_live
                else f"Upcoming: {next_event['name']}" if next_event
                else "Pakistan E-Commerce Season"
            ),
            "seasonal_sale": {
                "current_event": current_live,
                "next_event": next_event,
                "peak_event": peak_event,
            },
            "demand_multiplier_peak": (
                f"+{peak_event.get('demand_spike_pct', 0)}%" if peak_event else "N/A"
            ),
            "urgent_actions_count": 3,
            "total_skus_tracked": len(SAMPLE_STORE_INVENTORY),
            "total_inventory_value_pkr": 680450.0,
            "total_assessments_logged": 12,
            "database_engine": "Embedded SQLite Fixtures"
        }

    @staticmethod
    def get_demand_curve() -> List[Dict[str, Any]]:
        """Retrieve 12-month demand trajectory."""
        try:
            resp = requests.get(f"{API_BASE_URL}/intelligence/demand-curve", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return MONTHLY_DEMAND_CURVE

    # -------------------------------------------------------------------------
    # 2. EVENT INTELLIGENCE
    # -------------------------------------------------------------------------
    @staticmethod
    def get_events(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all synchronized Hijri-Gregorian events with optional filtering."""
        try:
            params = {}
            if status_filter and status_filter != "All":
                params["status_filter"] = status_filter
            resp = requests.get(f"{API_BASE_URL}/events", params=params, timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        today = date.today()
        events = []
        for event in EVENTS_DATA:
            try:
                start = datetime.strptime(event["start_date"], "%Y-%m-%d").date()
                end = datetime.strptime(event["end_date"], "%Y-%m-%d").date()
                if end < today:
                    continue
                event = dict(event)
                event["days_remaining"] = max(0, (start - today).days)
                event["event_phase"] = "Current" if start <= today <= end else "Upcoming"
                events.append(event)
            except (KeyError, TypeError, ValueError):
                continue
        events.sort(key=lambda x: (x["event_phase"] != "Current", x["start_date"]))
        if status_filter and status_filter != "All":
            events = [e for e in events if status_filter.lower() in e["status"].lower()]
        return events

    @staticmethod
    def create_custom_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new custom event alert."""
        try:
            resp = requests.post(f"{API_BASE_URL}/events", json=event_data, timeout=TIMEOUT_SEC)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception:
            pass
        # Fallback append in memory
        event_data["id"] = f"custom-{len(EVENTS_DATA)+1}"
        EVENTS_DATA.append(event_data)
        return event_data

    # -------------------------------------------------------------------------
    # 3. WINNING PRODUCTS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_winning_products(
        event_id: Optional[str] = None,
        category: Optional[str] = None,
        min_opportunity: int = 0,
        sort_by: str = "Opportunity Score (High to Low)"
    ) -> List[Dict[str, Any]]:
        """Filter and rank winning products."""
        try:
            params = {
                "event_id": event_id or "All Events",
                "category": category or "All Categories",
                "min_opportunity": min_opportunity,
                "sort_by": sort_by
            }
            resp = requests.get(f"{API_BASE_URL}/products", params=params, timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return [ApiClient._normalize_product(product) for product in resp.json()]
        except Exception:
            pass

        products = []
        for p in WINNING_PRODUCTS_DATA:
            products.append(ApiClient._normalize_product(p))

        if event_id and event_id != "All Events":
            products = [p for p in products if p.get("event_id") == event_id]
        if category and category != "All Categories":
            products = [p for p in products if p.get("category") == category]
        products = [p for p in products if p.get("opportunity_score", 0) >= min_opportunity]

        if sort_by == "Opportunity Score (High to Low)":
            products.sort(key=lambda x: x["opportunity_score"], reverse=True)
        elif sort_by == "Wholesale Price (Low to High)":
            products.sort(key=lambda x: x["sourcing_cost"])
        elif sort_by == "Retail Price (High to Low)":
            products.sort(key=lambda x: x["suggested_retail_price"], reverse=True)
        elif sort_by == "Profit Margin %":
            products.sort(key=lambda x: x["profit_margin_delivered_pct"], reverse=True)

        return products

    @staticmethod
    def create_winning_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a custom product to catalog."""
        try:
            resp = requests.post(f"{API_BASE_URL}/products", json=product_data, timeout=TIMEOUT_SEC)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception:
            pass
        product_data["id"] = f"custom-{len(WINNING_PRODUCTS_DATA)+1}"
        WINNING_PRODUCTS_DATA.append(product_data)
        return product_data

    @staticmethod
    def get_categories() -> List[str]:
        """Return unique categories across winning products."""
        try:
            resp = requests.get(f"{API_BASE_URL}/products/categories", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        cats = sorted(list(set(p["category"] for p in WINNING_PRODUCTS_DATA)))
        return ["All Categories"] + cats

    # -------------------------------------------------------------------------
    # 4. SMART PRICING & MARGIN PROTECTOR
    # -------------------------------------------------------------------------
    @staticmethod
    def calculate_margin_and_pricing(
        sourcing_cost: float,
        selling_price: float,
        ad_cac: float,
        courier_fee: float,
        packaging_cost: float,
        return_rate_pct: float,
        return_courier_charge: float,
        discount_pct: float = 0.0
    ) -> Dict[str, Any]:
        """Simulate safe pricing, net margin, and reverse shipping drag."""
        payload = {
            "sourcing_cost": sourcing_cost,
            "selling_price": selling_price,
            "ad_cac": ad_cac,
            "courier_fee": courier_fee,
            "packaging_cost": packaging_cost,
            "return_rate_pct": return_rate_pct,
            "return_courier_charge": return_courier_charge,
            "discount_pct": discount_pct
        }
        try:
            resp = requests.post(f"{API_BASE_URL}/pricing/calculate", json=payload, timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Local calculation fallback
        discounted_price = selling_price * (1 - (discount_pct / 100.0))
        delivered_orders = max(0.0, 100.0 - return_rate_pct)
        returned_orders = float(return_rate_pct)

        total_revenue = delivered_orders * discounted_price
        cogs_delivered = delivered_orders * sourcing_cost
        packaging_total = 100.0 * packaging_cost
        ad_spend_total = 100.0 * ad_cac
        outbound_shipping = 100.0 * courier_fee
        reverse_shipping = returned_orders * return_courier_charge

        total_costs = cogs_delivered + packaging_total + ad_spend_total + outbound_shipping + reverse_shipping
        net_profit_total = total_revenue - total_costs
        net_profit_per_order = net_profit_total / 100.0
        net_margin_pct = (net_profit_total / total_revenue * 100.0) if total_revenue > 0 else 0.0

        ideal_profit_per_order = discounted_price - (sourcing_cost + packaging_cost + ad_cac + courier_fee)
        ideal_margin_pct = (ideal_profit_per_order / discounted_price * 100.0) if discounted_price > 0 else 0.0
        rto_drag = ideal_profit_per_order - net_profit_per_order

        breakeven_roas = (selling_price / (selling_price - sourcing_cost - courier_fee - packaging_cost)) if (selling_price - sourcing_cost - courier_fee - packaging_cost) > 0 else 9.99
        actual_roas = (total_revenue / ad_spend_total) if ad_spend_total > 0 else 0.0

        max_discount = 0.0
        for disc in range(0, 70):
            test_rev = delivered_orders * (selling_price * (1 - disc / 100.0))
            if (test_rev - total_costs) <= 0:
                max_discount = max(0.0, disc - 1.0)
                break
            max_discount = float(disc)

        if net_margin_pct >= 25.0:
            verdict = "HEALTHY & HIGHLY PROFITABLE"
            verdict_color = "#10B981"
        elif net_margin_pct >= 12.0:
            verdict = "MODERATE SAFE MARGIN"
            verdict_color = "#38BDF8"
        elif net_margin_pct > 0.0:
            verdict = "THIN MARGIN (HIGH RISK OF LOSS ON RETURNS)"
            verdict_color = "#F59E0B"
        else:
            verdict = "LOSS-MAKING UNIT ECONOMICS (DO NOT LAUNCH)"
            verdict_color = "#EF4444"

        break_even_selling_price = (total_costs / delivered_orders) if delivered_orders > 0 else selling_price
        rto_penalty_per_order = max(0.0, abs(rto_drag))
        breakdown = {
            "cogs": sourcing_cost,
            "ad_spend": ad_cac,
            "outbound_shipping": courier_fee,
            "packaging": packaging_cost,
            "reverse_shipping_drag": rto_penalty_per_order,
        }

        return {
            "discounted_price": round(discounted_price, 0),
            "total_revenue_per_100": round(total_revenue, 0),
            "total_costs_per_100": round(total_costs, 0),
            "net_profit_per_100": round(net_profit_total, 0),
            "net_profit_per_order": round(net_profit_per_order, 1),
            "net_margin_pct": round(net_margin_pct, 1),
            "ideal_profit_per_order": round(ideal_profit_per_order, 1),
            "ideal_margin_pct": round(ideal_margin_pct, 1),
            "rto_profit_drag_per_order": round(rto_drag, 1),
            "cogs_total": round(cogs_delivered, 0),
            "packaging_total": round(packaging_total, 0),
            "ad_spend_total": round(ad_spend_total, 0),
            "outbound_shipping_total": round(outbound_shipping, 0),
            "reverse_shipping_total": round(reverse_shipping, 0),
            "breakeven_roas": round(breakeven_roas, 2),
            "actual_simulated_roas": round(actual_roas, 2),
            "max_safe_discount_pct": round(max_discount, 0),
            "breakeven_selling_price": round(break_even_selling_price, 0),
            "delivered_orders_per_100": int(delivered_orders),
            "returned_orders_per_100": int(returned_orders),
            "rto_loss_penalty_per_order": round(rto_penalty_per_order, 1),
            "breakdown": breakdown,
            "verdict": verdict,
            "verdict_color": verdict_color,
            "status": verdict,
            "status_color": verdict_color,
            "max_allowable_discount_pct": round(max_discount, 0),
        }

    @staticmethod
    def save_pricing_scenario(scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a calculation scenario to database."""
        try:
            resp = requests.post(f"{API_BASE_URL}/pricing/save", json=scenario_data, timeout=TIMEOUT_SEC)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception:
            pass
        return {"status": "saved_locally", **scenario_data}

    @staticmethod
    def get_saved_scenarios() -> List[Dict[str, Any]]:
        """Fetch previously saved calculation scenarios."""
        try:
            resp = requests.get(f"{API_BASE_URL}/pricing/saved", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return []

    # -------------------------------------------------------------------------
    # 5. COD RETURN RISK PREDICTOR
    # -------------------------------------------------------------------------
    @staticmethod
    def predict_cod_risk(
        city: str,
        category: str,
        order_value: float,
        customer_type: str,
        address_type: str,
        courier: str,
        order_ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """Predict COD RTO risk using trained Scikit-learn ML model with automated WhatsApp script."""
        payload = {
            "city": city,
            "category": category,
            "order_value": order_value,
            "customer_type": customer_type,
            "address_type": address_type,
            "courier": courier,
            "order_ref": order_ref
        }
        try:
            resp = requests.post(f"{API_BASE_URL}/cod-risk/predict", json=payload, timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Direct call to embedded ML model
        return ml_service.predict_risk(
            city=city,
            category=category,
            order_value=order_value,
            customer_type=customer_type,
            address_type=address_type,
            courier=courier,
            order_ref=order_ref
        )

    @staticmethod
    def get_assessment_history() -> List[Dict[str, Any]]:
        """Retrieve recent COD risk audit records."""
        try:
            resp = requests.get(f"{API_BASE_URL}/cod-risk/history", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return []

    @staticmethod
    def get_city_benchmarks() -> pd.DataFrame:
        """Fetch city COD tiers and delivery SLAs."""
        try:
            resp = requests.get(f"{API_BASE_URL}/cod-risk/city-benchmarks", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                rows = resp.json()
                if rows:
                    frame = pd.DataFrame(rows).rename(columns={
                        "Avg RTO %": "Average COD RTO %",
                        "Delivery SLA": "Avg Delivery Days",
                    })
                    frame["Tier"] = frame["Tier"].map(
                        lambda value: f"Tier {value}" if str(value).isdigit() else value
                    )
                    frame["Avg Delivery Days"] = frame["Avg Delivery Days"].astype(str).str.replace(
                        " Days", "", regex=False
                    ).astype(float)
                    frame["Zone"] = frame["City"].map(
                        lambda city: CITY_COD_TIERS.get(city, {}).get("zone", "Unknown")
                    )
                    frame["Coverage Quality"] = frame["City"].map(
                        lambda city: CITY_COD_TIERS.get(city, {}).get("courier_coverage", "Unknown")
                    )
                    return frame
        except Exception:
            pass

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
        return pd.DataFrame(rows)

    @staticmethod
    def get_couriers() -> List[Dict[str, Any]]:
        """Fetch logistics partner tariffs and metrics."""
        try:
            resp = requests.get(f"{API_BASE_URL}/cod-risk/couriers", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return COURIER_BENCHMARKS

    # -------------------------------------------------------------------------
    # 6. STORE INVENTORY & DEAD STOCK
    # -------------------------------------------------------------------------
    @staticmethod
    def get_store_inventory() -> List[Dict[str, Any]]:
        """Fetch store inventory."""
        try:
            resp = requests.get(f"{API_BASE_URL}/inventory", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                normalized = []
                for item in resp.json():
                    item = dict(item)
                    monthly_velocity = float(item.get("monthly_velocity", 0) or 0)
                    daily_velocity = float(item.get("daily_sales_velocity", monthly_velocity / 30.0) or 0)
                    days_supply = item.get("days_of_supply", item.get("days_of_inventory", 0))
                    item["daily_sales_velocity"] = daily_velocity
                    item["days_of_supply"] = float(days_supply or 0)
                    normalized.append(item)
                return normalized
        except Exception:
            pass

        # Normalize sample inventory
        normalized = []
        for item in SAMPLE_STORE_INVENTORY:
            normalized.append({
                "id": item["sku"],
                "sku": item["sku"],
                "title": item["title"],
                "category": item["category"],
                "stock": item["stock"],
                "unit_cost": item["unit_cost"],
                "selling_price": item["selling_price"],
                "monthly_velocity": int(item.get("daily_sales_velocity", 1.0) * 30),
                "daily_sales_velocity": item.get("daily_sales_velocity", 1.0),
                "status": item["status"],
                "event_affinity": item.get("event_relevance", "All Seasons"),
                "days_of_inventory": item.get("days_of_supply", 30),
                "days_of_supply": item.get("days_of_supply", 30),
                "action_recommendation": "Monitor seasonal velocity against upcoming event."
            })
        return normalized

    @staticmethod
    def add_inventory_sku(sku_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a SKU to inventory."""
        try:
            resp = requests.post(f"{API_BASE_URL}/inventory", json=sku_data, timeout=TIMEOUT_SEC)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception:
            pass
        return sku_data

    @staticmethod
    def delete_inventory_sku(sku: str) -> bool:
        """Delete a SKU from inventory."""
        try:
            resp = requests.delete(f"{API_BASE_URL}/inventory/{sku}", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return True
        except Exception:
            pass
        return False

    @staticmethod
    def get_dead_stock_analysis() -> Dict[str, Any]:
        """Retrieve automated dead stock liquidation and flash-discount recommendations."""
        try:
            resp = requests.get(f"{API_BASE_URL}/inventory/dead-stock-analysis", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return {
            "dead_sku_count": 2,
            "total_units_locked": 390,
            "total_capital_locked_pkr": 466500.0,
            "salvage_at_cost_pkr": 466500.0,
            "liquidation_plan": []
        }

    # -------------------------------------------------------------------------
    # 7. ADVANCED INTELLIGENCE (Heatmap, Bundling, Wholesale Hubs)
    # -------------------------------------------------------------------------
    @staticmethod
    def get_city_heatmap() -> Dict[str, Any]:
        """Fetch Pakistan regional demand & COD return heatmap coordinates."""
        try:
            resp = requests.get(f"{API_BASE_URL}/intelligence/city-heatmap", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.routers.intelligence import PAKISTAN_CITY_HEATMAP
        return {"total_hubs": len(PAKISTAN_CITY_HEATMAP), "heatmap_data": PAKISTAN_CITY_HEATMAP}

    @staticmethod
    def get_smart_bundles() -> List[Dict[str, Any]]:
        """Fetch AI-curated product bundling packages."""
        try:
            resp = requests.get(f"{API_BASE_URL}/intelligence/smart-bundles", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.routers.intelligence import SMART_BUNDLES
        return SMART_BUNDLES

    @staticmethod
    def get_wholesale_hubs() -> List[Dict[str, Any]]:
        """Fetch verified wholesale sourcing hubs."""
        try:
            resp = requests.get(f"{API_BASE_URL}/intelligence/wholesale-hubs", timeout=TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.routers.intelligence import WHOLESALE_HUBS
        return WHOLESALE_HUBS
