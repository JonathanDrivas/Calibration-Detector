import streamlit as st
from db import init_db

init_db()

st.set_page_config(
    page_title="Calibration Detector",
    page_icon="🎯",
    layout="wide",
)

PASSWORD = "calibrate2024"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🎯 Calibration Detector")
    st.markdown("This app is private. Please enter the password to continue.")
    pwd = st.text_input("Password", type="password")
    if st.button("Enter"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

st.title("🎯 Calibration Detector")
st.markdown(
    "Use the sidebar to navigate between pages."
)
