from app.ai.client import client
from app.core.config import settings

VALID_LABELS = {"positive", "negative", "neutral"}


def classify(text: str) -> str:
    if settings.TEST_MODE:
        return "neutral"

    response = client.chat.completions.create(
        model=settings.MODEL,
        messages=[
            {"role": "system", "content": settings.PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    result = response.choices[0].message.content.strip().lower().strip(".!?,:;")
    if result not in VALID_LABELS:
        return "neutral"
    return result
