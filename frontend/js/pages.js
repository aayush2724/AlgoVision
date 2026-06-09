import * as DATA from './data.js';

export const ROUTE_THEME = {
  "#/": "default",
  "#/explore": "default",
  "#/experience": "default",
  "#/a2z": "default",
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
    html: () => `
      <section class="hero" style="text-align: center; padding-top: 10vh;">
        <span class="eyebrow">BLUEPRINT v2.0.6</span>
        <h1>See the Algorithm.<br/>Master the Story.</h1>
        <p style="margin: 0 auto 2rem;">We turn complex data structures into cinematic visual journeys. No more dry slides — just pure intuition.</p>
        <div class="hero-cta">
          <a href="#/explore" class="btn btn-primary">Start Exploring</a>
          <a href="#/a2z" class="btn btn-ghost" style="margin-left: 1rem;">View Roadmap</a>
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
      const marquee = view.querySelector('.marquee');
      gsap.to(marquee, { xPercent: -50, duration: 30, ease: "none", repeat: -1 });
    }
  },

  "#/explore": {
    title: "Explore Worlds",
    html: () => `
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
          const cat = btn.dataset.cat;
          const filtered = cat === "All" ? DATA.WORLDS : DATA.WORLDS.filter(w => w.category === cat);
          grid.innerHTML = filtered.map(world => renderWorldCard(world)).join('');
          import('./animations.js').then(m => m.revealView(grid));
        });
      });
    }
  },

  "#/experience": {
    title: "The Live Engine",
    html: () => `
      <section>
        <span class="eyebrow">LIVE EXECUTION</span>
        <h1>Six Degrees (Dijkstra)</h1>
        <div class="panel panel-glow" style="margin-bottom: 2rem;">
          <div class="engine-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div id="engine-status" class="eyebrow" style="margin: 0;">STATUS: IDLE</div>
            <div class="engine-controls" style="display: flex; gap: 1rem;">
              <button id="run-btn" class="btn btn-primary">RUN DIJKSTRA</button>
              <button id="step-btn" class="btn btn-ghost" disabled>STEP</button>
              <button id="reset-btn" class="btn btn-ghost">RESET</button>
            </div>
          </div>
          
          <div id="engine-view" style="background: var(--bg1); border: 1px solid var(--cDeep); min-height: 400px; position: relative;">
            <svg id="engine-svg" viewBox="0 0 800 300" style="width: 100%; height: 100%;"></svg>
            <div id="engine-note" class="panel" style="position: absolute; bottom: 1rem; left: 1rem; right: 1rem; padding: 1rem; pointer-events: none; opacity: 0; transition: 0.3s; font-family: var(--font-mono); font-size: 1.1rem;"></div>
          </div>
        </div>

        <div style="display: flex; gap: 2rem;">
          <button id="explain-btn" class="btn btn-ghost" style="flex-shrink: 0; height: fit-content;">✦ EXPLAIN STEP</button>
          <div id="explanation-box" class="panel" style="flex: 1; display: none; font-family: var(--font-mono); font-size: 1.1rem; color: var(--c);"></div>
        </div>
      </section>
    `,
    mount: (view) => {
      import('./engine.js').then(m => m.mountEngine(view));
    }
  },

  "#/a2z": {
    title: "A2Z Journey",
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
              const diffColor = diff === 'E' ? 'var(--cDim)' : (diff === 'M' ? 'var(--c)' : 'var(--cBright)');
              return `
              <div class="station" data-index="${idx + 1}">
                <div class="station-dot"></div>
                <div class="station-card">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span class="eyebrow" style="margin: 0;">${step.step}</span>
                    <span style="font-family: var(--font-pixel); font-size: 8px; color: ${diffColor}; border: 1px solid ${diffColor}; padding: 2px 4px;">${diff}</span>
                  </div>
                  <h3 style="margin-bottom: 1rem;">${step.title}</h3>
                  <span class="eyebrow" style="font-size: 8px; color: var(--cDim);">${step.problems} PROBLEMS</span>
                  <div style="height: 6px; background: var(--cDeep); overflow: hidden; margin-top: 0.5rem;">
                    <div style="width: ${step.progress}%; height: 100%; background: var(--c); box-shadow: 0 0 10px var(--c);"></div>
                  </div>
                </div>
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

  "#/today": {
    title: "Insights Today",
    html: () => `
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
    html: () => `
      <section>
        <span class="eyebrow">DEBUGGER v1.0</span>
        <h1>Practice & Debug</h1>
        <div class="grid" style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
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
    html: () => `
      <section>
        <span class="eyebrow">OPERATOR DASHBOARD</span>
        <h1>Performance Metrics</h1>
        <div class="grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;">
          ${DATA.STATS.map(stat => `
            <div class="panel panel-glow">
              <span class="eyebrow">${stat.label.toUpperCase()}</span>
              <div style="font-size: 4rem; font-weight: 700; font-family: var(--font-display); margin: 0.5rem 0;">${stat.value}</div>
              <div style="height: 6px; background: var(--cDeep);">
                <div style="width: ${(stat.value.split(' ')[0] / stat.target) * 100}%; height: 100%; background: var(--c); box-shadow: 0 0 10px var(--c);"></div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "#/realworld": {
    title: "Real World Mapping",
    html: () => `
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
    html: () => `
      <section style="text-align: center; height: 60vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <span class="eyebrow" style="color: #ff5f5f">ERROR: 404</span>
        <h1>NODE NOT FOUND</h1>
        <p>You've wandered off the graph into untraced territory.</p>
        <div style="margin-top: 2rem;">
          <a href="#/" class="btn btn-primary">RETURN TO ROOT</a>
        </div>
      </section>
    `
  }
};

function renderWorldCard(world) {
  const blueprintName = TOPIC_NAMES[world.metaphor] || world.name;
  return `
    <div class="panel panel-glow" data-cat="${world.category}">
      <div style="font-size: 2.5rem; margin-bottom: 1.5rem;">${world.emoji}</div>
      <span class="eyebrow" style="color: var(--cBright)">${world.metaphor.toUpperCase()}</span>
      <h3 style="margin-bottom: 0.5rem;">${blueprintName}</h3>
      <p style="font-size: 0.9rem; margin-bottom: 1.5rem; color: var(--cDim)">${world.hook}</p>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="btn btn-ghost" style="padding: 0.2rem 0.5rem; font-size: 8px;">${world.category.toUpperCase()}</span>
        <span style="font-family: var(--font-mono); font-size: 14px; color: var(--cBright);">${world.complexity}</span>
      </div>
    </div>
  `;
}
