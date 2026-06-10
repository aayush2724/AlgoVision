import * as DATA from './data.js';

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

const TOPIC_NAMES = {
  "Sorting": "The Leaderboard",
  "Binary Search": "The Hunt",
  "Recursion": "The Fractal Mirror",
  "Trees": "The Family Tree",
  "Graphs": "Six Degrees",
  "Heaps": "The Priority Line",
  "DP": "The Memo Vault",
  "Greedy": "The Local Hero",
  "Backtracking": "The Maze Runner"
};

export const PAGES = {
  "#/": {
    title: "AlgoVision &middot; Home",
    html: (params) => `
      <section class="hero" style="text-align: center; padding-top: 10vh;">
        <span class="eyebrow">BLUEPRINT v2.0.6</span>
        <h1>See the Algorithm.<br/>Master the Story.</h1>
        <p style="margin: 0 auto 2rem;">We turn complex data structures into cinematic visual journeys. No more dry slides — just pure intuition.</p>
        <div class="hero-cta">
          <a href="#/explore" class="btn btn-primary">Start Exploring</a>
          <a href="#/a2z" class="btn btn-ghost" style="margin-left: 1rem;">View Roadmap</a>
        </div>

        <div class="paste-detect-panel panel panel-glow"
          style="margin: 3rem auto; max-width: 800px; width:100%;">
          <span class="eyebrow">⚡ INSTANT VISUALIZER</span>
          <p style="margin-bottom:1.5rem; font-size:0.9rem;">
            Paste any DSA code or problem statement — AlgoVision detects
            the algorithm and launches the cinematic experience.
          </p>
          <div id="paste-detect-status"
            style="display:none; font-family:var(--font-mono); font-size:0.9rem;
            color:var(--c); margin-bottom:1rem; padding:0.5rem;
            border-left:2px solid var(--c);">
          </div>
          <textarea id="hero-paste-area"
            style="width:100%; height:160px; background:#041014; color:var(--c);
            font-family:var(--font-mono); font-size:1rem; padding:1.2rem;
            border:1px solid var(--cDeep); outline:none; resize:vertical;
            transition:border-color 0.3s;"
            placeholder="Paste code or problem... e.g. 'def dijkstra(graph, start):'"
          ></textarea>
          <div style="display:flex; gap:1rem; margin-top:1rem; flex-wrap:wrap;">
            <button id="hero-visualize-btn" class="btn btn-primary" style="flex:1;">
              DETECT &amp; VISUALIZE →
            </button>
            <button id="hero-clear-btn" class="btn btn-ghost">CLEAR</button>
          </div>
        </div>
      </section>
      
      <section>
        <div class="grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
          ${DATA.ACTS.map(act => `
            <div class="panel panel-glow">
              <span class="eyebrow">${act.icon} PHASE</span>
              <h3>${act.title}</h3>
              <p>${act.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <section style="overflow: hidden; padding: 4rem 0;">
        <div class="marquee" style="display: flex; gap: 4rem; white-space: nowrap;">
          ${[...DATA.MARQUEE, ...DATA.MARQUEE].map(m => `<span style="font-family: var(--font-display); font-size: 4rem; font-weight: 700; opacity: 0.1; color: var(--c);">${m}</span>`).join('')}
        </div>
      </section>
    `,
    mount: (view) => {
      // Existing marquee
      const marquee = view.querySelector('.marquee');
      if (marquee) gsap.to(marquee, { xPercent: -50, duration: 30, ease: "none", repeat: -1 });

      // Hero paste detect
      const pasteArea = view.querySelector('#hero-paste-area');
      const status = view.querySelector('#paste-detect-status');
      const visualizeBtn = view.querySelector('#hero-visualize-btn');
      const clearBtn = view.querySelector('#hero-clear-btn');

      let detectedAlgo = null;
      let detectTimer = null;

      if (pasteArea) {
        pasteArea.addEventListener('focus', () => {
          pasteArea.style.borderColor = 'var(--c)';
        });
        pasteArea.addEventListener('blur', () => {
          pasteArea.style.borderColor = 'var(--cDeep)';
        });

        pasteArea.addEventListener('input', () => {
          clearTimeout(detectTimer);
          if (pasteArea.value.length < 15) {
            status.style.display = 'none';
            detectedAlgo = null;
            return;
          }
          detectTimer = setTimeout(async () => {
            try {
              import('./api.js').then(async ({ api }) => {
                const res = await api.detect(pasteArea.value);
                detectedAlgo = res.algorithm;
                const conf = Math.round(res.confidence * 100);
                status.style.display = 'block';
                status.innerHTML = `DETECTED: <strong style="color:var(--cBright)">
                  ${res.algorithm.toUpperCase().replace(/_/g,' ')}
                </strong> — <em style="color:var(--cDim)">
                  ${res.realworld?.title || ''}
                </em> <span style="color:var(--cDim); margin-left:0.5rem;">(${conf}% confidence)</span>`;
              });
            } catch { /* silent */ }
          }, 700);
        });
      }

      if (visualizeBtn) {
        visualizeBtn.addEventListener('click', () => {
          if (!pasteArea?.value.trim()) return;
          if (detectedAlgo) {
            window.location.hash = `#/experience?algo=${detectedAlgo}`;
          } else {
            // Detect first, then navigate
            import('./api.js').then(async ({ api }) => {
              try {
                const res = await api.detect(pasteArea.value);
                window.location.hash = `#/experience?algo=${res.algorithm}`;
              } catch {
                window.location.hash = '#/experience?algo=dijkstra';
              }
            });
          }
        });
      }

      if (clearBtn) {
        clearBtn.addEventListener('click', () => {
          if (pasteArea) pasteArea.value = '';
          if (status) status.style.display = 'none';
          detectedAlgo = null;
        });
      }
    }
  },

  "#/explore": {
    title: "Explore Worlds",
    html: (params) => `
      <section>
        <span class="eyebrow">WORLD SELECTION</span>
        <h1>Algorithm Worlds</h1>
        <div class="filters" style="display: flex; gap: 1rem; margin-bottom: 3rem;">
          ${DATA.CATEGORIES.map(cat => `<button class="btn btn-ghost filter-btn" data-cat="${cat}">${cat}</button>`).join('')}
        </div>
        <div class="grid" id="worlds-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
          ${DATA.WORLDS.map(world => renderWorldCard(world)).join('')}
        </div>
      </section>
    `,
    mount: (view) => {
      const grid = view.querySelector('#worlds-grid');
      const btns = view.querySelectorAll('.filter-btn');
      btns.forEach(btn => {
        btn.addEventListener('click', () => {
          btns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const cat = btn.dataset.cat;
          const filtered = cat === "All" ? DATA.WORLDS : DATA.WORLDS.filter(w => w.category === cat);
          grid.innerHTML = filtered.map(world => renderWorldCard(world)).join('');
          import('./animations.js').then(m => m.revealView(grid));
        });
      });
      // Set "All" as default active
      const allBtn = view.querySelector('.filter-btn[data-cat="All"]');
      if (allBtn) allBtn.classList.add('active');
    }
  },

  "#/experience": {
    title: "The Live Engine",
    html: (params) => {
      const algo = params.get('algo') || 'dijkstra';
      const displayName = algo.toUpperCase().replace(/[-_]/g, ' ');
      return `
      <section>
        <span class="eyebrow">LIVE EXECUTION ENGINE</span>
        <h1 id="experience-title">${displayName}</h1>
        <div id="scene-hook" style="display:none; font-family:var(--font-mono);
          font-size:1.1rem; color:var(--c); margin-bottom:2rem; padding:1rem;
          border-left:2px solid var(--c); background:rgba(95,214,230,0.04);">
        </div>

        <div class="panel panel-glow" style="margin-bottom:2rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
            <div style="display:flex; align-items:center; gap:1.5rem;">
              <div id="engine-status" class="eyebrow" style="margin:0;">STATUS: IDLE</div>
              <div id="step-counter" style="font-family:var(--font-pixel); font-size:8px; color:var(--cDim);"></div>
            </div>
            <div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
              <button id="run-btn" class="btn btn-primary">▶ RUN</button>
              <button id="step-btn" class="btn btn-ghost" disabled>STEP →</button>
              <button id="reset-btn" class="btn btn-ghost">↺ RESET</button>
            </div>
          </div>

          <div id="engine-view" style="background:var(--bg1); border:1px solid var(--cDeep);
            min-height:320px; position:relative;">
            <svg id="engine-svg" viewBox="0 0 800 300"
              style="width:100%; height:100%; min-height:320px;"></svg>
            <div id="engine-note" class="panel" style="position:absolute; bottom:0; left:0;
              right:0; padding:0.8rem 1rem; pointer-events:none; opacity:0; transition:0.3s;
              font-family:var(--font-mono); font-size:1rem; border-top:1px solid var(--cDeep);
              background:rgba(3,10,16,0.9); color:var(--c);">
            </div>
          </div>

          <details style="margin-top:1.5rem; border-top:1px solid var(--cDeep); padding-top:1rem;">
            <summary style="font-family:var(--font-pixel); font-size:9px;
              color:var(--cDim); cursor:pointer; list-style:none;">
              ⚙ WHAT IF MODE — ADJUST EDGE WEIGHTS
            </summary>
            <div id="whatif-controls" style="margin-top:1rem; display:flex;
              flex-direction:column; gap:0.8rem;">
            </div>
          </details>
        </div>

        <div style="display:flex; gap:1.5rem; flex-wrap:wrap;">
          <button id="explain-btn" class="btn btn-ghost" style="flex-shrink:0; height:fit-content;">
            ✦ AI NARRATE
          </button>
          <div id="explanation-box" class="panel" style="flex:1; display:none;
            font-family:var(--font-mono); font-size:0.95rem; color:var(--c);
            border-color:var(--c); min-width:200px;">
          </div>
        </div>
      </section>
    `},
    mount: (view, params) => {
      import('./engine.js').then(m => m.mountEngine(view, params.get('algo') || 'dijkstra'));
    }
  },

  "#/a2z": {
    title: "A2Z Journey",
    html: (params) => `
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
              const diffColor = diff === 'E' ? 'var(--cDim)' : (diff === 'M' ? 'var(--c)' : 'var(--cBright)');
              return `
              <div class="station" data-index="${idx + 1}">
                <div class="station-dot"></div>
                <a href="#/a2z-problem?step=${idx+1}&prob=${step.step.replace('Step ','')}-1"
                   style="text-decoration:none; color:inherit; display:block;"
                   class="station-card">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span class="eyebrow" style="margin: 0;">${step.step}</span>
                    <span style="font-family: var(--font-pixel); font-size: 8px; color: ${diffColor}; border: 1px solid ${diffColor}; padding: 2px 4px;">${diff}</span>
                  </div>
                  <h3 style="margin-bottom: 1rem;">${step.title}</h3>
                  <span class="eyebrow" style="font-size: 8px; color: var(--cDim);">${(step.problems||[]).length} PROBLEMS</span>
                  <div style="height: 6px; background: var(--cDeep); overflow: hidden; margin-top: 0.5rem;">
                    <div style="width: ${step.progress}%; height: 100%; background: var(--c); box-shadow: 0 0 10px var(--c);"></div>
                  </div>
                </a>
              </div>
            `;}).join('')}
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
    title: "Problem Visualizer",
    html: (params) => {
      const stepId  = params.get('step')    || '1';
      const probId  = params.get('prob')    || '1-1';
      return `
        <section>
          <span class="eyebrow">← <a href="#/a2z" style="color:var(--cDim);text-decoration:none;">A2Z JOURNEY</a> &nbsp;/&nbsp; PROBLEM VISUALIZER</span>
  
          <div style="display:grid; grid-template-columns:300px 1fr; gap:2rem; margin-top:2rem;" id="prob-layout">
  
            <!-- LEFT: Problem list -->
            <div class="panel" style="padding:0; overflow:hidden;">
              <div id="step-title" style="padding:1rem 1.5rem; border-bottom:1px solid var(--cDeep);
                font-family:var(--font-pixel); font-size:9px; color:var(--cDim);"></div>
              <div id="prob-list" style="overflow-y:auto; max-height:70vh;"></div>
            </div>
  
            <!-- RIGHT: Visualization + details -->
            <div>
              <div id="viz-container" class="panel" style="min-height:260px; margin-bottom:1.5rem;
                display:flex; align-items:center; justify-content:center; padding:1.5rem;
                position:relative; overflow:hidden;">
                <div id="viz-scanlines" style="position:absolute;inset:0;
                  background:repeating-linear-gradient(0deg,transparent,transparent 2px,
                  rgba(3,10,16,0.12) 2px,rgba(3,10,16,0.12) 3px);
                  pointer-events:none; z-index:2;"></div>
                <div id="viz-inner" style="width:100%; position:relative; z-index:1;"></div>
              </div>
  
              <div class="panel panel-glow" style="border-color:var(--c);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.5rem;">
                  <div>
                    <span class="eyebrow" id="prob-id-label" style="margin-bottom:0.3rem;"></span>
                    <h2 id="prob-title" style="margin:0;"></h2>
                  </div>
                  <span id="prob-difficulty" style="font-family:var(--font-pixel); font-size:9px;
                    padding:0.3rem 0.8rem; border:1px solid currentColor;"></span>
                </div>
  
                <div style="display:flex; gap:1rem; margin-bottom:1rem; align-items:center; flex-wrap:wrap;">
                  <span style="font-family:var(--font-pixel); font-size:8px; color:var(--cDim);">🌍 REAL WORLD:</span>
                  <span id="prob-world" style="font-family:var(--font-mono); font-size:1.1rem; color:var(--c);"></span>
                </div>
  
                <p id="prob-hook" style="font-family:var(--font-mono); font-size:1.1rem;
                  color:var(--cDim); border-left:2px solid var(--cDeep); padding-left:1rem;
                  margin-bottom:1.5rem;"></p>
  
                <div style="display:flex; gap:1rem; flex-wrap:wrap;">
                  <button id="prev-prob" class="btn btn-ghost">← PREV</button>
                  <button id="next-prob" class="btn btn-primary">NEXT →</button>
                  <a id="practice-link" href="#/practice" class="btn btn-ghost"
                    style="margin-left:auto;">🐞 PRACTICE</a>
                </div>
              </div>
            </div>
          </div>
        </section>
      `;
    },
    mount: (view, params) => {
      import('./vizScenes.js').then(({ VIZ_SCENES }) => {
        import('./data.js').then((DATA) => {
          let currentStepIdx = 0;
          let currentProbIdx = 0;
  
          // Find initial problem
          const targetProbId = params.get('prob') || '1-1';
          DATA.A2Z_STEPS.forEach((step, si) => {
            (step.problems||[]).forEach((p, pi) => {
              if (p.id === targetProbId) { currentStepIdx=si; currentProbIdx=pi; }
            });
          });
  
          const stepTitleEl   = view.querySelector('#step-title');
          const probListEl    = view.querySelector('#prob-list');
          const vizInner      = view.querySelector('#viz-inner');
          const probIdLabel   = view.querySelector('#prob-id-label');
          const probTitle     = view.querySelector('#prob-title');
          const probDiff      = view.querySelector('#prob-difficulty');
          const probWorld     = view.querySelector('#prob-world');
          const probHook      = view.querySelector('#prob-hook');
          const prevBtn       = view.querySelector('#prev-prob');
          const nextBtn       = view.querySelector('#next-prob');
  
          function renderStep(si) {
            const step = DATA.A2Z_STEPS[si];
            stepTitleEl.textContent = `${step.step}: ${step.title}`;
            probListEl.innerHTML = (step.problems||[]).map((p, pi) => {
              const diffCol = p.difficulty==='E'?'var(--cDim)':p.difficulty==='M'?'var(--c)':'var(--cBright)';
              return `<div class="prob-item" data-pi="${pi}" style="
                padding:0.8rem 1.2rem; border-bottom:1px solid var(--cDeep);
                cursor:pointer; display:flex; align-items:center; gap:0.8rem;
                transition:background 0.2s; font-family:var(--font-mono); font-size:0.95rem;">
                <span style="font-family:var(--font-pixel);font-size:7px;color:${diffCol};
                  min-width:12px;">${p.difficulty}</span>
                <span style="color:var(--ink);">${p.title}</span>
              </div>`;
            }).join('');
            probListEl.querySelectorAll('.prob-item').forEach(el => {
              el.addEventListener('mouseenter', () => el.style.background='rgba(12,42,49,0.8)');
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
  
            // Highlight active in list
            view.querySelectorAll('.prob-item').forEach((el,i) => {
              el.style.background = i===pi ? 'rgba(95,214,230,0.07)' : '';
              el.style.borderLeft = i===pi ? '2px solid var(--c)' : '2px solid transparent';
            });
  
            // Update info panel
            probIdLabel.textContent = `PROBLEM ${prob.id}`;
            probTitle.textContent   = prob.title;
            probDiff.textContent    = prob.difficulty==='E'?'EASY':prob.difficulty==='M'?'MEDIUM':'HARD';
            probDiff.style.color    = prob.difficulty==='E'?'var(--cDim)':prob.difficulty==='M'?'var(--c)':'var(--cBright)';
            probWorld.textContent   = prob.world;
            probHook.textContent    = `"${prob.hook}"`;
  
            // Render visualization
            vizInner.innerHTML = '';
            const scene = VIZ_SCENES[prob.viz] || VIZ_SCENES.default;
            scene.draw(vizInner, prob);
  
            // Update URL without reload
            const hash = `#/a2z-problem?step=${si+1}&prob=${prob.id}`;
            history.replaceState(null, '', hash);
  
            // Scroll active item into view
            const activeItem = view.querySelector(`.prob-item[data-pi="${pi}"]`);
            if (activeItem) activeItem.scrollIntoView({ block:'nearest', behavior:'smooth' });
          }
  
          // Navigation
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
  
          // Initial render
          renderStep(currentStepIdx);
          renderProblem(currentStepIdx, currentProbIdx);
  
          // Mobile: collapse sidebar
          if (window.innerWidth < 768) {
            const layout = view.querySelector('#prob-layout');
            if (layout) layout.style.gridTemplateColumns = '1fr';
            probListEl.style.maxHeight = '200px';
          }
        });
      });
    }
  },

  "#/today": {
    title: "Insights Today",
    html: (params) => `
      <section>
        <span class="eyebrow">DAILY BROADCAST</span>
        <h1>60-Second Insights</h1>
        <div class="grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
          ${DATA.CLIPS.map(clip => `
            <div class="panel panel-glow">
              <span class="eyebrow" style="color: var(--cBright)">${clip.tag} &middot; ${clip.topic}</span>
              <h3>${clip.title}</h3>
              <p style="font-size: 0.9rem; color: var(--cDim)">BLUEPRINT PROTOCOL: ${clip.topic.toUpperCase()}</p>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/practice": {
    title: "AI Bug Finder",
    html: (params) => `
      <section>
        <span class="eyebrow">DEBUGGER v1.0</span>
        <h1>Practice & Debug</h1>
        <div id="practice-grid" class="grid" style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
          <div class="panel panel-glow">
            <span class="eyebrow">🐞 AI BUG FINDER</span>
            <div style="margin: 1.5rem 0; display: flex; gap: 1rem; align-items: center;">
              <span class="eyebrow" style="margin: 0;">LANGUAGE:</span>
              <select id="lang-select" style="background: var(--bg1); border: 1px solid var(--cDim); color: var(--c); font-family: var(--font-pixel); font-size: 10px; padding: 0.4rem;">
                <option>PYTHON</option>
                <option>C++</option>
                <option>JAVA</option>
              </select>
            </div>
            <textarea id="code-area" style="width: 100%; height: 350px; background: #041014; color: var(--c); font-family: var(--font-mono); font-size: 1.2rem; padding: 1.5rem; border: 1px solid var(--cDeep); outline: none;"></textarea>
            <div id="detect-result" class="panel" style="margin-top:1rem;
              border-color:var(--cDim); display:none; font-family:var(--font-mono);
              font-size:0.9rem; color:var(--cDim); padding:0.8rem 1rem;">
            </div>
            <button id="find-bug-btn" class="btn btn-primary" style="margin-top: 1.5rem; width: 100%;">SCAN FOR BUGS</button>
            <div id="bug-result" class="panel" style="margin-top: 2rem; border-color: var(--cBright); display: none; color: var(--cBright); font-family: var(--font-mono);"></div>
          </div>
          <div class="panel">
            <span class="eyebrow">PRO TIPS</span>
            <ul style="color: var(--ink); font-family: var(--font-mono); font-size: 1.2rem; line-height: 2; list-style: none;">
              <li>> TRACE BY HAND FIRST.</li>
              <li>> EDGE CASES ARE LURKING.</li>
              <li>> THINK IN METAPHORS.</li>
              <li>> COMPLEXITY MATTERS.</li>
            </ul>
          </div>
        </div>
      </section>
    `,
    mount: (view) => {
      import('./engine.js').then(m => m.mountBugFinder(view));
    }
  },

  "#/journey": {
    title: "My Journey",
    html: (params) => `
      <section>
        <span class="eyebrow">OPERATOR DASHBOARD</span>
        <h1>Performance Metrics</h1>
        <div class="grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
          ${DATA.STATS.map(stat => `
            <div class="panel panel-glow">
              <span class="eyebrow">${stat.label.toUpperCase()}</span>
              <div style="font-size: 4rem; font-weight: 700; font-family: var(--font-display); margin: 0.5rem 0;">${stat.value}</div>
              <div style="height: 6px; background: var(--cDeep);">
                <div style="${(() => {
                  const raw = stat.value.split('/')[0].split(' ')[0];
                  const num = parseFloat(raw);
                  const pct = isNaN(num) ? 0 : Math.min((num / stat.target) * 100, 100);
                  return `width: ${pct}%`;
                })()}; height: 100%; background: var(--c); box-shadow: 0 0 10px var(--c);"></div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/realworld": {
    title: "Real World Mapping",
    html: (params) => `
      <section>
        <span class="eyebrow">SYSTEM MAPPINGS</span>
        <h1>The Global Blueprint</h1>
        <div class="grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
          ${DATA.REALWORLD.map(item => `
            <div class="panel panel-glow" style="text-align: center;">
              <div style="font-size: 3rem; margin-bottom: 1.5rem;">${item.icon}</div>
              <span class="eyebrow" style="color: var(--cBright)">${item.metaphor.toUpperCase()}</span>
              <h3>${item.title}</h3>
              <p style="font-size: 0.9rem; margin-top: 1rem;">${item.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/404": {
    title: "404 - Lost",
    html: (params) => `
      <section style="text-align: center; height: 60vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <span class="eyebrow" style="color: #ff5f5f">ERROR: 404</span>
        <h1>NODE NOT FOUND</h1>
        <p>You've wandered off the graph into untraced territory.</p>
        <div style="margin-top: 2rem;">
          <a href="#/" class="btn btn-primary">RETURN TO ROOT</a>
        </div>
      </section>
    `
  },

  "#/family": {
    title: "Algorithm Family Tree",
    html: (params) => `
      <section>
        <span class="eyebrow">KNOWLEDGE GRAPH</span>
        <h1>Algorithm Family Tree</h1>
        <p style="margin-bottom:2rem;">
          Algorithms don't exist in isolation. See how each one descends
          from, generalizes, or improves upon another.
        </p>
        <div class="panel" style="padding:0;">
          <div id="family-svg-wrapper" style="overflow:auto;">
            <svg id="family-svg" viewBox="0 0 900 580"
              style="width:100%; min-width:900px; display:block;"></svg>
          </div>
        </div>
        <div id="family-info" class="panel panel-glow"
          style="margin-top:1.5rem; display:none; border-color:var(--c);">
          <h3 id="family-info-title" style="color:var(--cBright); margin-bottom:0.5rem;"></h3>
          <p id="family-info-desc" style="font-size:0.9rem; margin-bottom:1rem;"></p>
          <a id="family-info-link" href="#/" class="btn btn-ghost"
            style="font-size:8px;">VISUALIZE THIS →</a>
        </div>
      </section>
    `,
    mount: (view) => {
      const svg = view.querySelector('#family-svg');
      const infoPanel = view.querySelector('#family-info');
      const infoTitle = view.querySelector('#family-info-title');
      const infoDesc = view.querySelector('#family-info-desc');
      const infoLink = view.querySelector('#family-info-link');

      const NODES = [
        { id: 'search', label: 'Searching',      x: 100, y: 60,  emoji: '🔍', desc: 'The root of all lookup operations.', color: 'var(--cDim)' },
        { id: 'linsearch', label: 'Linear Search', x: 50,  y: 180, emoji: '➡️', desc: 'Check every element. O(n). Brute force.', color: 'var(--cDim)', algo: 'bfs' },
        { id: 'binsearch', label: 'Binary Search', x: 180, y: 180, emoji: '📚', desc: 'Halve the search space. O(log n). Requires sorted input.', color: 'var(--c)', algo: 'binary-search' },
        { id: 'graph', label: 'Graph Traversal', x: 420, y: 60, emoji: '🌐', desc: 'Explore nodes and edges systematically.', color: 'var(--cDim)' },
        { id: 'bfs', label: 'BFS',           x: 310, y: 200, emoji: '👤', desc: 'Level by level. Queue-based. Shortest path in unweighted graphs.', color: 'var(--c)', algo: 'graphs' },
        { id: 'dfs', label: 'DFS',           x: 440, y: 200, emoji: '🗺️', desc: 'Go deep first. Stack-based. Cycle detection, topological sort.', color: 'var(--c)', algo: 'dfs' },
        { id: 'dijkstra', label: "Dijkstra's", x: 310, y: 340, emoji: '📍', desc: 'BFS + edge weights + priority queue. GPS routing.', color: 'var(--cBright)', algo: 'dijkstra' },
        { id: 'astar', label: 'A*',           x: 440, y: 340, emoji: '⭐', desc: "Dijkstra + heuristic. Game AI pathfinding. Faster than Dijkstra.", color: 'var(--cBright)', algo: 'dijkstra' },
        { id: 'sort', label: 'Sorting',       x: 680, y: 60,  emoji: '📊', desc: 'Order elements by comparison or distribution.', color: 'var(--cDim)' },
        { id: 'msort', label: 'Merge Sort',   x: 600, y: 200, emoji: '🏆', desc: 'Divide & conquer. O(n log n). Stable. Linked list friendly.', color: 'var(--c)', algo: 'sorting' },
        { id: 'qsort', label: 'Quick Sort',   x: 740, y: 200, emoji: '⚡', desc: 'Pivot & partition. O(n log n) avg. Cache-friendly in-place.', color: 'var(--c)', algo: 'sorting' },
        { id: 'dp', label: 'Dynamic Programming', x: 140, y: 420, emoji: '💾', desc: 'Optimal substructure + overlapping subproblems = memoization.', color: 'var(--cBright)', algo: 'dp' },
        { id: 'greedy', label: 'Greedy',       x: 300, y: 460, emoji: '🎯', desc: 'Local optimal choice at each step. Sometimes gives global optimum.', color: 'var(--c)', algo: 'greedy' },
        { id: 'backtrack', label: 'Backtracking', x: 500, y: 460, emoji: '🔄', desc: 'DFS + undo. Explores all possibilities. N-Queens, Sudoku.', color: 'var(--c)', algo: 'backtracking' },
        { id: 'twoptr', label: 'Two Pointers', x: 180, y: 320, emoji: '👈👉', desc: 'Binary search pattern. Converging/expanding window. O(n).', color: 'var(--c)', algo: 'binary-search' },
      ];

      const EDGES = [
        { s: 'search', t: 'linsearch', label: 'unsorted' },
        { s: 'search', t: 'binsearch', label: 'sorted' },
        { s: 'binsearch', t: 'twoptr', label: 'pattern' },
        { s: 'graph', t: 'bfs', label: 'queue' },
        { s: 'graph', t: 'dfs', label: 'stack' },
        { s: 'bfs', t: 'dijkstra', label: '+ weights' },
        { s: 'dijkstra', t: 'astar', label: '+ heuristic' },
        { s: 'dfs', t: 'backtrack', label: '+ undo' },
        { s: 'sort', t: 'msort', label: 'divide' },
        { s: 'sort', t: 'qsort', label: 'pivot' },
        { s: 'graph', t: 'dp', label: 'subproblems' },
        { s: 'dp', t: 'greedy', label: 'local optimal' },
      ];

      const ns = Object.fromEntries(NODES.map(n => [n.id, n]));

      // Draw edges first
      EDGES.forEach(e => {
        const a = ns[e.s], b = ns[e.t];
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
        line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
        line.setAttribute("stroke", "var(--cDeep)");
        line.setAttribute("stroke-width", "1.5");
        svg.appendChild(line);
        // Edge label
        const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
        t.setAttribute("x", (a.x + b.x) / 2 + 4);
        t.setAttribute("y", (a.y + b.y) / 2 - 4);
        t.setAttribute("fill", "var(--cDim)");
        t.setAttribute("font-family", "var(--font-mono)");
        t.setAttribute("font-size", "9");
        t.textContent = e.label;
        svg.appendChild(t);
      });

      // Draw nodes
      NODES.forEach(n => {
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.style.cursor = n.algo ? 'pointer' : 'default';

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", n.x); circle.setAttribute("cy", n.y);
        circle.setAttribute("r", n.algo ? "28" : "22");
        circle.setAttribute("fill", "var(--cDeep)");
        circle.setAttribute("stroke", n.color);
        circle.setAttribute("stroke-width", n.algo ? "1.5" : "1");
        g.appendChild(circle);

        const emoji = document.createElementNS("http://www.w3.org/2000/svg", "text");
        emoji.setAttribute("x", n.x); emoji.setAttribute("y", n.y + 5);
        emoji.setAttribute("text-anchor", "middle");
        emoji.setAttribute("font-size", "14");
        emoji.textContent = n.emoji;
        g.appendChild(emoji);

        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", n.x); label.setAttribute("y", n.y + (n.algo ? 46 : 38));
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("fill", n.color);
        label.setAttribute("font-family", "var(--font-pixel)");
        label.setAttribute("font-size", "8");
        label.textContent = n.label;
        g.appendChild(label);

        if (n.algo) {
          g.addEventListener('click', () => {
            infoPanel.style.display = 'block';
            infoTitle.textContent = `${n.emoji} ${n.label}`;
            infoDesc.textContent = n.desc;
            infoLink.href = `#/experience?algo=${n.algo}`;
            // Highlight
            svg.querySelectorAll('circle').forEach(c => c.setAttribute('filter', ''));
            circle.setAttribute('filter', 'drop-shadow(0 0 8px var(--c))');
            circle.setAttribute('stroke', 'var(--cBright)');
          });
          g.addEventListener('mouseenter', () => {
            circle.setAttribute('stroke', 'var(--cBright)');
          });
          g.addEventListener('mouseleave', () => {
            circle.setAttribute('stroke', n.color);
          });
        }

        svg.appendChild(g);
      });

      // Animate all SVG groups in with a stagger
      const allGroups = svg.querySelectorAll('g');
      allGroups.forEach((g, i) => {
        g.style.opacity = '0';
        g.style.transform = 'scale(0.7)';
        g.style.transformOrigin = `${g.querySelector('circle')?.getAttribute('cx') || 50}px ${g.querySelector('circle')?.getAttribute('cy') || 50}px`;
        g.style.transition = `opacity 0.4s ease ${i * 0.05}s, transform 0.4s ease ${i * 0.05}s`;
        setTimeout(() => {
          g.style.opacity = '1';
          g.style.transform = 'scale(1)';
        }, 50);
      });
    }
  }
};

