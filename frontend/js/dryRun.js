// ── DRY RUN ────────────────────────────────────────────────────────────────
//
// "Your code, line by line": the Practice page runs the student's own Python
// in their browser (see dryrun.worker.js) and replays the recording the way a
// dry run on paper goes — the line about to run, every variable, the call
// stack, what has been printed so far. Lists are drawn as cells, with index
// variables (i, j, low, mid, …) pointing at the cell they name.
//
// Only Python: it is the one language a browser can run safely without a
// compile server. Other languages still get detection and the bug scan.

const MAX_STEPS = 1500;          // a dry run longer than this is no longer readable
const RUN_TIMEOUT_MS = 8000;     // after Python has loaded; covers loops in C code
const INDEX_NAMES = new Set(['i', 'j', 'k', 'l', 'r', 'm', 'lo', 'hi', 'low', 'high', 'mid',
  'left', 'right', 'start', 'end', 'p', 'q', 'idx', 'pos', 'slow', 'fast']);

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// One worker for the whole session: Pyodide takes seconds to start, so a
// second dry run (or a revisit of the page) reuses the warm interpreter.
let worker = null;
let runSeq = 0;

function getWorker() {
  if (!worker) worker = new Worker('/js/dryrun.worker.js');
  return worker;
}

function runInWorker(code, call, onStatus) {
  const id = ++runSeq;
  const w = getWorker();
  return new Promise((resolve, reject) => {
    let timer = null;
    const done = (fn, v) => { clearTimeout(timer); w.onmessage = null; w.onerror = null; fn(v); };
    w.onmessage = (e) => {
      const m = e.data || {};
      if (m.type === 'status') {
        onStatus?.(m.text);
        // The clock starts once Python is up — loading time is not the
        // student's program's fault.
        if (m.text.startsWith('Running')) {
          timer = setTimeout(() => {
            worker?.terminate();
            worker = null;
            done(reject, new Error('Your code ran for more than 8 seconds, so it was stopped. '
              + 'Look for a loop whose condition never becomes false.'));
          }, RUN_TIMEOUT_MS);
        }
        return;
      }
      if (m.id !== id) return;
      if (m.type === 'result') done(resolve, m);
      else done(reject, new Error(m.message || 'Python could not start.'));
    };
    w.onerror = (e) => {
      worker?.terminate();
      worker = null;
      done(reject, new Error(e.message || 'Python could not start in this browser.'));
    };
    w.postMessage({ type: 'run', id, code, call, maxSteps: MAX_STEPS });
  });
}

