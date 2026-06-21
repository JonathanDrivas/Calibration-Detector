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
.sr-page-header { padding: 18px 0 14px 0; }
.sr-eyebrow {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 600; letter-spacing: 1.8px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 9px;
}
.sr-title {
    font-size: 32px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.04em; line-height: 1.05; margin-bottom: 7px;
}
.sr-tagline { font-size: 14px; color: #6B6B82; line-height: 1.6; margin-bottom: 12px; }

/* ── Pills ───────────────────────────────────────────────────────── */
.sr-pill-row { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 4px; }
.sr-pill {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9.5px; font-weight: 600; letter-spacing: .6px;
    color: #8A8A9A;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 100px;
    padding: 3px 10px;
    white-space: nowrap;
}

/* ── Submission guide card ───────────────────────────────────────── */
.sr-explain-card {
    background: rgba(13,13,21,0.96);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px 18px 16px 18px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
    margin-bottom: 10px;
}
.sr-explain-tag {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.3px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 16px;
}

/* ── Steps ───────────────────────────────────────────────────────── */
.sr-step { display: flex; gap: 12px; }
.sr-step-left {
    display: flex; flex-direction: column; align-items: center; flex-shrink: 0;
}
.sr-step-num {
    width: 24px; height: 24px; border-radius: 50%;
    background: rgba(124,92,255,0.13); border: 1px solid rgba(124,92,255,0.32);
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 700; color: #A06BFF;
    display: flex; align-items: center; justify-content: center;
}
.sr-step-connector {
    width: 1px; flex: 1; min-height: 14px;
    background: linear-gradient(to bottom, rgba(124,92,255,0.22), transparent);
    margin: 3px 0;
}
.sr-step-body { padding-bottom: 14px; }
.sr-step-label {
    font-size: 13px; font-weight: 700; color: #D8D8E8;
    margin-bottom: 3px; line-height: 1.3;
}
.sr-step-text { font-size: 12px; color: #737385; line-height: 1.55; }

/* ── Note inside guide ───────────────────────────────────────────── */
.sr-guide-note {
    font-size: 11.5px; color: #5A5A72; line-height: 1.5;
    border-top: 1px solid rgba(255,255,255,0.06);
    padding-top: 12px; margin-top: 2px;
    font-style: italic;
}

/* ── What happens next card ──────────────────────────────────────── */
.sr-next-card {
    background: rgba(13,13,21,0.96);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
    margin-bottom: 10px;
}
.sr-next-title {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #5AA9FF; margin-bottom: 7px;
}
.sr-next-body { font-size: 12px; color: #737385; line-height: 1.6; }

/* ── Privacy card ────────────────────────────────────────────────── */
.sr-privacy {
    background: rgba(124,92,255,0.05);
    border: 1px solid rgba(124,92,255,0.16);
    border-radius: 10px;
    padding: 13px 15px;
}
.sr-privacy-title {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; color: #A06BFF;
    text-transform: uppercase; letter-spacing: .6px; margin-bottom: 6px;
}
.sr-privacy-body { font-size: 12px; color: #7A7A8E; line-height: 1.58; }

/* ── Form panel heading ──────────────────────────────────────────── */
.sr-form-tag {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 5px;
}
.sr-form-title {
    font-size: 16px; font-weight: 700; color: #ECECF2;
    letter-spacing: -0.02em; margin-bottom: 10px;
}

/* ── Helper text ─────────────────────────────────────────────────── */
.sr-helper {
    font-size: 11px; color: #5A5A72; line-height: 1.5;
    margin: -4px 0 10px 0;
}

/* ── Form container ──────────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(13,13,21,0.96) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.42),
                inset 0 1px 0 rgba(255,255,255,0.025) !important;
}

/* ── Submit button: violet bg + white text ───────────────────────── */
button[data-testid="baseButton-primary"],
button[kind="primary"],
button[data-testid*="primary"] {
    background: #A06BFF !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    opacity: 1 !important;
    text-shadow: none !important;
}
button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover {
    background: #8D56EF !important;
    color: #FFFFFF !important;
}

/* ── Success card ────────────────────────────────────────────────── */
.sr-success {
    background: rgba(61,220,151,0.06);
    border: 1px solid rgba(61,220,151,0.22);
    border-radius: 12px;
    padding: 16px 18px;
    margin-top: 12px;
}
.sr-success-title {
    font-size: 14px; font-weight: 700; color: #3DDC97;
    margin-bottom: 5px; letter-spacing: -0.01em;
}
.sr-success-body { font-size: 12.5px; color: #7A9E8A; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sr-page-header">
  <div class="sr-eyebrow">Reflection &middot; Submit</div>
  <div class="sr-title">Student Reflection</div>
  <div class="sr-tagline">Submit a short reflection and rate your confidence.</div>
  <div class="sr-pill-row">
    <span class="sr-pill">Private by design</span>
    <span class="sr-pill">Topic-level review</span>
    <span class="sr-pill">Not used for grades</span>
  </div>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.5], gap="large")

with left_col:
    st.markdown("""
<div class="sr-explain-card">
  <div class="sr-explain-tag">Submission guide</div>
  <div class="sr-step">
    <div class="sr-step-left">
      <div class="sr-step-num">1</div>
      <div class="sr-step-connector"></div>
    </div>
    <div class="sr-step-body">
      <div class="sr-step-label">Choose a topic</div>
      <div class="sr-step-text">Pick the course concept your reflection is about.</div>
    </div>
  </div>
  <div class="sr-step">
    <div class="sr-step-left">
      <div class="sr-step-num">2</div>
      <div class="sr-step-connector"></div>
    </div>
    <div class="sr-step-body">
      <div class="sr-step-label">Explain in your own words</div>
      <div class="sr-step-text">Write 2 to 4 sentences. Short is fine if the core idea is clear.</div>
    </div>
  </div>
  <div class="sr-step">
    <div class="sr-step-left">
      <div class="sr-step-num">3</div>
    </div>
    <div class="sr-step-body">
      <div class="sr-step-label">Rate your confidence</div>
      <div class="sr-step-text">Use 1 if you are unsure and 5 if you feel very confident.</div>
    </div>
  </div>
  <div class="sr-guide-note">The goal is honest calibration, not perfect wording.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="sr-next-card">
  <div class="sr-next-title">What happens next</div>
  <div class="sr-next-body">The AI reads the reflection, estimates demonstrated understanding, and compares that with your confidence rating. Faculty see topic-level patterns, not a ranked list of students.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="sr-privacy">
  <div class="sr-privacy-title">Privacy</div>
  <div class="sr-privacy-body">Your reflection is stored under a randomly generated nickname, never your real name. Results are reviewed by topic to improve teaching and are never used for grades.</div>
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
                height=130,
                placeholder="Explain the concept in your own words\u2026",
            )
            st.markdown(
                "<p class='sr-helper'>Write in your own words. "
                "A simple correct explanation is better than memorized wording.</p>",
                unsafe_allow_html=True,
            )
            student_confidence = st.slider(
                "How confident are you in your understanding?",
                min_value=1, max_value=5, value=3,
            )
            st.markdown(
                "<p class='sr-helper'>1 = not confident &middot; 5 = very confident"
                " &nbsp;&mdash;&nbsp; Rate how confident you feel before seeing any feedback.</p>",
                unsafe_allow_html=True,
            )
            submitted = st.form_submit_button("Submit reflection", type="primary")

    if submitted:
        if not reflection_text.strip():
            st.error("Please write a reflection before submitting.")
        else:
            nickname = random_nickname()
            save_reflection(nickname, topic_name, reflection_text, student_confidence)
            st.markdown("""
<div class="sr-success">
  <div class="sr-success-title">Reflection submitted</div>
  <div class="sr-success-body">Your response was saved under a nickname and will be included in topic-level analysis.</div>
</div>
""", unsafe_allow_html=True)
