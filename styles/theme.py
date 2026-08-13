"""
AmarGari - Theme engine
Injects CSS variables + component styles matching the AmarGari brand
(blue accent, soft cards, light/dark mode). Pure Streamlit + CSS, no
external frontend framework required.
"""
import streamlit as st

PRIMARY = "#0B5FFF"
PRIMARY_DARK = "#0842B0"
ACCENT_CYAN = "#00C2FF"

LIGHT = {
    "bg": "#F5F8FF",
    "bg_soft": "#EEF3FF",
    "card": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#5B6478",
    "border": "#E4EAF7",
    "shadow": "0 8px 24px rgba(15, 23, 42, 0.06)",
}

DARK = {
    "bg": "#0A0E17",
    "bg_soft": "#111726",
    "card": "#131A2B",
    "text": "#EDF1FB",
    "muted": "#93A0BD",
    "border": "#212A40",
    "shadow": "0 8px 24px rgba(0, 0, 0, 0.35)",
}


def _palette():
    mode = st.session_state.get("theme", "light")
    return (DARK if mode == "dark" else LIGHT), mode


def apply_theme():
    """Call once near the top of every page, after st.set_page_config()."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"
    p, mode = _palette()

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background: {p['bg']};
        color: {p['text']};
    }}

    section[data-testid="stSidebar"] {{
        background: {p['bg_soft']};
        border-right: 1px solid {p['border']};
    }}

    h1, h2, h3, h4, h5, h6, p, span, label, li {{
        color: {p['text']};
    }}

    /* ---- Hero / landing text ---- */
    .main-header {{
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.02em;
        color: {p['text']};
        margin-bottom: 0.4rem;
    }}
    .main-header .accent, .accent {{
        background: linear-gradient(135deg, {PRIMARY}, {ACCENT_CYAN});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .sub-header {{
        font-size: 1.05rem;
        color: {p['muted']};
        max-width: 46rem;
        line-height: 1.6;
    }}

    /* ---- Badge pill ---- */
    .db-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        background: {p['bg_soft']};
        border: 1px solid {p['border']};
        color: {PRIMARY};
        font-size: 0.8rem;
        font-weight: 600;
    }}

    /* ---- Generic card ---- */
    .db-card {{
        background: {p['card']};
        border: 1px solid {p['border']};
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        box-shadow: {p['shadow']};
    }}

    /* ---- Metric card ---- */
    .db-metric {{
        background: {p['card']};
        border: 1px solid {p['border']};
        border-radius: 14px;
        padding: 1rem 1.2rem;
        box-shadow: {p['shadow']};
    }}
    .db-metric .db-metric-label {{
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: {p['muted']};
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}
    .db-metric .db-metric-value {{
        font-size: 1.35rem;
        font-weight: 700;
        color: {p['text']};
    }}

    /* ---- Stat block (landing page numbers) ---- */
    .db-stat-value {{
        font-size: 1.9rem;
        font-weight: 800;
        color: {PRIMARY};
        line-height: 1.1;
    }}
    .db-stat-label {{
        font-size: 0.85rem;
        color: {p['muted']};
        font-weight: 500;
    }}

    /* ---- Digital vehicle card ---- */
    .vehicle-card {{
        border-radius: 20px;
        padding: 1.5rem 1.6rem;
        background: linear-gradient(135deg, #0B1B3F 0%, #0B5FFF 55%, #00C2FF 120%);
        color: #F5F9FF;
        box-shadow: 0 14px 30px rgba(11, 95, 255, 0.28);
        position: relative;
        overflow: hidden;
    }}
    .vehicle-card::after {{
        content: "";
        position: absolute;
        right: -40px; top: -40px;
        width: 160px; height: 160px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }}
    .vehicle-card .vc-label {{
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        opacity: 0.85;
        font-weight: 700;
    }}
    .vehicle-card .vc-reg {{
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0.35rem 0 1rem 0;
        letter-spacing: 0.02em;
    }}
    .vehicle-card .vc-row {{
        display: flex;
        justify-content: space-between;
        font-size: 0.82rem;
        margin-top: 0.5rem;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 0.6rem;
    }}
    .vehicle-card .vc-row span:first-child {{ opacity: 0.75; }}
    .vehicle-card .vc-row span:last-child {{ font-weight: 700; }}

    /* ---- Buttons ---- */
    .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
        border-radius: 10px;
        border: 1px solid {PRIMARY};
        background: {PRIMARY};
        color: white;
        font-weight: 600;
        transition: all 0.15s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
        background: {PRIMARY_DARK};
        border-color: {PRIMARY_DARK};
        color: white;
    }}

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
        color: {p['muted']};
    }}
    .stTabs [aria-selected="true"] {{
        color: {PRIMARY} !important;
    }}

    /* ---- Dataframe / containers ---- */
    div[data-testid="stDataFrame"], div[data-testid="stForm"] {{
        border-radius: 14px;
    }}
    div[data-testid="stExpander"], div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 14px !important;
        border-color: {p['border']} !important;
    }}

    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)


def theme_toggle_control(container=None):
    """Renders a small light/dark toggle button. Pass st.sidebar or a column."""
    target = container if container is not None else st
    _, mode = _palette()
    icon = "☀️" if mode == "dark" else "🌙"
    if target.button(icon, key="theme_toggle_btn", help="Toggle light / dark mode"):
        st.session_state["theme"] = "light" if mode == "dark" else "dark"
        st.rerun()
