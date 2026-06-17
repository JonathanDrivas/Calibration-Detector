import random
import streamlit as st
from db import get_topics, save_reflection
from nav import render_nav

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


render_nav("reflection")

st.markdown("""
<style>
.sr-header {
    padding: 24px 0 18px 0;
}
.sr-header-title {
    font-size: 26px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.03em; margin-bottom: 6px;
}
.sr-header-sub { font-size: 14px; color: #9A9AAC; line-height: 1.5; }
.sr-explain-card {
    background: #14141C;
    border: 1px solid #262633;
    border-radius: 14px;
    padding: 22px 20px;
    height: 100%;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02), 0 4px 12px rgba(0,0,0,0.3);
}
.sr-explain-title {
    font-size: 13px; font-weight: 700; color: #ECECF2;
    margin-bottom: 10px; letter-spacing: -0.01em;
}
.sr-explain-body {
    font-size: 13px; color: #9A9AAC; line-height: 1.65;
}
.sr-privacy {
    background: rgba(160,107,255,0.07);
    border: 1px solid rgba(160,107,255,0.20);
    border-radius: 10px;
    padding: 12px 14px;
    margin-top: 16px;
    font-size: 12px; color: #9A9AAC; line-height: 1.5;
}
.sr-privacy-title {
    font-size: 11px; font-weight: 700; color: #A06BFF;
    text-transform: uppercase; letter-spacing: .4px; margin-bottom: 5px;
}
.sr-step {
    display: flex; gap: 10px; align-items: flex-start;
    margin-bottom: 12px;
}
.sr-step-num {
    width: 22px; height: 22px; border-radius: 50%;
    background: rgba(160,107,255,0.15); border: 1px solid rgba(160,107,255,0.30);
    font-size: 11px; font-weight: 700; color: #A06BFF;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
}
.sr-step-text { font-size: 13px; color: #9A9AAC; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sr-header">
  <div class="sr-header-title">Student Reflection</div>
  <div class="sr-header-sub">
    Submit a short reflection on a course topic along with your confidence rating.
  </div>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.5], gap="large")

with left_col:
    st.markdown("""
<div class="sr-explain-card">
  <div class="sr-explain-title">How this works</div>
  <div class="sr-step">
    <div class="sr-step-num">1</div>
    <div class="sr-step-text">Choose the topic your reflection is about.</div>
  </div>
  <div class="sr-step">
    <div class="sr-step-num">2</div>
    <div class="sr-step-text">
      Write 2 to 4 sentences explaining the concept in your own words.
      Focus on what it means and why it matters, not on memorized definitions.
    </div>
  </div>
  <div class="sr-step">
    <div class="sr-step-num">3</div>
    <div class="sr-step-text">
      Rate how confident you feel in your understanding on a scale of 1 to 5.
    </div>
  </div>
  <div class="sr-privacy">
    <div class="sr-privacy-title">Privacy</div>
    Your reflection is stored under a randomly generated nickname, never your real name.
    Results are reviewed by topic to improve teaching and are never used for grades.
  </div>
</div>
""", unsafe_allow_html=True)

topics = get_topics()

with right_col:
    with st.container(border=True):
        st.markdown(
            "<p style='font-size:14px;font-weight:700;color:#ECECF2;"
            "margin-bottom:4px;'>Submit your reflection</p>",
            unsafe_allow_html=True,
        )
        with st.form("reflection_form"):
            topic_name = st.selectbox("Topic", options=topics)
            reflection_text = st.text_area(
                "Reflection",
                height=160,
                placeholder="Explain the concept in your own words…",
            )
            student_confidence = st.slider(
                "How confident are you in your understanding?",
                min_value=1, max_value=5, value=3,
            )
            submitted = st.form_submit_button("Submit reflection", type="primary")

    if submitted:
        if not reflection_text.strip():
            st.error("Please write a reflection before submitting.")
        else:
            nickname = random_nickname()
            save_reflection(nickname, topic_name, reflection_text, student_confidence)
            st.success("Reflection submitted. Thank you!")
