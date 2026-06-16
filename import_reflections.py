"""
One-off script: replace the reflections dataset.
1. Clear results (FK dependency on reflections)
2. Clear reflections
3. Import CSV with random nicknames
4. Confirm count == 190
"""
import csv
import os
import random
import sys

import psycopg2

CSV_PATH = "attached_assets/simulated_reflections_realistic_1781640314253.csv"

_ADJECTIVES = [
    "Amber", "Birch", "Cobalt", "Dusk", "Ember", "Fern", "Glacier", "Hazel",
    "Indigo", "Juniper", "Kelp", "Linden", "Maple", "Nova", "Obsidian",
    "Pine", "Quartz", "Reed", "Slate", "Terra", "Umber", "Violet", "Willow",
    "Xeric", "Yarrow", "Zenith",
]
_NOUNS = [
    "Anchor", "Beacon", "Compass", "Drift", "Echo", "Flint", "Grove",
    "Harbor", "Isle", "Journey", "Kite", "Lantern", "Marsh", "Nimbus",
    "Orbit", "Prism", "Quest", "Ridge", "Summit", "Tide", "Uplift",
    "Vale", "Wren", "Apex", "Bloom", "Crest",
]

def random_nickname():
    return f"{random.choice(_ADJECTIVES)}{random.choice(_NOUNS)}"


conn = psycopg2.connect(os.environ["DATABASE_URL"])
try:
    with conn.cursor() as cur:
        print("Step 1: clearing results...")
        cur.execute("DELETE FROM results")
        print("Step 2: clearing reflections...")
        cur.execute("DELETE FROM reflections")

        print(f"Step 3: reading {CSV_PATH}...")
        rows = []
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append((
                    random_nickname(),
                    row["topic_name"].strip(),
                    row["reflection_text"].strip(),
                    int(row["student_confidence"]),
                    row["ground_truth_label"].strip(),
                ))

        print(f"  Read {len(rows)} rows from CSV.")
        cur.executemany(
            """
            INSERT INTO reflections
                (nickname, topic_name, reflection_text, student_confidence, ground_truth_label)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM reflections")
        count = cur.fetchone()[0]

    print(f"Step 4: DB count = {count}")
    if count != 190:
        print(f"ERROR: expected 190, got {count}", file=sys.stderr)
        sys.exit(1)
    print("OK — 190 reflections imported successfully.")
finally:
    conn.close()
