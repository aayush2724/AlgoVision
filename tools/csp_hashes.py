"""Print the CSP sha256 sources for index.html's inline scripts.

Run after editing either inline <script> in frontend/index.html, then paste
the two values into backend/app/security.py, vercel.json and
frontend/nginx-headers.inc (tests/test_security.py checks they agree).

    python3 tools/csp_hashes.py
"""
import base64
import hashlib
import re
from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "frontend" / "index.html"


def inline_scripts(html: str) -> list[str]:
  # Only scripts without src= are inline. The regex keeps the body verbatim —
  # the hash covers every byte between the tags, whitespace included.
  return re.findall(r'<script(?: type="importmap")?>(.*?)</script>', html, flags=re.S)


def csp_hash(body: str) -> str:
  digest = hashlib.sha256(body.encode()).digest()
  return f"'sha256-{base64.b64encode(digest).decode()}'"


if __name__ == "__main__":
  for body in inline_scripts(HTML.read_text()):
    print(csp_hash(body), "#", body.strip().splitlines()[0][:50])
