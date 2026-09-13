import { api } from './api.js';
import * as DATA from './data.js';
import * as Progress from './progress.js';
import * as Game from './game.js';

// ── REAL-WORLD SCENE RENDERERS ──────────────────────────────────────────────
// Each scene knows how to draw itself and label nodes/edges in metaphor language.

const SCENES = {
  gps: {
    label: "GPS NAVIGATION",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {
      // Draw road grid background lines (faint)
      for (let i = 0; i < 5; i++) {
        const line = makeSVG("line");
        Object.assign(line, {});
        line.setAttribute("x1", 0); line.setAttribute("y1", 60 + i * 50);
        line.setAttribute("x2", 800); line.setAttribute("y2", 60 + i * 50);
        line.setAttribute("stroke", "rgba(95,214,230,0.04)");
        line.setAttribute("stroke-width", "1");
        svg.appendChild(line);
      }
    },
    nodeLabel: (id) => `📍 ${id}`,
    edgeLabel: (w) => `${w} min`,
    stepNarrate(step, meta) {
      const m = meta.metaphors;
      if (step.note?.includes("Start")) return `${m.start} — setting distance to 0.`;
      if (step.note?.includes("Visit")) return `${m.visit} ${step.node || step.highlight?.node}. Checking all nearby roads.`;
      if (step.note?.includes("Relax")) return `${m.relax} ${step.node || step.highlight?.node}! Updating route on map.`;
      return step.note || "GPS computing...";
    }
  },
  social: {
    label: "SOCIAL NETWORK",
    color: "#a9f0fa",
    accentColor: "#5fd6e6",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `👤 ${id}`,
    edgeLabel: (w) => `friend`,
    stepNarrate(step, meta) {
      const m = meta.metaphors;
      if (step.note?.includes("Enqueue") || step.note?.includes("start")) return `${m.start} — scanning your immediate connections.`;
      if (step.note?.includes("Dequeue")) return `${m.visit} ${step.node || step.highlight?.node}'s profile.`;
      if (step.note?.includes("Discover")) return `${m.enqueue} — ${step.node || step.highlight?.node} is a friend-of-a-friend!`;
      return step.note || "Scanning network...";
    }
  },
  library: {
    label: "LIBRARY CATALOG",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `📚 ${id}`,
    edgeLabel: (w) => `section`,
    stepNarrate(step, meta) {
      const m = meta.metaphors || {};
      const idx = step.highlight?.index;
      const prefix = (idx === null || idx === undefined)
        ? '' : `${m.visit || 'Checking'} ${idx}. `;
      return `${prefix}${step.note || "Searching catalog..."}`;
    }
  },
  maze: {
    label: "MAZE EXPLORER",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🚪 ${id}`,
    edgeLabel: (w) => `corridor`,
    stepNarrate(step, meta) {
      const m = meta.metaphors;
      if (step.note?.includes("backtrack") || step.note?.toLowerCase().includes("visited")) return `${m.backtrack}`;
      return `${m.visit} ${step.node || step.highlight?.node}. ${step.note || "Exploring..."}`;
    }
  },
  leaderboard: {
    label: "LEADERBOARD SORT",
    color: "#a9f0fa",
    accentColor: "#5fd6e6",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🏆 ${id}`,
    edgeLabel: (w) => `vs`,
    stepNarrate(step, meta) {
      return `${step.note || "Comparing scores..."}`;
    }
  },
  vault: {
    label: "DECISION VAULT",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `💾 ${id}`,
    edgeLabel: (w) => `depends on`,
    stepNarrate(step, meta) {
      return `${step.note || "Computing optimal subproblem..."}`;
    }
  },
  train: {
    label: "TRAIN YARD",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🚃 ${id}`,
    edgeLabel: (w) => `coupling`,
    stepNarrate(step, meta) {
      return `${step.note || "Recoupling carriages..."}`;
    }
  },
  plates: {
    label: "PLATE STACK",
    color: "#a9f0fa",
    accentColor: "#5fd6e6",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🍽 ${id}`,
    edgeLabel: (w) => `match`,
    stepNarrate(step, meta) {
      return `${step.note || "Checking the stack..."}`;
    }
  },
  files: {
    label: "FILE SYSTEM",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `📁 ${id}`,
    edgeLabel: (w) => `subfolder`,
    stepNarrate(step, meta) {
      return `${step.note || "Walking the directory tree..."}`;
    }
  },
  scheduler: {
    label: "TRIAGE QUEUE",
    color: "#a9f0fa",
    accentColor: "#5fd6e6",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🏥 ${id}`,
    edgeLabel: (w) => `priority`,
    stepNarrate(step, meta) {
      return `${step.note || "Sorting the waiting room..."}`;
    }
  },
  market: {
    label: "SUPERMARKET",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🛒 ${id}`,
    edgeLabel: (w) => `pairing`,
    stepNarrate(step, meta) {
      return `${step.note || "Checking prices..."}`;
    }
  },
  stocks: {
    label: "MARKET CHART",
    color: "#a9f0fa",
    accentColor: "#5fd6e6",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `📈 ${id}`,
    edgeLabel: (w) => `streak`,
    stepNarrate(step, meta) {
      return `${step.note || "Tracking the run..."}`;
    }
  },
  grid_power: {
    label: "POWER GRID",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `⚡ ${id}`,
    edgeLabel: (w) => `${w} cost`,
    stepNarrate(step, meta) {
      return `${step.note || "Laying cable..."}`;
    }
  },
  dna: {
    label: "GENE LAB",
    color: "#5fd6e6",
    accentColor: "#a9f0fa",
    renderBase(svg, graph, meta) {},
    nodeLabel: (id) => `🧬 ${id}`,
    edgeLabel: (w) => `alignment`,
    stepNarrate(step, meta) {
      return `${step.note || "Aligning strands..."}`;
    }
  }
};

function makeSVG(tag) {
  return document.createElementNS("http://www.w3.org/2000/svg", tag);
}

// Escape text that gets interpolated into innerHTML (AI output is untrusted).
function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}

// ── Algorithm resolution ─────────────────────────────────────────────────────
// Maps any world/route name to a traceable algorithm id and its view type.

const VIEW_FOR = {
  dijkstra: 'graph', bfs: 'graph', dfs: 'graph',
  prims_mst: 'graph', kruskals_mst: 'graph',
  binary_search: 'array', merge_sort: 'array', quick_sort: 'array',
  bubble_sort: 'array', insertion_sort: 'array', selection_sort: 'array',
  linked_list_reverse: 'list', balanced_brackets: 'stack',
  bst_insert: 'tree', bst_search: 'tree', heap_insert: 'tree',
  two_sum_sorted: 'array', sliding_window: 'array', kadanes: 'array',
  knapsack_01: 'grid', lcs: 'grid',
  fibonacci_dp: 'table',
  topological_sort: 'graph',
  counting_sort: 'array', prefix_sums: 'array', next_greater_element: 'array',
  edit_distance: 'grid', floyd_cycle: 'list',
  tree_traversal: 'tree', trie_insert: 'tree',
  n_queens: 'grid', unique_paths: 'grid', sieve: 'array',
  kmp_search: 'array', segment_tree: 'tree', fenwick_tree: 'array',
  hash_table: 'grid', bst_delete: 'tree', heap_extract: 'tree',
  dsu: 'graph', merge_intervals: 'array', coin_change: 'grid',
  connected_components: 'graph', bipartite_check: 'graph', flood_fill: 'grid',
  house_robber: 'grid', lis: 'grid', subset_sum: 'grid',
  z_function: 'array', rabin_karp: 'array', manacher: 'array',
};

function resolveAlgoId(raw) {
  const key = String(raw || '').toLowerCase().replace(/[\s-]/g, '');
  // An exact catalog id always wins. The fuzzy list below is only for
  // aliases and scene names; without this, a new algorithm that matches no
  // alias would silently fall through to the dijkstra default.
  if (DATA.ALGORITHMS.some(a => a.id === key)) return key;
  const MAP = [
    ['edit_distance', 'edit_distance'], ['editdistance', 'edit_distance'],
    ['levenshtein', 'edit_distance'],
    ['topological', 'topological_sort'], ['toposort', 'topological_sort'],
    ['kahn', 'topological_sort'],
    ['counting_sort', 'counting_sort'], ['countingsort', 'counting_sort'],
    ['counting', 'counting_sort'],
    ['prefix', 'prefix_sums'], ['rangesum', 'prefix_sums'],
    ['nextgreater', 'next_greater_element'], ['next_greater', 'next_greater_element'],
    ['monotonic', 'next_greater_element'], ['nge', 'next_greater_element'],
    ['floyd', 'floyd_cycle'], ['tortoise', 'floyd_cycle'],
    ['cycledetect', 'floyd_cycle'], ['detectcycle', 'floyd_cycle'],
    ['fibonacci_dp', 'fibonacci_dp'], ['fibonacci', 'fibonacci_dp'],
    ['dynamic_programming', 'fibonacci_dp'], ['memovault', 'fibonacci_dp'],
    ['vault', 'fibonacci_dp'],
    ['linked_list_reverse', 'linked_list_reverse'], ['linkedlist', 'linked_list_reverse'],
    ['theflow', 'linked_list_reverse'], ['train', 'linked_list_reverse'],
    ['balanced_brackets', 'balanced_brackets'], ['brackets', 'balanced_brackets'],
    ['plates', 'balanced_brackets'], ['parenthes', 'balanced_brackets'],
    ['bubble_sort', 'bubble_sort'], ['bubblesort', 'bubble_sort'], ['bubble', 'bubble_sort'],
    ['insertion_sort', 'insertion_sort'], ['insertionsort', 'insertion_sort'], ['insertion', 'insertion_sort'],
    ['selection_sort', 'selection_sort'], ['selectionsort', 'selection_sort'], ['selection', 'selection_sort'],
    ['prims_mst', 'prims_mst'], ['prim', 'prims_mst'],
    ['kruskals_mst', 'kruskals_mst'], ['kruskal', 'kruskals_mst'],
    ['unionfind', 'kruskals_mst'], ['dsu', 'kruskals_mst'],
    ['spanningtree', 'prims_mst'], ['mst', 'prims_mst'],
    ['knapsack_01', 'knapsack_01'], ['knapsack', 'knapsack_01'],
    ['lcs', 'lcs'], ['longestcommon', 'lcs'], ['dna', 'lcs'],
    ['two_sum_sorted', 'two_sum_sorted'], ['twosum', 'two_sum_sorted'],
    ['two_pointers', 'two_sum_sorted'], ['twopointer', 'two_sum_sorted'],
    ['market', 'two_sum_sorted'],
    ['sliding_window', 'sliding_window'], ['slidingwindow', 'sliding_window'],
    ['windowslide', 'sliding_window'],
    ['kadane', 'kadanes'], ['maxsubarray', 'kadanes'], ['stockchart', 'kadanes'],
    ['stocks', 'kadanes'],
    ['binarysearchtree', 'bst_insert'], ['bst_search', 'bst_search'],
    ['bst_insert', 'bst_insert'], ['bst', 'bst_insert'], ['files', 'bst_insert'],
    ['heap_insert', 'heap_insert'], ['heapify', 'heap_insert'], ['heap', 'heap_insert'],
    ['priorityqueue', 'heap_insert'], ['scheduler', 'heap_insert'], ['triage', 'heap_insert'],
    ['binary_search', 'binary_search'], ['binarysearch', 'binary_search'],
    ['thehunt', 'binary_search'], ['library', 'binary_search'],
    ['quick_sort', 'quick_sort'], ['quicksort', 'quick_sort'],
    ['merge_sort', 'merge_sort'], ['mergesort', 'merge_sort'],
    ['sorting', 'merge_sort'], ['leaderboard', 'merge_sort'],
    ['dfs', 'dfs'], ['maze', 'dfs'], ['labyrinth', 'dfs'], ['backtrack', 'dfs'],
    ['sixdegrees', 'bfs'], ['social', 'bfs'], ['graphs', 'bfs'], ['graph', 'bfs'],
    ['bfs', 'bfs'],
    ['gps', 'dijkstra'], ['dijkstra', 'dijkstra'],
    ['dp', 'fibonacci_dp'],
  ];
  for (const [k, v] of MAP) if (key.includes(k)) return v;
  return 'dijkstra';
}

const fmt = (v) => String(Number(v));
// Cells are usually numbers, but some structures carry glyphs or letters
// (a trie's characters, a chessboard's queens) — pass those through as-is.
const fmtCell = (v) => (typeof v === 'string' ? v : fmt(v));

// Undirected edge key — same key for either direction
function edgeKey(a, b) {
  return a < b ? `${a}|${b}` : `${b}|${a}`;
}

const COUNT_LABELS = {
  visits: 'VISITS', edge_checks: 'EDGE CHECKS', relaxations: 'RELAXATIONS',
  heap_pushes: 'HEAP PUSHES', enqueues: 'ENQUEUES', dequeues: 'DEQUEUES',
  comparisons: 'COMPARISONS', writes: 'WRITES', merges: 'MERGES',
  swaps: 'SWAPS', partitions: 'PARTITIONS', backtracks: 'BACKTRACKS',
  calls: 'CALLS', cache_hits: 'CACHE HITS', computes: 'COMPUTES',
  passes: 'PASSES', shifts: 'SHIFTS', inserts: 'INSERTS',
  flips: 'FLIPS', pushes: 'PUSHES', pops: 'POPS',
  insertions: 'INSERTIONS', checks: 'CHECKS', moves: 'MOVES',
  additions: 'ADDITIONS', windows: 'WINDOWS',
  extensions: 'EXTENSIONS', restarts: 'RESTARTS', steps: 'STEPS',
  cells: 'CELLS', takes: 'TAKES', skips: 'SKIPS', matches: 'MATCHES',
  edges_added: 'EDGES ADDED', rejections: 'CYCLES AVOIDED',
  emitted: 'TASKS EMITTED', edge_relaxations: 'DEPENDENCIES CLEARED',
  tallies: 'TALLIES', query_ops: 'RANGE QUERIES',
  free_matches: 'FREE MATCHES', edits_charged: 'EDITS CHARGED',
  slow_moves: 'SLOW STEPS', fast_moves: 'FAST STEPS',
  descents: 'RECURSIVE CALLS', nodes_created: 'NODES CREATED',
  prefix_reuses: 'PREFIXES REUSED', words_added: 'WORDS ADDED',
  placements: 'QUEENS PLACED', conflicts: 'SQUARES REJECTED',
  solutions: 'SOLUTIONS', blocked: 'WALLS',
  primes_found: 'PRIMES FOUND', crossings: 'NUMBERS CROSSED OUT',
  skipped_as_done: 'PAST √N',
  shifts: 'PATTERN SHIFTS', naive_would_cost: 'NAIVE WOULD COST',
  nodes_built: 'NODES BUILT', nodes_visited: 'NODES VISITED',
  full_covers: 'WHOLE BLOCKS REUSED',
  elements_scanned_naively: 'NAIVE WOULD SCAN',
  updates: 'VALUES FOLDED IN', slots_touched: 'SLOTS TOUCHED',
  query_reads: 'SLOTS READ',
  unions: 'UNIONS', cycles_skipped: 'CYCLES SKIPPED',
};

// Value over label, right-aligned — the number is what changes each step,
// so it reads first. `compact` is for the side-by-side compare panes.
function countChips(counts, compact = false) {
  return Object.entries(counts || {}).map(([k, v]) =>
    `<div class="counter${compact ? ' counter-compact' : ''}">` +
    `<span class="counter-num">${v}</span>` +
    `<span class="counter-label">${COUNT_LABELS[k] || k.replace(/_/g, ' ')}</span></div>`
  ).join('');
}

// ── MAIN ENGINE MOUNT ────────────────────────────────────────────────────────

