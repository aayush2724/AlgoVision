import { api } from './api.js';
import * as DATA from './data.js';

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
  dijkstra: 'graph', bfs: 'graph',
  binary_search: 'array', merge_sort: 'array',
};

function resolveAlgoId(raw) {
  const key = String(raw || '').toLowerCase().replace(/[\s-]/g, '');
  const MAP = [
    ['binary_search', 'binary_search'], ['binarysearch', 'binary_search'],
    ['thehunt', 'binary_search'], ['library', 'binary_search'],
    ['merge_sort', 'merge_sort'], ['mergesort', 'merge_sort'],
    ['quick_sort', 'merge_sort'], ['sorting', 'merge_sort'], ['leaderboard', 'merge_sort'],
    ['sixdegrees', 'bfs'], ['social', 'bfs'], ['graphs', 'bfs'], ['graph', 'bfs'],
    ['bfs', 'bfs'], ['dfs', 'bfs'],
    ['gps', 'dijkstra'], ['dijkstra', 'dijkstra'],
  ];
  for (const [k, v] of MAP) if (key.includes(k)) return v;
  return 'dijkstra';
}

const fmt = (v) => String(Number(v));

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

  const algoId = resolveAlgoId(algo);
  const traceView = VIEW_FOR[algoId] || 'graph';

  let currentSteps = [];
  let currentStepIdx = -1;
  let isOffline = false;
  let currentMeta = null;  // stores realworld_meta for current algo
  let currentScene = null; // stores scene renderer
  let currentArrayValues = [];

  // ── Set scene based on algo name ──
  function resolveScene(algoName) {
    const map = {
      dijkstra: 'gps', bfs: 'social', dfs: 'maze',
      binary_search: 'library', merge_sort: 'leaderboard',
      dynamic_programming: 'vault', quick_sort: 'leaderboard',
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
    if (scene.renderBase) scene.renderBase(svg, DATA.SAMPLE_GRAPH, meta);

    // Draw edges
    DATA.SAMPLE_GRAPH.links.forEach(link => {
      const source = DATA.SAMPLE_GRAPH.nodes.find(n => n.id === link.source);
      const target = DATA.SAMPLE_GRAPH.nodes.find(n => n.id === link.target);

      const line = makeSVG("line");
      line.setAttribute("x1", source.x); line.setAttribute("y1", source.y);
      line.setAttribute("x2", target.x); line.setAttribute("y2", target.y);
      line.setAttribute("class", "edge");
      line.setAttribute("id", `edge-${link.source}-${link.target}`);
      svg.appendChild(line);

      // Edge weight label
      const tx = makeSVG("text");
      tx.setAttribute("x", (source.x + target.x) / 2);
      tx.setAttribute("y", (source.y + target.y) / 2 - 6);
      tx.setAttribute("fill", "var(--cDim)");
      tx.setAttribute("font-family", "var(--font-mono)");
      tx.setAttribute("font-size", "11");
      tx.setAttribute("text-anchor", "middle");
      tx.textContent = scene.edgeLabel(link.weight);
      svg.appendChild(tx);
    });

    // Draw nodes
    DATA.SAMPLE_GRAPH.nodes.forEach(node => {
      const circle = makeSVG("circle");
      circle.setAttribute("cx", node.x); circle.setAttribute("cy", node.y);
      circle.setAttribute("r", "22");
      circle.setAttribute("class", "node");
      circle.setAttribute("id", `node-${node.id}`);
      svg.appendChild(circle);

      // Node ID label
      const idText = makeSVG("text");
      idText.setAttribute("x", node.x); idText.setAttribute("y", node.y + 4);
      idText.setAttribute("text-anchor", "middle");
      idText.setAttribute("fill", "var(--cBright)");
      idText.setAttribute("font-family", "var(--font-pixel)");
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

      // Full location name below node (for GPS scene)
      if (node.label && currentMeta?.scene === 'gps') {
        const nameText = makeSVG("text");
        nameText.setAttribute("x", node.x);
        nameText.setAttribute("y", node.y + 38);
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
    sceneLabel.setAttribute("font-family", "var(--font-pixel)");
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
    sceneLabel.setAttribute("font-family", "var(--font-pixel)");
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
      rect.setAttribute("fill", "rgba(0,212,255,0.05)");
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
      val.textContent = fmt(v);
      g.appendChild(val);

      const pos = makeSVG("text");
      pos.setAttribute("x", x0 + idx * w + w / 2);
      pos.setAttribute("y", y + h + 16);
      pos.setAttribute("text-anchor", "middle");
      pos.setAttribute("fill", "var(--cDim)");
      pos.setAttribute("font-family", "var(--font-pixel)");
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
        if (el) el.textContent = fmt(v);
      });
    }
    for (let idx = 0; idx < currentArrayValues.length; idx++) {
      const cell = svg.querySelector(`#cell-${idx}`);
      const g = svg.querySelector(`#cellg-${idx}`);
      if (!cell) continue;
      cell.setAttribute("fill", "rgba(0,212,255,0.05)");
      cell.setAttribute("stroke", "var(--cDim)");
      cell.setAttribute("stroke-width", "1");
      if (g) g.setAttribute("opacity", "1");

      if (algoId === 'binary_search') {
        const inRange = s.low != null && idx >= s.low && idx <= s.high;
        if (!inRange && g) g.setAttribute("opacity", "0.22");
        if (inRange) cell.setAttribute("stroke", "var(--c)");
        if (idx === s.mid) {
          cell.setAttribute("fill", "rgba(255,107,0,0.18)");
          cell.setAttribute("stroke", s.found ? "#4ade80" : "var(--cAccent)");
          cell.setAttribute("stroke-width", "2");
        }
      } else {
        const inSorted = (s.sorted_ranges || []).some(r => idx >= r[0] && idx <= r[1]);
        if (inSorted) cell.setAttribute("stroke", "#4ade80");
        if (s.merging && idx >= s.merging[0] && idx <= s.merging[1] && !inSorted) {
          cell.setAttribute("stroke", "var(--c)");
        }
        if (idx === s.placed) {
          cell.setAttribute("fill", "rgba(255,107,0,0.18)");
          cell.setAttribute("stroke", "var(--cAccent)");
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
  };

  function parseArrayInput() {
    const raw = (arrayInput?.value || '').trim();
    const parts = raw.split(/[\s,;]+/).filter(Boolean);
    if (!parts.length) return { error: 'Enter some numbers first — e.g. 7, 3, 9, 1' };
    const values = parts.map(Number);
    if (values.some(v => !Number.isFinite(v))) return { error: 'Only numbers, separated by commas.' };
    if (values.some(v => Math.abs(v) > 1_000_000)) return { error: 'Keep values within ±1,000,000.' };
    const maxLen = algoId === 'merge_sort' ? 16 : 20;
    if (values.length > maxLen) return { error: `Max ${maxLen} values for this algorithm.` };

    if (algoId === 'binary_search') {
      const t = Number((targetInput?.value || '').trim());
      if (!Number.isFinite(t)) return { error: 'Enter a numeric target to search for.' };
      const sorted = values.slice().sort((a, b) => a - b);
      const sortedForYou = sorted.some((v, i) => v !== values[i]);
      return { array: sorted, target: t, sortedForYou };
    }
    return { array: values };
  }

  // Offline emulator for the array algorithms — mirrors the backend step shapes.
  function localArrayTrace(parsed) {
    if (algoId === 'binary_search') {
      const arr = parsed.array, target = parsed.target;
      const steps = [];
      let low = 0, high = arr.length - 1, found = false;
      steps.push({ i: 0, structures: { low, high, mid: null, found: null },
        highlight: { index: null },
        note: arr.length
          ? `Search ${arr.length} sorted values for target ${fmt(target)}.`
          : 'The array is empty — nothing to search.' });
      while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        steps.push({ i: steps.length, structures: { low, high, mid, found: null },
          highlight: { index: mid },
          note: `Check the middle: position ${mid} holds ${fmt(arr[mid])}.` });
        if (arr[mid] === target) {
          found = true;
          steps.push({ i: steps.length, structures: { low, high, mid, found: true },
            highlight: { index: mid },
            note: `Found it — ${fmt(target)} is at position ${mid}.` });
          break;
        } else if (arr[mid] < target) {
          low = mid + 1;
          steps.push({ i: steps.length, structures: { low, high, mid, found: null },
            highlight: { index: mid },
            note: `${fmt(arr[mid])} is smaller — search the right half.` });
        } else {
          high = mid - 1;
          steps.push({ i: steps.length, structures: { low, high, mid, found: null },
            highlight: { index: mid },
            note: `${fmt(arr[mid])} is larger — search the left half.` });
        }
      }
      if (!found) {
        steps.push({ i: steps.length, structures: { low, high, mid: null, found: false },
          highlight: { index: null },
          note: `The range is empty — ${fmt(target)} is not in the array.` });
      }
      return { steps };
    }

    // merge_sort
    const arr = parsed.array.slice();
    const steps = [];
    const sortedRanges = [];
    const snap = (note, extra = {}) => steps.push({
      i: steps.length,
      structures: { array: arr.slice(), merging: null, comparing: null, placed: null,
        sorted_ranges: sortedRanges.map(r => r.slice()), ...extra },
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
        commit();
        snap(`Compare ${fmt(a)} vs ${fmt(b)} — place ${fmt(merged[merged.length - 1])}.`,
          { merging: [lo, hi - 1], comparing: [a, b], placed: lo + merged.length - 1 });
      }
      while (i < left.length) {
        merged.push(left[i++]); commit();
        snap(`Copy remaining ${fmt(merged[merged.length - 1])}.`,
          { merging: [lo, hi - 1], placed: lo + merged.length - 1 });
      }
      while (j < right.length) {
        merged.push(right[j++]); commit();
        snap(`Copy remaining ${fmt(merged[merged.length - 1])}.`,
          { merging: [lo, hi - 1], placed: lo + merged.length - 1 });
      }
      for (let r = sortedRanges.length - 1; r >= 0; r--) {
        if (lo <= sortedRanges[r][0] && sortedRanges[r][1] <= hi - 1) sortedRanges.splice(r, 1);
      }
      sortedRanges.push([lo, hi - 1]);
      snap(`Positions ${lo}..${hi - 1} merged — this section is sorted.`, { merging: [lo, hi - 1] });
    };
    msort(0, arr.length);
    snap('Every section merged — the whole array is in order.');
    return { steps };
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
    // Local emulator for offline mode — Dijkstra and BFS
    const nodes = DATA.SAMPLE_GRAPH.nodes.map(n => n.id);
    const adj = {};
    DATA.SAMPLE_GRAPH.links.forEach(l => {
      if (!adj[l.source]) adj[l.source] = [];
      if (!adj[l.target]) adj[l.target] = [];
      adj[l.source].push({ to: l.target, w: l.weight });
      adj[l.target].push({ to: l.source, w: l.weight });
    });

    if (algorithm === 'bfs') {
      const steps = [];
      const visited = new Set([startNode]);
      const queue = [startNode];
      steps.push({ i: 0, highlight: { node: startNode, edge: null },
        note: `Enqueue start node ${startNode}.`,
        structures: { queue: [...queue], visited: [...visited] }
      });
      while (queue.length > 0) {
        const u = queue.shift();
        steps.push({ i: steps.length, highlight: { node: u, edge: null },
          note: `Dequeue ${u}.`,
          structures: { queue: [...queue], visited: [...visited] }
        });
        for (const edge of (adj[u] || [])) {
          if (visited.has(edge.to)) continue;
          visited.add(edge.to);
          queue.push(edge.to);
          steps.push({ i: steps.length, highlight: { node: edge.to, edge: [u, edge.to] },
            note: `Discover ${edge.to} from ${u}.`,
            structures: { queue: [...queue], visited: [...visited] }
          });
        }
      }
      return { steps };
    }

    const dist = {};
    const steps = [];
    nodes.forEach(n => dist[n] = Infinity);
    dist[startNode] = 0;
    const pq = [{ node: startNode, d: 0 }];
    const visited = new Set();

    steps.push({ i: 0, highlight: { node: startNode, edge: null },
      note: `Start at ${startNode} with distance 0.`,
      structures: { dist: { ...dist }, visited: [] }
    });

    while (pq.length > 0) {
      pq.sort((a, b) => a.d - b.d);
      const { node, d } = pq.shift();
      if (visited.has(node)) continue;
      visited.add(node);
      steps.push({ i: steps.length, highlight: { node, edge: null },
        note: `Visit ${node} (distance ${d}).`,
        structures: { dist: { ...dist }, visited: [...visited] }
      });
      for (const edge of (adj[node] || [])) {
        if (visited.has(edge.to)) continue;
        const nd = d + edge.w;
        if (nd < dist[edge.to]) {
          dist[edge.to] = nd;
          pq.push({ node: edge.to, d: nd });
          steps.push({ i: steps.length, highlight: { node: edge.to, edge: [node, edge.to] },
            note: `Relax edge ${node}→${edge.to}: new distance ${nd}.`,
            structures: { dist: { ...dist }, visited: [...visited] }
          });
        }
      }
    }
    return { steps };
  }

  async function run() {
    runBtn.disabled = true;
    explanationBox.style.display = 'none';
    status.innerHTML = 'STATUS: <span style="color:var(--c)">TRACING...</span>';
    status.className = 'eyebrow running';

    try {
      let res;
      if (traceView === 'array') {
        const parsed = parseArrayInput();
        if (parsed.error) {
          status.innerHTML = `STATUS: <span style="color:#ff5f5f">${escapeHTML(parsed.error).toUpperCase()}</span>`;
          status.className = 'eyebrow';
          runBtn.disabled = false;
          return;
        }
        if (parsed.sortedForYou && arrayHint) {
          arrayHint.textContent =
            'Heads up: your numbers were sorted first — binary search only works on sorted data.';
        }
        renderArrayView(parsed.array);
        if (isOffline) {
          res = localArrayTrace(parsed);
        } else {
          const payload = algoId === 'binary_search'
            ? { array: parsed.array, target: parsed.target }
            : { array: parsed.array };
          res = await api.postTrace(algoId, payload);
        }
      } else if (isOffline) {
        res = localTrace(algoId, 'A');
      } else {
        const graph = {
          nodes: DATA.SAMPLE_GRAPH.nodes,
          edges: DATA.SAMPLE_GRAPH.links.map(l => [l.source, l.target, l.weight])
        };
        res = await api.postTrace(algoId, { start: 'A', graph });
      }
      currentSteps = res.steps;
      currentStepIdx = -1;
      stepBtn.disabled = false;
      nextStep();
    } catch (e) {
      console.error(e);
      status.innerHTML = 'STATUS: <span style="color:#ff5f5f">TRACE FAILED</span>';
      runBtn.disabled = false;
      checkBackend();
    }
  }

  function nextStep() {
    currentStepIdx++;
    if (currentStepIdx >= currentSteps.length) {
      stepBtn.disabled = true;
      const lastStep = currentSteps[currentSteps.length - 1];
      const doneMsg = lastStep?.structures?.found === false
        ? 'Search complete — the target is not in this array.'
        : (currentMeta?.metaphors?.done || "ALGORITHM TRACE COMPLETE.");
      note.textContent = doneMsg.toUpperCase();
      status.innerHTML = 'STATUS: <span style="color:var(--cBright)">TERMINATED</span>';
      status.className = 'eyebrow done';
      runBtn.disabled = false;
      return;
    }

    const step = currentSteps[currentStepIdx];

    if (traceView === 'array') {
      renderArrayStep(step);
    } else {
      // Reset highlights, mark visited
      svg.querySelectorAll('.node.active').forEach(el => {
        el.classList.remove('active');
        el.classList.add('visited');
      });
      svg.querySelectorAll('.edge.active').forEach(el => {
        el.classList.remove('active');
        el.classList.add('visited');
      });

      const nodeId = step.node || step.highlight?.node;
      const edgeData = step.edge || step.highlight?.edge;

      if (nodeId) {
        const nodeEl = svg.querySelector(`#node-${nodeId}`);
        if (nodeEl) nodeEl.classList.add('active');
      }
      if (edgeData) {
        const s = Array.isArray(edgeData) ? edgeData[0] : edgeData.source;
        const t = Array.isArray(edgeData) ? edgeData[1] : edgeData.target;
        const edgeEl = svg.querySelector(`#edge-${s}-${t}`) || svg.querySelector(`#edge-${t}-${s}`);
        if (edgeEl) edgeEl.classList.add('active');
      }
    }

    // Use scene narrator for real-world note
    let narration = step.note || "Processing...";
    if (currentScene && currentMeta) {
      narration = currentScene.stepNarrate(step, currentMeta);
    }

    note.textContent = narration.toUpperCase();
    note.style.opacity = 1;

    // Update step counter
    const counter = view.querySelector('#step-counter');
    if (counter) counter.textContent = `STEP ${currentStepIdx + 1} / ${currentSteps.length}`;
  }

  async function explain() {
    if (currentStepIdx < 0 || currentStepIdx >= currentSteps.length) return;
    explainBtn.disabled = true;
    explanationBox.style.display = 'block';
    explanationBox.textContent = "CONSULTING AI NARRATOR...";

    try {
      const step = currentSteps[currentStepIdx];
      let res;
      if (isOffline) {
        const narration = currentScene?.stepNarrate(step, currentMeta || {}) || step.note;
        res = { text: `[OFFLINE] ${narration}` };
      } else {
        res = await api.explainStep(algoId, step, "beginner", currentMeta || {});
      }
      explanationBox.textContent = (res.text || "NO DATA AVAILABLE.").toUpperCase();
    } catch {
      explanationBox.textContent = "AI NARRATOR TIMEOUT. CHECK CONSOLE.";
    } finally {
      explainBtn.disabled = false;
    }
  }

  // ── Wire up buttons ──
  runBtn.addEventListener('click', run);
  stepBtn.addEventListener('click', nextStep);
  resetBtn.addEventListener('click', () => {
    currentStepIdx = -1;
    currentSteps = [];
    stepBtn.disabled = true;
    runBtn.disabled = false;
    note.style.opacity = 0;
    explanationBox.style.display = 'none';
    status.className = 'eyebrow';
    const counter = view.querySelector('#step-counter');
    if (counter) counter.textContent = '';
    if (traceView === 'array') {
      renderArrayView(currentArrayValues);
    } else {
      renderGraph(currentMeta);
    }
  });
  explainBtn.addEventListener('click', explain);

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

    if (traceView === 'array') {
      const defaults = ARRAY_DEFAULTS[algoId] || ARRAY_DEFAULTS.merge_sort;
      if (arrayControls) arrayControls.style.display = 'block';
      if (arrayInput && !arrayInput.value) arrayInput.value = defaults.array;
      if (algoId === 'binary_search' && targetWrap) {
        targetWrap.style.display = 'inline-flex';
        if (targetInput && !targetInput.value) targetInput.value = defaults.target;
      }
      if (arrayHint) arrayHint.textContent = defaults.hint;
      // What-If sliders only make sense for graphs — hide the whole section.
      const whatIfDetails = view.querySelector('#whatif-controls')?.closest('details');
      if (whatIfDetails) whatIfDetails.style.display = 'none';
      const parsed = parseArrayInput();
      renderArrayView(parsed.array || []);
      checkBackend();
      return;
    }

    renderGraph(currentMeta);
    checkBackend();

    // Build "What If" sliders for each edge weight
    const whatIfContainer = view.querySelector('#whatif-controls');
    if (whatIfContainer) {
      DATA.SAMPLE_GRAPH.links.forEach((link, idx) => {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex; align-items:center; gap:1rem; font-family:var(--font-mono); font-size:0.9rem; color:var(--cDim);';
        row.innerHTML = `
          <span style="min-width:120px;">${link.source}→${link.target}</span>
          <input type="range" min="1" max="30" value="${link.weight}"
            style="flex:1; accent-color:var(--c);"
            id="whatif-${idx}">
          <span id="whatif-val-${idx}" style="min-width:40px; color:var(--c);">${link.weight}</span>
        `;
        const slider = row.querySelector('input');
        const valLabel = row.querySelector(`#whatif-val-${idx}`);
        slider.addEventListener('input', () => {
          DATA.SAMPLE_GRAPH.links[idx].weight = parseInt(slider.value);
          valLabel.textContent = slider.value;
          renderGraph(currentMeta);
          // Reset trace
          currentStepIdx = -1;
          currentSteps = [];
          stepBtn.disabled = true;
          runBtn.disabled = false;
          note.style.opacity = 0;
        });
        whatIfContainer.appendChild(row);
      });
    }
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
          detectResult.innerHTML = `DETECTED: <span style="color:var(--cBright)">${res.algorithm.toUpperCase().replace('_',' ')}</span> (${conf}% confidence) — <span style="color:var(--cDim)">${res.realworld?.title || ''}</span>  <a href="#/experience?algo=${res.algorithm}" style="color:var(--c);font-family:var(--font-pixel);font-size:8px;margin-left:1rem;">VISUALIZE →</a>`;
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
