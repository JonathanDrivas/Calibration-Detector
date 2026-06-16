# Calibration Detector

A Streamlit app that helps faculty assess whether students' self-reported confidence matches their actual understanding of course topics.

## Run & Operate

- `streamlit run app.py --server.port 5000` — run the app (port 5000)
- Required env: `DATABASE_URL` — Postgres connection string (auto-set by Replit)

## Stack

- Python 3.11 + Streamlit 1.58
- DB: PostgreSQL + psycopg2-binary (raw SQL, CREATE TABLE IF NOT EXISTS on startup)

## Where things live

- `app.py` — entry point; password gate + home page
- `db.py` — DB connection helper and `init_db()` (runs `CREATE TABLE IF NOT EXISTS` for all three tables)
- `pages/1_Student_Reflection.py` — student-facing form (skeleton)
- `pages/2_Faculty_Dashboard.py` — faculty results view (skeleton)
- `.streamlit/config.toml` — server config (port 5000, headless, 0.0.0.0)

## Database schema

- `topics` — id (PK), name, description, misconceptions
- `reflections` — id (PK), nickname, topic_name, reflection_text, student_confidence, ground_truth_label
- `results` — id (PK), reflection_id (FK → reflections), understanding, misconception, label

## Architecture decisions

- Tables are created idempotently via `init_db()` called on every startup — no separate migration step needed for this skeleton phase.
- Password protection uses a hardcoded string in `app.py` with `st.session_state`; replace with an env var before sharing broadly.
- Each page re-checks `st.session_state.authenticated` and stops early if not logged in, keeping the gate consistent across all pages.

## Product

- **Student Reflection** (page 1): students enter a nickname, pick a topic, write a reflection, and rate their confidence.
- **Faculty Dashboard** (page 2): faculty review submitted reflections alongside AI-generated calibration labels.

## User preferences

- App should remain private (password-gated).

## Gotchas

- `init_db()` is called on every cold start — idempotent, so safe to leave in.
- Streamlit's multipage `pages/` convention requires filenames to start with a number for ordering (e.g. `1_Student_Reflection.py`).

## Pointers

- See the `streamlit` skill for UI and workflow guidelines.
- See the `database` skill for SQL query helpers.
