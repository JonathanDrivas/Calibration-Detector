import streamlit as st
import streamlit.components.v1 as components
from nav import render_nav

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.home-cards {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin: 8px 0 24px 0;
}
.home-card {
    background: rgba(20,20,28,0.85);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 22px 20px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.025), 0 8px 28px rgba(0,0,0,0.4);
    transition: border-color 0.2s ease;
}
.home-card:hover { border-color: rgba(255,255,255,0.10); }
.home-card-dot {
    width: 7px; height: 7px; border-radius: 50%;
    margin-bottom: 14px; opacity: 0.9;
}
.home-card-tag {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; margin-bottom: 9px;
}
.home-card-title {
    font-family: "Space Grotesk", system-ui, sans-serif;
    font-size: 15px; font-weight: 700; color: #ECECF2;
    margin-bottom: 8px; letter-spacing: -0.02em;
}
.home-card-body {
    font-size: 13px; color: #9A9AAC; line-height: 1.65;
}
.home-divider {
    border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 0 0 20px 0;
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
  justify-content: space-between;
  padding: 0 56px;
  gap: 40px;
  animation: fadeUp 0.65s ease both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Left: text ─────────────────────────────────────────────────────────── */
.left { flex-shrink: 0; max-width: 460px; }

.eyebrow {
  font-family: "SF Mono", "Fira Code", "Courier New", monospace;
  font-size: 10px; font-weight: 600; letter-spacing: 1.8px;
  text-transform: uppercase;
  color: #A06BFF;
  margin-bottom: 16px;
}

.wordmark {
  font-family: "Space Grotesk", system-ui, -apple-system, sans-serif;
  font-size: 50px; font-weight: 800; line-height: 1.0;
  color: #ECECF2;
  letter-spacing: -0.04em;
  margin-bottom: 18px;
}

.tagline {
  font-size: 15px; font-weight: 400; line-height: 1.6;
  color: #6B6B82;
  max-width: 340px;
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
  height: 248px;
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
  width: 124px; height: 116px;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  background: rgba(255,255,255,0.022);
  display: flex; flex-direction: column;
  justify-content: flex-end;
  padding: 11px 13px;
  position: relative;
  overflow: hidden;
}

.cell-label {
  font-family: "SF Mono", "Fira Code", "Courier New", monospace;
  font-size: 9px; font-weight: 600; letter-spacing: 0.3px;
  line-height: 1.45;
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
    padding: 30px 28px;
    gap: 26px;
  }
  .wordmark { font-size: 34px; }
  .cal-cell { width: 98px; height: 90px; }
  .axis-y-wrap { height: 193px; }
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
              <span class="cell-label">Under-<br>confident</span>
            </div>
            <div class="cal-cell cell-understands">
              <span class="cell-label">Under-<br>stands</span>
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

# ── Explainer cards ───────────────────────────────────────────────────────────
st.markdown("""
<div class="home-cards">
  <div class="home-card">
    <div class="home-card-tag" style="color:#A06BFF;">01 &middot; Overview</div>
    <div class="home-card-title">What it does</div>
    <div class="home-card-body">
      Reads short student reflections and flags topics where students are confident
      but have shaky understanding, the group least likely to ask for help on their own.
    </div>
  </div>
  <div class="home-card">
    <div class="home-card-tag" style="color:#5AA9FF;">02 &middot; Method</div>
    <div class="home-card-title">How it works</div>
    <div class="home-card-body">
      Students submit a brief reflection and a confidence rating. An AI model
      assesses their demonstrated understanding independently, then compares the two
      to produce a calibration label for every topic.
    </div>
  </div>
  <div class="home-card">
    <div class="home-card-tag" style="color:#FF5C6C;">03 &middot; Impact</div>
    <div class="home-card-title">Why calibration matters</div>
    <div class="home-card-body">
      Students who are confident but wrong rarely seek help. Catching that
      gap early lets instructors address misconceptions before they
      compound, without waiting for exam results.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA navigation ────────────────────────────────────────────────────────────
st.markdown(
    '<hr class="home-divider">'
    '<div style="font-family:\'SF Mono\',\'Fira Code\',\'Courier New\',monospace;'
    'font-size:10px;color:#A06BFF;margin-bottom:10px;font-weight:600;'
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
