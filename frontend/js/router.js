import { PAGES, ROUTE_THEME } from './pages.js';
import { pageTransition, revealView, magnetize, tiltCards } from './animations.js';

export function initRouter({ scene }) {
  const app = document.getElementById('app');

  async function handleRoute(isInitial = false) {
    let raw = window.location.hash;

    // On first load, if no hash, default to #/
    if (isInitial && (!raw || raw === "" || raw === "#")) {
      window.location.hash = "#/";
      raw = "#/";
    }

    // Strip query strings
    let normalized = raw.split('?')[0];

    // Normalize home/empty hash
    if (normalized === "" || normalized === "#" || normalized === "#/") {
      normalized = "#/";
    }

    const route = normalized;
    const page = PAGES[route] || PAGES["#/404"];

    const render = () => {
      document.title = page.title;
      app.innerHTML = page.html();
      
      // Update Active Nav
      document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        link.classList.toggle('active', href === route);
      });

      // Update Scene Theme
      if (scene) scene.setTheme(ROUTE_THEME[route] || 'default');

      // Mount Page Logic
      if (page.mount) page.mount(app);

      // Re-init animations
      revealView(app);
      magnetize();
      tiltCards();
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
