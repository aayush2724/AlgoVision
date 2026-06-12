from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from app.services import ml_client
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/ai", tags=["ai"])

# Max sizes — large enough for real code, blocks abuse
MAX_CODE_BYTES   = 8_000   # ~200 lines of code
MAX_ALGO_BYTES   = 60
MAX_LEVEL_BYTES  = 20

ALLOWED_LEVELS    = {"beginner", "intermediate", "advanced"}
ALLOWED_LANGUAGES = {"python", "c++", "java", "javascript", "cpp", "js"}

class ExplainBody(BaseModel):
  algorithm: str = Field(default="dijkstra", max_length=MAX_ALGO_BYTES)
  step:      dict = Field(default_factory=dict)
  level:     str  = Field(default="beginner",     max_length=MAX_LEVEL_BYTES)
  realworld_meta: dict = Field(default_factory=dict)

  @field_validator("level")
  @classmethod
  def validate_level(cls, v):
    if v not in ALLOWED_LEVELS:
      return "beginner"   # silently normalise — not a security issue
    return v

  @field_validator("algorithm")
  @classmethod
  def sanitise_algo(cls, v):
    # Allow only alphanumeric + underscore + hyphen
    import re
    return re.sub(r"[^a-zA-Z0-9_\-]", "", v)[:MAX_ALGO_BYTES]

class BugBody(BaseModel):
  language: str = Field(default="python", max_length=20)
  code:     str = Field(default="", max_length=MAX_CODE_BYTES)

  @field_validator("language")
  @classmethod
  def validate_language(cls, v):
    cleaned = v.lower().strip()
    if cleaned not in ALLOWED_LANGUAGES:
      return "python"
    return cleaned

  @field_validator("code")
  @classmethod
  def sanitise_code(cls, v):
    # Reject prompt injection attempts in the code field.
    # Legitimate code never needs these phrases.
    INJECTION_PATTERNS = [
      "ignore previous",
      "ignore all instructions",
      "disregard",
      "you are now",
      "act as",
      "jailbreak",
      "dan mode",
      "system prompt",
    ]
    low = v.lower()
    for pat in INJECTION_PATTERNS:
      if pat in low:
        raise ValueError("Invalid code content.")
    return v

# 30 explain calls per minute per IP — generous for normal use
@router.post("/explain")
@limiter.limit("30/minute")
async def explain(request: Request, body: ExplainBody):
  return await ml_client.explain(body.model_dump())

# 20 bug scans per minute per IP
@router.post("/bugfind")
@limiter.limit("20/minute")
async def bugfind(request: Request, body: BugBody):
  return await ml_client.bugfind(body.model_dump())
