import { NAV } from './data.js';
import { initScene } from './scene.js';
import { initCursor, playLoader } from './animations.js';
import { initRouter } from './router.js';

function buildNav() {
  const navLinks = document.getElementById('nav-links');
  navLinks.innerHTML = NAV.map(link => `
    <a href="${link.hash}" class="nav-link" data-magnet>${link.label}</a>
  `).join('');
}

function initMobileMenu() {
  const toggle = document.getElementById('nav-toggle');
  const nav = document.querySelector('.nav');
  
  toggle.addEventListener('click', () => {
    nav.classList.toggle('open');
  });

  // Close menu on link click
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('nav-link')) {
      nav.classList.remove('open');
    }
  });
}

async function start() {
  try {
    // 1. Build Static UI Parts
    buildNav();
    initMobileMenu();
    initCursor();

    // 2. Init Three.js Scene
    const canvas = document.getElementById('bg-canvas');
    let scene = null;
    try {
      scene = initScene(canvas);
    } catch (e) {
      console.warn("WebGL not supported or scene init failed. Proceeding without aurora.");
    }

    // 3. Play Intro Loader
    playLoader(() => {
      // 4. Init Router (starts rendering first page)
      initRouter({ scene });
    });

  } catch (err) {
    console.error("Critical Boot Error:", err);
    document.body.innerHTML = `<div style="padding: 2rem; color: white;"><h1>Something went wrong.</h1><p>${err.message}</p></div>`;
  }
}

// Start when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', start);
} else {
  start();
}
