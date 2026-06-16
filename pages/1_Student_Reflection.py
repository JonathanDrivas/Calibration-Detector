import streamlit as st

if not st.session_state.get("authenticated"):
    st.warning("Please log in from the home page.")
    st.stop()

st.title("Student Reflection")
st.markdown("Complete the form below to submit your reflection.")

with st.form("reflection_form"):
    nickname = st.text_input("Nickname")
    topic_name = st.text_input("Topic")
    reflection_text = st.text_area("Reflection")
    student_confidence = st.slider("Confidence (1 = low, 5 = high)", 1, 5, 3)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.info("Form submission coming soon.")
