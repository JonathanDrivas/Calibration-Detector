import streamlit as st
import streamlit.components.v1 as components
from nav import render_nav

render_nav("about")

# ── Hero ──────────────────────────────────────────────────────────────────────
_hero_html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0B0B12;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;overflow:hidden;padding:20px 18px 16px}
.grid{position:fixed;top:0;left:0;width:100%;height:100%;background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);background-size:32px 32px;pointer-events:none;z-index:0}
.gv{position:fixed;top:65%;left:30%;transform:translate(-50%,-50%);width:480px;height:260px;background:radial-gradient(ellipse,rgba(160,107,255,.09) 0%,transparent 70%);pointer-events:none;z-index:0}
.gb{position:fixed;top:35%;left:70%;transform:translate(-50%,-50%);width:340px;height:180px;background:radial-gradient(ellipse,rgba(90,169,255,.06) 0%,transparent 70%);pointer-events:none;z-index:0}
.hero{position:relative;z-index:1;display:flex;gap:20px;align-items:center}
.text{flex:1;min-width:0}
.eyebrow{font-size:10px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:#6B6B82;margin-bottom:10px;font-family:'SF Mono','Fira Code',monospace}
.title{font-size:27px;font-weight:800;color:#ECECF2;letter-spacing:-.03em;line-height:1.1;margin-bottom:12px}
.sub{font-size:13px;color:#8A8A9A;line-height:1.65;max-width:400px}
.visual{flex:0 0 310px;height:252px}
@media(max-width:520px){.hero{flex-direction:column}.visual{width:100%;flex:none;height:210px}}
@media(prefers-reduced-motion:reduce){}
</style></head>
<body>
<div class="grid"></div>
<div class="gv"></div>
<div class="gb"></div>
<div class="hero">
  <div class="text">
    <div class="eyebrow">GOVERNANCE&#8201;&middot;&#8201;RESPONSIBLE AI</div>
    <div class="title">Designed for trust,<br>not surveillance</div>
    <div class="sub">Calibration Detector turns student reflections into topic-level teaching signals while keeping the focus on privacy, transparency, and instructor judgment.</div>
  </div>
  <div class="visual">
    <svg viewBox="0 0 380 270" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
      <defs>
        <radialGradient id="cg" cx="50%" cy="50%" r="40%">
          <stop offset="0%" stop-color="#A06BFF" stop-opacity=".17"/>
          <stop offset="100%" stop-color="#A06BFF" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <ellipse cx="190" cy="135" rx="82" ry="82" fill="url(#cg)"/>
      <line x1="190" y1="135" x2="190" y2="53"  stroke="#252535" stroke-width="1"/>
      <line x1="190" y1="135" x2="268" y2="110" stroke="#252535" stroke-width="1"/>
      <line x1="190" y1="135" x2="238" y2="201" stroke="#252535" stroke-width="1"/>
      <line x1="190" y1="135" x2="142" y2="201" stroke="#252535" stroke-width="1"/>
      <line x1="190" y1="135" x2="112" y2="110" stroke="#252535" stroke-width="1"/>
      <path d="M190,106 L212,117 L212,143 Q212,158 190,164 Q168,158 168,143 L168,117 Z" fill="rgba(160,107,255,0.12)" stroke="rgba(160,107,255,0.65)" stroke-width="1.5"/>
      <polyline points="179,140 188,151 205,128" fill="none" stroke="#A06BFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="190" cy="53"  r="6" fill="#0D0D18" stroke="#A06BFF" stroke-width="1.5"/>
      <circle cx="268" cy="110" r="6" fill="#0D0D18" stroke="#5AA9FF" stroke-width="1.5"/>
      <circle cx="238" cy="201" r="6" fill="#0D0D18" stroke="#3DDC97" stroke-width="1.5"/>
      <circle cx="142" cy="201" r="6" fill="#0D0D18" stroke="#F5B544" stroke-width="1.5"/>
      <circle cx="112" cy="110" r="6" fill="#0D0D18" stroke="#C4B5FD" stroke-width="1.5"/>
      <text x="190" y="38"  text-anchor="middle" font-size="11" fill="#A06BFF" font-family="-apple-system,sans-serif" font-weight="700">Diagnostic</text>
      <text x="278" y="107" text-anchor="start"  font-size="11" fill="#5AA9FF" font-family="-apple-system,sans-serif" font-weight="700">Topic-level</text>
      <text x="248" y="220" text-anchor="start"  font-size="11" fill="#3DDC97" font-family="-apple-system,sans-serif" font-weight="700">Nicknames</text>
      <text x="132" y="220" text-anchor="end"    font-size="11" fill="#F5B544" font-family="-apple-system,sans-serif" font-weight="700">Human review</text>
      <text x="102" y="107" text-anchor="end"    font-size="11" fill="#C4B5FD" font-family="-apple-system,sans-serif" font-weight="700">Simulated data</text>
    </svg>
  </div>
</div>
</body></html>"""
components.html(_hero_html, height=328, scrolling=False)

# ── AI Methodology Panel ───────────────────────────────────────────────────
st.markdown("""
<style>
.aim-panel {
    background: rgba(13,13,20,0.95);
    border: 1px solid rgba(160,107,255,0.18);
    border-left: 3px solid rgba(160,107,255,0.55);
    border-radius: 14px;
    padding: 18px 20px 18px 20px;
    margin: 0 0 18px 0;
}
.aim-eyebrow {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.4px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 5px;
}
.aim-title {
    font-size: 15px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.02em; margin-bottom: 7px;
}
.aim-intro {
    font-size: 12.5px; color: #D0D0E0; line-height: 1.6; margin-bottom: 9px;
}
.aim-kv { display: flex; gap: 10px; margin-bottom: 4px; align-items: flex-start; }
.aim-kv-key {
    font-size: 10px; font-weight: 700; color: #8A8A9A; letter-spacing: .4px;
    text-transform: uppercase; font-family: "SF Mono","Fira Code",monospace;
    white-space: nowrap; flex-shrink: 0; min-width: 78px; padding-top: 1.5px;
}
.aim-kv-val { font-size: 12.5px; color: #D0D0E0; line-height: 1.45; }
.aim-note {
    font-size: 11.5px; color: #9A9AAC; line-height: 1.55;
    border-top: 1px solid rgba(255,255,255,0.07);
    padding-top: 9px; margin-top: 10px; font-style: italic;
}
.aim-example { font-size: 11px; color: #6B6B82; margin-top: 5px; line-height: 1.5; }
.aim-cbw { color: #FF5C6C; font-weight: 600; }
.aim-section-head {
    display: flex; align-items: center; gap: 10px; margin: 14px 0 14px 0;
}
.aim-section-line { flex: 1; height: 1px; background: rgba(255,255,255,0.07); }
.aim-section-label {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #6B6B82; flex-shrink: 0;
}
.aim-pipe { display: flex; align-items: flex-start; }
.aim-stage {
    flex: 1; min-width: 0; display: flex; flex-direction: column;
    align-items: center; text-align: center; padding: 0 2px;
}
.aim-conn {
    flex: 0 0 20px; display: flex; align-items: flex-start;
    padding-top: 15px;
}
.aim-conn-line {
    flex: 1; height: 1.5px;
    background: linear-gradient(90deg, rgba(160,107,255,0.45), rgba(160,107,255,0.22));
}
.aim-node {
    width: 32px; height: 32px; border-radius: 50%;
    background: #0D0D18; border: 1.5px solid rgba(160,107,255,0.42);
    color: #A06BFF; font-size: 11px; font-weight: 800;
    font-family: "SF Mono","Fira Code",monospace;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 8px; flex-shrink: 0;
}
.aim-node-hl {
    border-color: rgba(160,107,255,0.8);
    box-shadow: 0 0 12px rgba(160,107,255,0.3);
    background: rgba(160,107,255,0.1);
}
.aim-stage-title {
    font-size: 12px; font-weight: 700; color: #ECECF2;
    line-height: 1.25; margin-bottom: 3px;
}
.aim-stage-text { font-size: 11px; color: #9A9AAC; line-height: 1.4; }
@media(max-width:620px){
    .aim-pipe{flex-wrap:wrap; gap:10px}
    .aim-conn{display:none}
    .aim-stage{flex:0 0 44%; align-items:flex-start; text-align:left; flex-direction:row; gap:9px; padding:0}
    .aim-node{margin-bottom:0; flex-shrink:0}
}
</style>

<div class="aim-panel">
  <div class="aim-eyebrow">AI METHOD</div>
  <div class="aim-title">How the AI is used</div>
  <div class="aim-intro">The AI judges demonstrated understanding, while the app computes the final calibration label using fixed rules.</div>
  <div class="aim-kv"><span class="aim-kv-key">Model</span><span class="aim-kv-val">Claude, claude-sonnet-4-6, via built-in Anthropic integration</span></div>
  <div class="aim-kv"><span class="aim-kv-key">Input</span><span class="aim-kv-val">Topic description, common misconceptions, and reflection text</span></div>
  <div class="aim-kv"><span class="aim-kv-key">Output</span><span class="aim-kv-val">Understanding score 1 to 5, plus misconception detected or none</span></div>
  <div class="aim-kv"><span class="aim-kv-key">Confidence</span><span class="aim-kv-val">Student-provided only, from the 1 to 5 slider, never inferred from text</span></div>
  <div class="aim-kv"><span class="aim-kv-key">Final label</span><span class="aim-kv-val">Deterministic app logic, not chosen by the AI</span></div>
  <div class="aim-note">This keeps the AI assessment separate from the final calibration label, which is computed by transparent app logic.</div>
  <div class="aim-example">Example: a confident but incorrect explanation can still receive a low understanding score and become <span class="aim-cbw">confident_but_wrong</span>.</div>
  <div class="aim-section-head">
    <div class="aim-section-line"></div>
    <div class="aim-section-label">5-STAGE PIPELINE</div>
    <div class="aim-section-line"></div>
  </div>
  <div class="aim-pipe">
    <div class="aim-stage">
      <div class="aim-node aim-node-hl">1</div>
      <div class="aim-stage-title">Topic context</div>
      <div class="aim-stage-text">Topic description, misconceptions, reflection</div>
    </div>
    <div class="aim-conn"><div class="aim-conn-line"></div></div>
    <div class="aim-stage">
      <div class="aim-node">2</div>
      <div class="aim-stage-title">Understanding score</div>
      <div class="aim-stage-text">AI rates demonstrated understanding 1 to 5</div>
    </div>
    <div class="aim-conn"><div class="aim-conn-line"></div></div>
    <div class="aim-stage">
      <div class="aim-node">3</div>
      <div class="aim-stage-title">Misconception check</div>
      <div class="aim-stage-text">AI returns main misconception or none</div>
    </div>
    <div class="aim-conn"><div class="aim-conn-line"></div></div>
    <div class="aim-stage">
      <div class="aim-node">4</div>
      <div class="aim-stage-title">Student confidence</div>
      <div class="aim-stage-text">Slider value only, never inferred</div>
    </div>
    <div class="aim-conn"><div class="aim-conn-line"></div></div>
    <div class="aim-stage">
      <div class="aim-node">5</div>
      <div class="aim-stage-title">Fixed-rule label</div>
      <div class="aim-stage-text">App computes final category</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Principle cards + note ─────────────────────────────────────────────────
st.markdown("""
<style>
.ab-cards { display: flex; flex-direction: column; gap: 10px; margin: 8px 0 22px 0; }
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
.ab-card-text { font-size: 13px; color: #BCBCCC; line-height: 1.65; }

.ab-note {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 12px; color: #8A8A9A; line-height: 1.7;
    margin-top: 4px; margin-bottom: 10px;
}
.ab-note-label {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: #6B6B82; margin-bottom: 8px;
}
.ab-closing {
    background: rgba(255,255,255,0.015);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 13px 16px;
    font-size: 11px; color: #6B6B82; line-height: 1.6;
    margin-top: 8px;
}
</style>

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

<div class="ab-closing">
  In a real deployment, this tool would require instructor review, consent language,
  access controls, and institution-approved data handling before use with real student submissions.
</div>
""", unsafe_allow_html=True)
