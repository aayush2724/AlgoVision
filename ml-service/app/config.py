from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME:    str = "AlgoVision ML"
  GROQ_API_KEY:    str = ""
  GEMINI_API_KEY:  str = ""
  ANTHROPIC_API_KEY: str = ""

  model_config = {"env_file": ".env", "extra": "ignore"}

  @property
  def has_provider(self) -> bool:
    return bool(self.GROQ_API_KEY or self.GEMINI_API_KEY or self.ANTHROPIC_API_KEY)

settings = Settings()
