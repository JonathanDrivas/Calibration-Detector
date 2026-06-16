import streamlit as st
from db import get_unanalyzed_reflections, get_topic_info, save_result, get_all_results
from ai import analyze_reflection, compute_label

st.title("Faculty Dashboard")

# ── Analyze button ──────────────────────────────────────────────────────────
st.subheader("Run Analysis")

unanalyzed = get_unanalyzed_reflections()

if unanalyzed:
    st.write(f"{len(unanalyzed)} reflection(s) have not been analyzed yet.")
    if st.button("Analyze unanalyzed reflections"):
        progress = st.progress(0, text="Starting…")
        errors = []
        for i, ref in enumerate(unanalyzed):
            topic = get_topic_info(ref["topic_name"])
            if topic is None:
                errors.append(f"#{ref['id']}: topic '{ref['topic_name']}' not found")
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
            except Exception as e:
                errors.append(f"#{ref['id']}: {e}")
            progress.progress((i + 1) / len(unanalyzed), text=f"Analyzed {i + 1} of {len(unanalyzed)}")

        progress.empty()
        if errors:
            st.warning("Finished with errors:\n" + "\n".join(errors))
        else:
            st.success(f"Done — {len(unanalyzed)} reflection(s) analyzed.")
        st.rerun()
else:
    st.info("All reflections have been analyzed.")

st.divider()

# ── Results table ────────────────────────────────────────────────────────────
st.subheader("Results")

rows = get_all_results()

if not rows:
    st.info("No results yet. Submit some reflections and run the analysis.")
else:
    import pandas as pd

    df = pd.DataFrame([dict(r) for r in rows])
    df = df.rename(columns={
        "reflection_id": "ID",
        "nickname": "Nickname",
        "topic_name": "Topic",
        "reflection_text": "Reflection",
        "student_confidence": "Confidence",
        "understanding": "Understanding",
        "misconception": "Misconception",
        "label": "Label",
    })

    LABEL_COLORS = {
        "understands": "🟢",
        "underconfident": "🔵",
        "confident_but_wrong": "🔴",
        "knows_confused": "🟡",
        "partial": "⚪",
    }
    df["Label"] = df["Label"].apply(lambda l: f"{LABEL_COLORS.get(l, '')} {l}")

    st.dataframe(df, use_container_width=True, hide_index=True)
