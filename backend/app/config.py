import os
from functools import lru_cache


class Settings:
    PROJECT_NAME: str = "AlgoVision API"
    API_PREFIX: str = "/api"
    ML_SERVICE_URL: str = os.getenv("ML_SERVICE_URL", "http://localhost:8500")
    CORS_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5500,http://localhost:8080",
        ).split(",")
        if o.strip()
    ]


@lru_cache
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()
