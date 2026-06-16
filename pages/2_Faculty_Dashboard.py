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
/* ── Content width ───────────────────────────────────────────────── */
.block-container {
    max-width: 1240px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ── Active tab → NYU Violet ────────────────────────────────────── */
[data-baseweb="tab-highlight"] { background-color: #57068C !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #57068C !important; font-weight: 600 !important;
}

/* ── Primary buttons → NYU Violet ───────────────────────────────── */
[data-testid="baseButton-primary"] {
    background-color: #57068C !important;
    border-color: #57068C !important; color: #ffffff !important;
}
[data-testid="baseButton-primary"]:hover {
    background-color: #3d0466 !important; border-color: #3d0466 !important;
}

/* ── Metric cards ────────────────────────────────────────────────── */
.metric-card {
    background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 18px 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    height: 100%; box-sizing: border-box;
}
.metric-value { font-size: 30px; font-weight: 800; line-height: 1.1; }
.metric-sublabel { font-size: 11px; font-weight: 600; letter-spacing:.4px;
    text-transform: uppercase; margin-bottom: 4px; }
.metric-caption { font-size: 12px; color: #777; margin-top: 5px; }

/* ── Callout / insight cards ─────────────────────────────────────── */
.callout-card {
    background: #f9f5ff; border-left: 4px solid #57068C;
    border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 12px 0;
    box-shadow: 0 1px 3px rgba(87,6,140,0.08);
}

/* ── Priority topic cards ────────────────────────────────────────── */
.pri-card {
    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
    overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.06); height: 100%;
}
.pri-card-body { padding: 14px 16px; }
.pri-card-name {
    font-size: 13px; font-weight: 700; color: #1a1a2e;
    margin-bottom: 10px; line-height: 1.3;
}
.pri-card-num { font-size: 26px; font-weight: 800; line-height: 1; }
.pri-card-sub { font-size: 11px; color: #888; margin-bottom: 6px; }
.pri-card-gap { font-size: 12px; color: #555; margin-bottom: 10px; }

/* ── Reteach First table ─────────────────────────────────────────── */
.reteach-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.reteach-table th {
    text-align: left; padding: 9px 12px; font-weight: 600; font-size: 12px;
    text-transform: uppercase; letter-spacing: .4px; color: #666;
    border-bottom: 2px solid #e5e7eb; background: #f9fafb;
}
.reteach-table td {
    padding: 9px 12px; border-bottom: 1px solid #f0f0f0;
    vertical-align: middle; word-break: break-word;
}
.reteach-table tbody tr:nth-child(even) td { background: #fafafa; }
.reteach-table tbody tr:hover td { background: #f3f0ff; }

/* ── Action badges ───────────────────────────────────────────────── */
.badge {
    display: inline-block; border-radius: 4px; padding: 3px 9px;
    font-size: 12px; font-weight: 600; white-space: nowrap;
}

/* ── Evidence metric cards ───────────────────────────────────────── */
.ev-card {
    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 16px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    text-align: center;
}
.ev-value { font-size: 32px; font-weight: 800; line-height: 1.1; }
.ev-label { font-size: 12px; color: #666; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Header card ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#f5eeff 0%,#faf7ff 55%,#ffffff 100%);
border:1px solid #ddd0ec;border-radius:12px;padding:22px 28px;margin-bottom:6px;">
<div style="font-size:27px;font-weight:800;color:#1a1a2e;margin-bottom:4px;">
Faculty Dashboard</div>
<div style="font-size:14px;color:#666;">
Confidence vs. demonstrated understanding across student reflections.</div>
</div>
""", unsafe_allow_html=True)

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
    st.markdown("""
    <div class="callout-card">
    <span style="font-size:13px;font-weight:700;color:#57068C;">⚠ Key risk signal</span><br>
    <span style="font-size:13px;color:#333;">
    <strong>High confidence with low understanding is the highest-risk learning state</strong>
    because those students are unlikely to ask for help. This dashboard identifies those topics
    first, so instructors know where reteaching will have the biggest impact.
    </span></div>
    """, unsafe_allow_html=True)

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
                st.success(f"Done. {len(unanalyzed)} reflection(s) analyzed.")
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
        m1.markdown(f"""
        <div class="metric-card" style="border-top:3px solid #57068C;">
        <div class="metric-sublabel" style="color:#57068C;">📋 Total analyzed</div>
        <div class="metric-value" style="color:#1a1a2e;">{total_analyzed}</div>
        <div class="metric-caption">Reflections processed by the model</div>
        </div>""", unsafe_allow_html=True)
        m2.markdown(f"""
        <div class="metric-card" style="border-top:3px solid #dc2626;">
        <div class="metric-sublabel" style="color:#dc2626;">⚠ Confident but wrong</div>
        <div class="metric-value" style="color:#dc2626;">{total_cbw}</div>
        <div class="metric-caption">Highest-priority learning risk</div>
        </div>""", unsafe_allow_html=True)
        m3.markdown(f"""
        <div class="metric-card" style="border-top:3px solid #d97706;">
        <div class="metric-sublabel" style="color:#d97706;">📈 Avg calibration gap</div>
        <div class="metric-value" style="color:#d97706;">{avg_gap:+.2f}</div>
        <div class="metric-caption">Positive means students are overconfident</div>
        </div>""", unsafe_allow_html=True)
        m4.markdown(f"""
        <div class="metric-card" style="border-top:3px solid #2563eb;">
        <div class="metric-sublabel" style="color:#2563eb;">🔵 Underconfidence topics</div>
        <div class="metric-value" style="color:#2563eb;">{topics_with_uc}</div>
        <div class="metric-caption">May need reassurance, not reteaching</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

        def gap_label(gap: float) -> str:
            if gap >= 1.0:  return "High overconfidence"
            if gap >= 0.5:  return "Moderate overconfidence"
            if gap > 0:     return "Slight overconfidence"
            if gap == 0:    return "Calibrated"
            return "Underconfident"

        def action_label(cbw: int, uc: int) -> str:
            if cbw >= 3:  return "Reteach first"
            if cbw == 2:  return "Watch closely"
            if uc >= 2:   return "Reassure students"
            return "Monitor"

        def action_chip_html(cbw: int, uc: int) -> str:
            label = action_label(cbw, uc)
            styles = {
                "Reteach first":     ("color:#b91c1c;background:#fef2f2;"),
                "Watch closely":     ("color:#b45309;background:#fffbeb;"),
                "Reassure students": ("color:#1d4ed8;background:#eff6ff;"),
                "Monitor":           ("color:#6b7280;background:#f3f4f6;"),
            }
            s = styles.get(label, "color:#333;background:#f3f4f6;")
            return f'<span class="badge" style="{s}">{label}</span>'

        # Top insight callout
        top_cbw_topics = [(name, d) for name, d in sorted_topics
                          if d["label_counts"]["confident_but_wrong"] > 0][:4]
        if top_cbw_topics:
            hi = top_cbw_topics[0][1]["label_counts"]["confident_but_wrong"]
            lo = top_cbw_topics[-1][1]["label_counts"]["confident_but_wrong"]
            if len(top_cbw_topics) == 1:
                count_desc = f"{hi} confident-but-wrong reflection(s) on the top topic"
            elif hi == lo:
                count_desc = f"{hi} confident-but-wrong reflections each"
            else:
                count_desc = f"between {lo} and {hi} confident-but-wrong reflections each"
            names_html = ", ".join(f"<strong>{n}</strong>" for n, _ in top_cbw_topics)
            st.markdown(
                f"""<div class="callout-card">
                <div style="font-size:13px;font-weight:700;color:#57068C;margin-bottom:6px;">
                🔍 Top insight</div>
                <div style="font-size:13px;color:#333;margin-bottom:8px;">
                {names_html} show the highest overconfidence risk ({count_desc}).
                Review these topics first. See Topic Details for the detected misconceptions.
                </div>
                <div style="font-size:12px;color:#555;">
                <strong>What to do next:</strong> Start with the top-ranked topics, review
                the detected misconceptions, then decide whether students need reteaching
                or reassurance.</div></div>""",
                unsafe_allow_html=True,
            )

            # 3 compact priority cards
            pri_topics = top_cbw_topics[:3]
            def pri_accent(cbw: int, uc: int) -> str:
                if cbw >= 3: return "#dc2626"
                if cbw == 2: return "#d97706"
                if uc >= 2:  return "#2563eb"
                return "#6b7280"

            st.markdown("<div style='margin-top:16px;margin-bottom:4px;font-size:12px;"
                        "color:#888;font-weight:600;text-transform:uppercase;"
                        "letter-spacing:.5px;'>Priority topics</div>",
                        unsafe_allow_html=True)
            pri_cols = st.columns(len(pri_topics))
            for col, (name, d) in zip(pri_cols, pri_topics):
                cbw  = d["label_counts"]["confident_but_wrong"]
                uc   = d["label_counts"]["underconfident"]
                gap  = d["calibration_gap"]
                acc  = pri_accent(cbw, uc)
                chip = action_chip_html(cbw, uc)
                col.markdown(
                    f"""<div class="pri-card">
                    <div style="height:4px;background:{acc};"></div>
                    <div class="pri-card-body">
                    <div class="pri-card-name">{name}</div>
                    <div class="pri-card-num" style="color:{acc};">{cbw}</div>
                    <div class="pri-card-sub">confident but wrong</div>
                    <div class="pri-card-gap">Gap: {gap:+.2f} · {gap_label(gap)}</div>
                    {chip}
                    </div></div>""",
                    unsafe_allow_html=True,
                )

        st.divider()

        # Reteach First table
        st.subheader("Reteach First")
        st.caption(
            "Sorted by confident-but-wrong count. "
            "Calibration gap = avg student confidence − avg understanding. "
            "This is a relative ranking. A topic can appear even if it only needs monitoring."
        )

        rows_html = ""
        for rank, (topic_name, d) in enumerate(sorted_topics, start=1):
            cbw = d["label_counts"]["confident_but_wrong"]
            uc  = d["label_counts"]["underconfident"]
            gap = d["calibration_gap"]
            rows_html += (
                f"<tr>"
                f"<td style='width:44px;color:#888;'>{rank}</td>"
                f"<td>{topic_name}</td>"
                f"<td style='width:130px;text-align:center;'>{cbw}</td>"
                f"<td style='width:200px;'>{gap:+.2f} <span style='color:#888;font-size:12px;'>"
                f"{gap_label(gap)}</span></td>"
                f"<td style='width:160px;'>{action_chip_html(cbw, uc)}</td>"
                f"</tr>"
            )
        st.markdown(
            f"""<table class="reteach-table">
            <thead><tr>
            <th>#</th><th>Topic</th>
            <th style="text-align:center;">Confident but wrong</th>
            <th>Gap</th><th>Recommended action</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
            </table>""",
            unsafe_allow_html=True,
        )

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
                        "These students understand the material but doubt themselves. "
                        "Reassurance and visible success will help more than reteaching.",
                        icon=None,
                    )

                if cbw_count > 0:
                    st.markdown("**Confident but wrong: detected misconceptions**")
                    for item in cbw_by_topic.get(topic_name, []):
                        misconception = item["misconception"]
                        display = misconception if misconception.lower() != "none" else "(none)"
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

        CBW = "confident_but_wrong"
        tp  = sum(1 for gt, pred in evidence_pairs if gt == CBW and pred == CBW)
        fp  = sum(1 for gt, pred in evidence_pairs if gt != CBW and pred == CBW)
        fn  = sum(1 for gt, pred in evidence_pairs if gt == CBW and pred != CBW)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        ev1, ev2, ev3 = st.columns(3)
        ev1.markdown(f"""
        <div class="ev-card" style="border-top:3px solid #57068C;">
        <div style="font-size:11px;font-weight:600;color:#57068C;text-transform:uppercase;
        letter-spacing:.4px;margin-bottom:4px;">Overall accuracy</div>
        <div class="ev-value" style="color:#1a1a2e;">{accuracy:.0%}</div>
        <div class="ev-label">{correct} of {total} ground-truth reflections correct</div>
        </div>""", unsafe_allow_html=True)
        ev2.markdown(f"""
        <div class="ev-card" style="border-top:3px solid #d97706;">
        <div style="font-size:11px;font-weight:600;color:#d97706;text-transform:uppercase;
        letter-spacing:.4px;margin-bottom:4px;">CBW precision</div>
        <div class="ev-value" style="color:#d97706;">{precision:.0%}</div>
        <div class="ev-label">Of flagged CBW, this share truly were</div>
        </div>""", unsafe_allow_html=True)
        ev3.markdown(f"""
        <div class="ev-card" style="border-top:3px solid #dc2626;">
        <div style="font-size:11px;font-weight:600;color:#dc2626;text-transform:uppercase;
        letter-spacing:.4px;margin-bottom:4px;">CBW recall ← key metric</div>
        <div class="ev-value" style="color:#dc2626;">{recall:.0%}</div>
        <div class="ev-label">Of true CBW cases, this share were caught</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="callout-card">
        <div style="font-size:13px;font-weight:700;color:#57068C;margin-bottom:5px;">
        About this panel</div>
        <div style="font-size:13px;color:#333;">
        Compares computed labels against simulated ground truth. The most important metric is
        <strong>confident-but-wrong recall</strong>, because the tool is designed to catch
        students who are confident but mistaken. Missing a CBW case (low recall) is a more serious
        failure than a false positive.
        </div></div>""", unsafe_allow_html=True)

        st.markdown("**Confusion matrix** (rows: ground truth, columns: computed label)")

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
                f"Unrecognized labels skipped. Ground truth: {unknown_gt or 'none'}, "
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
                    "Understanding":  "N/A",
                    "Misconception":  "N/A",
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
        total_cases = len(ADVERSARIAL_CASES)
        rate_color = "#16a34a" if passes == total_cases else ("#d97706" if passes >= total_cases // 2 else "#dc2626")
        st.markdown(f"""
        <div class="ev-card" style="border-top:3px solid {rate_color};max-width:260px;
        text-align:left;margin-bottom:12px;">
        <div style="font-size:11px;font-weight:600;color:{rate_color};text-transform:uppercase;
        letter-spacing:.4px;margin-bottom:4px;">Robustness pass rate</div>
        <div class="ev-value" style="color:{rate_color};">{passes}/{total_cases}</div>
        <div class="ev-label">adversarial cases correctly labeled confident_but_wrong</div>
        </div>""", unsafe_allow_html=True)

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
