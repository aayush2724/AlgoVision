// The game layer: XP, levels, achievements, daily quests and challenge
// scoring. Sits on top of progress.js (which owns problem/trace state) and
// keeps its own store so progress data stays portable on its own.

import * as P from './progress.js';

const KEY = 'algovision.game.v1';

export const XP = {
  TRACE_RUN:        12,
  PREDICT_CORRECT:  20,
  PREDICT_WRONG:     2,   // still something — guessing beats not playing
  PROBLEM_DONE:     35,
  DAILY_VISIT:      25,
  QUEST_DONE:       60,
};

/* Level curve: each level costs a bit more than the last. */
export function levelFromXp(xp) {
  return Math.max(1, Math.floor(0.5 + Math.sqrt(1 + xp / 55)));
}
export function xpForLevel(lv) {
  return Math.max(0, Math.round((((lv - 0.5) ** 2) - 1) * 55));
}

export const RANKS = [
  'Novice', 'Tracer', 'Pathfinder', 'Optimizer', 'Strategist',
  'Architect', 'Grandmaster',
];
export function rankFor(level) {
  return RANKS[Math.min(RANKS.length - 1, Math.floor((level - 1) / 3))];
}

/* ── Achievements ─────────────────────────────────────────────
   Each has a test() over the combined game + progress state.  */
export const ACHIEVEMENTS = [
  { id: 'first_trace',  icon: '▶', name: 'First Contact',
    desc: 'Run your first live trace.',
    test: (g, s) => s.tracesRun >= 1 },
  { id: 'ten_traces',   icon: '⚡', name: 'Warmed Up',
    desc: 'Run 10 traces.',
    test: (g, s) => s.tracesRun >= 10 },
  { id: 'fifty_traces', icon: '🔥', name: 'Trace Addict',
    desc: 'Run 50 traces.',
    test: (g, s) => s.tracesRun >= 50 },
  { id: 'sorter',       icon: '🏆', name: 'Sorting Hat',
    desc: 'Trace all 5 sorting algorithms.',
    test: (g, s, t) => ['merge_sort', 'quick_sort', 'bubble_sort',
      'insertion_sort', 'selection_sort'].every(a => t[a]) },
  { id: 'pathfinder',   icon: '🗺', name: 'Pathfinder',
    desc: 'Trace every graph algorithm.',
    test: (g, s, t) => ['bfs', 'dfs', 'dijkstra', 'prims_mst', 'kruskals_mst']
      .every(a => t[a]) },
  { id: 'polyglot',     icon: '🧭', name: 'Explorer',
    desc: 'Trace 12 different algorithms.',
    test: (g, s, t) => Object.keys(t).length >= 12 },
  { id: 'completionist', icon: '💎', name: 'Completionist',
    desc: 'Trace all 22 algorithms.',
    test: (g, s, t) => Object.keys(t).length >= 22 },
  { id: 'first_predict', icon: '🎯', name: 'Good Call',
    desc: 'Predict a step correctly.',
    test: (g) => g.correct >= 1 },
  { id: 'combo5',       icon: '🔗', name: 'On a Roll',
    desc: 'Get a 5-prediction streak.',
    test: (g) => g.best.combo >= 5 },
  { id: 'combo15',      icon: '🌟', name: 'Unstoppable',
    desc: 'Get a 15-prediction streak.',
    test: (g) => g.best.combo >= 15 },
  { id: 'sharp',        icon: '🧠', name: 'Sharp Eye',
    desc: '85%+ accuracy over 20+ predictions.',
    test: (g) => (g.correct + g.wrong) >= 20 &&
      g.correct / (g.correct + g.wrong) >= 0.85 },
  { id: 'scholar',      icon: '📘', name: 'Scholar',
    desc: 'Mark 10 problems as understood.',
    test: (g, s) => s.completed >= 10 },
  { id: 'streak3',      icon: '📅', name: 'Habit Forming',
    desc: 'Practise 3 days in a row.',
    test: (g, s) => s.streak >= 3 },
  { id: 'streak7',      icon: '🗓', name: 'Week Streak',
    desc: 'Practise 7 days in a row.',
    test: (g, s) => s.streak >= 7 },
  { id: 'level5',       icon: '⭐', name: 'Levelled Up',
    desc: 'Reach level 5.',
    test: (g) => levelFromXp(g.xp) >= 5 },
  { id: 'level10',      icon: '👑', name: 'Grandmaster Track',
    desc: 'Reach level 10.',
    test: (g) => levelFromXp(g.xp) >= 10 },
];

/* ── Daily quests ─────────────────────────────────────────── */
export const QUESTS = [
  { id: 'q_trace3',   icon: '▶', name: 'Run 3 traces',
    goal: 3, of: (g) => g.today.traces },
  { id: 'q_predict5', icon: '🎯', name: 'Predict 5 steps correctly',
    goal: 5, of: (g) => g.today.correct },
  { id: 'q_learn1',   icon: '📘', name: 'Mark a problem understood',
    goal: 1, of: (g) => g.today.problems },
];

