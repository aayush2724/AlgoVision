export function initCursor() {
  const cursor = document.getElementById('cursor');
  if (!cursor || matchMedia('(pointer: coarse)').matches) return;

  window.addEventListener('mousemove', (e) => {
    gsap.to(cursor, { x: e.clientX - 20, y: e.clientY - 20, duration: 0.1 });
  });
}

export function playLoader(callback) {
  const bar = document.getElementById('loader-bar');
  const count = document.getElementById('loader-count');
  const phases = document.getElementById('loader-phases');
  const loader = document.getElementById('loader');
  
  const PHASE_LIST = [
    "CALIBRATING GRID", "PLOTTING NODES", "SNAPPING EDGES", 
    "RENDERING BUILDS", "READY TO PLAY"
  ];

  let pIdx = 0;
  const phaseInterval = setInterval(() => {
    phases.textContent = PHASE_LIST[pIdx];
    pIdx = (pIdx + 1) % PHASE_LIST.length;
  }, 100);

  gsap.to({ val: 0 }, {
    val: 100,
    duration: 1.5,
    ease: "power2.inOut",
    onUpdate: function() {
      const v = Math.floor(this.targets()[0].val);
      bar.style.width = v + "%";
      count.textContent = v.toString().padStart(3, '0');
    },
    onComplete: () => {
      clearInterval(phaseInterval);
      gsap.to(loader, { opacity: 0, duration: 0.3, onComplete: () => {
        loader.style.display = 'none';
        if (callback) callback();
      }});
    }
  });
}

export function revealView(el) {
  if (!el) return;
  const targets = Array.from(el.querySelectorAll('h1, h2, p, .panel, .world-card, .a2z-card, .act-card, .btn, .eyebrow'));
  if (!targets.length) return;
  gsap.from(targets, {
    y: 24,
    opacity: 0,
    duration: 0.5,
    stagger: 0.06,
    ease: "power3.out",
    clearProps: "all"
  });
}

export async function pageTransition(render) {
  const veil = document.createElement('div');
  veil.style.position = 'fixed';
  veil.style.inset = '0';
  veil.style.background = 'var(--bg1)';
  veil.style.borderBottom = '2px solid var(--c)';
  veil.style.zIndex = '12000';
  veil.style.transform = 'translateY(100%)';
  document.body.appendChild(veil);

  const tl = gsap.timeline();
  await tl.to(veil, { translateY: '0%', duration: 0.4, ease: "power2.in" });
  
  render();
  window.scrollTo(0, 0);

  await tl.to(veil, { translateY: '-100%', duration: 0.4, ease: "power2.out" });
  veil.remove();
}

export function magnetize() {
  document.querySelectorAll('.btn, .nav-link').forEach(el => {
    el.addEventListener('mousemove', (e) => {
      const { left, top, width, height } = el.getBoundingClientRect();
      const x = (e.clientX - (left + width / 2)) * 0.3;
      const y = (e.clientY - (top + height / 2)) * 0.3;
      gsap.to(el, { x, y, duration: 0.3 });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { x: 0, y: 0, duration: 0.5, ease: "elastic.out(1, 0.3)" });
    });
  });
}

export function tiltCards() {
  document.querySelectorAll('.panel-glow').forEach(el => {
    el.addEventListener('mousemove', (e) => {
      const { left, top, width, height } = el.getBoundingClientRect();
      const x = (e.clientX - (left + width / 2)) / (width / 2);
      const y = (e.clientY - (top + height / 2)) / (height / 2);
      gsap.to(el, {
        rotationY: x * 5,
        rotationX: -y * 5,
        duration: 0.1,
        transformPerspective: 1000
      });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { rotationY: 0, rotationX: 0, duration: 0.5 });
    });
  });
}

export function splitWords() {}
