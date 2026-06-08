// Scroll-driven 3D "morphing node network" background for AlgoVision.
// Glowing nodes reshape between graph -> tree -> sorted array -> path, scrubbed by page scroll.
// Same public API as before: initScene(canvas) -> { setTheme(name) }.
import * as THREE from "three";
const COL = { blue: 0x4d7bff, blueB: 0x6f9bff, violet: 0x8b5cff, purple: 0xa855f7, cyan: 0x38bdf8 };
// Per-route light tints (kept in the blue/purple family).
const THEMES = {
  default:     { a: 0x4d7bff, b: 0x8b5cff },
  explore:     { a: 0x38bdf8, b: 0x4d7bff },
  experience:  { a: 0x4d7bff, b: 0xa855f7 },
  a2z:         { a: 0x4d7bff, b: 0x6f9bff },
  today:       { a: 0x8b5cff, b: 0xa855f7 },
  practice:    { a: 0x4d7bff, b: 0x8b5cff },
  journey:     { a: 0x38bdf8, b: 0x8b5cff },
  realworld:   { a: 0x4d7bff, b: 0x38bdf8 },
};
function lerp(a, b, t) { return a + (b - a) * t; }
export function initScene(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x060713, 1);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060713, 0.022);
  const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 200);
  camera.position.set(0, 0, 18);
  scene.add(new THREE.AmbientLight(0x556088, 1.1));
  const l1 = new THREE.PointLight(0x4d7bff, 2.4, 200); l1.position.set(14, 12, 14); scene.add(l1);
  const l2 = new THREE.PointLight(0x8b5cff, 2.2, 200); l2.position.set(-14, -8, 10); scene.add(l2);
  const l3 = new THREE.PointLight(0x38bdf8, 1.4, 200); l3.position.set(0, 14, -10); scene.add(l3);
  const l1Target = new THREE.Color(0x4d7bff), l2Target = new THREE.Color(0x8b5cff);
  const group = new THREE.Group();
  scene.add(group);
  // Build 31 nodes and 4 target layouts: graph, tree, array, path.
  const N = 31;
  const layouts = [[], [], [], []];
  for (let i = 0; i < N; i++) {
    const u = Math.random(), v = Math.random(), th = u * Math.PI * 2, ph = Math.acos(2 * v - 1), r = 6 * Math.cbrt(Math.random());
    layouts[0].push(new THREE.Vector3(r * Math.sin(ph) * Math.cos(th), r * Math.sin(ph) * Math.sin(th), r * Math.cos(ph)));
    const level = Math.floor(Math.log2(i + 1));
    const start = Math.pow(2, level) - 1, idx = i - start, count = Math.pow(2, level);
    layouts[1].push(new THREE.Vector3(((idx + 0.5) / count - 0.5) * 16, 7 - level * 3.4, 0));
    layouts[2].push(new THREE.Vector3((i - (N - 1) / 2) * 0.62, Math.sin(i * 0.3) * 0.2, 0));
    layouts[3].push(new THREE.Vector3((i - (N - 1) / 2) * 0.62, Math.sin(i * 0.55) * 3.2, Math.cos(i * 0.4) * 1.2));
  }
  const cur = layouts[0].map(p => p.clone());
  const nodeGeo = new THREE.SphereGeometry(0.22, 16, 16);
  const meshes = [];
  for (let i = 0; i < N; i++) {
    const c = i % 3 === 0 ? COL.cyan : (i % 3 === 1 ? COL.blue : COL.violet);
    const mat = new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: 0.6, metalness: 0.3, roughness: 0.25 });
    const m = new THREE.Mesh(nodeGeo, mat); m.position.copy(cur[i]); group.add(m); meshes.push(m);
  }
  const pairs = [];
  for (let i = 1; i < N; i++) pairs.push([i, Math.floor((i - 1) / 2)]);
  const linePos = new Float32Array(pairs.length * 2 * 3);
  const lgeo = new THREE.BufferGeometry();
  lgeo.setAttribute("position", new THREE.BufferAttribute(linePos, 3));
  const lines = new THREE.LineSegments(lgeo, new THREE.LineBasicMaterial({ color: COL.blueB, transparent: true, opacity: 0.28 }));
  group.add(lines);
  const mouse = new THREE.Vector2(0, 0), mTarget = new THREE.Vector2(0, 0);
  window.addEventListener("pointermove", (e) => {
    mTarget.set(e.clientX / window.innerWidth - 0.5, e.clientY / window.innerHeight - 0.5);
  });
  function scrollProgress() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    return max > 40 ? Math.min(Math.max(window.scrollY / max, 0), 1) : -1;
  }
  const api = {
    setTheme(name) {
      const th = THEMES[name] || THEMES.default;
      l1Target.setHex(th.a); l2Target.setHex(th.b);
    },
  };
  let autoTimer = 0, autoIdx = 0;
  const target = layouts[0].map(p => p.clone());
  function computeTarget(dt) {
    const p = scrollProgress();
    if (p < 0) {
      autoTimer += dt;
      if (autoTimer > 3.4) { autoTimer = 0; autoIdx = (autoIdx + 1) % layouts.length; }
      for (let i = 0; i < N; i++) target[i].copy(layouts[autoIdx][i]);
    } else {
      const f = p * (layouts.length - 1);
      const i0 = Math.floor(f), i1 = Math.min(i0 + 1, layouts.length - 1), frac = f - i0;
      for (let i = 0; i < N; i++) target[i].copy(layouts[i0][i]).lerp(layouts[i1][i], frac);
    }
  }
  let last = performance.now();
  function loop(now) {
    const dt = Math.min((now - last) / 1000, 0.05); last = now;
    computeTarget(dt);
    for (let i = 0; i < N; i++) { cur[i].lerp(target[i], 0.12); meshes[i].position.copy(cur[i]); }
    let k = 0;
    for (const [a, b] of pairs) {
      linePos[k++] = cur[a].x; linePos[k++] = cur[a].y; linePos[k++] = cur[a].z;
      linePos[k++] = cur[b].x; linePos[k++] = cur[b].y; linePos[k++] = cur[b].z;
    }
    lgeo.attributes.position.needsUpdate = true;
    group.rotation.y += dt * 0.12;
    l1.color.lerp(l1Target, 0.04); l2.color.lerp(l2Target, 0.04);
    mouse.lerp(mTarget, 0.05);
    camera.position.x = lerp(camera.position.x, mouse.x * 6, 0.06);
    camera.position.y = lerp(camera.position.y, -mouse.y * 4, 0.06);
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
    requestAnimationFrame(loop);
  }
  function resize() {
    const w = window.innerWidth, h = window.innerHeight;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  window.addEventListener("resize", resize); resize();
  requestAnimationFrame(loop);
  return api;
}
