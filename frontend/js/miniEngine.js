// ── THE DESK SCREEN ────────────────────────────────────────────────────────
//
// The compact Experience that plays on the monitor when you click a keycap.
//
// It deliberately reuses the real `mountEngine` rather than reimplementing a
// cut-down tracer: that is what makes every algorithm in the catalog work here
// for free, and keeps the screen honest — what plays is the same trace the
// full Experience page runs.
//
// mountEngine reaches for a fixed set of element ids, so the markup below
// provides all of them. The ones a screen this size has no room for are
// present but hidden (`.mini-off`) rather than missing, because engine.js does
// not guard every lookup and an absent node would throw mid-trace.

import { ALGORITHMS } from './data.js';

const SHELL = (algo) => `
  <div class="mini-bezel">
    <div class="mini-head">
      <span class="mini-title">${algo.name}</span>
      <span class="chip chip-cx">${algo.complexity}</span>
      <span class="mini-spacer"></span>
      <div id="engine-status" class="engine-status-pill mini-status">Idle</div>
      <button class="mini-close" type="button" aria-label="Back to the keyboard">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <path d="M6 6l12 12M18 6L6 18"></path>
        </svg>
      </button>
    </div>

    <div id="engine-view" class="mini-stage">
      <svg id="engine-svg" viewBox="0 0 760 280"></svg>
    </div>

    <div class="mini-transport">
      <button id="prev-btn" class="transport-btn" aria-label="Previous step" disabled>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"></path></svg>
      </button>
      <button id="play-btn" class="transport-btn primary" aria-label="Play" disabled>
        <svg class="icon-play" width="10" height="10" viewBox="0 0 24 24" fill="currentColor"
             aria-hidden="true"><path d="M8 5v14l11-7z"></path></svg>
        <svg class="icon-pause" width="10" height="10" viewBox="0 0 24 24" fill="currentColor"
             aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"></path></svg>
      </button>
      <button id="step-btn" class="transport-btn" aria-label="Next step" disabled>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M9 18l6-6-6-6"></path></svg>
      </button>
      <div id="scrub-row" class="transport-scrub" style="display:none;">
        <input type="range" id="step-slider" min="0" max="0" value="0" aria-label="Step">
      </div>
      <span id="step-counter" class="transport-count"></span>
      <button id="run-btn" class="btn btn-primary mini-run">▶ Run</button>
    </div>

    <div class="mini-narration"><div id="engine-note"></div></div>

    <div class="mini-foot">
      <div id="counter-panel" class="counters" style="display:none;"></div>
      <span class="mini-spacer"></span>
      <a class="btn mini-open" href="#/experience?algo=${algo.id}">Open full Experience →</a>
    </div>
  </div>

  <!-- Present for mountEngine, deliberately not shown on a screen this size. -->
  <div class="mini-off">
    <div id="engine-panel"></div>
    <div id="scene-hook"></div>
    <div id="array-controls"><input id="array-input"><span id="array-hint"></span>
      <span id="target-wrap"><span id="target-label"></span><input id="target-input"></span></div>
    <div id="graph-controls"><select id="preset-select"></select><select id="start-select"></select>
      <span id="graph-stats"></span><span id="graph-error"></span></div>
    <select id="speed-select"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select>
    <button id="reset-btn"></button><button id="challenge-btn"></button>
    <span id="combo-chip"></span>
    <div id="complexity-card"><div id="complexity-rows"></div><p id="complexity-live"></p></div>
    <button id="explain-btn"></button><div id="explanation-box"></div>
    <select id="level-select"><option value="beginner" selected>beginner</option></select>
    <div id="whatif-controls"></div>
    <button id="compare-btn"></button>
    <div id="compare-panel">
      <button id="compare-prev"></button><button id="compare-play"></button><button id="compare-next"></button>
      <span id="compare-step-label"></span><input type="range" id="compare-slider" min="0" max="0">
      <div id="compare-grid">
        <select id="compare-pick-a"></select><span id="compare-total-a"></span>
        <svg id="compare-svg-a"></svg><div id="compare-note-a"></div><div id="compare-counts-a"></div>
        <select id="compare-pick-b"></select><span id="compare-total-b"></span>
        <svg id="compare-svg-b"></svg><div id="compare-note-b"></div><div id="compare-counts-b"></div>
      </div>
      <p id="compare-verdict"></p>
    </div>
  </div>
`;

export function mountMiniEngine(host, algo, onClose) {
  const entry = ALGORITHMS.find(a => a.id === algo.id) || algo;
  host.innerHTML = SHELL(entry);
  host.classList.add('on');

  host.querySelector('.mini-close')?.addEventListener('click', (e) => {
    e.stopPropagation();
    onClose?.();
  });

  // Clicks inside the panel must not reach the canvas underneath, or the
  // raycaster would read them as another keycap click.
  const swallow = (e) => e.stopPropagation();
  host.addEventListener('click', swallow);

  let autorun = 0;
  let disposed = false;

  import('./engine.js').then(m => {
    if (disposed || !document.body.contains(host)) return;
    m.mountEngine(host, entry.id);
    // A screen sitting there saying "Idle" reads as broken. Start the trace on
    // arrival — this is a display, not a form to fill in.
    autorun = setTimeout(() => {
      if (!disposed) host.querySelector('#run-btn')?.click();
    }, 420);
  }).catch(e => console.warn('Mini engine failed to mount:', e));

  return {
    dispose() {
      disposed = true;
      clearTimeout(autorun);
      host.removeEventListener('click', swallow);
    },
  };
}
