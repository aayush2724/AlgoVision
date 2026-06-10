import { NAV } from './data.js';
import { initScene } from './scene.js';
import { initCursor, playLoader } from './animations.js';
import { initRouter } from './router.js';

function buildNav() {
  const navLinks = document.getElementById('nav-links');
  navLinks.innerHTML = NAV.map(link => `
    <a href="${link.hash}" class="nav-link">${link.label}</a>
  `).join('') + `
    <a href="#/experience" class="btn btn-primary" style="margin-left: 1rem;">PLAY ▶</a>
  `;
}

function initVizzy() {
  const container = document.createElement('div');
  container.className = 'vizzy-container';
  container.innerHTML = `<div id="vizzy-bubble" class="vizzy-bubble"></div>`;
  document.body.appendChild(container);

  const bubble = document.getElementById('vizzy-bubble');

  window.addEventListener('hashchange', () => {
    const route = window.location.hash;
    const tips = {
      explore:    'EXPLORE: Select an algorithm world.',
      experience: 'EXPERIENCE: Watch the algorithm run live.',
      a2z:        'A2Z: Your mastery roadmap.',
      practice:   'PRACTICE: Paste code — find bugs.',
      today:      'TODAY: 60-second insights.',
      journey:    'JOURNEY: Track your progress.',
      realworld:  'REALWORLD: Algorithms in the wild.'
    };
    const key = Object.keys(tips).find(k => route.includes(k));
    bubble.textContent = key ? tips[key] : 'SYSTEM READY.';
    bubble.classList.add('show');
    setTimeout(() => bubble.classList.remove('show'), 4000);
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

  // Close menu when any link is clicked
  document.addEventListener('click', (e) => {
    if (e.target.closest('.nav-link') || e.target.closest('.btn')) {
      if (window.innerWidth <= 860) {
        navToggle.classList.remove('open');
        navLinks.classList.remove('open');
      }
    }
  });
}

async function start() {
  try {
    console.log("AlgoVision Booting...");
    
    // 1. Build Static UI Parts
    buildNav();
    initMobileMenu();
    initCursor();
    initVizzy();

    // 2. Init Three.js Scene
    const canvas = document.getElementById('bg-canvas');
    let scene = null;
    try {
      if (canvas) {
        scene = initScene(canvas);
      }
    } catch (e) {
      console.warn("Scene init failed:", e);
    }

    // 3. Play Intro Loader
    playLoader(() => {
      console.log("Loader Complete. Initializing Router...");
      // 4. Init Router
      initRouter({ scene });
    });

  } catch (err) {
    console.error("Critical Boot Error:", err);
    const loaderPhases = document.getElementById('loader-phases');
    if (loaderPhases) {
      loaderPhases.textContent = "BOOT ERROR: CHECK CONSOLE";
      loaderPhases.style.color = "#ff5f5f";
    }
  }
}

// Start when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', start);
} else {
  start();
}
