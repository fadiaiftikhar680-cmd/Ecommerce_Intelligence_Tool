"""
pages/1_Event_Intelligence.py
Module 1: Event Calendar & Alert System.
Synchronizes Hijri & Gregorian calendars, tracks 30-45 day advance demand alerts,
courier cutoff dates, and seller preparation checklists.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.api_client import ApiClient
from components.layout import apply_custom_styles, render_market_ticker, render_page_header
from components.cards import render_event_card, render_metric_card

st.set_page_config(
    page_title="Event Calendar & Alerts | Pakistan E-Commerce Intelligence",
    page_icon="📅",
    layout="wide"
)

apply_custom_styles()
render_market_ticker()

render_page_header(
    title="Event Calendar & Early Demand Alert System",
    subtitle="Hijri and Gregorian synchronized intelligence giving 30–45 day lead alerts before major Pakistani shopping peaks.",
    badge="MODULE 1 · EVENT INTELLIGENCE"
)

# Custom Event Creation Form in Expander
with st.expander("➕ Add Custom Flash Sale / Store Campaign Alert", expanded=False):
    st.markdown("Add your private store campaigns (Payday sale, 11.11 warm-up, seasonal clearance) to get automated deadline alerts.")
    with st.form("custom_event_form"):
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            ev_name = st.text_input("Event / Campaign Name *", placeholder="e.g. Mid-Summer Lawn Clearance")
            ev_name_ur = st.text_input("Urdu Title (Optional)", placeholder="مثلاً مڈ سمر کلیئرنس سیل")
            ev_status = st.selectbox("Preparation Status", ["Active Sourcing", "High Urgency", "Upcoming Planning", "Long-Term Strategic"])
        with ec2:
            start_d = st.date_input("Start Date", value=date.today())
            end_d = st.date_input("End Date", value=date.today())
            ev_spike = st.slider("Projected Sales Spike %", min_value=20, max_value=400, value=120, step=10)
        with ec3:
            sourcing_cut = st.date_input("Wholesale Sourcing Cutoff", value=date.today())
            courier_cut = st.date_input("Courier Dispatch Cutoff", value=date.today())
            ev_categories = st.text_input("Top Categories (Comma separated)", value="Women Fashion, Pret, Kurtis")

        ev_desc = st.text_area("Campaign Strategy & Notes", placeholder="Campaign objectives, target audience, marketing budget.")
        submit_ev = st.form_submit_button("🚀 Save Event Alert to Database", use_container_width=True)

        if submit_ev:
            if not ev_name:
                st.error("Please enter an event name.")
            else:
                days_left = max(0, (start_d - date.today()).days)
                cat_list = [c.strip() for c in ev_categories.split(",") if c.strip()]
                payload = {
                    "name": ev_name,
                    "name_ur": ev_name_ur or ev_name,
                    "hijri_date": "Custom Solar Milestone",
                    "start_date": str(start_d),
                    "end_date": str(end_d),
                    "demand_spike_pct": ev_spike,
                    "peak_window": f"{start_d} to {end_d}",
                    "sourcing_cutoff": str(sourcing_cut),
                    "courier_cutoff": str(courier_cut),
                    "status": ev_status,
                    "days_remaining": days_left,
                    "description": ev_desc or "Custom merchant promotional event.",
                    "top_categories": cat_list,
                    "recommended_lead_time_days": 25,
                    "historical_gmv_index": 80,
                    "courier_notes": "Book parcel slots 3-4 days in advance to avoid dispatch backlogs.",
                    "seller_checklist": [
                        "Finalize packaging materials & flyers.",
                        "Set up Meta / TikTok retargeting audiences.",
                        "Staff customer support team for WhatsApp order confirmation."
                    ]
                }
                res = ApiClient.create_custom_event(payload)
                st.success(f"✅ Event '{ev_name}' created successfully and synchronized with intelligence calendar!")
                st.rerun()

# Filter controls
filter_col1, filter_col2, filter_col3 = st.columns([40, 30, 30])

with filter_col1:
    status_filter = st.selectbox(
        "Filter by Preparation Status",
        ["All", "Active Sourcing", "High Urgency", "Upcoming Planning", "Long-Term Strategic"]
    )

with filter_col2:
    sort_option = st.selectbox(
        "Sort Order",
        ["Urgency (Days Remaining: Lowest First)", "Demand Surge (% Spike: Highest First)"]
    )

with filter_col3:
    st.write("")
    st.write("")
    refresh_btn = st.button("🔄 Refresh Events Feed")

events = ApiClient.get_events(status_filter=status_filter)

if sort_option == "Demand Surge (% Spike: Highest First)":
    events.sort(key=lambda x: x["demand_spike_pct"], reverse=True)

# Top summary KPIs for events
active_events_count = len([e for e in events if e.get("days_remaining", 999) <= 45])
nearest_event = events[0] if events else None

top_m1, top_m2, top_m3 = st.columns(3)
with top_m1:
    render_metric_card(
        label="Urgent Pre-Order Peaks (<45 Days)",
        value=f"{active_events_count} Events",
        subtext="Immediate inventory & creative preparation required",
        delta="Critical Window",
        delta_color="#EF4444"
    )

with top_m2:
    render_metric_card(
        label="Next Sourcing Cutoff",
        value=nearest_event["sourcing_cutoff"] if nearest_event else "N/A",
        subtext=f"Wholesale order deadline for {nearest_event['name'] if nearest_event else ''}",
        delta="Action Required",
        delta_color="#F59E0B"
    )

with top_m3:
    max_surge = max([e.get("demand_spike_pct", 100) for e in events]) if events else 100
    render_metric_card(
        label="Maximum Projected Surge",
        value=f"+{max_surge}%",
        subtext="Historical festive sales multiplier peak",
        delta="Peak Festive Season",
        delta_color="#10B981"
    )

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DETAILED EVENT CARDS & ACTION CHECKLISTS
# -----------------------------------------------------------------------------
st.markdown("### 🗓️ Synchronized Cultural & Commercial Event Roadmap")

for event in events:
    render_event_card(event)
    
    with st.expander(f"📋 View Action Checklist & Courier Rules for {event['name']}", expanded=False):
        c1, c2 = st.columns([55, 45])
        with c1:
            st.markdown("#### ✅ Recommended Seller Milestone Checklist")
            for item in event.get("seller_checklist", []):
                st.markdown(f"- {item}")
        with c2:
            st.markdown("#### 🚚 Courier & Logistics Advisory")
            st.warning(f"**Logistics Notice:** {event.get('courier_notes', 'N/A')}")
            st.markdown(f"**Recommended Wholesale Lead Time:** `{event.get('recommended_lead_time_days', 30)} Days` before event starts.")

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HIJRI VS GREGORIAN REFERENCE TABLE
# -----------------------------------------------------------------------------
st.markdown("### 🌙 Hijri-Gregorian Event Synchronization Table")
st.markdown("Because the Islamic lunar calendar shifts forward by approximately 10-11 days each solar year, syncing both timelines is crucial for inventory buying cycles.")

calendar_rows = []
for e in events:
    calendar_rows.append({
        "Event Name": e["name"],
        "Urdu Title": e.get("name_ur", ""),
        "Hijri Milestone": e.get("hijri_date", "Custom"),
        "Gregorian Date Window": f"{e['start_date']} to {e['end_date']}",
        "Days Remaining": f"{e.get('days_remaining', 0)} days",
        "Projected Demand Spike": f"+{e.get('demand_spike_pct', 0)}%",
        "Courier Cutoff": e.get("courier_cutoff", "N/A"),
        "Type": "Custom Merchant Event" if e.get("is_custom") else "Core Cultural Peak"
    })

cal_df = pd.DataFrame(calendar_rows)
st.dataframe(cal_df, use_container_width=True, hide_index=True)
