from app.core.config import settings
from app.services.embeddings import embed_texts
from app.vector.qdrant_client import qdrant


def search(question: str, k: int) -> list:
    qvec = embed_texts([question], input_type="query")[0]
    result = qdrant.query_points(
        collection_name=settings.COLLECTION,
        query=qvec,
        limit=k,
        with_payload=True,
    )
    return list(result.points)
