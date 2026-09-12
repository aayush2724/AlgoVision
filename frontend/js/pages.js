import * as DATA from './data.js';
import * as P from './progress.js';

function clientDetect(text) {
  const t = text.toLowerCase();
  if (t.includes('heappush') || t.includes('heappop') ||
      t.includes('dijkstra') || t.includes('shortest'))     return 'dijkstra';
  if (t.includes('deque') || t.includes('bfs') ||
      t.includes('breadth'))                                 return 'bfs';
  if (t.includes('dfs') || t.includes('depth first') ||
      t.includes('backtrack'))                               return 'dfs';
  if (t.includes('binary search') || t.includes('bisect') ||
      (t.includes('low') && t.includes('high') && t.includes('mid')))
                                                             return 'binary_search';
  if (t.includes('dp[') || t.includes('memo') ||
      t.includes('lru_cache'))                               return 'dynamic_programming';
  if (t.includes('merge') || t.includes('pivot') ||
      t.includes('sort'))                                    return 'sorting';
  return 'dijkstra';
}

export const ROUTE_THEME = {
  "#/": "default", "#/explore": "default", "#/experience": "default",
  "#/family": "default", "#/a2z": "default", "#/a2z-problem": "default",
  "#/today": "default", "#/practice": "default",
  "#/journey": "default", "#/realworld": "default"
};

function renderWorldCard(world) {
  return `
    <a href="#/experience?algo=${world.algo || 'dijkstra'}" class="world-card">
      <span class="world-card-complexity">${world.complexity}</span>
      <span class="world-card-emoji">${world.emoji}</span>
      <span class="world-card-metaphor">${world.metaphor}</span>
      <h3>${world.name}</h3>
      <p>${world.hook}</p>
      <div class="world-card-cta">Visualize <span style="margin-left:0.25rem;">→</span></div>
    </a>
  `;
}

