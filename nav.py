"""Shared top navigation bar injected at the top of every page."""
import streamlit as st


def render_nav(current: str = "") -> None:
    """
    Render an always-visible top nav bar.
    current: 'home' | 'reflection' | 'dashboard' | 'about'
    """
    st.markdown("""
<style>
/* ── Hide sidebar nav links (top nav replaces them) ─────────────── */
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Align nav columns vertically ───────────────────────────────── */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] {
    display: flex !important;
    align-items: center !important;
}

/* ── Page link: base style ───────────────────────────────────────── */
[data-testid="stPageLink"] {
    width: 100% !important;
}
[data-testid="stPageLink"] > a,
[data-testid="stPageLink"] > div > a {
    display: block !important;
    text-decoration: none !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #9A9AAC !important;
    padding: 5px 8px !important;
    border-radius: 6px !important;
    text-align: center !important;
    white-space: nowrap !important;
    transition: color 0.15s, background 0.15s !important;
}
[data-testid="stPageLink"] > a:hover,
[data-testid="stPageLink"] > div > a:hover {
    color: #ECECF2 !important;
    background: rgba(255,255,255,0.05) !important;
}

/* ── Active page (disabled link) → violet ────────────────────────── */
[data-testid="stPageLink"] > a[aria-disabled="true"],
[data-testid="stPageLink"] > a[tabindex="-1"],
[data-testid="stPageLink"] > div > a[aria-disabled="true"],
[data-testid="stPageLink"] > div > a[tabindex="-1"] {
    color: #A06BFF !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    pointer-events: none !important;
    background: rgba(160,107,255,0.08) !important;
}

/* ── Remove Streamlit's default link underline decoration ────────── */
[data-testid="stPageLink"] a::after { display: none !important; }
</style>
""", unsafe_allow_html=True)

    logo_col, sp, h_col, r_col, d_col, a_col = st.columns(
        [3.4, 0.1, 0.75, 1.0, 1.05, 0.7], gap="small"
    )

    with logo_col:
        st.markdown("""
<div style="display:flex;align-items:center;gap:9px;height:38px;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2.5px;
              width:18px;height:18px;flex-shrink:0;">
    <div style="background:#5AA9FF;border-radius:2px;"></div>
    <div style="background:#3DDC97;border-radius:2px;"></div>
    <div style="background:#F5B544;border-radius:2px;"></div>
    <div style="background:#FF5C6C;border-radius:2px;"></div>
  </div>
  <span style="font-size:15px;font-weight:800;color:#ECECF2;
               letter-spacing:-0.02em;white-space:nowrap;">
    Calibration Detector
  </span>
</div>""", unsafe_allow_html=True)

    with h_col:
        st.page_link("home.py", label="Home",
                     disabled=(current == "home"))
    with r_col:
        st.page_link("pages/1_Student_Reflection.py", label="Reflection",
                     disabled=(current == "reflection"))
    with d_col:
        st.page_link("pages/2_Faculty_Dashboard.py", label="Dashboard",
                     disabled=(current == "dashboard"))
    with a_col:
        st.page_link("pages/3_About_and_Responsible_Use.py", label="About",
                     disabled=(current == "about"))

    st.markdown(
        '<div style="border-top:1px solid #262633;margin:2px 0 14px 0;"></div>',
        unsafe_allow_html=True,
    )
