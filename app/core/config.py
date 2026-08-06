from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    API_URL: str
    RESULT_URL: str
    OPENAI_API_KEY: str = ""
    MODEL: str = "gpt-4o-mini"
    PROMPT: str = (
        "Определи тональность отзыва. Ответь строго одним словом: "
        "positive, negative или neutral."
    )
    TEST_MODE: bool = False
    MAX_ATTEMPTS: int = 3
    POLL_INTERVAL: int = 5
    STUCK_MINUTES: int = 5
    RUN_WORKER: bool = True
    EMBED_MODEL: str = "text-embedding-3-small"
    EMBED_DIM: int = 1536
    CHAT_MODEL: str = "gpt-4o-mini"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 75
    TOP_K: int = 5
    QDRANT_URL: str = "http://qdrant:6333"
    COLLECTION: str = "docs"

    class Config:
        env_file = ".env"


settings = Settings()
