import ipaddress
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app import llm
from app.config import settings

log = logging.getLogger(__name__)

app = FastAPI(
  title="AlgoVision ML Service",
  docs_url=None,    # hide docs — internal service
  redoc_url=None,
  openapi_url=None,
)

def _is_internal(host: str) -> bool:
  # Loopback (Replit / start-dev.sh) and private ranges (Docker bridge network).
  # The compose file does not publish this service's port, so this is
  # defense-in-depth, not the primary boundary.
  try:
    ip = ipaddress.ip_address(host)
    return ip.is_loopback or ip.is_private
  except ValueError:
    return host == "localhost"

@app.middleware("http")
async def internal_only(request: Request, call_next):
  client_host = request.client.host if request.client else ""
  # Two ways in. A private-range caller is the Docker/local case. A matching
  # shared secret is the split-host case (Render), where the backend reaches
  # this service over the public internet and its source IP proves nothing.
  token = settings.INTERNAL_TOKEN
  authorised = _is_internal(client_host) or (
    bool(token) and request.headers.get("x-internal-token") == token)
  if request.url.path != "/health" and not authorised:
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
