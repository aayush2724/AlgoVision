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
  # Shared secret proving to the ML service that a request came from here.
  # Only needed when the two run on different hosts.
  INTERNAL_TOKEN:  str  = ""

  model_config = {"env_file": ".env", "extra": "ignore"}

  @property
  def ml_service_url(self) -> str:
    """ML_SERVICE_URL with a scheme guaranteed.

    Render's `fromService: property: host` hands over a bare hostname with no
    scheme, which httpx refuses to parse — so every AI call silently fell back
    to offline narration. Normalising here means the setting works whether it
    is a bare host, or a full URL from compose.
    """
    raw = (self.ML_SERVICE_URL or "").strip().rstrip("/")
    if not raw:
      return ""
    if "://" in raw:
      return raw
    # Bare host: localhost stays http, anything else is a real deployment.
    scheme = "http" if raw.split(":")[0] in ("localhost", "127.0.0.1") else "https"
    return f"{scheme}://{raw}"

  @property
  def cors_origins(self) -> list[str]:
    return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
  return Settings()

settings = get_settings()
