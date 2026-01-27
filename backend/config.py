import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    database_url: str = "data/chat_history.db"

    class Config:
        env_file = ".env"


settings = Settings()
