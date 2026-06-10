from fastapi import APIRouter
from pydantic import BaseModel

from app.services import ml_client

router = APIRouter(prefix="/ai", tags=["ai"])


class ExplainBody(BaseModel):
    algorithm: str = "dijkstra"
    step: dict = {}
    level: str = "beginner"


class BugBody(BaseModel):
    language: str = "python"
    code: str = ""


@router.post("/explain")
async def explain(body: ExplainBody):
    return await ml_client.explain(body.model_dump())


@router.post("/bugfind")
async def bugfind(body: BugBody):
    body.language = body.language.lower()
    return await ml_client.bugfind(body.model_dump())
