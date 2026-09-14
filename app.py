"""
app.py
Main Streamlit Entry Point — Actionable Insights Overview.
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
from utils.api_client import ApiClient
from components.layout import apply_custom_styles, render_market_ticker, render_page_header
from components.cards import render_metric_card, render_product_card
from components.charts import plot_demand_timeline

st.set_page_config(
    page_title="Pakistan E-Commerce Intelligence Tool",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
render_market_ticker()

backend_health = ApiClient.check_backend_health()

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

    st.markdown("---")
    st.markdown("### 🇵🇰 Pakistan Market Specs")
    st.caption("• **COD Dominance:** 85%+ of Total GMV")
    st.caption("• **Benchmark RTO:** 14% (Metros) to 44% (Tier 3)")
    st.caption("• **Currency:** Pakistani Rupee (PKR)")
    st.caption("• **Calendar Sync:** Gregorian + Hijri Lunar")

render_page_header(
    title="E-Commerce Event & Profit Intelligence Dashboard",
    subtitle="Data-backed event alerts, hot products, safe pricing, and COD return protection for Pakistani online sellers.",
    badge="PAKISTAN MARKET SAAS EDITION"
)

# ── Fetch data
overview     = ApiClient.get_market_overview()
next_event   = overview.get("next_event")
current_live = overview.get("current_live_event")
top_upcoming = overview.get("top_upcoming_events", [])
seasonal_sale = overview.get("seasonal_sale", {})
seasonal_current = seasonal_sale.get("current_event")
seasonal_next = seasonal_sale.get("next_event") or next_event
seasonal_peak = seasonal_sale.get("peak_event")
tracked_products = ApiClient.get_winning_products(min_opportunity=0)
demand_curve = ApiClient.get_demand_curve()
today        = date.today()

# ─── LIVE NOW BANNER
if current_live:
    try:
        ed = datetime.strptime(current_live["end_date"], "%Y-%m-%d").date()
        live_days_left = max(0, (ed - today).days)
    except Exception:
        live_days_left = 0

    st.html(f"""
        <div style="background:linear-gradient(90deg,#052e16,#064e3b);
                    border:1px solid #10B981; border-radius:10px;
                    padding:12px 20px; margin-bottom:16px;
                    display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:0.75rem;color:#34D399;font-weight:700;letter-spacing:0.1em;">
                    EVENT LIVE RIGHT NOW
                </span>
                <div style="font-size:1.1rem;font-weight:700;color:#F8FAFC;margin-top:3px;">
                    {current_live['name']}
                </div>
                <div style="font-size:0.82rem;color:#94A3B8;margin-top:2px;">
                    {current_live.get('name_ur','')} - Ends: {current_live.get('end_date','')}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2rem;font-weight:800;color:#10B981;">{live_days_left}</div>
                <div style="font-size:0.75rem;color:#94A3B8;">days remaining in event</div>
                <div style="font-size:0.78rem;color:#10B981;margin-top:4px;">
                    +{current_live.get('demand_spike_pct',0)}% Demand Spike
                </div>
            </div>
        </div>
    """)

# ─── 1. KPI METRICS
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    if next_event:
        render_metric_card(
            label="Next Upcoming Event",
            value=f"{next_event.get('days_remaining', 0)} Days Left",
            subtext=f"{next_event.get('hijri_date','')} - {next_event.get('name','')}",
            delta=f"+{next_event.get('demand_spike_pct', 0)}% Volume",
            delta_color="#10B981",
            badge="UPCOMING"
        )
    else:
        render_metric_card(
            label="Next Peak Event",
            value="All Covered",
            subtext="Check Event Intelligence tab",
            delta="View Full Calendar",
            delta_color="#10B981",
            badge="CALENDAR"
        )

with kpi2:
    if seasonal_current:
        seasonal_value = f"+{seasonal_current.get('demand_spike_pct', 0)}%"
        seasonal_subtext = f"Current: {seasonal_current.get('name', 'Live event')}"
        seasonal_delta = (
            f"Next: {seasonal_next.get('start_date', 'N/A')}"
            if seasonal_next else "No upcoming event"
        )
    elif seasonal_next:
        seasonal_value = f"+{seasonal_next.get('demand_spike_pct', 0)}%"
        seasonal_subtext = f"Next: {seasonal_next.get('name', 'Upcoming event')}"
        seasonal_delta = "Upcoming seasonal sale"
    else:
        seasonal_value = "N/A"
        seasonal_subtext = "No current or upcoming seasonal event"
        seasonal_delta = "Calendar"

    render_metric_card(
        label="Current & Upcoming Seasonal Sale",
        value=seasonal_value,
        subtext=seasonal_subtext,
        delta=seasonal_delta,
        delta_color="#38BDF8",
        badge=(
            f"PEAK: +{seasonal_peak.get('demand_spike_pct', 0)}%"
            if seasonal_peak else "EVENT CALENDAR"
        )
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
        value=f"{len(tracked_products)} Items",
        subtext="Click below to see names and full product details",
        delta=f"Avg Score: {overview['avg_opportunity_score']}/100",
        delta_color="#10B981",
        badge="OPPORTUNITY"
    )
    show_products = st.button(
        f"View {len(tracked_products)} Tracked Products",
        key="show_tracked_products",
        use_container_width=True
    )

if show_products:
    st.markdown("### Tracked Winning Products - Full Details")
    st.caption("Every tracked item is listed below with its name, score, pricing, sourcing, risk and sales information.")
    if tracked_products:
        with st.expander(f"Open all {len(tracked_products)} product details", expanded=True):
            for index, product in enumerate(tracked_products, start=1):
                st.markdown(f"#### {index}. {product['name']}")
                detail_cols = st.columns(5)
                detail_cols[0].metric("Opportunity Score", f"{product.get('opportunity_score', 0)}/100")
                detail_cols[1].metric("Category", product.get("category", "N/A"))
                detail_cols[2].metric("Wholesale Price", f"PKR {product.get('sourcing_cost', 0):,}")
                detail_cols[3].metric("Retail Price", f"PKR {product.get('suggested_retail_price', 0):,}")
                detail_cols[4].metric("Margin", f"{product.get('profit_margin_delivered_pct', 0)}%")
                st.markdown(
                    f"**Urdu Name:** {product.get('name_ur') or 'N/A'}  \n"
                    f"**Wholesale Hub:** {product.get('wholesale_hub') or product.get('sourcing_hub') or 'N/A'}  \n"
                    f"**RTO Risk:** {product.get('return_risk_default', 'N/A')}  |  "
                    f"**Courier:** {product.get('recommended_courier', 'N/A')}  |  "
                    f"**Demand Trend:** {product.get('demand_trend', 'N/A')}  \n"
                    f"**Details:** {product.get('description') or 'Market-validated product opportunity.'}"
                )
                if index < len(tracked_products):
                    st.divider()
    else:
        st.info("No winning products are available right now.")

st.html("<div style='margin-top:18px;'></div>")

# ─── 2. UPCOMING EVENTS — Top 3 Clickable Cards
st.markdown("### Upcoming Events — Click to See Full Details")

if top_upcoming:
    cols = st.columns(min(len(top_upcoming), 3))
    for idx, ev in enumerate(top_upcoming[:3]):
        days  = ev.get("days_remaining", 0)
        spike = ev.get("demand_spike_pct", 0)

        if days <= 20:
            border = "#EF4444"
            dot    = "URGENT"
        elif days <= 60:
            border = "#F59E0B"
            dot    = "SOON"
        else:
            border = "#3B82F6"
            dot    = "PLANNED"

        with cols[idx]:
            st.html(f"""
                <div style="background:#1E293B; border:1px solid {border};
                            border-radius:10px; padding:14px 16px; margin-bottom:4px;">
                    <div style="font-size:0.70rem;color:{border};font-weight:700;
                                letter-spacing:0.08em;margin-bottom:5px;">
                        {dot} - {days} DAYS LEFT
                    </div>
                    <div style="font-size:0.92rem;font-weight:700;color:#F8FAFC;
                                line-height:1.35;margin-bottom:4px;">
                        {ev['name']}
                    </div>
                    <div style="font-size:0.75rem;color:#94A3B8;margin-bottom:8px;">
                        {ev.get('name_ur','')}
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:0.75rem;">
                        <span style="color:#10B981;font-weight:700;">+{spike}% Demand</span>
                        <span style="color:#64748B;">{ev.get('start_date','')}</span>
                    </div>
                </div>
            """)

            with st.expander("Click — Full Details & Action Plan", expanded=False):
                st.markdown(f"### {ev['name']}")
                st.markdown(f"**Hijri:** {ev.get('hijri_date','')}")

                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Starts In", f"{days} days")
                col_b.metric("Sourcing Cutoff", ev.get("sourcing_cutoff","N/A"))
                col_c.metric("Courier Cutoff", ev.get("courier_cutoff","N/A"))

                st.markdown("---")
                desc = ev.get("description", "")
                if "Past Analysis" in desc or "Forecast" in desc or "Analysis" in desc:
                    parts = desc.split("\n\n", 1)
                    st.info(parts[0].replace("Past Analysis", "**Past Analysis**"))
                    if len(parts) > 1:
                        st.success(parts[1].replace("Forecast", "**Forecast**"))
                else:
                    st.write(desc)

                cats = ev.get("top_categories", [])
                if cats:
                    st.markdown("**Top Winning Categories:**")
                    cat_html = " ".join([
                        f"<span style='background:#1E293B;border:1px solid #10B981;"
                        f"color:#10B981;padding:3px 10px;border-radius:12px;"
                        f"font-size:0.78rem;margin:2px;display:inline-block;'>{c}</span>"
                        for c in cats
                    ])
                    st.html(f"<div style='margin-top:6px;'>{cat_html}</div>")

                checklist = ev.get("seller_checklist", [])
                if checklist:
                    st.markdown("**Seller Action Checklist:**")
                    for item in checklist:
                        st.markdown(f"- {item}")

# Full Events List — collapsible
all_events_list = ApiClient.get_events()
if all_events_list:
    st.markdown("---")
    with st.expander("View All Upcoming Events — Full Calendar List", expanded=False):
        for ev in all_events_list:
            days  = ev.get("days_remaining", 0)
            spike = ev.get("demand_spike_pct", 0)

            try:
                sd = datetime.strptime(ev["start_date"], "%Y-%m-%d").date()
                ed = datetime.strptime(ev["end_date"], "%Y-%m-%d").date()
                is_live = sd <= today <= ed
            except Exception:
                is_live = False

            if is_live:
                icon, color, days_label = "LIVE NOW", "#10B981", "ACTIVE"
            elif days <= 20:
                icon, color, days_label = "URGENT", "#EF4444", f"{days}d"
            elif days <= 60:
                icon, color, days_label = "SOON", "#F59E0B", f"{days}d"
            else:
                icon, color, days_label = "PLANNED", "#3B82F6", f"{days}d"

            st.html(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            background:#1E293B;border-left:3px solid {color};
                            border-radius:6px;padding:10px 16px;margin-bottom:8px;">
                    <div>
                        <span style="font-size:0.70rem;color:{color};font-weight:700;">
                            {icon}
                        </span>
                        <span style="font-size:0.88rem;font-weight:700;color:#F8FAFC;margin-left:10px;">
                            {ev['name']}
                        </span>
                        <div style="font-size:0.73rem;color:#64748B;margin-top:3px;margin-left:10px;">
                            {ev.get('start_date','')} to {ev.get('end_date','')}
                            &nbsp;|&nbsp; Sourcing: {ev.get('sourcing_cutoff','N/A')}
                        </div>
                    </div>
                    <div style="text-align:right;min-width:80px;">
                        <div style="font-size:1.25rem;font-weight:800;color:{color};">
                            {days_label}
                        </div>
                        <div style="font-size:0.72rem;color:#10B981;">+{spike}%</div>
                    </div>
                </div>
            """)

