"""
components/charts.py
Plotly analytics charts styled specifically for dark/slate eCommerce theme.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

CHART_THEME = {
    "paper_bgcolor": "#1E293B",
    "plot_bgcolor": "#1E293B",
    "font": {"color": "#F8FAFC", "family": "Inter, sans-serif"},
    "margin": dict(l=30, r=30, t=40, b=30)
}

def plot_demand_timeline(curve_data: List[Dict[str, Any]]) -> go.Figure:
    """Plot the annual Pakistani eCommerce demand spike curve with seasonal milestones."""
    df = pd.DataFrame(curve_data)
    
    fig = go.Figure()

    # Base Area
    fig.add_trace(go.Scatter(
        x=df["month"],
        y=df["demand_index"],
        mode="lines+markers",
        line=dict(color="#10B981", width=3, shape="spline"),
        marker=dict(size=8, color="#059669", line=dict(width=2, color="#FFFFFF")),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.12)",
        text=df.apply(lambda r: f"<b>{r['month']}</b>: {r['event']}<br>Demand Index: {r['demand_index']}/100<br>Sales Multiplier: {r['typical_gmv_multiplier']}", axis=1),
        hoverinfo="text",
        name="Market Demand Index"
    ))

    # Add peak milestone annotations
    fig.add_annotation(
        x="Mar", y=100,
        text="🌙 Ramadan & Eid Peak (3.2x)",
        showarrow=True, arrowhead=2, arrowcolor="#10B981", arrowsize=1,
        font=dict(size=11, color="#10B981"),
        bgcolor="#064E3B", bordercolor="#10B981", borderpad=4
    )

    fig.add_annotation(
        x="Nov", y=98,
        text="🛍️ 11.11 Blessed Friday (3.8x)",
        showarrow=True, arrowhead=2, arrowcolor="#38BDF8", arrowsize=1,
        font=dict(size=11, color="#38BDF8"),
        bgcolor="#0C4A6E", bordercolor="#38BDF8", borderpad=4
    )

    fig.update_layout(
        title="<b>Pakistan E-Commerce Demand Curve & Seasonal Sales Multipliers</b>",
        title_font=dict(size=16, color="#F8FAFC"),
        xaxis=dict(
            title="",
            gridcolor="#334155",
            showline=True,
            linecolor="#334155"
        ),
        yaxis=dict(
            title="Relative Demand Index (0-100)",
            gridcolor="#334155",
            range=[40, 110]
        ),
        hovermode="closest",
        **CHART_THEME
    )
    return fig

def plot_margin_waterfall(pricing: Dict[str, Any]) -> go.Figure:
    """Waterfall chart visualizing unit economics and COD return drag per order."""
    bd = pricing.get("breakdown", {})
    selling_price = float(pricing.get("discounted_price", 0.0))
    net_profit = float(pricing.get("net_profit_per_order", 0.0))

    if not bd:
        bd = {
            "cogs": pricing.get("sourcing_cost", 0.0),
            "ad_spend": pricing.get("ad_spend_total", 0.0) / max(float(pricing.get("delivered_orders_per_100", 1)) or 1, 1),
            "outbound_shipping": pricing.get("outbound_shipping_total", 0.0) / max(float(pricing.get("delivered_orders_per_100", 1)) or 1, 1),
            "packaging": pricing.get("packaging_total", 0.0) / max(float(pricing.get("delivered_orders_per_100", 1)) or 1, 1),
            "reverse_shipping_drag": pricing.get("rto_loss_penalty_per_order", 0.0),
        }
    
    measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "total"]
    x = ["Selling Price", "Sourcing (COGS)", "Ad Spend (CAC)", "Courier Fee", "Packaging", "RTO Freight Drag", "Blended Net Profit"]
    y = [
        selling_price,
        -float(bd.get("cogs", 0.0)),
        -float(bd.get("ad_spend", 0.0)),
        -float(bd.get("outbound_shipping", 0.0)),
        -float(bd.get("packaging", 0.0)),
        -float(bd.get("reverse_shipping_drag", 0.0)),
        net_profit
    ]

    fig = go.Figure(go.Waterfall(
        name="Unit Margin",
        orientation="v",
        measure=measure,
        x=x,
        textposition="outside",
        text=[f"₨{val:+,.0f}" if i > 0 and i < 6 else f"₨{val:,.0f}" for i, val in enumerate(y)],
        y=y,
        connector={"line": {"color": "#64748B"}},
        decreasing={"marker": {"color": "#EF4444"}},
        increasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#10B981" if net_profit >= 0 else "#EF4444"}}
    ))

    fig.update_layout(
        title=f"<b>Order Unit Economics & Cashflow Breakdown (Delivered vs RTO Loss)</b>",
        title_font=dict(size=15, color="#F8FAFC"),
        yaxis=dict(title="Pakistani Rupees (₨)", gridcolor="#334155"),
        xaxis=dict(gridcolor="#334155"),
        **CHART_THEME
    )
    return fig

def plot_city_rto_barchart(city_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart comparing COD Return rates across Pakistan cities and tiers."""
    # Assign color by tier
    colors = []
    for tier in city_df["Tier"]:
        if "Tier 1" in tier:
            colors.append("#10B981")  # Green
        elif "Tier 2" in tier:
            colors.append("#F59E0B")  # Amber
        else:
            colors.append("#EF4444")  # Red

    fig = go.Figure(go.Bar(
        x=city_df["Average COD RTO %"],
        y=city_df["City"],
        orientation='h',
        marker=dict(color=colors, line=dict(color="#0F172A", width=1)),
        text=city_df["Average COD RTO %"].apply(lambda v: f"{v}%"),
        textposition="outside",
        hovertext=city_df.apply(lambda r: f"<b>{r['City']}</b> ({r['Tier']})<br>Zone: {r['Zone']}<br>RTO Rate: {r['Average COD RTO %']}%<br>Delivery: {r['Avg Delivery Days']} days", axis=1),
        hoverinfo="text"
    ))

    fig.update_layout(
        title="<b>COD Return (RTO) Rate Benchmark by City & Tier</b>",
        title_font=dict(size=15, color="#F8FAFC"),
        xaxis=dict(title="Historical COD Return Rate %", gridcolor="#334155", range=[0, 60]),
        yaxis=dict(autorange="reversed", gridcolor="#334155"),
        height=450,
        **CHART_THEME
    )
    return fig

def plot_opportunity_matrix(products: List[Dict[str, Any]]) -> go.Figure:
    """Scatter matrix mapping Opportunity Score vs Sourcing Wholesale Cost."""
    df = pd.DataFrame(products)
    
    fig = px.scatter(
        df,
        x="sourcing_cost",
        y="opportunity_score",
        size="suggested_retail_price",
        color="category",
        hover_name="name",
        hover_data={
            "sourcing_cost": ":₨,.0f",
            "suggested_retail_price": ":₨,.0f",
            "wholesale_hub": True,
            "opportunity_score": True,
            "profit_margin_delivered_pct": ":.1f%"
        },
        title="<b>Opportunity Matrix: Sourcing Cost vs Opportunity Score</b>",
        labels={
            "sourcing_cost": "Wholesale Sourcing Cost (₨)",
            "opportunity_score": "Market Opportunity Score (0-100)"
        }
    )

    fig.update_layout(
        xaxis=dict(gridcolor="#334155"),
        yaxis=dict(gridcolor="#334155", range=[75, 102]),
        **CHART_THEME
    )
    return fig
