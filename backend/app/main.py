import logging
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.routes import ai, detect, health, trace
from app.security import SECURITY_HEADERS

# Uvicorn configures its own loggers but leaves the root logger bare, so the
# app's log.info/log.warning calls (ML fallbacks, blocked requests) would be
# lost. One handler on the root makes them show up in Render's log stream.
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

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
  allow_origins=settings.cors_origins,  # from BACKEND_CORS_ORIGINS; "*" by default (no credentials)
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
  log.exception("Unhandled error on %s", request.url.path)
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

# The frontend is buildless ES modules with no version stamps in their URLs,
# so browsers must revalidate them on every load or a page can end up running
# last week's engine.js next to today's data.js. StaticFiles already sends an
# ETag, which makes an unchanged file a cheap 304. (nginx.conf and vercel.json
# set the same header for their deployments.)
#
# The security headers go on every response, API included, so a page served
# by start-dev.sh behaves exactly like the Vercel deployment — a CSP problem
# shows up on a developer's machine, not in production.
@app.middleware("http")
async def response_headers(request: Request, call_next):
  response = await call_next(request)
  for name, value in SECURITY_HEADERS.items():
    response.headers.setdefault(name, value)
  if request.url.path.startswith(settings.API_PREFIX):
    response.headers.setdefault("Cache-Control", "no-store")
  elif request.url.path.startswith("/fonts/"):
    response.headers.setdefault("Cache-Control", "public, max-age=31536000, immutable")
  else:
    response.headers.setdefault("Cache-Control", "no-cache, must-revalidate")
  return response


class SPAStaticFiles(StaticFiles):
  """Static files with a single-page-app fallback.

  Path-style deep links (/explore, /a2z-problem?prob=x) are real URLs now —
  the sitemap lists them and people share them — but there is no file at that
  path. Serve the shell and let the client router open the page, the same
  way nginx's try_files and Vercel's rewrite do. A missing *file* (anything
  with an extension, like js/missing.js) stays a 404 so broken asset paths
  are never masked by an HTML page.
  """

  async def get_response(self, path: str, scope):
    try:
      return await super().get_response(path, scope)
    except StarletteHTTPException as exc:
      last = path.rsplit("/", 1)[-1]
      if exc.status_code == 404 and "." not in last:
        return await super().get_response("index.html", scope)
      raise


FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
  app.mount("/", SPAStaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
