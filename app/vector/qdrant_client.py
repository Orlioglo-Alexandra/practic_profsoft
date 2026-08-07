from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.config import settings

qdrant = QdrantClient(url=settings.QDRANT_URL)


def ensure_collection() -> bool:
    """Создаёт коллекцию при отсутствии или неверной размерности.

    Returns:
        True, если коллекцию создали/пересоздали (нужна переиндексация).
    """
    collections = qdrant.get_collections().collections
    names = {collection.name for collection in collections}

    recreated = False
    if settings.COLLECTION in names:
        info = qdrant.get_collection(settings.COLLECTION)
        vectors = info.config.params.vectors
        size = getattr(vectors, "size", None)
        if size is not None and size != settings.EMBED_DIM:
            qdrant.delete_collection(settings.COLLECTION)
            recreated = True
        else:
            return False
    else:
        recreated = True

    qdrant.create_collection(
        collection_name=settings.COLLECTION,
        vectors_config=VectorParams(
            size=settings.EMBED_DIM,
            distance=Distance.COSINE,
        ),
    )
    return recreated
