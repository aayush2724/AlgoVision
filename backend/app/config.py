import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AlgoVision API"
    API_PREFIX: str = "/api"
    ML_SERVICE_URL: str = os.getenv("ML_SERVICE_URL", "http://localhost:8001")
    CORS_ORIGINS: list[str] = ["*"]

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
