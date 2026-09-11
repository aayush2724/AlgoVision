// Per-student progress, kept in localStorage. Every read/write is wrapped in
// try/catch — the site must work identically with storage blocked or cleared.

const KEY = 'algovision.progress.v1';

function defaultState() {
  return { problems: {}, traces: {}, days: [] };
}

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return defaultState();
    const s = JSON.parse(raw);
    return {
      problems: (s && typeof s.problems === 'object' && s.problems) || {},
      traces: (s && typeof s.traces === 'object' && s.traces) || {},
      days: Array.isArray(s?.days) ? s.days : [],
    };
  } catch {
    return defaultState();
  }
}

function save(state) {
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch { /* storage blocked */ }
}

function todayStr() {
  const d = new Date();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${day}`;
}

function touchDay(state) {
  const t = todayStr();
  if (!state.days.includes(t)) {
    state.days.push(t);
    state.days.sort();
    if (state.days.length > 400) state.days = state.days.slice(-400);
  }
}

export function getStatus(problemId) {
  return load().problems[problemId] || 'unseen';
}

export function markViewed(problemId) {
  const s = load();
  if (!s.problems[problemId]) {
    s.problems[problemId] = 'viewed';
    touchDay(s);
    save(s);
  }
}

// Returns the new status so callers can update their UI
export function toggleCompleted(problemId) {
  const s = load();
  const next = s.problems[problemId] === 'completed' ? 'viewed' : 'completed';
  s.problems[problemId] = next;
  touchDay(s);
  save(s);
  return next;
}

export function recordTraceRun(algoId) {
  const s = load();
  s.traces[algoId] = (s.traces[algoId] || 0) + 1;
  touchDay(s);
  save(s);
}

function streakOf(days) {
  if (!days.length) return 0;
  const set = new Set(days);
  const day = new Date();
  // A streak may end today or yesterday (today's session not started yet)
  const fmt = (d) => {
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${m}-${dd}`;
  };
  if (!set.has(fmt(day))) day.setDate(day.getDate() - 1);
  let n = 0;
  while (set.has(fmt(day))) {
    n++;
    day.setDate(day.getDate() - 1);
  }
  return n;
}

export function stats() {
  const s = load();
  const statuses = Object.values(s.problems);
  const completed = statuses.filter(v => v === 'completed').length;
  const viewed = statuses.filter(v => v === 'viewed').length;
  const tracesRun = Object.values(s.traces).reduce((a, b) => a + b, 0);
  const algorithmsTraced = Object.keys(s.traces).length;
  const streak = streakOf(s.days);
  const points = completed * 25 + viewed * 3 + tracesRun * 5;
  return { completed, viewed, tracesRun, algorithmsTraced, streak, points };
}

// % of a step's problems marked completed
export function stepProgress(problems) {
  if (!problems?.length) return 0;
  const s = load();
  const done = problems.filter(p => s.problems[p.id] === 'completed').length;
  return Math.round((done / problems.length) * 100);
}

export function hasAnyActivity() {
  const s = load();
  return Object.keys(s.problems).length > 0 || Object.keys(s.traces).length > 0;
}

export function exportJSON() {
  return JSON.stringify({ version: 1, exported: todayStr(), ...load() }, null, 2);
}

export function importJSON(text) {
  try {
    const s = JSON.parse(text);
    if (!s || typeof s !== 'object') return { ok: false, error: 'Not a progress file.' };
    const problems = (typeof s.problems === 'object' && s.problems) || null;
    const traces = (typeof s.traces === 'object' && s.traces) || null;
    if (!problems && !traces) return { ok: false, error: 'No progress data found in that file.' };
    const clean = defaultState();
    for (const [k, v] of Object.entries(problems || {})) {
      if ((v === 'viewed' || v === 'completed') && typeof k === 'string' && k.length <= 16) {
        clean.problems[k] = v;
      }
    }
    for (const [k, v] of Object.entries(traces || {})) {
      if (typeof k === 'string' && k.length <= 32 && Number.isFinite(Number(v))) {
        clean.traces[k] = Math.max(0, Math.min(100000, Math.floor(Number(v))));
      }
    }
    clean.days = (Array.isArray(s.days) ? s.days : [])
      .filter(d => typeof d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(d))
      .slice(-400)
      .sort();
    save(clean);
    return { ok: true };
  } catch {
    return { ok: false, error: 'Could not read that file — is it a valid JSON export?' };
  }
}

export function resetAll() {
  try { localStorage.removeItem(KEY); } catch { /* storage blocked */ }
}
