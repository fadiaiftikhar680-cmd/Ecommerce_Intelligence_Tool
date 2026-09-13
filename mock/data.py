"""
mock/data.py
Pakistani E-Commerce Market Intelligence Mock Dataset
Contains realistic events, Hijri-Gregorian synchronization, winning products,
wholesale sourcing hubs, courier benchmarks, city COD tiers, and store inventory.
"""

from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. PAKISTAN E-COMMERCE EVENTS (Gregorian & Hijri Synchronized)
# -----------------------------------------------------------------------------
EVENTS_DATA = [
    {
        "id": "ramadan-2026",
        "name": "Ramadan Mubarak & Pre-Eid Preparation",
        "name_ur": "رمضان المبارک اور عید کی تیاری",
        "hijri_date": "1 Ramadan 1448 AH",
        "start_date": "2026-02-18",
        "end_date": "2026-03-20",
        "demand_spike_pct": 240,
        "peak_window": "First 15 days of Ramadan",
        "sourcing_cutoff": "2026-01-25",
        "courier_cutoff": "2026-03-14",
        "status": "Active Sourcing & Campaign Setup",
        "days_remaining": 22,
        "description": "Massive surge in kitchen gadgets, modest wear (Abayas/Hijabs), dates packaging, prayer mats, and early Eid unstitched fabrics.",
        "top_categories": ["Modest Wear & Abayas", "Kitchen Appliances (Choppers/Air Fryers)", "Islamic Lifestyle & Decor", "Pre-Eid Unstitched Fabrics"],
        "recommended_lead_time_days": 40,
        "historical_gmv_index": 92,
        "courier_notes": "Heavy congestion expected from 15th Ramadan onward. Move high-ticket items to air cargo or book early.",
        "seller_checklist": [
            "Finalize unstitched fabric dyeing & packaging at Faisalabad/Shah Alam hubs.",
            "Test Meta & TikTok ad creative angles before CPMs inflate by 45%.",
            "Set up automated WhatsApp confirmation for COD orders above PKR 3,500.",
            "Stock up on branded flyers and double-bubble courier pouches."
        ]
    },
    {
        "id": "eid-ul-fitr-2026",
        "name": "Eid-ul-Fitr Grand Fashion Surge",
        "name_ur": "عید الفطر گرینڈ فیشن سیزن",
        "hijri_date": "1 Shawwal 1448 AH",
        "start_date": "2026-03-20",
        "end_date": "2026-03-23",
        "demand_spike_pct": 320,
        "peak_window": "10-25 Ramadan (Peak dispatch frenzy)",
        "sourcing_cutoff": "2026-02-15",
        "courier_cutoff": "2026-03-15",
        "status": "High Urgency Alert (Cutoff in 25 days)",
        "days_remaining": 35,
        "description": "Highest annual e-commerce volume for festive apparel, traditional footwear (Khussas), kidswear, Eid jewelry, and ittar perfumes.",
        "top_categories": ["Women's Festive Pret & Lawn", "Men's Kurta & Shalwar Kameez", "Festive Footwear (Khussas)", "Attar & Perfumes", "Eid Gifts & Bangles"],
        "recommended_lead_time_days": 45,
        "historical_gmv_index": 100,
        "courier_notes": "Leopards, TCS, and Trax cut off deliveries 4-5 days prior to Eid day. Orders after cutoff will be refused/returned.",
        "seller_checklist": [
            "Stop advertising unstitched materials 12 days before Eid; switch strictly to Ready-to-Wear (Pret).",
            "Mark all product pages with guaranteed delivery dates.",
            "Staff extra customer service reps for tracking inquiries and address corrections."
        ]
    },
    {
        "id": "eid-ul-adha-2026",
        "name": "Eid-ul-Adha (Bari Eid)",
        "name_ur": "عید الاضحیٰ (بڑی عید)",
        "hijri_date": "10 Dhul-Hijjah 1448 AH",
        "start_date": "2026-05-27",
        "end_date": "2026-05-30",
        "demand_spike_pct": 180,
        "peak_window": "15 days prior to Eid-ul-Adha",
        "sourcing_cutoff": "2026-04-25",
        "courier_cutoff": "2026-05-22",
        "status": "Upcoming Planning",
        "days_remaining": 88,
        "description": "High demand for BBQ grills, skewers, meat cutting tools, butcher knives (Wazirabad steel), deep freezers accessories, and semi-formal menswear.",
        "top_categories": ["BBQ Sets & Kitchen Utensils", "Wazirabad Cutlery & Knives", "Men's Casual Kurta", "Meat Preservation & Sealers"],
        "recommended_lead_time_days": 35,
        "historical_gmv_index": 78,
        "courier_notes": "Expect courier delivery delays due to animal market logistics in major cities like Karachi, Lahore, and Rawalpindi.",
        "seller_checklist": [
            "Source steel knives directly from Wazirabad wholesale suppliers.",
            "Bundle BBQ skewers with portable grills for higher AOV.",
            "Highlight anti-rust and heavy-duty warranty in ad copy."
        ]
    },
    {
        "id": "azadi-sale-2026",
        "name": "14th August Azadi Mega Sale",
        "name_ur": "14 اگست یوم آزادی میگا سیل",
        "hijri_date": "Safar 1449 AH",
        "start_date": "2026-08-01",
        "end_date": "2026-08-14",
        "demand_spike_pct": 160,
        "peak_window": "1st to 12th August",
        "sourcing_cutoff": "2026-07-15",
        "courier_cutoff": "2026-08-10",
        "status": "Upcoming Planning",
        "days_remaining": 155,
        "description": "Patriotic merchandise, green/white apparel for kids and adults, national badges, car flag accessories, and summer clearance flash sales.",
        "top_categories": ["Green & White Festive Wear", "Kids Azadi Outfits & Badges", "Automobile & Bike Accessories", "Summer Clearance Fashion"],
        "recommended_lead_time_days": 30,
        "historical_gmv_index": 72,
        "courier_notes": "National holiday logistics freeze on 13-14th August.",
        "seller_checklist": [
            "Run bundle clearance to eliminate remaining summer lawn stock.",
            "Create fast-shipping flash sales on Daraz, Shopify, and TikTok Shop."
        ]
    },
    {
        "id": "blessed-friday-2026",
        "name": "Blessed Friday / 11.11 Mega Shopping Festival",
        "name_ur": "بلیسڈ فرائیڈے اور 11.11 شاپنگ فیسٹیول",
        "hijri_date": "Jumada al-Thani 1449 AH",
        "start_date": "2026-11-10",
        "end_date": "2026-11-30",
        "demand_spike_pct": 380,
        "peak_window": "11th November to 27th November",
        "sourcing_cutoff": "2026-10-10",
        "courier_cutoff": "2026-11-28",
        "status": "Long-Term Strategic",
        "days_remaining": 245,
        "description": "The biggest discounted shopping event of the year in Pakistan. Skyrocketing electronics, winter apparel, smart home gadgets, beauty & skincare.",
        "top_categories": ["Smart Electronics & Audio", "Winter Outerwear & Hoodies", "Skincare & Beauty Cosmetics", "Home & Kitchen Appliances"],
        "recommended_lead_time_days": 60,
        "historical_gmv_index": 100,
        "courier_notes": "Severe COD courier backlogs across Trax, TCS, and Leopards. High return risk if delivery takes over 6 days.",
        "seller_checklist": [
            "Negotiate volume-based SLA rates with at least 2 courier companies.",
            "Pre-pack fast-moving stock to dispatch within 6 hours of order receipt."
        ]
    },
    {
        "id": "wedding-season-2026",
        "name": "Winter Wedding & Festive Gala (Shaadi Season)",
        "name_ur": "موسم سرما شادی سیزن",
        "hijri_date": "Rajab - Sha'ban 1448 AH",
        "start_date": "2026-11-15",
        "end_date": "2027-02-15",
        "demand_spike_pct": 290,
        "peak_window": "December to January continuous peak",
        "sourcing_cutoff": "2026-10-25",
        "courier_cutoff": "Rolling daily",
        "status": "Seasonal Constant",
        "days_remaining": 250,
        "description": "High average order values (AOV). Heavy formal wedding wear, velvet shawls, gold-plated jewelry sets, bridal makeup vanity cases, creator ring lights.",
        "top_categories": ["Chiffon & Velvet Formal Wear", "Bridal Jewelry Sets", "Groom Footwear & Sherwani Accessories", "Content Creator Ring Lights"],
        "recommended_lead_time_days": 45,
        "historical_gmv_index": 88,
        "courier_notes": "High-value COD parcel safety is paramount. Prefer couriers with insured cash collection.",
        "seller_checklist": [
            "Enforce partial advance payment (PKR 500-1000) on customized bridal orders.",
            "Inspect velvet and embroidered borders for defects before packaging."
        ]
    }
]

