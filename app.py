import streamlit as st
from db import init_db

init_db()

st.set_page_config(
    page_title="Calibration Detector",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Calibration Detector")
st.markdown("Use the sidebar to navigate between pages.")