export function mountEngine(view, algo = 'dijkstra') {
  const svg = view.querySelector('#engine-svg');
  const status = view.querySelector('#engine-status');
  const note = view.querySelector('#engine-note');
  const runBtn = view.querySelector('#run-btn');
  const stepBtn = view.querySelector('#step-btn');
  const resetBtn = view.querySelector('#reset-btn');
  const explainBtn = view.querySelector('#explain-btn');
  const explanationBox = view.querySelector('#explanation-box');
  const arrayControls = view.querySelector('#array-controls');
  const arrayInput    = view.querySelector('#array-input');
  const targetWrap    = view.querySelector('#target-wrap');
  const targetInput   = view.querySelector('#target-input');
  const arrayHint     = view.querySelector('#array-hint');
  const prevBtn       = view.querySelector('#prev-btn');
  const playBtn       = view.querySelector('#play-btn');
  const speedSelect   = view.querySelector('#speed-select');
  const stepSlider    = view.querySelector('#step-slider');
  const scrubRow      = view.querySelector('#scrub-row');
  const counterPanel  = view.querySelector('#counter-panel');
  const compareBtn    = view.querySelector('#compare-btn');
  const comparePanel  = view.querySelector('#compare-panel');
  const compareSlider = view.querySelector('#compare-slider');

  const algoId = resolveAlgoId(algo);
  const traceView = VIEW_FOR[algoId] || 'graph';

  let currentSteps = [];
  let currentStepIdx = -1;
  let isOffline = false;
  let currentMeta = null;  // stores realworld_meta for current algo
  let currentScene = null; // stores scene renderer
  let currentArrayValues = [];
  let traceSummary = '';   // end-of-trace message (unreachable nodes, not-found…)
  let currentTraceMeta = null;  // meta of the loaded trace (grid labels, results…)
  let playTimer = null;
  let compareData = null;  // { bfs: steps[], dijkstra: steps[] }
  let compareIdx = 0;
  let comparePlayTimer = null;

  // ── Editable graph state (graph view) ──
  // Mirrors the server limits in tracers/common.py
  const GRAPH_LIMITS = { nodes: 50, edges: 200, weight: 1_000_000 };

  const graphControls = view.querySelector('#graph-controls');
  const presetSelect  = view.querySelector('#preset-select');
  const startSelect   = view.querySelector('#start-select');
  const graphStats    = view.querySelector('#graph-stats');
  const graphError    = view.querySelector('#graph-error');

  function graphPreset(name) {
    if (name === 'tree') return {
      nodes: [
        { id: 'A', x: 380, y: 50 },  { id: 'B', x: 220, y: 130 }, { id: 'C', x: 540, y: 130 },
        { id: 'D', x: 140, y: 225 }, { id: 'E', x: 300, y: 225 }, { id: 'F', x: 460, y: 225 },
        { id: 'G', x: 620, y: 225 },
      ],
      links: [
        { source: 'A', target: 'B', weight: 2 }, { source: 'A', target: 'C', weight: 3 },
        { source: 'B', target: 'D', weight: 1 }, { source: 'B', target: 'E', weight: 4 },
        { source: 'C', target: 'F', weight: 2 }, { source: 'C', target: 'G', weight: 5 },
      ],
    };
    if (name === 'disconnected') return {
      nodes: [
        { id: 'A', x: 140, y: 100 }, { id: 'B', x: 300, y: 70 },  { id: 'C', x: 300, y: 185 },
        { id: 'D', x: 520, y: 90 },  { id: 'E', x: 660, y: 150 }, { id: 'F', x: 520, y: 230 },
      ],
      links: [
        { source: 'A', target: 'B', weight: 3 }, { source: 'A', target: 'C', weight: 2 },
        { source: 'B', target: 'C', weight: 4 }, { source: 'D', target: 'E', weight: 2 },
      ],
    };
    if (name === 'clear') return { nodes: [], links: [] };
    return JSON.parse(JSON.stringify({
      nodes: DATA.SAMPLE_GRAPH.nodes,
      links: DATA.SAMPLE_GRAPH.links,
    }));
  }

  let userGraph = graphPreset('sample');
  let startNodeId = userGraph.nodes[0]?.id || null;
  let selectedNodeId = null;

  function nextNodeId() {
    const used = new Set(userGraph.nodes.map(n => n.id));
    for (let c = 65; c <= 90; c++) {
      const id = String.fromCharCode(c);
      if (!used.has(id)) return id;
    }
    let n = 27;
    while (used.has(`N${n}`)) n++;
    return `N${n}`;
  }

  function showGraphError(msg) {
    if (!graphError) return;
    graphError.textContent = msg;
    graphError.style.display = 'block';
    clearTimeout(graphError._t);
    graphError._t = setTimeout(() => { graphError.style.display = 'none'; }, 3500);
  }

  function updateGraphMeta() {
    if (graphStats) {
      graphStats.textContent =
        `${userGraph.nodes.length} nodes · ${userGraph.links.length} edges`;
    }
    if (startSelect) {
      startSelect.innerHTML = userGraph.nodes
        .map(n => `<option value="${n.id}"${n.id === startNodeId ? ' selected' : ''}>${n.id}</option>`)
        .join('');
    }
  }

  function resetTraceState() {
    stopPlay();
    currentStepIdx = -1;
    currentSteps = [];
    traceSummary = '';
    stepBtn.disabled = true;
    if (prevBtn) prevBtn.disabled = true;
    if (playBtn) playBtn.disabled = true;
    if (scrubRow) scrubRow.style.display = 'none';
    if (counterPanel) counterPanel.style.display = 'none';
    const liveEl = view.querySelector('#complexity-live');
    if (liveEl) liveEl.style.display = 'none';
    runBtn.disabled = false;
    note.style.opacity = 0;
    explanationBox.classList.add('is-hidden');
    status.innerHTML = 'STATUS: IDLE';
    status.className = 'engine-status-pill';
    const counter = view.querySelector('#step-counter');
    if (counter) counter.textContent = '';
  }

  function graphChanged() {
    if (!userGraph.nodes.find(n => n.id === startNodeId)) {
      startNodeId = userGraph.nodes[0]?.id || null;
    }
    selectedNodeId = null;
    resetTraceState();
    // A stale comparison over an edited graph would lie — close it.
    if (comparePanel && !comparePanel.classList.contains('is-hidden')) closeCompare();
    renderGraph(currentMeta);
    updateGraphMeta();
    buildWhatIfSliders();
  }

  // ── Set scene based on algo name ──
  function resolveScene(algoName) {
    const map = {
      dijkstra: 'gps', bfs: 'social', dfs: 'maze',
      binary_search: 'library', merge_sort: 'leaderboard',
      dynamic_programming: 'vault', quick_sort: 'leaderboard',
      fibonacci_dp: 'vault',
      bubble_sort: 'leaderboard', insertion_sort: 'leaderboard',
      selection_sort: 'leaderboard',
      linked_list_reverse: 'train', balanced_brackets: 'plates',
      bst_insert: 'files', bst_search: 'files', heap_insert: 'scheduler',
      two_sum_sorted: 'market', sliding_window: 'stocks', kadanes: 'stocks',
      knapsack_01: 'vault', lcs: 'dna',
      prims_mst: 'grid_power', kruskals_mst: 'grid_power',
    };
    return map[algoName] || 'gps';
  }

  // ── Render the graph with scene-aware labels ──
  function renderGraph(meta) {
    svg.innerHTML = '';
    const sceneName = meta?.scene || resolveScene(algo);
    const scene = SCENES[sceneName] || SCENES.gps;
    currentScene = scene;

    // Scene-specific background decoration
    if (scene.renderBase) scene.renderBase(svg, userGraph, meta);

    if (!userGraph.nodes.length) {
      const hint = makeSVG("text");
      hint.setAttribute("x", "380"); hint.setAttribute("y", "145");
      hint.setAttribute("text-anchor", "middle");
      hint.setAttribute("fill", "var(--cDim)");
      hint.setAttribute("font-family", "var(--font-ui)");
      hint.setAttribute("font-size", "9");
      hint.textContent = "CLICK ANYWHERE TO ADD YOUR FIRST NODE";
      svg.appendChild(hint);
    }

    // Draw edges
    userGraph.links.forEach((link, idx) => {
      const source = userGraph.nodes.find(n => n.id === link.source);
      const target = userGraph.nodes.find(n => n.id === link.target);
      if (!source || !target) return;

      const line = makeSVG("line");
      line.setAttribute("x1", source.x); line.setAttribute("y1", source.y);
      line.setAttribute("x2", target.x); line.setAttribute("y2", target.y);
      line.setAttribute("class", "edge");
      line.setAttribute("id", `edge-${link.source}-${link.target}`);
      line.dataset.idx = idx;
      svg.appendChild(line);

      // Edge weight label — click to edit, right-click to delete
      const tx = makeSVG("text");
      tx.setAttribute("x", (source.x + target.x) / 2);
      tx.setAttribute("y", (source.y + target.y) / 2 - 6);
      tx.setAttribute("fill", "var(--cDim)");
      tx.setAttribute("font-family", "var(--font-mono)");
      tx.setAttribute("font-size", "11");
      tx.setAttribute("text-anchor", "middle");
      tx.setAttribute("class", "edge-weight");
      tx.dataset.idx = idx;
      tx.style.cursor = 'pointer';
      tx.textContent = scene.edgeLabel(link.weight);
      svg.appendChild(tx);
    });

    // Draw nodes
    userGraph.nodes.forEach(node => {
      const circle = makeSVG("circle");
      circle.setAttribute("cx", node.x); circle.setAttribute("cy", node.y);
      circle.setAttribute("r", "22");
      circle.setAttribute("class", "node");
      circle.setAttribute("id", `node-${node.id}`);
      circle.style.cursor = 'pointer';
      if (node.id === selectedNodeId) {
        circle.style.stroke = 'var(--c)';
        circle.style.strokeWidth = '3';
      }
      svg.appendChild(circle);

      // Node ID label
      const idText = makeSVG("text");
      idText.setAttribute("x", node.x); idText.setAttribute("y", node.y + 4);
      idText.setAttribute("text-anchor", "middle");
      idText.setAttribute("fill", "var(--cBright)");
      idText.setAttribute("font-family", "var(--font-ui)");
      idText.setAttribute("font-size", "9");
      idText.textContent = node.id;
      svg.appendChild(idText);

      // Scene-aware emoji label above node
      const emojiText = makeSVG("text");
      emojiText.setAttribute("x", node.x); emojiText.setAttribute("y", node.y - 30);
      emojiText.setAttribute("text-anchor", "middle");
      emojiText.setAttribute("font-size", "14");
      emojiText.setAttribute("opacity", "0.5");
      const label = scene.nodeLabel(node.id);
      emojiText.textContent = label.split(' ')[0]; // just the emoji
      svg.appendChild(emojiText);

      // Distance readout below node (filled in per-step for Dijkstra)
      const distText = makeSVG("text");
      distText.setAttribute("x", node.x);
      distText.setAttribute("y", node.y + 38);
      distText.setAttribute("text-anchor", "middle");
      distText.setAttribute("fill", "var(--c)");
      distText.setAttribute("font-family", "var(--font-mono)");
      distText.setAttribute("font-size", "10");
      distText.setAttribute("id", `dist-${node.id}`);
      svg.appendChild(distText);

      // Full location name below node (for GPS scene)
      if (node.label && currentMeta?.scene === 'gps') {
        const nameText = makeSVG("text");
        nameText.setAttribute("x", node.x);
        nameText.setAttribute("y", node.y + 51);
        nameText.setAttribute("text-anchor", "middle");
        nameText.setAttribute("fill", "var(--cDim)");
        nameText.setAttribute("font-family", "var(--font-mono)");
        nameText.setAttribute("font-size", "9");
        nameText.textContent = node.label;
        svg.appendChild(nameText);
      }
    });

    // Scene label in corner
    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);
  }

  // ── Array view (binary search / merge sort) ──
  function renderArrayView(values) {
    svg.innerHTML = '';
    currentArrayValues = values.slice();
    const scene = SCENES[currentMeta?.scene] || SCENES[resolveScene(algoId)] || SCENES.library;
    currentScene = scene;

    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);

    const n = values.length;
    if (!n) return;
    const w = Math.min(56, 700 / n);
    const x0 = (760 - w * n) / 2;
    const y = 110, h = 52;

    values.forEach((v, idx) => {
      const g = makeSVG("g");
      g.setAttribute("id", `cellg-${idx}`);

      const rect = makeSVG("rect");
      rect.setAttribute("x", x0 + idx * w + 2);
      rect.setAttribute("y", y);
      rect.setAttribute("width", Math.max(w - 4, 6));
      rect.setAttribute("height", h);
      rect.setAttribute("id", `cell-${idx}`);
      rect.setAttribute("fill", "rgba(212, 96, 44,0.05)");
      rect.setAttribute("stroke", "var(--cDim)");
      rect.setAttribute("stroke-width", "1");
      g.appendChild(rect);

      const val = makeSVG("text");
      val.setAttribute("x", x0 + idx * w + w / 2);
      val.setAttribute("y", y + h / 2 + 5);
      val.setAttribute("text-anchor", "middle");
      val.setAttribute("fill", "var(--cBright)");
      val.setAttribute("font-family", "var(--font-mono)");
      val.setAttribute("font-size", w < 34 ? "11" : "14");
      val.setAttribute("id", `cellval-${idx}`);
      val.textContent = fmtCell(v);
      g.appendChild(val);

      const pos = makeSVG("text");
      pos.setAttribute("x", x0 + idx * w + w / 2);
      pos.setAttribute("y", y + h + 16);
      pos.setAttribute("text-anchor", "middle");
      pos.setAttribute("fill", "var(--cDim)");
      pos.setAttribute("font-family", "var(--font-ui)");
      pos.setAttribute("font-size", "6");
      pos.textContent = idx;
      g.appendChild(pos);

      svg.appendChild(g);
    });
  }

  // Fully re-renders cell states from one step — idempotent, works for any index.
  function renderArrayStep(step) {
    const s = step.structures || {};
    if (Array.isArray(s.array)) {
      s.array.forEach((v, idx) => {
        const el = svg.querySelector(`#cellval-${idx}`);
        if (el) el.textContent = fmtCell(v);
      });
    }
    for (let idx = 0; idx < currentArrayValues.length; idx++) {
      const cell = svg.querySelector(`#cell-${idx}`);
      const g = svg.querySelector(`#cellg-${idx}`);
      if (!cell) continue;
      cell.setAttribute("fill", "rgba(212, 96, 44,0.05)");
      cell.setAttribute("stroke", "var(--cDim)");
      cell.setAttribute("stroke-width", "1");
      if (g) g.setAttribute("opacity", "1");

      if (algoId === 'binary_search') {
        const inRange = s.low != null && idx >= s.low && idx <= s.high;
        if (!inRange && g) g.setAttribute("opacity", "0.22");
        if (inRange) cell.setAttribute("stroke", "var(--c)");
        if (idx === s.mid) {
          cell.setAttribute("fill", "rgba(212, 96, 44,0.18)");
          cell.setAttribute("stroke", s.found ? "#4ade80" : "var(--c)");
          cell.setAttribute("stroke-width", "2");
        }
      } else if (algoId === 'two_sum_sorted') {
        const inRange = s.left != null && idx >= s.left && idx <= s.right;
        if (!inRange && g) g.setAttribute("opacity", "0.22");
        if (idx === s.left || idx === s.right) {
          cell.setAttribute("fill", s.found
            ? "rgba(74,222,128,0.2)" : "rgba(212, 96, 44,0.18)");
          cell.setAttribute("stroke", s.found ? "#4ade80" : "var(--c)");
          cell.setAttribute("stroke-width", "2");
        }
      } else if (algoId === 'sliding_window' || algoId === 'kadanes') {
        const inBest = s.best_window && idx >= s.best_window[0] && idx <= s.best_window[1];
        const inWindow = s.window && idx >= s.window[0] && idx <= s.window[1];
        if (inBest) cell.setAttribute("stroke", "#4ade80");
        if (inWindow) {
          cell.setAttribute("fill", "rgba(212, 96, 44,0.14)");
          if (!inBest) cell.setAttribute("stroke", "var(--c)");
          cell.setAttribute("stroke-width", inBest ? "2.5" : "1.5");
        }
      } else {
        const inSorted = (s.sorted_ranges || []).some(r => idx >= r[0] && idx <= r[1]);
        if (inSorted) cell.setAttribute("stroke", "#4ade80");
        if (s.merging && idx >= s.merging[0] && idx <= s.merging[1] && !inSorted) {
          cell.setAttribute("stroke", "var(--c)");
        }
        if (idx === s.placed) {
          cell.setAttribute("fill", "rgba(212, 96, 44,0.18)");
          cell.setAttribute("stroke", "var(--c)");
          cell.setAttribute("stroke-width", "2");
        }
      }
    }
  }

  const ARRAY_DEFAULTS = {
    binary_search: {
      array: '1, 3, 5, 7, 9, 12, 15', target: '9',
      hint: 'Up to 20 numbers. Unsorted input is sorted for you — binary search needs sorted data.',
    },
    merge_sort: {
      array: '7, 3, 9, 1, 12, 5',
      hint: 'Up to 16 numbers — watch them merge into order.',
    },
    quick_sort: {
      array: '7, 3, 9, 1, 12, 5',
      hint: 'Up to 16 numbers — pivots lock into their final place one at a time.',
    },
    bubble_sort: {
      array: '7, 3, 9, 1, 12, 5',
      hint: 'Up to 16 numbers — heavy values bubble to the right, pass by pass.',
    },
    insertion_sort: {
      array: '7, 3, 9, 1, 12, 5',
      hint: 'Up to 16 numbers — each one slides into place like a playing card.',
    },
    selection_sort: {
      array: '7, 3, 9, 1, 12, 5',
      hint: 'Up to 16 numbers — every round crowns a champion.',
    },
    linked_list_reverse: {
      array: '10, 20, 30, 40, 50',
      hint: 'Up to 10 values — watch every coupling flip, one pointer at a time.',
    },
    balanced_brackets: {
      array: '({[]})',
      hint: 'Brackets only: ( ) [ ] { } — up to 20. Try breaking it: (] or ((',
    },
    two_sum_sorted: {
      array: '1, 3, 5, 7, 9, 12', target: '16',
      hint: 'Sorted values + a target sum. Two pointers converge from both ends — one pass, no nested loops.',
    },
    sliding_window: {
      array: '4, 2, 9, 7, 1, 8, 6', target: '3',
      hint: 'K is the window size. Slide it across — drop one value, add one value, never recount.',
    },
    kadanes: {
      array: '-2, 1, -3, 4, -1, 2, 1, -5, 4',
      hint: 'Negatives welcome — that\'s the whole point. Extend the run or cut your losses.',
    },
    counting_sort: {
      array: '4, 2, 2, 8, 3, 3, 1',
      hint: 'Whole numbers 0–20 only. It sorts without ever comparing two values — try a big value like 20 and watch the empty buckets it costs.',
    },
    prefix_sums: {
      array: '3, 1, 4, 1, 5, 9',
      hint: 'The cells become running totals, not your original values. Any range sum then costs one subtraction.',
    },
    next_greater_element: {
      array: '2, 1, 2, 4, 3',
      hint: 'For each value, the first bigger one to its right. Try a descending list — nothing ever gets popped.',
    },
    edit_distance: {
      array: 'KITTEN, SITTING',
      hint: 'Two words, comma-separated (1–8 chars each). The answer is the fewest insert/delete/substitute edits.',
    },
    floyd_cycle: {
      array: '1, 2, 3, 4, 5', target: '2',
      hint: 'LOOPS TO is the index the tail points back to — use -1 for a normal list with no cycle.',
    },
    tree_traversal: {
      array: '8, 3, 10, 1, 6, 14, 4',
      hint: 'Up to 12 values. The same tree is walked three ways — watch inorder come out sorted.',
    },
    trie_insert: {
      array: 'CAT, CAR, DOG',
      hint: 'Up to 5 words, letters only. Words sharing a prefix reuse the same path — that is the whole idea.',
    },
    n_queens: {
      array: '', target: '6',
      hint: 'Board size 4–6. Watch queens get placed and then taken back off — that undo is backtracking.',
    },
    unique_paths: {
      array: '', target: '4',
      hint: 'Grid side 2–7. Optionally add walls as row:col pairs (e.g. 1:1, 2:0) and watch the count drop.',
    },
    flood_fill: {
      array: '', target: '5',
      hint: 'Grid side 2–8, starting at 0:0. Add walls as row:col pairs (e.g. 1:1, 2:1) and watch the paint stop at them.',
    },
    house_robber: {
      array: '2, 7, 9, 3, 1',
      hint: 'Up to 10 houses of loot (0+). The best row fills left to right; the robbed houses light up green at the end.',
    },
    lis: {
      array: '10, 9, 2, 5, 3, 7, 101, 18',
      hint: 'Up to 10 numbers. Each position scans everyone before it — watch it link to the run it extends.',
    },
    subset_sum: {
      array: '3, 4, 5', target: '9',
      hint: 'Up to 6 numbers (1–12) and a target sum (0–12). Each cell asks: reachable with these numbers?',
    },
    kmp_search: {
      array: 'ABABDABACDABABCABAB, ABABCABAB',
      hint: 'Text and pattern, comma-separated. Watch the failure table get built first — that is the real algorithm.',
    },
    z_function: {
      array: 'AABXAAB',
      hint: 'One word, up to 22 letters/digits. Z[i] is how much of the prefix restarts at i — the Z-box copies mirrors for free.',
    },
    rabin_karp: {
      array: 'ABRACADABRA, ABRA',
      hint: 'Text and pattern, comma-separated. Windows are screened by a rolling fingerprint; characters are read only on a hash hit.',
    },
    manacher: {
      array: 'FORGEEKSSKEEGFOR',
      hint: 'One word, up to 18 letters/digits. The longest palindrome grows around each centre, reusing earlier mirrors.',
    },
    segment_tree: {
      array: '3, 1, 4, 1, 5, 9, 2, 6', target: '',
      hint: 'Up to 8 values. Optionally set a query range as lo:hi in the range box — blank sums everything.',
    },
    fenwick_tree: {
      array: '3, 1, 4, 1, 5, 9, 2, 6', target: '4',
      hint: 'Up to 8 values. UP TO is the prefix end index — watch the low-bit trick pick which slots to read.',
    },
    sieve: {
      array: '', target: '30',
      hint: 'Upper limit 10–50. Crossing out starts at p², not 2p — the trace shows why that is safe.',
    },
    bst_insert: {
      array: '8, 3, 10, 1, 6, 14, 4',
      hint: 'Up to 12 values — try inserting sorted numbers and watch the tree degenerate into a chain.',
    },
    bst_search: {
      array: '8, 3, 10, 1, 6, 14, 4', target: '6',
      hint: 'The tree is built from your values, then searched — each comparison discards a whole subtree.',
    },
    heap_insert: {
      array: '3, 9, 5, 1, 12, 8',
      hint: 'Max-heap: every parent ≥ its children. Watch new values bubble up.',
    },
    knapsack_01: {
      array: '2:3, 3:4, 4:5, 5:6', target: '8',
      hint: 'weight:value pairs (up to 6 items) and a capacity (1–10). Every cell of the DP table, solved once.',
    },
    lcs: {
      array: 'ABCBDAB, BDCAB',
      hint: 'Two words (letters/digits, up to 8 chars each). The traceback at the end reveals the shared sequence.',
    },
    fibonacci_dp: {
      target: '10',
      hint: 'Pick n (0–18) — watch the memo vault fill; cache hits glow green.',
    },
    hash_table: {
      array: 'CAT, DOG, OWL, FOX | DOG',
      hint: 'Up to 8 keys, then | and a key to look up. Only 5 buckets, so collisions are the point.',
    },
    bst_delete: {
      array: '8, 3, 10, 1, 6, 14, 4, 7, 13', target: '3',
      hint: 'Delete a leaf (1), a node with one child (10), or one with two (3) — three different stories.',
    },
    heap_extract: {
      array: '3, 9, 2, 1, 7, 5',
      hint: 'Take the max, move the last leaf up, sift it down. Repeat and the output is sorted.',
    },
    merge_intervals: {
      array: '1-3, 2-6, 8-10, 15-18',
      hint: 'Up to 10 start-end pairs. Try them out of order — the sort is what makes one pass enough.',
    },
    coin_change: {
      array: '1, 3, 4', target: '6',
      hint: 'Coins then an amount (0–12). Try 1,3,4 for 6 — greedy says 3 coins, the table finds 2.',
    },
  };

  // Algorithms whose only input is a single number, whatever their view.
  const NUMBER_ONLY = { sieve: [10, 50, 'N ='], n_queens: [4, 6, 'BOARD ='] };

  function parseArrayInput() {
    const numOnly = NUMBER_ONLY[algoId];
    if (numOnly) {
      const [lo, hi] = numOnly;
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t) || t !== Math.floor(t)) {
        return { error: 'Enter a whole number.' };
      }
      if (t < lo || t > hi) return { error: `Keep it between ${lo} and ${hi}.` };
      return { target: t };
    }

    if (algoId === 'unique_paths') {
      const side = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(side) || side !== Math.floor(side) || side < 2 || side > 7) {
        return { error: 'Grid side must be a whole number 2–7.' };
      }
      const raw = (arrayInput?.value || '').replace(/\s+/g, '');
      if (!raw) return { target: side };
      if (!/^\d+:\d+(,\d+:\d+)*$/.test(raw)) {
        return { error: 'Walls are row:col pairs — e.g. 1:1, 2:0. Leave blank for an open grid.' };
      }
      const walls = raw.split(',').map(p => p.split(':').map(Number));
      if (walls.some(([r, c]) => r >= side || c >= side)) {
        return { error: `Wall coordinates must be within 0–${side - 1}.` };
      }
      if (walls.some(([r, c]) => r === 0 && c === 0)) {
        return { error: 'The start square cannot be a wall.' };
      }
      return { target: side, text: raw };
    }

    if (algoId === 'house_robber' || algoId === 'lis') {
      const parts = (arrayInput?.value || '').trim().split(/[\s,;]+/).filter(Boolean);
      if (!parts.length) return { error: 'Enter some numbers — e.g. 2, 7, 9, 3, 1' };
      const values = parts.map(Number);
      if (values.some(v => !Number.isInteger(v))) {
        return { error: 'Whole numbers only, separated by commas.' };
      }
      if (algoId === 'house_robber' && values.some(v => v < 0)) {
        return { error: 'House loot must be 0 or more.' };
      }
      if (values.length > 10) return { error: 'Max 10 numbers — the grid has to stay readable.' };
      return { array: values };
    }

    if (algoId === 'subset_sum') {
      const parts = (arrayInput?.value || '').trim().split(/[\s,;]+/).filter(Boolean);
      if (!parts.length) return { error: 'Enter some numbers — e.g. 3, 4, 5' };
      const values = parts.map(Number);
      if (values.some(v => !Number.isInteger(v) || v < 1 || v > 12)) {
        return { error: 'Numbers must be whole values 1–12.' };
      }
      if (values.length > 6) return { error: 'Max 6 numbers.' };
      const target = Number((targetInput?.value || '').trim());
      if (!Number.isInteger(target) || target < 0 || target > 12) {
        return { error: 'Target sum must be a whole number 0–12.' };
      }
      return { array: values, target };
    }

    if (algoId === 'flood_fill') {
      const side = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(side) || side !== Math.floor(side) || side < 2 || side > 8) {
        return { error: 'Grid side must be a whole number 2–8.' };
      }
      const raw = (arrayInput?.value || '').replace(/\s+/g, '');
      if (!raw) return { target: side };
      if (!/^\d+:\d+(,\d+:\d+)*$/.test(raw)) {
        return { error: 'Walls are row:col pairs — e.g. 1:1, 2:1. Leave blank for an open canvas.' };
      }
      const walls = raw.split(',').map(p => p.split(':').map(Number));
      if (walls.some(([r, c]) => r >= side || c >= side)) {
        return { error: `Wall coordinates must be within 0–${side - 1}.` };
      }
      if (walls.some(([r, c]) => r === 0 && c === 0)) {
        return { error: 'The start cell (0:0) cannot be a wall.' };
      }
      return { target: side, text: raw };
    }

    if (algoId === 'kmp_search') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '').toUpperCase();
      if (!/^[A-Z0-9]{1,24},[A-Z0-9]{1,12}$/.test(raw)) {
        return { error: 'Text then pattern, comma-separated — e.g. ABABCABAB, ABAB' };
      }
      const [hay, needle] = raw.split(',');
      if (needle.length > hay.length) {
        return { error: 'The pattern cannot be longer than the text.' };
      }
      return { text: raw, chars: hay.split('') };
    }

    if (algoId === 'rabin_karp') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '').toUpperCase();
      if (!/^[A-Z0-9]{1,24},[A-Z0-9]{1,12}$/.test(raw)) {
        return { error: 'Text then pattern, comma-separated — e.g. ABRACADABRA, ABRA' };
      }
      const [hay, needle] = raw.split(',');
      if (needle.length > hay.length) {
        return { error: 'The pattern cannot be longer than the text.' };
      }
      return { text: raw, chars: hay.split('') };
    }

    if (algoId === 'z_function' || algoId === 'manacher') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '').toUpperCase();
      const max = algoId === 'manacher' ? 18 : 22;
      if (!new RegExp(`^[A-Z0-9]{1,${max}}$`).test(raw)) {
        return { error: `One word of letters or digits, 1–${max} characters.` };
      }
      return { text: raw, chars: raw.split('') };
    }

    if (algoId === 'hash_table') {
      const raw = (arrayInput?.value || '').toUpperCase();
      const [head, look] = raw.split('|');
      const keys = head.split(',').map(k => k.trim()).filter(Boolean);
      const lookup = (look || '').trim();
      if (!keys.length) return { error: 'Type some keys — e.g. CAT, DOG, OWL' };
      if (keys.length > 8) return { error: 'Max 8 keys — the chains stop fitting.' };
      if (keys.concat(lookup ? [lookup] : []).some(k => !/^[A-Z0-9]{1,10}$/.test(k))) {
        return { error: 'Keys are 1–10 letters or digits.' };
      }
      return { text: keys.join(',') + (lookup ? ` | ${lookup}` : '') };
    }

    if (algoId === 'merge_intervals') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '');
      const parts = raw.split(',').filter(Boolean);
      if (!parts.length) return { error: 'Type intervals — e.g. 1-3, 2-6, 8-10' };
      if (parts.length > 10) return { error: 'Max 10 intervals.' };
      for (const p of parts) {
        if (!/^\d+-\d+$/.test(p)) {
          return { error: `Could not read "${p}" — use start-end pairs like 2-6.` };
        }
        const [a, b] = p.split('-').map(Number);
        if (a > b) return { error: `Interval "${p}" ends before it starts.` };
        if (b > 100) return { error: 'Keep interval bounds between 0 and 100.' };
      }
      return { text: parts.join(','), chars: parts };
    }

    if (algoId === 'coin_change') {
      const coins = (arrayInput?.value || '').split(',')
        .map(s => Number(s.trim())).filter(s => s !== '' && !Number.isNaN(s));
      if (!coins.length) return { error: 'Type coin values — e.g. 1, 3, 4' };
      if (coins.length > 4) return { error: 'Max 4 coin denominations.' };
      if (coins.some(c => !Number.isInteger(c) || c < 1)) {
        return { error: 'Coins must be whole numbers of 1 or more.' };
      }
      const amount = Number((targetInput?.value || '').trim());
      if (!Number.isInteger(amount)) return { error: 'Amount must be a whole number.' };
      if (amount < 0 || amount > 12) return { error: 'Keep the amount between 0 and 12.' };
      return { array: coins, target: amount };
    }

    if (algoId === 'trie_insert') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '').toUpperCase();
      const words = raw.split(',').filter(Boolean);
      if (!words.length) return { error: 'Type some words — e.g. CAT, CAR, DOG' };
      if (words.length > 5) return { error: 'Max 5 words.' };
      if (words.some(w => !/^[A-Z]{1,8}$/.test(w))) {
        return { error: 'Letters only, 1–8 characters per word.' };
      }
      return { text: words.join(','), words };
    }

    if (traceView === 'table') {
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t) || t !== Math.floor(t)) return { error: 'Enter a whole number n.' };
      if (t < 0 || t > 18) return { error: 'Keep n between 0 and 18.' };
      return { target: t };
    }
    if (traceView === 'stack') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '');
      if (!raw) return { error: 'Type a bracket sequence — e.g. ({[]})' };
      if (raw.length > 20) return { error: 'Max 20 characters.' };
      if (!/^[()\[\]{}]+$/.test(raw)) return { error: 'Only brackets: ( ) [ ] { }' };
      return { text: raw };
    }
    if (traceView === 'grid') {
      const raw = (arrayInput?.value || '').replace(/\s+/g, '');
      if (algoId === 'knapsack_01') {
        if (!/^\d+:\d+(,\d+:\d+)*$/.test(raw)) {
          return { error: 'Items as weight:value pairs — e.g. 2:3, 3:4, 4:5' };
        }
        const items = raw.split(',').map(p => p.split(':').map(Number));
        if (items.length > 6) return { error: 'Max 6 items.' };
        if (items.some(([w, v]) => w < 1 || w > 20 || v < 1 || v > 20)) {
          return { error: 'Weights and values must be 1–20.' };
        }
        const cap = Number((targetInput?.value || '').trim());
        if (!Number.isFinite(cap) || cap !== Math.floor(cap) || cap < 1 || cap > 10) {
          return { error: 'Capacity must be a whole number 1–10.' };
        }
        return { text: raw, target: cap, items };
      }
      // lcs and edit_distance — both take two comma-separated words
      const up = raw.toUpperCase();
      if (!/^[A-Z0-9]{1,8},[A-Z0-9]{1,8}$/.test(up)) {
        return { error: 'Two words (letters/digits, 1–8 chars each), comma-separated.' };
      }
      const [a, b] = up.split(',');
      return { text: up, a, b };
    }
    const raw = (arrayInput?.value || '').trim();
    const parts = raw.split(/[\s,;]+/).filter(Boolean);
    if (!parts.length) return { error: 'Enter some numbers first — e.g. 7, 3, 9, 1' };
    const values = parts.map(Number);
    if (values.some(v => !Number.isFinite(v))) return { error: 'Only numbers, separated by commas.' };
    if (values.some(v => Math.abs(v) > 1_000_000)) return { error: 'Keep values within ±1,000,000.' };
    const maxLen = (algoId === 'linked_list_reverse' || algoId === 'floyd_cycle') ? 10
      : traceView === 'tree' ? 12
      : algoId === 'binary_search' ? 20 : 16;
    if (values.length > maxLen) return { error: `Max ${maxLen} values for this algorithm.` };

    if (algoId === 'segment_tree') {
      const raw = (targetInput?.value || '').trim();
      if (!raw) return { array: values };
      if (!/^\d+:\d+$/.test(raw)) {
        return { error: 'Query range is lo:hi — e.g. 2:5. Leave blank to sum everything.' };
      }
      const [lo, hi] = raw.split(':').map(Number);
      if (lo > hi || hi >= values.length) {
        return { error: `Range must satisfy 0 ≤ lo ≤ hi ≤ ${values.length - 1}.` };
      }
      return { array: values, text: raw };
    }

    if (algoId === 'fenwick_tree') {
      const raw = (targetInput?.value || '').trim();
      const t = raw === '' ? values.length - 1 : Number(raw);
      if (!Number.isFinite(t) || t !== Math.floor(t) || t < 0 || t >= values.length) {
        return { error: `Prefix end index must be 0–${values.length - 1}.` };
      }
      return { array: values, target: t };
    }

    if (algoId === 'counting_sort') {
      if (values.some(v => v !== Math.floor(v) || v < 0 || v > 20)) {
        return { error: 'Counting sort needs whole numbers 0–20 — one bucket per value.' };
      }
      return { array: values };
    }

    if (algoId === 'bst_delete') {
      const raw = (targetInput?.value || '').trim();
      if (raw === '') return { error: 'Which value should be deleted?' };
      const t = Number(raw);
      if (!Number.isFinite(t)) return { error: 'The value to delete must be a number.' };
      return { array: values, target: t };
    }

    if (algoId === 'floyd_cycle') {
      const raw = (targetInput?.value || '').trim();
      // Blank means a normal terminated list; otherwise it is the index the
      // tail loops back to.
      const t = raw === '' ? -1 : Number(raw);
      if (!Number.isFinite(t) || t !== Math.floor(t) || t < -1 || t >= values.length) {
        return { error: `Link-back index must be -1 (no cycle) or 0–${values.length - 1}.` };
      }
      return { array: values, target: t };
    }

    if (algoId === 'bst_search') {
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t)) return { error: 'Enter a numeric target to search for.' };
      return { array: values, target: t };
    }

    if (algoId === 'two_sum_sorted') {
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t)) return { error: 'Enter a numeric target sum.' };
      const sorted = values.slice().sort((a, b) => a - b);
      const sortedForYou = sorted.some((v, i) => v !== values[i]);
      return { array: sorted, target: t, sortedForYou };
    }

    if (algoId === 'sliding_window') {
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t) || t !== Math.floor(t)) return { error: 'Window size k must be a whole number.' };
      if (t < 1 || t > values.length) return { error: `Keep k between 1 and ${values.length}.` };
      return { array: values, target: t };
    }

    if (algoId === 'binary_search') {
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t)) return { error: 'Enter a numeric target to search for.' };
      const sorted = values.slice().sort((a, b) => a - b);
      const sortedForYou = sorted.some((v, i) => v !== values[i]);
      return { array: sorted, target: t, sortedForYou };
    }
    return { array: values };
  }

  // ── Table view (memoized DP) ──
  let currentTableN = 10;

  function renderTableView(n) {
    svg.innerHTML = '';
    currentTableN = n;
    const scene = SCENES[currentMeta?.scene] || SCENES.vault;
    currentScene = scene;

    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);

    const cells = n + 1;
    const w = Math.min(56, 700 / cells);
    const x0 = (760 - w * cells) / 2;
    const y = 110, h = 52;

    for (let idx = 0; idx <= n; idx++) {
      const rect = makeSVG("rect");
      rect.setAttribute("x", x0 + idx * w + 2);
      rect.setAttribute("y", y);
      rect.setAttribute("width", Math.max(w - 4, 6));
      rect.setAttribute("height", h);
      rect.setAttribute("id", `cell-${idx}`);
      rect.setAttribute("fill", "rgba(212, 96, 44,0.03)");
      rect.setAttribute("stroke", "var(--cDim)");
      rect.setAttribute("stroke-width", "1");
      svg.appendChild(rect);

      const val = makeSVG("text");
      val.setAttribute("x", x0 + idx * w + w / 2);
      val.setAttribute("y", y + h / 2 + 5);
      val.setAttribute("text-anchor", "middle");
      val.setAttribute("fill", "var(--cBright)");
      val.setAttribute("font-family", "var(--font-mono)");
      val.setAttribute("font-size", w < 34 ? "10" : "13");
      val.setAttribute("id", `cellval-${idx}`);
      svg.appendChild(val);

      const pos = makeSVG("text");
      pos.setAttribute("x", x0 + idx * w + w / 2);
      pos.setAttribute("y", y + h + 16);
      pos.setAttribute("text-anchor", "middle");
      pos.setAttribute("fill", "var(--cDim)");
      pos.setAttribute("font-family", "var(--font-ui)");
      pos.setAttribute("font-size", "6");
      pos.textContent = `f(${idx})`;
      svg.appendChild(pos);
    }
  }

  function renderTableStep(step) {
    const s = step.structures || {};
    const table = s.table || {};
    for (let idx = 0; idx <= currentTableN; idx++) {
      const cell = svg.querySelector(`#cell-${idx}`);
      const val = svg.querySelector(`#cellval-${idx}`);
      if (!cell || !val) continue;
      const v = table[String(idx)];
      const filled = v !== null && v !== undefined;
      val.textContent = filled ? fmt(v) : '';
      cell.setAttribute("fill", filled ? "rgba(212, 96, 44,0.10)" : "rgba(212, 96, 44,0.03)");
      cell.setAttribute("stroke", filled ? "var(--c)" : "var(--cDim)");
      cell.setAttribute("stroke-width", "1");
      if (idx === s.computing) {
        cell.setAttribute("fill", s.cache_hit ? "rgba(74,222,128,0.18)" : "rgba(212, 96, 44,0.18)");
        cell.setAttribute("stroke", s.cache_hit ? "#4ade80" : "var(--c)");
        cell.setAttribute("stroke-width", "2");
      }
    }
  }

  // ── List view (linked list) ──
  let currentListValues = [];
  let listGeom = null;

  function renderListView(values) {
    svg.innerHTML = '';
    currentListValues = values.slice();
    const scene = SCENES[currentMeta?.scene] || SCENES.train;
    currentScene = scene;

    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);

    const n = values.length;
    if (!n) return;
    const w = Math.min(72, 680 / n);
    const x0 = (760 - w * n) / 2;
    const y = 120, h = 46;
    listGeom = { x0, w, y, h };

    values.forEach((v, idx) => {
      const rect = makeSVG("rect");
      rect.setAttribute("x", x0 + idx * w + 6);
      rect.setAttribute("y", y);
      rect.setAttribute("width", w - 12);
      rect.setAttribute("height", h);
      rect.setAttribute("id", `cell-${idx}`);
      rect.setAttribute("fill", "rgba(212, 96, 44,0.05)");
      rect.setAttribute("stroke", "var(--cDim)");
      svg.appendChild(rect);

      const val = makeSVG("text");
      val.setAttribute("x", x0 + idx * w + w / 2);
      val.setAttribute("y", y + h / 2 + 5);
      val.setAttribute("text-anchor", "middle");
      val.setAttribute("fill", "var(--cBright)");
      val.setAttribute("font-family", "var(--font-mono)");
      val.setAttribute("font-size", "13");
      val.textContent = fmtCell(v);
      svg.appendChild(val);

      const pos = makeSVG("text");
      pos.setAttribute("x", x0 + idx * w + w / 2);
      pos.setAttribute("y", y + h + 16);
      pos.setAttribute("text-anchor", "middle");
      pos.setAttribute("fill", "var(--cDim)");
      pos.setAttribute("font-family", "var(--font-ui)");
      pos.setAttribute("font-size", "6");
      pos.textContent = idx;
      svg.appendChild(pos);
    });
  }

  function renderListStep(step) {
    if (!listGeom) return;
    const s = step.structures || {};
    const { x0, w, y, h } = listGeom;
    svg.querySelector('#list-decor')?.remove();
    const g = makeSVG('g');
    g.setAttribute('id', 'list-decor');

    const cx = (idx) => x0 + idx * w + w / 2;

    // Arrows: rightward above the boxes, leftward below — they can't overlap
    (s.next || []).forEach((to, from) => {
      if (to === null || to === undefined) {
        // end of chain marker
        const t = makeSVG('text');
        t.setAttribute('x', cx(from));
        t.setAttribute('y', y - 12);
        t.setAttribute('text-anchor', 'middle');
        t.setAttribute('fill', 'var(--cDim)');
        t.setAttribute('font-size', '11');
        t.textContent = '∅';
        g.appendChild(t);
        return;
      }
      const right = to > from;
      const yy = right ? y - 14 : y + h + 28;
      const x1 = cx(from), x2 = cx(to) + (right ? -8 : 8);
      const line = makeSVG('line');
      line.setAttribute('x1', x1); line.setAttribute('y1', yy);
      line.setAttribute('x2', x2); line.setAttribute('y2', yy);
      const active = from === s.curr;
      line.setAttribute('stroke', active ? 'var(--c)' : 'var(--c)');
      line.setAttribute('stroke-width', active ? '2.5' : '1.5');
      g.appendChild(line);
      const head = makeSVG('polygon');
      const dir = right ? 1 : -1;
      head.setAttribute('points',
        `${x2 + dir * 8},${yy} ${x2},${yy - 4} ${x2},${yy + 4}`);
      head.setAttribute('fill', active ? 'var(--c)' : 'var(--c)');
      g.appendChild(head);
    });

    // Pointer labels under the index row. A step may name its own pointers
    // (Floyd's slow/fast); otherwise fall back to the prev/curr/next trio.
    const palette = ['var(--c)', 'var(--cBright)', 'var(--cDim)'];
    const ptrs = Array.isArray(s.pointers) && s.pointers.length
      ? s.pointers.map(([label, idx], n) => [label, idx, palette[n % palette.length]])
      : [['P', s.prev, 'var(--cBright)'], ['C', s.curr, 'var(--c)'],
         ['S', s.saved, 'var(--cDim)']];
    const seenAt = {};
    ptrs.forEach(([label, idx, color]) => {
      if (idx === null || idx === undefined) return;
      // Two pointers can share a node (that's the whole point of Floyd's
      // collision) — fan them out so neither label hides the other.
      const nth = seenAt[idx] = (seenAt[idx] ?? -1) + 1;
      const t = makeSVG('text');
      t.setAttribute('x', cx(idx) + nth * 11);
      t.setAttribute('y', y + h + 46);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', color);
      t.setAttribute('font-family', 'var(--font-ui)');
      t.setAttribute('font-size', '8');
      t.textContent = label;
      g.appendChild(t);
    });

    // Highlight the current node's box
    currentListValues.forEach((_, idx) => {
      const cell = svg.querySelector(`#cell-${idx}`);
      if (!cell) return;
      cell.setAttribute('stroke', idx === s.curr ? 'var(--c)' : 'var(--cDim)');
      cell.setAttribute('stroke-width', idx === s.curr ? '2' : '1');
    });

    svg.appendChild(g);
  }

  // ── Stack view (balanced brackets) ──
  let currentStackText = '';
  let stackGeom = null;

  function renderStackView(text) {
    svg.innerHTML = '';
    currentStackText = text;
    const scene = SCENES[currentMeta?.scene] || SCENES.plates;
    currentScene = scene;

    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);

    const n = text.length;
    if (!n) return;
    const w = Math.min(40, 640 / n);
    const x0 = (760 - w * n) / 2;
    const y = 55, h = 34;
    stackGeom = { x0, w, y, h };

    const rowLabel = makeSVG('text');
    rowLabel.setAttribute('x', '380'); rowLabel.setAttribute('y', '44');
    rowLabel.setAttribute('text-anchor', 'middle');
    rowLabel.setAttribute('fill', 'var(--cDim)');
    rowLabel.setAttribute('font-family', 'var(--font-ui)');
    rowLabel.setAttribute('font-size', '6');
    rowLabel.textContent = 'INPUT — LEFT TO RIGHT';
    svg.appendChild(rowLabel);

    [...text].forEach((ch, idx) => {
      const rect = makeSVG('rect');
      rect.setAttribute('x', x0 + idx * w + 2);
      rect.setAttribute('y', y);
      rect.setAttribute('width', w - 4);
      rect.setAttribute('height', h);
      rect.setAttribute('id', `schar-${idx}`);
      rect.setAttribute('fill', 'rgba(212, 96, 44,0.05)');
      rect.setAttribute('stroke', 'var(--cDim)');
      svg.appendChild(rect);
      const t = makeSVG('text');
      t.setAttribute('x', x0 + idx * w + w / 2);
      t.setAttribute('y', y + h / 2 + 5);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', 'var(--cBright)');
      t.setAttribute('font-family', 'var(--font-mono)');
      t.setAttribute('font-size', '15');
      t.textContent = ch;
      svg.appendChild(t);
    });

    const stackLabel = makeSVG('text');
    stackLabel.setAttribute('x', '80'); stackLabel.setAttribute('y', '205');
    stackLabel.setAttribute('fill', 'var(--cDim)');
    stackLabel.setAttribute('font-family', 'var(--font-ui)');
    stackLabel.setAttribute('font-size', '6');
    stackLabel.textContent = 'STACK: BOTTOM → TOP';
    svg.appendChild(stackLabel);
  }

  function renderStackStep(step) {
    if (!stackGeom) return;
    const s = step.structures || {};
    svg.querySelector('#stack-decor')?.remove();
    const g = makeSVG('g');
    g.setAttribute('id', 'stack-decor');

    // Highlight the current input character; mismatches turn red
    [...currentStackText].forEach((_, idx) => {
      const cell = svg.querySelector(`#schar-${idx}`);
      if (!cell) return;
      if (idx === s.pos) {
        cell.setAttribute('stroke', s.action === 'mismatch' ? '#f87171' : 'var(--c)');
        cell.setAttribute('stroke-width', '2');
        cell.setAttribute('fill', s.action === 'mismatch'
          ? 'rgba(248,113,113,0.15)' : 'rgba(212, 96, 44,0.15)');
      } else if (s.pos !== null && s.pos !== undefined && idx < s.pos) {
        cell.setAttribute('stroke', 'var(--c)');
        cell.setAttribute('stroke-width', '1');
        cell.setAttribute('fill', 'rgba(212, 96, 44,0.03)');
      } else {
        cell.setAttribute('stroke', 'var(--cDim)');
        cell.setAttribute('stroke-width', '1');
        cell.setAttribute('fill', 'rgba(212, 96, 44,0.05)');
      }
    });

    // Draw the stack growing left → right along the bottom
    const bx = 80, by = 215, bw = 38, bh = 36;
    (s.stack || []).forEach((ch, k) => {
      const rect = makeSVG('rect');
      rect.setAttribute('x', bx + k * (bw + 4));
      rect.setAttribute('y', by);
      rect.setAttribute('width', bw);
      rect.setAttribute('height', bh);
      const isTop = k === s.stack.length - 1;
      rect.setAttribute('fill', isTop ? 'rgba(212, 96, 44,0.12)' : 'rgba(212, 96, 44,0.06)');
      rect.setAttribute('stroke', isTop ? 'var(--c)' : 'var(--c)');
      rect.setAttribute('stroke-width', isTop ? '2' : '1');
      g.appendChild(rect);
      const t = makeSVG('text');
      t.setAttribute('x', bx + k * (bw + 4) + bw / 2);
      t.setAttribute('y', by + bh / 2 + 5);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', 'var(--cBright)');
      t.setAttribute('font-family', 'var(--font-mono)');
      t.setAttribute('font-size', '15');
      t.textContent = ch;
      g.appendChild(t);
    });
    if (!(s.stack || []).length) {
      const t = makeSVG('text');
      t.setAttribute('x', bx); t.setAttribute('y', by + 24);
      t.setAttribute('fill', 'var(--cDim)');
      t.setAttribute('font-family', 'var(--font-mono)');
      t.setAttribute('font-size', '12');
      t.textContent = '(empty)';
      g.appendChild(t);
    }

    // Verdict badge once decided
    if (s.balanced === true || s.balanced === false) {
      const t = makeSVG('text');
      t.setAttribute('x', '680'); t.setAttribute('y', '235');
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', s.balanced ? '#4ade80' : '#f87171');
      t.setAttribute('font-family', 'var(--font-ui)');
      t.setAttribute('font-size', '9');
      t.textContent = s.balanced ? 'BALANCED' : 'UNBALANCED';
      g.appendChild(t);
    }

    svg.appendChild(g);
  }

  // ── Tree view (BST / heap) ──
  function renderTreeView() {
    svg.innerHTML = '';
    const scene = SCENES[currentMeta?.scene] || SCENES.files;
    currentScene = scene;

    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);

    const hint = makeSVG("text");
    hint.setAttribute("x", "380"); hint.setAttribute("y", "145");
    hint.setAttribute("text-anchor", "middle");
    hint.setAttribute("fill", "var(--cDim)");
    hint.setAttribute("font-family", "var(--font-ui)");
    hint.setAttribute("font-size", "8");
    hint.setAttribute("id", "tree-hint");
    hint.textContent = "PRESS RUN TO GROW THE TREE";
    svg.appendChild(hint);
  }

  function renderTreeStep(step) {
    const s = step.structures || {};
    svg.querySelector('#tree-hint')?.remove();
    svg.querySelector('#tree-decor')?.remove();
    const g = makeSVG('g');
    g.setAttribute('id', 'tree-decor');

    const nodes = s.tree || [];
    if (!nodes.length) { svg.appendChild(g); return; }
    const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
    const maxDepth = Math.max(...nodes.map(n => n.depth), 1);
    const dy = Math.min(52, 210 / maxDepth);
    const px = (n) => 60 + n.x * 640;
    const py = (n) => 45 + n.depth * dy;

    // Edges first so they sit behind the nodes
    nodes.forEach(n => {
      [n.left, n.right].forEach(cid => {
        const c = byId[cid];
        if (c === undefined) return;
        const line = makeSVG('line');
        line.setAttribute('x1', px(n)); line.setAttribute('y1', py(n));
        line.setAttribute('x2', px(c)); line.setAttribute('y2', py(c));
        line.setAttribute('stroke', 'rgba(0,150,184,0.35)');
        line.setAttribute('stroke-width', '1.5');
        g.appendChild(line);
      });
    });

    nodes.forEach(n => {
      const isCurrent = n.id === s.current;
      const circle = makeSVG('circle');
      circle.dataset.nodeId = n.id;
      circle.setAttribute('cx', px(n)); circle.setAttribute('cy', py(n));
      circle.setAttribute('r', '15');
      circle.setAttribute('fill', isCurrent
        ? (s.found === true ? 'rgba(74,222,128,0.25)' : 'rgba(212, 96, 44,0.2)')
        : 'var(--cDeep)');
      circle.setAttribute('stroke', isCurrent
        ? (s.found === true ? '#4ade80' : 'var(--c)')
        : 'var(--cDim)');
      circle.setAttribute('stroke-width', isCurrent ? '2' : '1');
      g.appendChild(circle);

      const t = makeSVG('text');
      t.setAttribute('x', px(n)); t.setAttribute('y', py(n) + 4);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', 'var(--cBright)');
      t.setAttribute('font-family', 'var(--font-mono)');
      t.setAttribute('font-size', '11');
      t.textContent = fmtCell(n.value);
      g.appendChild(t);
    });

    if (s.inserting !== null && s.inserting !== undefined) {
      const t = makeSVG('text');
      t.setAttribute('x', '10'); t.setAttribute('y', '270');
      t.setAttribute('fill', 'var(--c)');
      t.setAttribute('font-family', 'var(--font-ui)');
      t.setAttribute('font-size', '8');
      t.textContent = `INSERTING ${fmt(s.inserting)}`;
      g.appendChild(t);
    }
    if (s.found === true || s.found === false) {
      const t = makeSVG('text');
      t.setAttribute('x', '700'); t.setAttribute('y', '270');
      t.setAttribute('text-anchor', 'end');
      t.setAttribute('fill', s.found ? '#4ade80' : '#f87171');
      t.setAttribute('font-family', 'var(--font-ui)');
      t.setAttribute('font-size', '9');
      t.textContent = s.found ? 'FOUND' : 'NOT FOUND';
      g.appendChild(t);
    }

    svg.appendChild(g);
  }

  // ── Grid view (2-D DP tables: knapsack, LCS) ──
  function renderGridView() {
    svg.innerHTML = '';
    const scene = SCENES[currentMeta?.scene] || SCENES.vault;
    currentScene = scene;

    const sceneLabel = makeSVG("text");
    sceneLabel.setAttribute("x", "10"); sceneLabel.setAttribute("y", "20");
    sceneLabel.setAttribute("fill", "var(--cDim)");
    sceneLabel.setAttribute("font-family", "var(--font-ui)");
    sceneLabel.setAttribute("font-size", "8");
    sceneLabel.textContent = scene.label;
    svg.appendChild(sceneLabel);

    const hint = makeSVG("text");
    hint.setAttribute("x", "380"); hint.setAttribute("y", "145");
    hint.setAttribute("text-anchor", "middle");
    hint.setAttribute("fill", "var(--cDim)");
    hint.setAttribute("font-family", "var(--font-ui)");
    hint.setAttribute("font-size", "8");
    hint.setAttribute("id", "grid-hint");
    hint.textContent = "PRESS RUN TO FILL THE TABLE";
    svg.appendChild(hint);
  }

  function renderGridStep(step) {
    const s = step.structures || {};
    svg.querySelector('#grid-hint')?.remove();
    svg.querySelector('#grid-decor')?.remove();
    const g = makeSVG('g');
    g.setAttribute('id', 'grid-decor');

    const grid = s.grid || [];
    if (!grid.length) { svg.appendChild(g); return; }
    const rowLabels = currentTraceMeta?.row_labels || grid.map((_, i) => String(i));
    const colLabels = currentTraceMeta?.col_labels || (grid[0] || []).map((_, i) => String(i));
    const rows = grid.length, cols = (grid[0] || []).length;
    const cw = Math.min(64, 690 / (cols + 1));
    const ch = Math.min(34, 235 / (rows + 1));
    const x0 = (760 - cw * (cols + 1)) / 2;
    const y0 = 32;
    const pathSet = new Set((s.path || []).map(([r, c]) => `${r}|${c}`));
    const depSet = new Set((s.deps || []).map(([r, c]) => `${r}|${c}`));

    const text = (x, y, str, fill, size, family = 'var(--font-mono)') => {
      const t = makeSVG('text');
      t.setAttribute('x', x); t.setAttribute('y', y);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', fill);
      t.setAttribute('font-family', family);
      t.setAttribute('font-size', size);
      t.textContent = str;
      g.appendChild(t);
    };

    // Headers
    colLabels.forEach((lab, c) => {
      text(x0 + cw * (c + 1) + cw / 2, y0 + ch / 2 + 3, lab, 'var(--cDim)', '9');
    });
    rowLabels.forEach((lab, r) => {
      text(x0 + cw / 2, y0 + ch * (r + 1) + ch / 2 + 3,
        String(lab).slice(0, 8), 'var(--cDim)', '8');
    });

    // Cells
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const v = grid[r][c];
        const filled = v !== null && v !== undefined;
        const isCurrent = r === s.row && c === s.col;
        const isDep = depSet.has(`${r}|${c}`);
        const onPath = pathSet.has(`${r}|${c}`);
        const rect = makeSVG('rect');
        rect.setAttribute('x', x0 + cw * (c + 1) + 1);
        rect.setAttribute('y', y0 + ch * (r + 1) + 1);
        rect.setAttribute('width', cw - 2);
        rect.setAttribute('height', ch - 2);
        rect.setAttribute('fill', onPath ? 'rgba(74,222,128,0.22)'
          : isCurrent ? (s.match ? 'rgba(74,222,128,0.18)' : 'rgba(212, 96, 44,0.18)')
          : isDep ? 'rgba(212, 96, 44,0.14)'
          : filled ? 'rgba(212, 96, 44,0.05)' : 'rgba(0,0,0,0.15)');
        rect.setAttribute('stroke', onPath ? '#4ade80'
          : isCurrent ? (s.match ? '#4ade80' : 'var(--c)')
          : isDep ? 'var(--c)' : 'var(--cDim)');
        rect.setAttribute('stroke-width', isCurrent || onPath ? '2' : '0.75');
        g.appendChild(rect);
        if (filled) {
          text(x0 + cw * (c + 1) + cw / 2, y0 + ch * (r + 1) + ch / 2 + 3.5,
            fmtCell(v), 'var(--cBright)', ch < 26 ? '9' : '11');
        }
      }
    }

    svg.appendChild(g);
  }

  // Offline emulator for the array algorithms — mirrors the backend step shapes.
  function localArrayTrace(parsed) {
    if (algoId === 'fibonacci_dp') {
      const n = parsed.target;
      const memo = {}, stack = [], steps = [];
      const counts = { calls: 0, cache_hits: 0, computes: 0 };
      const add = (note2, computing = null, cacheHit = false) => steps.push({
        i: steps.length,
        structures: {
          table: Object.fromEntries(
            Array.from({ length: n + 1 }, (_, k) => [String(k), memo[k] ?? null])),
          computing, cache_hit: cacheHit, stack: [...stack], counts: { ...counts },
        },
        highlight: { index: computing },
        note: note2,
      });
      add(`Compute fib(${n}) — the vault starts empty.`);
      const fib = (k) => {
        counts.calls++;
        if (memo[k] !== undefined) {
          counts.cache_hits++;
          add(`fib(${k}) is already in the vault: ${memo[k]}. No recomputation needed.`, k, true);
          return memo[k];
        }
        stack.push(k);
        if (k <= 1) {
          memo[k] = k; counts.computes++;
          add(`Base case: fib(${k}) = ${k}. Stored in the vault.`, k);
          stack.pop();
          return k;
        }
        add(`fib(${k}) unknown — need fib(${k - 1}) and fib(${k - 2}) first.`, k);
        const v = fib(k - 1) + fib(k - 2);
        memo[k] = v; counts.computes++;
        stack.pop();
        add(`fib(${k}) = ${v}. Stored in the vault.`, k);
        return v;
      };
      const result = fib(n);
      add(`Vault complete — fib(${n}) = ${result}.`);
      return { steps };
    }

    if (traceView === 'tree') {
      const values = parsed.array.slice();
      const steps = [];

      const bstSerialize = (nodes, root) => {
        const order = [];
        const inorder = (nid, depth) => {
          if (nid === null || nid === undefined) return;
          inorder(nodes[nid].left, depth + 1);
          order.push([nid, depth]);
          inorder(nodes[nid].right, depth + 1);
        };
        inorder(root, 0);
        const total = Math.max(order.length, 1);
        return order.map(([nid, depth], rank) => ({
          id: nid, value: nodes[nid].value,
          left: nodes[nid].left, right: nodes[nid].right,
          x: (rank + 0.5) / total, depth,
        }));
      };
      const heapSerialize = (heap) => heap.map((v, i) => {
        const depth = 31 - Math.clz32(i + 1);
        const pos = i - (2 ** depth - 1);
        return {
          id: i, value: v,
          left: 2 * i + 1 < heap.length ? 2 * i + 1 : null,
          right: 2 * i + 2 < heap.length ? 2 * i + 2 : null,
          x: (pos + 0.5) / (2 ** depth), depth,
        };
      });

      if (algoId === 'heap_insert') {
        const heap = [];
        const counts = { insertions: 0, comparisons: 0, swaps: 0 };
        const add = (note2, current = null) => steps.push({
          i: steps.length,
          structures: { tree: heapSerialize(heap), current, inserting: null,
            found: null, counts: { ...counts } },
          highlight: { node: current }, note: note2,
        });
        if (!values.length) { add('No values — an empty heap.'); return { steps }; }
        add(`Build a max-heap from ${values.length} values.`);
        for (const v of values) {
          heap.push(v); counts.insertions++;
          let i = heap.length - 1;
          add(`Insert ${fmt(v)} at the next free slot (index ${i}).`, i);
          while (i > 0) {
            const p = Math.floor((i - 1) / 2);
            counts.comparisons++;
            if (heap[i] > heap[p]) {
              [heap[i], heap[p]] = [heap[p], heap[i]];
              counts.swaps++;
              add(`${fmt(heap[p])} is bigger than its parent — swap up.`, p);
              i = p;
            } else {
              add(`${fmt(heap[i])} <= parent ${fmt(heap[p])} — heap property holds.`, i);
              break;
            }
          }
        }
        add(`Max-heap complete — ${fmt(heap[0])} sits at the root.`);
        return { steps };
      }

      // BST build (insert traces steps; search builds silently then traces)
      const nodes = {};
      let root = null;
      const bstAttach = (v) => {
        if (root === null) { nodes[0] = { value: v, left: null, right: null }; root = 0; return [0, 0]; }
        let cur = root, comps = 0;
        for (;;) {
          comps++;
          const n = nodes[cur];
          const side = v < n.value ? 'left' : 'right';
          if (n[side] === null) {
            const nid = Object.keys(nodes).length;
            nodes[nid] = { value: v, left: null, right: null };
            n[side] = nid;
            return [nid, comps];
          }
          cur = n[side];
        }
      };

      if (algoId === 'bst_insert') {
        const counts = { comparisons: 0, insertions: 0 };
        const add = (note2, current = null, inserting = null) => steps.push({
          i: steps.length,
          structures: { tree: bstSerialize(nodes, root), current, inserting,
            found: null, counts: { ...counts } },
          highlight: { node: current }, note: note2,
        });
        if (!values.length) { add('No values — an empty tree.'); return { steps }; }
        add(`Insert ${values.length} values: smaller left, bigger right.`);
        for (const v of values) {
          const [nid, comps] = bstAttach(v);
          counts.comparisons += comps;
          counts.insertions++;
          add(nid === 0 && Object.keys(nodes).length === 1
            ? `${fmt(v)} is the first value — it becomes the root.`
            : `${fmt(v)} attached after ${comps} comparison(s).`, nid);
        }
        add('Tree built — an in-order walk reads sorted.');
        return { steps };
      }

      // bst_search
      values.forEach(bstAttach);
      const target = parsed.target;
      const counts = { comparisons: 0 };
      const add = (note2, current = null, found = null) => steps.push({
        i: steps.length,
        structures: { tree: bstSerialize(nodes, root), current, inserting: null,
          found, counts: { ...counts } },
        highlight: { node: current }, note: note2,
      });
      if (root === null) { add('The tree is empty — nothing to search.', null, false); return { steps }; }
      add(`BST built. Search for ${fmt(target)}.`, root);
      let cur = root;
      while (cur !== null) {
        counts.comparisons++;
        const n = nodes[cur];
        if (target === n.value) { add(`${fmt(target)} found!`, cur, true); return { steps }; }
        const nxt = target < n.value ? n.left : n.right;
        add(`${fmt(target)} ${target < n.value ? '<' : '>'} ${fmt(n.value)} — go ${target < n.value ? 'left' : 'right'}.`,
          nxt === null ? cur : nxt);
        cur = nxt;
      }
      add(`Reached an empty branch — ${fmt(target)} is not in the tree.`, null, false);
      return { steps };
    }

    if (algoId === 'knapsack_01') {
      const items = parsed.items, W = parsed.target;
      const n = items.length;
      const grid = Array.from({ length: n + 1 }, () => Array(W + 1).fill(null));
      const steps = [];
      const counts = { cells: 0, takes: 0, skips: 0 };
      const add = (note2, row = null, col = null, deps = [], choice = null) =>
        steps.push({
          i: steps.length,
          structures: { grid: grid.map(r => r.slice()), row, col, deps,
            choice, path: [], counts: { ...counts } },
          highlight: { index: col }, note: note2,
        });
      const meta = {
        row_labels: ['no items', ...items.map(([w, v]) => `w${w}·v${v}`)],
        col_labels: Array.from({ length: W + 1 }, (_, c) => String(c)),
      };
      add(`Pack a capacity-${W} bag from ${n} items.`);
      for (let c = 0; c <= W; c++) grid[0][c] = 0;
      add('Row 0: with no items, every capacity holds value 0.', 0);
      for (let i = 1; i <= n; i++) {
        const [w, v] = items[i - 1];
        for (let c = 0; c <= W; c++) {
          counts.cells++;
          if (w > c) {
            grid[i][c] = grid[i - 1][c];
            counts.skips++;
            add(`Item ${i} (weight ${w}) doesn't fit in ${c} — copy from above.`,
              i, c, [[i - 1, c]], 'skip');
          } else {
            const skipV = grid[i - 1][c];
            const takeV = grid[i - 1][c - w] + v;
            grid[i][c] = Math.max(skipV, takeV);
            if (takeV > skipV) counts.takes++; else counts.skips++;
            add(`Capacity ${c}: ${takeV > skipV ? 'take' : 'skip'} item ${i} — ` +
              `max(${skipV}, ${takeV}) = ${grid[i][c]}.`,
              i, c, [[i - 1, c], [i - 1, c - w]], takeV > skipV ? 'take' : 'skip');
          }
        }
      }
      add(`Table complete — best value ${grid[n][W]} for capacity ${W}.`, n, W);
      return { steps, meta };
    }

    if (algoId === 'lcs') {
      const a = parsed.a, b = parsed.b;
      const n = a.length, m = b.length;
      const grid = Array.from({ length: n + 1 }, () => Array(m + 1).fill(null));
      const steps = [];
      const counts = { cells: 0, matches: 0 };
      const path = [];
      const add = (note2, row = null, col = null, deps = [], match = null) =>
        steps.push({
          i: steps.length,
          structures: { grid: grid.map(r => r.slice()), row, col, deps, match,
            path: path.map(p => p.slice()), counts: { ...counts } },
          highlight: { index: col }, note: note2,
        });
      const meta = { row_labels: ['∅', ...a], col_labels: ['∅', ...b] };
      add(`Find the longest subsequence common to '${a}' and '${b}'.`);
      for (let c = 0; c <= m; c++) grid[0][c] = 0;
      for (let r = 0; r <= n; r++) grid[r][0] = 0;
      add('Row 0 and column 0: against an empty string, the LCS is empty.', 0);
      for (let i = 1; i <= n; i++) {
        for (let j = 1; j <= m; j++) {
          counts.cells++;
          if (a[i - 1] === b[j - 1]) {
            grid[i][j] = grid[i - 1][j - 1] + 1;
            counts.matches++;
            add(`'${a[i - 1]}' matches — diagonal + 1 = ${grid[i][j]}.`,
              i, j, [[i - 1, j - 1]], true);
          } else {
            grid[i][j] = Math.max(grid[i - 1][j], grid[i][j - 1]);
            add(`No match — carry max(${grid[i - 1][j]}, ${grid[i][j - 1]}) = ${grid[i][j]}.`,
              i, j, [[i - 1, j], [i, j - 1]], false);
          }
        }
      }
      let i = n, j = m;
      const chars = [];
      add(`Table complete — LCS length ${grid[n][m]}. Walk back to recover it.`, n, m);
      while (i > 0 && j > 0) {
        if (a[i - 1] === b[j - 1]) {
          chars.push(a[i - 1]);
          path.push([i, j]);
          add(`'${a[i - 1]}' is part of the LCS — step diagonally.`, i, j, [], true);
          i--; j--;
        } else if (grid[i - 1][j] >= grid[i][j - 1]) {
          i--; add('Follow the larger neighbour upward.', i, j);
        } else {
          j--; add('Follow the larger neighbour leftward.', i, j);
        }
      }
      add(`The longest common subsequence is '${chars.reverse().join('')}'.`);
      return { steps, meta };
    }

    if (algoId === 'two_sum_sorted') {
      const arr = parsed.array, target = parsed.target;
      const steps = [];
      const counts = { checks: 0, moves: 0 };
      const add = (note2, left = null, right = null, sum = null, found = null) =>
        steps.push({
          i: steps.length,
          structures: { left, right, sum, found, counts: { ...counts } },
          highlight: { index: left }, note: note2,
        });
      if (arr.length < 2) { add('Fewer than two values — no pair to find.', null, null, null, false); return { steps }; }
      let left = 0, right = arr.length - 1;
      add(`Find two values summing to ${fmt(target)} — pointers start at both ends.`, left, right);
      while (left < right) {
        const s = arr[left] + arr[right];
        counts.checks++;
        if (s === target) {
          add(`${fmt(arr[left])} + ${fmt(arr[right])} = ${fmt(target)} — pair found!`, left, right, s, true);
          return { steps };
        }
        if (s < target) {
          add(`Sum ${fmt(s)} is too small — move the left pointer right.`, left, right, s);
          left++; counts.moves++;
        } else {
          add(`Sum ${fmt(s)} is too big — move the right pointer left.`, left, right, s);
          right--; counts.moves++;
        }
      }
      add(`Pointers met — no pair sums to ${fmt(target)}.`, left, right, null, false);
      return { steps };
    }

    if (algoId === 'sliding_window') {
      const arr = parsed.array, k = parsed.target;
      const steps = [];
      const counts = { additions: 0, windows: 0 };
      const add = (note2, window = null, sum = null, best = null, bw = null) =>
        steps.push({
          i: steps.length,
          structures: { window, sum, best, best_window: bw, counts: { ...counts } },
          highlight: { index: window ? window[1] : null }, note: note2,
        });
      add(`Find the size-${k} window with the biggest sum — drop one, add one.`);
      let cur = arr.slice(0, k).reduce((a, b) => a + b, 0);
      counts.additions += k; counts.windows++;
      let best = cur, bw = [0, k - 1];
      add(`First window [0..${k - 1}] sums to ${fmt(cur)}.`, [0, k - 1], cur, best, bw.slice());
      for (let i = k; i < arr.length; i++) {
        cur = cur - arr[i - k] + arr[i];
        counts.additions++; counts.windows++;
        const w = [i - k + 1, i];
        const isBest = cur > best;
        if (isBest) { best = cur; bw = w.slice(); }
        add(`Slide: drop ${fmt(arr[i - k])}, add ${fmt(arr[i])} — sum ${fmt(cur)}.${isBest ? ' New best!' : ''}`,
          w, cur, best, bw.slice());
      }
      add(`Done — best window [${bw[0]}..${bw[1]}] sums to ${fmt(best)}.`, null, cur, best, bw.slice());
      return { steps };
    }

    if (algoId === 'kadanes') {
      const arr = parsed.array;
      const steps = [];
      const counts = { steps: 0, extensions: 0, restarts: 0 };
      const add = (note2, window = null, sum = null, best = null, bw = null) =>
        steps.push({
          i: steps.length,
          structures: { window, sum, best, best_window: bw, counts: { ...counts } },
          highlight: { index: window ? window[1] : null }, note: note2,
        });
      if (!arr.length) { add('An empty array has no subarray to maximize.'); return { steps }; }
      add('Extend the current run, or cut losses and restart — one pass.');
      let cur = arr[0], start = 0, best = arr[0], bw = [0, 0];
      counts.steps++;
      add(`Start the run at ${fmt(arr[0])}.`, [0, 0], cur, best, bw.slice());
      for (let i = 1; i < arr.length; i++) {
        const v = arr[i];
        counts.steps++;
        let note2;
        if (cur + v < v) {
          cur = v; start = i; counts.restarts++;
          note2 = `The old run would drag ${fmt(v)} down — restart here.`;
        } else {
          cur += v; counts.extensions++;
          note2 = `Extend the run with ${fmt(v)} — run sum ${fmt(cur)}.`;
        }
        const w = [start, i];
        if (cur > best) { best = cur; bw = w.slice(); note2 += ' New best!'; }
        add(note2, w, cur, best, bw.slice());
      }
      add(`Best run [${bw[0]}..${bw[1]}] with sum ${fmt(best)}.`, null, cur, best, bw.slice());
      return { steps };
    }

    if (algoId === 'bubble_sort' || algoId === 'insertion_sort' || algoId === 'selection_sort') {
      const arr = parsed.array.slice();
      const n2 = arr.length;
      const steps = [];
      let sortedRanges = [];
      const counts = algoId === 'bubble_sort'
        ? { comparisons: 0, swaps: 0, passes: 0 }
        : algoId === 'insertion_sort'
          ? { comparisons: 0, shifts: 0, inserts: 0 }
          : { comparisons: 0, swaps: 0 };
      const add = (note2, extra = {}) => steps.push({
        i: steps.length,
        structures: { array: arr.slice(), merging: null, comparing: null, placed: null,
          sorted_ranges: sortedRanges.map(r => r.slice()), counts: { ...counts }, ...extra },
        highlight: { index: extra.placed ?? null },
        note: note2,
      });
      if (n2 <= 1) {
        if (n2) sortedRanges = [[0, 0]];
        add('Nothing to sort — already in order.');
        return { steps };
      }
      add(`Start with ${n2} unsorted values.`);
      if (algoId === 'bubble_sort') {
        let done = false;
        for (let end = n2 - 1; end > 0 && !done; end--) {
          counts.passes++;
          let swapped = false;
          for (let j = 0; j < end; j++) {
            counts.comparisons++;
            if (arr[j] > arr[j + 1]) {
              [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
              counts.swaps++; swapped = true;
              add(`${fmt(arr[j + 1])} > ${fmt(arr[j])} — swap; the heavier one bubbles right.`,
                { comparing: [arr[j], arr[j + 1]], placed: j + 1 });
            } else {
              add(`${fmt(arr[j])} <= ${fmt(arr[j + 1])} — in order, move on.`,
                { comparing: [arr[j], arr[j + 1]], placed: j });
            }
          }
          sortedRanges = [[end, n2 - 1]];
          add(`Pass ${counts.passes} done — position ${end} locked.`, { placed: end });
          if (!swapped) { sortedRanges = [[0, n2 - 1]]; add('No swaps — already sorted. Early exit!'); done = true; }
        }
        if (!done) { sortedRanges = [[0, n2 - 1]]; add('Only one value left unlocked — sorted.'); }
      } else if (algoId === 'insertion_sort') {
        sortedRanges = [[0, 0]];
        for (let i = 1; i < n2; i++) {
          const key = arr[i];
          add(`Pick up ${fmt(key)} (position ${i}) — find its slot.`, { placed: i });
          let j = i;
          while (j > 0) {
            counts.comparisons++;
            if (arr[j - 1] > key) {
              [arr[j], arr[j - 1]] = [arr[j - 1], key];
              counts.shifts++;
              add(`${fmt(arr[j])} is bigger — shift it right; the card slides left.`,
                { comparing: [arr[j], key], placed: j - 1 });
              j--;
            } else break;
          }
          counts.inserts++;
          sortedRanges = [[0, i]];
          add(`${fmt(key)} settles at position ${j}.`, { placed: j });
        }
        add('Every card placed — sorted.');
      } else {
        for (let i = 0; i < n2 - 1; i++) {
          let minIdx = i;
          add(`Round ${i + 1}: assume ${fmt(arr[i])} is the smallest.`, { placed: i, merging: [i, n2 - 1] });
          for (let j = i + 1; j < n2; j++) {
            counts.comparisons++;
            const champ = arr[minIdx];
            if (arr[j] < champ) {
              minIdx = j;
              add(`${fmt(arr[j])} beats ${fmt(champ)} — new champion.`,
                { comparing: [arr[j], champ], placed: j, merging: [i, n2 - 1] });
            } else {
              add(`${fmt(arr[j])} is not smaller — champion unchanged.`,
                { comparing: [arr[j], champ], placed: j, merging: [i, n2 - 1] });
            }
          }
          if (minIdx !== i) { [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]]; counts.swaps++; }
          sortedRanges = [[0, i]];
          add(`Champion ${fmt(arr[i])} locked at position ${i}.`, { placed: i });
        }
        sortedRanges = [[0, n2 - 1]];
        add('Last value must be the biggest — sorted.');
      }
      return { steps };
    }

    if (algoId === 'linked_list_reverse') {
      const values = parsed.array.slice();
      const n2 = values.length;
      const nxt = values.map((_, i) => (i < n2 - 1 ? i + 1 : null));
      const steps = [];
      const counts = { flips: 0 };
      let prev = null, curr = n2 ? 0 : null, saved = null;
      const add = (note2) => steps.push({
        i: steps.length,
        structures: { values: values.slice(), next: nxt.slice(), prev, curr, saved,
          counts: { ...counts } },
        highlight: { index: curr },
        note: note2,
      });
      if (n2 === 0) { add('An empty chain — nothing to reverse.'); return { steps }; }
      if (n2 === 1) { add('A single carriage is its own reversal.'); return { steps }; }
      add(`A chain of ${n2} carriages. Reverse every coupling with prev / curr / next.`);
      while (curr !== null) {
        saved = nxt[curr];
        nxt[curr] = prev;
        counts.flips++;
        add(`Save the next carriage, then flip node ${curr}'s coupling backwards.`);
        prev = curr; curr = saved; saved = null;
        add(`Advance: prev is node ${prev}, curr is ${curr === null ? 'None' : 'node ' + curr}.`);
      }
      add(`curr is None — node ${prev} is the new head. Chain reversed.`);
      return { steps };
    }

    if (algoId === 'balanced_brackets') {
      const text = parsed.text;
      const PAIRS = { ')': '(', ']': '[', '}': '{' };
      const steps = [];
      const stack = [];
      const counts = { pushes: 0, pops: 0 };
      let balanced = null;
      const add = (note2, pos = null, action = null) => steps.push({
        i: steps.length,
        structures: { stack: stack.slice(), pos, action, balanced, counts: { ...counts } },
        highlight: { index: pos },
        note: note2,
      });
      add(`Scan the ${text.length} symbols left to right.`);
      let mismatched = false;
      for (let idx = 0; idx < text.length; idx++) {
        const ch = text[idx];
        if ('([{'.includes(ch)) {
          stack.push(ch); counts.pushes++;
          add(`'${ch}' opens — push it. Depth ${stack.length}.`, idx, 'push');
        } else if (stack.length && stack[stack.length - 1] === PAIRS[ch]) {
          const op = stack.pop(); counts.pops++;
          add(`'${ch}' closes '${op}' — pop. Depth ${stack.length}.`, idx, 'pop');
        } else {
          balanced = false; mismatched = true;
          add(`'${ch}' has nothing to close — mismatch! Unbalanced.`, idx, 'mismatch');
          break;
        }
      }
      if (!mismatched) {
        balanced = stack.length === 0;
        add(balanced
          ? 'Every opener matched and the stack is empty — balanced!'
          : `${stack.length} opener(s) never closed — unbalanced.`, null, 'done');
      }
      return { steps };
    }
    if (algoId === 'binary_search') {
      const arr = parsed.array, target = parsed.target;
      const steps = [];
      let low = 0, high = arr.length - 1, found = false;
      const counts = { comparisons: 0 };
      const push = (structures, index, note2) => steps.push({
        i: steps.length, structures: { ...structures, counts: { ...counts } },
        highlight: { index }, note: note2,
      });
      push({ low, high, mid: null, found: null }, null, arr.length
        ? `Search ${arr.length} sorted values for target ${fmt(target)}.`
        : 'The array is empty — nothing to search.');
      while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        counts.comparisons++;
        push({ low, high, mid, found: null }, mid,
          `Check the middle: position ${mid} holds ${fmt(arr[mid])}.`);
        if (arr[mid] === target) {
          found = true;
          push({ low, high, mid, found: true }, mid,
            `Found it — ${fmt(target)} is at position ${mid}.`);
          break;
        } else if (arr[mid] < target) {
          low = mid + 1;
          push({ low, high, mid, found: null }, mid,
            `${fmt(arr[mid])} is smaller — search the right half.`);
        } else {
          high = mid - 1;
          push({ low, high, mid, found: null }, mid,
            `${fmt(arr[mid])} is larger — search the left half.`);
        }
      }
      if (!found) {
        push({ low, high, mid: null, found: false }, null,
          `The range is empty — ${fmt(target)} is not in the array.`);
      }
      return { steps };
    }

    if (algoId === 'quick_sort') {
      const arr = parsed.array.slice();
      const steps = [];
      const sortedRanges = [];
      const counts = { comparisons: 0, swaps: 0, partitions: 0 };
      const add = (note2, extra = {}) => steps.push({
        i: steps.length,
        structures: { array: arr.slice(), merging: null, comparing: null, placed: null,
          sorted_ranges: sortedRanges.map(r => r.slice()), counts: { ...counts }, ...extra },
        highlight: { index: extra.placed ?? null },
        note: note2,
      });
      if (arr.length <= 1) {
        if (arr.length) sortedRanges.push([0, 0]);
        add('Nothing to sort — already in order.');
        return { steps };
      }
      add(`Start with ${arr.length} unsorted values.`);
      const qs = (lo, hi) => {
        if (lo > hi) return;
        if (lo === hi) {
          sortedRanges.push([lo, lo]);
          add(`Position ${lo} holds a single value — locked in place.`, { placed: lo });
          return;
        }
        const pivot = arr[hi];
        add(`Partition ${lo}..${hi}: pivot is ${fmt(pivot)} (position ${hi}).`,
          { merging: [lo, hi], placed: hi });
        let i = lo - 1;
        for (let j = lo; j < hi; j++) {
          counts.comparisons++;
          if (arr[j] <= pivot) {
            i++;
            if (i !== j) {
              [arr[i], arr[j]] = [arr[j], arr[i]];
              counts.swaps++;
              add(`${fmt(arr[i])} <= pivot ${fmt(pivot)} — swap into the small side.`,
                { merging: [lo, hi], comparing: [arr[i], pivot], placed: i });
            } else {
              add(`${fmt(arr[j])} <= pivot ${fmt(pivot)} — already on the small side.`,
                { merging: [lo, hi], comparing: [arr[j], pivot], placed: j });
            }
          } else {
            add(`${fmt(arr[j])} > pivot ${fmt(pivot)} — stays on the big side.`,
              { merging: [lo, hi], comparing: [arr[j], pivot], placed: j });
          }
        }
        const p = i + 1;
        if (p !== hi) { [arr[p], arr[hi]] = [arr[hi], arr[p]]; counts.swaps++; }
        counts.partitions++;
        sortedRanges.push([p, p]);
        add(`Pivot ${fmt(pivot)} locked at its final position ${p}.`,
          { merging: [lo, hi], placed: p });
        qs(lo, p - 1);
        qs(p + 1, hi);
      };
      qs(0, arr.length - 1);
      add('Every pivot locked — the array is sorted.');
      return { steps };
    }

    // merge_sort
    const arr = parsed.array.slice();
    const steps = [];
    const sortedRanges = [];
    const mCounts = { comparisons: 0, writes: 0, merges: 0 };
    const snap = (note, extra = {}) => steps.push({
      i: steps.length,
      structures: { array: arr.slice(), merging: null, comparing: null, placed: null,
        sorted_ranges: sortedRanges.map(r => r.slice()), counts: { ...mCounts }, ...extra },
      highlight: { index: extra.placed ?? null },
      note,
    });
    if (arr.length <= 1) {
      if (arr.length) sortedRanges.push([0, 0]);
      snap('Nothing to sort — already in order.');
      return { steps };
    }
    snap(`Start with ${arr.length} unsorted values.`);
    const msort = (lo, hi) => {
      if (hi - lo <= 1) return;
      const mid = Math.floor((lo + hi) / 2);
      snap(`Split positions ${lo}..${hi - 1} into halves.`, { merging: [lo, hi - 1] });
      msort(lo, mid); msort(mid, hi);
      const left = arr.slice(lo, mid), right = arr.slice(mid, hi);
      let i = 0, j = 0;
      const merged = [];
      const commit = () => arr.splice(lo, hi - lo, ...merged, ...left.slice(i), ...right.slice(j));
      while (i < left.length && j < right.length) {
        const a = left[i], b = right[j];
        if (a <= b) { merged.push(a); i++; } else { merged.push(b); j++; }
        mCounts.comparisons++; mCounts.writes++;
        commit();
        snap(`Compare ${fmt(a)} vs ${fmt(b)} — place ${fmt(merged[merged.length - 1])}.`,
          { merging: [lo, hi - 1], comparing: [a, b], placed: lo + merged.length - 1 });
      }
      while (i < left.length) {
        merged.push(left[i++]); mCounts.writes++; commit();
        snap(`Copy remaining ${fmt(merged[merged.length - 1])}.`,
          { merging: [lo, hi - 1], placed: lo + merged.length - 1 });
      }
      while (j < right.length) {
        merged.push(right[j++]); mCounts.writes++; commit();
        snap(`Copy remaining ${fmt(merged[merged.length - 1])}.`,
          { merging: [lo, hi - 1], placed: lo + merged.length - 1 });
      }
      for (let r = sortedRanges.length - 1; r >= 0; r--) {
        if (lo <= sortedRanges[r][0] && sortedRanges[r][1] <= hi - 1) sortedRanges.splice(r, 1);
      }
      sortedRanges.push([lo, hi - 1]);
      mCounts.merges++;
      snap(`Positions ${lo}..${hi - 1} merged — this section is sorted.`, { merging: [lo, hi - 1] });
    };
    msort(0, arr.length);
    snap('Every section merged — the whole array is in order.');
    return { steps };
  }

  // ── Graph editor ──
  function svgCoords(e) {
    const rect = svg.getBoundingClientRect();
    return {
      x: Math.round((e.clientX - rect.left) * 760 / rect.width),
      y: Math.round((e.clientY - rect.top) * 280 / rect.height),
    };
  }

  function addNodeAt(x, y) {
    if (userGraph.nodes.length >= GRAPH_LIMITS.nodes) {
      showGraphError(`Max ${GRAPH_LIMITS.nodes} nodes — that's plenty for one trace.`);
      return;
    }
    const id = nextNodeId();
    userGraph.nodes.push({
      id,
      x: Math.min(Math.max(x, 30), 730),
      y: Math.min(Math.max(y, 35), 240),
    });
    if (!startNodeId) startNodeId = id;
    graphChanged();
  }

  function addEdge(a, b) {
    if (a === b) return;
    if (userGraph.links.length >= GRAPH_LIMITS.edges) {
      showGraphError(`Max ${GRAPH_LIMITS.edges} edges.`);
      return;
    }
    const exists = userGraph.links.some(l =>
      (l.source === a && l.target === b) || (l.source === b && l.target === a));
    if (exists) {
      showGraphError('Those two are already connected — click the weight to change it.');
      graphChanged();
      return;
    }
    userGraph.links.push({ source: a, target: b, weight: 5 });
    graphChanged();
  }

  function deleteNode(id) {
    userGraph.nodes = userGraph.nodes.filter(n => n.id !== id);
    userGraph.links = userGraph.links.filter(l => l.source !== id && l.target !== id);
    graphChanged();
  }

  function deleteEdge(idx) {
    if (Number.isNaN(idx)) return;
    userGraph.links.splice(idx, 1);
    graphChanged();
  }

  function editWeight(idx, anchorEl) {
    const link = userGraph.links[idx];
    const host = view.querySelector('#engine-view');
    if (!link || !host) return;
    host.style.position = 'relative';
    host.querySelector('.weight-editor')?.remove();

    const input = document.createElement('input');
    input.type = 'number';
    input.min = '0';
    input.max = String(GRAPH_LIMITS.weight);
    input.value = link.weight;
    input.className = 'weight-editor';
    const hostRect = host.getBoundingClientRect();
    const aRect = anchorEl.getBoundingClientRect();
    input.style.cssText = `position:absolute; width:72px; z-index:5;
      left:${Math.round(aRect.left - hostRect.left - 12)}px;
      top:${Math.round(aRect.top - hostRect.top - 10)}px;
      background:rgba(2,4,6,0.95); color:var(--c); border:1px solid var(--c);
      font-family:var(--font-mono); font-size:0.9rem; padding:2px 6px; outline:none;`;

    const commit = () => {
      const w = Number(input.value);
      input.remove();
      if (!Number.isFinite(w) || w < 0 || w > GRAPH_LIMITS.weight) {
        showGraphError(`Weight must be between 0 and ${GRAPH_LIMITS.weight.toLocaleString()}.`);
        return;
      }
      link.weight = w;
      graphChanged();
    };
    input.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter') commit();
      if (ev.key === 'Escape') input.remove();
    });
    input.addEventListener('blur', () => {
      if (document.body.contains(input)) commit();
    });
    host.appendChild(input);
    input.focus();
    input.select();
  }

  function attachGraphEditor() {
    svg.style.cursor = 'crosshair';

    svg.addEventListener('click', (e) => {
      const t = e.target;
      if (challenge.active) {
        if (challenge.awaiting && t.classList?.contains('node')) {
          challengeGuess(t.id.replace('node-', ''));
        }
        return;   // no graph editing mid-challenge
      }
      if (t.classList?.contains('node')) {
        const id = t.id.replace('node-', '');
        resetTraceState();
        if (selectedNodeId && selectedNodeId !== id) {
          const from = selectedNodeId;
          selectedNodeId = null;
          addEdge(from, id);
        } else if (selectedNodeId === id) {
          selectedNodeId = null;
          renderGraph(currentMeta);
        } else {
          selectedNodeId = id;
          renderGraph(currentMeta);
        }
        return;
      }
      if (t.classList?.contains('edge-weight')) {
        editWeight(Number(t.dataset.idx), t);
        return;
      }
      if (t === svg) {
        const { x, y } = svgCoords(e);
        addNodeAt(x, y);
      }
    });

    const deleteTarget = (t) => {
      if (t.classList?.contains('node')) { deleteNode(t.id.replace('node-', '')); return true; }
      if (t.classList?.contains('edge') || t.classList?.contains('edge-weight')) {
        deleteEdge(Number(t.dataset.idx));
        return true;
      }
      return false;
    };

    svg.addEventListener('contextmenu', (e) => {
      if (deleteTarget(e.target)) e.preventDefault();
    });

    // Long-press delete for touch devices
    let pressTimer = null;
    svg.addEventListener('pointerdown', (e) => {
      if (e.pointerType !== 'touch') return;
      const t = e.target;
      pressTimer = setTimeout(() => deleteTarget(t), 650);
    });
    ['pointerup', 'pointermove', 'pointercancel'].forEach(ev =>
      svg.addEventListener(ev, () => clearTimeout(pressTimer)));

    presetSelect?.addEventListener('change', () => {
      userGraph = graphPreset(presetSelect.value);
      startNodeId = userGraph.nodes[0]?.id || null;
      graphChanged();
    });
    startSelect?.addEventListener('change', () => {
      startNodeId = startSelect.value;
      resetTraceState();
      renderGraph(currentMeta);
    });
  }

  function buildWhatIfSliders() {
    const whatIfContainer = view.querySelector('#whatif-controls');
    if (!whatIfContainer || traceView !== 'graph') return;
    whatIfContainer.innerHTML = '';
    userGraph.links.forEach((link, idx) => {
      const row = document.createElement('div');
      row.style.cssText = 'display:flex; align-items:center; gap:1rem; font-family:var(--font-mono); font-size:0.9rem; color:var(--cDim);';
      row.innerHTML = `
        <span style="min-width:120px;">${link.source}→${link.target}</span>
        <input type="range" min="1" max="${Math.max(30, link.weight)}" value="${link.weight}"
          style="flex:1; accent-color:var(--c);"
          id="whatif-${idx}">
        <span id="whatif-val-${idx}" style="min-width:40px; color:var(--c);">${link.weight}</span>
      `;
      const slider = row.querySelector('input');
      const valLabel = row.querySelector(`#whatif-val-${idx}`);
      slider.addEventListener('input', () => {
        userGraph.links[idx].weight = parseInt(slider.value);
        valLabel.textContent = slider.value;
        resetTraceState();
        renderGraph(currentMeta);
      });
      whatIfContainer.appendChild(row);
    });
  }

  async function checkBackend() {
    try {
      await api.getAlgorithms();
      status.innerHTML = 'STATUS: <span style="color:var(--cBright)">CONNECTED</span>';
      isOffline = false;
    } catch {
      status.innerHTML = 'STATUS: <span style="color:#ff5f5f">OFFLINE (EMULATOR)</span>';
      isOffline = true;
    }
  }

  function localTrace(algorithm, startNode) {
    // Local emulator for offline mode — Dijkstra and BFS on the user's graph
    const nodes = userGraph.nodes.map(n => n.id);
    const adj = {};
    userGraph.links.forEach(l => {
      if (!adj[l.source]) adj[l.source] = [];
      if (!adj[l.target]) adj[l.target] = [];
      adj[l.source].push({ to: l.target, w: l.weight });
      adj[l.target].push({ to: l.source, w: l.weight });
    });

    if (algorithm === 'bfs') {
      const steps = [];
      const visited = new Set([startNode]);
      const queue = [startNode];
      const counts = { enqueues: 1, dequeues: 0, edge_checks: 0 };
      steps.push({ i: 0, highlight: { node: startNode, edge: null },
        note: `Enqueue start node ${startNode}.`,
        structures: { queue: [...queue], visited: [...visited], counts: { ...counts } }
      });
      while (queue.length > 0) {
        const u = queue.shift();
        counts.dequeues++;
        steps.push({ i: steps.length, highlight: { node: u, edge: null },
          note: `Dequeue ${u}.`,
          structures: { queue: [...queue], visited: [...visited], counts: { ...counts } }
        });
        for (const edge of (adj[u] || [])) {
          counts.edge_checks++;
          if (visited.has(edge.to)) continue;
          visited.add(edge.to);
          queue.push(edge.to);
          counts.enqueues++;
          steps.push({ i: steps.length, highlight: { node: edge.to, edge: [u, edge.to] },
            note: `Discover ${edge.to} from ${u}.`,
            structures: { queue: [...queue], visited: [...visited], counts: { ...counts } }
          });
        }
      }
      steps.push({ i: steps.length, highlight: { node: null, edge: null },
        note: 'Queue empty — traversal complete.',
        structures: { queue: [], visited: [...visited], counts: { ...counts } }
      });
      return { steps };
    }

    if (algorithm === 'prims_mst' || algorithm === 'kruskals_mst') {
      const steps = [];
      const mst = [];
      let total = 0;
      const allIds = nodes.slice();

      if (algorithm === 'prims_mst') {
        const inTree = new Set([startNode]);
        const counts = { edge_checks: 0, edges_added: 0, rejections: 0 };
        const add = (note2, node = null, edge = null) => steps.push({
          i: steps.length,
          structures: { visited: [...inTree].sort(), mst_edges: mst.map(e => e.slice()),
            total_weight: total, counts: { ...counts } },
          highlight: { node, edge }, note: note2,
        });
        add(`Build the cheapest network. Start at ${startNode}.`, startNode);
        const frontier = [];
        (adj[startNode] || []).forEach(e => frontier.push({ w: e.w, u: startNode, v: e.to }));
        while (frontier.length && inTree.size < allIds.length) {
          frontier.sort((a, b) => a.w - b.w || (a.v < b.v ? -1 : 1));
          const { w, u, v } = frontier.shift();
          counts.edge_checks++;
          if (inTree.has(v)) {
            counts.rejections++;
            add(`Edge ${u}–${v} (${fmt(w)}) leads back into the tree — would make a cycle. Skip.`, v, [u, v]);
            continue;
          }
          inTree.add(v); mst.push([u, v]); total += w; counts.edges_added++;
          add(`Add edge ${u}–${v} (${fmt(w)}) — cheapest way to a new node. ` +
            `Tree spans ${inTree.size} of ${allIds.length}.`, v, [u, v]);
          (adj[v] || []).forEach(e => { if (!inTree.has(e.to)) frontier.push({ w: e.w, u: v, v: e.to }); });
        }
        const unreached = allIds.filter(n => !inTree.has(n));
        add(unreached.length
          ? `${unreached.length} node(s) unreachable from ${startNode}: ${unreached.join(', ')}.`
          : `Every node connected with ${mst.length} edges at total cost ${fmt(total)}.`);
        return { steps };
      }

      // kruskals_mst
      const parent = {};
      allIds.forEach(n => { parent[n] = n; });
      const find = (x) => { while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; };
      const comps = () => {
        const g = {};
        allIds.forEach(n => { (g[find(n)] = g[find(n)] || []).push(n); });
        return Object.values(g).map(v => v.slice().sort()).sort((a, b) => (a[0] < b[0] ? -1 : 1));
      };
      const counts = { edge_checks: 0, unions: 0, cycles_skipped: 0 };
      const add = (note2, node = null, edge = null) => steps.push({
        i: steps.length,
        structures: { visited: [...new Set(mst.flat())].sort(), mst_edges: mst.map(e => e.slice()),
          components: comps(), total_weight: total, counts: { ...counts } },
        highlight: { node, edge }, note: note2,
      });
      const sorted = userGraph.links
        .map(l => ({ w: l.weight, a: l.source, b: l.target }))
        .sort((x, y) => x.w - y.w || (x.a < y.a ? -1 : 1));
      if (!sorted.length) { add(`No edges — ${allIds.length} isolated node(s).`); return { steps }; }
      add(`Sort every edge cheapest-first, then take each one unless it closes a cycle.`);
      add(`Every node starts in its own group — ${allIds.length} components.`);
      for (const { w, a, b } of sorted) {
        counts.edge_checks++;
        const ra = find(a), rb = find(b);
        if (ra === rb) {
          counts.cycles_skipped++;
          add(`Edge ${a}–${b} (${fmt(w)}): already in the same group — would close a cycle. Reject.`, b, [a, b]);
          continue;
        }
        parent[rb] = ra; mst.push([a, b]); total += w; counts.unions++;
        add(`Edge ${a}–${b} (${fmt(w)}): different groups — safe, union them. Cost ${fmt(total)}.`, b, [a, b]);
        if (mst.length === allIds.length - 1) break;
      }
      const groups = comps();
      add(groups.length > 1
        ? `${groups.length} components left — the graph is disconnected, so this is a spanning forest. Cost ${fmt(total)}.`
        : `Every node connected with ${mst.length} edges at total cost ${fmt(total)}.`);
      return { steps };
    }

    if (algorithm === 'dfs') {
      const steps = [];
      const visited = new Set();
      const path = [];
      const counts = { visits: 0, edge_checks: 0, backtracks: 0 };
      const add = (note2, node = null, edge = null) => steps.push({
        i: steps.length, highlight: { node, edge },
        structures: { stack: [...path], visited: [...visited].sort(), counts: { ...counts } },
        note: note2,
      });
      const go = (u, parent) => {
        visited.add(u); path.push(u); counts.visits++;
        add(parent ? `Go deeper: ${parent} to ${u}.` : `Start at ${u} — dive into the first corridor.`,
          u, parent ? [parent, u] : null);
        const neighbors = (adj[u] || []).slice().sort((a, b) => a.to < b.to ? -1 : 1);
        for (const e of neighbors) {
          counts.edge_checks++;
          if (!visited.has(e.to)) go(e.to, u);
        }
        path.pop(); counts.backtracks++;
        if (path.length) {
          add(`All routes from ${u} explored — backtrack to ${path[path.length - 1]}.`,
            path[path.length - 1]);
        }
      };
      go(startNode, null);
      add('Stack empty — every reachable room mapped.');
      return { steps };
    }

    const dist = {};
    const steps = [];
    nodes.forEach(n => dist[n] = Infinity);
    dist[startNode] = 0;
    const pq = [{ node: startNode, d: 0 }];
    const visited = new Set();
    const counts = { visits: 0, edge_checks: 0, relaxations: 0, heap_pushes: 1 };

    steps.push({ i: 0, highlight: { node: startNode, edge: null },
      note: `Start at ${startNode} with distance 0.`,
      structures: { dist: { ...dist }, visited: [], counts: { ...counts } }
    });

    while (pq.length > 0) {
      pq.sort((a, b) => a.d - b.d);
      const { node, d } = pq.shift();
      if (visited.has(node)) continue;
      visited.add(node);
      counts.visits++;
      steps.push({ i: steps.length, highlight: { node, edge: null },
        note: `Visit ${node} (distance ${d}).`,
        structures: { dist: { ...dist }, visited: [...visited], counts: { ...counts } }
      });
      for (const edge of (adj[node] || [])) {
        if (visited.has(edge.to)) continue;
        counts.edge_checks++;
        const nd = d + edge.w;
        if (nd < dist[edge.to]) {
          dist[edge.to] = nd;
          pq.push({ node: edge.to, d: nd });
          counts.relaxations++;
          counts.heap_pushes++;
          steps.push({ i: steps.length, highlight: { node: edge.to, edge: [node, edge.to] },
            note: `Relax edge ${node}→${edge.to}: new distance ${nd}.`,
            structures: { dist: { ...dist }, visited: [...visited], counts: { ...counts } }
          });
        }
      }
    }
    steps.push({ i: steps.length, highlight: { node: null, edge: null },
      note: 'Priority queue empty — all reachable nodes finalized.',
      structures: { dist: { ...dist }, visited: [...visited], counts: { ...counts } }
    });
    return { steps };
  }

  async function run() {
    runBtn.disabled = true;
    explanationBox.classList.add('is-hidden');
    status.innerHTML = 'STATUS: <span style="color:var(--c)">TRACING...</span>';
    status.className = 'engine-status-pill running';

    try {
      let res;
      if (traceView !== 'graph') {
        const parsed = parseArrayInput();
        if (parsed.error) {
          status.innerHTML = `STATUS: <span style="color:#ff5f5f">${escapeHTML(parsed.error).toUpperCase()}</span>`;
          status.className = 'engine-status-pill';
          runBtn.disabled = false;
          return;
        }
        if (parsed.sortedForYou && arrayHint) {
          arrayHint.textContent =
            'Heads up: your numbers were sorted first — this algorithm only works on sorted data.';
        }
        if (traceView === 'table') {
          renderTableView(parsed.target);
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { target: parsed.target });
        } else if (traceView === 'list') {
          renderListView(parsed.array);
          const payload = algoId === 'floyd_cycle'
            ? { array: parsed.array, target: parsed.target }
            : { array: parsed.array };
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, payload);
        } else if (traceView === 'stack') {
          renderStackView(parsed.text);
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { text: parsed.text });
        } else if (algoId === 'kmp_search' || algoId === 'rabin_karp'
                   || algoId === 'z_function' || algoId === 'manacher') {
          renderArrayView(parsed.chars);
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { text: parsed.text });
        } else if (algoId === 'segment_tree') {
          renderTreeView();
          const payload = parsed.text
            ? { array: parsed.array, text: parsed.text }
            : { array: parsed.array };
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, payload);
        } else if (algoId === 'fenwick_tree') {
          renderArrayView(parsed.array);
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { array: parsed.array, target: parsed.target });
        } else if (algoId === 'hash_table') {
          renderGridView();
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { text: parsed.text });
        } else if (algoId === 'merge_intervals') {
          renderArrayView(parsed.chars);
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { text: parsed.text });
        } else if (algoId === 'coin_change') {
          renderGridView();
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { array: parsed.array, target: parsed.target });
        } else if (algoId === 'bst_delete') {
          currentArrayValues = parsed.array.slice();
          renderTreeView();
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { array: parsed.array, target: parsed.target });
        } else if (algoId === 'trie_insert') {
          renderTreeView();
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { text: parsed.text });
        } else if (algoId === 'n_queens' || algoId === 'sieve') {
          if (algoId === 'sieve') {
            renderArrayView(Array.from({ length: parsed.target + 1 }, (_, i) => i));
          } else {
            renderGridView();
          }
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { target: parsed.target });
        } else if (algoId === 'unique_paths' || algoId === 'flood_fill') {
          renderGridView();
          const payload = parsed.text
            ? { target: parsed.target, text: parsed.text }
            : { target: parsed.target };
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, payload);
        } else if (algoId === 'house_robber' || algoId === 'lis') {
          renderGridView();
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { array: parsed.array });
        } else if (algoId === 'subset_sum') {
          renderGridView();
          res = isOffline
            ? localArrayTrace(parsed)
            : await api.postTrace(algoId, { array: parsed.array, target: parsed.target });
        } else if (traceView === 'tree') {
          currentArrayValues = parsed.array.slice();
          renderTreeView();
          const payload = algoId === 'bst_search'
            ? { array: parsed.array, target: parsed.target }
            : { array: parsed.array };
          res = isOffline ? localArrayTrace(parsed) : await api.postTrace(algoId, payload);
        } else if (traceView === 'grid') {
          renderGridView();
          const payload = algoId === 'knapsack_01'
            ? { text: parsed.text, target: parsed.target }
            : { text: parsed.text };
          res = isOffline ? localArrayTrace(parsed) : await api.postTrace(algoId, payload);
        } else {
          renderArrayView(parsed.array);
          if (isOffline) {
            res = localArrayTrace(parsed);
          } else {
            const needsTarget = ['binary_search', 'two_sum_sorted', 'sliding_window']
              .includes(algoId);
            const payload = needsTarget
              ? { array: parsed.array, target: parsed.target }
              : { array: parsed.array };
            res = await api.postTrace(algoId, payload);
          }
        }
      } else {
        if (!userGraph.nodes.length) {
          status.innerHTML = 'STATUS: <span style="color:#ff5f5f">ADD SOME NODES FIRST — CLICK THE CANVAS.</span>';
          status.className = 'engine-status-pill';
          runBtn.disabled = false;
          return;
        }
        if (!startNodeId) startNodeId = userGraph.nodes[0].id;
        if (isOffline) {
          res = localTrace(algoId, startNodeId);
        } else {
          const graph = {
            nodes: userGraph.nodes,
            edges: userGraph.links.map(l => [l.source, l.target, l.weight])
          };
          res = await api.postTrace(algoId, { start: startNodeId, graph });
        }
      }
      loadTrace(res.steps, res.meta);
    } catch (e) {
      console.error(e);
      status.innerHTML = 'STATUS: <span style="color:#ff5f5f">TRACE FAILED</span>';
      runBtn.disabled = false;
      checkBackend();
    }
  }

  // ── CHALLENGE MODE: predict the next step ─────────────────
  // After each shown step, the player clicks the node/cell they think the
  // algorithm touches next. Correct = XP + combo; wrong = reveal + reset.
  const challengeBtn = view.querySelector('#challenge-btn');
  const comboChip = view.querySelector('#combo-chip');
  const challenge = { on: false, active: false, awaiting: null, combo: 0, right: 0, total: 0 };

  const challengeSupported = () => ['graph', 'array', 'tree'].includes(traceView);

  function challengeTargetOf(step) {
    if (!step) return null;
    if (traceView === 'graph') return step.highlight?.node ?? null;
    const idx = step.highlight?.index;
    return (idx === null || idx === undefined) ? null : idx;
  }

  function updateComboChip() {
    if (!comboChip) return;
    comboChip.classList.toggle('is-hidden', !challenge.active);
    comboChip.textContent = `COMBO ×${challenge.combo}`;
    comboChip.classList.toggle('combo-hot', challenge.combo >= 3);
  }

  function challengeFlash(target, good) {
    let el = null;
    if (traceView === 'graph') el = svg.querySelector(`#node-${target}`);
    else el = svg.querySelector(`#cell-${target}`) ||
              svg.querySelector(`[data-node-id="${target}"]`);
    if (!el) return;
    el.classList.remove('guess-good', 'guess-bad');
    void el.getBBox && el.getBoundingClientRect();
    el.classList.add(good ? 'guess-good' : 'guess-bad');
    setTimeout(() => el.classList.remove('guess-good', 'guess-bad'), 800);
  }

  function challengePrompt() {
    const cur = challengeTargetOf(currentSteps[currentStepIdx]);
    let j = currentStepIdx + 1;
    while (j < currentSteps.length) {
      const t = challengeTargetOf(currentSteps[j]);
      if (t !== null && String(t) !== String(cur)) break;
      j++;
    }
    if (j >= currentSteps.length) { challengeEnd(); return; }
    challenge.awaiting = { j, target: challengeTargetOf(currentSteps[j]) };
    const what = traceView === 'graph' ? 'node' : 'cell';
    note.textContent = `🎮 PREDICT — CLICK THE ${what.toUpperCase()} THE ALGORITHM TOUCHES NEXT (${challenge.right}/${challenge.total} SO FAR)`;
    note.style.opacity = 1;
    status.innerHTML = 'STATUS: <span style="color:var(--c)">YOUR MOVE</span>';
  }

  function challengeGuess(value) {
    if (!challenge.awaiting) return;
    const { j, target } = challenge.awaiting;
    challenge.awaiting = null;
    challenge.total++;
    const ok = String(value) === String(target);
    if (ok) {
      challenge.right++;
      challenge.combo++;
      Game.recordPrediction(true, challenge.combo);
    } else {
      challenge.combo = 0;
      Game.recordPrediction(false, 0);
      if (value !== null && value !== undefined) challengeFlash(value, false);
    }
    updateComboChip();
    renderStep(j);
    challengeFlash(target, true);
    setTimeout(challengePrompt, ok ? 700 : 1100);
  }

  function challengeBegin() {
    challenge.active = true;
    challenge.combo = 0; challenge.right = 0; challenge.total = 0;
    updateComboChip();
    if (scrubRow) scrubRow.style.display = 'none';
    challengePrompt();
  }

  function challengeEnd() {
    challenge.active = false;
    challenge.awaiting = null;
    updateComboChip();
    const acc = challenge.total ? Math.round((challenge.right / challenge.total) * 100) : 0;
    if (challenge.total > 0) {
      Game.award(25 + (acc >= 80 ? 25 : 0), `Challenge complete — ${acc}% accuracy`);
      note.textContent = `CHALLENGE COMPLETE: ${challenge.right}/${challenge.total} (${acc}%).` +
        (acc >= 80 ? ' PERFECT-RUN BONUS!' : ' RUN IT AGAIN TO BEAT IT.');
    }
    if (scrubRow && currentSteps.length) scrubRow.style.display = 'flex';
    status.innerHTML = 'STATUS: <span style="color:var(--cBright)">DONE</span>';
  }

  // One shared click listener for array/tree challenge guesses.
  svg.addEventListener('click', (e) => {
    if (!challenge.active || !challenge.awaiting) return;
    if (traceView === 'array') {
      const m = (e.target.id || '').match(/^(?:cell|cellval)-(\d+)$/);
      if (m) challengeGuess(Number(m[1]));
    } else if (traceView === 'tree') {
      const id = e.target.dataset?.nodeId;
      if (id !== undefined) challengeGuess(id);
    }
  });

  challengeBtn?.addEventListener('click', () => {
    challenge.on = !challenge.on;
    challengeBtn.classList.toggle('btn-primary', challenge.on);
    challengeBtn.textContent = challenge.on ? '🎮 Challenge ON' : '🎮 Challenge';
    if (!challenge.on && challenge.active) challengeEnd();
    if (challenge.on) {
      status.innerHTML = 'STATUS: <span style="color:var(--c)">PRESS RUN TO PLAY</span>';
    }
  });

  // ── Step scrubber: any step index renders fully from its data ──

  function computeTraceSummary() {
    const lastStep = currentSteps[currentSteps.length - 1];
    if (!lastStep) return '';
    let msg = lastStep?.structures?.found === false
      ? '— The target is not in this array.'
      : '';
    if (traceView === 'graph') {
      const s = lastStep.structures || {};
      let unreachable = [];
      if (s.dist) {
        unreachable = Object.keys(s.dist)
          .filter(k => s.dist[k] === null || s.dist[k] === Infinity);
      } else if (s.visited) {
        unreachable = userGraph.nodes.map(n => n.id)
          .filter(id => !s.visited.includes(id));
      }
      if (unreachable.length) {
        msg += ` — ${unreachable.length} unreachable from ${startNodeId}: ${unreachable.join(', ')}.`;
      }
    }
    return msg.trim();
  }

  function loadTrace(steps, meta) {
    currentSteps = steps || [];
    currentTraceMeta = meta || null;
    if (!currentSteps.length) { resetTraceState(); return; }
    Game.recordTrace(algoId);
    traceSummary = computeTraceSummary();
    if (scrubRow) scrubRow.style.display = 'flex';
    if (counterPanel) counterPanel.style.display = 'flex';
    if (stepSlider) { stepSlider.max = currentSteps.length - 1; stepSlider.value = 0; }
    if (playBtn) playBtn.disabled = false;
    runBtn.disabled = false;
    renderStep(0);
    updateComplexityLive();
    if (challenge.on && challengeSupported()) challengeBegin();
  }

  function renderGraphStep(step, idx) {
    const s = step.structures || {};
    const visited = new Set(s.visited || []);
    const activeNode = step.node || step.highlight?.node;
    const e = step.edge || step.highlight?.edge;
    const activeEdgeKey = e
      ? edgeKey(Array.isArray(e) ? e[0] : e.source, Array.isArray(e) ? e[1] : e.target)
      : null;

    // Edges traversed so far — replayed from history so backward scrubbing works
    const traversed = new Set();
    for (let k = 0; k < idx; k++) {
      const pe = currentSteps[k].highlight?.edge;
      if (pe) traversed.add(edgeKey(pe[0], pe[1]));
    }

    userGraph.nodes.forEach(n => {
      const el = svg.querySelector(`#node-${n.id}`);
      if (!el) return;
      el.classList.remove('active', 'visited');
      if (n.id === activeNode) el.classList.add('active');
      else if (visited.has(n.id)) el.classList.add('visited');
    });
    // Edges chosen for the spanning tree stay lit for the rest of the trace
    const mstKeys = new Set((s.mst_edges || []).map(e => edgeKey(e[0], e[1])));

    userGraph.links.forEach(l => {
      const el = svg.querySelector(`#edge-${l.source}-${l.target}`);
      if (!el) return;
      el.classList.remove('active', 'visited');
      el.style.stroke = '';
      el.style.strokeWidth = '';
      const k = edgeKey(l.source, l.target);
      if (mstKeys.has(k)) {
        el.style.stroke = '#4ade80';
        el.style.strokeWidth = '3';
      } else if (k === activeEdgeKey) {
        el.classList.add('active');
      } else if (traversed.has(k)) {
        el.classList.add('visited');
      }
    });

    // Running MST cost readout
    svg.querySelector('#mst-total')?.remove();
    if (s.total_weight !== null && s.total_weight !== undefined) {
      const t = makeSVG('text');
      t.setAttribute('x', '750'); t.setAttribute('y', '270');
      t.setAttribute('text-anchor', 'end');
      t.setAttribute('id', 'mst-total');
      t.setAttribute('fill', '#4ade80');
      t.setAttribute('font-family', 'var(--font-mono)');
      t.setAttribute('font-size', '13');
      t.textContent = `TREE COST: ${fmt(s.total_weight)}`;
      svg.appendChild(t);
    }

    const dist = s.dist;
    const isLast = idx === currentSteps.length - 1;
    userGraph.nodes.forEach(n => {
      const el = svg.querySelector(`#dist-${n.id}`);
      if (!el) return;
      if (!dist) { el.textContent = ''; return; }
      const v = dist[n.id];
      const unreached = v === null || v === undefined || v === Infinity;
      el.textContent = unreached ? (isLast ? '—' : '∞') : fmt(v);
    });
  }

  function renderCounters(step) {
    if (!counterPanel) return;
    const counts = step.structures?.counts;
    counterPanel.innerHTML = counts ? countChips(counts) : '';
  }

  function renderStep(i) {
    if (!currentSteps.length) return;
    currentStepIdx = Math.max(0, Math.min(i, currentSteps.length - 1));
    const step = currentSteps[currentStepIdx];
    const isLast = currentStepIdx === currentSteps.length - 1;

    if (traceView === 'array') renderArrayStep(step);
    else if (traceView === 'table') renderTableStep(step);
    else if (traceView === 'list') renderListStep(step);
    else if (traceView === 'stack') renderStackStep(step);
    else if (traceView === 'tree') renderTreeStep(step);
    else if (traceView === 'grid') renderGridStep(step);
    else renderGraphStep(step, currentStepIdx);

    let narration = step.note || "Processing...";
    if (currentScene && currentMeta) {
      narration = currentScene.stepNarrate(step, currentMeta);
    }
    if (isLast && traceSummary) narration = `${narration} ${traceSummary}`;
    note.textContent = narration.toUpperCase();
    note.style.opacity = 1;

    renderCounters(step);

    if (stepSlider) stepSlider.value = currentStepIdx;
    const counter = view.querySelector('#step-counter');
    if (counter) counter.textContent = `STEP ${currentStepIdx + 1} / ${currentSteps.length}`;
    if (prevBtn) prevBtn.disabled = challenge.active || currentStepIdx === 0;
    stepBtn.disabled = challenge.active || isLast;
    if (playBtn && challenge.active) playBtn.disabled = true;
    if (isLast) stopPlay();
    status.innerHTML = isLast
      ? 'STATUS: <span style="color:var(--cBright)">DONE</span>'
      : 'STATUS: <span style="color:var(--c)">STEPPING</span>';
    status.className = isLast ? 'engine-status-pill done' : 'engine-status-pill running';
  }

  function stopPlay() {
    if (playTimer) { clearInterval(playTimer); playTimer = null; }
    if (playBtn) { playBtn.classList.remove('is-playing'); playBtn.setAttribute('aria-label', 'Play'); }
  }

  function startPlay() {
    if (!currentSteps.length) return;
    if (currentStepIdx >= currentSteps.length - 1) renderStep(0);
    stopPlay();
    const speed = Number(speedSelect?.value || 1);
    playTimer = setInterval(() => {
      if (currentStepIdx >= currentSteps.length - 1) { stopPlay(); return; }
      renderStep(currentStepIdx + 1);
    }, 900 / speed);
    if (playBtn) { playBtn.classList.add('is-playing'); playBtn.setAttribute('aria-label', 'Pause'); }
  }

  function initComplexityCard() {
    const card = DATA.COMPLEXITY?.[algoId];
    const cardEl = view.querySelector('#complexity-card');
    const rowsEl = view.querySelector('#complexity-rows');
    if (!card || !cardEl || !rowsEl) return;
    rowsEl.innerHTML = card.rows.map(([k, v]) =>
      `<div><div style="font-family:var(--font-ui); font-size:0.72rem; color:var(--cDim);
        margin-bottom:0.3rem;">${k.toUpperCase()}</div>
        <div style="color:var(--cBright);">${v}</div></div>`
    ).join('');
    cardEl.classList.remove('is-hidden');
  }

  function updateComplexityLive() {
    const card = DATA.COMPLEXITY?.[algoId];
    const liveEl = view.querySelector('#complexity-live');
    if (!card || !liveEl || !currentSteps.length) return;
    const counts = currentSteps[currentSteps.length - 1]?.structures?.counts;
    if (!counts) return;
    const sizes = traceView === 'graph'
      ? { V: userGraph.nodes.length, E: userGraph.links.length, n: userGraph.nodes.length }
      : traceView === 'table'
        ? { n: currentTableN, V: 0, E: 0 }
        : traceView === 'list'
          ? { n: currentListValues.length, V: 0, E: 0 }
          : traceView === 'stack'
            ? { n: currentStackText.length, V: 0, E: 0 }
            : { n: currentArrayValues.length, V: 0, E: 0 };
    liveEl.textContent = card.reading(counts, sizes);
    liveEl.style.display = 'block';
  }

  // ── Compare mode: BFS vs Dijkstra on the same graph ──

  function renderMiniGraph(svgEl, steps, idx) {
    if (!svgEl) return;
    svgEl.innerHTML = '';
    const i2 = Math.min(idx, steps.length - 1);
    const s = steps[i2].structures || {};
    const visited = new Set(s.visited || []);
    const activeNode = steps[i2].highlight?.node;
    const ae = steps[i2].highlight?.edge;
    const activeKey = ae ? edgeKey(ae[0], ae[1]) : null;
    const traversed = new Set();
    for (let k = 0; k < i2; k++) {
      const pe = steps[k].highlight?.edge;
      if (pe) traversed.add(edgeKey(pe[0], pe[1]));
    }

    userGraph.links.forEach(l => {
      const a = userGraph.nodes.find(n => n.id === l.source);
      const b = userGraph.nodes.find(n => n.id === l.target);
      if (!a || !b) return;
      const line = makeSVG('line');
      line.setAttribute('x1', a.x); line.setAttribute('y1', a.y);
      line.setAttribute('x2', b.x); line.setAttribute('y2', b.y);
      const k = edgeKey(l.source, l.target);
      line.setAttribute('stroke', k === activeKey
        ? 'var(--c)' : traversed.has(k) ? 'rgba(212, 96, 44,0.35)' : 'rgba(0,150,184,0.2)');
      line.setAttribute('stroke-width', k === activeKey ? '2.5' : '1.5');
      svgEl.appendChild(line);
    });
    userGraph.nodes.forEach(n => {
      const c = makeSVG('circle');
      c.setAttribute('cx', n.x); c.setAttribute('cy', n.y); c.setAttribute('r', '18');
      c.setAttribute('fill', n.id === activeNode
        ? 'var(--c)' : visited.has(n.id) ? 'rgba(0,80,100,0.5)' : 'var(--cDeep)');
      c.setAttribute('stroke', n.id === activeNode ? 'var(--cBright)' : 'var(--cDim)');
      svgEl.appendChild(c);
      const t = makeSVG('text');
      t.setAttribute('x', n.x); t.setAttribute('y', n.y + 4);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('fill', 'var(--cBright)');
      t.setAttribute('font-family', 'var(--font-ui)');
      t.setAttribute('font-size', '8');
      t.textContent = n.id;
      svgEl.appendChild(t);
      if (s.dist) {
        const d = makeSVG('text');
        d.setAttribute('x', n.x); d.setAttribute('y', n.y + 34);
        d.setAttribute('text-anchor', 'middle');
        d.setAttribute('fill', 'var(--c)');
        d.setAttribute('font-family', 'var(--font-mono)');
        d.setAttribute('font-size', '10');
        const v = s.dist[n.id];
        d.textContent = (v === null || v === undefined) ? '∞' : fmt(v);
        svgEl.appendChild(d);
      }
    });
  }

  function renderCompareStep(i) {
    if (!compareData) return;
    const maxIdx = Math.max(compareData.a.steps.length, compareData.b.steps.length) - 1;
    compareIdx = Math.max(0, Math.min(i, maxIdx));
    ['a', 'b'].forEach(side => {
      const steps = compareData[side].steps;
      const i2 = Math.min(compareIdx, steps.length - 1);
      renderMiniGraph(view.querySelector(`#compare-svg-${side}`), steps, compareIdx);
      const noteEl = view.querySelector(`#compare-note-${side}`);
      if (noteEl) {
        const done = compareIdx > steps.length - 1;
        noteEl.textContent = (steps[i2].note || '') + (done ? ' — FINISHED' : '');
      }
      const cEl = view.querySelector(`#compare-counts-${side}`);
      if (cEl) cEl.innerHTML = countChips(steps[i2].structures?.counts, true);
    });
    if (compareSlider) compareSlider.value = compareIdx;
    const label = view.querySelector('#compare-step-label');
    if (label) label.textContent = `STEP ${compareIdx + 1} / ${maxIdx + 1}`;
    if (compareIdx >= maxIdx) stopComparePlay();
  }

  function stopComparePlay() {
    if (comparePlayTimer) { clearInterval(comparePlayTimer); comparePlayTimer = null; }
    const b = view.querySelector('#compare-play');
    if (b) b.textContent = '▶';
  }

  function startComparePlay() {
    if (!compareData) return;
    const maxIdx = Math.max(compareData.a.steps.length, compareData.b.steps.length) - 1;
    if (compareIdx >= maxIdx) renderCompareStep(0);
    stopComparePlay();
    comparePlayTimer = setInterval(() => {
      const m = Math.max(compareData.a.steps.length, compareData.b.steps.length) - 1;
      if (compareIdx >= m) { stopComparePlay(); return; }
      renderCompareStep(compareIdx + 1);
    }, 700);
    const b = view.querySelector('#compare-play');
    if (b) b.textContent = '⏸';
  }

  function closeCompare() {
    stopComparePlay();
    if (comparePanel) comparePanel.classList.add('is-hidden');
    const mainPanel = view.querySelector('#engine-panel');
    if (mainPanel) mainPanel.classList.remove('is-hidden');
    if (compareBtn) compareBtn.textContent = '⚖ COMPARE';
    compareData = null;
  }

  async function toggleCompare() {
    if (comparePanel && !comparePanel.classList.contains('is-hidden')) {
      closeCompare();
      return;
    }
    if (!userGraph.nodes.length) {
      showGraphError('Add some nodes first — the comparison needs a graph.');
      return;
    }
    compareBtn.disabled = true;
    compareBtn.textContent = 'LOADING...';
    try {
      await loadComparePair();
      if (comparePanel) comparePanel.classList.remove('is-hidden');
      const mainPanel = view.querySelector('#engine-panel');
      if (mainPanel) mainPanel.classList.add('is-hidden');
      compareBtn.textContent = '✕ CLOSE COMPARE';
    } catch (e) {
      console.error(e);
      showGraphError('Could not load the comparison traces.');
    } finally {
      compareBtn.disabled = false;
    }
  }

  // Runs whichever two graph algorithms the dropdowns name, on the same graph.
  async function loadComparePair() {
    const pickA = view.querySelector('#compare-pick-a');
    const pickB = view.querySelector('#compare-pick-b');
    const idA = pickA?.value || 'bfs';
    const idB = pickB?.value || 'dijkstra';

    const get = async (alg) => {
      if (isOffline) return localTrace(alg, startNodeId).steps;
      const graph = {
        nodes: userGraph.nodes,
        edges: userGraph.links.map(l => [l.source, l.target, l.weight]),
      };
      return (await api.postTrace(alg, { start: startNodeId, graph })).steps;
    };

    const [sa, sb] = await Promise.all([get(idA), get(idB)]);
    compareData = { a: { id: idA, steps: sa }, b: { id: idB, steps: sb } };

    const nameOf = (id) =>
      DATA.ALGORITHMS.find(x => x.id === id)?.name || id.toUpperCase();
    const totA = view.querySelector('#compare-total-a');
    const totB = view.querySelector('#compare-total-b');
    if (totA) totA.textContent = `· ${sa.length} STEPS`;
    if (totB) totB.textContent = `· ${sb.length} STEPS`;

    const ca = sa[sa.length - 1]?.structures?.counts || {};
    const cb = sb[sb.length - 1]?.structures?.counts || {};
    const summarise = (id, steps, c) => {
      const bits = Object.entries(c)
        .map(([k, v]) => `${v} ${(COUNT_LABELS[k] || k).toLowerCase()}`);
      return `${nameOf(id)}: ${steps.length} steps` +
        (bits.length ? ` (${bits.join(', ')})` : '');
    };
    const verdict = view.querySelector('#compare-verdict');
    if (verdict) {
      let text = `Same graph, same start (${startNodeId}). ` +
        `${summarise(idA, sa, ca)}. ${summarise(idB, sb, cb)}.`;
      const mstA = sa[sa.length - 1]?.structures?.total_weight;
      const mstB = sb[sb.length - 1]?.structures?.total_weight;
      if (mstA !== undefined && mstB !== undefined && mstA !== null && mstB !== null) {
        text += mstA === mstB
          ? ` Both build a spanning tree costing ${fmt(mstA)} — different routes, identical minimum.`
          : ` Tree costs differ: ${fmt(mstA)} vs ${fmt(mstB)}.`;
      }
      verdict.textContent = text;
    }
    if (compareSlider) compareSlider.max = Math.max(sa.length, sb.length) - 1;
    renderCompareStep(0);
  }

  async function explain() {
    if (currentStepIdx < 0 || currentStepIdx >= currentSteps.length) return;
    explainBtn.disabled = true;
    explanationBox.classList.remove('is-hidden');
    explanationBox.textContent = "CONSULTING AI NARRATOR...";

    try {
      const step = currentSteps[currentStepIdx];
      let res;
      if (isOffline) {
        const narration = currentScene?.stepNarrate(step, currentMeta || {}) || step.note;
        res = { text: `[OFFLINE] ${narration}` };
      } else {
        const level = view.querySelector('#level-select')?.value || 'beginner';
        res = await api.explainStep(algoId, step, level, currentMeta || {});
      }
      explanationBox.textContent = (res.text || "NO DATA AVAILABLE.").toUpperCase();
    } catch {
      explanationBox.textContent = "AI NARRATOR TIMEOUT. CHECK CONSOLE.";
    } finally {
      explainBtn.disabled = false;
    }
  }

  // ── Wire up controls ──
  runBtn.addEventListener('click', run);
  stepBtn.addEventListener('click', () => { stopPlay(); renderStep(currentStepIdx + 1); });
  prevBtn?.addEventListener('click', () => { stopPlay(); renderStep(currentStepIdx - 1); });
  playBtn?.addEventListener('click', () => playTimer ? stopPlay() : startPlay());
  speedSelect?.addEventListener('change', () => { if (playTimer) startPlay(); });
  stepSlider?.addEventListener('input', () => { stopPlay(); renderStep(Number(stepSlider.value)); });
  resetBtn.addEventListener('click', () => {
    resetTraceState();
    if (traceView === 'array') {
      renderArrayView(currentArrayValues);
    } else if (traceView === 'table') {
      renderTableView(currentTableN);
    } else if (traceView === 'list') {
      renderListView(currentListValues);
    } else if (traceView === 'stack') {
      renderStackView(currentStackText);
    } else if (traceView === 'tree') {
      renderTreeView();
    } else if (traceView === 'grid') {
      renderGridView();
    } else {
      renderGraph(currentMeta);
    }
  });
  explainBtn.addEventListener('click', explain);
  if (traceView === 'graph') {
    compareBtn?.addEventListener('click', toggleCompare);
    view.querySelector('#compare-prev')?.addEventListener('click', () => { stopComparePlay(); renderCompareStep(compareIdx - 1); });
    view.querySelector('#compare-next')?.addEventListener('click', () => { stopComparePlay(); renderCompareStep(compareIdx + 1); });
    view.querySelector('#compare-play')?.addEventListener('click', () => comparePlayTimer ? stopComparePlay() : startComparePlay());
    compareSlider?.addEventListener('input', () => { stopComparePlay(); renderCompareStep(Number(compareSlider.value)); });
    // Changing either dropdown re-runs the pair on the same graph
    ['#compare-pick-a', '#compare-pick-b'].forEach(sel => {
      view.querySelector(sel)?.addEventListener('change', async () => {
        stopComparePlay();
        try { await loadComparePair(); }
        catch (e) { console.error(e); showGraphError('Could not load that comparison.'); }
      });
    });
  }

  // ── Init ──
  // Try to get realworld meta from backend detect endpoint
  async function init() {
    try {
      const detection = await api.detect("", algoId);
      currentMeta = detection.realworld;
      // Update page title/hook
      const hookEl = view.querySelector('#scene-hook');
      if (hookEl && currentMeta?.hook) {
        hookEl.textContent = currentMeta.hook;
        hookEl.style.display = 'block';
      }
    } catch {
      // Use offline meta
      currentMeta = {
        scene: resolveScene(algoId),
        metaphors: { node: 'node', visit: 'Visiting', done: 'Complete.' }
      };
    }

    if (traceView !== 'graph') {
      const defaults = ARRAY_DEFAULTS[algoId] || ARRAY_DEFAULTS.merge_sort;
      if (arrayControls) arrayControls.classList.remove('is-hidden');
      const numberOnly = !!NUMBER_ONLY[algoId];
      if (traceView === 'table' || numberOnly) {
        // These take a single number, not an array
        if (arrayInput) arrayInput.style.display = 'none';
        const targetLabel = view.querySelector('#target-label');
        if (targetLabel) targetLabel.textContent = NUMBER_ONLY[algoId]?.[2] || 'N =';
      } else if (arrayInput && !arrayInput.value) {
        arrayInput.value = defaults.array;
      }
      const wantsTarget = ['binary_search', 'bst_search', 'two_sum_sorted',
        'sliding_window', 'knapsack_01', 'floyd_cycle',
        'unique_paths', 'flood_fill', 'segment_tree', 'fenwick_tree',
        'bst_delete', 'coin_change', 'subset_sum'].includes(algoId)
        || numberOnly || traceView === 'table';
      if (wantsTarget && targetWrap) {
        targetWrap.style.display = 'inline-flex';
        if (targetInput && !targetInput.value) targetInput.value = defaults.target;
        const targetLabel = view.querySelector('#target-label');
        if (targetLabel && algoId === 'sliding_window') targetLabel.textContent = 'K =';
        if (targetLabel && algoId === 'knapsack_01') targetLabel.textContent = 'CAP =';
        if (targetLabel && algoId === 'floyd_cycle') targetLabel.textContent = 'LOOPS TO =';
        if (targetLabel && algoId === 'unique_paths') targetLabel.textContent = 'GRID =';
        if (targetLabel && algoId === 'flood_fill') targetLabel.textContent = 'GRID =';
        if (targetLabel && algoId === 'segment_tree') targetLabel.textContent = 'RANGE =';
        if (targetLabel && algoId === 'fenwick_tree') targetLabel.textContent = 'UP TO =';
        if (targetLabel && algoId === 'bst_delete') targetLabel.textContent = 'DELETE =';
        if (targetLabel && algoId === 'coin_change') targetLabel.textContent = 'AMOUNT =';
        if (targetLabel && algoId === 'subset_sum') targetLabel.textContent = 'SUM =';
      }
      if (arrayHint) arrayHint.textContent = defaults.hint;
      // What-If sliders only make sense for graphs — hide the whole section.
      const whatIfDetails = view.querySelector('#whatif-controls')?.closest('details');
      if (whatIfDetails) whatIfDetails.style.display = 'none';
      const parsed = parseArrayInput();
      if (traceView === 'table') renderTableView(parsed.target ?? 10);
      else if (algoId === 'kmp_search') renderArrayView(parsed.chars || []);
      else if (algoId === 'sieve') {
        renderArrayView(Array.from({ length: (parsed.target ?? 30) + 1 }, (_, i) => i));
      } else if (traceView === 'list') renderListView(parsed.array || []);
      else if (traceView === 'stack') renderStackView(parsed.text || '');
      else if (traceView === 'tree') renderTreeView();
      else if (traceView === 'grid') renderGridView();
      else renderArrayView(parsed.array || []);
      checkBackend();
      initComplexityCard();
      return;
    }

    if (graphControls) graphControls.classList.remove('is-hidden');
    if (compareBtn) compareBtn.classList.remove('is-hidden');
    updateGraphMeta();
    attachGraphEditor();
    renderGraph(currentMeta);
    checkBackend();
    buildWhatIfSliders();
    initComplexityCard();
  }

  init();
}

