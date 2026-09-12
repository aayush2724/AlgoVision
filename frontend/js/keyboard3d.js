import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { ALGORITHMS, KEYCAP_LABEL as SHORT } from './data.js';

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


// Layout entries: a = algorithm key, g = glyph novelty, m = modifier.
// `w` is width in key units; every row sums to 15u like a real 60% board.
const A = (id)              => ({ t: 'a', id, w: 1 });
const G = (glyph, c = 'grey', w = 1) => ({ t: 'g', glyph, c, w });
const M = (label, w, c = 'cream')    => ({ t: 'm', label, c, w });

const LAYOUT = [
  [ M('FN', 1, 'grey'), A('tree_traversal'), A('trie_insert'), G('F3'), A('n_queens'),
    G('F5'), A('unique_paths'), A('hash_table'), A('sieve'), A('kmp_search'), G('F10'),
    A('segment_tree'), A('fenwick_tree'), M('DEL', 2, 'orange') ],
  [ M('ESC', 1, 'orange'), A('edit_distance'), G('2'), A('fibonacci_dp'),
    A('coin_change'), G('5'),
    A('knapsack_01'), G('7'), A('merge_intervals'), G('9', 'tan'), A('lcs'),
    G('-'), G('='), M('⌫', 2) ],
  [ M('TAB', 1.5), A('dijkstra'), G('λ'), A('bfs'), G('Σ'), A('dfs'),
    A('topological_sort'), G('∞', 'tan'), A('prims_mst'), A('dsu'),
    A('kruskals_mst'), G('√'), A('balanced_brackets'), G('∴', 'grey', 1.5) ],
  [ M('CAPS', 1.75), A('merge_sort'), A('counting_sort'), A('quick_sort'), G('Δ'),
    A('bubble_sort'), A('heap_extract'), A('insertion_sort'), G('μ'),
    A('selection_sort'),
    A('bst_delete'), A('bst_search'), M('ENTER', 2.25) ],
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

export function initKeyboard(container, { onCount, onFocus, onBlur, onScreenRect } = {}) {
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

  // ── The desk monitor ────────────────────────────────────────────────────
  // Clicking a keycap pans here instead of leaving the page. The screen is a
  // plain dark plane; the live trace is an HTML panel the host aligns over it
  // (see screenRect()), which keeps the real SVG engine in charge of drawing
  // rather than reimplementing every view as a texture.
  const MON_W = 11.6, MON_H = 6.6, MON_Y = 4.7, MON_Z = -6.6;
  const SCREEN_W = MON_W - 0.72, SCREEN_H = MON_H - 0.72;

  const caseMat = new THREE.MeshStandardMaterial({
    color: 0x1c1814, roughness: 0.62, metalness: 0.3,
  });
  const monitor = new THREE.Group();
  const bezel = new THREE.Mesh(
    new RoundedBoxGeometry(MON_W, MON_H, 0.38, 4, 0.14), caseMat);
  bezel.castShadow = true;
  const screen = new THREE.Mesh(
    new THREE.PlaneGeometry(SCREEN_W, SCREEN_H),
    new THREE.MeshBasicMaterial({ color: 0x0c0a08 }));
  screen.position.z = 0.2;
  const neck = new THREE.Mesh(
    new RoundedBoxGeometry(0.8, 2.3, 0.55, 3, 0.1), caseMat);
  neck.position.y = -MON_H / 2 - 1.05;
  const foot = new THREE.Mesh(
    new RoundedBoxGeometry(3.8, 0.3, 1.9, 3, 0.1), caseMat);
  foot.position.set(0, -MON_H / 2 - 2.1, 0.35);
  foot.receiveShadow = true;
  monitor.add(bezel, screen, neck, foot);
  monitor.position.set(0, MON_Y, MON_Z);
  monitor.rotation.x = -0.05;
  scene.add(monitor);

  // Camera position that frames the whole screen with a little margin, at
  // whatever aspect the window happens to be. A fixed distance only worked at
  // one ratio — anything wider and the screen ran off the viewport.
  function monitorViewPos() {
    const halfFov = THREE.MathUtils.degToRad(camera.fov) / 2;
    const margin = 1.16;
    const dForH = (SCREEN_H * margin / 2) / Math.tan(halfFov);
    const dForW = (SCREEN_W * margin / 2) / (Math.tan(halfFov) * camera.aspect);
    const d = Math.max(dForH, dForW);
    return new THREE.Vector3(0, MON_Y + 0.2, MON_Z + d);
  }

  // Where the monitor's screen lands on the canvas, in CSS pixels. The host
  // overlay tracks this every frame so it stays glued through the pan.
  const _corner = new THREE.Vector3();
  function screenRect() {
    const el = renderer.domElement;
    const w = el.clientWidth, h = el.clientHeight;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      _corner.set(sx * SCREEN_W / 2, sy * SCREEN_H / 2, 0);
      screen.localToWorld(_corner).project(camera);
      const px = (_corner.x * 0.5 + 0.5) * w;
      const py = (-_corner.y * 0.5 + 0.5) * h;
      if (px < minX) minX = px;
      if (px > maxX) maxX = px;
      if (py < minY) minY = py;
      if (py > maxY) maxY = py;
    }
    return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
  }

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

  // The wheel zooms the board — that is the whole feel of the hero — and then
  // hands off to the page once there is nothing left to zoom.
  //
  // The handoff used to be `dist >= maxDistance - 0.01`, which almost never
  // fired: damping eases the camera toward maxDistance asymptotically, so on
  // any given wheel tick it is still short of the limit. The page stayed
  // trapped and everything below the hero was unreachable. A tolerance scaled
  // to the zoom range is forgiving enough to fire mid-ease.
  controls.enableZoom = true;

  function wheelGate(e) {
    const dist = camera.position.distanceTo(controls.target);
    const scrollingDown = e.deltaY > 0;
    const tol = Math.max(0.3, controls.maxDistance * 0.03);
    const fullyZoomedOut = dist >= controls.maxDistance - tol;

    // Zoomed all the way out and still pushing down → the page takes over.
    // Scrolling up while the page has moved → put the page back first, so the
    // board is always fully in view before it starts zooming in again.
    if ((scrollingDown && fullyZoomedOut) || (!scrollingDown && window.scrollY > 0)) {
      e.preventDefault();
      e.stopPropagation();   // keep OrbitControls from also consuming it
      window.scrollBy(0, e.deltaY);
    }
    // Otherwise fall through: OrbitControls zooms.
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
  let focused = null;   // the algo currently on screen
  // Where the camera was when the user clicked, so blur() puts them back
  // exactly there rather than at some recomputed default framing.
  const homePos = new THREE.Vector3();
  const homeTarget = new THREE.Vector3();

  function launch(cap) {
    const algo = cap.userData.algo;
    visited.add(algo.id);
    if (onCount) onCount(visited.size, algoKeys.length);
    homePos.copy(camera.position);
    homeTarget.copy(controls.target);
    // Pan to the monitor rather than navigating away — the trace plays there.
    flying = {
      toPos:    monitorViewPos(),
      toTarget: new THREE.Vector3(0, MON_Y, MON_Z),
      t: 0, algo, mode: 'focus',
    };
  }
  function onClick() { if (hovered && !flying && !focused) launch(hovered); }
  renderer.domElement.addEventListener('click', onClick);

  // Fly back to the board and hand control to the user again.
  function blur() {
    if (!focused && !flying) return;
    focused = null;
    controls.enabled = true;
    flying = { toPos: homePos.clone(), toTarget: homeTarget.clone(),
               t: 0, mode: 'home' };
    onBlur?.();
  }

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
    if (focused && !flying) {
      // Re-fit: a resize changes the aspect, and with it the right distance.
      camera.position.copy(monitorViewPos());
      controls.target.set(0, MON_Y, MON_Z);
    }
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
      if (flying.t > 0.85) {
        const done = flying;
        flying = null;
        if (done.mode === 'focus') {
          // Settle exactly on the framing so the overlay can't drift, and
          // lock the orbit controls while the screen is being read.
          camera.position.copy(done.toPos);
          controls.target.copy(done.toTarget);
          controls.update();
          focused = done.algo;
          controls.enabled = false;
          onFocus?.(done.algo, screenRect());
        } else {
          // Snap here too. The flight ends on a timer, not on convergence, so
          // without this the camera settles slightly short of where it started
          // and the board comes back subtly reframed — enough that clicking
          // the same spot afterwards picks a different key.
          camera.position.copy(done.toPos);
          controls.target.copy(done.toTarget);
          controls.update();
          controls.enabled = true;
        }
      }
    }

    if (focused || flying?.mode === 'focus') onScreenRect?.(screenRect());

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
    blur,
    isFocused: () => !!focused,
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
