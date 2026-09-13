"""
pages/4_My_Store.py
Module 5: Store Inventory Predictor & Dead Stock Liquidation.
Analyzes seller inventory against upcoming Pakistani event spikes,
flags imminent stockouts, and generates actionable liquidation and bundling plans.
"""

import streamlit as st
import pandas as pd
from utils.api_client import ApiClient
from components.layout import apply_custom_styles, render_market_ticker, render_page_header
from components.cards import render_metric_card

st.set_page_config(
    page_title="My Store Inventory Predictor | Pakistan E-Commerce Intelligence",
    page_icon="🏬",
    layout="wide"
)

apply_custom_styles()
render_market_ticker()

render_page_header(
    title="Store Inventory Predictor & Dead Stock Liquidation",
    subtitle="Align your Shopify or WooCommerce inventory with upcoming Pakistani seasonal demand surges to scale winners and clear dead stock.",
    badge="MODULE 5 · STORE PREDICTOR"
)

# Upload or demo choice
st.markdown("#### 📂 Inventory Data Source")
source_col1, source_col2 = st.columns([60, 40])

with source_col1:
    data_mode = st.radio(
        "Choose Data Source:",
        ["Load Pre-Configured Pakistani Apparel & Gadget Store (Demo)", "Upload Store Inventory CSV (Shopify/WooCommerce format)"],
        horizontal=True
    )

uploaded_file = None
if data_mode == "Upload Store Inventory CSV (Shopify/WooCommerce format)":
    uploaded_file = st.file_uploader("Upload CSV containing (SKU, Title, Category, Stock, Unit Cost, Selling Price)", type=["csv"])

# Load inventory data
if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        st.success("Custom inventory CSV uploaded successfully!")
        # Normalize columns if needed
        inventory_items = raw_df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error parsing uploaded CSV: {e}")
        inventory_items = ApiClient.get_store_inventory()
else:
    inventory_items = ApiClient.get_store_inventory()

# Convert to DataFrame for calculations
inv_df = pd.DataFrame(inventory_items)

# Normalize API and uploaded CSV naming differences for the dashboard.
if "daily_sales_velocity" not in inv_df.columns:
    monthly_velocity = pd.to_numeric(
        inv_df["monthly_velocity"] if "monthly_velocity" in inv_df else pd.Series(0, index=inv_df.index),
        errors="coerce",
    ).fillna(0)
    inv_df["daily_sales_velocity"] = monthly_velocity / 30.0
if "days_of_supply" not in inv_df.columns:
    inv_df["days_of_supply"] = inv_df["days_of_inventory"] if "days_of_inventory" in inv_df else 0
inv_df["daily_sales_velocity"] = pd.to_numeric(inv_df["daily_sales_velocity"], errors="coerce").fillna(0)
inv_df["days_of_supply"] = pd.to_numeric(inv_df["days_of_supply"], errors="coerce").fillna(0)

# Calculate financial metrics
inv_df["total_inventory_value"] = inv_df["stock"] * inv_df["unit_cost"]
inv_df["total_retail_value"] = inv_df["stock"] * inv_df["selling_price"]
inv_df["projected_margin_pct"] = ((inv_df["selling_price"] - inv_df["unit_cost"]) / inv_df["selling_price"] * 100).round(1)

total_cost_val = inv_df["total_inventory_value"].sum()
total_retail_val = inv_df["total_retail_value"].sum()

dead_stock_mask = inv_df["status"].str.contains("Dead Stock|Slow Mover", case=False, na=False)
dead_capital = inv_df.loc[dead_stock_mask, "total_inventory_value"].sum()
dead_units = inv_df.loc[dead_stock_mask, "stock"].sum()

stockout_mask = inv_df["status"].str.contains("Stockout", case=False, na=False)
stockout_count = stockout_mask.sum()

stars_mask = inv_df["status"].str.contains("Star|Healthy", case=False, na=False)
stars_count = stars_mask.sum()

# Top KPI Summary Cards
k1, k2, k3, k4 = st.columns(4)

with k1:
    render_metric_card(
        label="Total Working Capital in Stock",
        value=f"₨ {total_cost_val:,.0f}",
        subtext=f"Retail Value: ₨ {total_retail_val:,.0f}",
        delta=f"{len(inv_df)} Active SKUs",
        delta_color="#38BDF8"
    )

with k2:
    render_metric_card(
        label="Capital Tied in Dead Stock",
        value=f"₨ {dead_capital:,.0f}",
        subtext=f"{dead_units} Units slow-moving or frozen",
        delta="Liquidation Urgency",
        delta_color="#EF4444"
    )

with k3:
    render_metric_card(
        label="Stockout Warnings",
        value=f"{stockout_count} SKUs",
        subtext="Supply < 10 days at current velocity",
        delta="Reorder Immediately",
        delta_color="#F59E0B"
    )

with k4:
    render_metric_card(
        label="Event Stars & Scalable SKUs",
        value=f"{stars_count} SKUs",
        subtext="Directly aligned with Ramadan & Eid surge",
        delta="Ready for Ad Scaling",
        delta_color="#10B981"
    )

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INVENTORY HEALTH BREAKDOWN TABS
# -----------------------------------------------------------------------------
tab_stars, tab_stockouts, tab_deadstock = st.tabs([
    "⭐ Event Stars (Scale Advertising)",
    "⚠️ Stockout Alerts (Reorder Now)",
    "💸 Dead Stock Liquidation & Bundles"
])

