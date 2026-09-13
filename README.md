# 🇵🇰 E-Commerce Intelligence Dashboard Tool (Pakistan Market)

A Smart Event & Profit Intelligence SaaS Platform specifically engineered for the Pakistani e-commerce ecosystem.

---

## 📌 Executive Summary

E-commerce sales in Pakistan undergo dramatic seasonal spikes around cultural and commercial milestones:
- **Ramadan Mubarak & Pre-Eid Preparation** (Kitchen, modest fashion, unstitched fabric surge)
- **Eid-ul-Fitr Grand Fashion Season** (Highest volume for Pret, Khussas, Jewelry, Perfumes)
- **Eid-ul-Adha / Bari Eid** (BBQ equipment, Wazirabad steel knives, casual kurtas)
- **14th August Azadi Mega Sale** (Summer stock clearance & patriotic merchandise)
- **Blessed Friday / 11.11 Shopping Festival** (Biggest annual digital commerce discount spike)
- **Winter Wedding Gala / Shaadi Season** (High AOV formal wear, shawls, beauty, ring lights)

Because **Cash on Delivery (COD)** accounts for over 85% of transactions in Pakistan, uncalculated parcel returns (**RTO rates of 15% to 45%**) and double-courier freight wipe out merchant profits. This tool provides **advance event alerts, winning products, safe price margins, and COD risk mitigation**.

---

## 🏗️ System Architecture

Built strictly according to the 3-layer architecture defined in the Master Documentation:

```
┌─────────────────────────────────────────────────────────┐
│                 LAYER 1 · FRONTEND UI                   │
│         Streamlit (Python) · Plotly · Pandas            │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│          LAYER 2 · MOCK DATA & SERVICE CLIENT           │
│     mock/data.py (fixtures)  +  utils/api_client.py     │
└────────────────────────────┬────────────────────────────┘
                             │  (future API bridge)
┌────────────────────────────▼────────────────────────────┐
│         LAYER 3 · BACKEND & SCRAPERS  (Phase 2)         │
│   FastAPI · PostgreSQL · Scikit-learn · Store REST APIs │
└─────────────────────────────────────────────────────────┘
```

> **Design Principle:** All frontend pages query `utils/api_client.py`. When the Layer 3 FastAPI backend is attached, **only `utils/api_client.py` is updated** — the Streamlit UI requires zero code changes.

---

## 📂 Project Directory Structure

```
d:/Ecommerce Intelligence Tool/
├── .streamlit/
│   └── config.toml               # Emerald Pakistani eCommerce theme & config
├── app.py                        # Streamlit entry point (Actionable Insights Overview)
├── pages/
│   ├── 1_Event_Intelligence.py   # Module 1: Event Calendar, Hijri Sync & Alerts
│   ├── 2_Winning_Products.py     # Module 2 & 3: Hot Product Finder & Margin Protector
│   ├── 3_COD_Risk_Calculator.py  # Module 4: COD Return (RTO) Risk Predictor
│   └── 4_My_Store.py             # Module 5: Store Inventory Predictor & Dead Stock
├── components/
│   ├── __init__.py
│   ├── cards.py                  # Metric cards, event widgets, risk badges
│   ├── charts.py                 # Plotly demand timeline, waterfall, city RTO bar charts
│   └── layout.py                 # Responsive styling, headers, market status ticker
├── mock/
│   ├── __init__.py
│   └── data.py                   # Pakistan events, winning items, city tiers, couriers
├── utils/
│   ├── __init__.py
│   └── api_client.py             # Abstracted service client (Layer 2)
├── requirements.txt              # Production dependency specifications
└── README.md                     # Documentation & setup guide
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.11 & 3.13)
- Modern web browser

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Configure Gemini AI (Optional)
The backend exposes `POST /api/intelligence/gemini-insight` for merchant-specific AI advice.
Keep the Gemini key in the environment; do not paste it into Python files or commit it to git.

PowerShell:
```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key"
$env:GEMINI_MODEL = "gemini-2.5-flash"
py -m uvicorn backend.main:app --reload --port 8000
```

Example request:
```json
{
  "question": "Which COD mitigation should I use for a high-value first-time order in Karachi?",
  "context": {
    "order_value_pkr": 8500,
    "category": "Electronics & Gadgets",
    "customer_type": "First-Time Buyer"
  }
}
```

Endpoint: `POST http://127.0.0.1:8000/api/intelligence/gemini-insight`

---

## 💡 Core Modules & Features

### 1. Actionable Insights Overview (`app.py`)
- Live market pulse banner with Hijri date.
- Real-time event countdown timer and historical demand multipliers.
- Interactive 12-month Pakistani e-commerce demand curve.
- Top winning products snapshot and high-urgency seller deadlines.

### 2. Event Calendar & Early Demand Alert System (`pages/1_Event_Intelligence.py`)
- Synchronizes lunar Hijri calendar with solar Gregorian dates.
- 30–45 day lead alerts before Ramadan, Eid-ul-Fitr, Eid-ul-Adha, 14th August, and 11.11.
- Specific seller milestone checklists and logistics cutoff warnings for major couriers.

### 3. Hot Product Finder & Smart Margin Protector (`pages/2_Winning_Products.py`)
- High-opportunity winning catalog with verified local wholesale hubs (Shah Alam Lahore, Bolton Market Karachi, Raja Bazaar Rawalpindi, Faisalabad).
- **Smart Price & Margin Protector**: Calculates true blended profit, break-even ROAS, and max allowable discount % while factoring in COD return freight loss and wasted packaging.
- Interactive unit economics waterfall visualizer.

### 4. COD Return (RTO) Risk Predictor (`pages/3_COD_Risk_Calculator.py`)
- Parcel-level heuristic risk calculator based on:
  - Destination City & Tier (Metros vs Rural/Outskirts).
  - Product Category (Sizing risk vs non-sizing).
  - Customer Order History (Repeat vs cold traffic).
  - Address Completeness (Specific house/street vs landmark only).
  - Courier Service (Trax, PostEx, Leopards, TCS, Call Courier).
- Generates 1-click **WhatsApp verification templates** and **JazzCash/Easypaisa advance deposit SOPs**.
- Comprehensive Pakistan city COD benchmark table and courier comparisons.

### 5. Store Inventory Predictor & Dead Stock Liquidation (`pages/4_My_Store.py`)
- Aligns store catalog against upcoming seasonal event surges.
- Categorizes inventory into:
  - **Event Stars** (high velocity, ready for ad scaling).
  - **Stockout Warnings** (< 10 days of runway remaining).
  - **Dead Stock Liquidation** (capital tied up, bundling strategies).
- Support for custom CSV upload from Shopify or WooCommerce.

---

## 🇵🇰 Pakistan Market Logistics Reference

| Courier Partner | Base Delivery (PKR) | COD Fee % | SLA (Days) | Return Penalty (PKR) | Primary Strength |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Trax Logistics** | ₨ 240 | 2.5% | 2.8 | ₨ 160 | Fast COD portal disbursement & metro speed |
| **PostEx** | ₨ 235 | 2.2% | 2.6 | ₨ 150 | Instant COD financing & Shopify integration |
| **Leopards Courier** | ₨ 270 | 3.0% | 2.9 | ₨ 180 | Unmatched Tier 3 & rural town coverage |
| **TCS Express** | ₨ 320 | 3.0% | 2.1 | ₨ 210 | Highest reliability for luxury festive wear |
| **Call Courier** | ₨ 230 | 2.5% | 3.1 | ₨ 150 | Economical bulk dispatch across Punjab |
