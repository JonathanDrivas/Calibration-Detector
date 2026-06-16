import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    misconceptions TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS reflections (
                    id SERIAL PRIMARY KEY,
                    nickname TEXT,
                    topic_name TEXT,
                    reflection_text TEXT,
                    student_confidence INTEGER,
                    ground_truth_label TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    reflection_id INTEGER REFERENCES reflections(id),
                    understanding INTEGER,
                    misconception TEXT,
                    label TEXT
                )
            """)
        conn.commit()
    finally:
        conn.close()


def get_topics():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT name FROM topics ORDER BY name")
            return [row["name"] for row in cur.fetchall()]
    finally:
        conn.close()


def save_reflection(nickname, topic_name, reflection_text, student_confidence):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reflections
                    (nickname, topic_name, reflection_text, student_confidence)
                VALUES (%s, %s, %s, %s)
                """,
                (nickname, topic_name, reflection_text, student_confidence),
            )
        conn.commit()
    finally:
        conn.close()


def get_unanalyzed_reflections():
    """Return reflections that do not yet have a row in results."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT r.*
                FROM reflections r
                LEFT JOIN results res ON res.reflection_id = r.id
                WHERE res.id IS NULL
                ORDER BY r.id
            """)
            return cur.fetchall()
    finally:
        conn.close()


def get_topic_info(topic_name):
    """Return description and misconceptions for a topic by name."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT description, misconceptions FROM topics WHERE name = %s",
                (topic_name,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def save_result(reflection_id, understanding, misconception, label):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO results (reflection_id, understanding, misconception, label)
                VALUES (%s, %s, %s, %s)
                """,
                (reflection_id, understanding, misconception, label),
            )
        conn.commit()
    finally:
        conn.close()


def get_all_results():
    """Return all results joined with reflection data."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    r.id AS reflection_id,
                    r.nickname,
                    r.topic_name,
                    r.reflection_text,
                    r.student_confidence,
                    res.understanding,
                    res.misconception,
                    res.label
                FROM reflections r
                JOIN results res ON res.reflection_id = r.id
                ORDER BY r.topic_name, r.id
            """)
            return cur.fetchall()
    finally:
        conn.close()
