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
  "#/": "default",
  "#/explore": "default",
  "#/experience": "default",
  "#/family": "default",
  "#/a2z": "default",
  "#/a2z-problem": "default",
  "#/today": "default",
  "#/practice": "default",
  "#/journey": "default",
  "#/realworld": "default"
};

function renderWorldCard(world) {
  return `
    <a href="#/experience?algo=${world.algo || 'dijkstra'}" style="text-decoration:none; color:inherit; display:block;">
      <div class="panel panel-glow" style="height:100%;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.25rem;">
          <span style="font-size:2rem;">${world.emoji}</span>
          <span style="font-family:var(--font-pixel); font-size:7px; color:var(--cDim); border:1px solid var(--panel-border); padding:3px 7px;">${world.complexity}</span>
        </div>
        <span class="eyebrow" style="margin-bottom:0.4rem;">${world.metaphor}</span>
        <h3 style="margin-bottom:0.6rem; font-size:1.05rem;">${world.name}</h3>
        <p style="font-size:0.85rem; color:var(--inkDim);">${world.hook}</p>
        <div style="margin-top:1.25rem; display:flex; align-items:center; gap:0.4rem; color:var(--cDim); font-size:0.75rem; font-weight:600;">
          <span>Visualize</span>
          <span>→</span>
        </div>
      </div>
    </a>
  `;
}