with tab_stars:
    st.markdown("### ⭐ Event Stars Aligned with Ramadan & Eid Demand")
    st.markdown("These products have high customer demand velocity and sufficient inventory to support aggressive Meta & TikTok ad spend.")
    
    star_items = inv_df[stars_mask]
    for _, item in star_items.iterrows():
        st.html(f"""
            <div class="custom-card" style="border-left: 4px solid #10B981; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="card-badge-green">{item['status']}</span>
                        <h4 style="margin: 6px 0 2px 0; color: #F8FAFC;">{item['title']}</h4>
                        <span style="font-size: 0.85rem; color: #94A3B8;">SKU: {item['sku']} • Category: {item['category']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.25rem; font-weight: 800; color: #10B981;">₨ {item['selling_price']:,}</span>
                        <div style="font-size: 0.82rem; color: #94A3B8;">Cost: ₨ {item['unit_cost']:,} ({item['projected_margin_pct']}% margin)</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; background: #0F172A; padding: 10px 14px; border-radius: 8px; margin-top: 10px; font-size: 0.85rem;">
                    <div>In Stock: <strong style="color: #F8FAFC;">{item['stock']} Units</strong></div>
                    <div>Daily Velocity: <strong style="color: #10B981;">{item['daily_sales_velocity']} units/day</strong></div>
                    <div>Runway: <strong style="color: #38BDF8;">{item['days_of_supply']} Days of Supply</strong></div>
                </div>
            </div>
        """)

with tab_stockouts:
    st.markdown("### ⚠️ Imminent Stockout Warnings")
    st.markdown("High-velocity items that will run out before peak Eid dispatches if reorders are not initiated immediately.")
    
    stockout_items = inv_df[stockout_mask]
    for _, item in stockout_items.iterrows():
        st.html(f"""
            <div class="custom-card" style="border-left: 4px solid #F59E0B; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="card-badge-amber">{item['status']}</span>
                        <h4 style="margin: 6px 0 2px 0; color: #F8FAFC;">{item['title']}</h4>
                        <span style="font-size: 0.85rem; color: #94A3B8;">SKU: {item['sku']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.25rem; font-weight: 800; color: #F59E0B;">Only {item['stock']} Units Left</span>
                        <div style="font-size: 0.82rem; color: #EF4444; font-weight: 700;">Stockouts in ~{item['days_of_supply']} Days!</div>
                    </div>
                </div>
                <div style="background: rgba(245, 158, 11, 0.10); border: 1px solid #F59E0B; padding: 10px 14px; border-radius: 8px; margin-top: 10px; font-size: 0.85rem; color: #F8FAFC;">
                    🚨 <strong>Recommended Action:</strong> Place reorder of at least <strong>100 units</strong> with wholesale supplier to avoid leaving an estimated <strong>₨ {(100 * (item['selling_price'] - item['unit_cost'])):,.0f} in gross profit</strong> on the table during Ramadan peak.
                </div>
            </div>
        """)

with tab_deadstock:
    st.markdown("### 💸 Dead Stock Liquidation & Smart Bundling Engine")
    st.markdown(
        "Tied-up working capital kills cash flow. Rather than taking severe losses, bundle slow-moving SKUs with hot festive items "
        "or launch flash clearance promotions."
    )

    dead_items = inv_df[dead_stock_mask]
    for _, item in dead_items.iterrows():
        st.html(f"""
            <div class="custom-card" style="border-left: 4px solid #EF4444; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span class="card-badge-red">{item['status']}</span>
                        <h4 style="margin: 6px 0 2px 0; color: #F8FAFC;">{item['title']}</h4>
                        <span style="font-size: 0.85rem; color: #94A3B8;">SKU: {item['sku']} • Category: {item['category']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.15rem; font-weight: 800; color: #EF4444;">₨ {item['total_inventory_value']:,.0f} Tied Up</span>
                        <div style="font-size: 0.82rem; color: #94A3B8;">{item['stock']} Units • Velocity: {item['daily_sales_velocity']} units/day</div>
                    </div>
                </div>

                <div style="background: #0F172A; padding: 12px; border-radius: 8px; margin-top: 12px;">
                    <div style="font-weight: 700; color: #38BDF8; font-size: 0.90rem; margin-bottom: 6px;">
                        💡 Smart Liquidation Strategy:
                    </div>
                    <div style="font-size: 0.88rem; color: #CBD5E1;">
                        <strong>1. Festive Bundle Option:</strong> Offer as an add-on at <em>₨ {item['unit_cost'] + 200:,}</em> (30% off retail) when a customer buys a trending Eid suit. This recovers your full capital <strong>₨ {item['unit_cost']:,}</strong> while increasing Average Order Value (AOV).<br>
                        <strong>2. Flash Clearance Option:</strong> Run a 48-hour 'Pre-Ramadan Clearance' at <strong>₨ {item['unit_cost'] * 1.15:,.0f}</strong> on TikTok Shop.
                    </div>
                </div>
            </div>
        """)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.markdown("### 📊 Complete Store Inventory Table")
st.dataframe(
    inv_df[["sku", "title", "category", "stock", "unit_cost", "selling_price", "daily_sales_velocity", "days_of_supply", "projected_margin_pct", "status"]],
    use_container_width=True,
    hide_index=True
)
