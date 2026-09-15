"""
pages/2_Winning_Products.py
Module 2 & 3: Hot Product Finder & Smart Price & Margin Protector.
Discovers high-opportunity products tailored for Pakistani shopping seasons
and simulates real net profit, COD return drag, and break-even ROAS.
"""

import streamlit as st
import pandas as pd
from utils.api_client import ApiClient
from utils.sourcing_contacts import get_sourcing_contact
from components.layout import apply_custom_styles, render_market_ticker, render_page_header
from components.cards import render_metric_card
from components.charts import plot_opportunity_matrix, plot_margin_waterfall

st.set_page_config(
    page_title="Winning Products & Margin Protector | Pakistan E-Commerce Intelligence",
    page_icon="🛍️",
    layout="wide"
)

apply_custom_styles()
render_market_ticker()

render_page_header(
    title="Hot Product & Demand Finder + Smart Margin Protector",
    subtitle="Discover high-velocity winning items with verified Pakistani wholesale hubs, then simulate safe pricing after COD return losses.",
    badge="MODULE 2 & 3 · PROFIT INTELLIGENCE"
)

tab_finder, tab_margin = st.tabs(["🔥 Winning Products Catalog", "🛡️ Smart Price & Margin Protector"])

# -----------------------------------------------------------------------------
# TAB 1: WINNING PRODUCTS CATALOG
# -----------------------------------------------------------------------------
with tab_finder:
    # Filter controls
    f1, f2, f3, f4 = st.columns([25, 25, 25, 25])
    
    with f1:
        events = ApiClient.get_events()
        event_options = ["All Events"] + [e["name"] for e in events]
        selected_event_name = st.selectbox("Filter by Upcoming Event", event_options)
        event_id_filter = None
        if selected_event_name != "All Events":
            for e in events:
                if e["name"] == selected_event_name:
                    event_id_filter = e["id"]
                    break

    with f2:
        categories = ApiClient.get_categories(event_id_filter)
        selected_cat = st.selectbox("Filter by Category", categories)

    with f3:
        min_opp = st.slider("Minimum Opportunity Score", min_value=70, max_value=98, value=80, step=1)

    with f4:
        sort_by = st.selectbox(
            "Sort Catalog By",
            [
                "Opportunity Score (High to Low)",
                "Profit Margin %",
                "Wholesale Price (Low to High)",
                "Retail Price (High to Low)"
            ]
        )

    products = ApiClient.get_winning_products(
        event_id=event_id_filter,
        category=selected_cat,
        min_opportunity=min_opp,
        sort_by=sort_by
    )

    st.markdown(f"**Showing {len(products)} high-opportunity items for current market conditions:**")
    if not products:
        if event_id_filter:
            st.info(
                "No catalog items match this event and the selected score threshold. "
                "Choose another event/category or select All Events to browse the full catalog."
            )
        else:
            st.info(
                "No catalog items match the selected category and score threshold. "
                "Lower the minimum opportunity score or choose another category."
            )

    # Display product cards in grid
    cols = st.columns(2)
    for idx, prod in enumerate(products):
        with cols[idx % 2]:
            st.html(f"""
                <div class="custom-card" style="border-left: 4px solid #10B981; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="card-badge-green">Score: {prod['opportunity_score']}/100</span>
                            <span style="color: #64748B; font-size: 0.85rem; margin-left: 8px;">{prod['category']}</span>
                        </div>
                        <span class="card-badge-amber">Default RTO: {prod['return_risk_default']}</span>
                    </div>
                    
                    <h3 style="margin: 10px 0 4px 0; color: #F8FAFC; font-size: 1.25rem;">{prod['name']}</h3>
                    <div style="font-size: 0.92rem; color: #10B981; font-weight: 600; margin-bottom: 12px;">{prod['name_ur']}</div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; background: #0F172A; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                        <div>
                            <span style="color: #64748B; font-size: 0.80rem; display: block;">Wholesale Sourcing:</span>
                            <strong style="color: #38BDF8; font-size: 1.15rem;">₨ {prod['sourcing_cost']:,}</strong>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 0.80rem; display: block;">Suggested Selling:</span>
                            <strong style="color: #10B981; font-size: 1.15rem;">₨ {prod['suggested_retail_price']:,}</strong>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 0.80rem; display: block;">Est. Net Margin:</span>
                            <strong style="color: #F8FAFC; font-size: 1.15rem;">~{prod['profit_margin_delivered_pct']}%</strong>
                        </div>
                    </div>

                    <div style="font-size: 0.86rem; margin-bottom: 8px;">
                        🏢 <strong>Local Wholesale Hub:</strong> <span style="color: #E2E8F0;">{prod['wholesale_hub']}</span>
                    </div>

                    <div style="display: flex; gap: 15px; font-size: 0.84rem; color: #94A3B8; margin-bottom: 10px;">
                        <span>📈 Trend: <strong style="color: #10B981;">{prod.get('demand_trend', 'Market trend unavailable')}</strong></span>
                        <span>🔍 Searches: <strong style="color: #F8FAFC;">{prod.get('search_volume_pk', 'N/A')}</strong></span>
                        <span>🥊 Competition: <strong style="color: #F59E0B;">{prod.get('competition_level', 'Not assessed')}</strong></span>
                    </div>

                    <div style="background: rgba(255,255,255,0.02); padding: 8px 12px; border-radius: 6px; font-size: 0.83rem;">
                        <strong style="color: #CBD5E1;">Key Selling Angle:</strong> {prod.get('selling_points', ['Review product positioning before launch.'])[0]}
                    </div>
                </div>
            """)
            contact = get_sourcing_contact(prod.get("wholesale_hub", ""))
            listing_url = contact.get("listing_url")
            if not listing_url:
                listing_url = "https://www.google.com/maps/search/?api=1&query=wholesale+supplier"
            verified_on = contact.get("verified_on", "Not available")
            phone_label = (
                f"☎️ {contact['phone']}"
                if contact.get("phone")
                else "☎️ Phone: Not publicly verified"
            )
            st.info(
                f"**Sourcing contact — {contact['store_name']} ({contact['city']})**  \n"
                f"{phone_label}  \n"
                f"**How to contact:** {contact['contact_method']}  \n"
                f"_{contact['verification']}. Do not send advance payment until the supplier is verified._"
            )
            st.link_button(
                "Open public supplier listings",
                listing_url,
                key=f"sourcing-listing-{prod['id']}",
                use_container_width=True,
            )
            st.caption(
                f"Checked: {verified_on} · Open the listing to see current "
                "business details and verify the store name before ordering."
            )

    # Opportunity Matrix Chart
    if products:
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        fig_matrix = plot_opportunity_matrix(products)
        st.plotly_chart(fig_matrix, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: SMART PRICE & MARGIN PROTECTOR
# -----------------------------------------------------------------------------
with tab_margin:
    st.markdown("### 🛡️ Real Net Profit & Break-Even Simulator")
    st.markdown(
        "Many Pakistani sellers make the fatal mistake of calculating profit as `Selling Price - Sourcing Cost - Ad Spend`. "
        "In Pakistan's COD environment, **15% to 35% of parcels return (RTO)**, incurring double courier costs and wasted packaging. "
        "Use this calculator to find your **true blended profit and break-even ROAS**."
    )

    # Allow merchant to pre-fill from winning product catalog or enter custom
    preset_choice = st.selectbox(
        "Auto-fill preset values from a winning product or enter custom numbers:",
        ["Custom Product"] + [f"{p['name']} (₨{p['suggested_retail_price']:,})" for p in products]
    )

    # Defaults
    def_sourcing = 1850.0
    def_price = 3899.0
    def_ad = 650.0
    def_courier = 260.0
    def_pack = 50.0

    if preset_choice != "Custom Product":
        selected_title = preset_choice.split(" (₨")[0]
        match_prod = next((p for p in products if p['name'] == selected_title), None)
        if match_prod:
            def_sourcing = float(match_prod["sourcing_cost"])
            def_price = float(match_prod["suggested_retail_price"])
            def_ad = float(match_prod["typical_ad_cac"])
            def_courier = float(match_prod["typical_courier_fee"])
            def_pack = float(match_prod["packaging_cost"])

    sim_col1, sim_col2 = st.columns([40, 60])

    with sim_col1:
        st.markdown("#### ⚙️ Order Unit Economics Inputs")
        
        inp_price = st.number_input("Retail Selling Price (PKR ₨)", min_value=500.0, max_value=50000.0, value=def_price, step=100.0)
        inp_cost = st.number_input("Wholesale Sourcing Cost (PKR ₨)", min_value=100.0, max_value=30000.0, value=def_sourcing, step=50.0)
        inp_ad = st.number_input("Meta / TikTok Ad CAC per Order (PKR ₨)", min_value=50.0, max_value=5000.0, value=def_ad, step=25.0)
        inp_courier = st.number_input("Outbound Courier Delivery Fee (PKR ₨)", min_value=150.0, max_value=800.0, value=def_courier, step=10.0)
        inp_pack = st.number_input("Flyer & Packaging Material (PKR ₨)", min_value=10.0, max_value=300.0, value=def_pack, step=5.0)
        
        st.markdown("##### 🚚 COD Return & Logistics Risk Factors")
        inp_rto = st.slider("Expected COD Return Rate (RTO %)", min_value=0.0, max_value=60.0, value=22.0, step=1.0)
        inp_reverse = st.number_input("Courier Reverse Return Penalty (PKR ₨)", min_value=50.0, max_value=400.0, value=160.0, step=10.0)
        inp_discount = st.slider("Sale Discount to Apply (%)", min_value=0.0, max_value=50.0, value=0.0, step=1.0)

    # Run calculation via service client
    pricing_result = ApiClient.calculate_margin_and_pricing(
        sourcing_cost=inp_cost,
        selling_price=inp_price,
        ad_cac=inp_ad,
        courier_fee=inp_courier,
        packaging_cost=inp_pack,
        return_rate_pct=inp_rto,
        return_courier_charge=inp_reverse,
        discount_pct=inp_discount
    )

    with sim_col2:
        st.markdown("#### 📊 Real Profit & Margin Assessment")

        # Health Banner
        status_label = pricing_result.get("status") or pricing_result.get("verdict", "UNKNOWN")
        health_color = pricing_result.get("status_color") or pricing_result.get("verdict_color", "#10B981")
        st.html(f"""
            <div style="background: rgba(16,185,129,0.12); border: 1px solid {health_color}; border-radius: 10px; padding: 12px 18px; margin-bottom: 16px;">
                <span style="font-size: 0.80rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">PROFIT HEALTH STATUS</span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #F8FAFC;">
                    {status_label}
                </div>
            </div>
        """)

        res1, res2, res3 = st.columns(3)
        with res1:
            render_metric_card(
                label="Blended Net Profit",
                value=f"₨ {pricing_result['net_profit_per_order']:,.0f}",
                subtext="Per dispatched order after RTO loss",
                delta=f"{pricing_result['net_margin_pct']}% Net Margin",
                delta_color="#10B981" if pricing_result['net_profit_per_order'] >= 0 else "#EF4444"
            )
        with res2:
            render_metric_card(
                label="Break-Even ROAS",
                value=f"{pricing_result['breakeven_roas']:.2f}x",
                subtext="Minimum Meta Ad ROAS needed",
                delta="Ad Profitability Threshold",
                delta_color="#38BDF8"
            )
        with res3:
            render_metric_card(
                label="Max Safe Discount",
                value=f"{pricing_result.get('max_allowable_discount_pct', pricing_result.get('max_safe_discount_pct', 0))}%",
                subtext="Maximum discount before losing money",
                delta=f"Min Safe Price: ₨{pricing_result.get('breakeven_selling_price', pricing_result.get('discounted_price', 0)):,.0f}",
                delta_color="#F59E0B"
            )

        # Waterfall visualizer
        fig_waterfall = plot_margin_waterfall(pricing_result)
        st.plotly_chart(fig_waterfall, use_container_width=True)

        # Critical notice
        st.info(
            f"💡 **COD Return Drag Impact:** Out of 100 orders, you deliver {pricing_result.get('delivered_orders_per_100', max(0, 100 - inp_rto))} and "
            f"get {pricing_result.get('returned_orders_per_100', inp_rto)} returned. "
            f"Each returned parcel costs you **₨ {inp_courier + inp_reverse + inp_pack:,.0f} in lost shipping & packaging** plus wasted ad spend. "
            f"COD returns reduce your ideal profit by **₨ {pricing_result.get('rto_loss_penalty_per_order', 0):,.0f} per order**!"
        )
