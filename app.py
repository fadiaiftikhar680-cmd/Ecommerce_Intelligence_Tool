"""
app.py
Main Streamlit Entry Point — Actionable Insights Overview.
Provides the central dashboard for Pakistani e-commerce merchants with
live market alerts, countdown timers, seasonal demand trajectory, backend health, and top KPIs.
"""

import streamlit as st
import pandas as pd
from utils.api_client import ApiClient
from components.layout import apply_custom_styles, render_market_ticker, render_page_header
from components.cards import render_metric_card, render_product_card
from components.charts import plot_demand_timeline

# Page configuration
st.set_page_config(
    page_title="Pakistan E-Commerce Intelligence Tool",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling and layout components
apply_custom_styles()
render_market_ticker()

# Backend Health & Architecture Check
backend_health = ApiClient.check_backend_health()

# Sidebar Backend Health Badge
with st.sidebar:
    st.markdown("### ⚙️ System Architecture Status")
    if backend_health["is_online"]:
        st.success("🟢 **Layer 3 FastAPI Backend: Connected**")
        st.markdown(f"• **Service:** {backend_health['service']}")
        st.markdown(f"• **Database:** {backend_health['database']}")
        st.markdown(f"• **ML Engine:** {backend_health['ml_model']}")
        st.markdown("[📖 Open Swagger API Docs](http://localhost:8000/docs)")
    else:
        st.info("🟡 **Layer 2 Standalone Engine: Active**")
        st.caption("Running in resilient offline mode with embedded ML model & SQLite fixtures.")
        st.caption("Tip: Run `python run_all.py` to start both FastAPI & Streamlit concurrently.")

    st.markdown("---")
    st.markdown("### 🇵🇰 Pakistan Market Specs")
    st.caption("• **COD Dominance:** 85%+ of Total GMV")
    st.caption("• **Benchmark RTO:** 14% (Metros) to 44% (Tier 3)")
    st.caption("• **Currency:** Pakistani Rupee (PKR ₨)")
    st.caption("• **Calendar Sync:** Gregorian + Hijri Lunar")

# Page Header
render_page_header(
    title="E-Commerce Event & Profit Intelligence Dashboard",
    subtitle="Data-backed event alerts, hot products, safe pricing, and COD return protection for Pakistani online sellers.",
    badge="PAKISTAN MARKET SAAS EDITION"
)

# Fetch overview data via abstracted service layer (Layer 2 -> Layer 3)
overview = ApiClient.get_market_overview()
next_event = overview["next_event"]
demand_curve = ApiClient.get_demand_curve()

# -----------------------------------------------------------------------------
# 1. CORE KPI SUMMARY METRICS
# -----------------------------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    days_left = next_event['days_remaining'] if next_event else 0
    event_name = next_event['name'] if next_event else "No Event"
    render_metric_card(
        label="Next Peak Event",
        value=f"{days_left} Days Left",
        subtext=f"{next_event['hijri_date']} • {event_name}",
        delta=f"+{next_event['demand_spike_pct']}% Volume",
        delta_color="#10B981",
        badge="HIGH PRIORITY"
    )

with kpi2:
    render_metric_card(
        label="Seasonal Sales Multiplier",
        value=overview.get("demand_multiplier_peak", "3.2x"),
        subtext="Peak festive GMV surge vs baseline month",
        delta="Ramadan / Eid Peak",
        delta_color="#38BDF8",
        badge="SURGE INDEX"
    )

with kpi3:
    render_metric_card(
        label="Market COD Return Benchmark",
        value=f"{overview['benchmark_market_rto_pct']}%",
        subtext="Average Pakistani eCommerce RTO across all cities",
        delta="Tier 1: 13.5% | Tier 3: 44%",
        delta_color="#F59E0B",
        badge="COD RISK"
    )

with kpi4:
    render_metric_card(
        label="Winning Products Tracked",
        value=f"{overview['total_winning_products']} Items",
        subtext=f"Avg Opportunity Score: {overview['avg_opportunity_score']}/100",
        delta="Validated Local Sourcing",
        delta_color="#10B981",
        badge="OPPORTUNITY"
    )

st.html("<div style='margin-top: 15px;'></div>")

# -----------------------------------------------------------------------------
# 2. ANNUAL DEMAND CURVE & URGENT SELLER ACTION CHECKLIST
# -----------------------------------------------------------------------------
col_chart, col_actions = st.columns([65, 35])

with col_chart:
    fig_timeline = plot_demand_timeline(demand_curve)
    st.plotly_chart(fig_timeline, use_container_width=True)

with col_actions:
    st.html("""
        <div class="custom-card" style="height: 100%;">
            <div class="card-label">🚨 URGENT SELLER ACTION CHECKLIST</div>
            <h4 style="margin: 0 0 10px 0; color: #F8FAFC;">Pre-Ramadan Sourcing & Campaign Deadlines</h4>
            
            <div class="protocol-item" style="border-left-color: #EF4444; margin-bottom: 10px;">
                <div>
                    <strong style="color: #EF4444; display: block;">Sourcing Deadline in 5 Days:</strong>
                    Lock unstitched fabric dyeing & packaging at Faisalabad/Shah Alam hubs before weavers reach capacity.
                </div>
            </div>

            <div class="protocol-item" style="border-left-color: #F59E0B; margin-bottom: 10px;">
                <div>
                    <strong style="color: #F59E0B; display: block;">Ad Creative Testing (Meta & TikTok):</strong>
                    Launch test creatives now while CPMs are PKR 280-350. Ad costs spike by 45% once Ramadan commences.
                </div>
            </div>

            <div class="protocol-item" style="border-left-color: #10B981; margin-bottom: 10px;">
                <div>
                    <strong style="color: #10B981; display: block;">COD Courier Routing Setup:</strong>
                    Integrate PostEx/Trax API for automated WhatsApp OTP confirmation on high-ticket orders above PKR 3,500.
                </div>
            </div>

            <div style="background: #0F172A; padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 0.85rem; color: #94A3B8;">
                💡 <em>Tip: Pakistani courier services halt parcel dispatches 4-5 days prior to Eid day. Plan final ad cutoff accordingly.</em>
            </div>
        </div>
    """)

st.html("<div style='margin-top: 20px;'></div>")

# -----------------------------------------------------------------------------
# 3. TOP WINNING PRODUCTS SPOTLIGHT FOR ACTIVE SEASON
# -----------------------------------------------------------------------------
st.markdown("### 🔥 Top Winning Products for Upcoming Festive Peak")
st.markdown("Identified high-velocity items with verified wholesale hubs in Lahore, Karachi, Rawalpindi, and Faisalabad.")

top_products = ApiClient.get_winning_products(min_opportunity=90)
prod_display = top_products[:3] if top_products else []

if prod_display:
    prod_cols = st.columns(len(prod_display))
    for idx, prod in enumerate(prod_display):
        with prod_cols[idx]:
            render_product_card(prod)

# -----------------------------------------------------------------------------
# 4. SYSTEM ARCHITECTURE STATUS & FOOTER
# -----------------------------------------------------------------------------
st.html("<hr style='border-color: #334155; margin: 30px 0;'>")
footer_col1, footer_col2 = st.columns([70, 30])

with footer_col1:
    backend_status_text = "Layer 3 FastAPI + SQLite Connected" if backend_health["is_online"] else "Layer 2 Service Client Active"
    st.html(f"""
        <div style="font-size: 0.85rem; color: #64748B;">
            <strong>End-to-End SaaS Platform</strong> • {backend_status_text} • ML Return Risk Model Active.<br>
            Designed exclusively for Pakistani merchants selling via Shopify, WooCommerce, TikTok Shop, and Daraz.
        </div>
    """)

with footer_col2:
    status_dot = "#10B981" if backend_health["is_online"] else "#38BDF8"
    status_label = "FastAPI Backend Live" if backend_health["is_online"] else "Full-Stack Ready"
    st.html(f"""
        <div style="text-align: right; font-size: 0.85rem; color: {status_dot};">
            ● <strong>System Operational</strong> • {status_label}
        </div>
    """)
