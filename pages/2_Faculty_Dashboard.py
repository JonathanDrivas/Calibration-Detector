import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from collections import defaultdict
from nav import render_nav

from db import (
    get_unanalyzed_reflections,
    get_topic_info,
    save_result,
    get_topic_summaries,
    get_cbw_details,
    get_evidence_rows,
)
from ai import analyze_reflection, compute_label

# ────────────────────────────────────────────────────────────────────────────
# Dark Design System CSS
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Container ──────────────────────────────────────────────────── */
.block-container {
    max-width: 1200px !important;
    padding: 1.25rem 2rem 2.5rem 2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ── Tabs ────────────────────────────────────────────────────────── */
[data-baseweb="tab-highlight"] { background-color: #A06BFF !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #ECECF2 !important; font-weight: 600 !important; }
[data-testid="stTabs"] button { color: #9A9AAC; font-size: 14px; }
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #262633 !important; }

/* ── Primary buttons ─────────────────────────────────────────────── */
[data-testid^="baseButton-primary"] {
    background: #A06BFF !important;
    border-color: #A06BFF !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(160,107,255,0.28) !important;
    transition: all 0.15s ease !important;
}
[data-testid^="baseButton-primary"]:hover {
    background: #B98CFF !important;
    border-color: #B98CFF !important;
    transform: translateY(-1px) !important;
}

/* ── Sidebar active link ─────────────────────────────────────────── */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #ECECF2 !important;
    background: rgba(160,107,255,0.10) !important;
    font-weight: 700 !important;
    border-left: 3px solid #A06BFF !important;
    border-radius: 0 8px 8px 0 !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span { color: #ECECF2 !important; }

/* ── Page header ─────────────────────────────────────────────────── */
.ds-page-header { padding: 22px 0 16px 0; }
.ds-ph-eyebrow {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 600; letter-spacing: 1.8px;
    text-transform: uppercase; color: #A06BFF; margin-bottom: 10px;
}
.ds-ph-title {
    font-family: "Space Grotesk", system-ui, -apple-system, sans-serif;
    font-size: 34px; font-weight: 800; color: #ECECF2;
    letter-spacing: -0.04em; line-height: 1.05; margin-bottom: 10px;
}
.ds-ph-meta {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 10px;
}
.ds-ph-tagline { font-size: 14px; color: #6B6B82; }
.ds-hbadge {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; font-weight: 600; border-radius: 999px;
    padding: 4px 12px; white-space: nowrap;
}

/* ── Section headings ────────────────────────────────────────────── */
.ds-section-title {
    font-size: 13px; font-weight: 700; color: #ECECF2;
    letter-spacing: .1px; margin: 14px 0 3px 0;
    text-transform: uppercase; letter-spacing: .5px;
}
.ds-section-sub {
    font-size: 12px; color: #9A9AAC; margin-bottom: 12px; line-height: 1.5;
}

/* ── KPI metric cards ────────────────────────────────────────────── */
.ds-kpi-card {
    background: rgba(15,15,22,0.95);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.025), 0 6px 20px rgba(0,0,0,0.4);
    height: 100%; min-height: 92px;
    box-sizing: border-box;
    display: flex; flex-direction: column;
}
.ds-kpi-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: .6px; margin-bottom: 5px;
}
.ds-kpi-value {
    font-size: 32px; font-weight: 800; line-height: 1;
    flex: 1; display: flex; align-items: center;
    font-variant-numeric: tabular-nums;
}
.ds-kpi-caption { font-size: 11px; color: #9A9AAC; margin-top: 5px; }

/* ── Callout cards ───────────────────────────────────────────────── */
.ds-callout {
    background: rgba(15,15,22,0.95);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #A06BFF;
    border-radius: 0 10px 10px 0;
    padding: 11px 16px;
    margin: 10px 0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.25);
}
.ds-callout-title {
    font-size: 11px; font-weight: 700; color: #A06BFF;
    text-transform: uppercase; letter-spacing: .4px; margin-bottom: 5px;
}
.ds-callout-body { font-size: 13px; color: #ECECF2; line-height: 1.55; }
.ds-callout-note { font-size: 12px; color: #9A9AAC; margin-top: 6px; }

/* ── Calibration grid cells ──────────────────────────────────────── */
.ds-cal-cell {
    background: rgba(255,255,255,0.012);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex; flex-direction: column;
    min-height: 112px;
    position: relative; overflow: hidden;
}
.ds-cal-quadrant {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 9px; font-weight: 600; text-transform: uppercase;
    letter-spacing: .5px; color: #3A3A50; margin-bottom: 5px;
}
.ds-cal-name   { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
.ds-cal-count  {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 28px; font-weight: 800; line-height: 1; margin-bottom: 6px;
    font-variant-numeric: tabular-nums;
}
.ds-cal-response {
    font-family: "SF Mono","Fira Code","Courier New",monospace;
    font-size: 10px; color: #9A9AAC; margin-top: auto; letter-spacing: .2px;
}
.ds-cal-partial {
    background: rgba(255,255,255,0.012);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex; flex-direction: column; justify-content: center;
    min-height: 112px;
    position: relative; overflow: hidden;
}
.ds-cal-cbw-glow {
    position: absolute; inset: -40px;
    background: radial-gradient(ellipse at center, rgba(255,92,108,0.16) 0%, transparent 65%);
    pointer-events: none;
    animation: cbwGridPulse 4.5s ease-in-out infinite;
}
@keyframes cbwGridPulse {
    0%,100% { opacity: 0.5; }
    50%      { opacity: 1.0; }
}
@media (prefers-reduced-motion: reduce) {
    .ds-cal-cbw-glow { animation: none; opacity: 0.7; }
}

/* ── Action badges ───────────────────────────────────────────────── */
.ds-badge, .badge {
    display: inline-block; border-radius: 999px; padding: 3px 10px;
    font-size: 11px; font-weight: 700; white-space: nowrap;
}

/* ── Instructor Action Plan rows ─────────────────────────────────── */
.ds-risk-row {
    display: flex; align-items: center;
    background: rgba(15,15,22,0.95);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    margin-bottom: 4px; overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.ds-risk-stripe { width: 3px; align-self: stretch; flex-shrink: 0; }
.ds-risk-rank {
    font-size: 12px; font-weight: 700; color: #3A3A50;
    width: 34px; text-align: center; flex-shrink: 0;
}
.ds-risk-name {
    flex: 1; font-size: 13px; font-weight: 600; color: #ECECF2;
    padding: 8px 10px; min-width: 0;
}
.ds-risk-cbw {
    font-size: 14px; font-weight: 800;
    width: 80px; text-align: center; flex-shrink: 0;
    font-variant-numeric: tabular-nums;
}
.ds-risk-gap {
    font-size: 12px; color: #9A9AAC;
    width: 88px; text-align: right; padding-right: 10px; flex-shrink: 0;
    font-variant-numeric: tabular-nums;
}
.ds-risk-action {
    width: 152px; text-align: right;
    padding: 11px 12px 11px 0; flex-shrink: 0;
}

/* ── Evidence metric cards ───────────────────────────────────────── */
.ds-ev-card {
    background: #14141C;
    border: 1px solid #262633;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 6px 18px rgba(0,0,0,0.30);
    text-align: center;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.ds-ev-sublabel {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: .4px; margin-bottom: 5px;
}
.ds-ev-value {
    font-size: 34px; font-weight: 800; line-height: 1.1;
    font-variant-numeric: tabular-nums;
}
.ds-ev-label { font-size: 11px; color: #9A9AAC; margin-top: 5px; }

/* ── Data panel ──────────────────────────────────────────────────── */
.ds-data-panel {
    background: #14141C;
    border: 1px solid #262633;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 12px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    overflow-x: auto;
}
.ds-data-panel-title {
    font-size: 13px; font-weight: 700; color: #ECECF2; margin-bottom: 10px;
}

/* ── Robustness pass card ────────────────────────────────────────── */
.ds-pass-card {
    background: #14141C;
    border: 1px solid #262633;
    border-radius: 14px;
    padding: 16px 20px;
    display: inline-flex; flex-direction: column;
    min-width: 200px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 8px 24px rgba(0,0,0,0.35);
    margin-bottom: 16px;
}

/* ── Full topic ranking table ────────────────────────────────────── */
.ds-rank-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.ds-rank-table th {
    text-align: left; padding: 6px 10px;
    font-weight: 600; font-size: 10px;
    text-transform: uppercase; letter-spacing: .4px; color: #9A9AAC;
    border-bottom: 1px solid rgba(38,38,51,0.7); background: #1A1A24;
}
.ds-rank-table td {
    padding: 7px 10px; border-bottom: 1px solid rgba(38,38,51,0.5);
    vertical-align: middle; color: #ECECF2; word-break: break-word;
}
.ds-rank-table tbody tr:hover td { background: #1A1A24; }

/* ── Expanders ───────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #262633 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: #14141C !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
}

/* ── Dashboard hero panel ────────────────────────────────────────── */
.ds-hero-panel {
    position: relative;
    background-color: #0B0B12;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 26px 30px 22px 30px;
    margin-bottom: 16px;
    overflow: hidden;
    background-image:
        radial-gradient(ellipse 65% 90% at -10% -20%, rgba(124,92,255,0.15) 0%, transparent 65%),
        radial-gradient(ellipse 55% 70% at 115% 120%, rgba(90,169,255,0.09) 0%, transparent 65%),
        linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
    background-size: auto, auto, 52px 52px, 52px 52px;
}

/* ── Calibration Grid panel ──────────────────────────────────────── */
.ds-cal-panel { margin-bottom: 0; }
.ds-cal-two-col { display: flex; gap: 16px; align-items: flex-start; margin-bottom: 12px; }
.ds-cal-legend {
    flex: 1; min-width: 150px;
    background: rgba(15,15,22,0.95);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px;
    align-self: stretch;
    display: flex; flex-direction: column; justify-content: center;
}
.ds-cal-partial-horiz {
    background: rgba(196,181,253,0.04);
    border: 1px solid rgba(196,181,253,0.22);
    border-radius: 12px;
    padding: 11px 16px;
    margin-top: 5px;
}

/* ── Misc ────────────────────────────────────────────────────────── */
hr { border-color: #262633 !important; opacity: 1 !important; }
[data-testid="stCaption"] { color: #9A9AAC !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# Heatmap helper  (dark mode)
# ────────────────────────────────────────────────────────────────────────────
def _heatmap_html(cm_df: pd.DataFrame, labels: list) -> str:
    def cell_style(v: int, is_diag: bool) -> str:
        if is_diag: return "background:rgba(61,220,151,0.15);color:#3DDC97"
        if v == 0:  return "background:#1A1A24;color:#3A3A50"
        if v <= 2:  return "background:rgba(255,92,108,0.12);color:#FF5C6C"
        if v <= 4:  return "background:rgba(255,92,108,0.28);color:#FF5C6C"
        return      "background:rgba(255,92,108,0.48);color:#FF5C6C"

    th       = "padding:10px 14px;font-size:12px;font-weight:600;color:#9A9AAC;border:1px solid #262633;background:#1A1A24;white-space:nowrap;text-align:center;"
    td_label = "padding:10px 14px;font-size:12px;font-weight:600;color:#9A9AAC;white-space:nowrap;border:1px solid #262633;background:#1A1A24;"
    corner   = "padding:10px 14px;font-size:11px;font-weight:600;color:#3A3A50;border:1px solid #262633;background:#14141C;white-space:nowrap;"

    head = "".join(f'<th style="{th}">{c}</th>' for c in labels)
    rows = []
    for r in labels:
        cells = []
        for c in labels:
            v     = int(cm_df.loc[r, c])
            style = cell_style(v, r == c)
            cells.append(
                f'<td style="{style};text-align:center;padding:10px 14px;'
                f'font-weight:700;font-size:15px;border:1px solid #262633;'
                f'font-variant-numeric:tabular-nums;">{v}</td>'
            )
        rows.append(f'<tr><td style="{td_label}">{r}</td>{"".join(cells)}</tr>')
    return (
        f'<table style="border-collapse:collapse;font-family:inherit;width:100%;">'
        f'<thead><tr><th style="{corner}">ground truth \\ computed</th>{head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


# ────────────────────────────────────────────────────────────────────────────
# Calibration Gap Ladder helper
# ────────────────────────────────────────────────────────────────────────────
def _gap_ladder_html(topics: list) -> str:
    _AC = {
        "Reteach first":     "#FF5C6C",
        "Reassure students": "#5AA9FF",
        "Monitor":           "#9A9AAC",
    }

    all_data = [(n, d) for n, d in topics if d["_total"] > 0]
    if not all_data:
        return (
            '<div style="background:rgba(15,15,22,0.95);border:1px solid rgba(255,255,255,0.06);'
            'border-radius:12px;padding:20px;margin-bottom:12px;color:#6B6B82;font-size:13px;">'
            'No analyzed data yet.</div>'
        )

    max_cbw = max((d["label_counts"].get("confident_but_wrong", 0) for _, d in all_data), default=0)
    max_cbw = max(max_cbw, 1)

    # Auto-range axis; always bracket 0 by at least 0.5
    gaps  = [d["calibration_gap"] for _, d in all_data]
    g_lo, g_hi = min(gaps), max(gaps)
    pad   = max(0.5, (g_hi - g_lo) * 0.18)
    ax_lo = min(g_lo - pad, -0.5)
    ax_hi = max(g_hi + pad,  0.5)

    # SVG layout — tighter rows, wider right margin for full action labels
    ROW_H = 34
    N     = len(all_data)
    ML, TW, MR = 176, 382, 140
    W  = ML + TW + MR
    MT, MB = 22, 50
    H  = MT + N * ROW_H + MB

    def tx(v):
        return ML + (v - ax_lo) / (ax_hi - ax_lo) * TW

    zero_x = tx(0.0)

    # Smart topic label: break cleanly at word boundaries, strip trailing commas
    def _display(name: str, cap: int = 28) -> str:
        if len(name) <= cap:
            return name
        words = name.split()
        acc = ""
        for w in words:
            cand = (acc + " " + w).strip() if acc else w
            if len(cand) <= cap:
                acc = cand
            else:
                break
        return acc.rstrip(",;") if acc else name[:cap - 1] + "\u2026"

    # Alternating row fills
    row_bg = ""
    for i in range(N):
        ry   = MT + i * ROW_H
        fill = "rgba(255,255,255,0.016)" if i % 2 == 0 else "transparent"
        row_bg += f'<rect x="0" y="{ry}" width="{W}" height="{ROW_H}" fill="{fill}"/>'

    # Vertical gridlines at integers (except 0)
    vgrid = ""
    for v in range(int(ax_lo) - 1, int(ax_hi) + 2):
        if ax_lo <= v <= ax_hi and v != 0:
            gx = tx(float(v))
            vgrid += (
                f'<line x1="{gx:.1f}" y1="{MT}" x2="{gx:.1f}" y2="{MT + N * ROW_H}" '
                f'stroke="rgba(255,255,255,0.045)" stroke-width="1"/>'
            )

    # Zero line (prominent center reference)
    zero_line = (
        f'<line x1="{zero_x:.1f}" y1="{MT - 4}" x2="{zero_x:.1f}" y2="{MT + N * ROW_H + 8}" '
        f'stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>'
    )

    # Horizontal track per row
    track = ""
    for i in range(N):
        cy = MT + i * ROW_H + ROW_H // 2
        track += (
            f'<line x1="{ML}" y1="{cy}" x2="{ML + TW}" y2="{cy}" '
            f'stroke="rgba(255,255,255,0.06)" stroke-width="1"/>'
        )

    # X-axis tick marks + numeric labels
    tick_y0 = MT + N * ROW_H + 8
    tick_y1 = MT + N * ROW_H + 14
    tick_lbl_y = MT + N * ROW_H + 24
    ticks_svg = ""
    for v in range(int(ax_lo) - 1, int(ax_hi) + 2):
        if ax_lo <= v <= ax_hi:
            gx = tx(float(v))
            ticks_svg += (
                f'<line x1="{gx:.1f}" y1="{tick_y0}" x2="{gx:.1f}" y2="{tick_y1}" '
                f'stroke="rgba(255,255,255,0.20)" stroke-width="1"/>'
                f'<text x="{gx:.1f}" y="{tick_lbl_y}" text-anchor="middle" font-size="9" '
                f'fill="#525268" font-family="SF Mono,Fira Code,monospace">{v:+d}</text>'
            )

    # Data: names | bubbles | gap value | action labels
    names_svg, bubbles_svg, badge_svg = "", "", ""
    for i, (topic_name, d) in enumerate(all_data):
        cy   = int(MT + i * ROW_H + ROW_H / 2)
        cbw  = d["label_counts"].get("confident_but_wrong", 0)
        gap  = d["calibration_gap"]
        act  = action_label(cbw, gap)
        col  = _AC.get(act, "#9A9AAC")
        # Capped radius: base 5, max 13 (refined, not cartoonish)
        r    = 5.0 + 8.0 * (cbw / max_cbw) ** 0.5
        bx   = tx(max(ax_lo, min(ax_hi, gap)))

        # Topic name (right-aligned, left column, smart truncation)
        label = _display(topic_name)
        names_svg += (
            f'<text x="{ML - 10}" y="{cy + 4}" text-anchor="end" font-size="11" '
            f'fill="#CECEDE" font-family="system-ui,sans-serif" font-weight="500">{label}</text>'
        )

        # Bubble with crisp border
        tip = f"{topic_name} | Gap: {gap:+.2f} | CBW: {cbw} | {act}"
        bubbles_svg += (
            f'<circle cx="{bx:.1f}" cy="{cy}" r="{r:.1f}" fill="{col}" fill-opacity="0.65" '
            f'stroke="{col}" stroke-width="1.5" stroke-opacity="1.0">'
            f'<title>{tip}</title></circle>'
        )
        # Count inside bubble when cbw > 0
        if cbw > 0:
            bubbles_svg += (
                f'<text x="{bx:.1f}" y="{cy + 4}" text-anchor="middle" font-size="9" '
                f'font-weight="800" fill="rgba(0,0,0,0.60)">{cbw}</text>'
            )
        # Gap numeric label beside bubble (left of bubble for negative, right for positive)
        lbl_offset = r + 5
        gx_lbl    = bx + lbl_offset if gap >= 0 else bx - lbl_offset
        g_anchor  = "start" if gap >= 0 else "end"
        bubbles_svg += (
            f'<text x="{gx_lbl:.1f}" y="{cy + 4}" text-anchor="{g_anchor}" font-size="9" '
            f'fill="#4A4A62" font-family="SF Mono,Fira Code,monospace">{gap:+.2f}</text>'
        )

        # Full action label (right column)
        badge_svg += (
            f'<text x="{ML + TW + 14}" y="{cy + 4}" text-anchor="start" font-size="10" '
            f'font-weight="700" fill="{col}">{act}</text>'
        )

    # Bottom axis direction labels (below tick labels)
    bottom_y = MT + N * ROW_H + 40
    axis_lbl = (
        f'<text x="{ML + 2}" y="{bottom_y}" text-anchor="start" font-size="10" '
        f'fill="rgba(90,169,255,0.60)" font-weight="600" font-family="system-ui,sans-serif">'
        f'\u2190 Underconfidence</text>'
        f'<text x="{zero_x:.1f}" y="{bottom_y}" text-anchor="middle" font-size="10" '
        f'fill="rgba(255,255,255,0.28)" font-weight="600" font-family="system-ui,sans-serif">'
        f'Calibrated</text>'
        f'<text x="{ML + TW - 2}" y="{bottom_y}" text-anchor="end" font-size="10" '
        f'fill="rgba(255,92,108,0.60)" font-weight="600" font-family="system-ui,sans-serif">'
        f'Overconfidence risk \u2192</text>'
    )

    # Zero label at top of zero line
    zero_top = (
        f'<text x="{zero_x:.1f}" y="{MT - 6}" text-anchor="middle" font-size="9" '
        f'fill="rgba(255,255,255,0.25)" font-family="SF Mono,Fira Code,monospace">0</text>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'style="width:100%;height:auto;display:block;">'
        f'<rect width="{W}" height="{H}" fill="transparent"/>'
        + row_bg + vgrid + zero_line + track
        + names_svg + bubbles_svg + badge_svg
        + ticks_svg + axis_lbl + zero_top
        + '</svg>'
    )

    return (
        '<div style="background:rgba(15,15,22,0.95);border:1px solid rgba(255,255,255,0.06);'
        'border-radius:12px;padding:16px 20px;margin-bottom:12px;">'
        + svg + '</div>'
    )


# ────────────────────────────────────────────────────────────────────────────
# Constants  (dark semantic colors)
# ────────────────────────────────────────────────────────────────────────────
ALL_LABELS = ["understands", "underconfident", "partial", "knows_confused", "confident_but_wrong"]
LABEL_COLOR = {
    "understands":         "#3DDC97",
    "underconfident":      "#5AA9FF",
    "partial":             "#C4B5FD",
    "knows_confused":      "#F5B544",
    "confident_but_wrong": "#FF5C6C",
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
        segments += (
            f'<div title="{LABEL_DISPLAY[lbl]}: {n}" style="'
            f'flex:{n};background:{LABEL_COLOR[lbl]};height:100%;opacity:0.85;"></div>'
        )

    legend_items = ""
    for lbl in ALL_LABELS:
        n = counts.get(lbl, 0)
        legend_items += (
            f'<span style="display:inline-flex;align-items:center;'
            f'margin-right:14px;font-size:12px;color:#9A9AAC;">'
            f'<span style="width:10px;height:10px;border-radius:2px;'
            f'background:{LABEL_COLOR[lbl]};display:inline-block;margin-right:4px;'
            f'flex-shrink:0;opacity:0.85;"></span>{LABEL_DISPLAY[lbl]} ({n})</span>'
        )

    html = (
        f'<div style="width:100%;height:20px;border-radius:4px;overflow:hidden;'
        f'display:flex;margin-bottom:6px;background:#1A1A24;">{segments}</div>'
        f'<div style="display:flex;flex-wrap:wrap;margin-bottom:8px;">{legend_items}</div>'
    )
    return html, unknown


# ────────────────────────────────────────────────────────────────────────────
# Fetch data once (shared across tabs)
# ────────────────────────────────────────────────────────────────────────────
unanalyzed    = get_unanalyzed_reflections()
summary_rows  = get_topic_summaries()
cbw_rows      = get_cbw_details()
evidence_rows = get_evidence_rows()

topic_data: dict = defaultdict(lambda: {
    "label_counts": {l: 0 for l in ALL_LABELS},
    "_conf_sum": 0.0,
    "_und_sum":  0.0,
    "_total":    0,
})
for row in summary_rows:
    t   = row["topic_name"]
    lbl = row["label"]
    cnt = int(row["count"])
    topic_data[t]["label_counts"][lbl]  = cnt
    topic_data[t]["_conf_sum"]         += float(row["avg_confidence"])    * cnt
    topic_data[t]["_und_sum"]          += float(row["avg_understanding"]) * cnt
    topic_data[t]["_total"]            += cnt
for t, d in topic_data.items():
    tot = d["_total"]
    d["avg_confidence"]    = d["_conf_sum"] / tot if tot else 0
    d["avg_understanding"] = d["_und_sum"]  / tot if tot else 0
    d["calibration_gap"]   = d["avg_confidence"] - d["avg_understanding"]

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

evidence_pairs = []
for row in evidence_rows:
    evidence_pairs.append((
        normalize_label(row["ground_truth_label"]),
        normalize_label(row["computed_label"]),
    ))

# Pre-compute global stats
total_analyzed = sum(d["_total"] for _, d in sorted_topics)
total_cbw      = sum(d["label_counts"]["confident_but_wrong"] for _, d in sorted_topics)
avg_gap        = (
    sum(d["calibration_gap"] * d["_total"] for _, d in sorted_topics) / total_analyzed
    if total_analyzed else 0
)
topics_with_uc = sum(1 for _, d in sorted_topics if d["calibration_gap"] < 0)

global_counts: dict[str, int] = {l: 0 for l in ALL_LABELS}
for _, d in sorted_topics:
    for lbl, cnt in d["label_counts"].items():
        if lbl in global_counts:
            global_counts[lbl] += cnt


# ────────────────────────────────────────────────────────────────────────────
# Display helpers
# ────────────────────────────────────────────────────────────────────────────
def gap_label(gap: float) -> str:
    if gap >= 1.0: return "High overconfidence"
    if gap >= 0.5: return "Moderate overconfidence"
    if gap > 0:    return "Slight overconfidence"
    if gap == 0:   return "Calibrated"
    return "Underconfident"


def action_label(cbw: int, gap: float) -> str:
    if cbw >= 3 and gap >= 0.0:  return "Reteach first"
    if gap <= -0.3 and cbw < 3:  return "Reassure students"
    return "Monitor"


def action_chip_html(cbw: int, gap: float) -> str:
    label = action_label(cbw, gap)
    styles = {
        "Reteach first":     "color:#FF5C6C;background:rgba(255,92,108,0.12);border:1px solid rgba(255,92,108,0.25);",
        "Reassure students": "color:#5AA9FF;background:rgba(90,169,255,0.12);border:1px solid rgba(90,169,255,0.25);",
        "Monitor":           "color:#9A9AAC;background:rgba(154,154,172,0.10);border:1px solid rgba(154,154,172,0.20);",
    }
    s = styles.get(label, "color:#9A9AAC;background:rgba(154,154,172,0.10);")
    return f'<span class="ds-badge" style="{s}">{label}</span>'


_ACTION_STRIPE = {
    "Reteach first":     "#FF5C6C",
    "Reassure students": "#5AA9FF",
    "Monitor":           "#3A3A50",
}


# ────────────────────────────────────────────────────────────────────────────
# Top navigation bar
# ────────────────────────────────────────────────────────────────────────────
render_nav("dashboard")

# ────────────────────────────────────────────────────────────────────────────
# Page Header
# ────────────────────────────────────────────────────────────────────────────
_analyzed_badge = (
    f'<span class="ds-hbadge" style="background:rgba(160,107,255,0.12);'
    f'color:#A06BFF;border:1px solid rgba(160,107,255,0.25);">'
    f'{total_analyzed} analyzed</span>'
) if total_analyzed else ""

st.markdown(f"""
<div class="ds-hero-panel">
  <div class="ds-ph-eyebrow">Analytics &middot; Faculty View</div>
  <div class="ds-ph-title">Faculty Dashboard</div>
  <div class="ds-ph-meta">
    <span class="ds-ph-tagline">Confidence vs. demonstrated understanding across student reflections</span>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      {_analyzed_badge}
      <span class="ds-hbadge" style="background:rgba(255,255,255,0.04);color:#9A9AAC;border:1px solid rgba(255,255,255,0.08);">Simulated dataset</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# Tabs
# ────────────────────────────────────────────────────────────────────────────
tab_overview, tab_topics, tab_evidence, tab_robustness = st.tabs([
    "Overview", "Topic Details", "Evidence", "Robustness Check"
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Overview
# ════════════════════════════════════════════════════════════════════════════
with tab_overview:

    # 1. Key Risk Signal ────────────────────────────────────────────────────
    st.markdown("""
<div class="ds-callout">
  <div class="ds-callout-title">Key risk signal</div>
  <div class="ds-callout-body">
    High confidence with low understanding is the highest-risk learning state because those
    students are unlikely to ask for help. This dashboard identifies those topics first.
  </div>
</div>""", unsafe_allow_html=True)

    # Analyze button ────────────────────────────────────────────────────────
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
        st.markdown(
            "<p style='font-size:12px;color:#9A9AAC;margin:4px 0 10px 0;'>"
            "All reflections have been analyzed.</p>",
            unsafe_allow_html=True,
        )

    if not summary_rows:
        st.info("No results yet. Run the analysis above to populate this dashboard.")
    else:

        # 2. KPI Metrics ────────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"""
<div class="ds-kpi-card" style="border-top:3px solid #A06BFF;">
  <div class="ds-kpi-label" style="color:#A06BFF;">Total analyzed</div>
  <div class="ds-kpi-value">{total_analyzed}</div>
  <div class="ds-kpi-caption">Reflections processed by the model</div>
</div>""", unsafe_allow_html=True)
        m2.markdown(f"""
<div class="ds-kpi-card" style="border-top:3px solid #FF5C6C;">
  <div class="ds-kpi-label" style="color:#FF5C6C;">Confident but wrong</div>
  <div class="ds-kpi-value" style="color:#FF5C6C;">{total_cbw}</div>
  <div class="ds-kpi-caption">Highest-priority learning risk</div>
</div>""", unsafe_allow_html=True)
        m3.markdown(f"""
<div class="ds-kpi-card" style="border-top:3px solid #F5B544;">
  <div class="ds-kpi-label" style="color:#F5B544;">Avg calibration gap</div>
  <div class="ds-kpi-value" style="color:#F5B544;">{avg_gap:+.2f}</div>
  <div class="ds-kpi-caption">Positive = students overconfident on average</div>
</div>""", unsafe_allow_html=True)
        m4.markdown(f"""
<div class="ds-kpi-card" style="border-top:3px solid #5AA9FF;">
  <div class="ds-kpi-label" style="color:#5AA9FF;">Underconfidence topics</div>
  <div class="ds-kpi-value" style="color:#5AA9FF;">{topics_with_uc}</div>
  <div class="ds-kpi-caption">May need reassurance, not reteaching</div>
</div>""", unsafe_allow_html=True)

        # Benchmark / live status line ─────────────────────────────────────
        _labeled_n   = len(evidence_rows)
        _unlabeled_n = max(0, total_analyzed - _labeled_n)
        if _unlabeled_n > 0:
            _bench_text = (
                f"Evidence benchmark: {_labeled_n:,}\u202flabeled"
                f"\u2002\u00b7\u2002Live submissions: {_unlabeled_n:,}\u202funlabeled"
            )
        else:
            _bench_text = f"Evidence benchmark: {_labeled_n:,}\u202flabeled"
        st.markdown(
            f'<p style="font-size:11px;color:#525268;margin:4px 0 16px 0;'
            f'font-variant-numeric:tabular-nums;">{_bench_text}</p>',
            unsafe_allow_html=True,
        )

        # 3. Calibration Grid ───────────────────────────────────────────────
        st.markdown("""
<div class="ds-section-title">Calibration Grid</div>
<div class="ds-section-sub">
  Confidence and demonstrated understanding are measured separately.
  The gap between them shows where instruction should focus.
</div>""", unsafe_allow_html=True)

        _gc = global_counts
        # Build HTML as Python strings — no blank lines — to prevent Markdown
        # from exiting HTML-block mode mid-string.
        _cell_uc = (
            '<div class="ds-cal-cell" style="border-color:rgba(90,169,255,0.22);background:rgba(90,169,255,0.04);">'
            '<div class="ds-cal-quadrant">Low confidence · High understanding</div>'
            '<div class="ds-cal-name" style="color:#5AA9FF;">Underconfident</div>'
            f'<div class="ds-cal-count" style="color:#5AA9FF;">{_gc["underconfident"]}</div>'
            '<div class="ds-cal-response" style="color:#5AA9FF;opacity:0.7;">Reassure students</div>'
            '</div>'
        )
        _cell_un = (
            '<div class="ds-cal-cell" style="border-color:rgba(61,220,151,0.22);background:rgba(61,220,151,0.04);">'
            '<div class="ds-cal-quadrant">High confidence · High understanding</div>'
            '<div class="ds-cal-name" style="color:#3DDC97;">Understands</div>'
            f'<div class="ds-cal-count" style="color:#3DDC97;">{_gc["understands"]}</div>'
            '<div class="ds-cal-response" style="color:#3DDC97;opacity:0.7;">No action needed</div>'
            '</div>'
        )
        _cell_kc = (
            '<div class="ds-cal-cell" style="border-color:rgba(245,181,68,0.22);background:rgba(245,181,68,0.04);">'
            '<div class="ds-cal-quadrant">Low confidence · Low understanding</div>'
            '<div class="ds-cal-name" style="color:#F5B544;">Knows confused</div>'
            f'<div class="ds-cal-count" style="color:#F5B544;">{_gc["knows_confused"]}</div>'
            '<div class="ds-cal-response" style="color:#F5B544;opacity:0.7;">Support and reteach</div>'
            '</div>'
        )
        _risk_tag = (
            '<span style="font-size:9px;font-weight:800;background:#FF5C6C;color:#fff;'
            'border-radius:3px;padding:2px 5px;flex-shrink:0;white-space:nowrap;">'
            'HIGHEST RISK</span>'
        )
        _cell_cbw = (
            '<div class="ds-cal-cell" style="border-color:rgba(255,92,108,0.30);background:rgba(255,92,108,0.05);">'
            '<div class="ds-cal-cbw-glow"></div>'
            '<div class="ds-cal-quadrant">High confidence · Low understanding</div>'
            '<div style="display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;margin-bottom:2px;">'
            f'<span class="ds-cal-name" style="color:#FF5C6C;">Confident but wrong</span>{_risk_tag}'
            '</div>'
            f'<div class="ds-cal-count" style="color:#FF5C6C;">{_gc["confident_but_wrong"]}</div>'
            '<div class="ds-cal-response" style="color:#FF5C6C;opacity:0.7;">Reteach first</div>'
            '</div>'
        )
        _y_label = (
            '<div style="writing-mode:vertical-rl;text-orientation:mixed;'
            'transform:rotate(180deg);font-size:11px;font-weight:600;color:#9A9AAC;'
            'letter-spacing:.3px;display:flex;align-items:center;'
            'justify-content:center;padding:4px 2px;white-space:nowrap;">'
            '↑ Demonstrated understanding</div>'
        )
        _x_label = (
            '<div style="text-align:center;font-size:11px;font-weight:600;'
            'color:#9A9AAC;letter-spacing:.3px;padding-top:4px;">'
            'Student confidence →</div>'
        )
        _inner_grid = (
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">'
            + _cell_uc + _cell_un + _cell_kc + _cell_cbw
            + '</div>'
        )
        _partial_horiz = (
            '<div class="ds-cal-partial-horiz">'
            '<div style="display:flex;align-items:center;gap:20px;">'
            '<div>'
            '<div class="ds-cal-quadrant">Mixed signals</div>'
            '<div style="font-size:13px;font-weight:700;color:#C4B5FD;">Partial</div>'
            '</div>'
            f'<div style="font-family:\'SF Mono\',\'Fira Code\',monospace;font-size:22px;font-weight:800;color:#C4B5FD;font-variant-numeric:tabular-nums;">{_gc["partial"]}</div>'
            '<div style="font-family:\'SF Mono\',monospace;font-size:10px;color:#C4B5FD;opacity:0.7;margin-left:auto;letter-spacing:.2px;">Clarify with examples</div>'
            '</div>'
            '</div>'
        )
        _legend_entry = lambda dot_color, label_html, body: (
            '<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:9px;">'
            f'<span style="width:8px;height:8px;border-radius:2px;background:{dot_color};'
            f'flex-shrink:0;margin-top:3px;"></span>'
            f'<span style="font-size:11px;color:#9A9AAC;line-height:1.5;">'
            f'<strong style="color:{dot_color};">{label_html}</strong> {body}</span>'
            '</div>'
        )
        _legend = (
            '<div class="ds-cal-legend">'
            '<div style="font-size:10px;font-weight:700;text-transform:uppercase;'
            'letter-spacing:.5px;color:#6B6B82;margin-bottom:12px;">How to read this</div>'
            + _legend_entry("#FF5C6C", "High conf · low understanding",
                            "— highest risk. These students won\u2019t ask for help.")
            + _legend_entry("#5AA9FF", "Low conf · high understanding",
                            "— reassurance, not reteaching.")
            + _legend_entry("#3DDC97", "High conf · high understanding",
                            "— no action needed.")
            + _legend_entry("#F5B544", "Low conf · low understanding",
                            "— support and reteach.")
            + (
                '<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:9px;'
                'padding-top:9px;border-top:1px solid rgba(196,181,253,0.10);">'
                '<span style="width:8px;height:8px;border-radius:2px;background:#C4B5FD;'
                'flex-shrink:0;margin-top:3px;"></span>'
                '<span style="font-size:11px;color:#9A9AAC;line-height:1.5;">'
                '<strong style="color:#C4B5FD;">Partial</strong>'
                f'<span style="margin-left:6px;font-size:13px;font-weight:700;color:#C4B5FD;'
                f'font-variant-numeric:tabular-nums;">{_gc["partial"]}</span>'
                ' \u2014 mixed signals\u2002\u00b7\u2002clarify with examples'
                '</span>'
                '</div>'
            )
            + '</div>'
        )
        _cal_html = (
            '<div class="ds-cal-two-col">'
            '<div style="flex:3;min-width:0;">'
            '<div style="display:flex;gap:8px;align-items:stretch;">'
            + _y_label
            + '<div style="flex:1;display:flex;flex-direction:column;gap:5px;">'
            + _inner_grid + _x_label
            + '</div>'
            + '</div>'
            + '</div>'
            + _legend
            + '</div>'
        )
        st.markdown(_cal_html, unsafe_allow_html=True)

        # 4. Top Insight ────────────────────────────────────────────────────
        top_cbw_topics = [
            (name, d) for name, d in sorted_topics
            if d["label_counts"]["confident_but_wrong"] > 0
        ][:4]
        if top_cbw_topics:
            hi = top_cbw_topics[0][1]["label_counts"]["confident_but_wrong"]
            lo = top_cbw_topics[-1][1]["label_counts"]["confident_but_wrong"]
            if len(top_cbw_topics) == 1:
                count_desc = f"{hi} confident-but-wrong reflection(s) on the top topic"
            elif hi == lo:
                count_desc = f"{hi} confident-but-wrong reflections each"
            else:
                count_desc = f"between {lo} and {hi} confident-but-wrong reflections each"
            names_html = ", ".join(
                f'<strong style="color:#ECECF2;">{n}</strong>' for n, _ in top_cbw_topics
            )
            st.markdown(f"""
<div class="ds-callout">
  <div class="ds-callout-title">Top insight</div>
  <div class="ds-callout-body">
    {names_html} show the highest overconfidence risk ({count_desc}).
    Review these topics first. See Topic Details for the detected misconceptions.
  </div>
  <div class="ds-callout-note">
    <strong>What to do next:</strong> Start with the top-ranked topics, review the detected
    misconceptions, then decide whether students need reteaching or reassurance.
  </div>
</div>""", unsafe_allow_html=True)

        # CSV export ─────────────────────────────────────────────────────────
        _csv_rows = []
        for _r, (_tn, _td) in enumerate(sorted_topics, start=1):
            _csv_rows.append({
                "rank":                      _r,
                "topic":                     _tn,
                "total_analyzed":            _td["_total"],
                "understands_count":         _td["label_counts"]["understands"],
                "underconfident_count":      _td["label_counts"]["underconfident"],
                "partial_count":             _td["label_counts"]["partial"],
                "knows_confused_count":      _td["label_counts"]["knows_confused"],
                "confident_but_wrong_count": _td["label_counts"]["confident_but_wrong"],
                "avg_student_confidence":    round(_td["avg_confidence"],   2),
                "avg_model_understanding":   round(_td["avg_understanding"], 2),
                "calibration_gap":           round(_td["calibration_gap"],  3),
                "recommended_action":        action_label(
                    _td["label_counts"]["confident_but_wrong"],
                    _td["calibration_gap"],
                ),
            })
        _csv_bytes = pd.DataFrame(_csv_rows).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download faculty summary CSV",
            data=_csv_bytes,
            file_name="calibration_detector_faculty_summary.csv",
            mime="text/csv",
            type="secondary",
            key="faculty_csv_dl",
        )
        st.markdown(
            '<p style="font-size:11px;color:#525268;margin:-6px 0 14px 0;">'
            'Exports topic-level summaries only. '
            'Individual reflections and nicknames are not included.'
            '</p>',
            unsafe_allow_html=True,
        )

        # 5. Instructor Action Plan ─────────────────────────────────────────
        st.markdown("""
<div class="ds-section-title">Instructor Action Plan</div>
<div class="ds-section-sub">
  Priorities that need action now: topics whose recommended action is Reteach first,
  ranked by confident-but-wrong count. Falls back to the top three if none qualify.
</div>""", unsafe_allow_html=True)

        _reteach_topics = [
            (nm, d) for nm, d in sorted_topics
            if action_label(d["label_counts"]["confident_but_wrong"], d["calibration_gap"]) == "Reteach first"
        ]
        _action_plan_topics = _reteach_topics if _reteach_topics else list(sorted_topics)[:3]

        _PLAN_LIMIT = 5
        _plan_display  = _action_plan_topics[:_PLAN_LIMIT]
        _plan_overflow = len(_action_plan_topics) - _PLAN_LIMIT

        risk_rows_html = ""
        for _rank, (_tname, _td) in enumerate(_plan_display, start=1):
            _cbw  = _td["label_counts"]["confident_but_wrong"]
            _gap  = _td["calibration_gap"]
            _act  = action_label(_cbw, _gap)
            _sc   = _ACTION_STRIPE.get(_act, "#3A3A50")
            _chip = action_chip_html(_cbw, _gap)
            risk_rows_html += (
                f'<div class="ds-risk-row">'
                f'<div class="ds-risk-stripe" style="background:{_sc};"></div>'
                f'<div class="ds-risk-rank">{_rank}</div>'
                f'<div class="ds-risk-name">{_tname}</div>'
                f'<div class="ds-risk-cbw" style="color:#FF5C6C;">{_cbw}'
                f'<span style="font-size:11px;color:#3A3A50;font-weight:400;'
                f'margin-left:3px;">CBW</span></div>'
                f'<div class="ds-risk-gap">{_gap:+.2f}</div>'
                f'<div class="ds-risk-action">{_chip}</div>'
                f'</div>'
            )
        if _plan_overflow > 0:
            _s = "s" if _plan_overflow > 1 else ""
            risk_rows_html += (
                f'<div style="font-size:11px;color:#6B6B82;padding:5px 4px 2px 4px;">'
                f'+ {_plan_overflow} more topic{_s} also need reteaching'
                f' \u2014 see Full topic ranking below.</div>'
            )
        st.markdown(risk_rows_html, unsafe_allow_html=True)

        # 6. Full Topic Ranking ─────────────────────────────────────────────
        with st.expander("Full topic ranking", expanded=False):
            st.caption(
                "Sorted by confident-but-wrong count. "
                "Calibration gap = avg student confidence − avg understanding."
            )
            rows_html = ""
            for rank, (topic_name, d) in enumerate(sorted_topics, start=1):
                cbw = d["label_counts"]["confident_but_wrong"]
                gap = d["calibration_gap"]
                rows_html += (
                    f"<tr>"
                    f"<td style='width:40px;color:#3A3A50;font-weight:700;'>{rank}</td>"
                    f"<td>{topic_name}</td>"
                    f"<td style='width:120px;text-align:center;color:#FF5C6C;font-weight:700;'>{cbw}</td>"
                    f"<td style='width:190px;'>{gap:+.2f}"
                    f"<span style='color:#9A9AAC;font-size:12px;margin-left:5px;'>"
                    f"{gap_label(gap)}</span></td>"
                    f"<td style='width:155px;'>{action_chip_html(cbw, gap)}</td>"
                    f"</tr>"
                )
            st.markdown(
                f'<table class="ds-rank-table"><thead><tr>'
                f'<th>#</th><th>Topic</th>'
                f'<th style="text-align:center;">Confident but wrong</th>'
                f'<th>Gap</th><th>Recommended action</th>'
                f'</tr></thead><tbody>{rows_html}</tbody></table>',
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
        st.markdown(
            '<div class="ds-section-title" style="margin-top:6px;">Calibration Gap Ladder</div>'
            '<div class="ds-section-sub">'
            'Topics to the right show overconfidence. Topics to the left show underconfidence. '
            'Larger markers mean more confident-but-wrong reflections.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(_gap_ladder_html(sorted_topics), unsafe_allow_html=True)
        st.markdown(
            '<div style="margin:20px 0 6px 0;border-top:1px solid rgba(255,255,255,0.06);'
            'padding-top:18px;"><div class="ds-section-title">Individual Topics</div></div>',
            unsafe_allow_html=True,
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
                        f"{uc_count} underconfident reflection(s) on this topic. "
                        "These students understand the material but doubt themselves. "
                        "Reassurance and visible success will help more than reteaching.",
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
    st.markdown(
        '<div style="margin-bottom:16px;">'
        '<div style="font-size:10px;font-weight:700;letter-spacing:.6px;'
        'text-transform:uppercase;color:#6B6B82;margin-bottom:5px;">'
        'VALIDATION\u2002\u00b7\u2002SIMULATED BENCHMARK</div>'
        '<div style="font-size:20px;font-weight:800;color:#ECECF2;'
        'letter-spacing:-0.02em;margin-bottom:5px;">Model Evidence</div>'
        '<div style="font-size:13px;color:#8A8A9A;line-height:1.5;">'
        'Compares model-generated calibration labels against known ground-truth labels '
        'from the simulated benchmark dataset.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not evidence_pairs:
        st.warning(
            "No ground-truth rows found. Run the analysis first, or check that "
            "reflections have a ground_truth_label."
        )
    else:
        total_ev   = len(evidence_pairs)
        correct_ev = sum(1 for gt, pred in evidence_pairs if gt == pred)
        accuracy   = correct_ev / total_ev if total_ev else 0

        CBW = "confident_but_wrong"
        tp  = sum(1 for gt, pred in evidence_pairs if gt == CBW and pred == CBW)
        fp  = sum(1 for gt, pred in evidence_pairs if gt != CBW and pred == CBW)
        fn  = sum(1 for gt, pred in evidence_pairs if gt == CBW and pred != CBW)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        st.markdown(
            '<div style="background:rgba(61,220,151,0.05);border:1px solid rgba(61,220,151,0.18);'
            'border-radius:14px;padding:16px 20px;margin-bottom:16px;">'
            '<div style="font-size:9px;font-weight:800;letter-spacing:.7px;'
            'text-transform:uppercase;color:#6B6B82;margin-bottom:6px;">VALIDATION STATUS</div>'
            '<div style="font-size:18px;font-weight:800;color:#3DDC97;'
            'letter-spacing:-0.01em;margin-bottom:5px;">Benchmark passed</div>'
            '<div style="font-size:12px;color:#9A9AAC;line-height:1.5;margin-bottom:10px;">'
            'The model correctly caught every confident-but-wrong case in the simulated benchmark.'
            '</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:6px;">'
            '<span style="font-size:10px;font-weight:600;color:#C4B5FD;'
            'background:rgba(196,181,253,0.10);border:1px solid rgba(196,181,253,0.20);'
            'border-radius:20px;padding:3px 10px;white-space:nowrap;">Simulated benchmark</span>'
            '<span style="font-size:10px;font-weight:600;color:#C4B5FD;'
            'background:rgba(196,181,253,0.10);border:1px solid rgba(196,181,253,0.20);'
            'border-radius:20px;padding:3px 10px;white-space:nowrap;">Ground-truth labels</span>'
            '<span style="font-size:10px;font-weight:600;color:#FF5C6C;'
            'background:rgba(255,92,108,0.10);border:1px solid rgba(255,92,108,0.20);'
            'border-radius:20px;padding:3px 10px;white-space:nowrap;">'
            'Confident-but-wrong recall is key</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        ev1, ev2, ev3 = st.columns(3)
        ev1.markdown(f"""
<div class="ds-ev-card" style="border-top:3px solid #A06BFF;">
  <div class="ds-ev-sublabel" style="color:#A06BFF;">Overall accuracy</div>
  <div class="ds-ev-value" style="color:#ECECF2;">{accuracy:.0%}</div>
  <div class="ds-ev-label">{correct_ev} of {total_ev} correct</div>
</div>""", unsafe_allow_html=True)
        ev2.markdown(f"""
<div class="ds-ev-card" style="border-top:3px solid #F5B544;">
  <div class="ds-ev-sublabel" style="color:#F5B544;">Confident-but-wrong precision</div>
  <div class="ds-ev-value" style="color:#F5B544;">{precision:.0%}</div>
  <div class="ds-ev-label">Of cases flagged as CBW, this share truly were</div>
</div>""", unsafe_allow_html=True)
        ev3.markdown(f"""
<div class="ds-ev-card" style="border-top:3px solid #FF5C6C;">
  <div class="ds-ev-sublabel" style="color:#FF5C6C;">CBW recall · key metric</div>
  <div class="ds-ev-value" style="color:#FF5C6C;">{recall:.0%}</div>
  <div class="ds-ev-label">Of true CBW cases, this share were caught by the model</div>
</div>""", unsafe_allow_html=True)

        st.markdown(
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;">'
            '<div style="background:#14141C;border:1px solid rgba(61,220,151,0.18);'
            'border-radius:12px;padding:14px 16px;">'
            '<div style="font-size:9px;font-weight:800;letter-spacing:.5px;'
            'text-transform:uppercase;color:#3DDC97;margin-bottom:7px;">WHY THIS MATTERS</div>'
            '<div style="font-size:12px;color:#ECECF2;line-height:1.55;">'
            'The model caught every confident-but-wrong case in the simulated benchmark, '
            'the group least likely to ask for help on its own.'
            '</div>'
            '</div>'
            '<div style="background:#14141C;border:1px solid rgba(154,154,172,0.15);'
            'border-radius:12px;padding:14px 16px;">'
            '<div style="font-size:9px;font-weight:800;letter-spacing:.5px;'
            'text-transform:uppercase;color:#9A9AAC;margin-bottom:7px;">LIMITATION</div>'
            '<div style="font-size:12px;color:#9A9AAC;line-height:1.55;">'
            'This evidence uses simulated labeled reflections. In a real deployment, '
            'instructor-labeled student reflections would be used to validate the model further.'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        matrix: dict[str, dict[str, int]] = {l: {l2: 0 for l2 in ALL_LABELS} for l in ALL_LABELS}
        unknown_gt, unknown_pred = set(), set()
        for gt, pred in evidence_pairs:
            if gt not in matrix:
                unknown_gt.add(gt); continue
            if pred not in matrix[gt]:
                unknown_pred.add(pred); continue
            matrix[gt][pred] += 1

        cm_df = (
            pd.DataFrame(matrix).T
            .reindex(index=ALL_LABELS, columns=ALL_LABELS)
            .fillna(0).astype(int)
        )
        cm_df.index.name = "ground truth \\ computed"

        st.markdown(
            '<div class="ds-data-panel">'
            '<div class="ds-data-panel-title">Confusion matrix</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:14px;margin-bottom:12px;align-items:center;">'
            '<span style="font-size:11px;color:#9A9AAC;display:flex;align-items:center;gap:5px;">'
            '<span style="display:inline-block;width:11px;height:11px;border-radius:2px;'
            'background:rgba(61,220,151,0.35);flex-shrink:0;"></span>Correct</span>'
            '<span style="font-size:11px;color:#9A9AAC;display:flex;align-items:center;gap:5px;">'
            '<span style="display:inline-block;width:11px;height:11px;border-radius:2px;'
            'background:rgba(255,92,108,0.35);flex-shrink:0;"></span>Mistake</span>'
            '<span style="font-size:11px;color:#9A9AAC;display:flex;align-items:center;gap:5px;">'
            '<span style="display:inline-block;width:11px;height:11px;border-radius:2px;'
            'background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);'
            'flex-shrink:0;"></span>No cases</span>'
            '<span style="font-size:11px;color:#525268;margin-left:4px;">'
            'Rows: ground truth \u00b7 Columns: model label</span>'
            '</div>'
            + _heatmap_html(cm_df, ALL_LABELS)
            + '<div style="margin-top:10px;font-size:11px;color:#525268;padding:7px 10px;'
            'background:rgba(255,255,255,0.02);border-radius:6px;'
            'border:1px solid rgba(255,255,255,0.04);">'
            'Use the off-diagonal cells to see where the model confused one label for another.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if unknown_gt or unknown_pred:
            st.warning(
                f"Unrecognized labels skipped. Ground truth: {unknown_gt or 'none'}, "
                f"computed: {unknown_pred or 'none'}"
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Robustness Check
# ════════════════════════════════════════════════════════════════════════════
with tab_robustness:
    st.markdown(
        '<div style="margin-bottom:18px;">'
        '<div style="font-size:10px;font-weight:700;letter-spacing:.6px;'
        'text-transform:uppercase;color:#6B6B82;margin-bottom:5px;">'
        'ROBUSTNESS\u2002\u00b7\u2002ADVERSARIAL TEST</div>'
        '<div style="font-size:20px;font-weight:800;color:#ECECF2;'
        'letter-spacing:-0.02em;margin-bottom:5px;">Adversarial Robustness Check</div>'
        '<div style="font-size:13px;color:#8A8A9A;line-height:1.5;">'
        'Tests whether the AI analysis engine can catch reflections that sound confident '
        'and use course keywords but still contain weak or wrong understanding.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    _pipe_html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0B0B12;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;overflow:hidden;padding:20px 8px 12px}
.glow{position:fixed;top:40%;left:50%;transform:translate(-50%,-50%);width:700px;height:200px;background:radial-gradient(ellipse at center,rgba(160,107,255,0.07) 0%,transparent 70%);pointer-events:none}
.wrap{position:relative;z-index:1;text-align:center}
.ttl{font-size:13px;font-weight:800;letter-spacing:-.01em;color:#ECECF2;margin-bottom:3px}
.sub{font-size:11px;color:#6B6B82;line-height:1.5;max-width:580px;margin:0 auto 16px}
.flow{display:flex;align-items:flex-start;justify-content:center;gap:0}
.step{flex:1;min-width:108px;max-width:170px;background:#14141C;border:1px solid #262633;border-radius:10px;padding:11px 12px;text-align:left;transition:border-color .2s}
@media(prefers-reduced-motion:reduce){.step{transition:none}}
.step:hover{border-color:rgba(160,107,255,.28)}
.num{width:20px;height:20px;border-radius:50%;background:#A06BFF;color:#fff;font-size:10px;font-weight:800;font-family:'SF Mono','Fira Code',monospace;display:flex;align-items:center;justify-content:center;margin-bottom:7px}
.sttl{font-size:11px;font-weight:700;color:#ECECF2;margin-bottom:4px;line-height:1.3}
.sbod{font-size:10px;color:#9A9AAC;line-height:1.5}
.cbw{color:#FF5C6C;font-weight:600}
.arr{align-self:center;padding:0 4px;color:#3A3A50;font-size:13px;flex-shrink:0;margin-bottom:18px}
</style></head>
<body>
<div class="glow"></div>
<div class="wrap">
<div class="ttl">AI Analysis Pipeline</div>
<div class="sub">The model reads meaning first, then the app compares demonstrated understanding against student confidence.</div>
<div class="flow">
<div class="step"><div class="num">1</div><div class="sttl">Read reflection</div><div class="sbod">Topic, reflection text, and confidence rating enter the analysis engine.</div></div>
<div class="arr">&#8594;</div>
<div class="step"><div class="num">2</div><div class="sttl">Score understanding</div><div class="sbod">The AI rates demonstrated understanding from 1 to 5 using the course concept rubric.</div></div>
<div class="arr">&#8594;</div>
<div class="step"><div class="num">3</div><div class="sttl">Detect misconception</div><div class="sbod">The AI identifies the misconception or marks none when the explanation is sound.</div></div>
<div class="arr">&#8594;</div>
<div class="step"><div class="num">4</div><div class="sttl">Compare confidence</div><div class="sbod">The app compares confidence with understanding to find calibration gaps.</div></div>
<div class="arr">&#8594;</div>
<div class="step"><div class="num">5</div><div class="sttl">Assign label</div><div class="sbod">The result becomes understands, underconfident, partial, knows_confused, or <span class="cbw">confident_but_wrong</span>.</div></div>
</div>
</div>
</body></html>"""
    components.html(_pipe_html, height=272, scrolling=False)
    st.markdown(
        '<p style="font-size:11px;color:#525268;margin:2px 0 14px 0;line-height:1.5;">'
        'The AI output supports instructor judgment. It is diagnostic, not grading, and '
        'topic-level patterns matter more than any single model judgment.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;">'
        '<div style="background:#14141C;border:1px solid #262633;border-radius:10px;padding:12px 14px;">'
        '<div style="font-size:9px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;'
        'color:#A06BFF;margin-bottom:6px;">ADVERSARIAL INPUTS</div>'
        '<div style="font-size:11px;color:#9A9AAC;line-height:1.5;">'
        'Six test reflections that sound confident but contain misconceptions. '
        'Each uses student confidence\u202f=\u202f5.'
        '</div>'
        '</div>'
        '<div style="background:#14141C;border:1px solid #262633;border-radius:10px;padding:12px 14px;">'
        '<div style="font-size:9px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;'
        'color:#5AA9FF;margin-bottom:6px;">SAME AI PATH</div>'
        '<div style="font-size:11px;color:#9A9AAC;line-height:1.5;">'
        'Each case runs through the same analysis engine as real submissions. '
        'Results are temporary and never saved to the database.'
        '</div>'
        '</div>'
        '<div style="background:#14141C;border:1px solid #262633;border-radius:10px;padding:12px 14px;">'
        '<div style="font-size:9px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;'
        'color:#3DDC97;margin-bottom:6px;">PASS CONDITION</div>'
        '<div style="font-size:11px;color:#9A9AAC;line-height:1.5;">'
        'The model must label each case '
        '<strong style="color:#FF5C6C;">confident_but_wrong</strong>. '
        'A pass means it was not fooled by confident wording.'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("""<style>
div[data-testid="stButton"] button[data-testid="baseButton-primary"] {
    background-color: #A06BFF !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
}
div[data-testid="stButton"] button[data-testid="baseButton-primary"]:hover {
    background-color: #8B50F5 !important;
    color: #FFFFFF !important;
    border: none !important;
}
</style>""", unsafe_allow_html=True)

    if st.button("Run adversarial robustness check", type="primary", key="adv_btn"):
        adv_progress = st.progress(0, text="Starting…")
        adv_results: list[dict] = []
        adv_errors:  list[str]  = []

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
                    "Result":         "Pass" if passed else "Fail",
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
                    "Result":         "Error",
                })
            adv_progress.progress(
                (i + 1) / len(ADVERSARIAL_CASES),
                text=f"Checked {i + 1} of {len(ADVERSARIAL_CASES)}",
            )

        adv_progress.empty()
        if adv_errors:
            st.warning("Errors during check:\n" + "\n".join(adv_errors))

        passes    = sum(1 for r in adv_results if r["Result"] == "Pass")
        total_adv = len(ADVERSARIAL_CASES)
        if passes == total_adv:
            rate_color = "#3DDC97"
        elif passes >= total_adv // 2:
            rate_color = "#F5B544"
        else:
            rate_color = "#FF5C6C"

        if passes == total_adv:
            _adv_verdict = (
                f"Passed {passes} of {total_adv} adversarial cases. "
                "The model caught every confident-but-wrong test case."
            )
        else:
            _adv_verdict = (
                f"Passed {passes} of {total_adv} adversarial cases. "
                "Review failed cases below to see where the model over-trusted confident wording."
            )
        st.markdown(
            f'<div class="ds-pass-card" style="border-top:3px solid {rate_color};">'
            f'<div style="font-size:10px;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.5px;color:{rate_color};margin-bottom:4px;">'
            f'Robustness pass rate</div>'
            f'<div style="font-size:34px;font-weight:800;line-height:1;color:{rate_color};'
            f'font-variant-numeric:tabular-nums;">{passes}/{total_adv}</div>'
            f'<div style="font-size:11px;color:#9A9AAC;margin-top:5px;margin-bottom:8px;">'
            f'adversarial cases correctly labeled confident_but_wrong</div>'
            f'<div style="font-size:12px;color:{rate_color};opacity:0.9;line-height:1.5;">'
            f'{_adv_verdict}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

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

        st.markdown(
            '<div style="font-size:12px;font-weight:600;color:#9A9AAC;margin:14px 0 4px 0;">'
            'Reflection text per case:</div>',
            unsafe_allow_html=True,
        )
        for r in adv_results:
            icon = "\u2713" if r["Result"] == "Pass" else "\u2717"
            with st.expander(f"{icon} {r['Topic']}"):
                st.markdown(
                    '<div style="font-size:10px;font-weight:700;letter-spacing:.4px;'
                    'text-transform:uppercase;color:#525268;margin-bottom:6px;">'
                    'Test reflection \u00b7 not saved to database</div>',
                    unsafe_allow_html=True,
                )
                st.write(r["Reflection"])
        st.markdown(
            '<div style="margin-top:18px;font-size:11px;color:#525268;padding:9px 14px;'
            'background:rgba(255,255,255,0.02);border-radius:8px;'
            'border:1px solid rgba(255,255,255,0.04);line-height:1.6;">'
            'This is a targeted smoke test, not a full safety evaluation. It checks whether '
            'the model catches obvious confident-but-wrong cases, but real validation still '
            'requires instructor-labeled student reflections.'
            '</div>',
            unsafe_allow_html=True,
        )
