import * as DATA from './data.js';

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
      <section class="hero">
        <div class="hero-eyebrow">ALGORITHM VISUALIZATION ENGINE · A2Z ROADMAP</div>
        <h1 class="hero-title">
          <span class="hero-line hero-line-outline">SEE THE</span>
          <span class="hero-line hero-line-accent">ALGO-</span>
          <span class="hero-line hero-line-filled">RITHM</span>
        </h1>
        <p class="hero-sub">Turn complex data structures into cinematic visual journeys — real-world metaphors, live step-by-step traces, and AI-powered explanations.</p>
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="hero-stat-num">450+</span>
            <span class="hero-stat-label">Problems</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat-num">16</span>
            <span class="hero-stat-label">Steps</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat-num">40+</span>
            <span class="hero-stat-label">3D Scenes</span>
          </div>
          <div class="hero-stat">
            <span class="hero-stat-num">9</span>
            <span class="hero-stat-label">Algo Worlds</span>
          </div>
        </div>
        <div class="hero-cta">
          <a href="#/explore" class="btn btn-primary">Start Exploring →</a>
          <a href="#/a2z" class="btn btn-ghost">A2Z Roadmap</a>
        </div>
      </section>

      <div class="marquee-wrap">
        <div class="marquee" id="marquee-inner">
          ${[...DATA.MARQUEE, ...DATA.MARQUEE, ...DATA.MARQUEE].map(m => `<span>${m}</span>`).join('')}
        </div>
      </div>

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
        <div class="panel" style="max-width:680px; margin:0 auto; padding:3rem 2.5rem; border-top:3px solid var(--cAccent);">
          <div class="section-label">
            <span class="eyebrow" style="margin:0;">QUICK START</span>
          </div>
          <h2 style="margin-bottom:0.75rem; font-family:var(--font-display2); font-size:clamp(1.8rem,3vw,2.5rem); letter-spacing:0.04em;">PASTE ANY DSA CODE</h2>
          <p style="margin:0 0 2rem;">AlgoVision detects the algorithm and launches the cinematic experience automatically.</p>
          <div class="paste-detect-panel">
            <div id="paste-detect-status" style="display:none; font-family:var(--font-mono);
              font-size:1rem; color:var(--c); margin-bottom:1rem; padding:0.6rem 1rem;
              border-left:3px solid var(--cAccent); background:rgba(255,107,0,0.04);">
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
      const marquee = view.querySelector('#marquee-inner');
      if (marquee && typeof gsap !== 'undefined') {
        gsap.to(marquee, { xPercent: -33.33, duration: 28, ease: 'none', repeat: -1 });
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
    title: "AlgoVision · Explore Worlds",
    html: () => `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">WORLD SELECTION</span>
        </div>
        <h1 style="font-family:var(--font-display2); font-size:clamp(3rem,7vw,6rem); letter-spacing:0.04em; margin-bottom:0.5rem;">ALGORITHM WORLDS</h1>
        <p style="margin-bottom:2.5rem;">Each world frames a classic algorithm as a real-world story. Click any card to watch it run live.</p>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:2.5rem;">
          ${DATA.CATEGORIES.map(cat => `<button class="btn filter-btn" data-cat="${cat}">${cat}</button>`).join('')}
        </div>
        <div class="grid-3" id="worlds-grid">
          ${DATA.WORLDS.map(w => renderWorldCard(w)).join('')}
        </div>
      </section>
    `,
    mount: (view) => {
      const grid = view.querySelector('#worlds-grid');
      const btns = view.querySelectorAll('.filter-btn');
      const allBtn = view.querySelector('.filter-btn[data-cat="All"]');
      if (allBtn) allBtn.classList.add('active');
      btns.forEach(btn => {
        btn.addEventListener('click', () => {
          btns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const cat = btn.dataset.cat;
          const filtered = cat === "All" ? DATA.WORLDS : DATA.WORLDS.filter(w => w.category === cat);
          grid.innerHTML = filtered.map(w => renderWorldCard(w)).join('');
          import('./animations.js').then(m => m.revealView(grid));
        });
      });
    }
  },

  "#/experience": {
    title: "AlgoVision · Live Engine",
    html: (params) => {
      const algo = params.get('algo') || 'dijkstra';
      const displayName = algo.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      return `
      <section>
        <div class="section-label">
          <span class="eyebrow" style="margin:0;">LIVE EXECUTION ENGINE</span>
        </div>
        <h1 id="experience-title" style="font-family:var(--font-display2); font-size:clamp(3rem,6vw,5rem); letter-spacing:0.04em;">${displayName.toUpperCase()}</h1>

        <div id="scene-hook" style="display:none; font-family:var(--font-mono);
          font-size:1.05rem; color:var(--cDim); margin-bottom:2rem; padding:0.85rem 1.25rem;
          border-left:3px solid var(--cAccent); background:rgba(255,107,0,0.04);">
        </div>

        <div class="panel" style="margin-bottom:1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;
            margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
            <div style="display:flex; align-items:center; gap:1rem;">
              <div id="engine-status" class="eyebrow" style="margin:0;">STATUS: IDLE</div>
              <div id="step-counter" style="font-family:var(--font-pixel); font-size:7px; color:var(--cDim);"></div>
            </div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <button id="run-btn" class="btn btn-primary" style="font-size:0.85rem;">▶ RUN</button>
              <button id="step-btn" class="btn btn-ghost" style="font-size:0.85rem;" disabled>STEP →</button>
              <button id="reset-btn" class="btn" style="font-size:0.85rem;">↺ RESET</button>
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

          <details style="margin-top:1.25rem; border-top:1px solid var(--panel-border); padding-top:1rem;">
            <summary style="font-family:var(--font-body); font-size:0.8rem; font-weight:600;
              color:var(--inkDim); cursor:pointer; list-style:none; user-select:none;">
              ⚙ What-If Mode — Adjust edge weights
            </summary>
            <div id="whatif-controls" style="margin-top:1rem; display:flex; flex-direction:column; gap:0.75rem;"></div>
          </details>
        </div>

        <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-start;">
          <button id="explain-btn" class="btn btn-ghost" style="flex-shrink:0;">✦ AI NARRATE</button>
          <div id="explanation-box" class="panel" style="flex:1; display:none;
            font-family:var(--font-mono); font-size:1rem; color:var(--c);
            border-color:rgba(0,212,255,0.3); min-width:180px;">
          </div>
        </div>

        <div style="margin-top:2rem; display:flex; gap:0.75rem; flex-wrap:wrap; align-items:center;">
          <span style="font-size:0.8rem; color:var(--inkDim); font-family:var(--font-pixel); font-size:7px; letter-spacing:0.1em;">TRY ANOTHER:</span>
          ${DATA.WORLDS.slice(0,4).map(w => `
            <a href="#/experience?algo=${w.algo || 'dijkstra'}" class="btn" style="font-size:0.8rem; padding:0.4rem 0.8rem;">
              ${w.emoji} ${w.metaphor}
            </a>
          `).join('')}
        </div>
      </section>
    `},
    mount: (view, params) => {
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
            <span class="journey-stat-num">${Math.round(DATA.A2Z_STEPS.reduce((s,st)=>s+st.progress,0)/DATA.A2Z_STEPS.length)}%</span>
            <span class="journey-stat-label">Avg Progress</span>
          </div>
          <div class="journey-stat">
            <span class="journey-stat-num">40+</span>
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
              <div class="a2z-card-count">${(step.problems||[]).length} problems</div>
              <div class="a2z-progress-bar">
                <div class="a2z-progress-fill" style="width:${step.progress}%;"></div>
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
              font-family:var(--font-pixel); font-size:7px; color:var(--cDim);"></div>
            <div id="prob-list" style="overflow-y:auto; max-height:70vh;"></div>
          </div>

          <div id="viz-panel" style="min-width:0; display:flex; flex-direction:column; gap:1.25rem;">
            <div id="viz-inner" style="width:100%; min-height:320px;
              background:#02060a; border:1px solid var(--panel-border);
              position:relative; overflow:hidden;">
            </div>

            <div class="panel" style="padding:1rem 1.25rem; border-top:2px solid var(--cAccent);">
              <div style="display:flex; align-items:center; gap:0.75rem;
                margin-bottom:0.75rem; flex-wrap:wrap;">
                <button id="scene-step-back" class="btn btn-ghost"
                  style="font-size:0.85rem; padding:0.4rem 0.8rem;" disabled>
                  ← PREV STEP
                </button>
                <span id="scene-step-counter"
                  style="font-family:var(--font-pixel); font-size:8px;
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
                <span style="font-family:var(--font-pixel); font-size:7px;
                  color:var(--cDim);">REAL WORLD:</span>
                <span id="prob-world"
                  style="font-family:var(--font-mono); font-size:1.1rem; color:var(--c);">
                </span>
              </div>
              <p id="prob-hook"
                style="font-family:var(--font-mono); font-size:1rem;
                color:var(--inkDim); border-left:3px solid var(--cAccent);
                padding-left:1rem; margin-bottom:1.5rem; max-width:none;">
              </p>
              <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
                <button id="prev-prob" class="btn btn-ghost" style="font-size:0.85rem;">
                  ← PREV PROBLEM
                </button>
                <button id="next-prob" class="btn btn-primary" style="font-size:0.85rem;">
                  NEXT PROBLEM →
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

          function renderStep(si) {
            const step = DATA.A2Z_STEPS[si];
            stepTitleEl.textContent = `${step.step}: ${step.title}`;
            probListEl.innerHTML = (step.problems||[]).map((p, pi) => {
              const cols = { E:'var(--cDim)', M:'var(--c)', H:'var(--cAccent)' };
              return `<div class="prob-item" data-pi="${pi}" style="
                padding:0.7rem 1.25rem; border-bottom:1px solid var(--panel-border);
                cursor:pointer; display:flex; align-items:center; gap:0.75rem;
                transition:background 0.15s; font-size:0.875rem; border-left:2px solid transparent;">
                <span style="font-family:var(--font-pixel); font-size:6px; color:${cols[p.difficulty]};
                  min-width:10px;">${p.difficulty}</span>
                <span style="color:var(--ink); flex:1;">${p.title}</span>
              </div>`;
            }).join('');
            probListEl.querySelectorAll('.prob-item').forEach(el => {
              el.addEventListener('mouseenter', () => el.style.background='rgba(0,212,255,0.04)');
              el.addEventListener('mouseleave', () => { if (el.dataset.pi != currentProbIdx) el.style.background=''; });
              el.addEventListener('click', () => {
                currentProbIdx = parseInt(el.dataset.pi);
                renderProblem(currentStepIdx, currentProbIdx);
              });
            });
          }

          function renderProblem(si, pi) {
            const step = DATA.A2Z_STEPS[si];
            const prob = (step.problems||[])[pi];
            if (!prob) return;

            view.querySelectorAll('.prob-item').forEach((el, i) => {
              el.style.background = i===pi ? 'rgba(255,107,0,0.06)' : '';
              el.style.borderLeft = i===pi ? '2px solid var(--cAccent)' : '2px solid transparent';
            });

            const probIdLabel = view.querySelector('#prob-id-label');
            const probTitle   = view.querySelector('#prob-title');
            const probDiff    = view.querySelector('#prob-difficulty');
            const probWorld   = view.querySelector('#prob-world');
            const probHook    = view.querySelector('#prob-hook');

            if (probIdLabel) probIdLabel.textContent = `PROBLEM ${prob.id}`;
            if (probTitle)   probTitle.textContent   = prob.title;
            if (probDiff) {
              const diffMap = { E:'EASY', M:'MEDIUM', H:'HARD' };
              const colMap  = { E:'var(--cDim)', M:'var(--c)', H:'var(--cAccent)' };
              probDiff.textContent = diffMap[prob.difficulty] || prob.difficulty;
              probDiff.style.color = colMap[prob.difficulty] || 'var(--c)';
            }
            if (probWorld) probWorld.textContent = prob.world;
            if (probHook)  probHook.textContent  = `"${prob.hook}"`;

            history.replaceState(null,'',`#/a2z-problem?step=${si+1}&prob=${prob.id}`);

            const vizInner = view.querySelector('#viz-inner');
            if (!vizInner) return;

            if (vizInner._vizAutoInterval) {
              clearInterval(vizInner._vizAutoInterval);
              vizInner._vizAutoInterval = null;
            }
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

            const stepBackBtn   = view.querySelector('#scene-step-back');
            const stepFwdBtn    = view.querySelector('#scene-step-fwd');
            const stepCounter   = view.querySelector('#scene-step-counter');
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
          <div class="panel" style="border-top:3px solid var(--cAccent);">
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
              border:1px solid rgba(0,212,255,0.2);
              display:none; color:var(--cBright); font-family:var(--font-mono); font-size:1rem;
              background:rgba(0,212,255,0.03); line-height:1.7;"></div>
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
                  <span style="color:var(--cAccent); font-family:var(--font-condensed); font-weight:700; font-size:1.1rem; flex-shrink:0; margin-top:0.1rem;">${icon}</span>
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
        <div id="family-info" class="panel" style="margin-top:1.5rem; display:none; border-top:3px solid var(--cAccent);">
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
        { id:'dp',        label:'Dynamic Programming',x:140, y:420, emoji:'💾', desc:'Optimal substructure + overlapping subproblems = memoization.', color:'var(--cAccent)', algo:'dp' },
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
            <div class="panel panel-glow" style="cursor:pointer; border-top:3px solid ${i%2===0?'var(--cAccent)':'var(--c)'};">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
                <span style="font-family:var(--font-pixel); font-size:7px; color:var(--c);">${clip.tag}</span>
                <span style="font-family:var(--font-display2); font-size:1.5rem; color:rgba(0,212,255,0.15);">${(i+1).toString().padStart(2,'0')}</span>
              </div>
              <span class="eyebrow" style="margin-bottom:0.5rem; color:var(--cDim);">${clip.topic}</span>
              <h3 style="font-size:0.95rem; line-height:1.4;">${clip.title}</h3>
              <div style="margin-top:1.25rem; font-family:var(--font-condensed); font-size:0.85rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--cAccent);">Read more →</div>
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
        <p style="margin-bottom:2.5rem;">Track your mastery across algorithms, topics, and practice sessions.</p>
        <div class="grid-2">
          ${DATA.STATS.map((stat, i) => {
            const raw = stat.value.split('/')[0].split(' ')[0];
            const num = parseFloat(raw);
            const pct = isNaN(num) ? 0 : Math.min((num / stat.target) * 100, 100);
            return `
            <div class="panel" style="border-top:3px solid ${i%2===0?'var(--cAccent)':'var(--c)'};">
              <span class="eyebrow" style="margin-bottom:0.5rem;">${stat.label.toUpperCase()}</span>
              <div style="font-family:var(--font-display2); font-size:5rem; color:var(--ink); margin:0.25rem 0; letter-spacing:0.02em; line-height:1;">${stat.value}</div>
              <div class="stat-bar-bg">
                <div class="stat-bar-fill" style="width:${pct}%;"></div>
              </div>
              <div style="font-size:0.75rem; color:var(--inkDim); margin-top:0.5rem;">Target: ${stat.target}</div>
            </div>`;
          }).join('')}
        </div>
      </section>
    `
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
              <div style="position:absolute; bottom:0; left:0; width:${20+i*15}%; height:2px; background:var(--cAccent); opacity:0.4;"></div>
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
        <div style="font-family:var(--font-display2); font-size:12rem; color:rgba(255,107,0,0.08); line-height:1; margin-bottom:-2rem;">404</div>
        <span class="eyebrow" style="color:var(--cAccent); margin-bottom:1rem;">NODE NOT FOUND</span>
        <h1 style="font-family:var(--font-display2); font-size:3rem; letter-spacing:0.04em; margin-bottom:1rem;">OFF THE GRAPH</h1>
        <p style="margin:0 auto 2rem;">You've wandered into untraced territory.</p>
        <a href="#/" class="btn btn-primary">Return to Root →</a>
      </section>
    `
  }
};
