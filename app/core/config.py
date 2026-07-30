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

    class Config:
        env_file = ".env"


settings = Settings()
