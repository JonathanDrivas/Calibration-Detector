import streamlit as st

st.title("About & Responsible Use")

st.markdown("""
The **Calibration Detector** turns short student reflections into a topic-level picture
of where a class is struggling.
""")

st.divider()

principles = [
    (
        "🎯 Diagnostic, not evaluative",
        "This is a diagnostic tool, not an evaluation one. It does not grade or rank anyone, "
        "and it is not used for discipline.",
    ),
    (
        "🔒 Privacy by design",
        "Every result is shown to faculty by topic and never tied to a student's name. "
        "Reflections are stored under nicknames rather than real identities.",
    ),
    (
        "📢 Student transparency",
        "Students see a clear notice when they submit, explaining that their reflections are "
        "reviewed by topic to improve teaching and are never used for grades.",
    ),
    (
        "🤝 Human judgment stays central",
        "The model reads understanding from text, which is an imperfect signal. "
        "Low-certainty cases are routed for human review, and the tool is meant to support "
        "a teacher's judgment — never replace it.",
    ),
    (
        "🧪 Simulated data only",
        "This project runs only on simulated data and is written to respect FERPA "
        "in any real deployment.",
    ),
]

for icon_title, body in principles:
    with st.container(border=True):
        st.markdown(f"**{icon_title}**")
        st.markdown(body)

st.divider()

st.caption(
    "Full responsible-use note: The Calibration Detector turns short student reflections into "
    "a topic-level picture of where a class is struggling. It is a diagnostic tool, not an "
    "evaluation one. It does not grade or rank anyone, and it is not used for discipline. "
    "Every result is shown to faculty by topic and never tied to a student's name, and "
    "reflections are stored under nicknames rather than real identities. Students see a clear "
    "notice when they submit, explaining that their reflections are reviewed by topic to improve "
    "teaching and are never used for grades. The model reads understanding from text, which is "
    "an imperfect signal, so low-certainty cases are routed for human review and the tool is "
    "meant to support a teacher's judgment, never replace it. It runs only on simulated data "
    "for this project and is written to respect FERPA in any real deployment."
)
