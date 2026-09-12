// GSAP clamps its delta when a frame runs long ("lag smoothing"), which stalls
// tweens on slow machines and in background tabs. Our reveals animate *from*
// opacity 0, so a stalled tween leaves content permanently invisible. Use real
// elapsed time instead.
if (typeof gsap !== 'undefined') gsap.ticker.lagSmoothing(0);

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

  let done = false;
  let handedOff = false;

  // Booting the app must never depend on an animation finishing.
  const handOff = () => {
    if (handedOff) return;
    handedOff = true;
    loader.style.display = 'none';
    if (callback) callback();
  };

  const finish = () => {
    if (done) return;
    done = true;
    clearInterval(phaseInterval);
    clearTimeout(safety);
    bar.style.width = '100%';
    count.textContent = '100';
    if (typeof gsap !== 'undefined') {
      gsap.to(loader, { opacity: 0, duration: 0.3, onComplete: handOff });
      setTimeout(handOff, 700);   // fade is cosmetic; the handoff is not
    } else {
      handOff();
    }
  };

  // Safety net: requestAnimationFrame is throttled in background tabs and on
  // slow machines, and GSAP's lag smoothing stalls the tween when frames run
  // long. Never let the intro trap a student behind the loader.
  const safety = setTimeout(finish, 2600);

  gsap.to({ val: 0 }, {
    val: 100,
    duration: 1.5,
    ease: "power2.inOut",
    onUpdate: function() {
      if (done) return;
      const v = Math.floor(this.targets()[0].val);
      bar.style.width = v + "%";
      count.textContent = v.toString().padStart(3, '0');
    },
    onComplete: finish,
  });
}

// Entry reveal is CSS-driven on purpose — see the .av-reveal note in main.css.
// A stalled JS tween used to leave whole pages invisible.
export function revealView(el) {
  if (!el) return;
  const targets = Array.from(el.querySelectorAll(
    'h1, h2, p, .panel, .world-card, .a2z-card, .act-card, .btn, .eyebrow'));
  if (!targets.length) return;

  // Total stagger stays under ~0.6s however many cards there are
  const step = Math.min(30, 600 / targets.length);

  targets.forEach((t, i) => {
    t.classList.remove('av-reveal');
    t.style.animationDelay = `${Math.round(i * step)}ms`;
    // Restart the animation even if the class was just removed
    void t.offsetWidth;
    t.classList.add('av-reveal');
  });

  // Drop the class once it has played so later layout work isn't affected
  setTimeout(() => targets.forEach(t => {
    t.classList.remove('av-reveal');
    t.style.removeProperty('animation-delay');
  }), 1400);
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
