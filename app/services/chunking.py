import re


def split_text(text: str, size: int, overlap: int) -> list[str]:
    """Разбивает текст на чанки по абзацам/предложениям с перекрытием, без разрезания слов."""
    text = (text or "").strip()
    if not text:
        return []
    if size <= 0:
        return [text]
    overlap = max(0, min(overlap, size - 1))

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        paragraphs = [text]

    units: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph) <= size:
            units.append(paragraph)
            continue
        sentences = [
            s.strip()
            for s in re.split(r"(?<=[.!?…])\s+", paragraph)
            if s.strip()
        ]
        if not sentences:
            units.extend(_split_by_words(paragraph, size))
            continue
        for sentence in sentences:
            if len(sentence) <= size:
                units.append(sentence)
            else:
                units.extend(_split_by_words(sentence, size))

    chunks: list[str] = []
    current = ""

    for unit in units:
        if not current:
            current = unit
            continue

        candidate = f"{current} {unit}".strip()
        if len(candidate) <= size:
            current = candidate
            continue

        chunks.append(current)
        current = _overlap_prefix(current, overlap)
        if current:
            current = f"{current} {unit}".strip()
            if len(current) > size:
                chunks.append(current[:size].rsplit(" ", 1)[0] or current[:size])
                current = unit
        else:
            current = unit

        if len(current) > size:
            for piece in _split_by_words(current, size):
                chunks.append(piece)
            current = _overlap_prefix(chunks[-1], overlap) if chunks else ""

    if current:
        chunks.append(current)

    return [c for c in chunks if c]


def _split_by_words(text: str, size: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    parts: list[str] = []
    current = ""
    for word in words:
        if len(word) > size:
            if current:
                parts.append(current)
                current = ""
            for i in range(0, len(word), size):
                parts.append(word[i : i + size])
            continue

        candidate = f"{current} {word}".strip()
        if len(candidate) <= size:
            current = candidate
        else:
            if current:
                parts.append(current)
            current = word

    if current:
        parts.append(current)
    return parts


def _overlap_prefix(text: str, overlap: int) -> str:
    if overlap <= 0 or not text:
        return ""
    if len(text) <= overlap:
        return text
    tail = text[-overlap:]
    space = tail.find(" ")
    if space == -1:
        return tail.lstrip()
    return tail[space + 1 :].lstrip()
