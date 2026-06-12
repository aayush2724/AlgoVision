import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app import llm

log = logging.getLogger(__name__)

app = FastAPI(
  title="AlgoVision ML Service",
  docs_url=None,    # hide docs — internal service
  redoc_url=None,
  openapi_url=None,
)

# Only accept requests from localhost / backend container.
# On Replit both services run on the same machine so this works.
ALLOWED_INTERNAL_HOSTS = {
  "localhost", "127.0.0.1", "0.0.0.0",
  os.getenv("BACKEND_HOST", "localhost"),
}

@app.middleware("http")
async def internal_only(request: Request, call_next):
  client_host = request.client.host if request.client else ""
  # Allow health checks from anywhere, restrict everything else
  if request.url.path != "/health" and client_host not in ALLOWED_INTERNAL_HOSTS:
    log.warning("Blocked external request to ML service from %s", client_host)
    return JSONResponse(status_code=403, content={"detail": "Forbidden."})
  return await call_next(request)

@app.middleware("http")
async def limit_body_size(request: Request, call_next):
  cl = request.headers.get("content-length")
  if cl and int(cl) > 32 * 1024:
    return JSONResponse(status_code=413, content={"detail": "Too large."})
  return await call_next(request)

# Global error handler — no stack traces to caller
@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception):
  log.exception("ML service error on %s", request.url.path)
  return JSONResponse(status_code=500, content={"detail": "Internal error."})

class ExplainBody(BaseModel):
  algorithm:     str  = Field(default="dijkstra", max_length=60)
  step:          dict = Field(default_factory=dict)
  level:         str  = Field(default="beginner",  max_length=20)
  realworld_meta:dict = Field(default_factory=dict)

class BugFindBody(BaseModel):
  language: str = Field(default="python", max_length=20)
  code:     str = Field(default="",       max_length=8_000)

@app.get("/health")
def health():
  return {"status": "ok", "service": "algovision-ml"}

@app.post("/explain")
def explain(body: ExplainBody):
  return llm.explain_step(
    body.algorithm, body.step, body.level, body.realworld_meta
  )

@app.post("/bugfind")
def bugfind(body: BugFindBody):
  return llm.find_bug(body.language, body.code)
