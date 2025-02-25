from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_KEY:str
    SECRET_KEY: str
    DATABASE_URL: str
    DEBUG: bool

    class Config:
        env_file = ".env"  # Load from .env file

settings = Settings()
