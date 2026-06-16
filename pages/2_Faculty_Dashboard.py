import streamlit as st
from collections import defaultdict

from db import (
    get_unanalyzed_reflections,
    get_topic_info,
    save_result,
    get_topic_summaries,
    get_cbw_details,
    get_evidence_rows,
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

# ── Constants ────────────────────────────────────────────────────────────────
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


DISPLAY_TO_CANONICAL = {v: k for k, v in LABEL_DISPLAY.items()}


def normalize_label(raw: str) -> str:
    """Strip whitespace/emoji, lowercase, map display names back to canonical keys."""
    cleaned = raw.strip().lower()
    # Remove any leading emoji characters (non-ASCII)
    cleaned = "".join(ch for ch in cleaned if ch.isascii()).strip()
    # If it's already a canonical key, return it
    if cleaned in LABEL_COLOR:
        return cleaned
    # Try matching a display name (lowercased)
    for canonical, display in LABEL_DISPLAY.items():
        if cleaned == display.lower():
            return canonical
    return cleaned  # unknown — caller will handle it


def stacked_bar_html(raw_counts: dict) -> tuple[str, list[str]]:
    """
    Returns (html_string, list_of_unknown_labels).
    Uses flexbox so segments fill exactly 100% — no grey rounding gap.
    """
    counts: dict[str, int] = {}
    unknown: list[str] = []

    for raw_lbl, n in raw_counts.items():
        canonical = normalize_label(raw_lbl)
        if canonical in LABEL_COLOR:
            counts[canonical] = counts.get(canonical, 0) + int(n)
        elif int(n) > 0:
            unknown.append(f"{raw_lbl!r} ({n})")

    total = sum(counts.get(l, 0) for l in ALL_LABELS)
    if total == 0:
        return "", unknown

    # Flex-based bar: flex:N fills the container exactly, no rounding gaps
    segments = ""
    for lbl in ALL_LABELS:
        n = counts.get(lbl, 0)
        if n == 0:
            continue
        color = LABEL_COLOR[lbl]
        display = LABEL_DISPLAY[lbl]
        segments += (
            f'<div title="{display}: {n}" style="'
            f'flex:{n};background:{color};height:100%;"></div>'
        )

    legend_items = ""
    for lbl in ALL_LABELS:
        n = counts.get(lbl, 0)
        color = LABEL_COLOR[lbl]
        display = LABEL_DISPLAY[lbl]
        legend_items += (
            f'<span style="display:inline-flex;align-items:center;'
            f'margin-right:14px;font-size:12px;color:#444;">'
            f'<span style="width:12px;height:12px;border-radius:2px;'
            f'background:{color};display:inline-block;margin-right:4px;'
            f'flex-shrink:0;"></span>{display} ({n})</span>'
        )

    html = (
        f'<div style="width:100%;height:26px;border-radius:4px;'
        f'overflow:hidden;display:flex;margin-bottom:6px;">'
        f'{segments}</div>'
        f'<div style="display:flex;flex-wrap:wrap;margin-bottom:8px;">'
        f'{legend_items}</div>'
    )
    return html, unknown


# ── Topic-level results ───────────────────────────────────────────────────────
summary_rows = get_topic_summaries()

if not summary_rows:
    st.info("No results yet. Run the analysis above to populate this dashboard.")
    st.stop()

# Build per-topic structures
topic_data: dict = defaultdict(lambda: {
    "label_counts": {l: 0 for l in ALL_LABELS},
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

# Sort: most confident_but_wrong first (Reteach First)
sorted_topics = sorted(
    topic_data.items(),
    key=lambda kv: kv[1]["label_counts"]["confident_but_wrong"],
    reverse=True,
)

# Confident-but-wrong detail lookup
cbw_rows = get_cbw_details()
cbw_by_topic: dict = defaultdict(list)
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

        # ── Stacked bar (HTML/CSS) ────────────────────────────────────────
        bar_html, unknown_labels = stacked_bar_html(counts)
        st.markdown(bar_html, unsafe_allow_html=True)
        if unknown_labels:
            st.warning(f"Unknown label(s) in data — shown in grey: {', '.join(unknown_labels)}")

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
            for item in cbw_by_topic.get(topic_name, []):
                misconception = item["misconception"]
                display = misconception if misconception.lower() != "none" else "—"
                st.markdown(f"- `{item['nickname']}` · *{display}*")
        else:
            st.success("No confident-but-wrong reflections on this topic.")

st.divider()

# ── Evidence section ──────────────────────────────────────────────────────────
st.subheader("Evidence")
st.caption(
    "Compares computed labels against ground-truth labels from the simulated dataset. "
    "Uses only reflections that have a ground-truth label and have been analyzed."
)

evidence_rows = get_evidence_rows()

if not evidence_rows:
    st.warning("No ground-truth rows found. Run the analysis first, or check that reflections have a ground_truth_label.")
    st.stop()

# Normalize both labels using the same function already defined above
pairs = []
for row in evidence_rows:
    gt = normalize_label(row["ground_truth_label"])
    pred = normalize_label(row["computed_label"])
    pairs.append((gt, pred))

total = len(pairs)
correct = sum(1 for gt, pred in pairs if gt == pred)
accuracy = correct / total if total else 0

# ── Overall accuracy ─────────────────────────────────────────────────────────
st.metric("Overall accuracy", f"{accuracy:.0%}", help=f"{correct} correct out of {total} ground-truth reflections")

# ── Confident-but-wrong precision and recall ──────────────────────────────────
CBW = "confident_but_wrong"
tp  = sum(1 for gt, pred in pairs if gt == CBW and pred == CBW)
fp  = sum(1 for gt, pred in pairs if gt != CBW and pred == CBW)
fn  = sum(1 for gt, pred in pairs if gt == CBW and pred != CBW)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0

c1, c2 = st.columns(2)
c1.metric(
    "Confident-but-wrong precision",
    f"{precision:.0%}",
    help="Of all reflections the model flagged as confident-but-wrong, this share truly were.",
)
c2.metric(
    "Confident-but-wrong recall",
    f"{recall:.0%}",
    help="Of all ground-truth confident-but-wrong reflections, this share the model caught.",
)

# ── Confusion matrix ─────────────────────────────────────────────────────────
import pandas as pd

st.markdown("**Confusion matrix** — rows: ground truth · columns: computed label")

matrix: dict[str, dict[str, int]] = {l: {l2: 0 for l2 in ALL_LABELS} for l in ALL_LABELS}
unknown_gt, unknown_pred = set(), set()

for gt, pred in pairs:
    if gt not in matrix:
        unknown_gt.add(gt)
        continue
    if pred not in matrix[gt]:
        unknown_pred.add(pred)
        continue
    matrix[gt][pred] += 1

cm_df = pd.DataFrame(matrix).T.reindex(index=ALL_LABELS, columns=ALL_LABELS).fillna(0).astype(int)
cm_df.index.name = "ground truth \\ computed"

st.dataframe(cm_df, use_container_width=True)

if unknown_gt or unknown_pred:
    st.warning(
        f"Unrecognized labels skipped — ground truth: {unknown_gt or 'none'} · "
        f"computed: {unknown_pred or 'none'}"
    )
