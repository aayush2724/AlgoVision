import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AlgoVision API"
    API_PREFIX: str = "/api"
    ML_SERVICE_URL: str = os.getenv("ML_SERVICE_URL", "http://localhost:8500")
    CORS_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5500,http://localhost:8080,http://127.0.0.1:5500,http://localhost:3000",
        ).split(",")
        if o.strip()
    ]

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
