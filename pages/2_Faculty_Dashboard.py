import pandas as pd
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

st.set_page_config(
    page_title="Faculty Dashboard — Calibration Detector",
    page_icon="📊",
    layout="wide",
)

# ── NYU Violet theme ──────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Constrain content width and center ─────────────────────────── */
.block-container {
    max-width: 1200px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ── Active tab underline → NYU Violet ──────────────────────────── */
[data-baseweb="tab-highlight"] {
    background-color: #57068C !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #57068C !important;
    font-weight: 700 !important;
}
[data-testid="stTabs"] button:hover {
    color: #57068C !important;
}

/* ── Primary buttons → NYU Violet (keep red for alerts only) ────── */
[data-testid="baseButton-primary"] {
    background-color: #57068C !important;
    border-color: #57068C !important;
    color: #ffffff !important;
}
[data-testid="baseButton-primary"]:hover {
    background-color: #3d0466 !important;
    border-color: #3d0466 !important;
}

/* ── Section headings accent ────────────────────────────────────── */
h2, h3 { color: #57068C !important; }

/* ── Dataframe: prevent horizontal scroll by allowing cell wrap ─── */
[data-testid="stDataFrame"] table { table-layout: auto; word-break: break-word; }
[data-testid="stDataFrame"] td { white-space: normal !important; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Faculty Dashboard")

# ── Constants ─────────────────────────────────────────────────────────────────
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

ADVERSARIAL_CASES = [
    {
        "topic_name": "Crossing the Chasm",
        "reflection_text": (
            "I completely understand Crossing the Chasm. It is basically when an innovation "
            "moves smoothly from innovators straight into the early majority because the market "
            "naturally catches up once the product is exciting enough. The chasm is just another "
            "name for the full Rogers adoption curve."
        ),
        "student_confidence": 5,
        "expected_label": "confident_but_wrong",
    },
    {
        "topic_name": "Diffusion of Innovation",
        "reflection_text": (
            "Diffusion of Innovation is simple. The order is innovators, early majority, early "
            "adopters, late majority, and laggards. If the technology is good, people will adopt "
            "it automatically because the product itself controls the spread."
        ),
        "student_confidence": 5,
        "expected_label": "confident_but_wrong",
    },
    {
        "topic_name": "User-Led Adoption",
        "reflection_text": (
            "User-Led Adoption means companies listen to customer feedback, run surveys, and then "
            "their R&D teams build products for users. Lead users are basically the same as early "
            "adopters because they buy the product first and tell others about it."
        ),
        "student_confidence": 5,
        "expected_label": "confident_but_wrong",
    },
    {
        "topic_name": "Technology Creation",
        "reflection_text": (
            "Technology Creation is when a genius inventor creates something completely original "
            "from scratch. Recombination is mostly copying existing tools, so real technology "
            "creation happens when someone invents a brand-new idea no one has ever built from before."
        ),
        "student_confidence": 5,
        "expected_label": "confident_but_wrong",
    },
    {
        "topic_name": "Creative Destruction",
        "reflection_text": (
            "Creative Destruction means companies compete harder and lower prices until weaker "
            "businesses disappear. The destruction is an unfortunate side effect of competition, "
            "but the real growth comes from normal market rivalry and better marketing."
        ),
        "student_confidence": 5,
        "expected_label": "confident_but_wrong",
    },
    {
        "topic_name": "Adopt-Transform-Apply",
        "reflection_text": (
            "Adopt-Transform-Apply means finding a successful idea in another company and copying "
            "it into your own business as quickly as possible. The apply step is mostly just "
            "launching it, because the hard part is finding the idea in the first place."
        ),
        "student_confidence": 5,
        "expected_label": "confident_but_wrong",
    },
]


def normalize_label(raw: str) -> str:
    cleaned = raw.strip().lower()
    cleaned = "".join(ch for ch in cleaned if ch.isascii()).strip()
    if cleaned in LABEL_COLOR:
        return cleaned
    for canonical, display in LABEL_DISPLAY.items():
        if cleaned == display.lower():
            return canonical
    return cleaned


def stacked_bar_html(raw_counts: dict) -> tuple[str, list[str]]:
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


# ── Fetch data once (shared across tabs) ─────────────────────────────────────
unanalyzed   = get_unanalyzed_reflections()
summary_rows = get_topic_summaries()
cbw_rows     = get_cbw_details()
evidence_rows = get_evidence_rows()

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

sorted_topics = sorted(
    topic_data.items(),
    key=lambda kv: kv[1]["label_counts"]["confident_but_wrong"],
    reverse=True,
)

cbw_by_topic: dict = defaultdict(list)
for row in cbw_rows:
    cbw_by_topic[row["topic_name"]].append(
        {"nickname": row["nickname"], "misconception": row["misconception"]}
    )

# Evidence pairs
evidence_pairs = []
for row in evidence_rows:
    gt   = normalize_label(row["ground_truth_label"])
    pred = normalize_label(row["computed_label"])
    evidence_pairs.append((gt, pred))

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_overview, tab_topics, tab_evidence, tab_robustness = st.tabs([
    "Overview", "Topic Details", "Evidence", "Robustness Check"
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Overview
# ════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.info(
        "**High confidence with low understanding is the highest-risk learning state** "
        "because those students are unlikely to ask for help. This dashboard identifies "
        "those topics first, so instructors know where reteaching will have the biggest impact."
    )

    st.divider()

    # Analyze button
    if unanalyzed:
        st.write(f"**{len(unanalyzed)}** reflection(s) have not been analyzed yet.")
        if st.button("Analyze unanalyzed reflections", type="primary", key="analyze_btn"):
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

    if not summary_rows:
        st.info("No results yet. Run the analysis above to populate this dashboard.")
    else:
        st.divider()

        # High-level metrics
        total_analyzed = sum(d["_total"] for _, d in sorted_topics)
        total_cbw      = sum(d["label_counts"]["confident_but_wrong"] for _, d in sorted_topics)
        avg_gap        = (
            sum(d["calibration_gap"] * d["_total"] for _, d in sorted_topics) / total_analyzed
            if total_analyzed else 0
        )
        topics_with_uc = sum(1 for _, d in sorted_topics if d["label_counts"]["underconfident"] >= 2)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total analyzed", total_analyzed)
            st.caption("Reflections processed by the model")
        with m2:
            st.metric("Confident but wrong", total_cbw)
            st.caption("Highest-priority learning risk")
        with m3:
            st.metric("Avg calibration gap", f"{avg_gap:+.2f}")
            st.caption("Positive means students are overconfident")
        with m4:
            st.metric("Topics with underconfidence", topics_with_uc)
            st.caption("May need reassurance, not reteaching")

        def gap_label(gap: float) -> str:
            if gap >= 1.0:  return "High overconfidence"
            if gap >= 0.5:  return "Moderate overconfidence"
            if gap > 0:     return "Slight overconfidence"
            if gap == 0:    return "Calibrated"
            return "Underconfident"

        def action_badge(cbw: int, uc: int) -> str:
            if cbw >= 3:  return "🔴 Reteach first"
            if cbw == 2:  return "🟠 Watch closely"
            if uc >= 2:   return "🔵 Reassure students"
            return "⚫ Monitor"

        def action_bg(cbw: int, uc: int) -> str:
            if cbw >= 3:  return "#ef4444"
            if cbw == 2:  return "#f97316"
            if uc >= 2:   return "#3b82f6"
            return "#6b7280"

        # Top insight callout
        top_cbw_topics = [(name, d) for name, d in sorted_topics
                          if d["label_counts"]["confident_but_wrong"] > 0][:4]
        if top_cbw_topics:
            topic_list = ", ".join(f"**{name}**" for name, _ in top_cbw_topics)
            count_desc = (
                f"{top_cbw_topics[0][1]['label_counts']['confident_but_wrong']} confident-but-wrong "
                "reflection(s) on the top topic"
                if len(top_cbw_topics) == 1
                else (
                    f"between {top_cbw_topics[-1][1]['label_counts']['confident_but_wrong']} and "
                    f"{top_cbw_topics[0][1]['label_counts']['confident_but_wrong']} "
                    "confident-but-wrong reflections each"
                )
            )
            st.markdown(
                f"""<div style="background:#fdf4ff;border-left:4px solid #57068C;
                border-radius:6px;padding:14px 18px;margin:16px 0;">
                <span style="font-size:15px;font-weight:700;color:#57068C;">🔍 Top insight</span><br>
                <span style="font-size:14px;color:#333;">{', '.join(f'<strong>{n}</strong>' for n, _ in top_cbw_topics)}
                show the highest overconfidence risk ({count_desc}).
                Review these topics first — see Topic Details for the detected misconceptions.</span><br><br>
                <span style="font-size:13px;color:#57068C;font-weight:600;">What to do next</span><br>
                <span style="font-size:13px;color:#555;">Start with the top-ranked topics, review the detected
                misconceptions, then decide whether students need reteaching or reassurance.</span>
                </div>""",
                unsafe_allow_html=True,
            )

        st.divider()

        # 4 compact topic cards
        if top_cbw_topics:
            st.markdown(
                "<p style='font-size:13px;color:#888;margin-bottom:8px;'>"
                "Top topics by overconfidence risk</p>",
                unsafe_allow_html=True,
            )
            card_cols = st.columns(min(len(top_cbw_topics), 4))
            for col, (name, d) in zip(card_cols, top_cbw_topics):
                cbw  = d["label_counts"]["confident_but_wrong"]
                uc   = d["label_counts"]["underconfident"]
                gap  = d["calibration_gap"]
                bg   = action_bg(cbw, uc)
                badge = action_badge(cbw, uc)
                col.markdown(
                    f"""<div style="border:2px solid #57068C;border-radius:10px;
                    padding:14px 16px;background:#faf5ff;height:100%;">
                    <div style="font-weight:700;font-size:13px;color:#57068C;
                    margin-bottom:10px;line-height:1.3;">{name}</div>
                    <div style="font-size:26px;font-weight:800;color:#ef4444;
                    line-height:1;">{cbw}</div>
                    <div style="font-size:11px;color:#666;margin-bottom:8px;">
                    confident but wrong</div>
                    <div style="font-size:12px;color:#555;margin-bottom:10px;">
                    Gap: {gap:+.2f} · {gap_label(gap)}</div>
                    <div style="background:{bg};color:white;border-radius:4px;
                    padding:3px 8px;font-size:11px;font-weight:600;
                    display:inline-block;">{badge}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

        # Compact Reteach First table
        st.subheader("Reteach First")
        st.caption("Sorted by confident-but-wrong count. Calibration gap = avg student confidence − avg understanding.")

        reteach_df = pd.DataFrame([
            {
                "Rank":                rank,
                "Topic":               topic_name,
                "Confident but wrong": d["label_counts"]["confident_but_wrong"],
                "Gap":                 f"{d['calibration_gap']:+.2f}  {gap_label(d['calibration_gap'])}",
                "Recommended action":  action_badge(
                    d["label_counts"]["confident_but_wrong"],
                    d["label_counts"]["underconfident"],
                ),
            }
            for rank, (topic_name, d) in enumerate(sorted_topics, start=1)
        ])
        st.dataframe(reteach_df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Topic Details
# ════════════════════════════════════════════════════════════════════════════
with tab_topics:
    if not summary_rows:
        st.info("No results yet. Run the analysis in the Overview tab.")
    else:
        st.caption(
            "Sorted by **Confident but wrong** count. "
            "Calibration gap = avg student confidence − avg model-assessed understanding."
        )
        for rank, (topic_name, d) in enumerate(sorted_topics, start=1):
            counts    = d["label_counts"]
            gap       = d["calibration_gap"]
            cbw_count = counts["confident_but_wrong"]
            uc_count  = counts["underconfident"]

            with st.expander(f"**#{rank} · {topic_name}**", expanded=(rank == 1)):
                c1, c2, c3 = st.columns(3)
                c1.metric("Confident but wrong", cbw_count)
                c2.metric(
                    "Calibration gap", f"{gap:+.2f}",
                    help="Avg student confidence − avg AI-assessed understanding. "
                         "Positive = class is overconfident on this topic.",
                )
                c3.metric("Total analyzed", d["_total"])

                bar_html, unknown_labels = stacked_bar_html(counts)
                st.markdown(bar_html, unsafe_allow_html=True)
                if unknown_labels:
                    st.warning(f"Unknown label(s): {', '.join(unknown_labels)}")

                if uc_count >= 2:
                    st.info(
                        f"ℹ️ **{uc_count} underconfident** reflection(s) on this topic. "
                        "These students understand the material but doubt themselves — "
                        "reassurance and visible success will help more than reteaching.",
                        icon=None,
                    )

                if cbw_count > 0:
                    st.markdown("**Confident but wrong — detected misconceptions:**")
                    for item in cbw_by_topic.get(topic_name, []):
                        misconception = item["misconception"]
                        display = misconception if misconception.lower() != "none" else "—"
                        st.markdown(f"- `{item['nickname']}` · *{display}*")
                else:
                    st.success("No confident-but-wrong reflections on this topic.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Evidence
# ════════════════════════════════════════════════════════════════════════════
with tab_evidence:
    st.caption(
        "Compares computed labels against ground-truth labels from the simulated dataset. "
        "Uses only reflections that have a ground-truth label and have been analyzed."
    )

    if not evidence_pairs:
        st.warning(
            "No ground-truth rows found. Run the analysis first, or check that "
            "reflections have a ground_truth_label."
        )
    else:
        total   = len(evidence_pairs)
        correct = sum(1 for gt, pred in evidence_pairs if gt == pred)
        accuracy = correct / total if total else 0

        st.metric(
            "Overall accuracy", f"{accuracy:.0%}",
            help=f"{correct} correct out of {total} ground-truth reflections",
        )

        CBW = "confident_but_wrong"
        tp  = sum(1 for gt, pred in evidence_pairs if gt == CBW and pred == CBW)
        fp  = sum(1 for gt, pred in evidence_pairs if gt != CBW and pred == CBW)
        fn  = sum(1 for gt, pred in evidence_pairs if gt == CBW and pred != CBW)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        c1, c2 = st.columns(2)
        c1.metric(
            "Confident-but-wrong precision", f"{precision:.0%}",
            help="Of all reflections the model flagged as confident-but-wrong, this share truly were.",
        )
        c2.metric(
            "Confident-but-wrong recall", f"{recall:.0%}",
            help="Of all ground-truth confident-but-wrong reflections, this share the model caught.",
        )

        st.markdown(
            """<div style="background:#fdf4ff;border-left:4px solid #57068C;
            border-radius:6px;padding:14px 18px;margin:12px 0;">
            <span style="font-size:14px;font-weight:700;color:#57068C;">
            About this panel</span><br>
            <span style="font-size:13px;color:#333;">
            The evidence panel checks whether computed labels match the simulated ground truth.
            The most important metric is <strong>confident-but-wrong recall</strong>, because
            the tool is designed to catch students who are confident but mistaken.
            </span></div>""",
            unsafe_allow_html=True,
        )

        st.markdown("**Confusion matrix** — rows: ground truth · columns: computed label")

        matrix: dict[str, dict[str, int]] = {l: {l2: 0 for l2 in ALL_LABELS} for l in ALL_LABELS}
        unknown_gt, unknown_pred = set(), set()
        for gt, pred in evidence_pairs:
            if gt not in matrix:
                unknown_gt.add(gt)
                continue
            if pred not in matrix[gt]:
                unknown_pred.add(pred)
                continue
            matrix[gt][pred] += 1

        cm_df = (
            pd.DataFrame(matrix).T
            .reindex(index=ALL_LABELS, columns=ALL_LABELS)
            .fillna(0).astype(int)
        )
        cm_df.index.name = "ground truth \\ computed"
        st.dataframe(cm_df, use_container_width=True)

        if unknown_gt or unknown_pred:
            st.warning(
                f"Unrecognized labels skipped — ground truth: {unknown_gt or 'none'} · "
                f"computed: {unknown_pred or 'none'}"
            )

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Robustness Check
# ════════════════════════════════════════════════════════════════════════════
with tab_robustness:
    st.caption(
        "Six built-in reflections that sound confident and use course keywords but contain "
        "weak or wrong understanding. All have student confidence = 5. "
        "Pass means the model correctly labels them **confident_but_wrong**. "
        "These cases are never saved to the database and do not affect any other metric."
    )

    if st.button("Run adversarial robustness check", type="primary", key="adv_btn"):
        adv_progress = st.progress(0, text="Starting…")
        adv_results = []
        adv_errors  = []

        for i, case in enumerate(ADVERSARIAL_CASES):
            topic = get_topic_info(case["topic_name"])
            try:
                analysis = analyze_reflection(
                    reflection_text=case["reflection_text"],
                    topic_description=topic["description"] if topic else "",
                    topic_misconceptions=topic["misconceptions"] if topic else "",
                )
                computed = compute_label(
                    understanding=analysis["understanding"],
                    confidence=case["student_confidence"],
                )
                passed = computed == case["expected_label"]
                adv_results.append({
                    "Topic":          case["topic_name"],
                    "Reflection":     case["reflection_text"],
                    "Understanding":  analysis["understanding"],
                    "Misconception":  analysis["misconception"],
                    "Computed label": computed,
                    "Expected label": case["expected_label"],
                    "Result":         "✅ Pass" if passed else "❌ Fail",
                })
            except Exception as e:
                adv_errors.append(f"{case['topic_name']}: {e}")
                adv_results.append({
                    "Topic":          case["topic_name"],
                    "Reflection":     case["reflection_text"],
                    "Understanding":  "—",
                    "Misconception":  "—",
                    "Computed label": "error",
                    "Expected label": case["expected_label"],
                    "Result":         "❌ Error",
                })
            adv_progress.progress(
                (i + 1) / len(ADVERSARIAL_CASES),
                text=f"Checked {i + 1} of {len(ADVERSARIAL_CASES)}",
            )

        adv_progress.empty()

        if adv_errors:
            st.warning("Errors during check:\n" + "\n".join(adv_errors))

        passes = sum(1 for r in adv_results if r["Result"].startswith("✅"))
        st.metric("Robustness pass rate", f"{passes}/{len(ADVERSARIAL_CASES)}")

        compact_df = pd.DataFrame([
            {
                "Topic":         r["Topic"],
                "Understanding": r["Understanding"],
                "Misconception": r["Misconception"],
                "Computed":      r["Computed label"],
                "Expected":      r["Expected label"],
                "Result":        r["Result"],
            }
            for r in adv_results
        ])
        st.dataframe(compact_df, use_container_width=True, hide_index=True)

        st.markdown("**Reflection text per case:**")
        for r in adv_results:
            with st.expander(f"{r['Result']} {r['Topic']}"):
                st.write(r["Reflection"])
