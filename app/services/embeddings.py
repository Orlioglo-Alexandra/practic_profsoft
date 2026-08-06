import hashlib
import math
import re

from app.ai.client import client
from app.core.config import settings


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    try:
        response = client.embeddings.create(
            model=settings.EMBED_MODEL,
            input=texts,
        )
        by_index = {item.index: item.embedding for item in response.data}
        return [by_index[i] for i in range(len(texts))]
    except Exception:
        # Groq и ряд провайдеров не дают embeddings API — локальный fallback
        return [_hash_embed(text, settings.EMBED_DIM) for text in texts]


def _hash_embed(text: str, dim: int) -> list[float]:
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    vec = [0.0] * dim
    if not tokens:
        return vec

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vec[idx] += sign

    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]
