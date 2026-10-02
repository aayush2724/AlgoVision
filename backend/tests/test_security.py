"""Headers, deep links and the three copies of the CSP.

The static site is served by Vercel, nginx and this app; each carries its
own copy of the headers. These tests keep the copies honest and make sure
the dev server behaves like production.
"""
import json
import re
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.security import CSP, SECURITY_HEADERS

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from csp_hashes import csp_hash, inline_scripts  # noqa: E402

client = TestClient(app)


def test_api_responses_carry_security_headers():
  r = client.get("/api/health")
  assert r.status_code == 200
  for name, value in SECURITY_HEADERS.items():
    assert r.headers.get(name) == value, name
  assert r.headers["Cache-Control"] == "no-store"


def test_shell_carries_security_headers_and_revalidates():
  r = client.get("/")
  assert r.status_code == 200
  assert r.headers["Content-Security-Policy"] == CSP
  assert r.headers["X-Frame-Options"] == "DENY"
  assert r.headers["Cache-Control"] == "no-cache, must-revalidate"


def test_fonts_are_immutable():
  r = client.get("/fonts/geist-latin.woff2")
  assert r.status_code == 200
  assert r.headers["Cache-Control"] == "public, max-age=31536000, immutable"


def test_deep_links_serve_the_shell():
  # Path-style routes are real URLs (sitemap, shares); the router opens them.
  for path in ("/explore", "/a2z", "/a2z-problem?step=1&prob=x", "/privacy", "/nope"):
    r = client.get(path)
    assert r.status_code == 200, path
    assert r.headers["content-type"].startswith("text/html"), path
    assert "<main id=\"app\"" in r.text


def test_missing_files_stay_404():
  # A broken asset path must not be masked by an HTML page.
  assert client.get("/js/does-not-exist.js").status_code == 404
  assert client.get("/offline/nope.json").status_code == 404


def test_seo_files_are_served():
  robots = client.get("/robots.txt")
  assert robots.status_code == 200
  assert "Sitemap:" in robots.text
  sitemap = client.get("/sitemap.xml")
  assert sitemap.status_code == 200
  assert "<urlset" in sitemap.text
  assert client.get("/favicon.ico").status_code == 200
  assert client.get("/favicon.svg").status_code == 200
  assert client.get("/site.webmanifest").status_code == 200


def test_csp_hashes_match_index_html_inline_scripts():
  html = (ROOT / "frontend" / "index.html").read_text()
  bodies = inline_scripts(html)
  assert len(bodies) == 2, "expected the import map and the API-origin script"
  for body in bodies:
    assert csp_hash(body) in CSP, "run tools/csp_hashes.py and update the CSP"


def test_csp_copies_agree():
  vercel = json.loads((ROOT / "vercel.json").read_text())
  vercel_csp = next(
    h["value"]
    for rule in vercel["headers"] for h in rule["headers"]
    if h["key"] == "Content-Security-Policy"
  )
  assert vercel_csp == CSP

  nginx = (ROOT / "frontend" / "nginx-headers.inc").read_text()
  m = re.search(r'Content-Security-Policy "([^"]+)"', nginx)
  assert m and m.group(1) == CSP


def test_other_headers_agree_with_vercel():
  vercel = json.loads((ROOT / "vercel.json").read_text())
  vercel_headers = {
    h["key"]: h["value"]
    for rule in vercel["headers"] for h in rule["headers"]
    if rule["source"] == "/(.*)"
  }
  for name, value in SECURITY_HEADERS.items():
    assert vercel_headers.get(name) == value, name