# ─── 3. DEMAND CURVE + CHECKLIST
st.html("<div style='margin-top:20px;'></div>")
col_chart, col_actions = st.columns([65, 35])

with col_chart:
    fig_timeline = plot_demand_timeline(demand_curve)
    st.plotly_chart(fig_timeline, use_container_width=True)

with col_actions:
    checklist_title  = next_event['name'] if next_event else "Upcoming Event"
    checklist_items  = next_event.get('seller_checklist', []) if next_event else []
    action1 = checklist_items[0] if len(checklist_items) > 0 else "Prepare inventory for upcoming event."
    action2 = checklist_items[1] if len(checklist_items) > 1 else "Set up ad creatives early."
    action3 = next_event.get('courier_notes', 'Book courier slots in advance.') if next_event else "Plan logistics."

    st.html(f"""
        <div class="custom-card" style="height:100%;">
            <div class="card-label">URGENT SELLER ACTION CHECKLIST</div>
            <h4 style="margin:0 0 10px 0;color:#F8FAFC;">{checklist_title}</h4>

            <div class="protocol-item" style="border-left-color:#EF4444;margin-bottom:10px;">
                <div>
                    <strong style="color:#EF4444;display:block;">Action 1:</strong>
                    {action1}
                </div>
            </div>

            <div class="protocol-item" style="border-left-color:#F59E0B;margin-bottom:10px;">
                <div>
                    <strong style="color:#F59E0B;display:block;">Action 2:</strong>
                    {action2}
                </div>
            </div>

            <div class="protocol-item" style="border-left-color:#10B981;margin-bottom:10px;">
                <div>
                    <strong style="color:#10B981;display:block;">Courier Advisory:</strong>
                    {action3}
                </div>
            </div>

            <div style="background:#0F172A;padding:10px;border-radius:8px;
                        margin-top:15px;font-size:0.85rem;color:#94A3B8;">
                Tip: Pakistani couriers halt dispatches 4-5 days before Eid. Plan cutoffs early.
            </div>
        </div>
    """)