// ── BUG FINDER ENGINE ────────────────────────────────────────────────────────

export function mountBugFinder(view) {
  const btn = view.querySelector('#find-bug-btn');
  const codeArea = view.querySelector('#code-area');
  const langSelect = view.querySelector('#lang-select');
  const result = view.querySelector('#bug-result');
  const detectResult = view.querySelector('#detect-result');

  const DEFAULT_CODE = `def binary_search(arr, target):
    low = 0
    high = len(arr)  # BUG: should be len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid  # BUG: should be mid - 1
    return -1`;

  codeArea.value = DEFAULT_CODE;

  // Live detection as user types
  let detectTimer = null;
  codeArea.addEventListener('input', () => {
    clearTimeout(detectTimer);
    detectTimer = setTimeout(async () => {
      if (codeArea.value.length < 20) return;
      try {
        const res = await api.detect(codeArea.value);
        if (detectResult) {
          detectResult.style.display = 'block';
          const conf = Math.round(res.confidence * 100);
          detectResult.innerHTML = `DETECTED: <span style="color:var(--cBright)">${res.algorithm.toUpperCase().replace('_',' ')}</span> (${conf}% confidence) — <span style="color:var(--cDim)">${res.realworld?.title || ''}</span>  <a href="#/experience?algo=${res.algorithm}" style="color:var(--c);font-family:var(--font-ui);font-size:0.75rem;margin-left:1rem;">VISUALIZE →</a>`;
        }
      } catch { /* silent */ }
    }, 600);
  });

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    result.style.display = 'block';
    result.textContent = "SCANNING CODE...";

    try {
      const res = await api.bugFind(langSelect.value, codeArea.value);
      const hints = res.hints || ["No obvious bug found."];
      result.innerHTML = `<strong style="color:var(--cBright)">AI BUG SCAN:</strong><br><br>${hints.map(h => `<span style="color:var(--cDim)">▸</span> ${escapeHTML(h)}`).join('<br><br>')}${res.fallback ? '<br><br><small style="opacity:0.5">(OFFLINE FALLBACK)</small>' : ''}`;
    } catch {
      result.innerHTML = `<strong>ANALYSIS:</strong> Check loop boundaries and off-by-one errors.<br><small>(LOCAL FALLBACK)</small>`;
    } finally {
      btn.disabled = false;
    }
  });
}