# -----------------------------------------------------------------------------
# 2. WINNING PRODUCTS CATALOG (Pakistan Market Specific)
# -----------------------------------------------------------------------------
WINNING_PRODUCTS_DATA = [
    {
        "id": "prod-001",
        "name": "3-Piece Luxury Embroidered Lawn Collection (Unstitched)",
        "name_ur": "تین پیس کڑھائی والا لگژری لان سوٹ",
        "category": "Women's Fashion",
        "event_id": "ramadan-2026",
        "wholesale_hub": "Faisalabad Textile Market / Shah Alam Market, Lahore",
        "sourcing_cost": 1850,
        "suggested_retail_price": 3899,
        "typical_ad_cac": 650,
        "typical_courier_fee": 260,
        "packaging_cost": 50,
        "return_risk_default": "Medium",
        "opportunity_score": 96,
        "demand_trend": "+210% vs last month",
        "competition_level": "High",
        "search_volume_pk": "180K/month",
        "profit_margin_delivered_pct": 28.0,
        "selling_points": [
            "Heavy embroidered neckline with digital printed chiffon dupatta",
            "Direct factory sourcing price vs branded retail (Khaadi/Sapphire) at PKR 8,000+",
            "Fast dispatch ready"
        ],
        "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&q=80"
    },
    {
        "id": "prod-002",
        "name": "4-in-1 Rechargeable Handheld Electric Vegetable & Meat Chopper",
        "name_ur": "چار ان ون ریچارج ایبل الیکٹرک سبزی اور گوشت چوپر",
        "category": "Kitchen & Ramadan Prep",
        "event_id": "ramadan-2026",
        "wholesale_hub": "Bolton Market, Karachi / Hall Road, Lahore",
        "sourcing_cost": 880,
        "suggested_retail_price": 2350,
        "typical_ad_cac": 480,
        "typical_courier_fee": 250,
        "packaging_cost": 60,
        "return_risk_default": "Low",
        "opportunity_score": 94,
        "demand_trend": "+340% seasonal surge",
        "competition_level": "Medium",
        "search_volume_pk": "95K/month",
        "profit_margin_delivered_pct": 29.0,
        "selling_points": [
            "Iftar & Sehri fast meal prep in under 30 seconds",
            "Rechargeable USB-C motor, no load-shedding interruption",
            "High perceived value for online video ads on TikTok & Reels"
        ],
        "image_url": "https://images.unsplash.com/photo-1588854337236-6889d631faa8?w=600&q=80"
    },
    {
        "id": "prod-003",
        "name": "Men's Premium Wash & Wear Kurta Pajama (Eid Edition)",
        "name_ur": "مردانہ واش اینڈ ویئر کرتا پاجامہ (عید ایڈیشن)",
        "category": "Men's Apparel",
        "event_id": "eid-ul-fitr-2026",
        "wholesale_hub": "Raja Bazaar, Rawalpindi / Shah Alam, Lahore",
        "sourcing_cost": 1350,
        "suggested_retail_price": 3150,
        "typical_ad_cac": 520,
        "typical_courier_fee": 250,
        "packaging_cost": 45,
        "return_risk_default": "Medium",
        "opportunity_score": 91,
        "demand_trend": "+185% surge",
        "competition_level": "High",
        "search_volume_pk": "120K/month",
        "profit_margin_delivered_pct": 31.0,
        "selling_points": [
            "Wrinkle-resistant fabric ideal for summer Eid prayers",
            "Metallic studs and subtle embroidery on collar",
            "Standard Pakistani sizes (S, M, L, XL) with clear size chart"
        ],
        "image_url": "https://images.unsplash.com/photo-1617127365659-c47fa864d8bc?w=600&q=80"
    },
    {
        "id": "prod-004",
        "name": "Arabic Royal Oudh & White Musk Concentrated Perfume Oil (12ml)",
        "name_ur": "عربی رائل عود اور وائٹ مسک پرفیوم آئل",
        "category": "Perfumes & Lifestyle",
        "event_id": "ramadan-2026",
        "wholesale_hub": "Karkhano Market, Peshawar / Bolton Market, Karachi",
        "sourcing_cost": 550,
        "suggested_retail_price": 1899,
        "typical_ad_cac": 380,
        "typical_courier_fee": 220,
        "packaging_cost": 50,
        "return_risk_default": "Low",
        "opportunity_score": 92,
        "demand_trend": "+160% seasonal spike",
        "competition_level": "Low",
        "search_volume_pk": "65K/month",
        "profit_margin_delivered_pct": 36.8,
        "selling_points": [
            "100% Alcohol-Free Attar, ideal for Taraweeh & Eid prayers",
            "Long-lasting 18+ hours scent projection",
            "Luxury crystal bottle presentation in velvet pouch"
        ],
        "image_url": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=600&q=80"
    },
    {
        "id": "prod-005",
        "name": "Warm LED Ramadan & Eid Crescent Moon Fairy Light Curtain (3M)",
        "name_ur": "رمضان و عید ہلال چاند ایل ای ڈی فیری لائٹس",
        "category": "Home Decor & Festive",
        "event_id": "ramadan-2026",
        "wholesale_hub": "Hall Road, Lahore / Denso Hall, Karachi",
        "sourcing_cost": 650,
        "suggested_retail_price": 1950,
        "typical_ad_cac": 420,
        "typical_courier_fee": 230,
        "packaging_cost": 40,
        "return_risk_default": "Low",
        "opportunity_score": 89,
        "demand_trend": "+290% spike",
        "competition_level": "Medium",
        "search_volume_pk": "78K/month",
        "profit_margin_delivered_pct": 31.3,
        "selling_points": [
            "Transform home & drawing room for Ramadan Iftar hosting",
            "Energy-efficient low wattage LED",
            "High video visual appeal on Instagram story promotions"
        ],
        "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=600&q=80"
    },
    {
        "id": "prod-006",
        "name": "Handmade Multani Tilla Embroidered Velvet Khussa",
        "name_ur": "ہاتھ سے تیار کردہ ملتانی تلا کڑھائی دار ویلویٹ کھسہ",
        "category": "Festive Footwear",
        "event_id": "eid-ul-fitr-2026",
        "wholesale_hub": "Gole Market, Faisalabad / Mochi Gate, Lahore",
        "sourcing_cost": 920,
        "suggested_retail_price": 2499,
        "typical_ad_cac": 550,
        "typical_courier_fee": 240,
        "packaging_cost": 45,
        "return_risk_default": "High",
        "opportunity_score": 84,
        "demand_trend": "+175% surge",
        "competition_level": "Medium",
        "search_volume_pk": "82K/month",
        "profit_margin_delivered_pct": 29.8,
        "selling_points": [
            "Cushioned sole for high comfort during Eid gatherings",
            "Authentic handmade zari/tilla work",
            "High return risk due to shoe sizing — size exchange policy required"
        ],
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&q=80"
    },
    {
        "id": "prod-007",
        "name": "Heavy Duty Smokeless Foldable Charcoal BBQ Grill with 12 Skewers",
        "name_ur": "فولڈ ایبل چارکول بی بی کیو گرل اور سیخیں",
        "category": "Eid-ul-Adha Special",
        "event_id": "eid-ul-adha-2026",
        "wholesale_hub": "Gujranwala Metal Works / Shah Alam, Lahore",
        "sourcing_cost": 2100,
        "suggested_retail_price": 4650,
        "typical_ad_cac": 750,
        "typical_courier_fee": 380,
        "packaging_cost": 90,
        "return_risk_default": "Medium",
        "opportunity_score": 88,
        "demand_trend": "+310% seasonal demand",
        "competition_level": "Low",
        "search_volume_pk": "70K/month",
        "profit_margin_delivered_pct": 28.6,
        "selling_points": [
            "Compact folding design for roof & courtyard BBQ parties",
            "Stainless steel rust-resistant body",
            "High basket value (AOV) with bundling potential"
        ],
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80"
    },
    {
        "id": "prod-008",
        "name": "12-Inch Dual Light Studio Ring Light with 7ft Heavy Metal Tripod",
        "name_ur": "12 انچ اسٹوڈیو رنگ لائٹ مع 7 فٹ ٹرائی پوڈ",
        "category": "Electronics & Content Creators",
        "event_id": "wedding-season-2026",
        "wholesale_hub": "Hall Road, Lahore / Saddar Electronic Market, Karachi",
        "sourcing_cost": 1450,
        "suggested_retail_price": 3299,
        "typical_ad_cac": 590,
        "typical_courier_fee": 320,
        "packaging_cost": 75,
        "return_risk_default": "Medium",
        "opportunity_score": 87,
        "demand_trend": "+140% steady growth",
        "competition_level": "High",
        "search_volume_pk": "110K/month",
        "profit_margin_delivered_pct": 26.2,
        "selling_points": [
            "Must-have for wedding makeup artists and social media creators",
            "3 color light modes with dimmable remote controller",
            "Universal mobile holder"
        ],
        "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&q=80"
    }
]

