"""
backend/routers/intelligence.py
Tier 2 & Tier 3 Intelligence Modules:
- Pakistan City Demand & Risk Heatmap
- Smart Product Bundling Engine (AOV Booster & Courier Freight Absorber)
- Wholesale Sourcing Hubs Directory (Shah Alam, Faisalabad, Bolton Market, Wazirabad, Sialkot)
- Annual Pakistani E-Commerce Demand Curve
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from backend.gemini_service import GeminiServiceError, gemini_service
from backend.schemas import GeminiInsightRequest, GeminiInsightResponse
from mock.data import build_event_driven_demand_curve

router = APIRouter(prefix="/intelligence", tags=["Advanced Market Intelligence"])

# Pakistan Geographic Trade Hubs with Coordinates & Demand Indices
PAKISTAN_CITY_HEATMAP = [
    {"city": "Karachi", "lat": 24.8607, "lon": 67.0011, "tier": "Tier 1 Metro", "demand_index": 98, "avg_rto_pct": 14.2, "volume_share_pct": 34.0, "top_categories": ["Fast Fashion", "Gadgets", "Cosmetics"], "courier_hub": "Trax / Leopards / PostEx Main Gateways"},
    {"city": "Lahore", "lat": 31.5204, "lon": 74.3587, "tier": "Tier 1 Metro", "demand_index": 96, "avg_rto_pct": 12.8, "volume_share_pct": 28.0, "top_categories": ["Lawn & Festive Pret", "Footwear", "Home Living"], "courier_hub": "Shah Alam & Cargo Central"},
    {"city": "Islamabad", "lat": 33.6844, "lon": 73.0479, "tier": "Tier 1 Metro", "demand_index": 88, "avg_rto_pct": 11.5, "volume_share_pct": 12.0, "top_categories": ["Premium Electronics", "Branded Apparel", "Books"], "courier_hub": "TCS & Leopards Hub"},
    {"city": "Rawalpindi", "lat": 33.5651, "lon": 73.0169, "tier": "Tier 1 Metro", "demand_index": 84, "avg_rto_pct": 14.0, "volume_share_pct": 8.0, "top_categories": ["Electronics", "Pret", "Watches"], "courier_hub": "Raja Bazaar Regional Depot"},
    {"city": "Faisalabad", "lat": 31.4504, "lon": 73.1350, "tier": "Tier 2 Secondary", "demand_index": 80, "avg_rto_pct": 21.0, "volume_share_pct": 6.5, "top_categories": ["Unstitched Fabric", "Towels", "Yarn"], "courier_hub": "Clock Tower Wholesale Network"},
    {"city": "Multan", "lat": 30.1575, "lon": 71.5249, "tier": "Tier 2 Secondary", "demand_index": 72, "avg_rto_pct": 23.5, "volume_share_pct": 4.0, "top_categories": ["Embroidered Suits", "Bedwear", "Pottery"], "courier_hub": "Bosan Road Delivery Center"},
    {"city": "Peshawar", "lat": 34.0151, "lon": 71.5249, "tier": "Tier 2 Secondary", "demand_index": 74, "avg_rto_pct": 26.0, "volume_share_pct": 3.8, "top_categories": ["Dry Fruits", "Peshawari Chappal", "Crockery"], "courier_hub": "Karkhano Gate & G.T. Road"},
    {"city": "Gujranwala", "lat": 32.1877, "lon": 74.1945, "tier": "Tier 2 Secondary", "demand_index": 68, "avg_rto_pct": 22.0, "volume_share_pct": 2.5, "top_categories": ["Kitchen Utensils", "Sanitary", "Garments"], "courier_hub": "G.T. Road Transit Center"},
    {"city": "Sialkot", "lat": 32.4945, "lon": 74.5229, "tier": "Tier 2 Secondary", "demand_index": 65, "avg_rto_pct": 19.5, "volume_share_pct": 2.0, "top_categories": ["Sports Goods", "Leather Apparel", "Cutlery"], "courier_hub": "Export Zone Express Depot"},
    {"city": "Quetta", "lat": 30.1798, "lon": 66.9750, "tier": "Tier 3 Outstation", "demand_index": 52, "avg_rto_pct": 38.0, "volume_share_pct": 1.2, "top_categories": ["Balochi Shawls", "Dry Fruits", "Warm Wear"], "courier_hub": "Quetta Air & Railway Cargo"},
    {"city": "Hyderabad", "lat": 25.3960, "lon": 68.3578, "tier": "Tier 2 Secondary", "demand_index": 66, "avg_rto_pct": 24.0, "volume_share_pct": 2.2, "top_categories": ["Glass Bangles", "Ajrak Suits", "Sweets"], "courier_hub": "Resham Gali & Express Center"},
    {"city": "Sukkur", "lat": 27.7052, "lon": 68.8574, "tier": "Tier 3 Outstation", "demand_index": 48, "avg_rto_pct": 34.5, "volume_share_pct": 0.8, "top_categories": ["Dates", "Dresses", "Small Gadgets"], "courier_hub": "Upper Sindh Distribution"},
    {"city": "Muzaffarabad", "lat": 34.3700, "lon": 73.4711, "tier": "Tier 3 Outstation", "demand_index": 45, "avg_rto_pct": 42.0, "volume_share_pct": 0.6, "top_categories": ["Woolen Shawls", "Kashmiri Crafts"], "courier_hub": "AJK Hilly Transit Route"}
]

# Wholesale Sourcing Directory
WHOLESALE_HUBS = [
    {
        "hub_name": "Shah Alam Market (Shalmi)",
        "city": "Lahore",
        "primary_categories": ["Cosmetics & Skincare", "Small Electronics & Accessories", "Kitchen Tools", "Toys & Novelties"],
        "credit_terms": "Strictly Cash / Pay-and-Carry on initial 3 orders; 15-day credit after PKR 500k monthly volume.",
        "bargaining_tip": "Visit between 11 AM - 2 PM before peak retail rush. Quote bulk lots of 24-48 units for minimum wholesale rate.",
        "recommended_contact_channel": "Direct shop visits; obtain shopkeeper WhatsApp for reorder dispatch via Daewoo Cargo."
    },
    {
        "hub_name": "Faisalabad Cloth Market (Rail Bazaar & Clock Tower)",
        "city": "Faisalabad",
        "primary_categories": ["Unstitched Lawn (Digital Print / Embroidered)", "Men's Shalwar Kameez Fabric", "Bed Linens & Towels"],
        "credit_terms": "30% advance on printing runs, 70% against delivery bilti (cargo receipt).",
        "bargaining_tip": "Request 'thaan' pricing instead of cut pieces. Minimum efficient printing run is 500 meters per design.",
        "recommended_contact_channel": "Textile agents in Sootar Mandi and Karkhana Bazaar."
    },
    {
        "hub_name": "Bolton Market & Light House",
        "city": "Karachi",
        "primary_categories": ["Imported Chinese Goods", "Handbags & Wallets", "Watches & Mists", "Mobile Accessories"],
        "credit_terms": "Cash only; online transfer to shop owner Bank Alfalah / Meezan account upon physical carton count.",
        "bargaining_tip": "Carton-level pricing is 15-22% cheaper than open shelf pricing. Always verify master carton seals.",
        "recommended_contact_channel": "Wholesale traders in Denso Hall and Medicine/Cosmetics Lane."
    },
    {
        "hub_name": "Wazirabad Cutlery & Steel Cluster",
        "city": "Wazirabad / Gujranwala",
        "primary_categories": ["Butcher Knives", "BBQ Skewers & Grills", "Damascus Steel Blades", "Kitchen Scissors"],
        "credit_terms": "50% advance for customized brand etching; balance on shipment dispatch.",
        "bargaining_tip": "Peak manufacturing happens in Ramadan for Eid-ul-Adha. Pre-order in Shaban for best metallurgical quality.",
        "recommended_contact_channel": "Cutlery Manufacturers Association Wazirabad & direct factory workshops."
    },
    {
        "hub_name": "Raja Bazaar & Gakhar Plaza",
        "city": "Rawalpindi",
        "primary_categories": ["Electronic Accessories", "Wedding Trunks & Jewelry", "Shawls & Winter Woolens"],
        "credit_terms": "Cash on collection; local courier handoff available for Islamabad twin city sellers.",
        "bargaining_tip": "Shop upstairs in commercial plazas for true importers rather than ground floor retailers.",
        "recommended_contact_channel": "Market association WhatsApp groups."
    }
]

# Smart Product Bundling Combinations
SMART_BUNDLES = [
    {
        "bundle_id": "bundle-eid-glam",
        "name": "Eid Grand Festive Attire & Scent Combo",
        "target_event": "Eid-ul-Fitr Grand Fashion Surge",
        "components": [
            {"item": "Chiffon Embroidered 3-Piece Pret", "individual_price": 3800, "cogs": 1400},
            {"item": "Handcrafted Tilla Khussas", "individual_price": 2200, "cogs": 750},
            {"item": "Festive Body Mist (120ml)", "individual_price": 1200, "cogs": 350}
        ],
        "standalone_total_retail": 7200,
        "bundled_selling_price": 5950,
        "combined_cogs": 2500,
        "projected_margin_pct": 46.2,
        "strategic_benefit": "Absorbs courier freight in a single PKR 5,950 parcel. Reduces COD return risk from 24% to 11% because complete festive package buyers rarely refuse parcels."
    },
    {
        "bundle_id": "bundle-ramadan-kitchen",
        "name": "Iftar Fast-Prep Kitchen Power Bundle",
        "target_event": "Ramadan Mubarak & Pre-Eid Preparation",
        "components": [
            {"item": "Electric Vegetable Slicer & Samosa Chopper", "individual_price": 2600, "cogs": 950},
            {"item": "Oil Dispenser & Silicone Brush Duo", "individual_price": 950, "cogs": 280},
            {"item": "Non-Stick Jalebi / Pakora Fryer Basket", "individual_price": 1400, "cogs": 450}
        ],
        "standalone_total_retail": 4950,
        "bundled_selling_price": 3950,
        "combined_cogs": 1680,
        "projected_margin_pct": 44.8,
        "strategic_benefit": "High perceived utility for homemakers during Ramadan first-week rush. Boosts AOV by 52% over single chopper sales."
    },
    {
        "bundle_id": "bundle-bbq-master",
        "name": "Bari Eid Ultimate BBQ & Butcher Kit",
        "target_event": "Eid-ul-Adha (Bari Eid)",
        "components": [
            {"item": "Wazirabad Steel Meat Cleaver Knife", "individual_price": 1850, "cogs": 550},
            {"item": "Heavy Duty 12-Piece BBQ Skewers Set", "individual_price": 1250, "cogs": 380},
            {"item": "Portable Folding Charcoal Grill Box", "individual_price": 3200, "cogs": 1100}
        ],
        "standalone_total_retail": 6300,
        "bundled_selling_price": 4990,
        "combined_cogs": 2030,
        "projected_margin_pct": 48.1,
        "strategic_benefit": "Zero size-return risk. Target audience is male heads of household who prefer complete turnkey BBQ solutions."
    }
]


@router.get("/city-heatmap")
def get_city_heatmap_data():
    """Retrieve geographic coordinates, festive demand intensity, and COD risk across Pakistani trading hubs."""
    return {
        "total_hubs": len(PAKISTAN_CITY_HEATMAP),
        "heatmap_data": PAKISTAN_CITY_HEATMAP
    }


@router.get("/wholesale-hubs")
def get_wholesale_hubs():
    """Retrieve verified wholesale sourcing hubs across Pakistani manufacturing cities."""
    return WHOLESALE_HUBS


@router.get("/smart-bundles")
def get_smart_bundles():
    """Retrieve AI-curated product bundling packages engineered to absorb courier freight and reduce RTO."""
    return SMART_BUNDLES


@router.get("/demand-curve")
def get_annual_demand_curve():
    """Retrieve the current/upcoming-event-driven annual demand forecast."""
    return build_event_driven_demand_curve()


@router.post("/gemini-insight", response_model=GeminiInsightResponse)
def generate_gemini_insight(request: GeminiInsightRequest):
    """Generate an AI-assisted merchant insight through the configured Gemini API."""
    try:
        answer = gemini_service.generate_insight(request.question, request.context)
    except GeminiServiceError as exc:
        status_code = 503 if "not configured" in str(exc) else 502
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc

    return {"answer": answer, "model": gemini_service.model}