// Names of functions the code defines, in order.
function definedFunctions(code) {
  return [...code.matchAll(/^\s*def\s+([A-Za-z_]\w*)\s*\(/gm)].map(m => m[1]);
}

// Does the code already do something at the top level (not just define)?
function hasTopLevelCode(code) {
  return code.split('\n').some(line =>
    /^\S/.test(line) && !/^(def|class|import|from|#|@)/.test(line) && line.trim());
}

const looksLikeOtherLanguage = (code) =>
  /[;{}]\s*$/m.test(code) || /\b(public|static|void|int|const|let|function|#include)\b/.test(code);

export function mountDryRun(view, params) {
  const codeArea = view.querySelector('#code-area');
  const langSelect = view.querySelector('#lang-select');
  const callInput = view.querySelector('#dry-call');
  const runBtn = view.querySelector('#dry-run-btn');
  const panel = view.querySelector('#dry-panel');
  const status = view.querySelector('#dry-status');
  const codeList = view.querySelector('#dry-code');
  const framesEl = view.querySelector('#dry-frames');
  const outputEl = view.querySelector('#dry-output');
  const noteEl = view.querySelector('#dry-note');
  const prevBtn = view.querySelector('#dry-prev');
  const playBtn = view.querySelector('#dry-play');
  const nextBtn = view.querySelector('#dry-next');
  const slider = view.querySelector('#dry-slider');
  const counter = view.querySelector('#dry-count');
  const speedSel = view.querySelector('#dry-speed');
  if (!codeArea || !runBtn || !panel) return;

  let trace = null;
  let idx = 0;
  let playTimer = null;

  const setStatus = (text, cls = '') => {
    status.textContent = text;
    status.className = `engine-status-pill ${cls}`.trim();
  };

  // Keep "Then run" pointing at a function that exists in the code.
  const syncCall = () => {
    const defs = definedFunctions(codeArea.value);
    const callee = (callInput.value.match(/^\s*(?:print\s*\(\s*)?([A-Za-z_]\w*)\s*\(/) || [])[1];
    if (callee && !defs.includes(callee)) callInput.value = '';
    callInput.placeholder = defs.length ? `e.g. ${defs[0]}(...) with your own values` : 'optional';
  };
  codeArea.addEventListener('input', syncCall);

  // ── replay ──
  function stopPlay() {
    clearInterval(playTimer);
    playTimer = null;
    playBtn.classList.remove('is-playing');
    playBtn.setAttribute('aria-label', 'Play');
  }

  function startPlay() {
    if (!trace?.steps.length) return;
    if (idx >= trace.steps.length - 1) show(0);
    stopPlay();
    playTimer = setInterval(() => {
      if (idx >= trace.steps.length - 1) { stopPlay(); return; }
      show(idx + 1);
    }, 750 / Number(speedSel.value || 1));
    playBtn.classList.add('is-playing');
    playBtn.setAttribute('aria-label', 'Pause');
  }

  // Variables in the current frame that differ from the step before, when
  // that step was in the same frame. Entering a function marks nothing.
  function changedVars(step, prev) {
    const cur = step.frames[step.frames.length - 1];
    const before = prev?.frames[prev.frames.length - 1];
    const changed = new Set();
    if (!cur || !before || before.name !== cur.name || prev.frames.length !== step.frames.length) {
      return changed;
    }
    for (const [k, v] of Object.entries(cur.vars)) {
      if (!before.vars[k] || before.vars[k].r !== v.r) changed.add(k);
    }
    return changed;
  }

  function narrate(step, prev, changed) {
    const fn = step.frames[step.frames.length - 1]?.name || 'main program';
    if (step.event === 'exception') {
      return `<span class="dry-bad">Line ${step.line} raised ${esc(step.exc)}</span>`;
    }
    if (step.event === 'return' && step.fn === '<module>') return 'The program finished.';
    if (step.event === 'return') {
      return `<b>${esc(step.fn)}()</b> returns <code>${esc(step.ret?.r)}</code> to its caller.`;
    }
    const enteredNew = !prev || prev.frames.length < step.frames.length;
    if (enteredNew && step.frames.length > 1) {
      const args = Object.entries(step.frames[step.frames.length - 1].vars)
        .map(([k, v]) => `${esc(k)} = ${esc(v.r)}`).join(', ');
      return `Called <b>${esc(fn)}</b>${args ? ` with ${args}` : ''}. Next: line ${step.line}.`;
    }
    const cur = step.frames[step.frames.length - 1]?.vars || {};
    const bits = [...changed].map(k => `<b>${esc(k)}</b> = <code>${esc(cur[k].r)}</code>`);
    const ran = prev && prev.event === 'line' ? `Line ${prev.line} ran` : 'Starting';
    return `${ran}${bits.length ? ': ' + bits.join(', ') : ''}. Next: line ${step.line}.`;
  }

  function renderValue(name, v, frameVars, isChanged) {
    let cells = '';
    if (v.items) {
      const pointers = {};
      for (const [k, iv] of Object.entries(frameVars)) {
        const n = Number(iv.r);
        if (INDEX_NAMES.has(k) && iv.t === 'int' && n >= 0 && n < v.items.length) {
          (pointers[n] ||= []).push(k);
        }
      }
      cells = `<div class="dry-cells" aria-hidden="true">${v.items.map((it, i) => `
        <span class="dry-cell${pointers[i] ? ' is-pointed' : ''}">
          <span class="dry-cell-v">${esc(it)}</span>
          <span class="dry-cell-i">${i}</span>
          ${pointers[i] ? `<span class="dry-cell-p">${esc(pointers[i].join(' '))}</span>` : ''}
        </span>`).join('')}</div>`;
    }
    return `<div class="dry-var${isChanged ? ' is-changed' : ''}">
      <span class="dry-var-name">${esc(name)}</span>
      <span class="dry-var-val"><code>${esc(v.r)}</code>${cells}</span>
    </div>`;
  }

  function show(i) {
    if (!trace?.steps.length) return;
    idx = Math.max(0, Math.min(i, trace.steps.length - 1));
    const step = trace.steps[idx];
    const prev = idx > 0 ? trace.steps[idx - 1] : null;
    const changed = changedVars(step, prev);

    // Code: the line about to run is marked; the one that just ran is ghosted.
    codeList.querySelectorAll('li').forEach((li, n) => {
      li.classList.toggle('is-current', n + 1 === step.line);
      li.classList.toggle('is-prev', !!prev && prev.event === 'line' && n + 1 === prev.line
        && prev.line !== step.line);
      li.classList.toggle('is-error', step.event === 'exception' && n + 1 === step.line);
    });
    const cur = codeList.querySelector('li.is-current');
    if (cur) codeList.scrollTop = Math.max(0, cur.offsetTop - codeList.clientHeight / 2);

    // Frames: current function on top, its callers below.
    const frames = [...step.frames].reverse();
    framesEl.innerHTML = frames.map((f, n) => {
      const vars = Object.entries(f.vars);
      return `<div class="dry-frame${n === 0 ? ' is-top' : ''}">
        <div class="dry-frame-name">${n === 0 ? 'now in ' : 'called from '}<b>${esc(f.name)}</b>
          <span>line ${f.line}</span></div>
        ${vars.length ? vars.map(([k, v]) => renderValue(k, v, f.vars, n === 0 && changed.has(k))).join('')
          : '<div class="dry-empty">no variables yet</div>'}
      </div>`;
    }).join('') || '<div class="dry-empty">no variables yet</div>';

    outputEl.textContent = (trace.output || '').slice(0, step.out);

    noteEl.innerHTML = narrate(step, prev, changed);
    slider.value = String(idx);
    counter.textContent = `STEP ${idx + 1} / ${trace.steps.length}`;
    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx >= trace.steps.length - 1;

    if (idx === trace.steps.length - 1) finish();
    else setStatus('Stepping', 'running');
  }

  // What the end of the recording means.
  function finish() {
    if (trace.error) {
      setStatus(trace.error.type, 'is-bad');
      noteEl.innerHTML = `<span class="dry-bad">${esc(trace.error.type)}: ${esc(trace.error.message)}</span>`
        + (trace.error.line ? ` — on line ${trace.error.line}.` : '');
      codeList.querySelectorAll('li')[trace.error.line - 1]?.classList.add('is-error');
      outputEl.textContent = trace.output || '';
    } else if (trace.truncated) {
      setStatus('Stopped early', 'is-warn');
      noteEl.innerHTML = `Stopped after ${MAX_STEPS} steps — that is past what a dry run can show.`
        + ' Try a smaller input, or check for a loop that never ends.';
    } else {
      setStatus('Finished', 'done');
      outputEl.textContent = trace.output || '';
    }
  }

  function loadTrace(t) {
    trace = t;
    codeList.innerHTML = t.lines.map((line, n) =>
      `<li class="${n + 1 === t.callLine ? 'is-call' : ''}">${esc(line) || ' '}</li>`).join('');
    slider.max = String(Math.max(0, t.steps.length - 1));
    [prevBtn, playBtn, nextBtn, slider].forEach(el => { el.disabled = !t.steps.length; });
    if (!t.steps.length) {
      // Compile errors, or code that ran no line of its own.
      framesEl.innerHTML = '<div class="dry-empty">nothing ran</div>';
      outputEl.textContent = t.output || '';
      counter.textContent = '';
      if (t.error) {
        setStatus(t.error.type, 'is-bad');
        const other = t.error.type === 'SyntaxError' && looksLikeOtherLanguage(codeArea.value);
        noteEl.innerHTML = `<span class="dry-bad">${esc(t.error.type)}: ${esc(t.error.message)}</span>`
          + (t.error.line ? ` — on line ${t.error.line}.` : '')
          + (other ? ' This looks like C++, Java or JavaScript — the dry run understands Python only.' : '');
        codeList.querySelectorAll('li')[t.error.line - 1]?.classList.add('is-error');
      } else {
        setStatus('Nothing ran', 'is-warn');
        noteEl.textContent = 'Nothing in your code ran. Put a call in “Then run” to watch a function work.';
      }
      return;
    }
    show(0);
  }

  async function run() {
    stopPlay();
    panel.classList.remove('is-hidden');
    if (langSelect && langSelect.value !== 'python') {
      setStatus('Python only', 'is-warn');
      noteEl.textContent = 'The dry run runs Python in your browser. For C++, Java or JavaScript, '
        + 'use “Scan for bugs” — or switch the language to Python and paste a Python version.';
      return;
    }
    const code = codeArea.value;
    if (!code.trim()) {
      setStatus('No code', 'is-warn');
      noteEl.textContent = 'Paste some Python first.';
      return;
    }
    let call = callInput.value.trim();
    // A bare call → print its answer, so it shows up under Output.
    if (call && !/^print\s*\(/.test(call) && /^[A-Za-z_][\w.]*\s*\(.*\)$/.test(call)) {
      call = `print(${call})`;
    }
    if (!call && !hasTopLevelCode(code)) {
      const defs = definedFunctions(code);
      setStatus('Nothing to run', 'is-warn');
      noteEl.textContent = defs.length
        ? `Your code defines ${defs.map(d => d + '()').join(', ')} but never calls it. `
          + `Type a call in “Then run”, e.g. ${defs[0]}(...) with your own values.`
        : 'There is nothing to run yet.';
      callInput.focus();
      return;
    }
    runBtn.disabled = true;
    runBtn.setAttribute('aria-busy', 'true');
    setStatus('Starting Python…', 'running');
    noteEl.textContent = 'Your code runs inside this browser — nothing is sent anywhere.';
    try {
      const t = await runInWorker(code, call, (text) => setStatus(text, 'running'));
      loadTrace(t);
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {
      trace = null;
      setStatus('Could not run', 'is-bad');
      noteEl.innerHTML = `<span class="dry-bad">${esc(e.message)}</span>`
        + (/start|load|fetch|network|import/i.test(e.message)
          ? ' Python is downloaded the first time you dry run — check your connection and try again.'
          : '');
    } finally {
      runBtn.disabled = false;
      runBtn.removeAttribute('aria-busy');
    }
  }

  runBtn.addEventListener('click', run);
  runBtn.disabled = false;     // rendered disabled so an early click isn't lost
  callInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); run(); } });
  prevBtn.addEventListener('click', () => { stopPlay(); show(idx - 1); });
  nextBtn.addEventListener('click', () => { stopPlay(); show(idx + 1); });
  playBtn.addEventListener('click', () => (playTimer ? stopPlay() : startPlay()));
  slider.addEventListener('input', () => { stopPlay(); show(Number(slider.value)); });
  speedSel.addEventListener('change', () => { if (playTimer) startPlay(); });
  panel.addEventListener('keydown', (e) => {
    if (e.target.closest('input, select, textarea')) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); stopPlay(); show(idx + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); stopPlay(); show(idx - 1); }
  });

  // Leaving the page stops playback; the warm worker is kept for next time.
  const mo = new MutationObserver(() => {
    if (!view.isConnected) { stopPlay(); mo.disconnect(); }
  });
  mo.observe(document.getElementById('app') || document.body, { childList: true });

  // Arrived from the home page's "Dry run it" with code in hand.
  let handoff = null;
  try {
    handoff = sessionStorage.getItem('av-dryrun-code');
    sessionStorage.removeItem('av-dryrun-code');
  } catch { /* storage blocked — the student can paste here instead */ }
  if (handoff && params?.get('dry') === '1') {
    codeArea.value = handoff;
    if (langSelect) langSelect.value = 'python';
    callInput.value = '';
    codeArea.dispatchEvent(new Event('input'));
    if (hasTopLevelCode(handoff)) run();
    else {
      panel.classList.remove('is-hidden');
      setStatus('Add a call', 'is-warn');
      noteEl.textContent = 'Your code defines functions but never calls one. '
        + 'Type a call in “Then run” with your own values, then press Dry run.';
      callInput.focus();
    }
  } else {
    syncCall();
  }
}