export const PAGES = {
  "#/": {
    title: "AlgoVision · See the algorithm before the code",
    html: () => `
      <section class="hero" style="padding-top:0;">
        <span class="eyebrow" style="margin-bottom:1.5rem;">ALGORITHM VISUALIZATION ENGINE</span>
        <h1 style="max-width:16ch; margin:0 auto 1.5rem;">See the Algorithm.<br>Master the Story.</h1>
        <p style="margin:0 auto 2.5rem;">Turn complex data structures into cinematic visual journeys — real-world metaphors, live step-by-step traces, and AI-powered explanations.</p>
        <div class="hero-cta">
          <a href="#/explore" class="btn btn-primary" style="font-size:0.85rem; padding:0.75rem 2rem;">Start Exploring →</a>
          <a href="#/a2z" class="btn btn-ghost" style="font-size:0.85rem; padding:0.75rem 2rem;">View A2Z Roadmap</a>
        </div>
      </section>

      <section style="padding-top:0; padding-bottom:1.5rem;">
        <div class="marquee-wrap">
          <div class="marquee" id="marquee-inner">
            ${[...DATA.MARQUEE, ...DATA.MARQUEE].map(m => `<span>${m}</span>`).join('')}
          </div>
        </div>
      </section>

      <section>
        <span class="eyebrow">HOW IT WORKS</span>
        <h2 style="margin-bottom:2rem;">Three Acts, One Insight</h2>
        <div class="grid-3">
          ${DATA.ACTS.map(act => `
            <div class="panel panel-glow">
              <div style="font-family:var(--font-pixel); font-size:8px; color:var(--c); margin-bottom:1rem;">${act.icon}</div>
              <h3 style="margin-bottom:0.6rem;">${act.title}</h3>
              <p style="font-size:0.875rem;">${act.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <section>
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2rem; flex-wrap:wrap; gap:1rem;">
          <div>
            <span class="eyebrow">FEATURED WORLDS</span>
            <h2 style="margin:0;">Pick your algorithm</h2>
          </div>
          <a href="#/explore" class="btn btn-ghost" style="font-size:0.8rem;">View all →</a>
        </div>
        <div class="grid-3">
          ${DATA.WORLDS.slice(0, 3).map(world => renderWorldCard(world)).join('')}
        </div>
      </section>

      <section style="text-align:center; padding-bottom:6rem;">
        <div class="panel" style="max-width:640px; margin:0 auto; padding:3rem 2.5rem;">
          <span class="eyebrow" style="margin-bottom:1.5rem;">QUICK START</span>
          <h2 style="margin-bottom:1rem;">Paste any DSA code</h2>
          <p style="margin:0 auto 2rem;">AlgoVision detects the algorithm and launches the cinematic experience automatically.</p>
          <div class="paste-detect-panel" style="text-align:left;">
            <div id="paste-detect-status" style="display:none; font-family:var(--font-mono);
              font-size:1rem; color:var(--c); margin-bottom:1rem; padding:0.6rem 1rem;
              border-left:2px solid var(--c); background:rgba(95,214,230,0.04);">
            </div>
            <textarea id="hero-paste-area"
              style="width:100%; height:130px; background:rgba(4,9,14,0.8); color:var(--c);
              font-family:var(--font-mono); font-size:1.1rem; padding:1rem;
              border:1px solid var(--panel-border); outline:none; resize:none;
              border-radius:2px; transition:border-color 0.3s;"
              placeholder="def dijkstra(graph, start): ..."></textarea>
            <div style="display:flex; gap:0.75rem; margin-top:0.75rem;">
              <button id="hero-visualize-btn" class="btn btn-primary" style="flex:1; font-size:0.8rem;"><span>DETECT & VISUALIZE →</span></button>
              <button id="hero-clear-btn" class="btn btn-ghost" style="font-size:0.8rem;">Clear</button>
            </div>
          </div>
        </div>
      </section>
    `,
    mount: (view) => {
      const marquee = view.querySelector('#marquee-inner');
      if (marquee && typeof gsap !== 'undefined') {
        gsap.to(marquee, { xPercent: -50, duration: 32, ease: 'none', repeat: -1 });
      }

      const pasteArea    = view.querySelector('#hero-paste-area');
      const statusEl     = view.querySelector('#paste-detect-status');
      const visualizeBtn = view.querySelector('#hero-visualize-btn');
      const clearBtn     = view.querySelector('#hero-clear-btn');

      if (!pasteArea || !visualizeBtn) {
        console.error('AlgoVision: paste panel elements not found in DOM');
        return;
      }

      let detectedAlgo = null;
      let detectTimer  = null;

      pasteArea.addEventListener('input', () => {
        clearTimeout(detectTimer);
        const text = pasteArea.value.trim();
        if (text.length < 20) {
          statusEl.style.display = 'none';
          detectedAlgo = null;
          return;
        }
        detectTimer = setTimeout(async () => {
          try {
            const { api } = await import('./api.js');
            const res  = await api.detect(text);
            detectedAlgo = res.algorithm;
            const conf  = Math.round((res.confidence || 0) * 100);
            const title = res.realworld?.title || '';
            statusEl.style.display = 'block';
            statusEl.innerHTML =
              `DETECTED: <strong style="color:var(--cBright)">${res.algorithm.toUpperCase().replace(/_/g,' ')}</strong>` +
              (title ? `<span style="color:var(--cDim);margin:0 0.5rem;">—</span><em style="color:var(--cDim)">${title}</em>` : '') +
              `<span style="color:var(--cDim);margin-left:0.75rem;">(${conf}% confidence)</span>`;
          } catch {
            detectedAlgo = clientDetect(text);
            statusEl.style.display = 'block';
            statusEl.innerHTML =
              `DETECTED (OFFLINE): <strong style="color:var(--cBright)">${detectedAlgo.toUpperCase().replace(/_/g,' ')}</strong>`;
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
          if (detectedAlgo) {
            window.location.hash = `#/experience?algo=${detectedAlgo}`;
            return;
          }
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
        <span class="eyebrow">WORLD SELECTION</span>
        <h1>Algorithm Worlds</h1>
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
        <span class="eyebrow">LIVE EXECUTION ENGINE</span>
        <h1 id="experience-title">${displayName}</h1>

        <div id="scene-hook" style="display:none; font-family:var(--font-mono);
          font-size:1.05rem; color:var(--cDim); margin-bottom:2rem; padding:0.85rem 1.25rem;
          border-left:2px solid var(--c); background:rgba(95,214,230,0.04); border-radius:2px;">
        </div>

        <div class="panel" style="margin-bottom:1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;
            margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
            <div style="display:flex; align-items:center; gap:1rem;">
              <div id="engine-status" class="eyebrow" style="margin:0;">STATUS: IDLE</div>
              <div id="step-counter" style="font-family:var(--font-pixel); font-size:7px; color:var(--cDim);"></div>
            </div>
            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              <button id="run-btn" class="btn btn-primary" style="font-size:0.8rem;">▶ Run</button>
              <button id="step-btn" class="btn btn-ghost" style="font-size:0.8rem;" disabled>Step →</button>
              <button id="reset-btn" class="btn" style="font-size:0.8rem;">↺ Reset</button>
            </div>
          </div>

          <div id="engine-view" style="min-height:300px;">
            <svg id="engine-svg" viewBox="0 0 760 280"
              style="width:100%; height:100%; min-height:300px; display:block;"></svg>
            <div id="engine-note" style="padding:0.75rem 1.25rem; opacity:0; transition:0.3s;
              font-family:var(--font-mono); font-size:1.05rem;
              border-top:1px solid var(--panel-border); background:rgba(4,9,14,0.9); color:var(--c);">
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
          <button id="explain-btn" class="btn btn-ghost" style="flex-shrink:0; font-size:0.8rem;">✦ AI Narrate</button>
          <div id="explanation-box" class="panel" style="flex:1; display:none;
            font-family:var(--font-mono); font-size:1rem; color:var(--c);
            border-color:rgba(95,214,230,0.3); min-width:180px;">
          </div>
        </div>

        <div style="margin-top:2rem; display:flex; gap:0.75rem; flex-wrap:wrap; align-items:center;">
          <span style="font-size:0.8rem; color:var(--inkDim);">Try another:</span>
          ${DATA.WORLDS.slice(0,4).map(w => `
            <a href="#/experience?algo=${w.algo || 'dijkstra'}" class="btn" style="font-size:0.75rem; padding:0.4rem 0.8rem;">
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
      <div class="scroll-progress">
        ${DATA.A2Z_STEPS.map(() => `<div class="scroll-segment"></div>`).join('')}
      </div>
      <div class="journey-container">
        <div class="journey-track-wrapper">
          <div class="journey-track">
            <div class="rail-bg"><div class="rail-fill"></div></div>
            ${DATA.A2Z_STEPS.map((step, idx) => {
              const diffs = ['E', 'M', 'H'];
              const diff = diffs[idx % 3];
              const diffColors = { E: 'var(--cDim)', M: 'var(--c)', H: 'var(--cBright)' };
              const diffLabels = { E: 'Easy', M: 'Medium', H: 'Hard' };
              return `
              <div class="station" data-index="${idx + 1}">
                <div class="station-dot"></div>
                <a href="#/a2z-problem?step=${idx+1}&prob=${step.step.replace('Step ','')}-1"
                   style="text-decoration:none; color:inherit; display:block;" class="station-card">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                    <span style="font-family:var(--font-pixel); font-size:7px; color:var(--cDim);">${step.step}</span>
                    <span style="font-family:var(--font-pixel); font-size:6px; color:${diffColors[diff]};
                      border:1px solid ${diffColors[diff]}; padding:2px 5px;">${diffLabels[diff]}</span>
                  </div>
                  <h3 style="font-size:0.9rem; margin-bottom:0.75rem;">${step.title}</h3>
                  <div style="font-size:0.75rem; color:var(--inkDim); margin-bottom:0.5rem;">${(step.problems||[]).length} problems</div>
                  <div style="height:2px; background:var(--cDeep); border-radius:2px; overflow:hidden;">
                    <div style="width:${step.progress}%; height:100%; background:var(--c);"></div>
                  </div>
                </a>
              </div>`;
            }).join('')}
          </div>
        </div>
      </div>
    `,
    mount: (view) => {
      const track = view.querySelector('.journey-track');
      const stations = view.querySelectorAll('.station');
      const railFill = view.querySelector('.rail-fill');
      const segments = view.querySelectorAll('.scroll-segment');

      if (window.innerWidth <= 860) return;

      ScrollTrigger.create({
        trigger: ".journey-container",
        start: "top top",
        end: () => `+=${track.offsetWidth}`,
        pin: true,
        scrub: 1,
        onUpdate: (self) => {
          const p = self.progress;
          gsap.set(track, { x: -p * (track.offsetWidth - window.innerWidth) });
          gsap.set(railFill, { width: `${p * 100}%` });
          const activeIdx = Math.floor(p * stations.length);
          segments.forEach((s, i) => s.classList.toggle('active', i <= activeIdx));
          stations.forEach((s, i) => s.classList.toggle('active', i === activeIdx));
        }
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
          <div>
            <div id="viz-container" class="panel" style="min-height:240px; margin-bottom:1.5rem;
              display:flex; align-items:center; justify-content:center; padding:1.5rem;">
              <div id="viz-inner" style="width:100%;"></div>
            </div>
            <div class="panel panel-glow" style="border-color:rgba(95,214,230,0.25);">
              <div style="display:flex; justify-content:space-between; align-items:flex-start;
                flex-wrap:wrap; gap:1rem; margin-bottom:1.25rem;">
                <div>
                  <span class="eyebrow" id="prob-id-label" style="margin-bottom:0.25rem;"></span>
                  <h2 id="prob-title" style="margin:0; font-size:1.3rem;"></h2>
                </div>
                <span id="prob-difficulty" style="font-family:var(--font-pixel); font-size:7px;
                  padding:4px 10px; border:1px solid currentColor; align-self:flex-start;"></span>
              </div>
              <div style="display:flex; gap:0.75rem; align-items:center; margin-bottom:1rem; flex-wrap:wrap;">
                <span style="font-family:var(--font-pixel); font-size:7px; color:var(--cDim);">REAL WORLD:</span>
                <span id="prob-world" style="font-family:var(--font-mono); font-size:1.1rem; color:var(--c);"></span>
              </div>
              <p id="prob-hook" style="font-family:var(--font-mono); font-size:1rem;
                color:var(--inkDim); border-left:2px solid var(--cDeep); padding-left:1rem;
                margin-bottom:1.5rem; max-width:none;"></p>
              <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
                <button id="prev-prob" class="btn btn-ghost" style="font-size:0.8rem;">← Prev</button>
                <button id="next-prob" class="btn btn-primary" style="font-size:0.8rem;">Next →</button>
                <a id="practice-link" href="#/practice" class="btn" style="margin-left:auto; font-size:0.8rem;">🐞 Practice</a>
              </div>
            </div>
          </div>
        </div>
      </section>
    `,
    mount: (view, params) => {
      import('./vizScenes.js').then(({ VIZ_SCENES }) => {
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
          const vizInner    = view.querySelector('#viz-inner');
          const probIdLabel = view.querySelector('#prob-id-label');
          const probTitle   = view.querySelector('#prob-title');
          const probDiff    = view.querySelector('#prob-difficulty');
          const probWorld   = view.querySelector('#prob-world');
          const probHook    = view.querySelector('#prob-hook');
          const prevBtn     = view.querySelector('#prev-prob');
          const nextBtn     = view.querySelector('#next-prob');

          function renderStep(si) {
            const step = DATA.A2Z_STEPS[si];
            stepTitleEl.textContent = `${step.step}: ${step.title}`;
            probListEl.innerHTML = (step.problems||[]).map((p, pi) => {
              const cols = { E:'var(--cDim)', M:'var(--c)', H:'var(--cBright)' };
              return `<div class="prob-item" data-pi="${pi}" style="
                padding:0.7rem 1.25rem; border-bottom:1px solid var(--panel-border);
                cursor:pointer; display:flex; align-items:center; gap:0.75rem;
                transition:background 0.15s; font-size:0.875rem;">
                <span style="font-family:var(--font-pixel); font-size:6px; color:${cols[p.difficulty]};
                  min-width:10px;">${p.difficulty}</span>
                <span style="color:var(--ink); flex:1;">${p.title}</span>
              </div>`;
            }).join('');
            probListEl.querySelectorAll('.prob-item').forEach(el => {
              el.addEventListener('mouseenter', () => el.style.background='rgba(95,214,230,0.04)');
              el.addEventListener('mouseleave', () => el.style.background='');
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
              el.style.background = i===pi ? 'rgba(95,214,230,0.06)' : '';
              el.style.borderLeft = i===pi ? '2px solid var(--c)' : '2px solid transparent';
            });

            probIdLabel.textContent = `PROBLEM ${prob.id}`;
            probTitle.textContent   = prob.title;
            const diffMap = { E:'EASY', M:'MEDIUM', H:'HARD' };
            const colMap  = { E:'var(--cDim)', M:'var(--c)', H:'var(--cBright)' };
            probDiff.textContent    = diffMap[prob.difficulty];
            probDiff.style.color    = colMap[prob.difficulty];
            probWorld.textContent   = prob.world;
            probHook.textContent    = `"${prob.hook}"`;

            vizInner.innerHTML = '';
            try {
              const scene = VIZ_SCENES[prob.viz] || VIZ_SCENES.default;
              scene.draw(vizInner, prob);
            } catch (e) {
              if (!vizInner.firstChild) {
                vizInner.innerHTML = '<div style="height:240px;display:flex;align-items:center;justify-content:center;color:#2a7f8c;font-family:monospace;font-size:11px;opacity:0.5;">[ 3D VISUALIZATION — OPEN IN BROWSER ]</div>';
              }
            }

            history.replaceState(null, '', `#/a2z-problem?step=${si+1}&prob=${prob.id}`);
            const activeItem = view.querySelector(`.prob-item[data-pi="${pi}"]`);
            if (activeItem) activeItem.scrollIntoView({ block:'nearest', behavior:'smooth' });
          }

          prevBtn.addEventListener('click', () => {
            if (currentProbIdx > 0) {
              currentProbIdx--;
            } else if (currentStepIdx > 0) {
              currentStepIdx--;
              currentProbIdx = (DATA.A2Z_STEPS[currentStepIdx].problems||[]).length - 1;
              renderStep(currentStepIdx);
            }
            renderProblem(currentStepIdx, currentProbIdx);
          });

          nextBtn.addEventListener('click', () => {
            const probs = DATA.A2Z_STEPS[currentStepIdx].problems||[];
            if (currentProbIdx < probs.length - 1) {
              currentProbIdx++;
            } else if (currentStepIdx < DATA.A2Z_STEPS.length - 1) {
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
        <span class="eyebrow">AI DEBUGGER</span>
        <h1>Practice & Debug</h1>
        <p style="margin-bottom:2.5rem;">Paste any DSA code. AlgoVision detects the algorithm and the AI scans for bugs.</p>
        <div id="practice-grid" style="display:grid; grid-template-columns:2fr 1fr; gap:1.5rem;">
          <div class="panel panel-glow">
            <span class="eyebrow" style="margin-bottom:1.25rem;">CODE EDITOR</span>
            <div style="display:flex; gap:1rem; align-items:center; margin-bottom:1rem;">
              <label style="font-size:0.8rem; color:var(--inkDim);">Language:</label>
              <select id="lang-select" style="background:var(--bg1); border:1px solid var(--panel-border);
                color:var(--ink); font-family:var(--font-body); font-size:0.8rem; padding:0.35rem 0.6rem;
                border-radius:2px; outline:none;">
                <option value="python">Python</option>
                <option value="cpp">C++</option>
                <option value="java">Java</option>
                <option value="javascript">JavaScript</option>
              </select>
            </div>
            <textarea id="code-area" style="width:100%; height:320px; background:rgba(4,9,14,0.9);
              color:var(--c); font-family:var(--font-mono); font-size:1.1rem; padding:1.25rem;
              border:1px solid var(--panel-border); outline:none; resize:vertical; border-radius:2px;
              line-height:1.5;"></textarea>
            <div id="detect-result" style="display:none; margin-top:0.75rem; padding:0.6rem 1rem;
              border:1px solid var(--panel-border); font-size:0.85rem; color:var(--inkDim);
              border-radius:2px; font-family:var(--font-body);">
            </div>
            <button id="find-bug-btn" class="btn btn-primary" style="margin-top:1rem; width:100%; font-size:0.85rem;">
              Scan for Bugs
            </button>
            <div id="bug-result" style="margin-top:1.25rem; padding:1.25rem; border:1px solid rgba(95,214,230,0.2);
              display:none; color:var(--cBright); font-family:var(--font-mono); font-size:1rem;
              border-radius:2px; background:rgba(95,214,230,0.03); line-height:1.7;"></div>
          </div>
          <div class="panel">
            <span class="eyebrow" style="margin-bottom:1.5rem;">PRO TIPS</span>
            <div style="display:flex; flex-direction:column; gap:1.25rem;">
              ${[
                ['🔍', 'Trace by hand first', 'Before running, manually walk through 2–3 examples.'],
                ['🎯', 'Check edge cases', 'Empty arrays, single elements, max values — test them all.'],
                ['📐', 'Think in metaphors', 'Visualize the algorithm as a real-world process.'],
                ['⏱️', 'Complexity matters', 'O(n²) may pass small tests but fail large inputs.'],
              ].map(([icon, title, desc]) => `
                <div style="display:flex; gap:0.75rem; align-items:flex-start;">
                  <span style="font-size:1.1rem; flex-shrink:0; margin-top:0.1rem;">${icon}</span>
                  <div>
                    <div style="font-size:0.85rem; font-weight:600; color:var(--ink); margin-bottom:0.2rem;">${title}</div>
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
        <span class="eyebrow">KNOWLEDGE GRAPH</span>
        <h1>Algorithm Family Tree</h1>
        <p style="margin-bottom:2rem;">Algorithms don't exist in isolation — see how each one descends from, generalizes, or improves upon another.</p>
        <div class="panel" style="padding:0;">
          <div id="family-svg-wrapper" style="overflow:auto;">
            <svg id="family-svg" viewBox="0 0 900 580"
              style="width:100%; min-width:900px; display:block;"></svg>
          </div>
        </div>
        <div id="family-info" class="panel panel-glow" style="margin-top:1.5rem; display:none; border-color:rgba(95,214,230,0.3);">
          <h3 id="family-info-title" style="color:var(--cBright); margin-bottom:0.4rem;"></h3>
          <p id="family-info-desc" style="font-size:0.875rem; margin-bottom:1rem; max-width:none;"></p>
          <a id="family-info-link" href="#/" class="btn btn-ghost" style="font-size:0.8rem;">Visualize this →</a>
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
        { id:'dp',        label:'Dynamic Programming',x:140, y:420, emoji:'💾', desc:'Optimal substructure + overlapping subproblems = memoization.', color:'var(--cBright)', algo:'dp' },
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
        line.setAttribute("stroke","rgba(58,154,170,0.25)"); line.setAttribute("stroke-width","1.5");
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
        <span class="eyebrow">DAILY BROADCAST</span>
        <h1>60-Second Insights</h1>
        <p style="margin-bottom:2.5rem;">Quick deep-dives into algorithm concepts — one insight at a time.</p>
        <div class="grid-3">
          ${DATA.CLIPS.map((clip, i) => `
            <div class="panel panel-glow" style="cursor:pointer;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
                <span style="font-family:var(--font-pixel); font-size:7px; color:var(--c);">${clip.tag}</span>
                <span style="font-family:var(--font-pixel); font-size:7px; color:var(--cDim);">${(i+1).toString().padStart(2,'0')}</span>
              </div>
              <span class="eyebrow" style="margin-bottom:0.5rem; color:var(--cDim);">${clip.topic}</span>
              <h3 style="font-size:0.95rem; line-height:1.4;">${clip.title}</h3>
              <div style="margin-top:1.25rem; font-size:0.75rem; color:var(--cDim); font-weight:600;">Read more →</div>
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
        <span class="eyebrow">PROGRESS DASHBOARD</span>
        <h1>My Journey</h1>
        <p style="margin-bottom:2.5rem;">Track your mastery across algorithms, topics, and practice sessions.</p>
        <div class="grid-2">
          ${DATA.STATS.map(stat => {
            const raw = stat.value.split('/')[0].split(' ')[0];
            const num = parseFloat(raw);
            const pct = isNaN(num) ? 0 : Math.min((num / stat.target) * 100, 100);
            return `
            <div class="panel panel-glow">
              <span class="eyebrow" style="margin-bottom:0.5rem;">${stat.label.toUpperCase()}</span>
              <div style="font-size:3.5rem; font-weight:700; font-family:var(--font-display);
                color:var(--ink); margin:0.25rem 0; letter-spacing:-1px;">${stat.value}</div>
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
        <span class="eyebrow">SYSTEM MAPPINGS</span>
        <h1>Algorithms in the Wild</h1>
        <p style="margin-bottom:2.5rem;">These aren't just textbook concepts — they power the products you use every day.</p>
        <div class="grid-3">
          ${DATA.REALWORLD.map(item => `
            <div class="panel panel-glow">
              <div style="font-size:2.25rem; margin-bottom:1.25rem;">${item.icon}</div>
              <span class="eyebrow" style="margin-bottom:0.4rem; color:var(--cDim);">${item.metaphor.toUpperCase()}</span>
              <h3 style="margin-bottom:0.6rem;">${item.title}</h3>
              <p style="font-size:0.875rem;">${item.desc}</p>
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
        <span class="eyebrow" style="color:#ff5f5f; margin-bottom:1rem;">ERROR 404</span>
        <h1 style="margin-bottom:1rem;">Node Not Found</h1>
        <p style="margin:0 auto 2rem;">You've wandered off the graph into untraced territory.</p>
        <a href="#/" class="btn btn-primary">Return to Root →</a>
      </section>
    `
  }
};
