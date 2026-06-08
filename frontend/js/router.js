import { PAGES, ROUTE_THEME } from './pages.js';
import { pageTransition, revealView, magnetize, tiltCards } from './animations.js';

export function initRouter({ scene }) {
  const app = document.getElementById('app');
  const navLinks = document.getElementById('nav-links');

  async function handleRoute(isInitial = false) {
    const hash = window.location.hash || '#/';
    const route = PAGES[hash] ? hash : '/404';
    const page = PAGES[route];

    const render = () => {
      document.title = page.title;
      app.innerHTML = page.html();
      
      // Update Active Nav
      document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === hash);
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
