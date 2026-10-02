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
  "script-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net "
  "'sha256-V99skbXtDVAxWZSHXS2i4WXvtMsWc/EBx2i6b00xLDo=' "
  "'sha256-YSGIfJf//vwC94PYVxEcfZ75M4ZB+ZUTjl9J3hLZp5w='; "
  # The templates use style="" attributes throughout; GSAP writes styles
  # via the CSSOM, which CSP does not block.
  "style-src 'self' 'unsafe-inline'; "
  # The paper-grain background is an inline SVG data URI.
  "img-src 'self' data:; "
  "font-src 'self'; "
  "connect-src 'self'; "
  "worker-src 'none'; "
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
