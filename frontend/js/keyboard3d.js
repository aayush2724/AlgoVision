import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { ALGORITHMS } from './data.js';

/* ══════════════════════════════════════════════════════════════
   The AlgoVision keyboard.

   A full-size 3D mechanical keyboard. Most caps are decorative —
   modifiers and math-glyph novelties — and scattered among them
   are 22 algorithm keys. Drag to rotate, scroll to zoom, hover to
   inspect, click an algorithm key to dive into its live trace.
══════════════════════════════════════════════════════════════ */

// Colourway of the reference board: warm greys, cream, tan, burnt orange.
const PLATE  = '#221d16';
const GREY   = '#514c43';   // standard cap
const CREAM  = '#e7ddc4';   // modifier cap
const TAN    = '#a8895f';   // novelty cap
const ORANGE = '#c94f22';   // corner accents

const CAP_COLORS = {
  grey:   { cap: GREY,   legend: '#eae3d3', sub: 'rgba(234,227,211,0.66)' },
  cream:  { cap: CREAM,  legend: '#3a352c', sub: 'rgba(58,53,44,0.72)' },
  tan:    { cap: TAN,    legend: '#2e2820', sub: 'rgba(46,40,32,0.72)' },
  orange: { cap: ORANGE, legend: '#f7ede2', sub: 'rgba(247,237,226,0.8)' },
};

function capStyle(algo) {
  if (algo.id === 'dijkstra' || algo.id === 'lcs') return CAP_COLORS.orange;
  if (algo.category === 'DP' || algo.category === 'Searching') return CAP_COLORS.cream;
  if (algo.category === 'Structures') return CAP_COLORS.tan;
  return CAP_COLORS.grey;
}

// Short face label per algorithm.
const SHORT = {
  dijkstra: 'DIJK', bfs: 'BFS', dfs: 'DFS', prims_mst: 'PRIM', kruskals_mst: 'KRSK',
  merge_sort: 'MRG', quick_sort: 'QCK', bubble_sort: 'BUB', insertion_sort: 'INS', selection_sort: 'SEL',
  binary_search: 'BIN', bst_search: 'BSTs', two_sum_sorted: '2SUM', sliding_window: 'WIN', kadanes: 'KDN',
  linked_list_reverse: 'LIST', balanced_brackets: '{ }', bst_insert: 'BST', heap_insert: 'HEAP',
  fibonacci_dp: 'FIB', knapsack_01: 'KNAP', lcs: 'LCS',
  edit_distance: 'EDIT', topological_sort: 'TOPO', counting_sort: 'CNT',
  prefix_sums: 'PRE', next_greater_element: 'NGE', floyd_cycle: 'CYCL',
  tree_traversal: 'WALK', trie_insert: 'TRIE', n_queens: 'NQ',
  unique_paths: 'PATH', sieve: 'PRIME',
  kmp_search: 'KMP', segment_tree: 'SEG', fenwick_tree: 'BIT',
};

// Layout entries: a = algorithm key, g = glyph novelty, m = modifier.
// `w` is width in key units; every row sums to 15u like a real 60% board.
const A = (id)              => ({ t: 'a', id, w: 1 });
const G = (glyph, c = 'grey', w = 1) => ({ t: 'g', glyph, c, w });
const M = (label, w, c = 'cream')    => ({ t: 'm', label, c, w });

const LAYOUT = [
  [ M('FN', 1, 'grey'), A('tree_traversal'), A('trie_insert'), G('F3'), A('n_queens'),
    G('F5'), A('unique_paths'), G('F7'), A('sieve'), A('kmp_search'), G('F10'),
    A('segment_tree'), A('fenwick_tree'), M('DEL', 2, 'orange') ],
  [ M('ESC', 1, 'orange'), A('edit_distance'), G('2'), A('fibonacci_dp'), G('4'), G('5'),
    A('knapsack_01'), G('7'), G('8'), G('9', 'tan'), A('lcs'), G('-'), G('='), M('⌫', 2) ],
  [ M('TAB', 1.5), A('dijkstra'), G('λ'), A('bfs'), G('Σ'), A('dfs'),
    A('topological_sort'), G('∞', 'tan'), A('prims_mst'), G('⊕'),
    A('kruskals_mst'), G('√'), A('balanced_brackets'), G('∴', 'grey', 1.5) ],
  [ M('CAPS', 1.75), A('merge_sort'), A('counting_sort'), A('quick_sort'), G('Δ'),
    A('bubble_sort'), G('θ'), A('insertion_sort'), G('μ'), A('selection_sort'),
    G('Ω', 'tan'), A('bst_search'), M('ENTER', 2.25) ],
  [ M('SHIFT', 2.25), A('binary_search'), A('prefix_sums'), A('linked_list_reverse'),
    A('two_sum_sorted'), A('next_greater_element'), A('sliding_window'),
    A('bst_insert'), A('floyd_cycle'), A('kadanes'),
    A('heap_insert'), M('SHIFT', 2.75) ],
  [ M('CTRL', 1.25, 'grey'), M('FN', 1.25, 'grey'), M('ALT', 1.25, 'grey'),
    M('ALGOVISION', 6.25), M('ALT', 1.25, 'grey'), M('⌘', 1.25, 'grey'), M('CTRL', 2.5, 'grey') ],
];

