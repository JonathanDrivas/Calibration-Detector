import streamlit as st
from nav import render_nav

render_nav("about")

st.markdown("""
<style>
/* ── Page header ─────────────────────────────────────────────────── */
.ab-page-header { padding: 22px 0 20px 0; }
.ab-eyebrow {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 600; letter-spacing: 1.8px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 10px;
}
.ab-title {
    font-family: "Space Grotesk", system-ui, -apple-system, sans-serif;
    font-size: 34px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.04em; line-height: 1.05; margin-bottom: 10px;
}
.ab-tagline { font-size: 14px; color: #6B6B82; line-height: 1.6; max-width: 560px; }

/* ── Governance cards ────────────────────────────────────────────── */
.ab-cards { display: flex; flex-direction: column; gap: 10px; margin: 24px 0 28px 0; }
.ab-card {
    border-radius: 14px;
    padding: 20px 22px;
    display: flex; gap: 18px; align-items: flex-start;
    position: relative; overflow: hidden;
}
.ab-card-accent {
    width: 3px; flex-shrink: 0; border-radius: 999px; margin-top: 2px; align-self: stretch;
}
.ab-card-body { flex: 1; min-width: 0; }
.ab-card-num {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; margin-bottom: 7px;
}
.ab-card-title {
    font-size: 14px; font-weight: 700; color: #ECECF2;
    margin-bottom: 7px; letter-spacing: -0.01em;
}
.ab-card-text { font-size: 13px; color: #9A9AAC; line-height: 1.65; }

/* ── Full note ───────────────────────────────────────────────────── */
.ab-note {
    background: rgba(255,255,255,0.012);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 12px; color: #555566; line-height: 1.7;
    margin-top: 4px;
}
.ab-note-label {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #3A3A50; margin-bottom: 8px;
}
</style>

<div class="ab-page-header">
  <div class="ab-eyebrow">Governance &amp; Ethics</div>
  <div class="ab-title">About &amp; Responsible Use</div>
  <div class="ab-tagline">
    The Calibration Detector turns short student reflections into a topic-level picture
    of where a class is struggling. It is a diagnostic tool, not an evaluative one.
  </div>
</div>

<div class="ab-cards">

  <div class="ab-card" style="background:rgba(160,107,255,0.05);border:1px solid rgba(160,107,255,0.14);">
    <div class="ab-card-accent" style="background:#A06BFF;"></div>
    <div class="ab-card-body">
      <div class="ab-card-num" style="color:#A06BFF;">Principle 01</div>
      <div class="ab-card-title">Diagnostic, not evaluative</div>
      <div class="ab-card-text">
        This tool does not grade or rank anyone and is not used for discipline.
        Its purpose is to help instructors see where a topic needs more attention,
        not to judge individual students.
      </div>
    </div>
  </div>

  <div class="ab-card" style="background:rgba(90,169,255,0.05);border:1px solid rgba(90,169,255,0.14);">
    <div class="ab-card-accent" style="background:#5AA9FF;"></div>
    <div class="ab-card-body">
      <div class="ab-card-num" style="color:#5AA9FF;">Principle 02</div>
      <div class="ab-card-title">Topic-level review, never individual</div>
      <div class="ab-card-text">
        Every result is shown to faculty by topic, not by student. The dashboard
        shows patterns across a class, not a ranked list of individuals.
      </div>
    </div>
  </div>

  <div class="ab-card" style="background:rgba(61,220,151,0.05);border:1px solid rgba(61,220,151,0.14);">
    <div class="ab-card-accent" style="background:#3DDC97;"></div>
    <div class="ab-card-body">
      <div class="ab-card-num" style="color:#3DDC97;">Principle 03</div>
      <div class="ab-card-title">Nicknames, not real identities</div>
      <div class="ab-card-text">
        Reflections are stored under a randomly generated nickname rather than
        a student's real name. Students are told this before they submit, so they
        understand how their data is handled.
      </div>
    </div>
  </div>

  <div class="ab-card" style="background:rgba(245,181,68,0.05);border:1px solid rgba(245,181,68,0.14);">
    <div class="ab-card-accent" style="background:#F5B544;"></div>
    <div class="ab-card-body">
      <div class="ab-card-num" style="color:#F5B544;">Principle 04</div>
      <div class="ab-card-title">Human judgment stays central</div>
      <div class="ab-card-text">
        The model reads understanding from text, which is an imperfect signal.
        Low-certainty cases are surfaced for human review, and the tool is designed
        to support a teacher's judgment, not replace it.
      </div>
    </div>
  </div>

  <div class="ab-card" style="background:rgba(196,181,253,0.05);border:1px solid rgba(196,181,253,0.14);">
    <div class="ab-card-accent" style="background:#C4B5FD;"></div>
    <div class="ab-card-body">
      <div class="ab-card-num" style="color:#C4B5FD;">Principle 05</div>
      <div class="ab-card-title">Simulated data for this project</div>
      <div class="ab-card-text">
        This deployment runs only on simulated student data and is written to respect
        FERPA in any real deployment. No real student data is collected or stored here.
      </div>
    </div>
  </div>

</div>

<div class="ab-note">
  <div class="ab-note-label">Full responsible-use note</div>
  The Calibration Detector turns short student reflections into
  a topic-level picture of where a class is struggling. It is a diagnostic tool, not an
  evaluative one. It does not grade or rank anyone, and it is not used for discipline.
  Every result is shown to faculty by topic and never tied to a student's name, and
  reflections are stored under nicknames rather than real identities. Students see a clear
  notice when they submit, explaining that their reflections are reviewed by topic to improve
  teaching and are never used for grades. The model reads understanding from text, which is
  an imperfect signal, so low-certainty cases are routed for human review and the tool is
  meant to support a teacher's judgment, never replace it. It runs only on simulated data
  for this project and is written to respect FERPA in any real deployment.
</div>
""", unsafe_allow_html=True)
