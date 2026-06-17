import streamlit as st
from db import init_db

init_db()

st.set_page_config(
    page_title="Calibration Detector",
    page_icon="🎯",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global font ─────────────────────────────────────────────────── */
html, body, [class*="css"], button, input, textarea, select {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif !important;
}

/* ── App background with radial glow ─────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 1200px 600px at 50% -10%,
            rgba(160,107,255,0.10) 0%, transparent 60%),
        #0B0B12 !important;
    background-attachment: fixed !important;
}
[data-testid="stHeader"]     { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"]    { display: none !important; }

/* ── Max-width container ─────────────────────────────────────────── */
.block-container {
    max-width: 1200px !important;
    padding: 1.25rem 2rem 2.5rem !important;
    margin: 0 auto !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #14141C !important;
    border-right: 1px solid #262633 !important;
}
[data-testid="stSidebarNav"] a {
    color: #9A9AAC !important;
    border-radius: 0 8px 8px 0 !important;
    transition: all 0.15s !important;
    font-size: 14px !important;
}
[data-testid="stSidebarNav"] a:hover {
    color: #ECECF2 !important;
    background: rgba(255,255,255,0.04) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #ECECF2 !important;
    background: rgba(160,107,255,0.10) !important;
    border-left: 3px solid #A06BFF !important;
    font-weight: 700 !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span { color: #ECECF2 !important; }

/* ── Tabs ────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #262633 !important; }
[data-testid="stTabs"] button { color: #9A9AAC !important; font-size: 14px !important; font-weight: 500 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #ECECF2 !important; font-weight: 600 !important; }
[data-baseweb="tab-highlight"] { background: #A06BFF !important; }

/* ── Primary buttons ─────────────────────────────────────────────── */
[data-testid^="baseButton-primary"] {
    background: #A06BFF !important;
    border-color: #A06BFF !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(160,107,255,0.28) !important;
    transition: all 0.15s ease !important;
}
[data-testid^="baseButton-primary"]:hover {
    background: #B98CFF !important;
    border-color: #B98CFF !important;
    box-shadow: 0 8px 24px rgba(160,107,255,0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── Secondary buttons ───────────────────────────────────────────── */
[data-testid^="baseButton-secondary"] {
    background: #1A1A24 !important;
    border-color: #262633 !important;
    color: #ECECF2 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
[data-testid^="baseButton-secondary"]:hover {
    background: #262633 !important;
    border-color: #A06BFF !important;
}

/* ── Inputs / textarea ───────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #14141C !important;
    border-color: #262633 !important;
    color: #ECECF2 !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #A06BFF !important;
    box-shadow: 0 0 0 2px rgba(160,107,255,0.20) !important;
}
textarea::placeholder { color: #555566 !important; }

/* ── Selectbox ───────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: #14141C !important;
    border-color: #262633 !important;
    border-radius: 10px !important;
    color: #ECECF2 !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #A06BFF !important;
    box-shadow: 0 0 0 2px rgba(160,107,255,0.20) !important;
}
[data-baseweb="popover"] {
    background: #1A1A24 !important;
    border: 1px solid #262633 !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5) !important;
}
[data-baseweb="menu"] { background: #1A1A24 !important; }
[data-baseweb="menu"] [role="option"] { color: #ECECF2 !important; }
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"][aria-selected="true"] {
    background: rgba(160,107,255,0.10) !important;
}

/* ── Expanders ───────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #14141C !important;
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
}

/* ── st.container(border=True) ───────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #14141C !important;
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02) !important;
}

/* ── Metrics ─────────────────────────────────────────────────────── */
[data-testid="stMetricLabel"] { color: #9A9AAC !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #ECECF2 !important; font-variant-numeric: tabular-nums !important; }

/* ── Dataframe ───────────────────────────────────────────────────── */
[data-testid="stDataFrame"] > div {
    background: #14141C !important;
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Progress bar ────────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div > div { background: #A06BFF !important; }

/* ── Captions / dividers / misc ──────────────────────────────────── */
[data-testid="stCaption"]   { color: #9A9AAC !important; }
hr                          { border-color: #262633 !important; opacity: 1 !important; }
</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("home.py",                              title="Home"),
    st.Page("pages/1_Student_Reflection.py",        title="Student Reflection"),
    st.Page("pages/2_Faculty_Dashboard.py",         title="Faculty Dashboard"),
    st.Page("pages/3_About_and_Responsible_Use.py", title="About & Responsible Use"),
])
pg.run()
