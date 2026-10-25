"""Response headers shared by every way the frontend is served.

The static site is served three ways — Vercel (production), nginx (Docker)
and this FastAPI app (start-dev.sh). The headers have to agree or a page
that works in one deployment breaks in another, so the single source of
truth is here and tests/test_security.py checks vercel.json and the nginx
include against it.

When index.html's inline scripts change, the two sha256 values in CSP must
be recomputed (see tools/csp_hashes.py) and updated in all three places.
"""

CSP = (
  "default-src 'self'; "
  "base-uri 'self'; "
  "object-src 'none'; "
  "frame-ancestors 'none'; "
  "form-action 'self'; "
  # GSAP comes from cdnjs, three.js from jsDelivr; the two hashes cover the
  # import map and the tiny API-origin script inlined in index.html.
  "script-src 'self' 'wasm-unsafe-eval' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net "
  "'sha256-V99skbXtDVAxWZSHXS2i4WXvtMsWc/EBx2i6b00xLDo=' "
  "'sha256-YSGIfJf//vwC94PYVxEcfZ75M4ZB+ZUTjl9J3hLZp5w='; "
  # The templates use style="" attributes throughout; GSAP writes styles
  # via the CSSOM, which CSP does not block.
  "style-src 'self' 'unsafe-inline'; "
  # The paper-grain background is an inline SVG data URI.
  "img-src 'self' data:; "
  "font-src 'self'; "
  # The Practice page's dry run runs the student's Python in a same-origin
  # worker (js/dryrun.worker.js) on Pyodide, fetched from jsDelivr and compiled
  # as WebAssembly: hence the jsDelivr connect, worker-src 'self' and
  # 'wasm-unsafe-eval' above (WebAssembly only; JS eval stays blocked).
  "connect-src 'self' https://cdn.jsdelivr.net; "
  "worker-src 'self'; "
  "manifest-src 'self'"
)

SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "DENY",
  "Permissions-Policy": (
    "camera=(), microphone=(), geolocation=(), payment=(), usb=(), "
    "interest-cohort=()"
  ),
  "Cross-Origin-Opener-Policy": "same-origin",
  "Content-Security-Policy": CSP,
}

# FastAPI's /docs page (dev only; main.py switches it off outside ENV=dev) is
# Swagger UI: swagger-ui-bundle.js and swagger-ui.css from jsDelivr plus an
# inline bootstrap script that FastAPI generates, so it cannot be hash-pinned
# the way index.html's two scripts are. The site CSP above blocks that inline
# script and the stylesheet, which left /docs a blank white page. This policy
# is sent on /docs and /docs/oauth2-redirect only; the app and the API keep
# the strict one.
DOCS_CSP = (
  "default-src 'self'; "
  "base-uri 'self'; "
  "object-src 'none'; "
  "frame-ancestors 'none'; "
  "form-action 'self'; "
  "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
  "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
  # Swagger UI's icons are data URIs; the favicon is FastAPI's own.
  "img-src 'self' data: https://fastapi.tiangolo.com; "
  "font-src 'self'; "
  # /openapi.json and "Try it out" calls are same-origin.
  "connect-src 'self'"
)
