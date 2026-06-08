import httpx

from app.config import settings


async def _post(path: str, payload: dict) -> dict:
    url = settings.ML_SERVICE_URL.rstrip("/") + path
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:  # noqa: BLE001
        return _fallback(path, str(exc))


async def explain(payload: dict) -> dict:
    return await _post("/explain", payload)


async def bugfind(payload: dict) -> dict:
    return await _post("/bugfind", payload)


def _fallback(path: str, error: str) -> dict:
    if path == "/explain":
        text = (
            "This step expands the most promising option before all the rest "
            "— that greedy choice is the heart of the algorithm."
        )
    else:
        text = "No obvious bug found offline. Start the ML service for a deeper review."
    return {"fallback": True, "error": error, "text": text}