# -----------------------------------------------------------------------------
# 3. CITY & REGIONAL COD RISK TIERS (Pakistan Market)
# -----------------------------------------------------------------------------
CITY_COD_TIERS = {
    "Karachi": {"tier": 1, "zone": "South Metros", "avg_rto_pct": 14.5, "avg_delivery_days": 2.1, "courier_coverage": "Excellent"},
    "Lahore": {"tier": 1, "zone": "Central Punjab", "avg_rto_pct": 13.8, "avg_delivery_days": 1.9, "courier_coverage": "Excellent"},
    "Islamabad": {"tier": 1, "zone": "Capital Territory", "avg_rto_pct": 11.2, "avg_delivery_days": 1.8, "courier_coverage": "Excellent"},
    "Rawalpindi": {"tier": 1, "zone": "North Punjab", "avg_rto_pct": 12.9, "avg_delivery_days": 2.0, "courier_coverage": "Excellent"},
    
    "Faisalabad": {"tier": 2, "zone": "Central Punjab", "avg_rto_pct": 19.5, "avg_delivery_days": 2.6, "courier_coverage": "Good"},
    "Multan": {"tier": 2, "zone": "South Punjab", "avg_rto_pct": 21.0, "avg_delivery_days": 2.8, "courier_coverage": "Good"},
    "Peshawar": {"tier": 2, "zone": "KPK Urban", "avg_rto_pct": 22.8, "avg_delivery_days": 3.0, "courier_coverage": "Good"},
    "Sialkot": {"tier": 2, "zone": "North Punjab", "avg_rto_pct": 18.2, "avg_delivery_days": 2.4, "courier_coverage": "Good"},
    "Gujranwala": {"tier": 2, "zone": "Central Punjab", "avg_rto_pct": 20.4, "avg_delivery_days": 2.5, "courier_coverage": "Good"},
    "Hyderabad": {"tier": 2, "zone": "Sindh Urban", "avg_rto_pct": 23.1, "avg_delivery_days": 2.7, "courier_coverage": "Good"},
    "Quetta": {"tier": 2, "zone": "Balochistan Urban", "avg_rto_pct": 27.5, "avg_delivery_days": 4.2, "courier_coverage": "Moderate"},
    
    "Interior Sindh (Sukkur, Larkana, Mirpurkhas)": {"tier": 3, "zone": "Rural / Distant", "avg_rto_pct": 42.0, "avg_delivery_days": 4.8, "courier_coverage": "Low/Agent Delivery"},
    "South Punjab Outskirts (Muzaffargarh, D.G. Khan, Rajanpur)": {"tier": 3, "zone": "Rural / Distant", "avg_rto_pct": 39.5, "avg_delivery_days": 4.5, "courier_coverage": "Moderate"},
    "Interior KPK (Bannu, Swat, D.I. Khan)": {"tier": 3, "zone": "Rural / Distant", "avg_rto_pct": 44.2, "avg_delivery_days": 5.1, "courier_coverage": "Low/Outskirts"},
    "Balochistan Distant (Turbat, Khuzdar, Gwadar)": {"tier": 3, "zone": "Remote Outskirts", "avg_rto_pct": 51.0, "avg_delivery_days": 6.2, "courier_coverage": "Poor"}
}

