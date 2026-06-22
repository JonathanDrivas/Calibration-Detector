import streamlit as st
import streamlit.components.v1 as components
from db import init_db
from nav import render_nav

init_db()

st.set_page_config(
    page_title="Calibration Detector",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@700;800&display=swap');

/* ── Global font ─────────────────────────────────────────────────── */
html, body, [class*="css"], button, input, textarea, select {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif !important;
}

/* ── App background: glows + hairline grid ───────────────────────── */
[data-testid="stAppViewContainer"] {
    background-color: #0B0B12 !important;
    background-image:
        linear-gradient(rgba(255,255,255,0.016) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.016) 1px, transparent 1px),
        radial-gradient(ellipse 1100px 580px at 15% 0%,
            rgba(124,92,255,0.08) 0%, transparent 62%),
        radial-gradient(ellipse 800px 480px at 88% 100%,
            rgba(90,169,255,0.06) 0%, transparent 62%) !important;
    background-size: 52px 52px, 52px 52px, auto, auto !important;
    background-attachment: fixed !important;
}
@media (prefers-reduced-motion: reduce) {
    [data-testid="stAppViewContainer"] { background-image: none !important; }
}
[data-testid="stHeader"]     { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"]    { display: none !important; }

/* ── Max-width container ─────────────────────────────────────────── */
.block-container {
    max-width: 1200px !important;
    padding: 1.25rem 2rem 2.5rem !important;
    margin: 0 auto !important;
}

/* ── Sidebar: completely hidden (custom top nav is used instead) ──── */
[data-testid="stSidebar"],
section[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Tabs ────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #262633 !important; }
[data-testid="stTabs"] button { color: #9A9AAC !important; font-size: 14px !important; font-weight: 500 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #ECECF2 !important; font-weight: 600 !important; }
[data-baseweb="tab-highlight"] { background: #A06BFF !important; }

/* ── Primary buttons ─────────────────────────────────────────────── */
[data-testid^="baseButton-primary"] {
    background: #A06BFF !important;
    border-color: #A06BFF !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(160,107,255,0.28) !important;
    transition: all 0.15s ease !important;
}
[data-testid^="baseButton-primary"]:hover {
    background: #B98CFF !important;
    border-color: #B98CFF !important;
    box-shadow: 0 8px 24px rgba(160,107,255,0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── Secondary buttons ───────────────────────────────────────────── */
[data-testid^="baseButton-secondary"] {
    background: #1A1A24 !important;
    border-color: #262633 !important;
    color: #ECECF2 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
[data-testid^="baseButton-secondary"]:hover {
    background: #262633 !important;
    border-color: #A06BFF !important;
}

/* ── Inputs / textarea ───────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #14141C !important;
    border-color: #262633 !important;
    color: #ECECF2 !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #A06BFF !important;
    box-shadow: 0 0 0 2px rgba(160,107,255,0.20) !important;
}
textarea::placeholder { color: #555566 !important; }

/* ── Selectbox ───────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: #14141C !important;
    border-color: #262633 !important;
    border-radius: 10px !important;
    color: #ECECF2 !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #A06BFF !important;
    box-shadow: 0 0 0 2px rgba(160,107,255,0.20) !important;
}
[data-baseweb="popover"] {
    background: #1A1A24 !important;
    border: 1px solid #262633 !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5) !important;
}
[data-baseweb="menu"] { background: #1A1A24 !important; }
[data-baseweb="menu"] [role="option"] { color: #ECECF2 !important; }
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"][aria-selected="true"] {
    background: rgba(160,107,255,0.10) !important;
}

/* ── Expanders ───────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #14141C !important;
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
}

/* ── st.container(border=True) ───────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #14141C !important;
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02) !important;
}

/* ── Metrics ─────────────────────────────────────────────────────── */
[data-testid="stMetricLabel"] { color: #9A9AAC !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #ECECF2 !important; font-variant-numeric: tabular-nums !important; }

/* ── Dataframe ───────────────────────────────────────────────────── */
[data-testid="stDataFrame"] > div {
    background: #14141C !important;
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Progress bar ────────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div > div { background: #A06BFF !important; }

/* ── Captions / dividers / misc ──────────────────────────────────── */
[data-testid="stCaption"]   { color: #9A9AAC !important; }
hr                          { border-color: #262633 !important; opacity: 1 !important; }

/* ── Home page ───────────────────────────────────────────────────── */
.home-section-label {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #404055;
    margin: 22px 0 13px 0;
}
.home-cards {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin: 0 0 22px 0;
}
.home-card {
    background: rgba(14,14,22,0.94);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 20px 18px;
    box-shadow: 0 4px 22px rgba(0,0,0,0.42);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    position: relative;
    overflow: hidden;
}
.home-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.home-card-v::before { background: linear-gradient(90deg,#A06BFF 0%,transparent 80%); }
.home-card-b::before { background: linear-gradient(90deg,#5AA9FF 0%,transparent 80%); }
.home-card-r::before { background: linear-gradient(90deg,#FF5C6C 0%,transparent 80%); }
.home-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.55);
    border-color: rgba(255,255,255,0.12);
}
.home-card-icon { display: block; margin-bottom: 14px; }
.home-card-tag {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.4px;
    text-transform: uppercase; margin-bottom: 8px;
}
.home-card-title {
    font-size: 15px; font-weight: 700; color: #DCDCE8;
    margin-bottom: 9px; letter-spacing: -0.02em; line-height: 1.25;
}
.home-card-body {
    font-size: 12.5px; color: #737385; line-height: 1.68;
}
.home-divider {
    border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 12px 0 0 0;
}
</style>
""", unsafe_allow_html=True)

# ── Top nav ───────────────────────────────────────────────────────────────────
render_nav("home")

# ── Cinematic hero (components.html iframe) ───────────────────────────────────
_hero_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&display=swap"
      rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 100%; height: 100%;
  background: #0B0B12;
  overflow: hidden;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* ── Hero shell ─────────────────────────────────────────────────────────── */
.hero {
  position: relative;
  width: 100%; height: 100%;
  display: flex;
  align-items: center;
  overflow: hidden;
}

/* ── Background glows ───────────────────────────────────────────────────── */
.glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}
.glow-violet {
  width: 620px; height: 500px;
  background: radial-gradient(ellipse, rgba(124,92,255,0.20) 0%, transparent 68%);
  top: -140px; left: -100px;
  animation: driftV 14s ease-in-out infinite;
}
.glow-blue {
  width: 520px; height: 400px;
  background: radial-gradient(ellipse, rgba(90,169,255,0.14) 0%, transparent 68%);
  bottom: -110px; right: -80px;
  animation: driftB 18s ease-in-out infinite;
}
@keyframes driftV {
  0%,100% { transform: translate(0,0) scale(1); }
  50%      { transform: translate(26px,18px) scale(1.04); }
}
@keyframes driftB {
  0%,100% { transform: translate(0,0) scale(1); }
  50%      { transform: translate(-20px,-14px) scale(1.03); }
}

/* ── Hairline grid ──────────────────────────────────────────────────────── */
.grid-bg {
  position: absolute; inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255,255,255,0.027) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.027) 1px, transparent 1px);
  background-size: 52px 52px;
  -webkit-mask-image: radial-gradient(ellipse 88% 88% at 50% 50%, black 15%, transparent 100%);
  mask-image:         radial-gradient(ellipse 88% 88% at 50% 50%, black 15%, transparent 100%);
}

/* ── Content row ────────────────────────────────────────────────────────── */
.content {
  position: relative; z-index: 2;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 44px;
  gap: 48px;
  animation: fadeUp 0.65s ease both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Left: text ─────────────────────────────────────────────────────────── */
.left { flex-shrink: 0; max-width: 380px; }

.eyebrow {
  font-family: "SF Mono", "Fira Code", "Courier New", monospace;
  font-size: 10px; font-weight: 600; letter-spacing: 1.8px;
  text-transform: uppercase;
  color: #A06BFF;
  margin-bottom: 14px;
}

.wordmark {
  font-family: "Space Grotesk", system-ui, -apple-system, sans-serif;
  font-size: 70px; font-weight: 800; line-height: 0.95;
  color: #ECECF2;
  letter-spacing: -0.04em;
  margin-bottom: 18px;
}

.tagline {
  font-size: 15px; font-weight: 400; line-height: 1.6;
  color: #6B6B82;
  max-width: 310px;
}

/* ── Right: calibration motif ───────────────────────────────────────────── */
.right { flex-shrink: 0; }

.motif-wrap {
  display: flex;
  align-items: flex-start;
  gap: 7px;
}

.axis-y-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 302px;
}
.axis-y-label {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  transform: rotate(180deg);
  font-family: "SF Mono", "Courier New", monospace;
  font-size: 9px; font-weight: 500; letter-spacing: 0.9px;
  color: #3A3A50;
  white-space: nowrap;
}

.grid-area { display: flex; flex-direction: column; }

.cal-row { display: flex; gap: 5px; }
.cal-row + .cal-row { margin-top: 5px; }

.cal-cell {
  width: 172px; height: 148px;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  background: rgba(255,255,255,0.022);
  display: flex; flex-direction: column;
  justify-content: flex-end;
  padding: 14px 16px;
  position: relative;
  overflow: hidden;
}

.cell-label {
  font-family: "SF Mono", "Fira Code", "Courier New", monospace;
  font-size: 11px; font-weight: 600; letter-spacing: 0.2px;
  line-height: 1.4;
  position: relative; z-index: 1;
}

.cell-underconf   .cell-label { color: #5AA9FF; }
.cell-understands .cell-label { color: #3DDC97; }
.cell-knowsconf   .cell-label { color: #F5B544; }

.cell-cbw {
  border-color: rgba(255,92,108,0.22) !important;
  background: rgba(255,92,108,0.045) !important;
}
.cell-cbw .cell-label { color: #FF5C6C; }

.cbw-glow {
  position: absolute; inset: -30px;
  background: radial-gradient(ellipse at center, rgba(255,92,108,0.18) 0%, transparent 60%);
  animation: cbwPulse 4.5s ease-in-out infinite;
}
@keyframes cbwPulse {
  0%,100% { opacity: 0.5; }
  50%      { opacity: 1.0; }
}

.axis-x-wrap {
  display: flex;
  justify-content: center;
  margin-top: 7px;
}
.axis-x-label {
  font-family: "SF Mono", "Courier New", monospace;
  font-size: 9px; font-weight: 500; letter-spacing: 0.9px;
  color: #3A3A50;
}

/* ── Narrow screens ─────────────────────────────────────────────────────── */
@media (max-width: 700px) {
  .content {
    flex-direction: column;
    align-items: flex-start;
    padding: 28px 24px;
    gap: 24px;
  }
  .wordmark { font-size: 40px; }
  .cal-cell { width: 116px; height: 102px; }
  .axis-y-wrap { height: 212px; }
}

/* ── Reduced motion ─────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .content { animation: none; opacity: 1; transform: none; }
  .glow-violet, .glow-blue { animation: none; }
  .cbw-glow { animation: none; opacity: 0.7; }
}
</style>
</head>
<body>
<div class="hero">
  <div class="glow glow-violet"></div>
  <div class="glow glow-blue"></div>
  <div class="grid-bg"></div>

  <div class="content">

    <!-- Left: wordmark + tagline -->
    <div class="left">
      <div class="eyebrow">Academic Learning Analytics</div>
      <div class="wordmark">Calibration<br>Detector</div>
      <div class="tagline">Where student confidence outpaces real understanding.</div>
    </div>

    <!-- Right: calibration motif -->
    <div class="right">
      <div class="motif-wrap">

        <!-- Y-axis label -->
        <div class="axis-y-wrap">
          <span class="axis-y-label">understanding &#x2191;</span>
        </div>

        <!-- 2x2 grid + x-axis -->
        <div class="grid-area">
          <div class="cal-row">
            <div class="cal-cell cell-underconf">
              <span class="cell-label">Underconfident</span>
            </div>
            <div class="cal-cell cell-understands">
              <span class="cell-label">Understands</span>
            </div>
          </div>
          <div class="cal-row">
            <div class="cal-cell cell-knowsconf">
              <span class="cell-label">Knows<br>confused</span>
            </div>
            <div class="cal-cell cell-cbw">
              <div class="cbw-glow"></div>
              <span class="cell-label">Confident<br>but wrong</span>
            </div>
          </div>
          <div class="axis-x-wrap">
            <span class="axis-x-label">confidence &#x2192;</span>
          </div>
        </div>

      </div>
    </div>

  </div>
</div>
</body>
</html>"""

components.html(_hero_html, height=460, scrolling=False)

# ── CTA navigation (immediately below hero) ───────────────────────────────────
st.markdown(
    '<div style="font-family:\'SF Mono\',\'Fira Code\',\'Courier New\',monospace;'
    'font-size:10px;color:#A06BFF;margin:4px 0 10px 0;font-weight:600;'
    'letter-spacing:1.8px;text-transform:uppercase;">Get started</div>',
    unsafe_allow_html=True,
)

cta1, cta2, _ = st.columns([1.5, 1.5, 4])
with cta1:
    if st.button("Submit a reflection", type="primary", use_container_width=True):
        st.switch_page("pages/1_Student_Reflection.py")
with cta2:
    if st.button("View analytics", use_container_width=True):
        st.switch_page("pages/2_Faculty_Dashboard.py")

# ── Pillar cards (below CTAs) ─────────────────────────────────────────────────
st.markdown('<hr class="home-divider">', unsafe_allow_html=True)
st.markdown('<div class="home-section-label">System overview</div>', unsafe_allow_html=True)
st.markdown("""
<div class="home-cards">
  <div class="home-card home-card-v">
    <span class="home-card-icon">
      <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="13" cy="13" r="2.5" fill="#A06BFF"/>
        <path d="M8 13 A5 5 0 0 1 18 13" stroke="#A06BFF" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.55"/>
        <path d="M4 13 A9 9 0 0 1 22 13" stroke="#A06BFF" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0.28"/>
      </svg>
    </span>
    <div class="home-card-tag" style="color:#A06BFF;">01 &middot; Overview</div>
    <div class="home-card-title">What it does</div>
    <div class="home-card-body">Reads short student reflections and surfaces topics where confidence is high but demonstrated understanding is shaky.</div>
  </div>
  <div class="home-card home-card-b">
    <span class="home-card-icon">
      <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="5"  cy="13" r="2.5" fill="#5AA9FF"/>
        <circle cx="13" cy="7"  r="2.5" fill="#5AA9FF" opacity="0.7"/>
        <circle cx="13" cy="19" r="2.5" fill="#5AA9FF" opacity="0.7"/>
        <circle cx="21" cy="13" r="2.5" fill="#5AA9FF" opacity="0.45"/>
        <line x1="7.4" y1="12.1" x2="10.6" y2="8.9"  stroke="#5AA9FF" stroke-width="1" opacity="0.45"/>
        <line x1="7.4" y1="13.9" x2="10.6" y2="17.1" stroke="#5AA9FF" stroke-width="1" opacity="0.45"/>
        <line x1="15.4" y1="8.9"  x2="18.6" y2="12.1" stroke="#5AA9FF" stroke-width="1" opacity="0.3"/>
        <line x1="15.4" y1="17.1" x2="18.6" y2="13.9" stroke="#5AA9FF" stroke-width="1" opacity="0.3"/>
      </svg>
    </span>
    <div class="home-card-tag" style="color:#5AA9FF;">02 &middot; Method</div>
    <div class="home-card-title">How it works</div>
    <div class="home-card-body">Students submit a reflection and confidence rating. The AI assesses understanding, then the app compares the two signals.</div>
  </div>
  <div class="home-card home-card-r">
    <span class="home-card-icon">
      <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="13" cy="13" r="9"   stroke="#FF5C6C" stroke-width="1.2" fill="none" opacity="0.35"/>
        <circle cx="13" cy="13" r="5"   stroke="#FF5C6C" stroke-width="1.2" fill="none" opacity="0.6"/>
        <circle cx="13" cy="13" r="2"   fill="#FF5C6C"/>
        <line x1="13" y1="4"  x2="13" y2="7.5"  stroke="#FF5C6C" stroke-width="1.2" stroke-linecap="round" opacity="0.45"/>
        <line x1="13" y1="18.5" x2="13" y2="22" stroke="#FF5C6C" stroke-width="1.2" stroke-linecap="round" opacity="0.45"/>
        <line x1="4"  y1="13" x2="7.5"  y2="13" stroke="#FF5C6C" stroke-width="1.2" stroke-linecap="round" opacity="0.45"/>
        <line x1="18.5" y1="13" x2="22" y2="13" stroke="#FF5C6C" stroke-width="1.2" stroke-linecap="round" opacity="0.45"/>
      </svg>
    </span>
    <div class="home-card-tag" style="color:#FF5C6C;">03 &middot; Impact</div>
    <div class="home-card-title">Why calibration matters</div>
    <div class="home-card-body">Confident-but-wrong students rarely ask for help. Catching that gap early helps instructors address misconceptions before they compound.</div>
  </div>
</div>
""", unsafe_allow_html=True)
