import streamlit as st
import pandas as pd
import altair as alt
from collections import defaultdict

from db import (
    get_unanalyzed_reflections,
    get_topic_info,
    save_result,
    get_topic_summaries,
    get_cbw_details,
)
from ai import analyze_reflection, compute_label

st.title("Faculty Dashboard")

# ── Explanation box ──────────────────────────────────────────────────────────
st.info(
    "**High confidence with low understanding is the highest-risk learning state** "
    "because those students are unlikely to ask for help. This dashboard identifies "
    "those topics first, so instructors know where reteaching will have the biggest impact."
)

st.divider()

# ── Analyze button ───────────────────────────────────────────────────────────
unanalyzed = get_unanalyzed_reflections()

if unanalyzed:
    st.write(f"**{len(unanalyzed)}** reflection(s) have not been analyzed yet.")
    if st.button("Analyze unanalyzed reflections", type="primary"):
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
            progress.progress(
                (i + 1) / len(unanalyzed),
                text=f"Analyzed {i + 1} of {len(unanalyzed)}",
            )
        progress.empty()
        if errors:
            st.warning("Finished with errors:\n" + "\n".join(errors))
        else:
            st.success(f"Done — {len(unanalyzed)} reflection(s) analyzed.")
        st.rerun()
else:
    st.caption("All reflections have been analyzed.")

st.divider()

# ── Topic-level results ───────────────────────────────────────────────────────
summary_rows = get_topic_summaries()

if not summary_rows:
    st.info("No results yet. Run the analysis above to populate this dashboard.")
    st.stop()

ALL_LABELS = ["understands", "underconfident", "partial", "knows_confused", "confident_but_wrong"]
LABEL_COLOR = {
    "understands":         "#22c55e",
    "underconfident":      "#3b82f6",
    "partial":             "#a78bfa",
    "knows_confused":      "#f59e0b",
    "confident_but_wrong": "#ef4444",
}
LABEL_DISPLAY = {
    "understands":         "Understands",
    "underconfident":      "Underconfident",
    "partial":             "Partial",
    "knows_confused":      "Knows confused",
    "confident_but_wrong": "Confident but wrong",
}

# Build per-topic structures
topic_data: dict[str, dict] = defaultdict(lambda: {
    "label_counts": {l: 0 for l in ALL_LABELS},
    "avg_confidence": 0.0,
    "avg_understanding": 0.0,
    "_conf_sum": 0.0,
    "_und_sum": 0.0,
    "_total": 0,
})

for row in summary_rows:
    t = row["topic_name"]
    lbl = row["label"]
    cnt = int(row["count"])
    topic_data[t]["label_counts"][lbl] = cnt
    topic_data[t]["_conf_sum"] += float(row["avg_confidence"]) * cnt
    topic_data[t]["_und_sum"] += float(row["avg_understanding"]) * cnt
    topic_data[t]["_total"] += cnt

for t, d in topic_data.items():
    total = d["_total"]
    d["avg_confidence"] = d["_conf_sum"] / total if total else 0
    d["avg_understanding"] = d["_und_sum"] / total if total else 0
    d["calibration_gap"] = d["avg_confidence"] - d["avg_understanding"]

# Sort topics: most confident_but_wrong first (Reteach First)
sorted_topics = sorted(
    topic_data.items(),
    key=lambda kv: kv[1]["label_counts"]["confident_but_wrong"],
    reverse=True,
)

# Build confident_but_wrong detail lookup
cbw_rows = get_cbw_details()
cbw_by_topic: dict[str, list] = defaultdict(list)
for row in cbw_rows:
    cbw_by_topic[row["topic_name"]].append(
        {"nickname": row["nickname"], "misconception": row["misconception"]}
    )

st.subheader("Topics — Reteach First")
st.caption(
    "Sorted by number of **Confident but wrong** reflections. "
    "Calibration gap = avg student confidence − avg model-assessed understanding."
)

for rank, (topic_name, d) in enumerate(sorted_topics, start=1):
    counts = d["label_counts"]
    gap = d["calibration_gap"]
    cbw_count = counts["confident_but_wrong"]
    uc_count = counts["underconfident"]

    with st.expander(f"**#{rank} · {topic_name}**", expanded=(rank <= 3)):

        # ── Metrics row ──────────────────────────────────────────────────
        c1, c2, c3 = st.columns(3)
        c1.metric("Confident but wrong", cbw_count)
        c2.metric(
            "Calibration gap",
            f"{gap:+.2f}",
            help="Avg student confidence − avg AI-assessed understanding. "
                 "Positive = class is overconfident on this topic.",
        )
        c3.metric("Total analyzed", d["_total"])

        # ── Stacked bar chart ─────────────────────────────────────────────
        bar_df = pd.DataFrame([
            {"Label": LABEL_DISPLAY[lbl], "Count": counts[lbl], "order": i}
            for i, lbl in enumerate(ALL_LABELS)
            if counts[lbl] > 0
        ])

        chart = (
            alt.Chart(bar_df)
            .mark_bar()
            .encode(
                x=alt.X("Count:Q", stack="normalize", axis=alt.Axis(format="%", title="")),
                color=alt.Color(
                    "Label:N",
                    scale=alt.Scale(
                        domain=[LABEL_DISPLAY[l] for l in ALL_LABELS],
                        range=[LABEL_COLOR[l] for l in ALL_LABELS],
                    ),
                    legend=alt.Legend(orient="bottom", columns=5, title=None),
                ),
                order=alt.Order("order:Q"),
                tooltip=["Label:N", "Count:Q"],
            )
            .properties(height=40)
        )
        st.altair_chart(chart, use_container_width=True, theme=None)

        # ── Underconfident note ──────────────────────────────────────────
        if uc_count >= 2:
            st.info(
                f"ℹ️ **{uc_count} underconfident** reflection(s) on this topic. "
                "These students understand the material but doubt themselves — "
                "reassurance and visible success will help more than reteaching.",
                icon=None,
            )

        # ── Confident-but-wrong detail list ─────────────────────────────
        if cbw_count > 0:
            st.markdown("**Confident but wrong — detected misconceptions:**")
            cbw_list = cbw_by_topic.get(topic_name, [])
            for item in cbw_list:
                misconception = item["misconception"]
                display = misconception if misconception.lower() != "none" else "—"
                st.markdown(
                    f"- `{item['nickname']}` · *{display}*"
                )
        else:
            st.success("No confident-but-wrong reflections on this topic.")
