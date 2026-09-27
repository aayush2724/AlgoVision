// ── Capture the request every algorithm sends for its DEFAULT input ────────
//
// Offline mode replays a pre-computed trace of each algorithm's sample input
// (frontend/offline/<id>.json). To compute those traces we need the exact
// request the engine builds for the default input — the input parsers are
// bespoke per algorithm, so instead of re-implementing them we let the real
// engine build each request and record it.
//
// How to run (only needed when an algorithm is added or a default changes):
//   1. Start the app locally:  cd backend && python -m uvicorn app.main:app --port 8123
//   2. Open http://localhost:8123/ and paste this file into the devtools console.
//   3. Run:  await captureOfflinePayloads()          (a few minutes)
//      Then: copy(JSON.stringify(window.__offlinePayloads, null, 1))
//      and paste it into tools/offline_payloads.json.
//   4. python tools/build_offline_traces.py
//
// Each algorithm opens in a hidden same-origin iframe; its window.fetch is
// wrapped to record the POST /api/trace body, then Run is clicked.

async function captureOfflinePayloads({ ids = null, postTo = null } = {}) {
  const { ALGORITHMS } = await import('/js/data.js');
  const todo = ids || ALGORITHMS.map(a => a.id);
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = window.__offlinePayloads = window.__offlinePayloads || {};
  window.__offlineProgress = { done: 0, total: todo.length, failed: [] };

  for (const id of todo) {
    const frame = document.createElement('iframe');
    frame.style.cssText = 'position:fixed;left:-3000px;top:0;width:1280px;height:900px';
    frame.src = `/?capture=${encodeURIComponent(id)}#/experience?algo=${encodeURIComponent(id)}`;
    document.body.appendChild(frame);
    await new Promise(r => { frame.onload = r; });
    const w = frame.contentWindow;
    let body = null;
    const realFetch = w.fetch.bind(w);
    w.fetch = (url, opts) => {
      if (String(url).includes('/api/trace') && opts && opts.body) body = opts.body;
      return realFetch(url, opts);
    };
    let run = null;
    for (let i = 0; i < 50 && !run; i++) {
      run = [...w.document.querySelectorAll('button')]
        .find(b => /^\s*(▶\s*)?run/i.test(b.textContent));
      if (!run) await sleep(100);
    }
    await sleep(300);                      // let the engine finish its backend check
    if (run) run.click();
    for (let i = 0; i < 50 && !body; i++) await sleep(100);
    if (body) out[id] = JSON.parse(body);
    else window.__offlineProgress.failed.push(id);
    window.__offlineProgress.done++;
    frame.remove();
  }
  if (postTo) {
    await fetch(postTo, { method: 'POST', body: JSON.stringify(out) });
  }
  return window.__offlineProgress;
}
