"""
One-off script: re-run analysis over every unanalyzed reflection.
Run with --clear first to wipe results before starting.
Subsequent runs pick up exactly where the previous one left off.
"""
import sys
from db import clear_results, get_unanalyzed_reflections, get_topic_info, save_result
from ai import analyze_reflection, compute_label

if "--clear" in sys.argv:
    print("Clearing existing results...")
    clear_results()
    print("Done.")

reflections = get_unanalyzed_reflections()
if not reflections:
    print("All reflections already analyzed.")
    sys.exit(0)

print(f"Analyzing {len(reflections)} remaining reflection(s)...")

errors = []
for i, ref in enumerate(reflections, start=1):
    topic = get_topic_info(ref["topic_name"])
    if topic is None:
        errors.append(f"  #{ref['id']}: topic '{ref['topic_name']}' not found — skipped")
        continue
    try:
        result = analyze_reflection(
            reflection_text=ref["reflection_text"],
            topic_description=topic["description"] or "",
            topic_misconceptions=topic["misconceptions"] or "",
        )
        label = compute_label(
            understanding=result["understanding"],
            confidence=ref["student_confidence"],
        )
        save_result(
            reflection_id=ref["id"],
            understanding=result["understanding"],
            misconception=result["misconception"],
            label=label,
        )
        print(f"  [{i}/{len(reflections)}] #{ref['id']} ({ref['topic_name']}) "
              f"→ understanding={result['understanding']} label={label}")
    except Exception as e:
        errors.append(f"  #{ref['id']}: {e}")
        print(f"  [{i}/{len(reflections)}] #{ref['id']} ERROR: {e}", file=sys.stderr)

print()
if errors:
    print(f"Finished with {len(errors)} error(s):")
    for err in errors:
        print(err)
    sys.exit(1)
else:
    print(f"Done — {len(reflections)} reflection(s) analyzed.")