function today() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function blank() {
  return {
    xp: 0, correct: 0, wrong: 0,
    best: { combo: 0 },
    unlocked: [],
    quests: { date: today(), claimed: [] },
    today: { date: today(), traces: 0, correct: 0, problems: 0 },
    lastVisit: '',
  };
}

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    const s = raw ? JSON.parse(raw) : null;
    if (!s || typeof s !== 'object') return blank();
    const g = { ...blank(), ...s };
    g.best = { combo: 0, ...(s.best || {}) };
    g.unlocked = Array.isArray(s.unlocked) ? s.unlocked : [];
    g.quests = { date: today(), claimed: [], ...(s.quests || {}) };
    g.today = { date: today(), traces: 0, correct: 0, problems: 0, ...(s.today || {}) };
    if (g.today.date !== today()) g.today = { date: today(), traces: 0, correct: 0, problems: 0 };
    if (g.quests.date !== today()) g.quests = { date: today(), claimed: [] };
    return g;
  } catch { return blank(); }
}

function save(g) {
  try { localStorage.setItem(KEY, JSON.stringify(g)); } catch { /* blocked */ }
}

/* Events other modules can listen to for celebration UI. */
function emit(name, detail) {
  try { window.dispatchEvent(new CustomEvent(name, { detail })); } catch { /* noop */ }
}

/** Award XP. Emits 'av:xp' and 'av:levelup'; checks achievements. */
export function award(amount, reason = '') {
  const g = load();
  const before = levelFromXp(g.xp);
  g.xp = Math.max(0, g.xp + amount);
  const after = levelFromXp(g.xp);
  save(g);
  emit('av:xp', { amount, reason, xp: g.xp, level: after });
  if (after > before) emit('av:levelup', { level: after, rank: rankFor(after) });
  checkAchievements();
  return g.xp;
}

export function recordTrace(algoId) {
  P.recordTraceRun(algoId);
  const g = load();
  g.today.traces++;
  save(g);
  award(XP.TRACE_RUN, 'Trace run');
}

export function recordProblemDone() {
  const g = load();
  g.today.problems++;
  save(g);
  award(XP.PROBLEM_DONE, 'Problem understood');
}

/** Score one prediction. combo is the caller's current streak. */
export function recordPrediction(isCorrect, combo) {
  const g = load();
  if (isCorrect) {
    g.correct++;
    g.today.correct++;
    g.best.combo = Math.max(g.best.combo, combo);
  } else {
    g.wrong++;
  }
  save(g);
  // Combo multiplier, capped so it stays sane
  const bonus = isCorrect ? Math.min(Math.floor(combo / 3) * 5, 30) : 0;
  award((isCorrect ? XP.PREDICT_CORRECT : XP.PREDICT_WRONG) + bonus,
        isCorrect ? 'Correct prediction' : 'Nice try');
  return bonus;
}

/** Called once per session; grants the daily bonus at most once a day. */
export function touchDailyVisit() {
  const g = load();
  if (g.lastVisit === today()) return false;
  g.lastVisit = today();
  save(g);
  award(XP.DAILY_VISIT, 'Daily visit');
  return true;
}

function traceMap() {
  try {
    const raw = localStorage.getItem('algovision.progress.v1');
    return (raw && JSON.parse(raw).traces) || {};
  } catch { return {}; }
}

/** Unlocks any newly-earned achievements and emits 'av:achievement'. */
export function checkAchievements() {
  const g = load();
  const s = P.stats();
  const t = traceMap();
  let changed = false;
  for (const a of ACHIEVEMENTS) {
    if (g.unlocked.includes(a.id)) continue;
    let ok = false;
    try { ok = !!a.test(g, s, t); } catch { ok = false; }
    if (ok) {
      g.unlocked.push(a.id);
      changed = true;
      emit('av:achievement', a);
    }
  }
  if (changed) save(g);
  return g.unlocked;
}

export function questState() {
  const g = load();
  return QUESTS.map(q => {
    const have = Math.min(q.of(g), q.goal);
    return { ...q, have, done: have >= q.goal, claimed: g.quests.claimed.includes(q.id) };
  });
}

export function claimQuest(id) {
  const g = load();
  const q = questState().find(x => x.id === id);
  if (!q || !q.done || q.claimed) return false;
  g.quests.claimed.push(id);
  save(g);
  award(XP.QUEST_DONE, `Quest: ${q.name}`);
  return true;
}

export function state() {
  const g = load();
  const s = P.stats();
  const level = levelFromXp(g.xp);
  const base = xpForLevel(level);
  const next = xpForLevel(level + 1);
  const shots = g.correct + g.wrong;
  return {
    xp: g.xp,
    level,
    rank: rankFor(level),
    intoLevel: g.xp - base,
    levelSpan: Math.max(1, next - base),
    pct: Math.round(((g.xp - base) / Math.max(1, next - base)) * 100),
    correct: g.correct,
    wrong: g.wrong,
    accuracy: shots ? Math.round((g.correct / shots) * 100) : 0,
    bestCombo: g.best.combo,
    unlocked: g.unlocked,
    streak: s.streak,
    tracesRun: s.tracesRun,
    completed: s.completed,
  };
}

export function resetGame() {
  try { localStorage.removeItem(KEY); } catch { /* blocked */ }
}
