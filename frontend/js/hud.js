// Persistent game HUD: level badge + XP bar in the nav, toast stack for
// XP/achievement/level-up moments, and a lightweight confetti burst.

import * as Game from './game.js';

let xpFill, xpLabel, levelBadge;

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function refresh() {
  const s = Game.state();
  if (levelBadge) {
    levelBadge.textContent = `LV ${s.level}`;
    levelBadge.title = `${s.rank} — ${s.xp} XP`;
  }
  if (xpFill) xpFill.style.width = `${Math.max(4, s.pct)}%`;
  if (xpLabel) xpLabel.textContent = `${s.intoLevel}/${s.levelSpan}`;
}

function toast(icon, title, sub, cls = '') {
  const stack = document.getElementById('toast-stack');
  if (!stack) return;
  const t = el('div', `game-toast ${cls}`,
    `<span class="gt-icon">${icon}</span>
     <span class="gt-body"><strong>${title}</strong>${sub ? `<em>${sub}</em>` : ''}</span>`);
  stack.appendChild(t);
  requestAnimationFrame(() => t.classList.add('show'));
  setTimeout(() => {
    t.classList.remove('show');
    setTimeout(() => t.remove(), 400);
  }, 3400);
  // Keep the stack short
  while (stack.children.length > 4) stack.firstChild.remove();
}

function confetti() {
  const host = el('div', 'confetti-host');
  document.body.appendChild(host);
  const colors = ['#d4602c', '#e7ddc4', '#cfdee5', '#c94f22'];
  for (let i = 0; i < 36; i++) {
    const p = el('span', 'confetti-bit');
    p.style.left = `${8 + Math.random() * 84}vw`;
    p.style.background = colors[i % colors.length];
    p.style.animationDelay = `${Math.random() * 0.25}s`;
    p.style.animationDuration = `${0.9 + Math.random() * 0.9}s`;
    p.style.transform = `rotate(${Math.random() * 360}deg)`;
    host.appendChild(p);
  }
  setTimeout(() => host.remove(), 2400);
}

export function initHUD() {
  // Nav widget, injected before the burger toggle
  const nav = document.querySelector('.nav');
  if (nav && !document.getElementById('game-hud')) {
    const hud = el('div', '', '');
    hud.id = 'game-hud';
    hud.innerHTML = `
      <a href="#/journey" class="hud-inner" title="Open your profile">
        <span id="hud-level" class="hud-level">LV 1</span>
        <span class="hud-bar"><span id="hud-fill" class="hud-fill"></span></span>
        <span id="hud-xp" class="hud-xp"></span>
      </a>`;
    const toggle = nav.querySelector('.nav-toggle');
    nav.insertBefore(hud, toggle);
    levelBadge = hud.querySelector('#hud-level');
    xpFill = hud.querySelector('#hud-fill');
    xpLabel = hud.querySelector('#hud-xp');
  }

  if (!document.getElementById('toast-stack')) {
    const stack = el('div', '');
    stack.id = 'toast-stack';
    document.body.appendChild(stack);
  }

  addEventListener('av:xp', (e) => {
    const { amount, reason } = e.detail || {};
    if (amount > 0) toast('✦', `+${amount} XP`, reason || '', 'gt-xp');
    refresh();
  });
  addEventListener('av:levelup', (e) => {
    const { level, rank } = e.detail || {};
    toast('⬆', `Level ${level}!`, rank, 'gt-level');
    confetti();
    refresh();
  });
  addEventListener('av:achievement', (e) => {
    const a = e.detail || {};
    toast(a.icon || '🏅', 'Achievement unlocked', a.name || '', 'gt-achv');
    confetti();
  });

  refresh();
  // Daily bonus (fires its own toast through the events above)
  Game.touchDailyVisit();
  Game.checkAchievements();
}
