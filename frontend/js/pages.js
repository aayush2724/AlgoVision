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
        <div class="group-head"><span class="eyebrow">How it works</span></div>
        <div class="home-section-head">
          <h2 class="home-h2">Three acts, one insight</h2>
          <p class="page-lede">Every algorithm here is taught the same way — a metaphor you already understand, then the mechanics underneath it, then a trace on your own input.</p>
        </div>
        <div class="grid-3">
          ${DATA.ACTS.map((act, i) => `
            <div class="act-card">
              <span class="act-step-num">${String(i+1).padStart(2,'0')}</span>
              <h3 class="act-title">${act.title}</h3>
              <p>${act.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <!-- Paste-detect promoted: it's the strongest single thing the product
           does, and it used to sit at the very bottom of the page. -->
      <section>
        <div class="group-head"><span class="eyebrow">Quick start</span></div>
        <div class="panel paste-split">
          <div class="paste-pitch">
            <h2 class="home-h2">Paste any DSA code</h2>
            <p class="page-lede">AlgoVision reads it, names the algorithm, and opens the matching trace on your own input — no sign-up, no configuration.</p>
            <div class="paste-recognises">
              <span class="transport-count">Recognises</span>
              <span class="chip chip-cx">${DATA.ALGORITHMS.length} algorithms</span>
            </div>
          </div>
          <div class="paste-detect-panel paste-editor">
            <div id="paste-detect-status" style="display:none;"></div>
            <textarea id="hero-paste-area" spellcheck="false"
              placeholder="def dijkstra(graph, start): ..."></textarea>
            <div class="paste-actions">
              <button id="hero-visualize-btn" class="btn btn-primary"><span>Visualize it →</span></button>
              <button id="hero-clear-btn" class="btn">Clear</button>
            </div>
          </div>
        </div>
      </section>

      <section class="home-last">
        <div class="group-head">
          <span class="eyebrow">Start here</span>
          <a href="#/explore" class="group-head-link">All ${DATA.ALGORITHMS.length} →</a>
        </div>
        <div class="grid-3">
          ${DATA.WORLDS.slice(0, 3).map(world => renderWorldCard(world)).join('')}
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
          // The panel that sits on the monitor's screen once a key is clicked.
          const deck = document.createElement('div');
          deck.className = 'kbd-deck';
          stage.appendChild(deck);
          let deckCtl = null;

          const kbd = initKeyboard(stage, {
            onCount: (n, total) => {
              if (countEl) countEl.textContent = `${n} / ${total}`;
            },
            // Keep the panel glued to the screen for the whole pan.
            onScreenRect: (r) => {
              deck.style.transform = `translate(${r.x}px, ${r.y}px)`;
              deck.style.width  = `${r.w}px`;
              deck.style.height = `${r.h}px`;
            },
            onFocus: (algo) => {
              // The board's corner legend would otherwise show through the
              // screen — it describes gestures that are disabled while focused.
              stage.closest('.hero-kbd')?.classList.add('focused');
              import('./miniEngine.js')
                .then(m => { deckCtl = m.mountMiniEngine(deck, algo, () => kbd.blur()); })
                .catch(e => {
                  console.warn('Mini engine unavailable:', e);
                  kbd.blur();
                });
            },
            onBlur: () => {
              stage.closest('.hero-kbd')?.classList.remove('focused');
              deckCtl?.dispose();
              deckCtl = null;
              deck.classList.remove('on');
              deck.innerHTML = '';
            },
          });

          // Escape backs out of the screen, like any other focused view.
          const onEsc = (e) => { if (e.key === 'Escape' && kbd.isFocused()) kbd.blur(); };
          document.addEventListener('keydown', onEsc);

          // Dispose with the page — hook into the router's DOM teardown
          const mo = new MutationObserver(() => {
            if (!document.body.contains(stage)) {
              deckCtl?.dispose();
              document.removeEventListener('keydown', onEsc);
              kbd.dispose();
              mo.disconnect();
            }
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
              `DETECTED <strong class="detect-name">${res.algorithm.toUpperCase().replace(/_/g,' ')}</strong>` +
              (title ? ` — <em class="detect-world">${title}</em>` : '') +
              `<span class="detect-conf">${conf}%</span>`;
          } catch {
            detectedAlgo = clientDetect(text);
            statusEl.style.display = 'block';
            statusEl.innerHTML =
              `DETECTED (OFFLINE) <strong class="detect-name">${detectedAlgo.toUpperCase().replace(/_/g,' ')}</strong>`;
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
        <div class="page-head">
          <div class="page-head-row">
            <div>
              <span class="eyebrow">Algorithm index</span>
              <h1 class="page-title">Every algorithm</h1>
              <p class="page-lede">All ${DATA.ALGORITHMS.length} trace live on your own input — pick one and watch it run, step by step.</p>
            </div>
            <span id="algo-count" class="transport-count"></span>
          </div>
        </div>

        <div class="explore-controls">
          <label class="explore-search">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path>
            </svg>
            <input id="algo-search" type="search" placeholder="Search algorithms…"
                   autocomplete="off" aria-label="Search algorithms">
          </label>
          <div class="segmented" role="tablist" aria-label="Filter by category">
            ${DATA.ALGO_CATEGORIES.map(cat =>
              `<button type="button" role="tab" data-cat="${cat}">${cat}</button>`).join('')}
          </div>
        </div>

        <div id="algo-groups"></div>
        <p id="algo-empty" class="is-hidden page-lede">No algorithm matches that search.</p>
      </section>
    `,
    mount: (view) => {
      const groupsEl = view.querySelector('#algo-groups');
      const search   = view.querySelector('#algo-search');
      const countEl  = view.querySelector('#algo-count');
      const emptyEl  = view.querySelector('#algo-empty');
      const btns     = view.querySelectorAll('.segmented [data-cat]');
      let cat = 'All';

      const card = (a) => `
        <a href="#/experience?algo=${a.id}" class="world-card algo-card">
          <div class="algo-card-top">
            <span class="algo-card-emoji">${a.emoji}</span>
            <span class="chip chip-cx">${a.complexity}</span>
          </div>
          <h3>${a.name}</h3>
          <p>${a.hook}</p>
        </a>`;

      // Grouping by family turns one undifferentiated wall of 36 into
      // something you can scan. "All" groups; a single category doesn't.
      function render() {
        const q = (search?.value || '').trim().toLowerCase();
        const list = DATA.ALGORITHMS.filter(a =>
          (cat === 'All' || a.category === cat) &&
          (!q || a.name.toLowerCase().includes(q) || a.hook.toLowerCase().includes(q) ||
           a.category.toLowerCase().includes(q) || a.id.includes(q)));

        const families = cat === 'All'
          ? DATA.ALGO_CATEGORIES.filter(c => c !== 'All')
          : [cat];

        groupsEl.innerHTML = families.map(fam => {
          const items = list.filter(a => a.category === fam);
          if (!items.length) return '';
          return `
            <div class="group-head">
              <span class="eyebrow">${fam}</span>
              <span class="transport-count">${items.length}</span>
            </div>
            <div class="grid-3">${items.map(card).join('')}</div>`;
        }).join('');

        if (countEl) countEl.textContent = `${list.length} / ${DATA.ALGORITHMS.length} shown`;
        emptyEl?.classList.toggle('is-hidden', list.length > 0);
        import('./animations.js').then(m => m.revealView(groupsEl));
      }

      const allBtn = view.querySelector('.segmented [data-cat="All"]');
      if (allBtn) { allBtn.classList.add('active'); allBtn.setAttribute('aria-selected', 'true'); }
      btns.forEach(btn => {
        btn.addEventListener('click', () => {
          btns.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');
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
      // Prefer the catalog's real name ("Breadth-First Search") over a
      // title-cased slug ("Bfs"), which reads wrong beside the switcher.
      const entry = DATA.ALGORITHMS.find(a => a.id === algo);
      const displayName = entry
        ? entry.name
        : algo.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      return `
      <section class="experience-section">
        <div class="toolbar">
          <a href="#/explore" class="toolbar-back" aria-label="Back to all algorithms">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M19 12H5"></path><path d="M12 19l-7-7 7-7"></path>
            </svg>
          </a>
          <h1 id="experience-title" class="toolbar-title">${displayName}</h1>
          <label class="toolbar-switch">
            <span class="visually-hidden">Switch algorithm</span>
            <select id="algo-switch">
              ${DATA.ALGO_CATEGORIES.filter(c => c !== 'All').map(cat => `
                <optgroup label="${cat}">
                  ${DATA.ALGORITHMS.filter(a => a.category === cat).map(a =>
                    `<option value="${a.id}"${a.id === algo ? ' selected' : ''}>${a.emoji} ${a.name}</option>`
                  ).join('')}
                </optgroup>`).join('')}
            </select>
          </label>
          <div id="engine-status" class="engine-status-pill">Idle</div>
          <div class="toolbar-spacer"></div>
          <div class="toolbar-actions">
            <button id="run-btn" class="btn btn-primary">▶ Run</button>
            <button id="reset-btn" class="btn">↺ Reset</button>
            <button id="challenge-btn" class="btn">🎮 Challenge</button>
            <span id="combo-chip" class="combo-chip is-hidden">COMBO ×0</span>
          </div>
        </div>

        <div id="scene-hook" class="scene-hook" style="display:none;"></div>

        <div class="workbench">
        <div class="workbench-main">

        <div id="array-controls" class="panel is-hidden" style="margin-bottom:1.5rem;">
          <span class="eyebrow" style="margin-bottom:0.75rem;">YOUR DATA</span>
          <div style="display:flex; gap:0.75rem; flex-wrap:wrap; align-items:center;">
            <input id="array-input" type="text" spellcheck="false"
              placeholder="e.g. 7, 3, 9, 1"
              style="flex:1; min-width:220px; background:rgba(2,4,6,0.9); color:var(--c);
              font-family:var(--font-mono); font-size:1rem; padding:0.6rem 0.9rem;
              border:1px solid var(--panel-border); outline:none; border-radius:0;">
            <span id="target-wrap" style="display:none; align-items:center; gap:0.5rem;
              font-family:var(--font-ui); font-size:0.72rem; color:var(--cDim);">
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

        <div id="graph-controls" class="panel is-hidden" style="margin-bottom:1.5rem;">
          <span class="eyebrow" style="margin-bottom:0.75rem;">YOUR GRAPH</span>
          <div style="display:flex; gap:1.25rem; flex-wrap:wrap; align-items:center;">
            <label style="display:flex; align-items:center; gap:0.5rem;
              font-family:var(--font-ui); font-size:0.72rem; color:var(--cDim);">
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
              font-family:var(--font-ui); font-size:0.72rem; color:var(--cDim);">
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

        <div id="engine-panel">
          <div id="engine-view" class="stage">
            <svg id="engine-svg" viewBox="0 0 760 280"></svg>
          </div>

          <div class="transport">
            <div class="transport-btns">
              <button id="prev-btn" class="transport-btn" aria-label="Previous step" disabled>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M15 18l-6-6 6-6"></path></svg>
              </button>
              <button id="play-btn" class="transport-btn primary" aria-label="Play" disabled>
                <svg class="icon-play" width="11" height="11" viewBox="0 0 24 24"
                     fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"></path></svg>
                <svg class="icon-pause" width="11" height="11" viewBox="0 0 24 24"
                     fill="currentColor" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"></path></svg>
              </button>
              <button id="step-btn" class="transport-btn" aria-label="Next step" disabled>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M9 18l6-6-6-6"></path></svg>
              </button>
            </div>

            <div id="scrub-row" class="transport-scrub" style="display:none;">
              <input type="range" id="step-slider" min="0" max="0" value="0" aria-label="Step">
            </div>
            <div id="step-counter" class="transport-count"></div>

            <select id="speed-select" class="transport-speed" aria-label="Playback speed">
              <option value="0.5">0.5×</option>
              <option value="1" selected>1×</option>
              <option value="2">2×</option>
            </select>

            <div class="transport-sep"></div>
            <div id="counter-panel" class="counters" style="display:none;"></div>
          </div>

          <!-- Reserved height: the note changes every step, and a growing
               box used to shove the whole page down as the trace ran. -->
          <div class="narration">
            <div id="engine-note" style="opacity:0;"></div>
          </div>
        </div>

        <div id="compare-panel" class="panel is-hidden" style="margin-bottom:1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;
            margin-bottom:1rem; flex-wrap:wrap; gap:0.75rem;">
            <span class="eyebrow" style="margin:0;">SAME GRAPH · TWO ALGORITHMS</span>
            <div style="display:flex; gap:0.5rem; align-items:center;">
              <button id="compare-prev" class="btn btn-ghost" style="font-size:0.8rem; padding:0.35rem 0.7rem;">←</button>
              <button id="compare-play" class="btn btn-ghost" style="font-size:0.8rem; padding:0.35rem 0.7rem;">▶</button>
              <button id="compare-next" class="btn btn-ghost" style="font-size:0.8rem; padding:0.35rem 0.7rem;">→</button>
              <span id="compare-step-label" style="font-family:var(--font-ui); font-size:0.72rem; color:var(--cDim);"></span>
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
                <span id="compare-total-${side}" style="font-family:var(--font-ui); font-size:0.72rem; color:var(--cDim);"></span>
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

        </div><!-- /workbench-main -->

        <aside class="workbench-rail">
          <div id="complexity-card" class="rail-panel is-hidden">
            <div class="rail-panel-head">
              <span class="eyebrow">Complexity</span>
              <span class="eyebrow rail-panel-aside">What am I paying?</span>
            </div>
            <div id="complexity-rows"></div>
            <p id="complexity-live" class="rail-reading" style="display:none;"></p>
          </div>

          <div class="rail-panel">
            <div class="rail-panel-head">
              <span class="eyebrow">Narration</span>
              <select id="level-select" title="Narration level" aria-label="Narration level">
                <option value="beginner" selected>Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <button id="explain-btn" class="btn btn-ghost rail-btn">✦ Explain this step</button>
            <div id="explanation-box" class="rail-reading is-hidden"></div>
          </div>

          <details class="rail-panel">
            <summary class="rail-summary">⚙ What-if — adjust edge weights</summary>
            <div id="whatif-controls"></div>
          </details>

          <button id="compare-btn" class="btn rail-btn is-hidden">⚖ Compare two algorithms</button>

          <div class="rail-panel">
            <span class="eyebrow" style="display:block; margin-bottom:0.75rem;">Try another</span>
            <div class="rail-chips">
              ${DATA.WORLDS.slice(0,4).map(w => `
                <a href="#/experience?algo=${w.algo || 'dijkstra'}" class="btn rail-chip">
                  ${w.emoji} ${w.metaphor}
                </a>`).join('')}
            </div>
          </div>
        </aside>
      </div><!-- /workbench -->
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
      ${(() => {
        const totalProblems = DATA.A2Z_STEPS.reduce((s, st) => s + (st.problems || []).length, 0);
        const doneProblems  = P.stats().completed;
        const stepsDone     = DATA.A2Z_STEPS.filter(st => P.stepProgress(st.problems) >= 100).length;

        // The first step that isn't finished is where the student actually is.
        const currentIdx = DATA.A2Z_STEPS.findIndex(st => P.stepProgress(st.problems) < 100);
        const resumeIdx  = currentIdx === -1 ? DATA.A2Z_STEPS.length - 1 : currentIdx;
        const resumeStep = DATA.A2Z_STEPS[resumeIdx];
        const resumeProb = (resumeStep.problems || []).find(p => P.getStatus(p.id) !== 'completed')
                        || (resumeStep.problems || [])[0];

        return `
      <section>
        <div class="workbench">
          <div class="workbench-main">
            <div class="page-head">
              <span class="eyebrow">Complete roadmap</span>
              <h1 class="page-title">A2Z mastery path</h1>
              <p class="page-lede">${DATA.A2Z_STEPS.length} steps, ${totalProblems} problems, in order. Each one opens a metaphor scene you can step through — not a wall of links.</p>
            </div>

            <div class="step-rail">
              ${DATA.A2Z_STEPS.map((step, idx) => {
                const probs = step.problems || [];
                const pct   = P.stepProgress(probs);
                const done  = probs.filter(p => P.getStatus(p.id) === 'completed').length;
                const state = pct >= 100 ? 'done' : (idx === resumeIdx ? 'current' : '');
                const first = probs[0];
                return `
                <div class="step-row${state === '' && idx > resumeIdx ? ' locked' : ''}">
                  <div class="step-dot ${state}">${
                    state === 'done'
                      ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                             stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                           <path d="M20 6L9 17l-5-5"></path></svg>`
                      : idx + 1
                  }</div>
                  <div class="step-body">
                    <div class="step-head">
                      <a class="step-link" href="#/a2z-problem?step=${idx+1}&prob=${step.step.replace('Step ','')}-1">
                        <span class="step-name">${step.title}</span>
                      </a>
                      <span class="step-meta">${step.step} · ${probs.length} problems</span>
                      <span class="step-pct">${pct >= 100 ? '100%' : (pct > 0 ? pct + '%' : 'Not started')}</span>
                    </div>
                    <div class="bar"><span style="width:${pct}%;"></span></div>
                    ${idx === resumeIdx ? `
                    <div class="step-problems">
                      ${probs.slice(0, 5).map(p => {
                        const isDone = P.getStatus(p.id) === 'completed';
                        const isNext = !isDone && p.id === resumeProb?.id;
                        return `
                        <a class="prob-item${isNext ? ' current' : ''}"
                           href="#/a2z-problem?step=${idx+1}&prob=${p.id}">
                          ${isDone
                            ? `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#34d399"
                                   stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                 <path d="M20 6L9 17l-5-5"></path></svg>`
                            : `<span class="prob-dot${isNext ? ' next' : ''}"></span>`}
                          <span class="prob-item-name">${p.title}</span>
                          <span class="prob-item-world">${p.world}</span>
                          <span class="chip chip-${(p.difficulty || 'E').toLowerCase()}">${p.difficulty}</span>
                        </a>`;
                      }).join('')}
                      ${probs.length > 5
                        ? `<a class="prob-item prob-more" href="#/a2z-problem?step=${idx+1}&prob=${probs[5].id}">
                             <span class="prob-item-name">+ ${probs.length - 5} more in this step</span></a>`
                        : ''}
                    </div>` : ''}
                  </div>
                </div>`;
              }).join('')}
            </div>
          </div>

          <aside class="workbench-rail">
            <div class="rail-panel rail-resume">
              <span class="eyebrow" style="display:block; margin-bottom:0.75rem;">Pick up where you left off</span>
              <span class="resume-title">${resumeProb ? resumeProb.title : resumeStep.title}</span>
              <span class="resume-meta">${resumeStep.step} · ${resumeProb ? resumeProb.world : ''}</span>
              <a class="btn btn-primary rail-btn"
                 href="#/a2z-problem?step=${resumeIdx+1}&prob=${resumeProb ? resumeProb.id : ''}">Continue →</a>
            </div>

            <div class="rail-panel">
              <span class="eyebrow" style="display:block; margin-bottom:0.85rem;">Overall</span>
              <div class="overall-count">
                <strong>${doneProblems}</strong>
                <span>of ${totalProblems} problems</span>
              </div>
              <div class="bar" style="height:4px; margin-bottom:0.85rem;">
                <span style="width:${totalProblems ? Math.round(doneProblems / totalProblems * 100) : 0}%;"></span>
              </div>
              <div class="overall-split">
                <div><span class="counter-num">${P.stats().streak ?? 0}</span><span class="counter-label">Day streak</span></div>
                <div><span class="counter-num">${stepsDone} / ${DATA.A2Z_STEPS.length}</span><span class="counter-label">Steps done</span></div>
              </div>
            </div>
          </aside>
        </div>
      </section>`;
      })()}
    `,
    mount: (view) => {
      if (typeof gsap === 'undefined') return;
      view.querySelectorAll('.step-row').forEach((row, i) => {
        gsap.from(row, {
          opacity: 0,
          y: 14,
          duration: 0.4,
          delay: i * 0.05,
          ease: 'power2.out',
          clearProps: 'all'
        });
      });
    }
  },

  "#/a2z-problem": {
    title: "AlgoVision · Problem Visualizer",
    html: (params) => `
      <section class="experience-section">
        <!-- Breadcrumb carries the identity, so the scene starts immediately below. -->
        <nav class="crumbs" aria-label="Breadcrumb">
          <a href="#/a2z" class="crumb-back" aria-label="Back to A2Z">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M19 12H5"></path><path d="M12 19l-7-7 7-7"></path>
            </svg>
          </a>
          <a href="#/a2z">A2Z</a>
          <span class="crumb-sep">/</span>
          <span id="step-title"></span>
          <span class="crumb-sep">/</span>
          <h1 id="prob-title" class="crumb-current"></h1>
          <span id="prob-difficulty" class="chip"></span>
          <span class="toolbar-spacer"></span>
          <span id="prob-id-label" class="transport-count"></span>
        </nav>

        <div class="prob-layout" id="prob-layout">
          <aside class="panel prob-sidebar">
            <div class="prob-sidebar-head">
              <span class="eyebrow">This step</span>
            </div>
            <div id="prob-list"></div>
          </aside>

          <div id="viz-panel" class="workbench-main">
            <div id="viz-inner" class="stage"></div>

            <div class="transport">
              <div class="transport-btns">
                <button id="scene-step-back" class="transport-btn" aria-label="Previous step" disabled>
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                       stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M15 18l-6-6 6-6"></path></svg>
                </button>
                <button id="scene-step-fwd" class="transport-btn primary" aria-label="Next step">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                       stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M9 18l6-6-6-6"></path></svg>
                </button>
              </div>
              <span id="scene-step-counter" class="transport-count">1 / ?</span>
              <span class="toolbar-spacer"></span>
              <span id="prob-world" class="chip chip-cat"></span>
            </div>

            <div class="narration">
              <p id="scene-narration"></p>
            </div>

            <div class="panel prob-actions">
              <p id="prob-hook"></p>
              <div class="prob-actions-btns">
                <button id="prev-prob" class="btn">← Previous</button>
                <button id="mark-understood" class="btn">☐ Mark understood</button>
                <button id="next-prob" class="btn btn-primary">Next →</button>
                <a id="practice-link" href="#/practice" class="btn">🐞 Practice</a>
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

          // Status marker markup lives in one place so the sidebar and the
          // "mark understood" button can't drift apart.
          function statusMark(pid) {
            const st = P.getStatus(pid);
            if (st === 'completed') {
              return `<svg class="prob-status" data-pid="${pid}" width="13" height="13" viewBox="0 0 24 24"
                        fill="none" stroke="var(--ok)" stroke-width="2.2" stroke-linecap="round"
                        stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"></path></svg>`;
            }
            return `<span class="prob-status prob-dot${st === 'viewed' ? ' seen' : ''}" data-pid="${pid}"></span>`;
          }

          function refreshStatusMarker(pid) {
            const el = view.querySelector(`.prob-status[data-pid="${pid}"]`);
            if (!el) return;
            const wrapper = document.createElement('div');
            wrapper.innerHTML = statusMark(pid);
            el.replaceWith(wrapper.firstElementChild);
          }

          function renderStep(si) {
            const step = DATA.A2Z_STEPS[si];
            stepTitleEl.textContent = `${step.step} · ${step.title}`;
            // Steps run to 47 problems, so break the list on the sheet's own
            // sub-sections rather than presenting one undifferentiated scroll.
            let lastSection = null;
            probListEl.innerHTML = (step.problems || []).map((p, pi) => {
              const header = p.section && p.section !== lastSection
                ? `<div class="prob-section">${p.section}</div>` : '';
              lastSection = p.section || lastSection;
              return header + `
              <div class="prob-item" data-pi="${pi}" role="button" tabindex="0">
                ${statusMark(p.id)}
                <span class="prob-item-name">${p.title}</span>
                <span class="chip chip-${(p.difficulty || 'E').toLowerCase()}">${p.difficulty}</span>
              </div>`;
            }).join('');

            probListEl.querySelectorAll('.prob-item').forEach(el => {
              const open = () => {
                currentProbIdx = parseInt(el.dataset.pi);
                renderProblem(currentStepIdx, currentProbIdx);
              };
              el.addEventListener('click', open);
              el.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
              });
            });
          }

          function renderProblem(si, pi) {
            const step = DATA.A2Z_STEPS[si];
            const prob = (step.problems || [])[pi];
            if (!prob) return;

            // Highlight active problem in sidebar
            view.querySelectorAll('.prob-item').forEach((el, i) => {
              el.classList.toggle('current', i === pi);
            });

            // Update metadata
            const probIdLabel = view.querySelector('#prob-id-label');
            const probTitle   = view.querySelector('#prob-title');
            const probDiff    = view.querySelector('#prob-difficulty');
            const probWorld   = view.querySelector('#prob-world');
            const probHook    = view.querySelector('#prob-hook');

            if (probIdLabel) probIdLabel.textContent = prob.id;
            if (probTitle)   probTitle.textContent   = prob.title;
            if (probDiff) {
              const diffMap = { E:'Easy', M:'Medium', H:'Hard' };
              probDiff.textContent = diffMap[prob.difficulty] || prob.difficulty;
              // Semantic colour comes from the chip class, not an inline style.
              probDiff.className = `chip chip-${(prob.difficulty || 'E').toLowerCase()}`;
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
                muBtn.textContent = done ? '✓ Understood' : '☐ Mark understood';
                muBtn.classList.toggle('btn-done', done);
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
        <div class="page-head">
          <span class="eyebrow">AI debugger</span>
          <h1 class="page-title">Practice &amp; debug</h1>
          <p class="page-lede">Paste any DSA code. AlgoVision detects the algorithm and the AI scans for bugs.</p>
        </div>
        <div id="practice-grid" class="practice-grid">
          <div class="panel practice-editor">
            <div class="practice-editor-head">
              <span class="eyebrow">Code editor</span>
              <label class="practice-lang">
                <span class="visually-hidden">Language</span>
                <select id="lang-select">
                  <option value="python">Python</option>
                  <option value="cpp">C++</option>
                  <option value="java">Java</option>
                  <option value="javascript">JavaScript</option>
                </select>
              </label>
            </div>
            <textarea id="code-area" spellcheck="false"></textarea>
            <div id="detect-result" style="display:none;"></div>
            <button id="find-bug-btn" class="btn btn-primary">Scan for bugs</button>
            <div id="bug-result" style="display:none;"></div>
          </div>

          <aside class="panel">
            <span class="eyebrow" style="display:block; margin-bottom:1rem;">Pro tips</span>
            <div class="tip-list">
              ${[
                ['Trace by hand first', 'Before running, manually walk through 2–3 examples.'],
                ['Check edge cases', 'Empty arrays, single elements, max values — test them all.'],
                ['Think in metaphors', 'Visualize the algorithm as a real-world process.'],
                ['Complexity matters', 'O(n²) may pass small tests but fail large inputs.'],
              ].map(([title, desc]) => `
                <div class="tip">
                  <span class="tip-title">${title}</span>
                  <span class="tip-desc">${desc}</span>
                </div>
              `).join('')}
            </div>
          </aside>
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
        <div class="page-head">
          <span class="eyebrow">Knowledge graph</span>
          <h1 class="page-title">Algorithm family tree</h1>
          <p class="page-lede">Algorithms don't exist in isolation — see how each one descends from, generalizes, or improves upon another.</p>
        </div>
        <div class="panel" style="padding:0;">
          <div id="family-svg-wrapper" style="overflow:auto;">
            <svg id="family-svg" viewBox="0 0 900 580"
              style="width:100%; min-width:900px; display:block;"></svg>
          </div>
        </div>
        <div id="family-info" class="panel" style="margin-top:1.5rem; display:none;">
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
        <div class="page-head">
          <span class="eyebrow">Daily broadcast</span>
          <h1 class="page-title">60-second insights</h1>
          <p class="page-lede">Quick deep-dives into algorithm concepts — one insight at a time.</p>
        </div>
        <div class="grid-3">
          ${DATA.CLIPS.map((clip, i) => `
            <div class="panel panel-glow clip-card">
              <div class="clip-card-top">
                <span class="chip chip-cx">${clip.tag}</span>
                <span class="clip-card-num">${(i+1).toString().padStart(2,'0')}</span>
              </div>
              <span class="eyebrow">${clip.topic}</span>
              <h3>${clip.title}</h3>
              <span class="clip-card-cta">Read more →</span>
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
        <div class="page-head">
          <span class="eyebrow">Progress dashboard</span>
          <h1 class="page-title">My journey</h1>
          <p class="page-lede">Your real progress — tracked in this browser as you explore, trace, and understand.</p>
        </div>
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

      function tile(label, value, current, target) {
        const pct = Math.min((current / target) * 100, 100);
        return `
          <div class="panel stat-tile">
            <span class="eyebrow">${label}</span>
            <span class="stat-tile-num">${value}</span>
            <div class="stat-bar-bg"><div class="stat-bar-fill" style="width:${pct}%;"></div></div>
            <span class="stat-tile-target">Target: ${target}</span>
          </div>`;
      }

      function renderStats() {
        if (!P.hasAnyActivity()) {
          content.innerHTML = `
            <div class="panel" style="text-align:center; padding:3rem 2rem;">
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
          ${tile('Problems understood', s.completed, s.completed, totalProblems)}
          ${tile('Traces run', s.tracesRun, s.tracesRun, 50)}
          ${tile('Streak', `${s.streak} day${s.streak === 1 ? '' : 's'}`, s.streak, 30)}
          ${tile('Mastery score', `${s.points} pts`, s.points, 1000)}
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
        <div class="page-head">
          <span class="eyebrow">System mappings</span>
          <h1 class="page-title">Algorithms in the wild</h1>
          <p class="page-lede">These aren't just textbook concepts — they power the products you use every day.</p>
        </div>
        <div class="grid-3">
          ${DATA.REALWORLD.map(item => `
            <div class="panel panel-glow info-card">
              <span class="info-card-icon">${item.icon}</span>
              <span class="eyebrow">${item.metaphor}</span>
              <h3>${item.title}</h3>
              <p>${item.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/404": {
    title: "AlgoVision · 404",
    html: () => `
      <section class="page-404">
        <span class="page-404-num">404</span>
        <span class="eyebrow">Node not found</span>
        <h1 class="page-title">Off the graph</h1>
        <p class="page-lede">You've wandered into untraced territory.</p>
        <a href="#/" class="btn btn-primary">Return to root →</a>
      </section>
    `
  }
};
