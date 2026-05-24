from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    OPENROUTER_API_KEY: str | None = None

settings = Settings()