# -----------------------------------------------------------------------------
# 4. COURIER BENCHMARKS (Pakistani Logistics Partners)
# -----------------------------------------------------------------------------
COURIER_BENCHMARKS = [
    {
        "name": "Trax Logistics",
        "base_rate_pkr": 240,
        "cod_fee_pct": 2.5,
        "avg_sla_days": 2.8,
        "return_charge_pkr": 160,
        "best_for": "Metros & Tier 2 Cities, fast COD portal disbursement",
        "rating": 4.2
    },
    {
        "name": "PostEx",
        "base_rate_pkr": 235,
        "cod_fee_pct": 2.2,
        "avg_sla_days": 2.6,
        "return_charge_pkr": 150,
        "best_for": "Instant COD financing, Shopify/WooCommerce fast plugin",
        "rating": 4.4
    },
    {
        "name": "Leopards Courier",
        "base_rate_pkr": 270,
        "cod_fee_pct": 3.0,
        "avg_sla_days": 2.9,
        "return_charge_pkr": 180,
        "best_for": "Massive deep coverage in Tier 3 towns & rural areas",
        "rating": 4.0
    },
    {
        "name": "TCS Express",
        "base_rate_pkr": 320,
        "cod_fee_pct": 3.0,
        "avg_sla_days": 2.1,
        "return_charge_pkr": 210,
        "best_for": "High-ticket luxury apparel, fastest metropolitan delivery",
        "rating": 4.5
    },
    {
        "name": "Call Courier",
        "base_rate_pkr": 230,
        "cod_fee_pct": 2.5,
        "avg_sla_days": 3.1,
        "return_charge_pkr": 150,
        "best_for": "Budget bulk apparel dispatches across Punjab",
        "rating": 3.9
    }
]

