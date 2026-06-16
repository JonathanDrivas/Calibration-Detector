import streamlit as st
from db import init_db

init_db()

st.set_page_config(
    page_title="Calibration Detector",
    page_icon="🎯",
    layout="wide",
)

pg = st.navigation([
    st.Page("home.py",                                   title="Home",                      icon="🎯"),
    st.Page("pages/1_Student_Reflection.py",             title="Student Reflection",         icon="✏️"),
    st.Page("pages/2_Faculty_Dashboard.py",              title="Faculty Dashboard",          icon="📊"),
    st.Page("pages/3_About_and_Responsible_Use.py",      title="About & Responsible Use",    icon="ℹ️"),
])
pg.run()
