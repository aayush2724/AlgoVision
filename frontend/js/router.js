import { PAGES, ROUTE_THEME } from './pages.js';
import { pageTransition, revealView, magnetize, tiltCards } from './animations.js';
import { SITE } from './site.js';

// Two URL shapes reach the app. Internally it navigates by hash (#/explore);
// the sitemap, social shares and typed addresses use plain paths (/explore).
// Both open the same page: on entry the path is folded into the hash so one
// shape exists from then on, and the canonical URL always points at the path.
function hashFromPath() {
  const path = location.pathname
    .replace(/\/index\.html$/, '')
    .replace(/\/+$/, '');
  return path ? `#${path}${location.search}` : null;
}

function setMeta(selector, attr, value) {
  const el = document.head.querySelector(selector);
  if (el) el.setAttribute(attr, value);
}

function resolve(value, params) {
  return typeof value === 'function' ? value(params) : value;
}

// Title, description, canonical and the social tags follow the page. They
// are static in index.html for the home page; every other page sets its own.
function applyMeta(routeKey, page, params) {
  const title = resolve(page.title, params) || SITE.name;
  const description = resolve(page.description, params) || SITE.description;
  const path = routeKey === '#/' ? '/' : routeKey.slice(1);
  const query = params.toString();
  const canonical = `${SITE.url}${path}${query ? `?${query}` : ''}`;

  document.title = title;
  setMeta('meta[name="description"]', 'content', description);
  setMeta('link[rel="canonical"]', 'href', canonical);
  setMeta('meta[name="robots"]', 'content', page.noindex ? 'noindex, follow' : 'index, follow');
  setMeta('meta[property="og:title"]', 'content', title);
  setMeta('meta[property="og:description"]', 'content', description);
  setMeta('meta[property="og:url"]', 'content', canonical);
  setMeta('meta[name="twitter:title"]', 'content', title);
  setMeta('meta[name="twitter:description"]', 'content', description);
  return title;
}

function announce(text) {
  const el = document.getElementById('route-announcer');
  if (!el) return;
  el.textContent = '';
  // A repeated identical string is not re-announced; clear first.
  requestAnimationFrame(() => { el.textContent = text; });
}

function mountFailed(app, err) {
  console.error('Page failed to mount:', err);
  app.insertAdjacentHTML('afterbegin', `
    <div class="page-notice is-error" role="alert">
      <strong>This page hit a problem while loading.</strong>
      <span>Reloading usually fixes it. If it keeps happening, the rest of the site still works.</span>
      <button type="button" class="btn" data-reload>Reload page</button>
      <a href="#/explore">Browse algorithms →</a>
    </div>`);
  app.querySelector('[data-reload]')?.addEventListener('click', () => location.reload());
}

export function initRouter({ scene }) {
  const app = document.getElementById('app');

  async function handleRoute(isInitial = false) {
    let raw = window.location.hash;

    if (isInitial) {
      if (!raw || raw === '#') {
        // /explore?x → /#/explore?x, or nothing at all → /#/. replaceState
        // keeps history clean and does not fire hashchange (which would
        // render the page twice).
        raw = hashFromPath() || '#/';
        history.replaceState(null, '', `/${raw}`);
      } else if (location.pathname !== '/') {
        // /explore#/a2z — the hash wins; tidy the path so relative URLs and
        // the canonical tag agree with what is shown.
        history.replaceState(null, '', `/${raw}`);
      }
    }

    // Strip query strings and extract params
    const [path, query] = raw.split('?');
    const params = new URLSearchParams(query || "");
    const normalized = (!path || path === "" || path === "#" || path === "#/") ? "#/" : path;

    const route = normalized;
    const known = Object.prototype.hasOwnProperty.call(PAGES, route);
    const routeKey = known ? route : '#/404';
    const page = PAGES[routeKey];

    const render = () => {
      // Dispose any mounted 3D viz scene before wiping the DOM,
      // otherwise its WebGL context and animation loop leak.
      const viz = app.querySelector('#viz-inner');
      if (viz) {
        if (viz._vizAutoInterval) { clearInterval(viz._vizAutoInterval); viz._vizAutoInterval = null; }
        if (viz._vizDispose) { viz._vizDispose(); viz._vizDispose = null; }
      }

      const title = applyMeta(routeKey, page, params);
      app.innerHTML = page.html(params);

      // Update Active Nav
      document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        link.classList.toggle('active', href === route);
        if (href === route) link.setAttribute('aria-current', 'page');
        else link.removeAttribute('aria-current');
      });

      // Update Scene Theme
      if (scene) scene.setTheme(ROUTE_THEME[route] || 'default');

      // Mount Page Logic. A throwing mount must not leave a half-wired page
      // with nothing to say about it.
      if (page.mount) {
        try { page.mount(app, params); }
        catch (err) { mountFailed(app, err); }
      }

      // Re-init animations
      revealView(app);
      magnetize();
      tiltCards();

      // Keyboard and screen-reader users land on the new page's content,
      // not wherever focus was on the old one.
      if (!isInitial) {
        app.focus({ preventScroll: true });
        announce(title);
      }
    };

    if (isInitial) {
      render();
    } else {
      await pageTransition(render);
    }
  }

  window.addEventListener('hashchange', () => handleRoute(false));

  // Initial route
  handleRoute(true);

  return {
    navigate: (hash) => {
      window.location.hash = hash;
    }
  };
}
