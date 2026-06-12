import logging
import httpx
from app.config import settings

log = logging.getLogger(__name__)

# Safe error messages — never expose internal details to client
_SAFE_ERRORS = {
  "/explain":  "AI narrator temporarily unavailable. Using offline mode.",
  "/bugfind":  "AI scanner temporarily unavailable. Using offline analysis.",
}

async def _post(path: str, payload: dict) -> dict:
  url = settings.ML_SERVICE_URL.rstrip("/") + path
  try:
    async with httpx.AsyncClient(timeout=8.0) as client:
      resp = await client.post(url, json=payload)
      resp.raise_for_status()
      return resp.json()
  except httpx.TimeoutException:
    log.warning("ML service timeout on %s", path)
    return _fallback(path, "timeout")
  except httpx.HTTPStatusError as exc:
    log.warning("ML service HTTP error %s on %s", exc.response.status_code, path)
    return _fallback(path, "http_error")
  except httpx.ConnectError:
    log.info("ML service not reachable on %s — using fallback", path)
    return _fallback(path, "unavailable")
  except Exception:
    log.exception("Unexpected ML client error on %s", path)
    return _fallback(path, "unknown")

async def explain(payload: dict) -> dict:
  return await _post("/explain", payload)

async def bugfind(payload: dict) -> dict:
  return await _post("/bugfind", payload)

def _fallback(path: str, reason: str) -> dict:
  # NEVER include exception details, URLs, or internal state in response
  if path == "/explain":
    return {
      "text": (
        "This step advances the algorithm toward its goal. "
        "Start the ML service with a GROQ_API_KEY for live narration."
      ),
      "live": False,
      "fallback": True,
    }
  return {
    "hints": [
      "Check boundary conditions — off-by-one errors are common.",
      "Verify your base case handles empty input.",
      "Trace through a small example by hand before coding.",
    ],
    "live": False,
    "fallback": True,
  }
