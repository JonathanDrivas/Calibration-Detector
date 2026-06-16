import json
import os
import anthropic

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(
            base_url=os.environ["AI_INTEGRATIONS_ANTHROPIC_BASE_URL"],
            api_key=os.environ["AI_INTEGRATIONS_ANTHROPIC_API_KEY"],
        )
    return _client


def compute_label(understanding: int, confidence: int) -> str:
    if understanding >= 4 and confidence >= 4:
        return "understands"
    if understanding <= 2 and confidence >= 4:
        return "confident_but_wrong"
    if understanding >= 4 and confidence <= 2:
        return "underconfident"
    if understanding <= 2 and confidence <= 2:
        return "knows_confused"
    return "partial"


def analyze_reflection(reflection_text: str, topic_description: str, topic_misconceptions: str) -> dict:
    prompt = f"""You are judging a student's demonstrated understanding of a course topic.

Topic description (correct):
{topic_description}

Common misconceptions for this topic:
{topic_misconceptions}

Student's reflection:
{reflection_text}

Rate the student's understanding on a scale of 1 to 5 using these criteria:

5 — The reflection captures the core idea correctly, even if it is short or plainly worded.
4 — Mostly correct with a minor gap or imprecision.
3 — Partially correct but missing or muddling something important. The reflection must actually attempt to explain the concept to earn a 3.
2 — Mostly wrong or shows a clear misconception.
1 — Empty, off topic, entirely wrong, or admits confusion without giving any real explanation.

Critical rules for scoring:
- Brevity is NOT a reason to lower the score. A correct core idea stated simply should score 4 or 5.
- Plain wording should NOT be penalized. Simple, clear, correct answers deserve high scores.
- Reserve 1 and 2 ONLY for answers that are actually wrong, empty, off topic, or show a real misconception.
- Do NOT reward confident tone, keywords, or buzzwords if the explanation is conceptually wrong.
- If the reflection uses correct vocabulary but explains the concept incorrectly, score it 1 or 2.
- Do NOT infer confidence from the reflection text. Confidence comes only from the student_confidence value, which is handled separately.
- If a reflection does not actually explain the concept, score it 1 or 2. This includes reflections where the student only says they are confused, unsure, or cannot explain the idea. No explanation means no demonstrated understanding.
- Use 3 ONLY when the reflection actually attempts to explain the concept but is partially correct, incomplete, or muddles something important.
- IMPORTANT nuance: do NOT automatically penalize a student just for saying they are unsure. If the student admits uncertainty but then gives a correct or mostly correct explanation, score the demonstrated explanation normally. The low score applies only when the reflection admits confusion AND gives no real explanation.

Anchor examples:
- SCORES 5: "Adoption goes innovators, early adopters, early majority, late majority, laggards, and depends on more than the technology." — Correct and complete even though brief.
- SCORES 1 or 2: "The early majority is the most venturesome group, the first to adopt anything new." — Confident phrasing but a clear misconception.
- SCORES 1: "I am not sure I understand this and I cannot really explain it." — Admits confusion and demonstrates no understanding.

Respond with ONLY valid JSON in this exact format, no markdown, no explanation:
{{"understanding": <integer 1-5>, "misconception": "<short phrase or none>"}}

Rules:
- understanding must be an integer from 1 to 5
- misconception must be a short phrase naming the main misconception, or the exact word none
- Do not include markdown
- Do not include any explanation outside the JSON"""

    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    data = json.loads(raw)

    understanding = int(data["understanding"])
    misconception = str(data["misconception"]).strip()

    if not (1 <= understanding <= 5):
        raise ValueError(f"understanding out of range: {understanding}")

    return {"understanding": understanding, "misconception": misconception}
