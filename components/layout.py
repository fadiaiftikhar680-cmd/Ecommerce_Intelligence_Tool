"""
components/layout.py
Layout helpers, custom CSS styles, header styling, and market status ticker.
"""

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
    """Renders the top live market status bar with Hijri date and peak alert."""
    st.html("""
        <div class="market-ticker">
            <div>
                <span class="ticker-pill">🇵🇰 PAKISTAN MARKET PULSE</span>
                <strong>Active Season:</strong> Ramadan 1448 AH Prep & Eid Sourcing Window
            </div>
            <div style="text-align: right; font-size: 0.85rem;">
                <span>🕒 Hijri: <strong>Sha'ban 1448 AH</strong></span> &nbsp;|&nbsp;
                <span>🚚 High COD Traffic: <strong>Active</strong></span>
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
