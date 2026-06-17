import streamlit as st
from nav import render_nav

render_nav("about")

st.markdown("""
<style>
.about-header {
    padding: 28px 0 20px 0;
}
.about-header-tag {
    font-size: 11px; font-weight: 700; letter-spacing: .7px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 10px;
}
.about-header-title {
    font-size: 26px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.03em; margin-bottom: 10px;
}
.about-header-body {
    font-size: 14px; color: #9A9AAC; line-height: 1.6; max-width: 620px;
}
.about-cards {
    display: flex; flex-direction: column; gap: 10px; margin: 24px 0 28px 0;
}
.about-card {
    background: #14141C;
    border: 1px solid #262633;
    border-left: 4px solid #262633;
    border-radius: 0 12px 12px 0;
    padding: 18px 20px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02), 0 4px 12px rgba(0,0,0,0.3);
}
.about-card-title {
    font-size: 13px; font-weight: 700; color: #ECECF2;
    margin-bottom: 6px; letter-spacing: -0.01em;
}
.about-card-body {
    font-size: 13px; color: #9A9AAC; line-height: 1.6;
}
.about-note {
    background: #14141C;
    border: 1px solid #262633;
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 12px; color: #555566; line-height: 1.6;
    margin-top: 4px;
}
</style>

<div class="about-header">
  <div class="about-header-tag">Governance</div>
  <div class="about-header-title">About &amp; Responsible Use</div>
  <div class="about-header-body">
    The Calibration Detector turns short student reflections into a topic-level picture
    of where a class is struggling. It is a diagnostic tool, not an evaluative one.
  </div>
</div>

<div class="about-cards">

  <div class="about-card" style="border-left-color:#A06BFF;">
    <div class="about-card-title">Diagnostic, not evaluative</div>
    <div class="about-card-body">
      This tool does not grade or rank anyone and is not used for discipline.
      Its purpose is to help instructors see where a topic needs more attention,
      not to judge individual students.
    </div>
  </div>

  <div class="about-card" style="border-left-color:#5AA9FF;">
    <div class="about-card-title">Topic-level review, never individual</div>
    <div class="about-card-body">
      Every result is shown to faculty by topic, not by student. The dashboard
      shows patterns across a class, not a ranked list of individuals.
    </div>
  </div>

  <div class="about-card" style="border-left-color:#3DDC97;">
    <div class="about-card-title">Nicknames, not real identities</div>
    <div class="about-card-body">
      Reflections are stored under a randomly generated nickname rather than
      a student's real name. Students are told this before they submit, so they
      understand how their data is handled.
    </div>
  </div>

  <div class="about-card" style="border-left-color:#F5B544;">
    <div class="about-card-title">Human judgment stays central</div>
    <div class="about-card-body">
      The model reads understanding from text, which is an imperfect signal.
      Low-certainty cases are surfaced for human review, and the tool is designed
      to support a teacher's judgment, not replace it.
    </div>
  </div>

  <div class="about-card" style="border-left-color:#C4B5FD;">
    <div class="about-card-title">Simulated data for this project</div>
    <div class="about-card-body">
      This deployment runs only on simulated student data and is written to respect
      FERPA in any real deployment. No real student data is collected or stored here.
    </div>
  </div>

</div>

<div class="about-note">
  Full responsible-use note: The Calibration Detector turns short student reflections into
  a topic-level picture of where a class is struggling. It is a diagnostic tool, not an
  evaluation one. It does not grade or rank anyone, and it is not used for discipline.
  Every result is shown to faculty by topic and never tied to a student's name, and
  reflections are stored under nicknames rather than real identities. Students see a clear
  notice when they submit, explaining that their reflections are reviewed by topic to improve
  teaching and are never used for grades. The model reads understanding from text, which is
  an imperfect signal, so low-certainty cases are routed for human review and the tool is
  meant to support a teacher's judgment, never replace it. It runs only on simulated data
  for this project and is written to respect FERPA in any real deployment.
</div>
""", unsafe_allow_html=True)
