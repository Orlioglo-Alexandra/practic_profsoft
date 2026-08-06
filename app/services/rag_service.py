from app.ai.client import client
from app.core.config import settings
from app.services.retrieval import search

SYSTEM_PROMPT = (
    "Отвечай ТОЛЬКО на основе предоставленного контекста. "
    "Если в контексте нет ответа на вопрос — ответь строго фразой: "
    "«В документации нет». "
    "Если ответ есть — укажи источник (source)."
)

# Минимальный score (cosine) для считания чанка релевантным
MIN_RELEVANCE = 0.05


def answer(question: str) -> dict:
    points = search(question, k=settings.TOP_K)

    context_parts: list[str] = []
    sources: list[dict] = []
    seen_sources: set[tuple] = set()

    for point in points:
        payload = point.payload or {}
        text = payload.get("text", "")
        source = payload.get("source")
        doc_id = payload.get("doc_id")
        section = payload.get("section")

        context_parts.append(
            f"[source={source}, doc_id={doc_id}, section={section}]\n{text}"
        )

        key = (source, doc_id, section)
        if key not in seen_sources:
            seen_sources.add(key)
            sources.append(
                {
                    "source": source,
                    "doc_id": doc_id,
                    "section": section,
                    "score": point.score,
                    "text": text,
                }
            )

    context = "\n\n".join(context_parts) if context_parts else "(контекст пуст)"
    relevant = [s for s in sources if (s.get("score") or 0) >= MIN_RELEVANCE]

    try:
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Контекст:\n{context}\n\nВопрос: {question}",
                },
            ],
            temperature=0,
        )
        answer_text = (response.choices[0].message.content or "").strip()
    except Exception:
        answer_text = _fallback_answer(question, relevant)

    return {"answer": answer_text, "sources": sources}


def _fallback_answer(question: str, relevant: list[dict]) -> str:
    if not relevant:
        return "В документации нет"

    q_tokens = {t for t in question.lower().replace("?", "").split() if len(t) > 3}
    for item in relevant:
        text = (item.get("text") or "").lower()
        if q_tokens and any(token in text for token in q_tokens):
            source = item.get("source") or "unknown"
            return f"{item.get('text')} (source: {source})"

    return "В документации нет"
