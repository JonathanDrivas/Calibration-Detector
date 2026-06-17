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
/* ── Global background ──────────────────────────────────────────── */
[data-testid="stAppViewContainer"] { background-color: #F7F5FA !important; }
[data-testid="stHeader"]           { background-color: #F7F5FA !important; }

/* ── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #E4DEEC !important;
}

/* ── Global font ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif !important;
    color: #20202A;
}
</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("home.py",                                   title="Home",                      icon="🎯"),
    st.Page("pages/1_Student_Reflection.py",             title="Student Reflection",         icon="✏️"),
    st.Page("pages/2_Faculty_Dashboard.py",              title="Faculty Dashboard",          icon="📊"),
    st.Page("pages/3_About_and_Responsible_Use.py",      title="About & Responsible Use",    icon="ℹ️"),
])
pg.run()
