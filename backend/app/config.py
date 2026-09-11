from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME:    str  = "AlgoVision API"
  API_PREFIX:      str  = "/api"
  ML_SERVICE_URL:  str  = "http://localhost:8500"
  ENV:             str  = "dev"
  # Comma-separated list of allowed origins, or "*" for a public API.
  BACKEND_CORS_ORIGINS: str = "*"

  model_config = {"env_file": ".env", "extra": "ignore"}

  @property
  def cors_origins(self) -> list[str]:
    return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
  return Settings()

settings = get_settings()
