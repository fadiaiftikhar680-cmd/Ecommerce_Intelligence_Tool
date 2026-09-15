"""
mock/data.py
Pakistani E-Commerce Market Intelligence Mock Dataset
Contains realistic events, Hijri-Gregorian synchronization, winning products,
wholesale sourcing hubs, courier benchmarks, city COD tiers, and store inventory.

Last Updated: September 2026 — Events are CURRENT & FUTURE only.
Past events (Ramadan 2026, Eid-ul-Fitr 2026, Eid-ul-Adha 2026, 14th Aug 2026)
have been analyzed and used to forecast the upcoming demand calendar.
"""

from datetime import datetime, timedelta, date

# Helper: auto-compute days remaining from today
def _days_left(date_str: str) -> int:
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        delta = (target - date.today()).days
        return max(0, delta)
    except Exception:
        return 0

# -----------------------------------------------------------------------------
# 1. PAKISTAN E-COMMERCE EVENTS — CURRENT & UPCOMING ONLY
#    (Based on today: September 14, 2026)
#    Analysis of past peaks: Ramadan +240%, Eid-ul-Fitr +320%, Eid-ul-Adha +180%,
#    14th August +160% — these inform the forecasts below.
# -----------------------------------------------------------------------------
_EVENTS_RAW = [
    # ── ✅ ACTIVE NOW ──────────────────────────────────────────────────
    {
        "id": "pre-winter-launch-2026",
        "name": "Pre-Winter Collection Launch 🧥",
        "name_ur": "سردیوں کی نئی کلیکشن لانچ",
        "hijri_date": "Rabi al-Awwal 1448 AH",
        "start_date": "2026-09-01",
        "end_date": "2026-09-30",
        "demand_spike_pct": 110,
        "peak_window": "Mid-September to End of September 2026",
        "sourcing_cutoff": "2026-08-20",
        "courier_cutoff": "2026-09-28",
        "status": "Active Sourcing",
        "description": (
            "📊 Past Analysis → Sep is historically a 1.1x GMV month. Buyers begin exploring "
            "winter knitwear, shawls, and light jackets. Smart sellers use Sep to build inventory "
            "and launch awareness content before the Oct-Nov mega-peak.\n\n"
            "🔮 Current Opportunity: List winter basics (hoodies, light shawls, warm socks bundles). "
            "TikTok UGC content with 'first winter haul' hooks perform 2x better this month."
        ),
        "top_categories": [
            "Light Knitwear & Hoodies",
            "Ladies Winter Shawls (Pashmina style)",
            "Kids Warm Fleece Sets",
            "Men's Sweatshirts & Joggers"
        ],
        "recommended_lead_time_days": 20,
        "historical_gmv_index": 62,
        "courier_notes": "Normal courier operations. Good window to negotiate SLA rates before festive backlogs.",
        "seller_checklist": [
            "List winter knitwear & hoodies NOW — buyers begin searching from mid-Sep.",
            "Create size-chart videos for men's sweatshirts (high return risk from wrong sizes).",
            "Set up retargeting audiences on Meta — cheaper CPMs before Oct inflation.",
            "Negotiate courier volume deals before Blessed Friday congestion begins."
        ]
    },
    # ── 📅 UPCOMING — HIGH PRIORITY ────────────────────────────────────
    {
        "id": "shaadi-season-oct-2026",
        "name": "Shaadi Season Kick-off — October Peak 💍",
        "name_ur": "شادی سیزن اکتوبر 2026",
        "hijri_date": "Rabi al-Thani 1448 AH",
        "start_date": "2026-10-01",
        "end_date": "2026-10-31",
        "demand_spike_pct": 185,
        "peak_window": "1st October to 31st October 2026",
        "sourcing_cutoff": "2026-09-10",
        "courier_cutoff": "2026-10-28",
        "status": "Upcoming Planning",
        "description": (
            "📊 Past Analysis → Wedding season has been a 1.5x GMV multiplier historically. "
            "October marks the start of the 5-month shaadi peak (Oct–Feb). Past Eid-ul-Fitr data "
            "showed +320% on festive apparel — wedding season follows with sustained 185% spikes.\n\n"
            "🔮 Forecast: Formal chiffon suits, bridal jewelry, mehndi accessories, and groom sherwanis "
            "will dominate. AOV (Average Order Value) is highest in this season — PKR 4,000–12,000 range."
        ),
        "top_categories": [
            "Bridal & Mehndi Formal Wear",
            "Gold-Plated Jewelry Sets",
            "Groom Sherwani & Accessories",
            "Mehndi Decor & Dholki Accessories",
            "Makeup Vanity Cases & Beauty Kits"
        ],
        "recommended_lead_time_days": 25,
        "historical_gmv_index": 79,
        "courier_notes": "High-value COD parcels. Use TCS or PostEx for insured delivery above PKR 5,000.",
        "seller_checklist": [
            "Source embroidered formal wear from Faisalabad / Gujranwala textile markets NOW.",
            "Enforce PKR 500–1,000 advance on custom bridal orders to reduce RTO risk.",
            "Run 'wedding haul' content on TikTok & Instagram Reels for max organic reach.",
            "Bundle mehndi accessories (cones + holders + decor) for 35% higher AOV."
        ]
    },
    {
        "id": "pre-1111-sourcing-2026",
        "name": "11.11 Pre-Sourcing & Inventory Build Window ⚡",
        "name_ur": "11.11 سورسنگ اور اسٹاک بلڈ ونڈو",
        "hijri_date": "Jumada al-Awwal 1448 AH",
        "start_date": "2026-10-01",
        "end_date": "2026-10-10",
        "demand_spike_pct": 75,
        "peak_window": "1st October to 10th October 2026 (SOURCING DEADLINE)",
        "sourcing_cutoff": "2026-10-10",
        "courier_cutoff": "N/A",
        "status": "High Urgency",
        "description": (
            "📊 Past Analysis → Blessed Friday 2025 saw +380% demand surge — the highest in Pakistan's "
            "e-commerce history. Sellers who sourced 45+ days in advance captured 3x more orders. "
            "Those who missed the cutoff ran out of stock by Day 2 of the festival.\n\n"
            "🔮 ACTION REQUIRED: October 1–10 is your LAST WINDOW to wholesale source for 11.11 Mega Sale. "
            "Electronics, skincare, winter wear, and home appliances must be in your warehouse by Oct 15."
        ),
        "top_categories": [
            "Smart Electronics (Earbuds, Power Banks, Smartwatches)",
            "Winter Outerwear (Puffer Jackets, Hoodies, Fleece)",
            "Skincare & Beauty Combos",
            "Home & Kitchen Appliances"
        ],
        "recommended_lead_time_days": 45,
        "historical_gmv_index": 95,
        "courier_notes": "Pre-negotiate bulk SLA with Trax / PostEx before October 15 to lock discounted rates.",
        "seller_checklist": [
            "⚠️ DEADLINE: Complete wholesale sourcing by October 10, 2026.",
            "Order 40-60% more stock than your normal monthly volume for 11.11.",
            "Prepare product listings, creatives, and TikTok ads in October for Nov launch.",
            "Set up Daraz flash deal submissions & Shopify discount codes in advance."
        ]
    },
    {
        "id": "blessed-friday-1111-2026",
        "name": "Blessed Friday & 11.11 Mega Shopping Festival 🛍️",
        "name_ur": "بلیسڈ فرائیڈے اور 11.11 شاپنگ فیسٹیول",
        "hijri_date": "Jumada al-Thani 1448 AH",
        "start_date": "2026-11-10",
        "end_date": "2026-11-28",
        "demand_spike_pct": 380,
        "peak_window": "11th November to 28th November 2026",
        "sourcing_cutoff": "2026-10-10",
        "courier_cutoff": "2026-11-26",
        "status": "Upcoming Planning",
        "description": (
            "📊 Past Analysis → Pakistan's biggest e-commerce event. In 2025 Blessed Friday: "
            "+380% sales volume, Daraz reported 3M+ orders in 24 hours. Electronics & winter apparel "
            "were the #1 and #2 categories. Sellers with pre-packed stock shipped 6x faster.\n\n"
            "🔮 2026 Forecast: Expect even higher volumes with TikTok Shop now mainstream. "
            "Budget-friendly bundles (PKR 999–1,999) will outperform luxury items. "
            "COD confirmation via WhatsApp bot is critical to reduce fake orders."
        ),
        "top_categories": [
            "Smart Electronics & TWS Earbuds",
            "Winter Outerwear & Puffer Jackets",
            "Skincare & Whitening Serums",
            "Home Appliances (Air Fryers, Heaters)",
            "Kids Winter Clothing Sets"
        ],
        "recommended_lead_time_days": 60,
        "historical_gmv_index": 100,
        "courier_notes": "SEVERE backlogs expected. Trax/TCS/PostEx will be at 400% capacity. Pre-book slots by Nov 1.",
        "seller_checklist": [
            "All stock must be in warehouse by October 20 — no exceptions.",
            "Pre-pack your top 10 SKUs in courier bags to dispatch within 2 hours of order.",
            "Set up WhatsApp Business auto-reply for order tracking links.",
            "Negotiate minimum 300 daily booking slots with your courier partner.",
            "Cap daily orders to what you can dispatch same-day — overselling kills ratings."
        ]
    },
    {
        "id": "winter-wedding-peak-2026",
        "name": "Winter Wedding Grand Peak — Dec/Jan 💒",
        "name_ur": "سردیوں کی شادیاں — دسمبر جنوری",
        "hijri_date": "Rajab - Sha'ban 1448 AH",
        "start_date": "2026-12-01",
        "end_date": "2027-01-31",
        "demand_spike_pct": 290,
        "peak_window": "December 2026 to January 2027",
        "sourcing_cutoff": "2026-11-10",
        "courier_cutoff": "Rolling daily",
        "status": "Long-Term Strategic",
        "description": (
            "📊 Past Analysis → December-January is the pinnacle of Pakistani shaadi season. "
            "Historical GMV index: 88. Chiffon, velvet, and gold-plated jewelry dominate. "
            "AOV consistently at PKR 5,000–15,000 — highest of the entire year.\n\n"
            "🔮 2026-27 Forecast: Post-Blessed Friday, buyers shift focus to wedding essentials. "
            "Bridal sets, mehndi jewelry, formal shoes, and home decor for guest rooms will peak. "
            "International Pakistani diaspora orders from UK/UAE/US increase 40% in Dec."
        ),
        "top_categories": [
            "Velvet & Chiffon Formal Suits",
            "Bridal Gold-Plated Jewelry",
            "Groom Sherwani & Nagra Footwear",
            "Mehndi & Baraat Decor Sets",
            "Luxury Perfumes & Ittars"
        ],
        "recommended_lead_time_days": 45,
        "historical_gmv_index": 88,
        "courier_notes": "International orders via TCS WorldWide or DHL. Domestic high-value via TCS Express only.",
        "seller_checklist": [
            "Source velvet & formal fabrics from Faisalabad by November 10.",
            "Enable international shipping on Shopify for diaspora buyers (UK, UAE, USA).",
            "Offer express 1-2 day delivery for last-minute wedding buyers at premium price.",
            "Create bridal combo bundles (suit + jewelry + perfume) for +60% AOV uplift."
        ]
    },
    {
        "id": "1212-year-end-sale-2026",
        "name": "12.12 Year-End Clearance Sale 🎊",
        "name_ur": "12.12 سال آخر کلیئرنس سیل",
        "hijri_date": "Sha'ban 1448 AH",
        "start_date": "2026-12-12",
        "end_date": "2026-12-31",
        "demand_spike_pct": 220,
        "peak_window": "12th December to 31st December 2026",
        "sourcing_cutoff": "2026-11-20",
        "courier_cutoff": "2026-12-28",
        "status": "Long-Term Strategic",
        "description": (
            "📊 Past Analysis → 12.12 is Pakistan's 3rd biggest online shopping day. "
            "It serves as a clearance festival — sellers dump excess 11.11 inventory at discounts. "
            "Electronics, home goods, and fashion bundles dominate with 2.2x GMV multiplier.\n\n"
            "🔮 2026 Forecast: Use 12.12 to liquidate remaining 11.11 stock. Bundle slow-movers "
            "with bestsellers for clearance combos. Year-end gifting (corporate gifts, "
            "family sets) will drive B2B orders above PKR 10,000."
        ),
        "top_categories": [
            "Electronics Clearance (Bundles)",
            "Winter Fashion Clearance Sets",
            "Home & Kitchen Gift Sets",
            "Corporate Gift Hampers",
            "Kids Toy & Clothing Bundles"
        ],
        "recommended_lead_time_days": 30,
        "historical_gmv_index": 82,
        "courier_notes": "Year-end courier rush. Book extra slots. Avoid COD on high-value orders above PKR 8,000.",
        "seller_checklist": [
            "Plan clearance pricing strategy by November 20 for 11.11 leftover stock.",
            "Create 'Year-End Gift Set' bundles — corporate buyers order 5-20 units.",
            "Run countdown timer campaigns on WhatsApp broadcast (3x open rate vs email).",
            "Offer free gift-wrapping service — 28% conversion uplift on gift orders."
        ]
    },
    {
        "id": "ramadan-2027",
        "name": "Ramadan 2027 — Pre-Sourcing Intelligence 🌙",
        "name_ur": "رمضان 2027 — ابتدائی سورسنگ پلاننگ",
        "hijri_date": "1 Ramadan 1449 AH",
        "start_date": "2027-02-07",
        "end_date": "2027-03-09",
        "demand_spike_pct": 250,
        "peak_window": "First 20 days of Ramadan 2027",
        "sourcing_cutoff": "2027-01-10",
        "courier_cutoff": "2027-03-03",
        "status": "Long-Term Strategic",
        "description": (
            "📊 Past Analysis → Ramadan 2026 (Feb-Mar) delivered +240% demand spike — "
            "the 2nd highest event of the year. Kitchen gadgets (+340%), modest wear (+210%), "
            "and Islamic decor (+180%) were the top performers. Sellers who sourced 40+ days "
            "early captured 5x more orders than last-minute competitors.\n\n"
            "🔮 2027 Forecast: Ramadan 1449 starts ~Feb 7, 2027. Begin market research NOW "
            "(Sep 2026) for new product trends. Rechargeable kitchen tools, premium Abayas, "
            "and Ramadan hampers will again be mega-sellers. "
            "⚡ Sourcing deadline: January 10, 2027."
        ),
        "top_categories": [
            "Ramadan Kitchen Gadgets (Rechargeable Choppers, Air Fryers)",
            "Modest Wear — Abayas, Hijabs, Modest Kurtis",
            "Islamic Lifestyle (Prayer Mats, Tasbihs, Quran Stands)",
            "Dates & Ramadan Hamper Gift Sets",
            "Pre-Eid Unstitched Embroidered Fabric"
        ],
        "recommended_lead_time_days": 45,
        "historical_gmv_index": 92,
        "courier_notes": "Heavy congestion from 15th Ramadan onward. Air cargo recommended for high-ticket items.",
        "seller_checklist": [
            "Start competitor product research for Ramadan 2027 categories in Oct 2026.",
            "Sample new kitchen gadget products from wholesale hubs by November 2026.",
            "Build your Ramadan 2027 email & WhatsApp subscriber list from December onward.",
            "Submit Daraz Ramadan Mega deals application by December 2026 (early access).",
            "Lock Faisalabad fabric sourcing before January 10, 2027 deadline."
        ]
    },
    {
        "id": "eid-ul-fitr-2027",
        "name": "Eid-ul-Fitr 2027 — Early Intelligence 🎉",
        "name_ur": "عید الفطر 2027 — ابتدائی تیاری",
        "hijri_date": "1 Shawwal 1449 AH",
        "start_date": "2027-03-09",
        "end_date": "2027-03-12",
        "demand_spike_pct": 330,
        "peak_window": "Last 15 days of Ramadan 2027",
        "sourcing_cutoff": "2027-02-01",
        "courier_cutoff": "2027-03-05",
        "status": "Long-Term Strategic",
        "description": (
            "📊 Past Analysis → Eid-ul-Fitr 2026 was Pakistan's #1 annual e-commerce event "
            "with +320% surge and 100/100 GMV index. Women's festive pret, men's kurta pajama, "
            "and Eid jewelry drove the highest order volumes. Courier cutoffs 4-5 days before Eid "
            "are non-negotiable — late sellers lost 30% of revenue to returns.\n\n"
            "🔮 2027 Forecast: Eid ~March 9, 2027. Expect +330% or higher as TikTok Shop matures. "
            "Ready-to-Wear (Pret) will dominate over unstitched. Start building your Eid collection "
            "by January 2027. Influencer collaborations should be locked by February 2027."
        ),
        "top_categories": [
            "Women's Ready-to-Wear Eid Pret (3-Piece)",
            "Men's Embroidered Kurta Pajama",
            "Kids Eid Outfits (Boys & Girls)",
            "Eid Jewelry & Bangles Sets",
            "Khussas & Festive Footwear"
        ],
        "recommended_lead_time_days": 50,
        "historical_gmv_index": 100,
        "courier_notes": "Critical: All Eid deliveries MUST be dispatched by March 5, 2027. No exceptions.",
        "seller_checklist": [
            "Begin Eid 2027 collection design brief in November 2026.",
            "Lock Lahore/Karachi manufacturing slots by December 2026.",
            "Book TikTok & Instagram influencer collaborations by February 2027.",
            "Set up pre-order system for Eid suits by January 2027 for early buyers.",
            "Strictly enforce March 5 dispatch cutoff — no orders after this date for Eid delivery."
        ]
    }
]

