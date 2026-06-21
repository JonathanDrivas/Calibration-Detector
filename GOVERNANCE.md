# Governance and Responsible Use

**Project:** Calibration Detector
**Course:** MASY1-GC1800 Emerging Technologies, NYU School of Professional Studies, Summer 2026
**Team:** Jonathan, Yolande, Joyce

The Calibration Detector turns short student reflections into a topic-level picture of where a class is struggling. This note explains how it is kept responsible.

## Purpose and boundary

The tool is diagnostic, not evaluative. It exists to help an instructor see which concepts need attention while the term is still live. It does not grade or rank students, and nothing it produces is used for discipline or for any decision about an individual. It is not a tutoring or surveillance system, and it is not a replacement for an instructor's judgment.

## Student disclosure

Students see a clear notice at the moment they submit a reflection. The notice explains that reflections are reviewed by topic to improve teaching and are never used for grades. Nothing about how the data is used is hidden from the student.

## Privacy and data handling

Reflections are stored under randomly assigned nicknames rather than real identities. No part of the faculty view ties a reflection back to a named student. The data model is written to respect FERPA in any real deployment, and for this project the system runs on simulated reflections only, with no real student data involved.

## Aggregation by default

The faculty dashboard reports results by topic, never at the level of a named individual. An instructor sees that a concept is shaky and what the common misconception is, without seeing who wrote what. This aggregation is not only a privacy measure. It is also what makes the confident-but-wrong signal safe to act on, because it points an instructor toward a topic to reteach rather than toward a student to single out.

## Human oversight

The model reads understanding from text, which is an imperfect signal. Low-certainty cases are routed for human review rather than acted on automatically. The instructor remains the authority on what a result means and what to do about it, with the system offering a signal rather than a verdict.

## Risk controls and limitations

The main risk is a wrong read, where the model misjudges a reflection. Several controls reduce its impact. Results are shown by topic, so a single misread does not define a student, and low-certainty cases go to human review instead of being acted on directly. The engine is also validated against a labeled dataset, with accuracy reported openly rather than assumed. The known limitations are that the understanding read depends on how well a topic is represented in the context store, and that short reflections carry less signal than longer ones. The current evidence also comes from simulated data, so a real deployment would first validate the engine against instructor-labeled reflections.
