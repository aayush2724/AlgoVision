from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME:    str  = "AlgoVision API"
  API_PREFIX:      str  = "/api"
  ML_SERVICE_URL:  str  = "http://localhost:8000"
  ENV:             str  = "dev"

  model_config = {"env_file": ".env", "extra": "ignore"}

@lru_cache
def get_settings() -> Settings:
  return Settings()

settings = get_settings()
