export function initCursor() {
  const cursor = document.getElementById('cursor');
  const ring = cursor.querySelector('.cursor-ring');
  
  if (!cursor || matchMedia('(pointer: coarse)').matches) return;

  window.addEventListener('mousemove', (e) => {
    gsap.to(cursor, { x: e.clientX, y: e.clientY, duration: 0.1 });
    gsap.to(ring, { x: 0, y: 0, duration: 0.2 });
  });

  document.querySelectorAll('a, button, .tilt').forEach(el => {
    el.addEventListener('mouseenter', () => {
      gsap.to(ring, { width: 60, height: 60, duration: 0.3 });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(ring, { width: 32, height: 32, duration: 0.3 });
    });
  });
}

export function playLoader(callback) {
  const tl = gsap.timeline({ onComplete: callback });
  const count = document.getElementById('loader-count');
  const bar = document.getElementById('loader-bar');
  const loader = document.getElementById('loader');

  tl.to(bar, { width: '100%', duration: 2, ease: "power2.inOut" });
  tl.to({ val: 0 }, {
    val: 100,
    duration: 2,
    ease: "power2.inOut",
    onUpdate: function() {
      count.textContent = Math.floor(this.targets()[0].val).toString().padStart(3, '0');
    }
  }, 0);

  tl.to(loader, { yPercent: -100, duration: 1, ease: "expo.inOut" });
}

export function revealView(view) {
  const reveals = view.querySelectorAll('[data-reveal]');
  const scrolls = view.querySelectorAll('[data-scroll]');

  gsap.fromTo(reveals, 
    { opacity: 0, y: 30 },
    { opacity: 1, y: 0, duration: 1, stagger: 0.1, ease: "power3.out" }
  );

  scrolls.forEach(el => {
    gsap.fromTo(el,
      { opacity: 0, y: 50 },
      { 
        opacity: 1, y: 0, duration: 1, ease: "power3.out",
        scrollTrigger: {
          trigger: el,
          start: "top 85%",
        }
      }
    );
  });
}

export async function pageTransition(action) {
  const veil = document.createElement('div');
  veil.id = 'page-veil';
  document.body.appendChild(veil);

  const tl = gsap.timeline();
  await tl.to(veil, { yPercent: -100, duration: 0.6, ease: "expo.inOut" });
  
  action();
  window.scrollTo(0, 0);

  await tl.to(veil, { yPercent: -200, duration: 0.6, ease: "expo.inOut" });
  veil.remove();
}

export function magnetize() {
  const magnets = document.querySelectorAll('[data-magnet]');
  magnets.forEach(el => {
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      gsap.to(el, { x: x * 0.3, y: y * 0.3, duration: 0.3 });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { x: 0, y: 0, duration: 0.5, ease: "elastic.out(1, 0.3)" });
    });
  });
}

export function tiltCards() {
  const cards = document.querySelectorAll('.tilt');
  cards.forEach(el => {
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      gsap.to(el, {
        rotationY: x * 10,
        rotationX: -y * 10,
        transformPerspective: 1000,
        duration: 0.1
      });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { rotationY: 0, rotationX: 0, duration: 0.5 });
    });
  });
}

export function splitWords(el) {
  if (!el) return;
  const text = el.textContent;
  el.innerHTML = text.split(' ').map(word => `<span>${word}</span>`).join(' ');
  const spans = el.querySelectorAll('span');
  gsap.from(spans, {
    yPercent: 100,
    opacity: 0,
    stagger: 0.05,
    duration: 1,
    ease: "expo.out"
  });
}
