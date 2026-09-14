"""
components/cards.py
Reusable visual metric cards, event countdown widgets, and product display cards.
"""

import streamlit as st
from typing import Dict, Any, Optional

def render_metric_card(
    label: str,
    value: str,
    subtext: str,
    delta: Optional[str] = None,
    delta_color: str = "#10B981",
    badge: Optional[str] = None
):
    """Render a modern styled KPI metric card."""
    badge_html = f'<span class="card-badge-green" style="float: right;">{badge}</span>' if badge else ''
    delta_html = f'<span style="color: {delta_color}; font-weight: 700; font-size: 0.9rem;">{delta}</span>' if delta else ''
    
    st.html(f"""
        <div class="custom-card">
            <div class="card-label">
                {label} {badge_html}
            </div>
            <div class="card-value">
                {value}
            </div>
            <div class="card-subtext">
                {delta_html} {subtext}
            </div>
        </div>
    """)

def render_event_card(event: Dict[str, Any]):
    """Render a rich event calendar intelligence card.
    
    Shows:
    - LIVE NOW badge for currently active events
    - Past Analysis section (data-backed)
    - Future Forecast section (predictive)
    - Clickable anchor link for deep-linking to event
    """
    from datetime import date, datetime
    
    days = event.get("days_remaining", 0)
    event_id = event.get("id", "")
    
    # Determine the event phase from dates so labels stay accurate over time.
    try:
        today = date.today()
        start_d = datetime.strptime(event["start_date"], "%Y-%m-%d").date()
        end_d = datetime.strptime(event["end_date"], "%Y-%m-%d").date()
        is_live = start_d <= today <= end_d
        event_phase = "Current" if is_live else "Upcoming" if start_d > today else "Past"
    except Exception:
        is_live = False
        event_phase = event.get("event_phase", "Upcoming")
    
    # Badge color logic
    if is_live:
        urgency_badge_class = "card-badge-green"
        status_text = "🟢 LIVE NOW"
        border_color = "#10B981"
        days_label = "Days left this month"
    elif days <= 30:
        urgency_badge_class = "card-badge-red"
        status_text = event.get("status", "High Urgency")
        border_color = "#EF4444"
        days_label = "days to start"
    elif days <= 60:
        urgency_badge_class = "card-badge-amber"
        status_text = event.get("status", "Upcoming")
        border_color = "#F59E0B"
        days_label = "days to start"
    else:
        urgency_badge_class = "card-badge-green"
        status_text = event.get("status", "Long-Term")
        border_color = "#3B82F6"
        days_label = "days to start"
    
    # Parse description: split on \n\n to get Past Analysis vs Forecast
    raw_desc = event.get("description", "")
    if "🔮" in raw_desc and "📊" in raw_desc:
        parts = raw_desc.split("\n\n", 1)
        past_part = parts[0].replace("📊 Past Analysis →", "<strong style='color:#94A3B8;'>📊 Past Analysis</strong> →")
        future_part = parts[1].replace("🔮", "<strong style='color:#10B981;'>🔮 Forecast</strong>") if len(parts) > 1 else ""
        desc_html = f"""
            <div style='background:#0F172A; border-left:3px solid #475569; padding:10px 14px; border-radius:6px; margin-bottom:8px; font-size:0.88rem; color:#CBD5E1;'>
                {past_part}
            </div>
            <div style='background:#052e16; border-left:3px solid #10B981; padding:10px 14px; border-radius:6px; font-size:0.88rem; color:#CBD5E1;'>
                {future_part}
            </div>
        """
    else:
        desc_html = f"<p style='color:#CBD5E1; font-size:0.92rem;'>{raw_desc}</p>"
    
    # Anchor id for clickable linking
    anchor_id = f"event-{event_id}"
    live_banner = ""
    if is_live:
        live_banner = """
            <div style='background: linear-gradient(90deg, #052e16, #064e3b); border: 1px solid #10B981;
                        padding: 6px 14px; border-radius: 6px; margin-bottom: 10px;
                        font-size: 0.82rem; color: #34D399; font-weight: 700; letter-spacing: 0.05em;'>
                ✅ THIS EVENT IS HAPPENING RIGHT NOW — Act on inventory & ads immediately!
            </div>
        """
    
    phase_icon = "🟢" if event_phase == "Current" else "📅"
    phase_label = "LIVE NOW" if event_phase == "Current" else "UPCOMING"
    with st.expander(f"{phase_icon} {phase_label} · {event['name']} · {days} days", expanded=False):
        st.html(f"""
        <div id="{anchor_id}" class="custom-card" style="border-left: 4px solid {border_color};">
            {live_banner}
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <div>
                    <span style="font-size: 0.85rem; color: #10B981; font-weight: 600;">{event.get('hijri_date', '')}</span>
                    <h3 style="margin: 4px 0; font-size: 1.35rem; color: #F8FAFC;">{event['name']}</h3>
                    <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">{event.get('name_ur', '')}</p>
                </div>
                <div style="text-align: right;">
                    <span class="{urgency_badge_class}">{status_text}</span>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC; margin-top: 6px;">
                        {days} <span style="font-size: 0.85rem; color: #94A3B8;">{days_label}</span>
                    </div>
                    <a href="#{anchor_id}" style="font-size: 0.75rem; color: #3B82F6; text-decoration: none;">
                        🔗 #{event_id}
                    </a>
                </div>
            </div>
            
            <div style="margin: 12px 0;">
                {desc_html}
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; background: #0F172A; padding: 10px 14px; border-radius: 8px; margin-bottom: 12px; font-size: 0.85rem;">
                <div>
                    <span style="color: #64748B; display: block;">Projected Demand:</span>
                    <strong style="color: #10B981; font-size: 1.05rem;">+{event.get('demand_spike_pct', 0)}% Spike</strong>
                </div>
                <div>
                    <span style="color: #64748B; display: block;">Sourcing Cutoff:</span>
                    <strong style="color: #F59E0B;">{event.get('sourcing_cutoff', 'N/A')}</strong>
                </div>
                <div>
                    <span style="color: #64748B; display: block;">Courier Delivery Cutoff:</span>
                    <strong style="color: #EF4444;">{event.get('courier_cutoff', 'N/A')}</strong>
                </div>
            </div>

            <div style="margin-top: 10px;">
                <span style="font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Top Winning Niches:</span>
                <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px;">
                    {' '.join([f'<span class="card-badge-green" style="font-size: 0.76rem;">{cat}</span>' for cat in event.get('top_categories', [])])}
                </div>
            </div>
        </div>
        """)
        c1, c2 = st.columns([55, 45])
        with c1:
            st.markdown("#### Recommended Seller Milestone Checklist")
            for item in event.get("seller_checklist", []):
                st.markdown(f"- {item}")
        with c2:
            st.markdown("#### Courier & Logistics Advisory")
            st.warning(f"Logistics Notice: {event.get('courier_notes', 'N/A')}")
            st.markdown(f"Recommended Wholesale Lead Time: `{event.get('recommended_lead_time_days', 30)} Days` before event starts.")