function renderWorldCard(world) {
  const SCENE_LABELS = {
    'Sorting': { scene: '🏆 LEADERBOARD SORT', algo: 'sorting' },
    'Binary Search': { scene: '📚 LIBRARY CATALOG', algo: 'binary-search' },
    'Graphs': { scene: '👤 SOCIAL NETWORK', algo: 'graphs' },
    'DP': { scene: '💾 DECISION VAULT', algo: 'dp' },
    'Heaps': { scene: '👑 PRIORITY QUEUE', algo: 'heaps' },
    'Recursion': { scene: '🪞 FRACTAL MIRROR', algo: 'recursion' },
    'Backtracking': { scene: '🗺️ MAZE EXPLORER', algo: 'backtracking' },
    'Hashing': { scene: '🔑 HASH VAULT', algo: 'hashing' },
    'Linked Lists': { scene: '🔗 CHAIN SYSTEM', algo: 'linkedlists' },
  };
  const meta = SCENE_LABELS[world.metaphor] || { scene: world.name, algo: world.metaphor.toLowerCase() };

  return `
    <a href="#/experience?algo=${meta.algo}"
      style="text-decoration:none; color:inherit; display:block;">
      <div class="panel panel-glow" data-cat="${world.category}"
        style="height:100%; transition:all 0.3s; position:relative; overflow:hidden;">
        <div style="position:absolute; top:0; right:0; padding:0.5rem 0.8rem;
          font-family:var(--font-pixel); font-size:7px; color:var(--cDeep);
          background:var(--c); letter-spacing:0.1em;">
          ${world.complexity}
        </div>
        <div style="font-size:2.5rem; margin-bottom:1rem;">${world.emoji}</div>
        <span class="eyebrow" style="color:var(--c); margin-bottom:0.3rem;">
          ${meta.scene}
        </span>
        <h3 style="margin-bottom:0.5rem;">${world.name}</h3>
        <p style="font-size:0.85rem; color:var(--cDim); margin-bottom:1.5rem;">
          ${world.hook}
        </p>
        <span class="btn btn-ghost"
          style="padding:0.2rem 0.5rem; font-size:7px; pointer-events:none;">
          ${world.category.toUpperCase()} ›
        </span>
      </div>
    </a>
  `;
}