st.html("<div style='margin-top:20px;'></div>")

# ─── 4. TOP WINNING PRODUCTS
st.markdown("### Top Winning Products for Upcoming Festive Peak")
st.markdown("Identified high-velocity items with verified wholesale hubs in Lahore, Karachi, Rawalpindi, and Faisalabad.")

top_products = ApiClient.get_winning_products(min_opportunity=90)
prod_display = top_products[:3] if top_products else []

if prod_display:
    prod_cols = st.columns(len(prod_display))
    for idx, prod in enumerate(prod_display):
        with prod_cols[idx]:
            with st.expander(
                f"{prod['name']} · Score {prod.get('opportunity_score', 0)}/100",
                expanded=False
            ):
                render_product_card(prod)
                st.page_link(
                    "pages/2_Winning_Products.py",
                    label="Open full product catalog",
                    icon="🛍️"
                )

# ─── 5. FOOTER
st.html("<hr style='border-color:#334155;margin:30px 0;'>")
footer_col1, footer_col2 = st.columns([70, 30])

with footer_col1:
    backend_status_text = "Layer 3 FastAPI + SQLite Connected" if backend_health["is_online"] else "Layer 2 Service Client Active"
    st.html(f"""
        <div style="font-size:0.85rem;color:#64748B;">
            <strong>End-to-End SaaS Platform</strong> - {backend_status_text} - ML Return Risk Model Active.<br>
            Designed for Pakistani merchants on Shopify, WooCommerce, TikTok Shop, and Daraz.
        </div>
    """)

with footer_col2:
    status_dot   = "#10B981" if backend_health["is_online"] else "#38BDF8"
    status_label = "FastAPI Backend Live" if backend_health["is_online"] else "Full-Stack Ready"
    st.html(f"""
        <div style="text-align:right;font-size:0.85rem;color:{status_dot};">
            System Operational - {status_label}
        </div>
    """)