def render_risk_result_box(prediction: Dict[str, Any]):
    """Renders the COD Risk Calculator prediction output box."""
    risk_color = prediction.get("color", "#F59E0B")
    risk_level = prediction.get("risk_tier", "Unknown Return Risk")
    rto_pct = prediction.get("predicted_rto_pct", 0.0)
    loss_risk = prediction.get("expected_reverse_loss_pkr", 0.0)
    action_label = prediction.get("action_label", "Review order before dispatch.")
    action_code = prediction.get("action_code", "REVIEW")
    
    st.html(f"""
        <div class="custom-card" style="border: 2px solid {risk_color}; background: #1E293B;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div>
                    <span style="font-size: 0.80rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">PREDICTIVE COD ASSESSMENT</span>
                    <h2 style="margin: 2px 0 0 0; color: {risk_color}; font-size: 1.8rem; font-weight: 800;">
                        {risk_level} ({rto_pct}% RTO Risk)
                    </h2>
                </div>
                <div style="text-align: right; background: #0F172A; padding: 10px 16px; border-radius: 8px;">
                    <span style="font-size: 0.75rem; color: #94A3B8; display: block;">LOSS IF RETURNED</span>
                    <span style="font-size: 1.3rem; font-weight: 800; color: #EF4444;">₨ {loss_risk:,.0f}</span>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.03); padding: 12px 16px; border-radius: 8px; margin-bottom: 14px;">
                <div style="font-weight: 600; color: #F8FAFC; margin-bottom: 4px;">
                    📌 Action Protocol: {action_code}
                </div>
                <div style="color: #CBD5E1; font-size: 0.92rem;">
                    {action_label}
                </div>
            </div>

            <div style="font-size: 0.85rem; font-weight: 700; color: #94A3B8; margin-bottom: 8px;">
                MANDATORY DISPATCH STEPS:
            </div>
            <div class="protocol-item"><span>👉</span><span style="margin-left: 8px;">{action_label}</span></div>
        </div>
    """)

def render_product_card(prod: Dict[str, Any]):
    """Renders a winning product card with sourcing and sales details."""
    hub_value = prod.get("wholesale_hub") or prod.get("sourcing_hub") or "N/A"
    hub_display = hub_value.split("/")[0] if isinstance(hub_value, str) else str(hub_value)
    description = prod.get("description") or "Market-validated product opportunity."

    st.html(f"""
        <div class="custom-card" style="border-top: 3px solid #10B981;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <span class="card-badge-green">Score: {prod['opportunity_score']}/100</span>
                <span style="color: #94A3B8; font-size: 0.80rem;">{prod['category']}</span>
            </div>
            <h4 style="margin: 8px 0 4px 0; color: #F8FAFC; min-height: 48px;">{prod['name']}</h4>
            <div style="font-size: 0.88rem; color: #10B981; margin-bottom: 10px;">{prod.get('name_ur', '')}</div>
            
            <div style="background: #0F172A; padding: 10px; border-radius: 8px; font-size: 0.85rem; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748B;">Wholesale Hub:</span>
                    <strong style="color: #CBD5E1;">{hub_display}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748B;">Wholesale Price:</span>
                    <strong style="color: #38BDF8;">₨ {prod['sourcing_cost']:,}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #64748B;">Retail Selling Price:</span>
                    <strong style="color: #10B981;">₨ {prod['suggested_retail_price']:,}</strong>
                </div>
            </div>

            <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 6px;">
                📈 <strong>Trend:</strong> {prod.get('demand_trend', 'N/A')}
            </div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap; font-size: 0.82rem; color: #CBD5E1; margin-bottom: 8px;">
                <span>📊 Margin: <strong style="color: #10B981;">{prod.get('profit_margin_delivered_pct', 0)}%</strong></span>
                <span>⚠️ RTO: <strong style="color: #F59E0B;">{prod.get('return_risk_default', 'N/A')}</strong></span>
                <span>🚚 Courier: <strong>{prod.get('recommended_courier', 'N/A')}</strong></span>
            </div>
            <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.45;">
                <strong style="color: #94A3B8;">Details:</strong> {description}
            </div>
        </div>
    """)
