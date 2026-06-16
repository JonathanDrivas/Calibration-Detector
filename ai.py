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

Judge ONLY the student's demonstrated understanding of the topic based on how well the reflection matches the correct topic description and common misconceptions. Do NOT factor in the student's confidence, tone, certainty, or wording style.

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
