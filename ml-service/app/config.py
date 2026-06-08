import os


class Settings:
    PROJECT_NAME = "AlgoVision ML"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    @property
    def has_provider(self) -> bool:
        return bool(self.GROQ_API_KEY or self.GEMINI_API_KEY)


settings = Settings()
