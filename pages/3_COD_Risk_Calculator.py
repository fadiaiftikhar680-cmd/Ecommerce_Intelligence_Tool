"""
pages/3_COD_Risk_Calculator.py
Module 4: COD Return (RTO) Risk Predictor.
Calculates parcel-level return risk based on Pakistani city tiers, product category,
address quality, and order value, with automated WhatsApp & Advance Deposit mitigation rules.
"""

import streamlit as st
import pandas as pd
from utils.api_client import ApiClient
from components.layout import apply_custom_styles, render_market_ticker, render_page_header
from components.cards import render_metric_card, render_risk_result_box
from components.charts import plot_city_rto_barchart

st.set_page_config(
    page_title="COD Return Risk Predictor | Pakistan E-Commerce Intelligence",
    page_icon="⚠️",
    layout="wide"
)

apply_custom_styles()
render_market_ticker()

render_page_header(
    title="Cash on Delivery (COD) Return Risk Predictor",
    subtitle="Assess individual parcel return risk before dispatch to prevent irreversible courier freight losses and fake orders.",
    badge="MODULE 4 · RISK PREDICTOR"
)

tab_calc, tab_benchmarks, tab_couriers = st.tabs([
    "🎯 Order Risk Predictor",
    "🗺️ Pakistan City COD Benchmarks",
    "🚚 Courier Tariffs & Performance"
])

# -----------------------------------------------------------------------------
# TAB 1: ORDER RISK PREDICTOR
# -----------------------------------------------------------------------------
with tab_calc:
    c_left, c_right = st.columns([45, 55])

    with c_left:
        st.markdown("#### 📦 Order & Customer Particulars")

        # Destination City
        city_options = list(ApiClient.get_city_benchmarks()["City"])
        city_sel = st.selectbox("Destination City / Region", city_options, index=0)

        # Product Category
        cat_options = [
            "Apparel & Footwear (Size Risk)",
            "Festive Pret / Unstitched",
            "Kitchen & Home Appliances",
            "Perfumes & Fragrances",
            "Electronics & Gadgets",
            "Jewelry & Fashion Accessories"
        ]
        cat_sel = st.selectbox("Product Category", cat_options, index=0)

        # Order Value
        order_val = st.number_input("Total Order Value (PKR ₨)", min_value=500.0, max_value=50000.0, value=3250.0, step=250.0)

        # Customer History
        cust_options = [
            "First-Time Buyer (Cold Traffic / Ad Click)",
            "Repeat Verified Buyer (1+ Delivered Orders)",
            "Repeat Buyer (With 1 Prior Cancellation)"
        ]
        cust_sel = st.selectbox("Customer Purchase History", cust_options, index=0)

        # Address Verification Quality
        addr_options = [
            "Complete (House/Flat No, Street, Sector/Block)",
            "Moderate (Area/Mohalla mentioned, No house #)",
            "Poor / Vague ('Near Grid Station / Shop', Landmark Only)"
        ]
        addr_sel = st.selectbox("Address Completeness Quality", addr_options, index=1)

        # Courier Selection
        courier_options = [c["name"] for c in ApiClient.get_couriers()]
        courier_sel = st.selectbox("Assigned Courier Partner", courier_options, index=0)

    # Perform risk prediction
    prediction = ApiClient.predict_cod_risk(
        city=city_sel,
        category=cat_sel,
        order_value=order_val,
        customer_type=cust_sel,
        address_type=addr_sel,
        courier=courier_sel
    )

    with c_right:
        st.markdown("#### 🎯 AI Predictive Return Score & Mitigation SOP")
        render_risk_result_box(prediction)

        # WhatsApp Template Generator
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        with st.expander("📲 Generate 1-Click WhatsApp Verification Message Template", expanded=True):
            if prediction["action_code"] == "REQUIRE_PARTIAL_ADVANCE":
                wa_message = (
                    f"Assalam-o-Alaikum! Thank you for ordering from our store. "
                    f"Your Order for {cat_sel} worth Rs. {order_val:,.0f} has been received. "
                    f"As per our delivery policy for {city_sel}, kindly transfer Rs. 300 advance delivery charges "
                    f"via JazzCash/Easypaisa to confirm booking. Balance Rs. {order_val - 300:,.0f} will be paid on delivery. "
                    f"Reply with payment screenshot to confirm dispatch."
                )
            elif prediction["action_code"] == "WHATSAPP_CONFIRM":
                wa_message = (
                    f"Assalam-o-Alaikum! Your order of Rs. {order_val:,.0f} is being packed. "
                    f"Please confirm your delivery address: '{addr_sel.split(' (')[0]}' in {city_sel}. "
                    f"Kindly reply with '1' to CONFIRM or reply with updated house/street number so courier rider can reach smoothly."
                )
            else:
                wa_message = (
                    f"Assalam-o-Alaikum! Your order of Rs. {order_val:,.0f} is confirmed and dispatched via {courier_sel}. "
                    f"Tracking number will be shared shortly. Thank you for shopping with us!"
                )
            st.code(wa_message, language="text")
            st.caption("Copy and send directly to customer on WhatsApp before booking airway bill.")