const U = 1.0;          // key unit
const GAP = 0.14;
const STEP = U + GAP;
const ROW_UNITS = 15;

function capTexture(entry, algo) {
  const wPx = Math.round(256 * entry.w);
  const c = document.createElement('canvas');
  c.width = wPx; c.height = 256;
  const x = c.getContext('2d');
  const st = entry.t === 'a' ? capStyle(algo) : CAP_COLORS[entry.c || 'grey'];
  x.fillStyle = st.cap;
  x.fillRect(0, 0, wPx, 256);
  const g = x.createLinearGradient(0, 0, 0, 256);
  g.addColorStop(0, 'rgba(255,255,255,0.10)');
  g.addColorStop(0.5, 'rgba(255,255,255,0)');
  g.addColorStop(1, 'rgba(0,0,0,0.12)');
  x.fillStyle = g; x.fillRect(0, 0, wPx, 256);
  x.textAlign = 'center'; x.textBaseline = 'middle';
  if (entry.t === 'a') {
    x.fillStyle = st.legend;
    x.font = '600 64px Geist, system-ui, sans-serif';
    x.fillText(SHORT[algo.id] || algo.id.slice(0, 4).toUpperCase(), wPx / 2, 116);
    x.fillStyle = st.sub;
    x.font = '500 28px "Geist Mono", monospace';
    x.fillText(algo.complexity, wPx / 2, 184);
  } else if (entry.t === 'g') {
    x.fillStyle = st.sub;
    x.font = '500 86px Geist, "Geist Mono", system-ui, sans-serif';
    x.fillText(entry.glyph, wPx / 2, 134);
  } else {
    x.fillStyle = st.sub;
    x.font = '500 40px Geist, system-ui, sans-serif';
    x.fillText(entry.label, wPx / 2, 134);
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

export function initKeyboard(container, { onCount } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);
  renderer.domElement.style.display = 'block';
  renderer.domElement.style.width = '100%';
  renderer.domElement.style.height = '100%';
  renderer.domElement.style.cursor = 'grab';

  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0, 10.5, 9.0);

  scene.add(new THREE.AmbientLight(0xffe6c4, 0.5));
  const lamp = new THREE.PointLight(0xffb46b, 90, 30, 1.8);
  lamp.position.set(2.5, 7, -1.5);
  scene.add(lamp);
  const key = new THREE.DirectionalLight(0xffe0b8, 1.05);
  key.position.set(-6, 11, 6);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.left = -11; key.shadow.camera.right = 11;
  key.shadow.camera.top = 11; key.shadow.camera.bottom = -11;
  scene.add(key);
  const fill = new THREE.DirectionalLight(0x9fb4d0, 0.35);
  fill.position.set(7, 5, -5);
  scene.add(fill);

  const rows = LAYOUT.length;
  const rowW = ROW_UNITS * STEP - GAP;
  const plateW = rowW + 1.1;
  const plateD = rows * STEP - GAP + 1.1;
  const plateGeo = new RoundedBoxGeometry(plateW, 0.7, plateD, 4, 0.18);
  const plate = new THREE.Mesh(plateGeo,
    new THREE.MeshStandardMaterial({ color: PLATE, roughness: 0.85, metalness: 0.15 }));
  plate.position.y = -0.35;
  plate.receiveShadow = true;
  scene.add(plate);

  // Geometry per distinct cap width, side material per cap colour.
  const geoCache = new Map();
  const geoFor = (wu) => {
    if (!geoCache.has(wu)) {
      geoCache.set(wu, new RoundedBoxGeometry(wu * U + (wu - 1) * GAP, 0.5, U, 3, 0.09));
    }
    return geoCache.get(wu);
  };
  const sideCache = new Map();
  const sideFor = (hex) => {
    if (!sideCache.has(hex)) {
      sideCache.set(hex, new THREE.MeshStandardMaterial({
        color: new THREE.Color(hex).multiplyScalar(0.62),
        roughness: 0.72, metalness: 0.08,
      }));
    }
    return sideCache.get(hex);
  };

  const algoKeys = [];
  const decorMats = [];
  const byAlgo = Object.fromEntries(ALGORITHMS.map(a => [a.id, a]));
  const raycaster = new THREE.Raycaster();

  LAYOUT.forEach((row, ri) => {
    let cursor = -rowW / 2;
    const z = ri * STEP - (rows * STEP - GAP) / 2 + U / 2;
    row.forEach((entry) => {
      const capW = entry.w * U + (entry.w - 1) * GAP;
      const algo = entry.t === 'a' ? byAlgo[entry.id] : null;
      if (entry.t === 'a' && !algo) { cursor += capW + GAP; return; }
      const st = entry.t === 'a' ? capStyle(algo) : CAP_COLORS[entry.c || 'grey'];
      const topMat = new THREE.MeshStandardMaterial({
        map: capTexture(entry, algo), roughness: 0.55, metalness: 0.05,
      });
      const sideMat = sideFor(st.cap);
      // Box face order: +x -x +y -y +z -z → index 2 is the top face
      const mats = [sideMat, sideMat, topMat, sideMat, sideMat, sideMat];
      const cap = new THREE.Mesh(geoFor(entry.w), mats);
      cap.position.set(cursor + capW / 2, 0, z);
      cap.castShadow = true;
      scene.add(cap);
      if (algo) {
        cap.userData = { algo, targetY: 0 };
        algoKeys.push(cap);
      } else {
        decorMats.push(topMat);
      }
      cursor += capW + GAP;
    });
  });

  const controls = new OrbitControls(camera, renderer.domElement);
  // Aim just below the plate so the board sits centred under the nav.
  controls.target.set(0, -0.8, 0);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 5;
  controls.maxDistance = 17;
  controls.minPolarAngle = 0.15;
  controls.maxPolarAngle = Math.PI / 2.15;
  controls.enablePan = false;
  // The board stays put — rotation happens only when the user drags it.
  controls.autoRotate = false;
  // Keep the board from spinning behind itself; a shallow arc reads as a desk.
  controls.minAzimuthAngle = -Math.PI / 5;
  controls.maxAzimuthAngle = Math.PI / 5;

  // The stage fills the whole hero, so the wheel must not trap the page:
  // once fully zoomed out (or when the page is mid-scroll), hand the wheel
  // back to normal document scrolling instead of OrbitControls.
  function wheelGate(e) {
    const dist = camera.position.distanceTo(controls.target);
    const zoomingOut = e.deltaY > 0;
    if ((zoomingOut && dist >= controls.maxDistance - 0.01) ||
        (!zoomingOut && window.scrollY > 0)) {
      e.preventDefault();
      e.stopPropagation();
      window.scrollBy(0, e.deltaY);
    }
  }
  container.addEventListener('wheel', wheelGate, { capture: true, passive: false });

  const tip = document.createElement('div');
  tip.className = 'kbd-tip';
  container.appendChild(tip);

  const mouse = new THREE.Vector2(-2, -2);
  let hovered = null;
  const visited = new Set();

  function onPointerMove(e) {
    const r = renderer.domElement.getBoundingClientRect();
    mouse.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    mouse.y = -((e.clientY - r.top) / r.height) * 2 + 1;
    tip._client = { x: e.clientX - r.left, y: e.clientY - r.top };
  }
  renderer.domElement.addEventListener('pointermove', onPointerMove);
  renderer.domElement.addEventListener('pointerleave', () => { mouse.set(-2, -2); });

  let flying = null;
  function launch(cap) {
    const algo = cap.userData.algo;
    visited.add(algo.id);
    if (onCount) onCount(visited.size, algoKeys.length);
    const dest = cap.position.clone().add(new THREE.Vector3(0, 2.4, 2.6));
    flying = { toPos: dest, toTarget: cap.position.clone(), t: 0, algo };
  }
  function onClick() { if (hovered && !flying) launch(hovered); }
  renderer.domElement.addEventListener('click', onClick);

  // Distance at which the whole board spans the viewport width, so the
  // board is the hero at any window size instead of overflowing it.
  const ELEV = 0.86;   // radians above the desk
  const corners = [];
  for (const sx of [-1, 1]) for (const sy of [-0.7, 0.25]) for (const sz of [-1, 1]) {
    corners.push(new THREE.Vector3(sx * plateW / 2, sy, sz * plateD / 2));
  }
  const probe = new THREE.Vector3();

  function placeCamera(d) {
    camera.position.set(0,
      controls.target.y + Math.sin(ELEV) * d,
      controls.target.z + Math.cos(ELEV) * d);
    camera.lookAt(controls.target);
    camera.updateMatrixWorld();
  }
  // Perspective foreshortening makes the near corners the widest points on
  // screen, so fit by projecting the actual corners rather than by trig.
  function fitDistance() {
    let d = 8;
    for (let i = 0; i < 60; i++) {
      placeCamera(d);
      const fits = corners.every(c =>
        (probe.copy(c).project(camera), Math.abs(probe.x) <= 0.95 && Math.abs(probe.y) <= 0.95));
      if (fits) break;
      d *= 1.04;
    }
    return d;
  }
  let userMoved = false;
  controls.addEventListener('start', () => { userMoved = true; });

  function resize() {
    const w = container.clientWidth || 1;
    const h = container.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();

    const home = camera.position.clone();
    const d = fitDistance();
    controls.maxDistance = Math.max(17, d * 1.15);
    if (userMoved) camera.position.copy(home);
    controls.update();
  }
  const ro = new ResizeObserver(resize);
  ro.observe(container);
  resize();

  const clock = new THREE.Clock();
  let raf = 0, alive = true;
  function frame() {
    if (!alive) return;
    raf = requestAnimationFrame(frame);
    const dt = Math.min(clock.getDelta(), 0.05);

    raycaster.setFromCamera(mouse, camera);
    const hits = flying ? [] : raycaster.intersectObjects(algoKeys, false);
    const hit = hits.length ? hits[0].object : null;
    if (hit !== hovered) {
      hovered = hit;
      renderer.domElement.style.cursor = hit ? 'pointer' : 'grab';
      if (hit) {
        const a = hit.userData.algo;
        tip.innerHTML = `<strong>${a.name}</strong><span>${a.category} · ${a.complexity}</span>`;
        tip.classList.add('show');
      } else {
        tip.classList.remove('show');
      }
    }
    if (hovered && tip._client) {
      tip.style.transform = `translate(${tip._client.x + 16}px, ${tip._client.y - 8}px)`;
    }

    algoKeys.forEach(k => {
      k.userData.targetY = (k === hovered) ? 0.22 : 0;
      k.position.y += (k.userData.targetY - k.position.y) * Math.min(1, dt * 14);
    });

    if (flying) {
      flying.t += dt;
      camera.position.lerp(flying.toPos, Math.min(1, dt * 3.2));
      controls.target.lerp(flying.toTarget, Math.min(1, dt * 3.2));
      if (flying.t > 0.9) {
        const id = flying.algo.id;
        flying = null;
        location.hash = `#/experience?algo=${id}`;
      }
    }

    controls.update();
    renderer.render(scene, camera);
  }
  raf = requestAnimationFrame(frame);

  const onVis = () => {
    if (document.hidden) { alive = false; cancelAnimationFrame(raf); }
    else if (!alive) { alive = true; clock.getDelta(); raf = requestAnimationFrame(frame); }
  };
  document.addEventListener('visibilitychange', onVis);

  return {
    dispose() {
      alive = false;
      cancelAnimationFrame(raf);
      ro.disconnect();
      document.removeEventListener('visibilitychange', onVis);
      controls.dispose();
      container.removeEventListener('wheel', wheelGate, { capture: true });
      renderer.domElement.removeEventListener('pointermove', onPointerMove);
      renderer.domElement.removeEventListener('click', onClick);
      tip.remove();
      algoKeys.forEach(k => { (k.material || []).forEach?.(m => { if (m.map) { m.map.dispose(); m.dispose(); } }); });
      decorMats.forEach(m => { m.map?.dispose(); m.dispose(); });
      sideCache.forEach(m => m.dispose());
      geoCache.forEach(g => g.dispose());
      plateGeo.dispose();
      renderer.dispose();
      if (renderer.domElement.parentNode === container) container.removeChild(renderer.domElement);
    },
  };
}
