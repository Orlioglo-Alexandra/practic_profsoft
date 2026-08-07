import voyageai

from app.core.config import settings

voyage_client = voyageai.Client(api_key=settings.VOYAGE_API_KEY or None, timeout=30)