# -----------------------------------------------------------------------------
# TAB 2: PAKISTAN CITY COD BENCHMARKS
# -----------------------------------------------------------------------------
with tab_benchmarks:
    st.markdown("### 🗺️ City & Regional COD Return (RTO) Benchmarks")
    st.markdown(
        "Pakistani e-commerce logistics vary drastically by geography. Metropolitan Tier 1 cities boast lower return rates (~11-15%), "
        "while rural and distant outskirts face delivery delays and return rates soaring beyond 40%."
    )

    city_df = ApiClient.get_city_benchmarks()
    
    b1, b2 = st.columns([55, 45])
    with b1:
        fig_rto = plot_city_rto_barchart(city_df)
        st.plotly_chart(fig_rto, use_container_width=True)

    with b2:
        st.markdown("#### 📋 Detailed Regional Reference")
        st.dataframe(
            city_df[["City", "Tier", "Zone", "Average COD RTO %", "Avg Delivery Days", "Coverage Quality"]],
            use_container_width=True,
            hide_index=True,
            height=450
        )

# -----------------------------------------------------------------------------
# TAB 3: COURIER TARIFFS & PERFORMANCE
# -----------------------------------------------------------------------------
with tab_couriers:
    st.markdown("### 🚚 Pakistan Courier Performance & Tariff Benchmarks")
    st.markdown("Compare delivery rates, COD handling fees, return charges, and typical transit days across major Pakistani courier services.")

    couriers = ApiClient.get_couriers()
    
    cour_cols = st.columns(len(couriers))
    for idx, c in enumerate(couriers):
        with cour_cols[idx]:
            st.html(f"""
                <div class="custom-card" style="border-top: 3px solid #38BDF8; height: 100%;">
                    <div style="font-size: 0.80rem; color: #94A3B8;">RATING: ⭐ {c['rating']}</div>
                    <h3 style="margin: 4px 0 10px 0; color: #F8FAFC; font-size: 1.15rem;">{c['name']}</h3>
                    
                    <div style="background: #0F172A; padding: 8px 12px; border-radius: 6px; font-size: 0.82rem; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="color: #64748B;">Base Delivery:</span>
                            <strong style="color: #10B981;">₨ {c['base_rate_pkr']}</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="color: #64748B;">COD Handling Fee:</span>
                            <strong style="color: #F8FAFC;">{c['cod_fee_pct']}%</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="color: #64748B;">Return Penalty:</span>
                            <strong style="color: #EF4444;">₨ {c['return_charge_pkr']}</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #64748B;">Avg Delivery SLA:</span>
                            <strong style="color: #38BDF8;">{c['avg_sla_days']} Days</strong>
                        </div>
                    </div>

                    <div style="font-size: 0.80rem; color: #94A3B8;">
                        🎯 <strong>Best For:</strong> {c['best_for']}
                    </div>
                </div>
            """)
