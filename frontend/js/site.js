// Site-wide facts that the HTML shell, the router and the legal pages share.
// Everything here is public. Keep it in sync with the static copies in
// index.html (meta tags), robots.txt and sitemap.xml when the origin changes.
export const SITE = {
  name: 'AlgoVision',
  // Canonical origin, no trailing slash. Change this if the site moves to a
  // custom domain — and update index.html, robots.txt and sitemap.xml too.
  url: 'https://algo-vision-vert.vercel.app',
  tagline: 'See the algorithm before the code',
  description:
    'AlgoVision teaches data structures and algorithms through real-world ' +
    'metaphors and live step-by-step traces of your own input — no sign-up, ' +
    'free, built for colleges and self-learners.',
  // Public source — also the real support channel (issues) until an email
  // address is configured below.
  repo: 'https://github.com/aayush2724/AlgoVision',

  // ── Values the site owner must provide ─────────────────────────────────
  // Leave empty and the UI falls back to the GitHub issues link. Never put a
  // made-up address here.
  contactEmail: '',              // TODO(owner): a monitored address, e.g. hello@example.com
  // Who operates the site, as it should appear in the privacy policy and
  // terms ("operated by …"). Empty → "the AlgoVision maintainers".
  operator: '',                  // TODO(owner): legal name of the person or organisation
  // Date the legal pages were last reviewed (ISO). Bump when you edit them.
  legalUpdated: '2026-10-02',
};

export function operatorName() {
  return SITE.operator || 'the AlgoVision maintainers';
}

export function contactHref() {
  return SITE.contactEmail ? `mailto:${SITE.contactEmail}` : `${SITE.repo}/issues`;
}

export function contactLabel() {
  return SITE.contactEmail ? SITE.contactEmail : 'open an issue on GitHub';
}
