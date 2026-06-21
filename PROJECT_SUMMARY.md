# PROJECT_SUMMARY.md

## 1. Project Concept

Calibration Detector is an AI-assisted learning analytics tool for higher education.
It surfaces a specific, high-risk gap: students who are confident they understand a
topic but whose written reflections reveal clear misconceptions. These students are
the least likely to seek help and the hardest to identify from grades alone.

The tool separates student-reported confidence from AI-assessed demonstrated
understanding, then maps the combination to one of five calibration states. Faculty
see a ranked picture of where the class is overconfident, not just where it is
struggling.

---

## 2. Use Case

An instructor assigns short written reflections on course topics. Students rate their
own confidence. An AI model independently reads the reflection and scores the
student's demonstrated understanding. The mismatch between those two signals
identifies calibration problems at the topic level without any individual grading.

**Primary user:** Faculty, reviewing aggregated topic-level signals before deciding
where to focus re-teaching time.

**Secondary user:** Students, submitting reflections under a random nickname.

---

## 3. Solution Design

**Stack**
- Python 3.11, Streamlit 1.58, psycopg2-binary
- PostgreSQL database (three tables: `topics`, `reflections`, `results`)
- Anthropic Claude Sonnet via Replit AI Integrations proxy (no direct API key required)

**Database schema**
- `topics` — name, description, common misconceptions per topic
- `reflections` — nickname, topic_name, reflection_text, student_confidence (1–5),
  optional ground_truth_label for validation
- `results` — reflection_id FK, understanding score (1–5), misconception phrase, label

**AI scoring (`ai.py`)**
The model receives the topic description, known misconceptions, and the student's
reflection text. It returns:
- `understanding`: integer 1–5
- `misconception`: short phrase naming the main error, or "none"

**Calibration labels (`compute_label`)**

| Understanding | Confidence | Label |
|---|---|---|
| ≥ 4 | ≥ 4 | understands |
| ≤ 2 | ≥ 4 | confident_but_wrong |
| ≥ 4 | ≤ 2 | underconfident |
| ≤ 2 | ≤ 2 | knows_confused |
| all other | all other | partial |

**Calibration gap** = avg student confidence − avg AI-assessed understanding.
Positive = class is overconfident on that topic.

**Action labels (per topic)**
- Reteach first: CBW count ≥ 3 AND gap ≥ 0
- Reassure students: gap ≤ −0.3 AND CBW < 3
- Monitor: all others

---

## 4. Planned MVP

Four pages covering the complete instructor workflow:

1. **Home** — landing page explaining what the tool does and why calibration matters.
2. **Student Reflection** — anonymous submission form (topic, reflection text,
   confidence slider 1–5). Reflections stored under randomly generated nicknames.
3. **Faculty Dashboard** — analysis and visualization of results across all topics.
4. **About & Responsible Use** — governance and privacy policy displayed as cards.

---

## 5. Current Status

**Completed**

- Full PostgreSQL schema initialized on startup; topics seeded with descriptions and
  known misconceptions.
- 190 simulated student reflections imported from CSV for demonstration.
- Student Reflection page: topic selector, text area, confidence slider (1–5), form
  submission, success confirmation with random nickname.
- Faculty Dashboard with four tabs:
  - **Overview**: key-risk callout, on-demand analysis button with progress bar, four
    KPI cards (total analyzed, confident-but-wrong count, avg calibration gap,
    underconfidence topic count), calibration grid (2×2 quadrant visual + partial),
    top-insight callout, Instructor Action Plan (filtered to "Reteach first" topics
    only, falling back to top 3 by CBW count), full topic ranking expander.
  - **Topic Details**: per-topic expandable section with CBW count, calibration gap
    metric, stacked bar chart of all five labels, per-nickname misconception list.
  - **Evidence**: overall accuracy, CBW precision, CBW recall, confusion matrix
    heatmap validated against simulated ground-truth labels.
  - **Robustness Check**: six adversarial test cases using correct vocabulary but
    containing clear misconceptions; pass rate card and per-case dataframe.
- About & Responsible Use page with five governance cards.
- Persistent top navigation bar (`nav.py`) injected on every page; active page
  highlighted in violet; Streamlit sidebar nav hidden.
- Cinematic hero on the Home page rendered via `components.html`: animated radial
  glows, hairline grid overlay, Space Grotesk wordmark, animated 2×2 calibration
  motif with CBW red-glow pulse, reduced-motion support.
- Unified visual design system extended across all pages: deep `#0B0B12` background
  with hairline grid and radial glows, hero-language page headers (monospace eyebrow,
  Space Grotesk display heading, muted tagline), calibration grid visually rhyming
  with the hero motif, cinematic governance cards on the About page, Inter body font,
  monospace numbers and labels throughout.
- All emojis removed from the UI; em/en dashes replaced with commas or middots.

**Data note:** The app runs entirely on simulated data. No real student data is
collected or stored.

---

## 6. Key Next Steps

- **Authentication**: add instructor login so the dashboard is not publicly accessible.
- **Multi-course support**: scope topics, reflections, and results to a course/section.
- **Live data collection**: connect to a real course and replace simulated reflections
  with genuine student submissions.
- **Export**: allow faculty to download topic summaries and action plans as CSV.
- **Student feedback loop**: optionally show students their calibration result after
  submission so they can self-correct.
- **Instructor-labeled validation set**: replace simulated ground-truth labels with
  real instructor annotations to improve the Evidence tab.
- **Deployment hardening**: environment-based secrets, connection pooling, rate
  limiting on the analyze endpoint.
