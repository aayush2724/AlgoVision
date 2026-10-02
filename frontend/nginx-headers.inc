# Security headers for every nginx response. Included from each `location`
# because nginx drops inherited add_header lines the moment a location adds
# its own (Cache-Control, here).
#
# Keep the CSP identical to vercel.json and backend/app/security.py —
# backend/tests/test_security.py checks that the three strings match.
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header X-Frame-Options "DENY" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;
add_header Content-Security-Policy "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; script-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net 'sha256-V99skbXtDVAxWZSHXS2i4WXvtMsWc/EBx2i6b00xLDo=' 'sha256-YSGIfJf//vwC94PYVxEcfZ75M4ZB+ZUTjl9J3hLZp5w='; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; worker-src 'none'; manifest-src 'self'" always;
