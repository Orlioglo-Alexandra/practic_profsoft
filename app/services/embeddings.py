from app.ai.voyage_client import voyage_client
from app.core.config import settings


def embed_texts(texts: list[str], input_type: str | None = None) -> list[list[float]]:
    """Строит эмбеддинги через Voyage AI.

    input_type: "document" для индексации, "query" для поиска.
    """
    if not texts:
        return []
    if not settings.VOYAGE_API_KEY:
        raise RuntimeError(
            "VOYAGE_API_KEY не задан. Добавьте ключ Voyage AI в .env"
        )

    response = voyage_client.embed(
        texts=texts,
        model=settings.EMBED_MODEL,
        input_type=input_type,
        output_dimension=settings.EMBED_DIM,
    )
    return list(response.embeddings)
