import { api } from './api.js';
import * as DATA from './data.js';

export function mountEngine(view, algo = 'dijkstra') {
  const svg = view.querySelector('#engine-svg');
  const status = view.querySelector('#engine-status');
  const note = view.querySelector('#engine-note');
  const runBtn = view.querySelector('#run-btn');
  const stepBtn = view.querySelector('#step-btn');
  const resetBtn = view.querySelector('#reset-btn');
  const explainBtn = view.querySelector('#explain-btn');
  const explanationBox = view.querySelector('#explanation-box');

  let currentSteps = [];
  let currentStepIdx = -1;
  let isOffline = false;

  function renderGraph() {
    svg.innerHTML = '';
    // Draw links
    DATA.SAMPLE_GRAPH.links.forEach(link => {
      const source = DATA.SAMPLE_GRAPH.nodes.find(n => n.id === link.source);
      const target = DATA.SAMPLE_GRAPH.nodes.find(n => n.id === link.target);
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", source.x);
      line.setAttribute("y1", source.y);
      line.setAttribute("x2", target.x);
      line.setAttribute("y2", target.y);
      line.setAttribute("class", "edge");
      line.setAttribute("id", `edge-${link.source}-${link.target}`);
      svg.appendChild(line);
      
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", (source.x + target.x) / 2);
      text.setAttribute("y", (source.y + target.y) / 2 - 5);
      text.setAttribute("fill", "var(--cDim)");
      text.setAttribute("font-size", "10");
      text.textContent = link.weight;
      svg.appendChild(text);
    });

    // Draw nodes
    DATA.SAMPLE_GRAPH.nodes.forEach(node => {
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", node.x);
      circle.setAttribute("cy", node.y);
      circle.setAttribute("r", "20");
      circle.setAttribute("class", "node");
      circle.setAttribute("id", `node-${node.id}`);
      svg.appendChild(circle);

      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", node.x);
      text.setAttribute("y", node.y + 4);
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("fill", "var(--cBright)");
      text.setAttribute("font-family", "var(--font-pixel)");
      text.setAttribute("font-size", "10");
      text.textContent = node.id;
      svg.appendChild(text);
    });
  }

  async function checkBackend() {
    try {
      await api.getAlgorithms();
      status.innerHTML = 'STATUS: <span style="color: var(--cBright)">CONNECTED</span>';
      isOffline = false;
    } catch (e) {
      status.innerHTML = 'STATUS: <span style="color: #ff5f5f">OFFLINE (EMULATOR ACTIVE)</span>';
      isOffline = true;
    }
  }

  function localTrace(algorithm, startNode) {
    // Basic Dijkstra emulator
    const nodes = DATA.SAMPLE_GRAPH.nodes.map(n => n.id);
    const adj = {};
    DATA.SAMPLE_GRAPH.links.forEach(l => {
      if (!adj[l.source]) adj[l.source] = [];
      if (!adj[l.target]) adj[l.target] = [];
      adj[l.source].push({ to: l.target, w: l.weight });
      adj[l.target].push({ to: l.source, w: l.weight });
    });

    const dist = {};
    const steps = [];
    nodes.forEach(n => dist[n] = Infinity);
    dist[startNode] = 0;
    
    const pq = [{ node: startNode, d: 0 }];
    
    while (pq.length > 0) {
      pq.sort((a, b) => a.d - b.d);
      const { node, d } = pq.shift();
      
      steps.push({ node, note: `VISITING NODE ${node} (DIST: ${d})` });

      if (d > dist[node]) continue;

      for (const edge of (adj[node] || [])) {
        if (dist[node] + edge.w < dist[edge.to]) {
          dist[edge.to] = dist[node] + edge.w;
          pq.push({ node: edge.to, d: dist[edge.to] });
          steps.push({ edge: { source: node, target: edge.to }, note: `FOUND SHORTER PATH TO ${edge.to} VIA ${node} (NEW DIST: ${dist[edge.to]})` });
        }
      }
    }
    return { steps };
  }

  async function run() {
    runBtn.disabled = true;
    explanationBox.style.display = 'none';
    status.innerHTML = 'STATUS: <span style="color: var(--c)">TRACING...</span>';
    
    try {
      let res;
      // Normalize algo name for backend
      const normalizedAlgo = algo.includes('sorting') ? 'dijkstra' : (algo.includes('graphs') ? 'bfs' : 'dijkstra');
      
      if (isOffline) {
        res = localTrace(normalizedAlgo, 'A');
      } else {
        const graph = {
          nodes: DATA.SAMPLE_GRAPH.nodes.map(n => n.id),
          edges: DATA.SAMPLE_GRAPH.links.map(l => [l.source, l.target, l.weight])
        };
        res = await api.postTrace(normalizedAlgo, 'A', graph);
      }
      currentSteps = res.steps;
      currentStepIdx = -1;
      stepBtn.disabled = false;
      nextStep();
    } catch (e) {
      console.error(e);
      status.innerHTML = 'STATUS: <span style="color: #ff5f5f">TRACE FAILED</span>';
      checkBackend();
    }
  }

  function nextStep() {
    currentStepIdx++;
    if (currentStepIdx >= currentSteps.length) {
      stepBtn.disabled = true;
      note.textContent = "ALGORITHM TRACE COMPLETE.";
      status.innerHTML = 'STATUS: <span style="color: var(--cBright)">TERMINATED</span>';
      return;
    }

    const step = currentSteps[currentStepIdx];
    
    // Reset highlights
    svg.querySelectorAll('.node.active, .edge.active').forEach(el => el.classList.remove('active'));

    if (step.node || (step.highlight && step.highlight.node)) {
      const node = step.node || step.highlight.node;
      const nodeEl = svg.querySelector(`#node-${node}`);
      if (nodeEl) nodeEl.classList.add('active');
    }
    if (step.edge || (step.highlight && step.highlight.edge)) {
      const edge = step.edge || step.highlight.edge;
      const source = Array.isArray(edge) ? edge[0] : edge.source;
      const target = Array.isArray(edge) ? edge[1] : edge.target;
      const edgeEl = svg.querySelector(`#edge-${source}-${target}`) || 
                     svg.querySelector(`#edge-${target}-${source}`);
      if (edgeEl) edgeEl.classList.add('active');
    }

    note.textContent = (step.note || "SYSTEM PROCESSING...").toUpperCase();
    note.style.opacity = 1;
  }

  async function explain() {
    if (currentStepIdx < 0) return;
    explainBtn.disabled = true;
    explanationBox.style.display = 'block';
    explanationBox.textContent = "CONSULTING BLUEPRINT AI...";
    
    try {
      const step = currentSteps[currentStepIdx];
      let res;
      if (isOffline) {
        res = { text: `[EMULATOR] THIS STEP SHOWS THE SYSTEM ${step.node ? `VISITING NODE ${step.node}` : `TRACING THE EDGE BETWEEN ${step.edge.source} AND ${step.edge.target}`}.` };
      } else {
        res = await api.explainStep(algo, step);
      }
      explanationBox.textContent = (res.text || res.explanation || "NO DATA AVAILABLE.").toUpperCase();
    } catch (e) {
      explanationBox.textContent = "AI PROTOCOL TIMEOUT. RETRY LATER.";
    } finally {
      explainBtn.disabled = false;
    }
  }

  runBtn.addEventListener('click', run);
  stepBtn.addEventListener('click', nextStep);
  resetBtn.addEventListener('click', () => {
    currentStepIdx = -1;
    currentSteps = [];
    stepBtn.disabled = true;
    runBtn.disabled = false;
    note.style.opacity = 0;
    explanationBox.style.display = 'none';
    renderGraph();
  });
  explainBtn.addEventListener('click', explain);

  renderGraph();
  checkBackend();
}

export function mountBugFinder(view) {
  const btn = view.querySelector('#find-bug-btn');
  const codeArea = view.querySelector('#code-area');
  const langSelect = view.querySelector('#lang-select');
  const result = view.querySelector('#bug-result');

  const DEFAULT_CODE = `def binary_search(arr, target):
    low = 0
    high = len(arr) # BUG: should be len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid # BUG: should be mid - 1
    return -1`;

  codeArea.value = DEFAULT_CODE;

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    result.style.display = 'block';
    result.textContent = "ANALYZING CODE...";
    
    try {
      const res = await api.bugFind(langSelect.value, codeArea.value);
      const hints = res.hints || [res.hint] || ["No obvious bug found."];
      result.innerHTML = `<strong>AI SCAN:</strong><br>${hints.map(h => `> ${h}`).join('<br>')} ${res.fallback ? '<br><small>(OFFLINE FALLBACK)</small>' : ''}`;
    } catch (e) {
      result.innerHTML = `<strong>ANALYSIS:</strong> Check your loop boundaries and update conditions. Binary search is tricky! <br><small>(LOCAL FALLBACK)</small>`;
    } finally {
      btn.disabled = false;
    }
  });
}
