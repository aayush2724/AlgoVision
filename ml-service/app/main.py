from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import llm
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExplainBody(BaseModel):
    algorithm: str = "dijkstra"
    step: dict = {}
    level: str = "beginner"


class BugBody(BaseModel):
    language: str = "python"
    code: str = ""


@app.get("/health")
def health():
    return {"status": "ok", "service": "algovision-ml", "live_provider": settings.has_provider}


@app.post("/explain")
def explain(body: ExplainBody):
    return llm.explain_step(body.algorithm, body.step, body.level)


@app.post("/bugfind")
def bugfind(body: BugBody):
    return llm.find_bug(body.language, body.code)