# -----------------------------------------------------------------------------
# 5. SAMPLE STORE INVENTORY DATA (Pakistani Store Simulation)
# -----------------------------------------------------------------------------
SAMPLE_STORE_INVENTORY = [
    {
        "sku": "SKU-LAWN-01",
        "title": "Embroidered Digital Lawn Kurti - Peach",
        "category": "Women's Fashion",
        "stock": 140,
        "unit_cost": 1100,
        "selling_price": 2450,
        "daily_sales_velocity": 8.5,
        "days_of_supply": 16,
        "event_relevance": "ramadan-2026",
        "status": "Event Star (Scale Ads)"
    },
    {
        "sku": "SKU-CHOP-02",
        "title": "USB Rechargeable Mini Food Chopper 250ml",
        "category": "Kitchen",
        "stock": 18,
        "unit_cost": 750,
        "selling_price": 1999,
        "daily_sales_velocity": 4.2,
        "days_of_supply": 4,
        "event_relevance": "ramadan-2026",
        "status": "Stockout Imminent (Reorder Now)"
    },
    {
        "sku": "SKU-ATTAR-03",
        "title": "Dehn Al Oudh Concentrated Ittar 6ml",
        "category": "Perfumes",
        "stock": 85,
        "unit_cost": 450,
        "selling_price": 1499,
        "daily_sales_velocity": 3.1,
        "days_of_supply": 27,
        "event_relevance": "ramadan-2026",
        "status": "Healthy Stock"
    },
    {
        "sku": "SKU-KURTA-04",
        "title": "Men Cotton Silk Semi-Formal Kurta - Black",
        "category": "Men's Apparel",
        "stock": 65,
        "unit_cost": 1250,
        "selling_price": 2899,
        "daily_sales_velocity": 2.8,
        "days_of_supply": 23,
        "event_relevance": "eid-ul-fitr-2026",
        "status": "Healthy Stock"
    },
    {
        "sku": "SKU-KHUSSA-05",
        "title": "Velvet Zari Embroidered Golden Khussa (Size 38)",
        "category": "Footwear",
        "stock": 210,
        "unit_cost": 850,
        "selling_price": 2200,
        "daily_sales_velocity": 0.6,
        "days_of_supply": 350,
        "event_relevance": "eid-ul-fitr-2026",
        "status": "Dead Stock Risk (Liquidate/Bundle)"
    },
    {
        "sku": "SKU-SHAWL-06",
        "title": "Heavy Kashmiri Wool Embroidered Shawl - Maroon",
        "category": "Winter Fashion",
        "stock": 180,
        "unit_cost": 1600,
        "selling_price": 3800,
        "daily_sales_velocity": 0.4,
        "days_of_supply": 450,
        "event_relevance": "wedding-season-2026",
        "status": "Dead Stock (Tied Up Capital PKR 288,000)"
    },
    {
        "sku": "SKU-RING-07",
        "title": "10-inch LED Selfie Ring Light with Table Stand",
        "category": "Electronics",
        "stock": 42,
        "unit_cost": 950,
        "selling_price": 2350,
        "daily_sales_velocity": 2.1,
        "days_of_supply": 20,
        "event_relevance": "wedding-season-2026",
        "status": "Healthy Stock"
    },
    {
        "sku": "SKU-JEWEL-08",
        "title": "Kundan Choker Necklace Set with Jhumkas",
        "category": "Jewelry",
        "stock": 95,
        "unit_cost": 580,
        "selling_price": 1750,
        "daily_sales_velocity": 1.2,
        "days_of_supply": 79,
        "event_relevance": "wedding-season-2026",
        "status": "Slow Mover (Bundle Candidate)"
    }
]