export const PAGES = {
  "#/": {
    title: "AlgoVision · See the algorithm before the code",
    html: () => `
      <section class="hero hero-kbd">
        <div id="kbd-stage" class="kbd-stage"></div>
        <div class="kbd-corner kbd-tl">
          <span class="kbd-tiny-label">KEYS EXPLORED</span>
          <span id="kbd-count" class="kbd-count">0 / ${DATA.ALGORITHMS.length}</span>
        </div>
        <div class="kbd-corner kbd-tc">
          <span class="kbd-tc-brand">AlgoVision</span>
          <span class="kbd-tc-sub">A Display of Algorithms</span>
        </div>
        <div class="kbd-corner kbd-ml">
          <span class="kbd-tiny-label">NAVIGATION</span>
          <div class="kbd-legend"><span>DRAG</span><em>ROTATE</em></div>
          <div class="kbd-legend"><span>SCROLL</span><em>ZOOM</em></div>
          <div class="kbd-legend"><span>CLICK KEY</span><em>TRACE IT</em></div>
        </div>
        <div class="kbd-corner kbd-br">
          <a href="#/explore">ALL ALGORITHMS →</a>
          <a href="#/a2z">A2Z ROADMAP →</a>
        </div>
      </section>

      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">HOW IT WORKS</span>
        </div>
        <h2 style="margin-bottom:2rem; font-family:var(--font-display2); font-size:clamp(2rem,4vw,3.5rem); letter-spacing:0.04em;">THREE ACTS, ONE INSIGHT</h2>
        <div class="grid-3">
          ${DATA.ACTS.map((act, i) => `
            <div class="act-card">
              <span class="act-num">${String(i+1).padStart(2,'0')}</span>
              <h3 style="margin-bottom:0.6rem; font-family:var(--font-condensed); font-size:1.2rem; letter-spacing:0.06em; text-transform:uppercase;">${act.title}</h3>
              <p style="font-size:0.875rem;">${act.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <section>
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2rem; flex-wrap:wrap; gap:1rem;">
          <div>
            <div class="section-label" style="margin-bottom:0.5rem;">
              <span class="eyebrow" style="margin:0;">FEATURED WORLDS</span>
            </div>
            <h2 style="margin:0; font-family:var(--font-display2); font-size:clamp(1.8rem,3vw,2.8rem); letter-spacing:0.04em;">PICK YOUR ALGORITHM</h2>
          </div>
          <a href="#/explore" class="btn btn-ghost">View All →</a>
        </div>
        <div class="grid-3">
          ${DATA.WORLDS.slice(0, 3).map(world => renderWorldCard(world)).join('')}
        </div>
      </section>

      <section style="padding-bottom:6rem;">
        <div class="panel" style="max-width:680px; margin:0 auto; padding:3rem 2.5rem; border-top:3px solid var(--c);">
          <div class="section-label">
            <span class="eyebrow" style="margin:0;">QUICK START</span>
          </div>
          <h2 style="margin-bottom:0.75rem; font-family:var(--font-display2); font-size:clamp(1.8rem,3vw,2.5rem); letter-spacing:0.04em;">PASTE ANY DSA CODE</h2>
          <p style="margin:0 0 2rem;">AlgoVision detects the algorithm and launches the cinematic experience automatically.</p>
          <div class="paste-detect-panel">
            <div id="paste-detect-status" style="display:none; font-family:var(--font-mono);
              font-size:1rem; color:var(--c); margin-bottom:1rem; padding:0.6rem 1rem;
              border-left:3px solid var(--c); background:rgba(212, 96, 44,0.04);">
            </div>
            <textarea id="hero-paste-area"
              style="width:100%; height:130px; background:rgba(2,4,6,0.9); color:var(--c);
              font-family:var(--font-mono); font-size:1.1rem; padding:1rem;
              border:1px solid var(--panel-border); outline:none; resize:none;
              border-radius:0; transition:border-color 0.3s;"
              placeholder="def dijkstra(graph, start): ..."></textarea>
            <div style="display:flex; gap:0.75rem; margin-top:0.75rem;">
              <button id="hero-visualize-btn" class="btn btn-primary" style="flex:1;"><span>DETECT & VISUALIZE →</span></button>
              <button id="hero-clear-btn" class="btn btn-ghost">Clear</button>
            </div>
          </div>
        </div>
      </section>
    `,
    mount: (view) => {
      // ── The keyboard ──
      const stage = view.querySelector('#kbd-stage');
      const countEl = view.querySelector('#kbd-count');
      if (stage) {
        import('./keyboard3d.js').then(({ initKeyboard }) => {
          // Guard: user may have navigated away while the module loaded
          if (!document.body.contains(stage)) return;
          const kbd = initKeyboard(stage, {
            onCount: (n, total) => {
              if (countEl) countEl.textContent = `${n} / ${total}`;
            },
          });
          // Dispose with the page — hook into the router's DOM teardown
          const mo = new MutationObserver(() => {
            if (!document.body.contains(stage)) { kbd.dispose(); mo.disconnect(); }
          });
          mo.observe(document.getElementById('app'), { childList: true });
        }).catch(e => {
          console.warn('Keyboard unavailable:', e);
          stage.innerHTML = '<p style="padding:2rem;">3D not available on this device — <a href="#/explore" style="color:var(--c)">browse the algorithm index instead →</a></p>';
        });
      }

      const pasteArea    = view.querySelector('#hero-paste-area');
      const statusEl     = view.querySelector('#paste-detect-status');
      const visualizeBtn = view.querySelector('#hero-visualize-btn');
      const clearBtn     = view.querySelector('#hero-clear-btn');

      if (!pasteArea || !visualizeBtn) return;

      let detectedAlgo = null;
      let detectTimer  = null;

      pasteArea.addEventListener('input', () => {
        clearTimeout(detectTimer);
        const text = pasteArea.value.trim();
        if (text.length < 20) { statusEl.style.display = 'none'; detectedAlgo = null; return; }
        detectTimer = setTimeout(async () => {
          try {
            const { api } = await import('./api.js');
            const res  = await api.detect(text);
            detectedAlgo = res.algorithm;
            const conf  = Math.round((res.confidence || 0) * 100);
            const title = res.realworld?.title || '';
            statusEl.style.display = 'block';
            statusEl.innerHTML =
              `DETECTED: <strong style="color:var(--cAccentBright)">${res.algorithm.toUpperCase().replace(/_/g,' ')}</strong>` +
              (title ? `<span style="color:var(--cDim);margin:0 0.5rem;">—</span><em style="color:var(--cDim)">${title}</em>` : '') +
              `<span style="color:var(--cDim);margin-left:0.75rem;">(${conf}% confidence)</span>`;
          } catch {
            detectedAlgo = clientDetect(text);
            statusEl.style.display = 'block';
            statusEl.innerHTML =
              `DETECTED (OFFLINE): <strong style="color:var(--cAccentBright)">${detectedAlgo.toUpperCase().replace(/_/g,' ')}</strong>`;
          }
        }, 600);
      });

      visualizeBtn.addEventListener('click', async () => {
        const text = pasteArea.value.trim();
        if (!text) return;
        const btnLabel = visualizeBtn.querySelector('span');
        visualizeBtn.disabled = true;
        if (btnLabel) btnLabel.textContent = 'DETECTING...';
        try {
          if (detectedAlgo) { window.location.hash = `#/experience?algo=${detectedAlgo}`; return; }
          const { api } = await import('./api.js');
          const res = await api.detect(text);
          window.location.hash = `#/experience?algo=${res.algorithm}`;
        } catch {
          const fallback = clientDetect(text);
          window.location.hash = `#/experience?algo=${fallback}`;
        } finally {
          visualizeBtn.disabled = false;
          if (btnLabel) btnLabel.textContent = 'DETECT & VISUALIZE →';
        }
      });

      clearBtn?.addEventListener('click', () => {
        pasteArea.value = '';
        statusEl.style.display = 'none';
        detectedAlgo = null;
      });
    }
  },

  "#/explore": {
    title: "AlgoVision · Explore Algorithms",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">ALGORITHM INDEX</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,7vw,6rem); letter-spacing:0.04em; margin-bottom:0.5rem;">EVERY ALGORITHM</h1>
        <p style="margin-bottom:2rem;">All ${DATA.ALGORITHMS.length} trace live on your own input — pick one and watch it run, step by step.</p>

        <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:center; margin-bottom:2rem;">
          <input id="algo-search" type="search" placeholder="Search algorithms…" autocomplete="off"
            style="flex:1; min-width:220px; background:rgba(2,4,6,0.9); color:var(--c);
            font-family:var(--font-mono); font-size:1rem; padding:0.6rem 0.9rem;
            border:1px solid var(--panel-border); outline:none; border-radius:0;">
          <span id="algo-count" style="font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);"></span>
        </div>

        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:2.5rem;">
          ${DATA.ALGO_CATEGORIES.map(cat => `<button class="btn filter-btn" data-cat="${cat}">${cat}</button>`).join('')}
        </div>
        <div class="grid-3" id="algo-grid"></div>
        <p id="algo-empty" style="display:none; font-family:var(--font-mono); color:var(--cDim);">
          No algorithm matches that search.
        </p>
      </section>
    `,
    mount: (view) => {
      const grid = view.querySelector('#algo-grid');
      const search = view.querySelector('#algo-search');
      const countEl = view.querySelector('#algo-count');
      const emptyEl = view.querySelector('#algo-empty');
      const btns = view.querySelectorAll('.filter-btn');
      let cat = 'All';

      const card = (a) => `
        <a href="#/experience?algo=${a.id}" class="world-card">
          <span class="world-card-complexity">${a.complexity}</span>
          <span class="world-card-emoji">${a.emoji}</span>
          <span class="world-card-metaphor">${a.category}</span>
          <h3>${a.name}</h3>
          <p>${a.hook}</p>
          <div class="world-card-cta">Trace it <span style="margin-left:0.25rem;">→</span></div>
        </a>`;

      function render() {
        const q = (search?.value || '').trim().toLowerCase();
        const list = DATA.ALGORITHMS.filter(a =>
          (cat === 'All' || a.category === cat) &&
          (!q || a.name.toLowerCase().includes(q) || a.hook.toLowerCase().includes(q) ||
           a.category.toLowerCase().includes(q) || a.id.includes(q)));
        grid.innerHTML = list.map(card).join('');
        if (countEl) countEl.textContent = `${list.length} / ${DATA.ALGORITHMS.length} SHOWN`;
        if (emptyEl) emptyEl.style.display = list.length ? 'none' : 'block';
        import('./animations.js').then(m => m.revealView(grid));
      }

      const allBtn = view.querySelector('.filter-btn[data-cat="All"]');
      if (allBtn) allBtn.classList.add('active');
      btns.forEach(btn => {
        btn.addEventListener('click', () => {
          btns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          cat = btn.dataset.cat;
          render();
        });
      });
      search?.addEventListener('input', render);
      render();
    }
  },

  "#/experience": {
    title: "AlgoVision · Live Engine",
    html: (params) => {
      // Whitelist chars — this comes from the URL and lands in innerHTML.
      const algo = (params.get('algo') || 'dijkstra').replace(/[^a-zA-Z0-9_-]/g, '') || 'dijkstra';
      const displayName = algo.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      return `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">LIVE EXECUTION ENGINE</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:flex-end;
          gap:1rem; flex-wrap:wrap;">
          <h1 id="experience-title" style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em; margin-bottom:0;">${displayName.toUpperCase()}</h1>
          <label style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.6rem;
            font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);">
            SWITCH
            <select id="algo-switch" style="background:var(--bg1); border:1px solid var(--panel-border);
              color:var(--ink); font-family:var(--font-body); font-size:0.85rem;
              padding:0.45rem 0.7rem; border-radius:0; outline:none; max-width:260px;">
              ${DATA.ALGO_CATEGORIES.filter(c => c !== 'All').map(cat => `
                <optgroup label="${cat}">
                  ${DATA.ALGORITHMS.filter(a => a.category === cat).map(a =>
                    `<option value="${a.id}"${a.id === algo ? ' selected' : ''}>${a.emoji} ${a.name}</option>`
                  ).join('')}
                </optgroup>`).join('')}
            </select>
          </label>
        </div>

        <div id="scene-hook" style="display:none; font-family:var(--font-mono);
          font-size:1.05rem; color:var(--cDim); margin-bottom:2rem; padding:0.85rem 1.25rem;
          border-left:3px solid var(--c); background:rgba(212, 96, 44,0.04);">
        </div>

        <div id="array-controls" class="panel is-hidden" style="margin-bottom:1.5rem;
          border-top:2px solid var(--c);">
          <span class="eyebrow" style="margin-bottom:0.75rem;">YOUR DATA</span>
          <div style="display:flex; gap:0.75rem; flex-wrap:wrap; align-items:center;">
            <input id="array-input" type="text" spellcheck="false"
              placeholder="e.g. 7, 3, 9, 1"
              style="flex:1; min-width:220px; background:rgba(2,4,6,0.9); color:var(--c);
              font-family:var(--font-mono); font-size:1rem; padding:0.6rem 0.9rem;
              border:1px solid var(--panel-border); outline:none; border-radius:0;">
            <span id="target-wrap" style="display:none; align-items:center; gap:0.5rem;
              font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);">
              <span id="target-label">TARGET</span>
              <input id="target-input" type="text" inputmode="numeric"
                style="width:80px; background:rgba(2,4,6,0.9); color:var(--c);
                font-family:var(--font-mono); font-size:1rem; padding:0.6rem 0.9rem;
                border:1px solid var(--panel-border); outline:none; border-radius:0;">
            </span>
          </div>
          <div id="array-hint" style="margin-top:0.6rem; font-size:0.8rem;
            color:var(--inkDim); font-family:var(--font-body);"></div>
        </div>

        <div id="graph-controls" class="panel is-hidden" style="margin-bottom:1.5rem;
          border-top:2px solid var(--c);">
          <span class="eyebrow" style="margin-bottom:0.75rem;">YOUR GRAPH</span>
          <div style="display:flex; gap:1.25rem; flex-wrap:wrap; align-items:center;">
            <label style="display:flex; align-items:center; gap:0.5rem;
              font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);">
              PRESET
              <select id="preset-select" style="background:var(--bg1); border:1px solid var(--panel-border);
                color:var(--ink); font-family:var(--font-body); font-size:0.8rem; padding:0.35rem 0.6rem;
                border-radius:0; outline:none;">
                <option value="sample">City map</option>
                <option value="tree">Small tree</option>
                <option value="disconnected">Disconnected</option>
                <option value="clear">Empty (build your own)</option>
              </select>
            </label>
            <label style="display:flex; align-items:center; gap:0.5rem;
              font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);">
              START
              <select id="start-select" style="background:var(--bg1); border:1px solid var(--panel-border);
                color:var(--ink); font-family:var(--font-body); font-size:0.8rem; padding:0.35rem 0.6rem;
                border-radius:0; outline:none;"></select>
            </label>
            <span id="graph-stats" style="font-family:var(--font-mono); font-size:0.8rem;
              color:var(--cDim);"></span>
          </div>
          <div style="margin-top:0.6rem; font-size:0.8rem; color:var(--inkDim);
            font-family:var(--font-body);">
            Click empty space to add a node &middot; click two nodes to connect them &middot;
            click a weight to edit it &middot; right-click (or long-press) a node or edge to delete
          </div>
          <div id="graph-error" style="display:none; margin-top:0.5rem; font-size:0.8rem;
            color:#ff5f5f; font-family:var(--font-mono);"></div>
        </div>

        <div id="engine-panel" class="panel" style="margin-bottom:1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;
            margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
            <div style="display:flex; align-items:center; gap:1rem;">
              <div id="engine-status" class="eyebrow" style="margin:0;">STATUS: IDLE</div>
              <div id="step-counter" style="font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);"></div>
            </div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center;">
              <button id="run-btn" class="btn btn-primary" style="font-size:0.85rem;">▶ RUN</button>
              <button id="challenge-btn" class="btn" style="font-size:0.85rem;">🎮 Challenge</button>
              <span id="combo-chip" class="combo-chip is-hidden">COMBO ×0</span>
              <button id="prev-btn" class="btn btn-ghost" style="font-size:0.85rem;" disabled>← PREV</button>
              <button id="play-btn" class="btn btn-ghost" style="font-size:0.85rem;" disabled>▶ PLAY</button>
              <button id="step-btn" class="btn btn-ghost" style="font-size:0.85rem;" disabled>NEXT →</button>
              <select id="speed-select" style="background:var(--bg1); border:1px solid var(--panel-border);
                color:var(--ink); font-family:var(--font-body); font-size:0.8rem; padding:0.35rem 0.5rem;
                border-radius:0; outline:none;">
                <option value="0.5">0.5×</option>
                <option value="1" selected>1×</option>
                <option value="2">2×</option>
              </select>
              <button id="reset-btn" class="btn" style="font-size:0.85rem;">↺ RESET</button>
              <button id="compare-btn" class="btn is-hidden" style="font-size:0.85rem;">⚖ COMPARE</button>
            </div>
          </div>

          <div id="engine-view" style="min-height:300px;">
            <svg id="engine-svg" viewBox="0 0 760 280"
              style="width:100%; height:100%; min-height:300px; display:block;"></svg>
            <div id="engine-note" style="padding:0.75rem 1.25rem; opacity:0; transition:0.3s;
              font-family:var(--font-mono); font-size:1.05rem;
              border-top:1px solid var(--panel-border); background:rgba(2,4,6,0.9); color:var(--c);">
            </div>
          </div>

          <div id="scrub-row" style="display:none; margin-top:1rem; align-items:center; gap:1rem;">
            <input type="range" id="step-slider" min="0" max="0" value="0"
              style="flex:1; width:100%; accent-color:var(--c);">
          </div>
          <div id="counter-panel" style="display:none; margin-top:0.85rem; gap:0.5rem; flex-wrap:wrap;"></div>

          <details style="margin-top:1.25rem; border-top:1px solid var(--panel-border); padding-top:1rem;">
            <summary style="font-family:var(--font-body); font-size:0.8rem; font-weight:600;
              color:var(--inkDim); cursor:pointer; list-style:none; user-select:none;">
              ⚙ What-If Mode — Adjust edge weights
            </summary>
            <div id="whatif-controls" style="margin-top:1rem; display:flex; flex-direction:column; gap:0.75rem;"></div>
          </details>
        </div>

        <div id="compare-panel" class="panel is-hidden" style="margin-bottom:1.5rem; border-top:2px solid var(--c);">
          <div style="display:flex; justify-content:space-between; align-items:center;
            margin-bottom:1rem; flex-wrap:wrap; gap:0.75rem;">
            <span class="eyebrow" style="margin:0;">SAME GRAPH · TWO ALGORITHMS</span>
            <div style="display:flex; gap:0.5rem; align-items:center;">
              <button id="compare-prev" class="btn btn-ghost" style="font-size:0.8rem; padding:0.35rem 0.7rem;">←</button>
              <button id="compare-play" class="btn btn-ghost" style="font-size:0.8rem; padding:0.35rem 0.7rem;">▶</button>
              <button id="compare-next" class="btn btn-ghost" style="font-size:0.8rem; padding:0.35rem 0.7rem;">→</button>
              <span id="compare-step-label" style="font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);"></span>
            </div>
          </div>
          <input type="range" id="compare-slider" min="0" max="0" value="0"
            style="width:100%; accent-color:var(--c); margin-bottom:1rem;">
          <div id="compare-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:1.25rem;">
            ${['a', 'b'].map((side, i) => `
            <div>
              <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem; flex-wrap:wrap;">
                <select id="compare-pick-${side}" style="background:var(--bg1);
                  border:1px solid ${i === 0 ? 'var(--c)' : 'var(--c)'};
                  color:var(--ink); font-family:var(--font-body); font-size:0.8rem;
                  padding:0.3rem 0.5rem; border-radius:0; outline:none;">
                  ${DATA.GRAPH_ALGORITHMS.map(a =>
                    `<option value="${a.id}"${(i === 0 ? a.id === 'bfs' : a.id === 'dijkstra') ? ' selected' : ''}>${a.emoji} ${a.name}</option>`
                  ).join('')}
                </select>
                <span id="compare-total-${side}" style="font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);"></span>
              </div>
              <svg id="compare-svg-${side}" viewBox="0 0 760 280"
                style="width:100%; background:rgba(2,4,6,0.6); border:1px solid var(--panel-border);"></svg>
              <div id="compare-note-${side}" style="font-family:var(--font-mono); font-size:0.85rem;
                color:var(--c); margin-top:0.5rem; min-height:2.2em;"></div>
              <div id="compare-counts-${side}" style="display:flex; gap:0.4rem; flex-wrap:wrap; margin-top:0.4rem;"></div>
            </div>`).join('')}
          </div>
          <p id="compare-verdict" style="font-family:var(--font-mono); font-size:0.9rem;
            color:var(--inkDim); margin:1rem 0 0; border-left:3px solid var(--c);
            padding-left:1rem; max-width:none;"></p>
        </div>

        <div id="complexity-card" class="panel is-hidden" style="margin-bottom:1.5rem;">
          <span class="eyebrow" style="margin-bottom:0.85rem;">COMPLEXITY — WHAT AM I PAYING?</span>
          <div id="complexity-rows" style="display:flex; gap:2.5rem; flex-wrap:wrap;
            font-family:var(--font-mono); font-size:0.95rem;"></div>
          <p id="complexity-live" style="display:none; font-family:var(--font-mono); font-size:0.9rem;
            color:var(--cDim); margin:0.85rem 0 0; border-left:3px solid var(--c);
            padding-left:1rem; max-width:none;"></p>
        </div>

        <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-start;">
          <button id="explain-btn" class="btn btn-ghost" style="flex-shrink:0;">✦ AI NARRATE</button>
          <select id="level-select" title="Narration level"
            style="background:var(--bg1); border:1px solid var(--panel-border);
            color:var(--ink); font-family:var(--font-body); font-size:0.8rem;
            padding:0.5rem 0.6rem; border-radius:0; outline:none; flex-shrink:0;">
            <option value="beginner" selected>Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <div id="explanation-box" class="panel is-hidden" style="flex:1;
            font-family:var(--font-mono); font-size:1rem; color:var(--c);
            border-color:rgba(212, 96, 44,0.3); min-width:180px;">
          </div>
        </div>

        <div style="margin-top:2rem; display:flex; gap:0.75rem; flex-wrap:wrap; align-items:center;">
          <span style="font-size:0.8rem; color:var(--inkDim); font-family:var(--font-pixel); font-size:0.72rem; letter-spacing:0.1em;">TRY ANOTHER:</span>
          ${DATA.WORLDS.slice(0,4).map(w => `
            <a href="#/experience?algo=${w.algo || 'dijkstra'}" class="btn" style="font-size:0.8rem; padding:0.4rem 0.8rem;">
              ${w.emoji} ${w.metaphor}
            </a>
          `).join('')}
        </div>
      </section>
    `},
    mount: (view, params) => {
      const switcher = view.querySelector('#algo-switch');
      switcher?.addEventListener('change', () => {
        window.location.hash = `#/experience?algo=${switcher.value}`;
      });
      import('./engine.js').then(m => m.mountEngine(view, params.get('algo') || 'dijkstra'));
    }
  },

  "#/a2z": {
    title: "AlgoVision · A2Z Journey",
    html: () => `
      <div class="a2z-section">
        <div class="a2z-header">
          <div class="section-label">
            <span class="eyebrow" style="margin:0;">COMPLETE ROADMAP</span>
          </div>
          <h1 style="font-family:var(--font-display2); font-size:clamp(3.5rem,8vw,7rem); letter-spacing:0.04em; margin-bottom:0.75rem;">A2Z ALGORITHM<br>MASTERY</h1>
          <p style="max-width:52ch; margin-bottom:0;">Every concept. Every pattern. Every problem — in one structured journey from absolute beginner to expert.</p>
        </div>
        <div class="journey-stats">
          <div class="journey-stat">
            <span class="journey-stat-num">${DATA.A2Z_STEPS.length}</span>
            <span class="journey-stat-label">Total Steps</span>
          </div>
          <div class="journey-stat">
            <span class="journey-stat-num">${DATA.A2Z_STEPS.reduce((s,st)=>(s + (st.problems||[]).length),0)}</span>
            <span class="journey-stat-label">Problems</span>
          </div>
          <div class="journey-stat">
            <span class="journey-stat-num">${(() => {
              const total = DATA.A2Z_STEPS.reduce((s, st) => s + (st.problems || []).length, 0);
              const done = P.stats().completed;
              return total ? Math.round((done / total) * 100) : 0;
            })()}%</span>
            <span class="journey-stat-label">Understood</span>
          </div>
          <div class="journey-stat">
            <span class="journey-stat-num">12</span>
            <span class="journey-stat-label">3D Vizzes</span>
          </div>
        </div>
        <div class="a2z-grid">
          ${DATA.A2Z_STEPS.map((step, idx) => `
            <a href="#/a2z-problem?step=${idx+1}&prob=${step.step.replace('Step ','')}-1"
               class="a2z-card"
               data-num="${String(idx+1).padStart(2,'0')}">
              <div class="a2z-card-num">${String(idx+1).padStart(2,'0')}</div>
              <div class="a2z-card-step">${step.step}</div>
              <div class="a2z-card-title">${step.title}</div>
              <div class="a2z-card-count">${(() => {
                const probs = step.problems || [];
                const done = probs.filter(p => P.getStatus(p.id) === 'completed').length;
                return done ? `${done} of ${probs.length} understood` : `${probs.length} problems`;
              })()}</div>
              <div class="a2z-progress-bar">
                <div class="a2z-progress-fill" style="width:${P.stepProgress(step.problems)}%;"></div>
              </div>
            </a>
          `).join('')}
        </div>
      </div>
    `,
    mount: (view) => {
      if (typeof gsap === 'undefined') return;
      const cards = view.querySelectorAll('.a2z-card');
      cards.forEach((card, i) => {
        gsap.from(card, {
          opacity: 0,
          y: 20,
          duration: 0.4,
          delay: i * 0.04,
          ease: 'power2.out',
          clearProps: 'all'
        });
      });
    }
  },

  "#/a2z-problem": {
    title: "AlgoVision · Problem Visualizer",
    html: (params) => `
      <section>
        <span class="eyebrow" style="margin-bottom:1.5rem;">
          ← <a href="#/a2z" style="color:var(--cDim); text-decoration:none;">A2Z JOURNEY</a>
          &nbsp;/&nbsp; PROBLEM VIEWER
        </span>
        <div style="display:grid; grid-template-columns:280px 1fr; gap:1.5rem; margin-top:1.5rem;" id="prob-layout">
          <div class="panel" style="padding:0; overflow:hidden; align-self:start;">
            <div id="step-title" style="padding:0.85rem 1.25rem; border-bottom:1px solid var(--panel-border);
              font-family:var(--font-pixel); font-size:0.72rem; color:var(--cDim);"></div>
            <div id="prob-list" style="overflow-y:auto; max-height:70vh;"></div>
          </div>

          <!-- RIGHT PANEL: Visualization + Details -->
          <div id="viz-panel" style="min-width:0; display:flex; flex-direction:column; gap:1.25rem;">

            <!-- 3D Scene Canvas -->
            <div id="viz-inner" style="width:100%; min-height:320px;
              background:#02060a; border:1px solid var(--panel-border);
              position:relative; overflow:hidden;">
            </div>

            <!-- Step Controls -->
            <div class="panel" style="padding:1rem 1.25rem; border-top:2px solid var(--c);">
              <div style="display:flex; align-items:center; gap:0.75rem;
                margin-bottom:0.75rem; flex-wrap:wrap;">
                <button id="scene-step-back" class="btn btn-ghost"
                  style="font-size:0.85rem; padding:0.4rem 0.8rem;" disabled>
                  ← PREV STEP
                </button>
                <span id="scene-step-counter"
                  style="font-family:var(--font-pixel); font-size:0.75rem;
                  color:var(--cDim); min-width:60px; text-align:center;">
                  1 / ?
                </span>
                <button id="scene-step-fwd" class="btn btn-primary"
                  style="font-size:0.85rem; padding:0.4rem 0.8rem;">
                  NEXT STEP →
                </button>
              </div>
              <p id="scene-narration"
                style="font-family:var(--font-mono); font-size:1.05rem;
                color:var(--c); margin:0; line-height:1.6; min-height:2.5rem;">
              </p>
            </div>

            <!-- Problem Details -->
            <div class="panel">
              <div style="display:flex; justify-content:space-between;
                align-items:flex-start; margin-bottom:0.75rem; gap:1rem; flex-wrap:wrap;">
                <div>
                  <span class="eyebrow" id="prob-id-label" style="margin-bottom:0.25rem;"></span>
                  <h2 id="prob-title" style="margin:0; font-size:1.3rem;"></h2>
                </div>
                <span id="prob-difficulty"
                  style="font-family:var(--font-display2); font-size:1.1rem;
                  padding:4px 12px; border:1px solid currentColor;
                  align-self:flex-start; letter-spacing:0.08em;">
                </span>
              </div>
              <div style="display:flex; gap:0.75rem; align-items:center;
                margin-bottom:1rem; flex-wrap:wrap;">
                <span style="font-family:var(--font-pixel); font-size:0.72rem;
                  color:var(--cDim);">REAL WORLD:</span>
                <span id="prob-world"
                  style="font-family:var(--font-mono); font-size:1.1rem; color:var(--c);">
                </span>
              </div>
              <p id="prob-hook"
                style="font-family:var(--font-mono); font-size:1rem;
                color:var(--inkDim); border-left:3px solid var(--c);
                padding-left:1rem; margin-bottom:1.5rem; max-width:none;">
              </p>
              <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
                <button id="prev-prob" class="btn btn-ghost" style="font-size:0.85rem;">
                  ← PREV PROBLEM
                </button>
                <button id="next-prob" class="btn btn-primary" style="font-size:0.85rem;">
                  NEXT PROBLEM →
                </button>
                <button id="mark-understood" class="btn" style="font-size:0.85rem;">
                  ☐ MARK AS UNDERSTOOD
                </button>
                <a id="practice-link" href="#/practice"
                  class="btn" style="margin-left:auto; font-size:0.85rem;">
                  🐞 PRACTICE
                </a>
              </div>
            </div>

          </div>
        </div>
      </section>
    `,
    mount: (view, params) => {
      import('./vizScenes.js').then(({ mountScene }) => {
        import('./data.js').then((DATA) => {
          let currentStepIdx = 0;
          let currentProbIdx = 0;

          const targetProbId = params.get('prob') || '1-1';
          DATA.A2Z_STEPS.forEach((step, si) => {
            (step.problems||[]).forEach((p, pi) => {
              if (p.id === targetProbId) { currentStepIdx=si; currentProbIdx=pi; }
            });
          });

          const stepTitleEl = view.querySelector('#step-title');
          const probListEl  = view.querySelector('#prob-list');
          const prevBtn     = view.querySelector('#prev-prob');
          const nextBtn     = view.querySelector('#next-prob');

          function refreshStatusMarker(pid) {
            const el = view.querySelector(`.prob-status[data-pid="${pid}"]`);
            if (!el) return;
            const st = P.getStatus(pid);
            el.textContent = st === 'completed' ? '✓' : st === 'viewed' ? '·' : '';
            el.style.color = st === 'completed' ? '#4ade80' : 'var(--cDim)';
          }

          function renderStep(si) {
            const step = DATA.A2Z_STEPS[si];
            stepTitleEl.textContent = `${step.step}: ${step.title}`;
            probListEl.innerHTML = (step.problems||[]).map((p, pi) => {
              const cols = { E:'var(--cDim)', M:'var(--c)', H:'var(--c)' };
              return `<div class="prob-item" data-pi="${pi}" style="
                padding:0.7rem 1.25rem; border-bottom:1px solid var(--panel-border);
                cursor:pointer; display:flex; align-items:center; gap:0.75rem;
                transition:background 0.15s; font-size:0.875rem; border-left:2px solid transparent;">
                <span style="font-family:var(--font-pixel); font-size:0.7rem; color:${cols[p.difficulty]};
                  min-width:10px;">${p.difficulty}</span>
                <span style="color:var(--ink); flex:1;">${p.title}</span>
                <span class="prob-status" data-pid="${p.id}" style="min-width:14px; text-align:center;
                  font-family:var(--font-mono); font-size:0.85rem;
                  color:${P.getStatus(p.id) === 'completed' ? '#4ade80' : 'var(--cDim)'};">${
                  P.getStatus(p.id) === 'completed' ? '✓' : P.getStatus(p.id) === 'viewed' ? '·' : ''}</span>
              </div>`;
            }).join('');
            probListEl.querySelectorAll('.prob-item').forEach(el => {
              el.addEventListener('mouseenter', () => el.style.background='rgba(212, 96, 44,0.04)');
              el.addEventListener('mouseleave', () => { if (el.dataset.pi != currentProbIdx) el.style.background=''; });
              el.addEventListener('click', () => {
                currentProbIdx = parseInt(el.dataset.pi);
                renderProblem(currentStepIdx, currentProbIdx);
              });
            });
          }

          function renderProblem(si, pi) {
            const step = DATA.A2Z_STEPS[si];
            const prob = (step.problems || [])[pi];
            if (!prob) return;

            // Highlight active problem in sidebar
            view.querySelectorAll('.prob-item').forEach((el, i) => {
              el.style.background    = i === pi ? 'rgba(212, 96, 44,0.06)' : '';
              el.style.borderLeft    = i === pi ? '2px solid var(--c)' : '2px solid transparent';
            });

            // Update metadata
            const probIdLabel = view.querySelector('#prob-id-label');
            const probTitle   = view.querySelector('#prob-title');
            const probDiff    = view.querySelector('#prob-difficulty');
            const probWorld   = view.querySelector('#prob-world');
            const probHook    = view.querySelector('#prob-hook');

            if (probIdLabel) probIdLabel.textContent = `PROBLEM ${prob.id}`;
            if (probTitle)   probTitle.textContent   = prob.title;
            if (probDiff) {
              const diffMap = { E:'EASY', M:'MEDIUM', H:'HARD' };
              const colMap  = { E:'var(--cDim)', M:'var(--c)', H:'var(--c)' };
              probDiff.textContent = diffMap[prob.difficulty] || prob.difficulty;
              probDiff.style.color = colMap[prob.difficulty] || 'var(--c)';
            }
            if (probWorld) probWorld.textContent = prob.world;
            if (probHook)  probHook.textContent  = `"${prob.hook}"`;

            // Progress: opening a problem marks it viewed
            P.markViewed(prob.id);
            refreshStatusMarker(prob.id);
            const muBtnOld = view.querySelector('#mark-understood');
            if (muBtnOld) {
              const muBtn = muBtnOld.cloneNode(true);
              muBtnOld.parentNode.replaceChild(muBtn, muBtnOld);
              const refreshMu = () => {
                const done = P.getStatus(prob.id) === 'completed';
                muBtn.textContent = done ? '✓ UNDERSTOOD' : '☐ MARK AS UNDERSTOOD';
                muBtn.style.color = done ? '#4ade80' : '';
                muBtn.style.borderColor = done ? '#4ade80' : '';
              };
              refreshMu();
              muBtn.addEventListener('click', () => {
                const st = P.toggleCompleted(prob.id);
                if (st === 'completed') {
                  import('./game.js').then(G => G.recordProblemDone());
                }
                refreshMu();
                refreshStatusMarker(prob.id);
              });
            }

            history.replaceState(null,'',`#/a2z-problem?step=${si+1}&prob=${prob.id}`);

            // ── Mount 3D Scene ──────────────────────────────────────
            const vizInner = view.querySelector('#viz-inner');
            if (!vizInner) return;

            // Clear any auto-advance interval from VIZ_SCENES compat shim
            if (vizInner._vizAutoInterval) {
              clearInterval(vizInner._vizAutoInterval);
              vizInner._vizAutoInterval = null;
            }
            // Dispose previous scene
            if (vizInner._vizDispose) {
              vizInner._vizDispose();
              vizInner._vizDispose = null;
            }

            let controller = null;
            let currentSceneStep = 0;

            try {
              controller = mountScene(vizInner, prob.viz || 'default', prob);
            } catch (e) {
              console.error('Scene mount failed:', e);
              vizInner.innerHTML = '<div style="height:300px;display:flex;align-items:center;' +
                'justify-content:center;color:#2a7f8c;font-family:monospace;font-size:12px;">' +
                'Scene loading...</div>';
            }

            // ── Step Controls ────────────────────────────────────────
            const stepBackBtn  = view.querySelector('#scene-step-back');
            const stepFwdBtn   = view.querySelector('#scene-step-fwd');
            const stepCounter  = view.querySelector('#scene-step-counter');
            const stepNarration = view.querySelector('#scene-narration');

            function updateStepUI() {
              if (!controller) return;
              const total = controller.totalSteps();
              if (stepCounter)   stepCounter.textContent  = `${currentSceneStep + 1} / ${total}`;
              if (stepNarration) stepNarration.textContent = controller.narration(currentSceneStep);
              if (stepBackBtn)   stepBackBtn.disabled = currentSceneStep === 0;
              if (stepFwdBtn)    stepFwdBtn.disabled  = currentSceneStep >= total - 1;
            }

            if (stepBackBtn) {
              // Remove old listener by cloning the button
              const newBack = stepBackBtn.cloneNode(true);
              stepBackBtn.parentNode.replaceChild(newBack, stepBackBtn);
              newBack.addEventListener('click', () => {
                if (!controller || currentSceneStep <= 0) return;
                currentSceneStep--;
                controller.step(currentSceneStep);
                updateStepUI();
              });
            }

            if (stepFwdBtn) {
              const newFwd = stepFwdBtn.cloneNode(true);
              stepFwdBtn.parentNode.replaceChild(newFwd, stepFwdBtn);
              newFwd.addEventListener('click', () => {
                if (!controller || currentSceneStep >= controller.totalSteps()-1) return;
                currentSceneStep++;
                controller.step(currentSceneStep);
                updateStepUI();
              });
            }

            updateStepUI();

            // Scroll active item into view
            const activeItem = view.querySelector(`.prob-item[data-pi="${pi}"]`);
            if (activeItem) activeItem.scrollIntoView({ block:'nearest', behavior:'smooth' });
          }

          prevBtn.addEventListener('click', () => {
            if (currentProbIdx > 0) { currentProbIdx--; }
            else if (currentStepIdx > 0) {
              currentStepIdx--;
              currentProbIdx = (DATA.A2Z_STEPS[currentStepIdx].problems||[]).length - 1;
              renderStep(currentStepIdx);
            }
            renderProblem(currentStepIdx, currentProbIdx);
          });

          nextBtn.addEventListener('click', () => {
            const probs = DATA.A2Z_STEPS[currentStepIdx].problems||[];
            if (currentProbIdx < probs.length - 1) { currentProbIdx++; }
            else if (currentStepIdx < DATA.A2Z_STEPS.length - 1) {
              currentStepIdx++;
              currentProbIdx = 0;
              renderStep(currentStepIdx);
            }
            renderProblem(currentStepIdx, currentProbIdx);
          });

          renderStep(currentStepIdx);
          renderProblem(currentStepIdx, currentProbIdx);

          if (window.innerWidth < 768) {
            const layout = view.querySelector('#prob-layout');
            if (layout) layout.style.gridTemplateColumns = '1fr';
            probListEl.style.maxHeight = '180px';
          }
        });
      });
    }
  },

  "#/practice": {
    title: "AlgoVision · AI Bug Finder",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">AI DEBUGGER</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em; margin-bottom:0.5rem;">PRACTICE & DEBUG</h1>
        <p style="margin-bottom:2.5rem;">Paste any DSA code. AlgoVision detects the algorithm and the AI scans for bugs.</p>
        <div id="practice-grid" style="display:grid; grid-template-columns:2fr 1fr; gap:1.5rem;">
          <div class="panel" style="border-top:3px solid var(--c);">
            <span class="eyebrow" style="margin-bottom:1.25rem;">CODE EDITOR</span>
            <div style="display:flex; gap:1rem; align-items:center; margin-bottom:1rem;">
              <label style="font-size:0.8rem; color:var(--inkDim);">Language:</label>
              <select id="lang-select" style="background:var(--bg1); border:1px solid var(--panel-border);
                color:var(--ink); font-family:var(--font-body); font-size:0.8rem; padding:0.35rem 0.6rem;
                border-radius:0; outline:none;">
                <option value="python">Python</option>
                <option value="cpp">C++</option>
                <option value="java">Java</option>
                <option value="javascript">JavaScript</option>
              </select>
            </div>
            <textarea id="code-area" style="width:100%; height:320px; background:rgba(2,4,6,0.95);
              color:var(--c); font-family:var(--font-mono); font-size:1.1rem; padding:1.25rem;
              border:1px solid var(--panel-border); outline:none; resize:vertical; border-radius:0;
              line-height:1.5;"></textarea>
            <div id="detect-result" style="display:none; margin-top:0.75rem; padding:0.6rem 1rem;
              border:1px solid var(--panel-border); font-size:0.85rem; color:var(--inkDim);">
            </div>
            <button id="find-bug-btn" class="btn btn-primary" style="margin-top:1rem; width:100%;">
              SCAN FOR BUGS
            </button>
            <div id="bug-result" style="margin-top:1.25rem; padding:1.25rem;
              border:1px solid rgba(212, 96, 44,0.2);
              display:none; color:var(--cBright); font-family:var(--font-mono); font-size:1rem;
              background:rgba(212, 96, 44,0.03); line-height:1.7;"></div>
          </div>
          <div class="panel">
            <span class="eyebrow" style="margin-bottom:1.5rem;">PRO TIPS</span>
            <div style="display:flex; flex-direction:column; gap:1.25rem;">
              ${[
                ['→', 'Trace by hand first', 'Before running, manually walk through 2–3 examples.'],
                ['→', 'Check edge cases', 'Empty arrays, single elements, max values — test them all.'],
                ['→', 'Think in metaphors', 'Visualize the algorithm as a real-world process.'],
                ['→', 'Complexity matters', 'O(n²) may pass small tests but fail large inputs.'],
              ].map(([icon, title, desc]) => `
                <div style="display:flex; gap:0.75rem; align-items:flex-start; padding-bottom:1.25rem; border-bottom:1px solid var(--panel-border);">
                  <span style="color:var(--c); font-family:var(--font-condensed); font-weight:700; font-size:1.1rem; flex-shrink:0; margin-top:0.1rem;">${icon}</span>
                  <div>
                    <div style="font-family:var(--font-condensed); font-size:1rem; font-weight:700; letter-spacing:0.05em; text-transform:uppercase; color:var(--ink); margin-bottom:0.2rem;">${title}</div>
                    <div style="font-size:0.8rem; color:var(--inkDim);">${desc}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </section>
    `,
    mount: (view) => {
      import('./engine.js').then(m => m.mountBugFinder(view));
    }
  },

  "#/family": {
    title: "AlgoVision · Algorithm Family Tree",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">KNOWLEDGE GRAPH</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em; margin-bottom:0.75rem;">ALGORITHM FAMILY TREE</h1>
        <p style="margin-bottom:2rem;">Algorithms don't exist in isolation — see how each one descends from, generalizes, or improves upon another.</p>
        <div class="panel" style="padding:0;">
          <div id="family-svg-wrapper" style="overflow:auto;">
            <svg id="family-svg" viewBox="0 0 900 580"
              style="width:100%; min-width:900px; display:block;"></svg>
          </div>
        </div>
        <div id="family-info" class="panel" style="margin-top:1.5rem; display:none; border-top:3px solid var(--c);">
          <h3 id="family-info-title" style="color:var(--cAccentBright); margin-bottom:0.4rem;"></h3>
          <p id="family-info-desc" style="font-size:0.875rem; margin-bottom:1rem; max-width:none;"></p>
          <a id="family-info-link" href="#/" class="btn btn-ghost">Visualize this →</a>
        </div>
      </section>
    `,
    mount: (view) => {
      const svg = view.querySelector('#family-svg');
      const infoPanel = view.querySelector('#family-info');
      const infoTitle = view.querySelector('#family-info-title');
      const infoDesc  = view.querySelector('#family-info-desc');
      const infoLink  = view.querySelector('#family-info-link');

      const NODES = [
        { id:'search',    label:'Searching',         x:100, y:60,  emoji:'🔍', desc:'The root of all lookup operations.', color:'var(--cDim)' },
        { id:'linsearch', label:'Linear Search',     x:50,  y:180, emoji:'➡️', desc:'Check every element. O(n). Brute force.', color:'var(--cDim)', algo:'bfs' },
        { id:'binsearch', label:'Binary Search',     x:180, y:180, emoji:'📚', desc:'Halve the search space. O(log n). Requires sorted input.', color:'var(--c)', algo:'binary_search' },
        { id:'graph',     label:'Graph Traversal',   x:420, y:60,  emoji:'🌐', desc:'Explore nodes and edges systematically.', color:'var(--cDim)' },
        { id:'bfs',       label:'BFS',               x:310, y:200, emoji:'👤', desc:'Level by level. Queue-based. Shortest path in unweighted graphs.', color:'var(--c)', algo:'bfs' },
        { id:'dfs',       label:'DFS',               x:440, y:200, emoji:'🗺️', desc:'Go deep first. Stack-based. Cycle detection, topological sort.', color:'var(--c)', algo:'dfs' },
        { id:'dijkstra',  label:"Dijkstra's",        x:310, y:340, emoji:'📍', desc:'BFS + edge weights + priority queue. GPS routing.', color:'var(--cBright)', algo:'dijkstra' },
        { id:'astar',     label:'A*',                x:440, y:340, emoji:'⭐', desc:"Dijkstra + heuristic. Game AI pathfinding.", color:'var(--cBright)', algo:'dijkstra' },
        { id:'sort',      label:'Sorting',           x:680, y:60,  emoji:'📊', desc:'Order elements by comparison or distribution.', color:'var(--cDim)' },
        { id:'msort',     label:'Merge Sort',        x:600, y:200, emoji:'🏆', desc:'Divide & conquer. O(n log n). Stable.', color:'var(--c)', algo:'sorting' },
        { id:'qsort',     label:'Quick Sort',        x:740, y:200, emoji:'⚡', desc:'Pivot & partition. O(n log n) avg. Cache-friendly.', color:'var(--c)', algo:'sorting' },
        { id:'dp',        label:'Dynamic Programming',x:140, y:420, emoji:'💾', desc:'Optimal substructure + overlapping subproblems = memoization.', color:'var(--c)', algo:'dp' },
        { id:'greedy',    label:'Greedy',            x:300, y:460, emoji:'🎯', desc:'Local optimal choice at each step.', color:'var(--c)', algo:'greedy' },
        { id:'backtrack', label:'Backtracking',      x:500, y:460, emoji:'🔄', desc:'DFS + undo. Explores all possibilities. N-Queens, Sudoku.', color:'var(--c)', algo:'backtracking' },
        { id:'twoptr',    label:'Two Pointers',      x:180, y:320, emoji:'👈👉', desc:'Binary search pattern. Converging/expanding window. O(n).', color:'var(--c)', algo:'binary_search' },
      ];
      const EDGES = [
        {s:'search',t:'linsearch',label:'unsorted'},{s:'search',t:'binsearch',label:'sorted'},
        {s:'binsearch',t:'twoptr',label:'pattern'},{s:'graph',t:'bfs',label:'queue'},
        {s:'graph',t:'dfs',label:'stack'},{s:'bfs',t:'dijkstra',label:'+ weights'},
        {s:'dijkstra',t:'astar',label:'+ heuristic'},{s:'dfs',t:'backtrack',label:'+ undo'},
        {s:'sort',t:'msort',label:'divide'},{s:'sort',t:'qsort',label:'pivot'},
        {s:'graph',t:'dp',label:'subproblems'},{s:'dp',t:'greedy',label:'local optimal'},
      ];

      const ns = Object.fromEntries(NODES.map(n => [n.id, n]));
      const mkSVG = (tag) => document.createElementNS("http://www.w3.org/2000/svg", tag);

      EDGES.forEach(e => {
        const a=ns[e.s], b=ns[e.t];
        const line=mkSVG("line");
        line.setAttribute("x1",a.x); line.setAttribute("y1",a.y);
        line.setAttribute("x2",b.x); line.setAttribute("y2",b.y);
        line.setAttribute("stroke","rgba(0,150,184,0.2)"); line.setAttribute("stroke-width","1.5");
        svg.appendChild(line);
        const tx=mkSVG("text");
        tx.setAttribute("x",(a.x+b.x)/2); tx.setAttribute("y",(a.y+b.y)/2-5);
        tx.setAttribute("fill","var(--cDim)"); tx.setAttribute("font-size","9");
        tx.setAttribute("text-anchor","middle"); tx.setAttribute("font-family","var(--font-body)");
        tx.textContent=e.label; svg.appendChild(tx);
      });

      NODES.forEach(n => {
        const g=mkSVG("g"); g.style.cursor='pointer';
        const circle=mkSVG("circle");
        circle.setAttribute("cx",n.x); circle.setAttribute("cy",n.y);
        circle.setAttribute("r","22"); circle.setAttribute("fill","var(--cDeep)");
        circle.setAttribute("stroke",n.color); circle.setAttribute("stroke-width","1.5");
        g.appendChild(circle);
        const emoji=mkSVG("text");
        emoji.setAttribute("x",n.x); emoji.setAttribute("y",n.y+5);
        emoji.setAttribute("text-anchor","middle"); emoji.setAttribute("font-size","14");
        emoji.textContent=n.emoji; g.appendChild(emoji);
        const label=mkSVG("text");
        label.setAttribute("x",n.x); label.setAttribute("y",n.y+38);
        label.setAttribute("text-anchor","middle"); label.setAttribute("font-size","10");
        label.setAttribute("fill","var(--inkDim)"); label.setAttribute("font-family","var(--font-body)");
        label.textContent=n.label; g.appendChild(label);
        g.addEventListener('click', () => {
          infoPanel.style.display='block';
          infoTitle.textContent=n.label;
          infoDesc.textContent=n.desc;
          infoLink.href=n.algo?`#/experience?algo=${n.algo}`:'#/explore';
        });
        svg.appendChild(g);
      });
    }
  },

  "#/today": {
    title: "AlgoVision · Daily Insights",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">DAILY BROADCAST</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em; margin-bottom:0.5rem;">60-SECOND INSIGHTS</h1>
        <p style="margin-bottom:2.5rem;">Quick deep-dives into algorithm concepts — one insight at a time.</p>
        <div class="grid-3">
          ${DATA.CLIPS.map((clip, i) => `
            <div class="panel panel-glow" style="cursor:pointer; border-top:3px solid ${i%2===0?'var(--c)':'var(--c)'};">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
                <span style="font-family:var(--font-pixel); font-size:0.72rem; color:var(--c);">${clip.tag}</span>
                <span style="font-family:var(--font-display2); font-size:1.5rem; color:rgba(212, 96, 44,0.15);">${(i+1).toString().padStart(2,'0')}</span>
              </div>
              <span class="eyebrow" style="margin-bottom:0.5rem; color:var(--cDim);">${clip.topic}</span>
              <h3 style="font-size:0.95rem; line-height:1.4;">${clip.title}</h3>
              <div style="margin-top:1.25rem; font-family:var(--font-condensed); font-size:0.85rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--c);">Read more →</div>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/journey": {
    title: "AlgoVision · My Journey",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">PROGRESS DASHBOARD</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em; margin-bottom:0.5rem;">MY JOURNEY</h1>
        <p style="margin-bottom:2.5rem;">Your real progress — tracked in this browser as you explore, trace, and understand.</p>
        <div id="journey-content"></div>
        <div class="panel" style="margin-top:1.5rem;">
          <span class="eyebrow" style="margin-bottom:0.75rem;">CLASSROOM TOOLS</span>
          <p style="font-size:0.85rem; margin-bottom:1rem;">Progress lives in this browser only.
            Export it to move machines or hand it in; import to restore.</p>
          <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
            <button id="export-progress" class="btn btn-ghost" style="font-size:0.85rem;">⬇ EXPORT JSON</button>
            <button id="import-progress" class="btn btn-ghost" style="font-size:0.85rem;">⬆ IMPORT JSON</button>
            <input type="file" id="import-file" accept=".json,application/json" style="display:none;">
            <button id="reset-progress" class="btn" style="font-size:0.85rem; margin-left:auto;">RESET PROGRESS</button>
          </div>
          <div id="journey-tools-msg" style="display:none; margin-top:0.75rem; font-family:var(--font-mono);
            font-size:0.85rem; color:var(--c);"></div>
        </div>
      </section>
    `,
    mount: (view) => {
      const content = view.querySelector('#journey-content');
      const msg = view.querySelector('#journey-tools-msg');

      // ── Player card + quests + achievement wall ──
      import('./game.js').then((Game) => {
        const host = document.createElement('div');
        view.querySelector('section')?.insertBefore(host, content);

        function renderGame() {
          const g = Game.state();
          const quests = Game.questState();
          host.innerHTML = `
            <div class="player-card panel">
              <div class="pc-left">
                <div class="pc-level">${g.level}</div>
                <div>
                  <div class="pc-rank">${g.rank}</div>
                  <div class="pc-xpbar"><span style="width:${Math.max(4, g.pct)}%"></span></div>
                  <div class="pc-xptext">${g.intoLevel} / ${g.levelSpan} XP to level ${g.level + 1}</div>
                </div>
              </div>
              <div class="pc-stats">
                <div><strong>${g.tracesRun}</strong><span>traces</span></div>
                <div><strong>${g.accuracy}%</strong><span>prediction acc.</span></div>
                <div><strong>×${g.bestCombo}</strong><span>best combo</span></div>
                <div><strong>${g.streak}</strong><span>day streak</span></div>
              </div>
            </div>

            <div class="panel" style="margin-bottom:1rem;">
              <span class="eyebrow">DAILY QUESTS — RESET AT MIDNIGHT</span>
              ${quests.map(q => `
                <div class="quest-row ${q.claimed ? 'claimed' : q.done ? 'ready' : ''}">
                  <span class="q-icon">${q.icon}</span>
                  <span class="q-name">${q.name}</span>
                  <span class="q-progress">${q.have}/${q.goal}</span>
                  <button class="btn q-claim" data-q="${q.id}"
                    ${q.done && !q.claimed ? '' : 'disabled'}>
                    ${q.claimed ? '✓ Claimed' : q.done ? `Claim +${Game.XP.QUEST_DONE} XP` : 'In progress'}
                  </button>
                </div>`).join('')}
            </div>

            <div class="panel" style="margin-bottom:1rem;">
              <span class="eyebrow">ACHIEVEMENTS — ${g.unlocked.length}/${Game.ACHIEVEMENTS.length}</span>
              <div class="achv-grid">
                ${Game.ACHIEVEMENTS.map(a2 => {
                  const got = g.unlocked.includes(a2.id);
                  return `<div class="achv ${got ? 'got' : 'locked'}" title="${a2.desc}">
                    <span class="a-icon">${a2.icon}</span>
                    <span class="a-name">${a2.name}</span>
                    <span class="a-desc">${a2.desc}</span>
                  </div>`;
                }).join('')}
              </div>
            </div>`;

          host.querySelectorAll('.q-claim').forEach(btn => {
            btn.addEventListener('click', () => {
              if (Game.claimQuest(btn.dataset.q)) renderGame();
            });
          });
        }
        renderGame();
        addEventListener('av:xp', renderGame);
      });

      const say = (text, isError = false) => {
        if (!msg) return;
        msg.textContent = text;
        msg.style.color = isError ? '#ff5f5f' : 'var(--c)';
        msg.style.display = 'block';
      };

      function tile(label, value, current, target, i) {
        const pct = Math.min((current / target) * 100, 100);
        return `
          <div class="panel" style="border-top:3px solid ${i % 2 === 0 ? 'var(--c)' : 'var(--c)'};">
            <span class="eyebrow" style="margin-bottom:0.5rem;">${label}</span>
            <div style="font-family:var(--font-display2); font-size:4.5rem; color:var(--ink); margin:0.25rem 0; letter-spacing:0.02em; line-height:1;">${value}</div>
            <div class="stat-bar-bg"><div class="stat-bar-fill" style="width:${pct}%;"></div></div>
            <div style="font-size:0.75rem; color:var(--inkDim); margin-top:0.5rem;">Target: ${target}</div>
          </div>`;
      }

      function renderStats() {
        if (!P.hasAnyActivity()) {
          content.innerHTML = `
            <div class="panel" style="text-align:center; padding:3rem 2rem; border-top:3px solid var(--c);">
              <div style="font-size:2.5rem; margin-bottom:1rem;">🌱</div>
              <h3 style="margin-bottom:0.6rem;">Nothing tracked yet</h3>
              <p style="margin:0 auto 1.5rem; max-width:44ch;">Open a problem in the A2Z roadmap or run a
                live trace — your progress starts counting from the first step you take.</p>
              <div style="display:flex; gap:0.75rem; justify-content:center; flex-wrap:wrap;">
                <a href="#/a2z" class="btn btn-primary">Start Step 1 →</a>
                <a href="#/experience" class="btn btn-ghost">Run a Trace</a>
              </div>
            </div>`;
          return;
        }
        const s = P.stats();
        const totalProblems = DATA.A2Z_STEPS.reduce((t, st) => t + (st.problems || []).length, 0);
        content.innerHTML = `<div class="grid-2">
          ${tile('PROBLEMS UNDERSTOOD', s.completed, s.completed, totalProblems, 0)}
          ${tile('TRACES RUN', s.tracesRun, s.tracesRun, 50, 1)}
          ${tile('STREAK', `${s.streak} day${s.streak === 1 ? '' : 's'}`, s.streak, 30, 2)}
          ${tile('MASTERY SCORE', `${s.points} pts`, s.points, 1000, 3)}
        </div>`;
      }

      renderStats();

      view.querySelector('#export-progress')?.addEventListener('click', () => {
        try {
          const blob = new Blob([P.exportJSON()], { type: 'application/json' });
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'algovision-progress.json';
          a.click();
          URL.revokeObjectURL(a.href);
          say('Progress exported — check your downloads.');
        } catch {
          say('Export failed — your browser may be blocking downloads.', true);
        }
      });

      const fileInput = view.querySelector('#import-file');
      view.querySelector('#import-progress')?.addEventListener('click', () => fileInput?.click());
      fileInput?.addEventListener('change', () => {
        const f = fileInput.files?.[0];
        if (!f) return;
        const reader = new FileReader();
        reader.onload = () => {
          const res = P.importJSON(String(reader.result));
          if (res.ok) { renderStats(); say('Progress imported.'); }
          else say(res.error || 'Import failed.', true);
          fileInput.value = '';
        };
        reader.onerror = () => say('Could not read that file.', true);
        reader.readAsText(f);
      });

      // Two-click confirm — no blocking browser dialogs
      const resetBtn = view.querySelector('#reset-progress');
      let armed = false;
      resetBtn?.addEventListener('click', () => {
        if (!armed) {
          armed = true;
          resetBtn.textContent = 'CLICK AGAIN TO CONFIRM';
          resetBtn.style.color = '#ff5f5f';
          setTimeout(() => {
            armed = false;
            resetBtn.textContent = 'RESET PROGRESS';
            resetBtn.style.color = '';
          }, 3000);
          return;
        }
        P.resetAll();
        armed = false;
        resetBtn.textContent = 'RESET PROGRESS';
        resetBtn.style.color = '';
        renderStats();
        say('Progress cleared.');
      });
    }
  },

  "#/realworld": {
    title: "AlgoVision · Real World",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">SYSTEM MAPPINGS</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em; margin-bottom:0.5rem;">ALGORITHMS IN THE WILD</h1>
        <p style="margin-bottom:2.5rem;">These aren't just textbook concepts — they power the products you use every day.</p>
        <div class="grid-3">
          ${DATA.REALWORLD.map((item, i) => `
            <div class="panel panel-glow" style="position:relative; overflow:hidden;">
              <div style="font-size:2.25rem; margin-bottom:1.25rem;">${item.icon}</div>
              <span class="eyebrow" style="margin-bottom:0.4rem; color:var(--cDim);">${item.metaphor.toUpperCase()}</span>
              <h3 style="margin-bottom:0.6rem;">${item.title}</h3>
              <p style="font-size:0.875rem;">${item.desc}</p>
              <div style="position:absolute; bottom:0; left:0; width:${20+i*15}%; height:2px; background:var(--c); opacity:0.4;"></div>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/404": {
    title: "AlgoVision · 404",
    html: () => `
      <section style="text-align:center; min-height:60vh; display:flex; flex-direction:column;
        justify-content:center; align-items:center;">
        <div style="font-family:var(--font-display2); font-size:12rem; color:rgba(212, 96, 44,0.08); line-height:1; margin-bottom:-2rem;">404</div>
        <span class="eyebrow" style="color:var(--c); margin-bottom:1rem;">NODE NOT FOUND</span>
        <h1 style="font-family:var(--font-display2); font-size:3rem; letter-spacing:0.04em; margin-bottom:1rem;">OFF THE GRAPH</h1>
        <p style="margin:0 auto 2rem;">You've wandered into untraced territory.</p>
        <a href="#/" class="btn btn-primary">Return to Root →</a>
      </section>
    `
  }
};
