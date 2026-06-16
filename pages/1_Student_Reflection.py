import random
import streamlit as st
from db import get_topics, save_reflection

if not st.session_state.get("authenticated"):
    st.warning("Please log in from the home page.")
    st.stop()

_ADJECTIVES = [
    "Amber", "Birch", "Cobalt", "Dusk", "Ember", "Fern", "Glacier", "Hazel",
    "Indigo", "Juniper", "Kelp", "Linden", "Maple", "Nova", "Obsidian",
    "Pine", "Quartz", "Reed", "Slate", "Terra", "Umber", "Violet", "Willow",
    "Xeric", "Yarrow", "Zenith",
]
_NOUNS = [
    "Anchor", "Beacon", "Compass", "Drift", "Echo", "Flint", "Grove",
    "Harbor", "Isle", "Journey", "Kite", "Lantern", "Marsh", "Nimbus",
    "Orbit", "Prism", "Quest", "Ridge", "Summit", "Tide", "Uplift",
    "Vale", "Wren", "Apex", "Bloom", "Crest",
]


def random_nickname():
    return f"{random.choice(_ADJECTIVES)}{random.choice(_NOUNS)}"


st.title("Student Reflection")

st.info(
    "Your reflections help your instructor see which topics need more attention. "
    "They are reviewed by topic, not by name, and are never used for grades."
)

topics = get_topics()

with st.form("reflection_form"):
    topic_name = st.selectbox("Topic", options=topics)
    reflection_text = st.text_area("Reflection", height=160)
    student_confidence = st.slider(
        "How confident are you in your answer", min_value=1, max_value=5, value=3
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    if not reflection_text.strip():
        st.error("Please write a reflection before submitting.")
    else:
        nickname = random_nickname()
        save_reflection(nickname, topic_name, reflection_text, student_confidence)
        st.success("Reflection submitted — thank you!")
