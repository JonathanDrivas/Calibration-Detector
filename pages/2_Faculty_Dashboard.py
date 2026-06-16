import streamlit as st

if not st.session_state.get("authenticated"):
    st.warning("Please log in from the home page.")
    st.stop()

st.title("Faculty Dashboard")
st.markdown("View and analyze student reflection results here.")

st.subheader("Topics")
st.info("No topics yet.")

st.subheader("Reflections")
st.info("No reflections yet.")

st.subheader("Results")
st.info("No results yet.")
