"""
components/layout.py
Layout helpers, custom CSS styles, header styling, and market status ticker.
"""

from datetime import date, datetime
from html import escape

import streamlit as st

def apply_custom_styles():
    """Inject custom responsive styles tailored for modern analytics dashboards."""
    st.markdown("""
        <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Top header container */
        .market-ticker {
            background: linear-gradient(90deg, #064E3B 0%, #0F172A 100%);
            border: 1px solid #059669;
            border-radius: 10px;
            padding: 10px 18px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: #E2E8F0;
            font-size: 0.92rem;
        }

        .ticker-pill {
            background-color: #10B981;
            color: #064E3B;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.80rem;
            margin-right: 10px;
            display: inline-block;
        }

        /* Metric card styling */
        .custom-card {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            margin-bottom: 14px;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }

        .custom-card:hover {
            border-color: #059669;
            transform: translateY(-2px);
        }

        .courier-card {
            border-top: 3px solid #38BDF8;
            min-height: 330px;
            padding: 20px;
        }

        .courier-card__rating {
            color: #94A3B8;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
        }

        .courier-card__rating span {
            color: #FBBF24;
            letter-spacing: 0;
            margin-left: 6px;
        }

        .courier-card__title {
            color: #F8FAFC;
            font-size: 1.25rem;
            line-height: 1.25;
            min-height: 52px;
            margin: 10px 0 16px;
        }

        .courier-card__metrics {
            background: #0F172A;
            border: 1px solid #263449;
            border-radius: 10px;
            padding: 12px 14px;
        }

        .courier-card__metrics div {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 7px 0;
            border-bottom: 1px solid #1E293B;
            font-size: 0.82rem;
        }

        .courier-card__metrics div:last-child {
            border-bottom: 0;
        }

        .courier-card__metrics span {
            color: #94A3B8;
        }

        .courier-card__metrics strong {
            color: #F8FAFC;
            white-space: nowrap;
        }

        .courier-card__metrics .positive { color: #10B981; }
        .courier-card__metrics .negative { color: #F87171; }
        .courier-card__metrics .info { color: #38BDF8; }

        .courier-card__best {
            margin-top: 16px;
            color: #94A3B8;
            font-size: 0.82rem;
        }

        .courier-card__best span {
            color: #CBD5E1;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .courier-card__best p {
            color: #CBD5E1;
            line-height: 1.5;
            margin: 5px 0 0;
        }

        .card-label {
            font-size: 0.84rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        .card-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: #F8FAFC;
            line-height: 1.2;
            margin-bottom: 4px;
        }

        .card-subtext {
            font-size: 0.82rem;
            color: #64748B;
        }

        .card-badge-green {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid #10B981;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.78rem;
        }

        .card-badge-amber {
            background-color: rgba(245, 158, 11, 0.15);
            color: #F59E0B;
            border: 1px solid #F59E0B;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.78rem;
        }

        .card-badge-red {
            background-color: rgba(239, 68, 68, 0.15);
            color: #EF4444;
            border: 1px solid #EF4444;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.78rem;
        }

        /* Product container card */
        .product-box {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }

        /* Protocol check item */
        .protocol-item {
            display: flex;
            align-items: flex-start;
            padding: 8px 12px;
            background: #0F172A;
            border-left: 3px solid #059669;
            border-radius: 0 8px 8px 0;
            margin-bottom: 8px;
            font-size: 0.90rem;
            color: #E2E8F0;
        }

        /* Streamlit overrides */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid #1E293B;
        }

        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton>button:hover {
            border-color: #10B981;
            color: #10B981;
        }
        </style>
    """, unsafe_allow_html=True)

def render_market_ticker():
    """Render the current and next event from the live event service."""
    from utils.api_client import ApiClient

    events = ApiClient.get_events()
    today = date.today()
    current_event = None
    next_event = None
    for event in events:
        try:
            start = datetime.strptime(event["start_date"], "%Y-%m-%d").date()
            end = datetime.strptime(event["end_date"], "%Y-%m-%d").date()
        except (KeyError, TypeError, ValueError):
            continue
        if start <= today <= end and current_event is None:
            current_event = event
        elif start > today and next_event is None:
            next_event = event

    primary_event = current_event or next_event
    if primary_event:
        phase = "Current Event" if current_event else "Next Upcoming"
        event_name = escape(primary_event.get("name", "Pakistan E-Commerce Calendar"))
        hijri_date = escape(primary_event.get("hijri_date") or "Hijri date pending")
        date_range = (
            f"{escape(primary_event.get('start_date', ''))} to "
            f"{escape(primary_event.get('end_date', ''))}"
        )
        days_remaining = primary_event.get("days_remaining", 0)
        if current_event:
            event_status = f"Ends in {max(0, (datetime.strptime(current_event['end_date'], '%Y-%m-%d').date() - today).days)} days"
        else:
            event_status = f"Starts in {days_remaining} days"
    else:
        phase = "Market Calendar"
        event_name = "No active or upcoming event"
        hijri_date = "Hijri date pending"
        date_range = "Calendar update required"
        event_status = "No scheduled event"

    next_summary = ""
    if current_event and next_event:
        next_summary = (
            f"<span>Next: <strong>{escape(next_event.get('name', 'Upcoming event'))}</strong> "
            f"({next_event.get('days_remaining', 0)} days)</span>"
        )
    elif next_event is None and current_event is None:
        next_summary = "<span>Next: <strong>No upcoming event</strong></span>"

    st.html(f"""
        <div class="market-ticker">
            <div>
                <span class="ticker-pill">🇵🇰 PAKISTAN MARKET PULSE</span>
                <strong>{phase}:</strong> {event_name}
                <div style="color:#94A3B8;font-size:0.78rem;margin-top:5px;">
                    {date_range} · {event_status}
                </div>
            </div>
            <div style="text-align: right; font-size: 0.85rem;">
                <span>🕒 Hijri: <strong>{hijri_date}</strong></span>
                <div style="color:#CBD5E1;font-size:0.78rem;margin-top:5px;">
                    {next_summary}
                </div>
            </div>
        </div>
    """)

def render_page_header(title: str, subtitle: str, badge: str = "LIVE INTELLIGENCE"):
    """Render consistent branded page header."""
    st.html(f"""
        <div style="margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                <span class="card-badge-green">{badge}</span>
                <span style="color: #64748B; font-size: 0.85rem;">E-Commerce Intelligence Platform</span>
            </div>
            <h1 style="font-size: 2.1rem; font-weight: 800; margin: 0; color: #F8FAFC; letter-spacing: -0.02em;">{title}</h1>
            <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 6px;">{subtitle}</p>
        </div>
    """)