# Auto-compute days_remaining dynamically
def _build_events():
    events = []
    for ev in _EVENTS_RAW:
        ev_copy = dict(ev)
        ev_copy["days_remaining"] = _days_left(ev["start_date"])
        events.append(ev_copy)
    # Sort: active first (start_date <= today), then upcoming by start_date
    today = date.today()
    def sort_key(e):
        try:
            sd = datetime.strptime(e["start_date"], "%Y-%m-%d").date()
            ed = datetime.strptime(e["end_date"], "%Y-%m-%d").date() if e["end_date"] != "Rolling daily" else sd
            if sd <= today <= ed:
                return (0, sd)  # Currently active
            elif sd > today:
                return (1, sd)  # Upcoming
            else:
                return (2, sd)  # Past (should not appear but safety)
        except Exception:
            return (1, date.max)
    events.sort(key=sort_key)
    return events

EVENTS_DATA = _build_events()

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
        "wholesale_hub": "Shah Alam Market, Lahore",
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
    },
    {
        "id": "prod-009",
        "name": "ANC Wireless TWS Earbuds with Charging Case",
        "name_ur": "اے این سی وائرلیس ٹی ڈبلیو ایس ایئربڈز",
        "category": "Smart Electronics & TWS Earbuds",
        "event_id": "pre-1111-sourcing-2026",
        "wholesale_hub": "Hall Road, Lahore / Saddar Electronic Market, Karachi",
        "sourcing_cost": 780,
        "suggested_retail_price": 1899,
        "typical_ad_cac": 390,
        "typical_courier_fee": 230,
        "packaging_cost": 35,
        "return_risk_default": "Medium",
        "opportunity_score": 93,
        "demand_trend": "+265% forecast for 11.11",
        "competition_level": "High",
        "search_volume_pk": "150K/month",
        "profit_margin_delivered_pct": 30.4,
        "selling_points": ["Affordable ANC upgrade for daily commuters", "Compact bundle suited to 11.11 flash deals"],
        "image_url": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=600&q=80"
    },
    {
        "id": "prod-010",
        "name": "Compact 4.5L Digital Air Fryer",
        "name_ur": "کمپیکٹ ڈیجیٹل ایئر فرائر",
        "category": "Home Appliances (Air Fryers, Heaters)",
        "event_id": "blessed-friday-1111-2026",
        "wholesale_hub": "Bolton Market, Karachi / Hall Road, Lahore",
        "sourcing_cost": 5200,
        "suggested_retail_price": 8999,
        "typical_ad_cac": 850,
        "typical_courier_fee": 420,
        "packaging_cost": 120,
        "return_risk_default": "Low",
        "opportunity_score": 90,
        "demand_trend": "+180% forecast for 11.11",
        "competition_level": "Medium",
        "search_volume_pk": "88K/month",
        "profit_margin_delivered_pct": 22.1,
        "selling_points": ["Family-size capacity at a flash-sale price", "Strong gifting and winter cooking appeal"],
        "image_url": "https://images.unsplash.com/photo-1648138752703-7f2e6e5a6c4d?w=600&q=80"
    },
    {
        "id": "prod-011",
        "name": "Soft Fleece Hoodie and Jogger Winter Set",
        "name_ur": "نرم فلیس ہُڈی اور جاگر ونٹر سیٹ",
        "category": "Light Knitwear & Hoodies",
        "event_id": "pre-winter-launch-2026",
        "wholesale_hub": "Azam Cloth Market, Lahore / Faisalabad Textile Market",
        "sourcing_cost": 1250,
        "suggested_retail_price": 2999,
        "typical_ad_cac": 500,
        "typical_courier_fee": 250,
        "packaging_cost": 45,
        "return_risk_default": "Medium",
        "opportunity_score": 86,
        "demand_trend": "+145% early winter demand",
        "competition_level": "Medium",
        "search_volume_pk": "72K/month",
        "profit_margin_delivered_pct": 27.6,
        "selling_points": ["Warm everyday set for the first winter wave", "Easy-to-size bundle with broad family appeal"],
        "image_url": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=600&q=80"
    },
    {
        "id": "prod-012",
        "name": "Embroidered Chiffon Formal Wedding Suit",
        "name_ur": "کڑھائی والا شیفون فارمل ویڈنگ سوٹ",
        "category": "Bridal & Mehndi Formal Wear",
        "event_id": "shaadi-season-oct-2026",
        "wholesale_hub": "Faisalabad Textile Market / Shah Alam Market, Lahore",
        "sourcing_cost": 2800,
        "suggested_retail_price": 6499,
        "typical_ad_cac": 720,
        "typical_courier_fee": 280,
        "packaging_cost": 70,
        "return_risk_default": "Medium",
        "opportunity_score": 89,
        "demand_trend": "+185% wedding-season forecast",
        "competition_level": "High",
        "search_volume_pk": "105K/month",
        "profit_margin_delivered_pct": 31.0,
        "selling_points": ["Event-ready formal styling for October weddings", "Premium look without branded-retail pricing"],
        "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&q=80"
    },
    {
        "id": "prod-013",
        "name": "Velvet Embroidered Formal Wedding Suit",
        "name_ur": "ویلویٹ کڑھائی والا فارمل ویڈنگ سوٹ",
        "category": "Velvet & Chiffon Formal Suits",
        "event_id": "winter-wedding-peak-2026",
        "wholesale_hub": "Faisalabad Textile Market / Shah Alam Market, Lahore",
        "sourcing_cost": 3200,
        "suggested_retail_price": 7499,
        "typical_ad_cac": 780,
        "typical_courier_fee": 300,
        "packaging_cost": 80,
        "return_risk_default": "Medium",
        "opportunity_score": 91,
        "demand_trend": "+290% winter wedding forecast",
        "competition_level": "High",
        "search_volume_pk": "98K/month",
        "profit_margin_delivered_pct": 30.2,
        "selling_points": ["Premium winter wedding fabric", "High-AOV formalwear with bundle potential"],
        "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600&q=80"
    },
    {
        "id": "prod-014",
        "name": "Year-End Home & Kitchen Gift Bundle",
        "name_ur": "سال آخر ہوم اینڈ کچن گفٹ بنڈل",
        "category": "Home & Kitchen Gift Sets",
        "event_id": "1212-year-end-sale-2026",
        "wholesale_hub": "Bolton Market, Karachi / Hall Road, Lahore",
        "sourcing_cost": 1450,
        "suggested_retail_price": 3299,
        "typical_ad_cac": 520,
        "typical_courier_fee": 260,
        "packaging_cost": 65,
        "return_risk_default": "Low",
        "opportunity_score": 85,
        "demand_trend": "+220% year-end gifting forecast",
        "competition_level": "Medium",
        "search_volume_pk": "61K/month",
        "profit_margin_delivered_pct": 28.5,
        "selling_points": ["Ready-to-gift bundle for year-end clearance", "Compact SKU with easy shipping"],
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600&q=80"
    },
    {
        "id": "prod-015",
        "name": "Rechargeable Mini Kitchen Chopper",
        "name_ur": "ریچارج ایبل منی کچن چوپر",
        "category": "Ramadan Kitchen Gadgets (Rechargeable Choppers, Air Fryers)",
        "event_id": "ramadan-2027",
        "wholesale_hub": "Bolton Market, Karachi / Hall Road, Lahore",
        "sourcing_cost": 690,
        "suggested_retail_price": 1899,
        "typical_ad_cac": 400,
        "typical_courier_fee": 230,
        "packaging_cost": 45,
        "return_risk_default": "Low",
        "opportunity_score": 92,
        "demand_trend": "+340% Ramadan forecast",
        "competition_level": "Medium",
        "search_volume_pk": "110K/month",
        "profit_margin_delivered_pct": 31.8,
        "selling_points": ["Fast iftar prep in a compact rechargeable format", "Strong video-demo conversion angle"],
        "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=600&q=80"
    },
    {
        "id": "prod-016",
        "name": "Women's Ready-to-Wear Eid Pret 3-Piece",
        "name_ur": "خواتین کا ریڈی ٹو وئیر عید پریٹ تھری پیس",
        "category": "Women's Ready-to-Wear Eid Pret (3-Piece)",
        "event_id": "eid-ul-fitr-2027",
        "wholesale_hub": "Faisalabad Textile Market / Shah Alam Market, Lahore",
        "sourcing_cost": 1900,
        "suggested_retail_price": 4299,
        "typical_ad_cac": 640,
        "typical_courier_fee": 260,
        "packaging_cost": 55,
        "return_risk_default": "Medium",
        "opportunity_score": 94,
        "demand_trend": "+330% Eid forecast",
        "competition_level": "High",
        "search_volume_pk": "175K/month",
        "profit_margin_delivered_pct": 29.4,
        "selling_points": ["Ready-to-wear sizing reduces alteration friction", "Festive styling for Eid gifting and family orders"],
        "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&q=80"
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


def build_event_driven_demand_curve(events=None):
    """Build a transparent annual forecast from the current event calendar.

    The baseline is a curated planning benchmark. Current and future event
    demand spikes override the baseline for their calendar month.
    """
    today = date.today()
    active_events = events if events is not None else EVENTS_DATA
    future_events = []
    for event in active_events:
        try:
            start = datetime.strptime(event["start_date"], "%Y-%m-%d").date()
            end = datetime.strptime(event["end_date"], "%Y-%m-%d").date()
        except (KeyError, TypeError, ValueError):
            continue
        if end >= today:
            future_events.append((event, start, end))

    baseline_by_month = {
        datetime.strptime(row["month"], "%b").month: row
        for row in MONTHLY_DEMAND_CURVE
    }
    curve = []
    for offset in range(12):
        month_start = (today.replace(day=1) + timedelta(days=32 * offset)).replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        month_end = next_month - timedelta(days=1)
        baseline = baseline_by_month[month_start.month]
        month_events = [
            (event, start)
            for event, start, end in future_events
            if start <= month_end and end >= month_start
        ]
        best_event = max(
            month_events,
            key=lambda item: item[0].get("demand_spike_pct", 0),
            default=None
        )
        row = dict(baseline)
        row["month"] = month_start.strftime("%b '%y")
        row["forecast_month"] = month_start.isoformat()
        row["is_forecast"] = True
        row["event_names"] = [event.get("name", "Scheduled event") for event, _ in month_events]
        if best_event:
            event, _ = best_event
            spike = int(event.get("demand_spike_pct", 0))
            row["demand_index"] = max(
                int(baseline["demand_index"]),
                min(100, round(45 + spike * 0.145))
            )
            row["event"] = event.get("name", baseline["event"])
            row["typical_gmv_multiplier"] = f"{1 + spike / 100:.1f}x"
            row["event_id"] = event.get("id")
            row["event_demand_spike_pct"] = spike
        curve.append(row)
    return curve
