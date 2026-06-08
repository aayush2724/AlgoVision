import * as DATA from './data.js';

export const ROUTE_THEME = {
  "/": "default",
  "/explore": "purple",
  "/experience": "cyan",
  "/a2z": "deep",
  "/today": "purple",
  "/practice": "default",
  "/journey": "cyan",
  "/realworld": "deep"
};

export const PAGES = {
  "/": {
    title: "AlgoVision &middot; Home",
    html: () => `
      <section class="hero">
        <h1 data-reveal>${DATA.HERO.title}</h1>
        <p data-reveal>${DATA.HERO.lead}</p>
        <div class="hero-cta" data-reveal>
          <a href="#/explore" class="btn btn-primary" data-magnet>${DATA.HERO.primaryCTA}</a>
          <a href="#/a2z" class="btn btn-ghost" data-magnet>${DATA.HERO.ghostCTA}</a>
        </div>
      </section>
      
      <section>
        <h2 data-scroll>The 3-Act Method</h2>
        <div class="grid">
          ${DATA.ACTS.map(act => `
            <div class="card tilt" data-scroll>
              <div style="font-size: 3rem; margin-bottom: 1rem;">${act.icon}</div>
              <h3>${act.title}</h3>
              <p>${act.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <section style="overflow: hidden; padding: 2rem 0;">
        <div class="marquee" style="display: flex; gap: 4rem; white-space: nowrap;">
          ${[...DATA.MARQUEE, ...DATA.MARQUEE].map(m => `<span style="font-family: var(--font-heading); font-size: 2rem; font-weight: 700; opacity: 0.2;">${m}</span>`).join('')}
        </div>
      </section>
    `,
    mount: (view) => {
      const marquee = view.querySelector('.marquee');
      gsap.to(marquee, { xPercent: -50, duration: 20, ease: "none", repeat: -1 });
    }
  },

  "/explore": {
    title: "Explore Worlds",
    html: () => `
      <section>
        <h1 data-reveal>Algorithm Worlds</h1>
        <div class="filters" style="display: flex; gap: 1rem; margin-bottom: 3rem;" data-reveal>
          ${DATA.CATEGORIES.map(cat => `<button class="btn btn-ghost filter-btn" data-cat="${cat}">${cat}</button>`).join('')}
        </div>
        <div class="grid" id="worlds-grid">
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
          import('./animations.js').then(m => m.tiltCards());
        });
      });
    }
  },

  "/experience": {
    title: "The Live Engine",
    html: () => `
      <section>
        <h1 data-reveal>Experience Dijkstra</h1>
        <div class="engine-header" style="display: flex; justify-content: space-between; align-items: center;" data-reveal>
          <div id="engine-status"></div>
          <div class="engine-controls" style="display: flex; gap: 1rem;">
            <button id="run-btn" class="btn btn-primary btn-sm">Run Dijkstra</button>
            <button id="step-btn" class="btn btn-ghost btn-sm" disabled>Step</button>
            <button id="reset-btn" class="btn btn-ghost btn-sm">Reset</button>
          </div>
        </div>
        
        <div id="engine-view" data-scroll>
          <svg id="engine-svg" viewBox="0 0 800 300"></svg>
          <div id="engine-note" style="position: absolute; bottom: 2rem; left: 2rem; right: 2rem; background: var(--panel); border: 1px solid var(--border); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px); pointer-events: none; opacity: 0; transition: 0.3s;"></div>
        </div>

        <div style="margin-top: 2rem; display: flex; gap: 1rem;" data-scroll>
          <button id="explain-btn" class="btn btn-ghost">✦ Explain this step</button>
          <div id="explanation-box" style="flex: 1; padding: 1.5rem; background: var(--bg-soft); border: 1px solid var(--border); border-radius: 8px; display: none;"></div>
        </div>
      </section>
    `,
    mount: (view) => {
      import('./engine.js').then(m => m.mountEngine(view));
    }
  },

  "/a2z": {
    title: "A2Z Journey",
    html: () => `
      <section>
        <h1 data-reveal>The Roadmap</h1>
        <p data-reveal>Our comprehensive path through 455+ problems, inspired by the takeuforward A2Z sheet.</p>
        
        <div class="timeline" style="margin-top: 5rem;">
          ${DATA.A2Z_STEPS.map(step => `
            <div class="timeline-step" data-scroll>
              <div class="step-marker"></div>
              <div class="card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                  <span style="color: var(--blue-bright); font-weight: 700; font-family: var(--font-heading);">${step.step}</span>
                  <span style="color: var(--muted);">${step.problems} problems</span>
                </div>
                <h3>${step.title}</h3>
                <div style="height: 4px; background: var(--border); border-radius: 2px; overflow: hidden;">
                  <div style="width: ${step.progress}%; height: 100%; background: var(--blue);"></div>
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "/today": {
    title: "Insights Today",
    html: () => `
      <section>
        <h1 data-reveal>60-Second Insights</h1>
        <div class="grid">
          ${DATA.CLIPS.map(clip => `
            <div class="card tilt" data-scroll style="border-left: 4px solid ${clip.accent};">
              <span class="badge" style="background: ${clip.accent}33; color: ${clip.accent}; margin-bottom: 1rem; display: inline-block;">${clip.tag}</span>
              <h3>${clip.title}</h3>
              <p style="font-size: 0.8rem;">Topic: ${clip.topic}</p>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "/practice": {
    title: "AI Bug Finder",
    html: () => `
      <section>
        <h1 data-reveal>Practice & Debug</h1>
        <div class="grid" style="grid-template-columns: 2fr 1fr;">
          <div class="card" data-reveal>
            <h3>🐞 AI Bug Finder</h3>
            <div style="margin: 1.5rem 0;">
              <label style="display: block; margin-bottom: 0.5rem; color: var(--muted);">Language</label>
              <select id="lang-select" style="width: 100%; padding: 0.8rem; background: var(--bg); border: 1px solid var(--border); color: white; border-radius: 4px;">
                <option>Python</option>
                <option>C++</option>
                <option>Java</option>
              </select>
            </div>
            <textarea id="code-area" style="width: 100%; height: 300px; background: #000; color: #0f0; font-family: monospace; padding: 1rem; border: 1px solid var(--border); border-radius: 4px; resize: none;"></textarea>
            <button id="find-bug-btn" class="btn btn-primary" style="margin-top: 1rem; width: 100%;">Find the bug</button>
            <div id="bug-result" style="margin-top: 1.5rem; padding: 1rem; background: rgba(255, 210, 74, 0.1); border: 1px solid var(--gold); border-radius: 4px; display: none;"></div>
          </div>
          <div class="card" data-scroll>
            <h3>Pro Tips</h3>
            <ul style="color: var(--muted); padding-left: 1.5rem; line-height: 2;">
              <li>Trace your code by hand first.</li>
              <li>Edge cases are your enemies.</li>
              <li>Think in metaphors.</li>
              <li>Complexity matters.</li>
            </ul>
          </div>
        </div>
      </section>
    `,
    mount: (view) => {
      import('./engine.js').then(m => m.mountBugFinder(view));
    }
  },

  "/journey": {
    title: "My Journey",
    html: () => `
      <section>
        <h1 data-reveal>Dashboard</h1>
        <div class="grid">
          ${DATA.STATS.map(stat => `
            <div class="card" data-scroll>
              <h4 style="color: var(--muted);">${stat.label}</h4>
              <div style="font-size: 3rem; font-weight: 700; font-family: var(--font-heading); margin: 0.5rem 0;">${stat.value}</div>
              <div style="height: 4px; background: var(--border); border-radius: 2px;">
                <div style="width: ${(stat.value.split(' ')[0] / stat.target) * 100}%; height: 100%; background: var(--cyan);"></div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "/realworld": {
    title: "Real World Mapping",
    html: () => `
      <section>
        <h1 data-reveal>Real-World Mapping</h1>
        <div class="grid">
          ${DATA.REALWORLD.map(item => `
            <div class="card tilt" data-scroll style="min-height: 250px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
              <div style="font-size: 3rem; margin-bottom: 1rem;">${item.icon}</div>
              <h3>${item.title}</h3>
              <p style="color: var(--blue-bright); font-weight: 700;">Uses: ${item.metaphor}</p>
              <p style="font-size: 0.8rem; margin-top: 0.5rem;">${item.desc}</p>
            </div>
          `).join('')}
        </div>
      </section>
    `
  },

  "/404": {
    title: "404 - Lost",
    html: () => `
      <section style="text-align: center; height: 60vh; display: flex; flex-direction: column; justify-content: center;">
        <h1 data-reveal>404</h1>
        <p data-reveal>You've wandered off the graph.</p>
        <div data-reveal style="margin-top: 2rem;">
          <a href="#/" class="btn btn-primary">Back to Root</a>
        </div>
      </section>
    `
  }
};

function renderWorldCard(world) {
  return `
    <div class="card tilt" data-scroll data-cat="${world.category}">
      <div style="font-size: 2rem; margin-bottom: 1rem;">${world.emoji}</div>
      <div style="color: var(--blue-bright); font-weight: 700; font-size: 0.8rem;">${world.metaphor}</div>
      <h3>${world.name}</h3>
      <p style="font-size: 0.9rem; margin-bottom: 1rem;">${world.hook}</p>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="badge badge-live" style="font-size: 0.6rem;">${world.category}</span>
        <span style="font-family: monospace; font-size: 0.7rem; color: var(--muted);">${world.complexity}</span>
      </div>
    </div>
  `;
}
