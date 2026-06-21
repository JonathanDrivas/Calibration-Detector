# Calibration Detector

An AI-assisted diagnostic tool that turns short student reflections and confidence ratings into topic-level calibration analytics for instructors.

Calibration Detector is built around one learning problem: a student can be confident and still misunderstand the concept. Those students are often the least likely to ask for help, because they believe they already understand. This app surfaces those calibration gaps by topic, so reteaching can focus where it matters most.

Built for MASY1-GC1800 Emerging Technologies at NYU School of Professional Studies, Summer 2026, as the team MVP for the Adaptive Learning Context Understanding competition.

**Team:** Jonathan, Yolande, Joyce
**Instructor:** Joseph X. Ng
**Status:** Working MVP and class prototype

---

## What the app does

A student submits a course topic, a short written reflection, and a confidence rating from 1 to 5. The AI analysis engine reads the reflection, rates the demonstrated understanding from 1 to 5, names any misconception, and the app then compares that understanding against the student's own confidence to assign one calibration label.

Faculty never see a ranked list of students. They see topic-level patterns that answer which topics have the most confident-but-wrong students, which topics to reteach first, where students understand the material but doubt themselves, and which misconceptions recur.

---

## Why calibration matters

Most reflection tools ask either whether a student feels confident or whether they can explain a concept. Calibration Detector measures both signals separately and compares them, which follows a metacognition framing of the gap between felt and demonstrated understanding.

The most important group is `confident_but_wrong`: students who sound sure but show weak or incorrect understanding. They are the priority, because they are unlikely to seek help on their own.

---

## Calibration labels

| Label | Confidence | Demonstrated understanding | Teaching response |
|---|---|---|---|
| `understands` | high | high | No action needed |
| `confident_but_wrong` | high | low | Reteach first |
| `underconfident` | low | high | Reassure students |
| `knows_confused` | low | low | Support and reteach |
| `partial` | mixed | mixed | Clarify with examples |

---

## Key features

**Student Reflection.** Students submit a short reflection and a confidence rating. The response is stored under a randomly generated nickname, never a real name.

**AI analysis.** The engine evaluates the meaning of a reflection rather than keywords. It returns a demonstrated understanding score from 1 to 5, a detected misconception or the word none, and the computed calibration label.

**Faculty Dashboard.** A topic-level view that includes the Calibration Grid, KPI cards for analyzed reflections, confident-but-wrong count, average calibration gap, and underconfidence topics, plus an Instructor Action Plan, Topic Details, a Topic Risk Heatmap, a Calibration Gap Ladder, a full topic ranking, and a topic-level CSV export. The export is privacy-safe and contains topic-level summary fields only, with no nicknames or reflection text.

**Evidence.** The Evidence tab compares computed labels against the simulated ground-truth labels and reports overall accuracy, confident-but-wrong precision and recall, and a confusion matrix. The current simulated benchmark shows 99 percent overall accuracy with 100 percent precision and recall on `confident_but_wrong`.

**Robustness Check.** The Robustness Check tab runs built-in adversarial reflections that sound confident and use course vocabulary but contain weak or incorrect understanding. A pass means the model labels them `confident_but_wrong` rather than mistaking confident wording for understanding. These checks are not saved to the database and do not affect any dashboard metrics.

**Responsible Use.** The About page explains the guardrails. A fuller version is in `GOVERNANCE.md`.

---

## How the AI analysis works

The engine lives in `ai.py` and calls Claude (`claude-sonnet-4-6`) through Anthropic's SDK.

1. **Read.** The model receives the topic description, the topic's common misconceptions, and the reflection text.
2. **Score understanding.** It rates demonstrated understanding from 1 to 5 against the topic's correct description, with explicit rules so that brevity and plain wording are not penalized and confident vocabulary over a wrong explanation is not rewarded.
3. **Detect misconception.** It names the main misconception, or returns none.
4. **Compare confidence.** The app compares the student's own confidence against the model's understanding score.
5. **Assign label.** `compute_label` applies the fixed rule in the table above. Confidence comes only from the student's slider, never inferred from the text.

The output supports instructor judgment. It is diagnostic, not grading, and topic-level patterns matter more than any single model call.

---

## Data

The project runs on simulated data only. The benchmark contains 190 simulated reflections across the ten course topics, each with a ground-truth label for validation, and no real student data.

The dataset files live in `attached_assets/`. The reflections are loaded into the database by `import_reflections.py`, which clears the existing reflections and results, imports the CSV under random nicknames, and confirms a count of 190. The CSV path is set near the top of that script.

```bash
python import_reflections.py
```

To run the model over every reflection that does not yet have a result, use `rerun_analysis.py`. Pass `--clear` to wipe results first, and note that a normal run resumes from where it left off.

```bash
python rerun_analysis.py            # analyze any unanalyzed reflections
python rerun_analysis.py --clear    # wipe results, then analyze all
```

The ten topics are Creative Destruction, The Creative Force, Technology Creation, Displacement of Concepts, Adopt-Transform-Apply, Invention Innovation and Entrepreneurship, Diffusion of Innovation, Crossing the Chasm, User-Led Adoption, and Technology Classification and Adoption Strategy.

---

## Validation and limitations

The Evidence tab validates computed labels against the simulated benchmark. This is useful for a prototype but is not the same as proving performance on real student writing. The simulated labels are built around the same calibration categories the app uses, so a real deployment would need independent instructor-labeled examples to test model quality rigorously. The Robustness Check is a targeted smoke test for one failure mode, over-crediting confident language, and is not a full AI safety evaluation.