# -----------------------------------------------------------------------------
# 6. HISTORICAL REVENUE SPIKE TREND (12-Month Curve)
# -----------------------------------------------------------------------------
MONTHLY_DEMAND_CURVE = [
    {"month": "Jan", "event": "Winter Clearance / Weddings", "demand_index": 78, "typical_gmv_multiplier": "1.3x"},
    {"month": "Feb", "event": "Pre-Ramadan Sourcing & Buildup", "demand_index": 85, "typical_gmv_multiplier": "1.6x"},
    {"month": "Mar", "event": "Ramadan Mubarak & Pre-Eid Peak", "demand_index": 100, "typical_gmv_multiplier": "3.2x"},
    {"month": "Apr", "event": "Eid-ul-Fitr Celebrations & Post-Eid", "demand_index": 65, "typical_gmv_multiplier": "1.2x"},
    {"month": "May", "event": "Eid-ul-Adha Pre-Booking Surge", "demand_index": 82, "typical_gmv_multiplier": "1.8x"},
    {"month": "Jun", "event": "Post-Adha Lull & Mid-Summer Lawn", "demand_index": 52, "typical_gmv_multiplier": "0.9x"},
    {"month": "Jul", "event": "Monsoon & Pre-Azadi Sourcing", "demand_index": 58, "typical_gmv_multiplier": "1.0x"},
    {"month": "Aug", "event": "14th August Azadi Mega Sales", "demand_index": 75, "typical_gmv_multiplier": "1.6x"},
    {"month": "Sep", "event": "Pre-Winter Collection Launch", "demand_index": 62, "typical_gmv_multiplier": "1.1x"},
    {"month": "Oct", "event": "Shaadi Season & Pre-11.11 Prep", "demand_index": 79, "typical_gmv_multiplier": "1.5x"},
    {"month": "Nov", "event": "Blessed Friday & 11.11 Megasale", "demand_index": 98, "typical_gmv_multiplier": "3.8x"},
    {"month": "Dec", "event": "Peak Winter Shaadi & Year-End Sale", "demand_index": 88, "typical_gmv_multiplier": "2.2x"}
]
