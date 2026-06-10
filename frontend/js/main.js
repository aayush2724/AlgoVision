import { NAV } from './data.js';
import { initScene } from './scene.js';
import { initCursor, playLoader } from './animations.js';
import { initRouter } from './router.js';

function buildNav() {
  const navLinks = document.getElementById('nav-links');
  navLinks.innerHTML = NAV.map(link => `
    <a href="${link.hash}" class="nav-link">${link.label}</a>
  `).join('') + `
    <a href="#/experience" class="btn btn-primary nav-play">▶ Play</a>
  `;
}

function initVizzy() {
  const container = document.createElement('div');
  container.className = 'vizzy-container';
  container.innerHTML = `<div id="vizzy-bubble" class="vizzy-bubble"></div>`;
  document.body.appendChild(container);

  const bubble = document.getElementById('vizzy-bubble');
  const tips = {
    explore:    'Select an algorithm world to explore.',
    experience: 'Watch the algorithm run live, step by step.',
    a2z:        'Your structured mastery roadmap.',
    practice:   'Paste code — the AI finds your bugs.',
    today:      '60-second algorithm insights.',
    family:     'See how algorithms relate to each other.',
  };

  window.addEventListener('hashchange', () => {
    const route = window.location.hash;
    const key = Object.keys(tips).find(k => route.includes(k));
    bubble.textContent = key ? tips[key] : '';
    if (key) {
      bubble.classList.add('show');
      setTimeout(() => bubble.classList.remove('show'), 3500);
    }
  });
}

function initMobileMenu() {
  const navLinks = document.getElementById('nav-links');
  const navToggle = document.getElementById('nav-toggle');

  if (navToggle) {
    navToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (window.innerWidth <= 860) {
        navToggle.classList.toggle('open');
        navLinks.classList.toggle('open');
      }
    });
  }

  document.addEventListener('click', (e) => {
    if (e.target.closest('.nav-link') || e.target.closest('.btn')) {
      if (window.innerWidth <= 860 && navToggle) {
        navToggle.classList.remove('open');
        navLinks.classList.remove('open');
      }
    }
  });
}

async function start() {
  try {
    buildNav();
    initMobileMenu();
    initCursor();
    initVizzy();

    const canvas = document.getElementById('bg-canvas');
    let scene = null;
    try {
      if (canvas) scene = initScene(canvas);
    } catch (e) {
      console.warn("Scene init failed:", e);
    }

    playLoader(() => {
      initRouter({ scene });
    });

  } catch (err) {
    console.error("Boot Error:", err);
    const phases = document.getElementById('loader-phases');
    if (phases) { phases.textContent = "BOOT ERROR"; phases.style.color = "#ff5f5f"; }
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', start);
} else {
  start();
}
