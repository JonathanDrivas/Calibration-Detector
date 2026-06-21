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
/* ── Page header ─────────────────────────────────────────────────── */
.sr-page-header { padding: 22px 0 18px 0; }
.sr-eyebrow {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 600; letter-spacing: 1.8px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 10px;
}
.sr-title {
    font-family: "Space Grotesk", system-ui, -apple-system, sans-serif;
    font-size: 34px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.04em; line-height: 1.05; margin-bottom: 8px;
}
.sr-tagline { font-size: 14px; color: #6B6B82; line-height: 1.6; }

/* ── Instruction panel ───────────────────────────────────────────── */
.sr-explain-card {
    background: rgba(15,15,22,0.95);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 20px;
    height: 100%;
    box-sizing: border-box;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.025), 0 8px 28px rgba(0,0,0,0.4);
}
.sr-explain-tag {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 12px;
}
.sr-explain-title {
    font-family: "Space Grotesk", system-ui, sans-serif;
    font-size: 15px; font-weight: 700; color: #ECECF2;
    margin-bottom: 16px; letter-spacing: -0.02em;
}
.sr-step {
    display: flex; gap: 12px; align-items: flex-start;
    margin-bottom: 11px;
}
.sr-step-num {
    width: 24px; height: 24px; border-radius: 50%;
    background: rgba(124,92,255,0.12); border: 1px solid rgba(124,92,255,0.28);
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 700; color: #A06BFF;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
}
.sr-step-text { font-size: 13px; color: #8A8A9A; line-height: 1.55; }

/* ── Privacy callout ─────────────────────────────────────────────── */
.sr-privacy {
    background: rgba(124,92,255,0.06);
    border: 1px solid rgba(124,92,255,0.18);
    border-radius: 10px;
    padding: 12px 14px;
    margin-top: 14px;
}
.sr-privacy-title {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; color: #A06BFF;
    text-transform: uppercase; letter-spacing: .6px; margin-bottom: 6px;
}
.sr-privacy-body { font-size: 12px; color: #8A8A9A; line-height: 1.55; }

/* ── Form panel heading ──────────────────────────────────────────── */
.sr-form-tag {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 6px;
}
.sr-form-title {
    font-family: "Space Grotesk", system-ui, sans-serif;
    font-size: 16px; font-weight: 700; color: #ECECF2;
    letter-spacing: -0.02em; margin-bottom: 10px;
}

/* ── Helper text ─────────────────────────────────────────────────── */
.sr-helper {
    font-size: 11px; color: #6B6B82; line-height: 1.5;
    margin: -6px 0 10px 0;
}

/* ── Form container override ─────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15,15,22,0.95) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.025) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sr-page-header">
  <div class="sr-eyebrow">Reflection &middot; Submit</div>
  <div class="sr-title">Student Reflection</div>
  <div class="sr-tagline">Submit a short reflection and rate your confidence.</div>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.5], gap="large")

with left_col:
    st.markdown("""
<div class="sr-explain-card">
  <div class="sr-explain-tag">How it works</div>
  <div class="sr-explain-title">Three steps</div>
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
    <div class="sr-privacy-body">
      Your reflection is stored under a randomly generated nickname, never your real name.
      Results are reviewed by topic to improve teaching and are never used for grades.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

topics = get_topics()

with right_col:
    with st.container(border=True):
        st.markdown(
            "<div class='sr-form-tag'>Reflection &middot; Submission</div>"
            "<div class='sr-form-title'>Submit your reflection</div>",
            unsafe_allow_html=True,
        )
        with st.form("reflection_form"):
            topic_name = st.selectbox("Topic", options=topics)
            reflection_text = st.text_area(
                "Reflection",
                height=128,
                placeholder="Explain the concept in your own words…",
            )
            st.markdown(
                "<p class='sr-helper'>Write in your own words. "
                "Short is fine if the core idea is clear.</p>",
                unsafe_allow_html=True,
            )
            student_confidence = st.slider(
                "How confident are you in your understanding?",
                min_value=1, max_value=5, value=3,
            )
            st.markdown(
                "<p class='sr-helper'>1 = not confident &middot; 5 = very confident</p>",
                unsafe_allow_html=True,
            )
            submitted = st.form_submit_button("Submit reflection", type="primary")

    if submitted:
        if not reflection_text.strip():
            st.error("Please write a reflection before submitting.")
        else:
            nickname = random_nickname()
            save_reflection(nickname, topic_name, reflection_text, student_confidence)
            st.success("Reflection submitted. Thank you!")
