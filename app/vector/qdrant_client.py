from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.config import settings

qdrant = QdrantClient(url=settings.QDRANT_URL)


def ensure_collection() -> None:
    collections = qdrant.get_collections().collections
    names = {collection.name for collection in collections}
    if settings.COLLECTION not in names:
        qdrant.create_collection(
            collection_name=settings.COLLECTION,
            vectors_config=VectorParams(
                size=settings.EMBED_DIM,
                distance=Distance.COSINE,
            ),
        )
