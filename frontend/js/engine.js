import { api } from './api.js';
import * as DATA from './data.js';

export function mountEngine(view) {
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
      text.setAttribute("fill", "var(--muted)");
      text.setAttribute("font-size", "12");
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
      text.setAttribute("y", node.y + 5);
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("fill", "var(--ink)");
      text.setAttribute("font-weight", "bold");
      text.textContent = node.id;
      svg.appendChild(text);
    });
  }

  async function checkBackend() {
    try {
      await api.getAlgorithms();
      status.innerHTML = '<span class="badge badge-live">live · backend</span>';
      isOffline = false;
    } catch (e) {
      status.innerHTML = '<span class="badge badge-offline">offline · in-browser fallback</span>';
      isOffline = true;
    }
  }

  function localDijkstra(startNode) {
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
      
      steps.push({ node, note: `Visiting node ${node} with distance ${d}` });

      if (d > dist[node]) continue;

      for (const edge of (adj[node] || [])) {
        if (dist[node] + edge.w < dist[edge.to]) {
          dist[edge.to] = dist[node] + edge.w;
          pq.push({ node: edge.to, d: dist[edge.to] });
          steps.push({ edge: { source: node, target: edge.to }, note: `Found shorter path to ${edge.to} via ${node} (dist: ${dist[edge.to]})` });
        }
      }
    }
    return { steps };
  }

  async function run() {
    runBtn.disabled = true;
    explanationBox.style.display = 'none';
    try {
      let res;
      if (isOffline) {
        res = localDijkstra('A');
      } else {
        const graph = {
          nodes: DATA.SAMPLE_GRAPH.nodes.map(n => n.id),
          edges: DATA.SAMPLE_GRAPH.links.map(l => [l.source, l.target, l.weight])
        };
        res = await api.postTrace('dijkstra', 'A', graph);
      }
      currentSteps = res.steps;
      currentStepIdx = -1;
      stepBtn.disabled = false;
      nextStep();
    } catch (e) {
      console.error(e);
      alert("Failed to run Dijkstra. Checking backend...");
      checkBackend();
    }
  }

  function nextStep() {
    currentStepIdx++;
    if (currentStepIdx >= currentSteps.length) {
      stepBtn.disabled = true;
      note.textContent = "Algorithm Complete.";
      return;
    }

    const step = currentSteps[currentStepIdx];
    
    // Reset highlights
    svg.querySelectorAll('.node.active, .edge.active').forEach(el => el.classList.remove('active'));

    if (step.node) {
      const nodeEl = svg.querySelector(`#node-${step.node}`);
      if (nodeEl) nodeEl.classList.add('active');
    }
    if (step.edge) {
      const edgeEl = svg.querySelector(`#edge-${step.edge.source}-${step.edge.target}`) || 
                     svg.querySelector(`#edge-${step.edge.target}-${step.edge.source}`);
      if (edgeEl) edgeEl.classList.add('active');
    }

    note.textContent = step.note || "Processing...";
    note.style.opacity = 1;
  }

  async function explain() {
    if (currentStepIdx < 0) return;
    explainBtn.disabled = true;
    explanationBox.style.display = 'block';
    explanationBox.textContent = "Consulting AI...";
    
    try {
      const step = currentSteps[currentStepIdx];
      let res;
      if (isOffline) {
        res = { explanation: `[Offline Fallback] This step shows the algorithm ${step.node ? `visiting node ${step.node}` : `exploring the edge from ${step.edge.source} to ${step.edge.target}`}. It's updating the shortest known distance.` };
      } else {
        res = await api.explainStep('dijkstra', step);
      }
      explanationBox.textContent = res.explanation;
    } catch (e) {
      explanationBox.textContent = "AI is currently resting. Try again later.";
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
    result.textContent = "Analyzing code...";
    
    try {
      const res = await api.bugFind(langSelect.value, codeArea.value);
      result.innerHTML = `<strong>AI Hint:</strong> ${res.hint} ${res.fallback ? '<br><small>(Offline Fallback)</small>' : ''}`;
    } catch (e) {
      result.innerHTML = `<strong>Analysis:</strong> Check your loop boundaries and update conditions. Binary search is tricky! <br><small>(Local Fallback)</small>`;
    } finally {
      btn.disabled = false;
    }
  });
}
