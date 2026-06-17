import streamlit as st
from nav import render_nav

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.home-hero {
    padding: 40px 0 28px 0;
    max-width: 680px;
}
.home-hero-tag {
    font-size: 11px; font-weight: 700; letter-spacing: .8px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 12px;
}
.home-hero-title {
    font-size: 36px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.04em; line-height: 1.1; margin-bottom: 14px;
}
.home-hero-sub {
    font-size: 16px; color: #9A9AAC; line-height: 1.6; max-width: 520px;
}
.home-cards {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 14px; margin: 28px 0 24px 0;
}
.home-card {
    background: #14141C;
    border: 1px solid #262633;
    border-radius: 14px;
    padding: 22px 20px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 8px 24px rgba(0,0,0,0.35);
}
.home-card-dot {
    width: 8px; height: 8px; border-radius: 50%;
    margin-bottom: 14px;
}
.home-card-title {
    font-size: 14px; font-weight: 700; color: #ECECF2;
    margin-bottom: 8px; letter-spacing: -0.01em;
}
.home-card-body {
    font-size: 13px; color: #9A9AAC; line-height: 1.6;
}
.home-divider {
    border: none; border-top: 1px solid #262633; margin: 0 0 20px 0;
}

</style>
""", unsafe_allow_html=True)

# ── Top nav ───────────────────────────────────────────────────────────────────
render_nav("home")

# ── Hero + feature cards ──────────────────────────────────────────────────────
st.markdown("""
<div class="home-hero">
  <div class="home-hero-tag">Academic Learning Analytics</div>
  <div class="home-hero-title">Calibration Detector</div>
  <div class="home-hero-sub">
    An AI-assisted diagnostic tool that turns student reflections into a topic-level
    picture of where confidence outpaces demonstrated understanding.
  </div>
</div>

<div class="home-cards">
  <div class="home-card">
    <div class="home-card-dot" style="background:#A06BFF;"></div>
    <div class="home-card-title">What it does</div>
    <div class="home-card-body">
      Reads short student reflections and flags topics where students are confident
      but have shaky understanding — the group least likely to ask for help on their own.
    </div>
  </div>
  <div class="home-card">
    <div class="home-card-dot" style="background:#5AA9FF;"></div>
    <div class="home-card-title">How it works</div>
    <div class="home-card-body">
      Students submit a brief reflection and a confidence rating. An AI model
      assesses their demonstrated understanding independently, then compares the two
      to produce a calibration label for every topic.
    </div>
  </div>
  <div class="home-card">
    <div class="home-card-dot" style="background:#FF5C6C;"></div>
    <div class="home-card-title">Why calibration matters</div>
    <div class="home-card-body">
      Students who are confident but wrong rarely seek help. Catching that
      gap early lets instructors address misconceptions before they
      compound — without waiting for exam results.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA navigation ────────────────────────────────────────────────────────────
st.markdown(
    '<hr class="home-divider">'
    '<div style="font-size:12px;color:#555566;margin-bottom:10px;font-weight:600;'
    'text-transform:uppercase;letter-spacing:.5px;">Get started</div>',
    unsafe_allow_html=True,
)

cta1, cta2, _ = st.columns([1.5, 1.5, 4])
with cta1:
    if st.button("✏  Submit a reflection", type="primary", use_container_width=True):
        st.switch_page("pages/1_Student_Reflection.py")
with cta2:
    if st.button("📊  View analytics", use_container_width=True):
        st.switch_page("pages/2_Faculty_Dashboard.py")
