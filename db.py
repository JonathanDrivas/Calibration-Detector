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
                    understanding TEXT,
                    misconception TEXT,
                    label TEXT
                )
            """)
        conn.commit()
    finally:
        conn.close()