---

## Privacy and responsible use

Calibration Detector supports teaching decisions, it does not evaluate individual students. For this MVP, results are grouped by topic, reflections are stored under generated nicknames, no real student data is used, the views are meant for instructors, and AI outputs are treated as diagnostic signals rather than final judgments. A real deployment would add consent language, instructor authentication and access controls, institution-approved data handling, human review of uncertain cases, and FERPA-aware storage and retention. This tool must not be used for grading, discipline, or ranking individual students. See `GOVERNANCE.md` for the full note.

---

## Tech stack

- Python 3.11
- Streamlit front end
- PostgreSQL, hosted in Replit for the MVP
- Anthropic SDK, calling `claude-sonnet-4-6` through Replit's built-in Anthropic integration
- psycopg2 for database access
- Custom HTML and CSS for the dark analytics interface

Dependencies are declared in `pyproject.toml` and locked with `uv.lock`. Secrets are not stored in the repository.

---

## Environment variables

The app reads its configuration from environment variables. Inside Replit these are provided automatically, the database URL by the Replit Postgres service and the Anthropic values by Replit's built-in Anthropic integration, so there is nothing to set by hand.

| Variable | Used by | Provided by |
|---|---|---|
| `DATABASE_URL` | `db.py` | Replit Postgres |
| `AI_INTEGRATIONS_ANTHROPIC_BASE_URL` | `ai.py` | Replit Anthropic integration |
| `AI_INTEGRATIONS_ANTHROPIC_API_KEY` | `ai.py` | Replit Anthropic integration |

Do not commit real keys or secrets. The `.gitignore` already excludes `.env` files and `.streamlit/secrets.toml`.

---

## How to run

This project was built and tested in Replit, where the database and the Anthropic integration are wired in for you.

### Replit

1. Open the project in Replit.
2. Confirm the Postgres database is provisioned and the three tables exist.
3. Confirm the Anthropic integration is enabled, which supplies the `AI_INTEGRATIONS_ANTHROPIC_*` values.
4. Press Run. The configured command is `streamlit run app.py --server.port 5000`.
5. Open the Student Reflection page to submit a reflection.
6. Open the Faculty Dashboard for the analytics, the Evidence tab, and the Robustness Check.

### Local setup

Running locally means recreating the database and pointing the Anthropic variables at a real endpoint and key.

```bash
git clone <repo-url>
cd Calibration-Detector
python -m venv .venv
source .venv/bin/activate
pip install anthropic psycopg2-binary streamlit   # or: uv sync

export DATABASE_URL="your_postgres_url"
export AI_INTEGRATIONS_ANTHROPIC_BASE_URL="your_anthropic_base_url"
export AI_INTEGRATIONS_ANTHROPIC_API_KEY="your_anthropic_api_key"

streamlit run app.py
```

---

## Project structure

```text
.
├── app.py                  Streamlit entry point: init_db, page config, global styling
├── home.py                 Home page content and hero
├── nav.py                  Shared top navigation bar
├── ai.py                   AI engine: analyze_reflection and compute_label (claude-sonnet-4-6)
├── db.py                   Postgres access and table setup (topics, reflections, results)
├── import_reflections.py   One-off: load the simulated CSV into the reflections table
├── rerun_analysis.py       One-off: run the model over unanalyzed reflections
├── pages/
│   ├── 1_Student_Reflection.py
│   ├── 2_Faculty_Dashboard.py
│   └── 3_About_and_Responsible_Use.py
├── attached_assets/        Simulated reflection dataset (CSV)
├── .streamlit/config.toml  Theme and app configuration
├── GOVERNANCE.md           Responsible-use note
├── pyproject.toml          Dependencies (anthropic, psycopg2-binary, streamlit)
├── uv.lock                 Locked dependency versions
├── .gitignore
└── README.md
```

The repository also carries Node and TypeScript scaffolding from the Replit workspace stack, such as `package.json`, `pnpm-lock.yaml`, `tsconfig.json`, `main.py`, and the `lib/`, `artifacts/`, and `scripts/` folders. These are not used by the Streamlit app and can be ignored.

A system architecture diagram is included as a PNG and SVG for review and slides.

---

## Current status

Implemented: the Student Reflection form, AI analysis of reflection text, the topic-level Faculty Dashboard with the Calibration Grid, Instructor Action Plan, Topic Details, Topic Risk Heatmap, and Calibration Gap Ladder, the Evidence validation tab, the Robustness Check tab, the topic-level CSV export, the Responsible Use page, and the loaded and validated simulated benchmark of 190 reflections.

Not production-ready: there is no instructor authentication, no multi-course or multi-section management, no validation on real student data, and no institution-approved deployment review.

---

## Roadmap

1. Build an instructor-labeled validation set from real student reflections.
2. Add instructor authentication and private dashboard access.
3. Add multi-course and multi-section support.
4. Add consent language and institution-approved data handling for real submissions.
5. Add a student feedback loop so a student can review their own calibration result.
6. Add deployment hardening, including secret management, rate limits, and access controls.
7. Measure whether confident-but-wrong clusters shrink after instructors reteach a topic.

---

## Course context

This repository is the team MVP for an Emerging Technologies class project at NYU SPS. The goal is to show how an AI system can be designed, tested, governed, and communicated in a way that is technically credible, ethically defensible, and useful to an institution.
