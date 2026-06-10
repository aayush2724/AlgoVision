from fastapi import FastAPI
from pydantic import BaseModel
from app import llm

app = FastAPI()

class ExplainBody(BaseModel):
    algorithm: str = "dijkstra"
    step: dict = {}
    level: str = "beginner"
    realworld_meta: dict = {}

class BugFindBody(BaseModel):
    language: str = "python"
    code: str = ""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/explain")
def explain(body: ExplainBody):
    return llm.explain_step(body.algorithm, body.step, body.level, body.realworld_meta)

@app.post("/bugfind")
def bugfind(body: BugFindBody):
    return llm.find_bug(body.language, body.code)
