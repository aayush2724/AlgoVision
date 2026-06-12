import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.routes import ai, health, trace, detect

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
  title=settings.PROJECT_NAME,
  # Hide implementation details in production
  docs_url="/docs" if os.getenv("ENV", "dev") == "dev" else None,
  redoc_url=None,
  openapi_url="/openapi.json" if os.getenv("ENV", "dev") == "dev" else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],      # public portfolio API — no credentials
  allow_credentials=False,
  allow_methods=["GET", "POST"],
  allow_headers=["Content-Type"],
)

# Global request body size limit — 64KB max
@app.middleware("http")
async def limit_body_size(request: Request, call_next):
  max_body = 64 * 1024  # 64 KB
  content_length = request.headers.get("content-length")
  if content_length and int(content_length) > max_body:
    return JSONResponse(
      status_code=413,
      content={"detail": "Request body too large."}
    )
  return await call_next(request)

# Global exception handler — never leak stack traces
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
  import logging
  logging.getLogger(__name__).exception("Unhandled error on %s", request.url.path)
  return JSONResponse(
    status_code=500,
    content={"detail": "An internal error occurred."}
  )

app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(trace.router, prefix=settings.API_PREFIX)
app.include_router(ai.router,    prefix=settings.API_PREFIX)
app.include_router(detect.router,prefix=settings.API_PREFIX)

@app.get("/health-root")
def root():
  return {"name": settings.PROJECT_NAME}

FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
  app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
