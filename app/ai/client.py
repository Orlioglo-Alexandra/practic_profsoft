from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url="https://api.groq.com/openai/v1", timeout=30)
