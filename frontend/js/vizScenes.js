/**
 * vizScenes.js — 3D animated visualizations for every A2Z problem type.
 * Uses Three.js (available via importmap) + GSAP (global).
 */

import * as THREE from 'three';

// ── SHARED 3D SETUP ──────────────────────────────────────────────────────────

function setup3D(container, camPos = [0, 4, 12]) {
  const rect = container.getBoundingClientRect();
  const w = (rect.width > 0 ? rect.width : container.clientWidth) || 520;
  const h = 260;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  } catch (e) {
    const fb = document.createElement('div');
    fb.style.cssText = `height:${h}px;display:flex;align-items:center;justify-content:center;
      color:#2a7f8c;font-family:monospace;font-size:12px;opacity:0.6;border:1px solid #0c2a31;border-radius:2px;`;
    fb.textContent = '[ 3D VISUALIZATION — OPEN IN BROWSER ]';
    container.appendChild(fb);
    throw e;
  }
  renderer.setSize(w, h, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  renderer.setClearColor(0x04090e, 1);
  Object.assign(renderer.domElement.style, {
    width: '100%', height: `${h}px`, display: 'block', borderRadius: '2px'
  });
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x04090e, 18, 38);

  const camera = new THREE.PerspectiveCamera(46, w / h, 0.1, 100);
  camera.position.set(...camPos);
  camera.lookAt(0, 0, 0);

  // Lighting
  scene.add(new THREE.AmbientLight(0x0c3040, 5));
  const key = new THREE.PointLight(0x5fd6e6, 120, 25);
  key.position.set(4, 7, 6);
  scene.add(key);
  const fill = new THREE.PointLight(0x2a7f8c, 60, 20);
  fill.position.set(-5, 3, 4);
  scene.add(fill);
  const back = new THREE.PointLight(0xa9f0fa, 30, 15);
  back.position.set(0, -2, -5);
  scene.add(back);

  // Grid floor
  const grid = new THREE.GridHelper(24, 24, 0x0c2a31, 0x080f14);
  grid.position.y = -3.2;
  scene.add(grid);

  return { renderer, scene, camera };
}

// ── MATERIAL HELPERS ─────────────────────────────────────────────────────────

const C      = 0x5fd6e6;
const BRIGHT = 0xa9f0fa;
const DIM    = 0x2a7f8c;
const DEEP   = 0x0c2a31;

function matCyan(intensity = 0.5) {
  return new THREE.MeshStandardMaterial({
    color: C, emissive: C, emissiveIntensity: intensity,
    metalness: 0.8, roughness: 0.2
  });
}
function matBright(intensity = 0.5) {
  return new THREE.MeshStandardMaterial({
    color: BRIGHT, emissive: BRIGHT, emissiveIntensity: intensity,
    metalness: 0.8, roughness: 0.2
  });
}
function matDim(intensity = 0.2) {
  return new THREE.MeshStandardMaterial({
    color: DIM, emissive: DIM, emissiveIntensity: intensity,
    metalness: 0.6, roughness: 0.4
  });
}
function matDark() {
  return new THREE.MeshStandardMaterial({
    color: DEEP, emissive: 0x051a20, emissiveIntensity: 0.15,
    metalness: 0.9, roughness: 0.15
  });
}
function matColor(hex, intensity = 0.4) {
  return new THREE.MeshStandardMaterial({
    color: hex, emissive: hex, emissiveIntensity: intensity,
    metalness: 0.7, roughness: 0.3
  });
}

// ── ANIMATION LOOP HELPER ────────────────────────────────────────────────────

function animLoop(renderer, scene, camera, updateFn) {
  const tick = () => {
    if (!renderer.domElement.isConnected) { renderer.dispose(); return; }
    requestAnimationFrame(tick);
    if (updateFn) updateFn();
    renderer.render(scene, camera);
  };
  tick();
}

// ── GEOMETRY HELPERS ─────────────────────────────────────────────────────────

function box(scene, w, h, d, mat, x, y, z) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
  m.position.set(x, y, z);
  scene.add(m);
  return m;
}

function sphere(scene, r, mat, x, y, z) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 12), mat);
  m.position.set(x, y, z);
  scene.add(m);
  return m;
}

function cylinder(scene, rT, rB, h, mat, x, y, z) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rT, rB, h, 16), mat);
  m.position.set(x, y, z);
  scene.add(m);
  return m;
}

function glowLine(scene, from, to, color = C) {
  const pts = [new THREE.Vector3(...from), new THREE.Vector3(...to)];
  const geo = new THREE.BufferGeometry().setFromPoints(pts);
  const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ color }));
  scene.add(line);
  return line;
}

// ═══════════════════════════════════════════════════════════════════════════
//  VIZ SCENES
// ═══════════════════════════════════════════════════════════════════════════

export const VIZ_SCENES = {

  // ── ARRAY / TRAIN CARRIAGES ───────────────────────────────────────────────
  array: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3.5, 13]);
      const vals = [3, 7, 1, 9, 4, 6, 2, 8];
      const boxes = [];
      vals.forEach((v, i) => {
        const m = box(scene, 1.15, 1.15, 0.7,
          i === 3 ? matBright(0.7) : matDark(), i * 1.38 - 4.8, -4, 0);
        boxes.push(m);
        gsap.to(m.position, { y: 0, duration: 0.6, delay: i * 0.07, ease: 'back.out(1.5)' });
        if (i < vals.length - 1)
          box(scene, 0.28, 0.08, 0.08, matDim(0.4), i * 1.38 - 4.8 + 0.72, 0, 0);
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.012;
        boxes.forEach((b, i) => { b.rotation.y = Math.sin(t + i * 0.6) * 0.06; });
        camera.position.x = Math.sin(t * 0.12) * 0.6;
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // alias
  train: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      const n = 7;
      const nodes = [];
      for (let i = 0; i < n; i++) {
        const m = box(scene, 1.2, 0.9, 0.65, i === 0 ? matCyan(0.7) : matDark(),
          i * 1.6 - 4.8, -4, 0);
        nodes.push(m);
        gsap.to(m.position, { y: 0, duration: 0.55, delay: i * 0.1, ease: 'back.out(1.4)' });
        if (i < n - 1) {
          const conn = box(scene, 0.35, 0.12, 0.12, matCyan(0.3),
            i * 1.6 - 4.8 + 0.78, 0, 0);
          nodes.push(conn);
        }
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        nodes[0] && (nodes[0].rotation.y = Math.sin(t * 2) * 0.1);
        camera.position.x = Math.sin(t * 0.1) * 0.5;
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── LEADERBOARD / BAR CHART ───────────────────────────────────────────────
  leaderboard: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 5, 14]);
      const vals = [4, 7, 2, 9, 1, 6, 3, 8, 5];
      const bars = [];
      vals.forEach((v, i) => {
        const h = v * 0.5;
        const m = box(scene, 0.9, 0.01, 0.7,
          i === 3 ? matBright(0.8) : matCyan(0.4),
          i * 1.15 - 4.6, -3.2, 0);
        bars.push({ mesh: m, targetH: h, v });
        gsap.to(m.scale, { y: h / 0.01, duration: 0.8, delay: i * 0.07, ease: 'power2.out' });
        gsap.to(m.position, { y: h / 2 - 3.2, duration: 0.8, delay: i * 0.07, ease: 'power2.out' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        bars.forEach((b, i) => { b.mesh.rotation.y = Math.sin(t * 0.5 + i) * 0.04; });
        camera.position.set(Math.sin(t * 0.08) * 1.5, 5, 14);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── BUBBLES (Bubble Sort) ─────────────────────────────────────────────────
  bubbles: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 2, 14]);
      const spheres = [];
      const sizes = [0.5, 0.8, 0.4, 0.95, 0.6, 0.7, 0.45, 0.85];
      sizes.forEach((r, i) => {
        const m = sphere(scene, r,
          new THREE.MeshStandardMaterial({
            color: C, emissive: C, emissiveIntensity: 0.3,
            transparent: true, opacity: 0.5 + r * 0.3,
            metalness: 0.1, roughness: 0.1
          }),
          (i - 3.5) * 1.4, -5, 0);
        spheres.push({ mesh: m, baseY: (1 - r) * 2.5, phase: i * 0.8 });
        gsap.to(m.position, { y: (1 - r) * 2.5, duration: 0.9, delay: i * 0.08, ease: 'power2.out' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.014;
        spheres.forEach(({ mesh, baseY, phase }) => {
          mesh.position.y = baseY + Math.sin(t + phase) * 0.18;
          mesh.rotation.y += 0.008;
        });
        camera.position.set(Math.sin(t * 0.1) * 1, 2, 14);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── MERGESORT ────────────────────────────────────────────────────────────
  mergesort: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 13]);
      const left  = [1, 3, 5, 7];
      const right = [2, 4, 6, 8];
      const leftBoxes = [], rightBoxes = [];

      left.forEach((v, i) => {
        const m = box(scene, 0.95, 0.95, 0.6, matCyan(0.5), i * 1.1 - 5.5, -4, 0.5);
        leftBoxes.push(m);
        gsap.to(m.position, { y: 0.6, duration: 0.5, delay: i * 0.08, ease: 'back.out(1.5)' });
      });
      right.forEach((v, i) => {
        const m = box(scene, 0.95, 0.95, 0.6, matDim(0.6), i * 1.1 - 0.7, -4, 0.5);
        rightBoxes.push(m);
        gsap.to(m.position, { y: 0.6, duration: 0.5, delay: i * 0.08 + 0.3, ease: 'back.out(1.5)' });
      });
      // Merged row
      const merged = [1, 2, 3, 4, 5, 6, 7, 8];
      const mergedBoxes = merged.map((v, i) => {
        const m = box(scene, 0.95, 0.95, 0.6, matDark(), i * 1.1 - 3.85, -4, -1.2);
        gsap.to(m.position, { y: -1.2, duration: 0.5, delay: 0.8 + i * 0.12, ease: 'power2.out' });
        return m;
      });
      gsap.delayedCall(1.6, () => {
        mergedBoxes.forEach(m => {
          gsap.to(m.material, { emissiveIntensity: 0.6, duration: 0.4 });
          m.material.color.setHex(C);
          m.material.emissive.setHex(C);
        });
      });

      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.08) * 1.2, 4, 13);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── QUICKSORT / PARTITION ─────────────────────────────────────────────────
  quicksort: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3.5, 12]);
      const vals   = [5, 2, 8, 1, 9, 3, 7, 4, 6];
      const pivotI = 4;
      const boxes  = [];
      vals.forEach((v, i) => {
        const isLeft  = i < pivotI;
        const isPivot = i === pivotI;
        const mat = isPivot ? matBright(0.9) : isLeft ? matCyan(0.4) : matDim(0.5);
        const m = box(scene, 0.9, 0.9, 0.6, mat, i * 1.15 - 4.7, -4, 0);
        boxes.push(m);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: i * 0.07, ease: 'back.out(1.4)' });
      });
      // Pivot line
      gsap.delayedCall(0.8, () => {
        const pivotLine = new THREE.Mesh(
          new THREE.BoxGeometry(0.05, 6, 0.05),
          new THREE.MeshStandardMaterial({ color: BRIGHT, emissive: BRIGHT, emissiveIntensity: 1 })
        );
        pivotLine.position.set(pivotI * 1.15 - 4.7, 0, 0);
        scene.add(pivotLine);
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.011;
        boxes.forEach((b, i) => { b.rotation.y = Math.sin(t * 0.7 + i * 0.5) * 0.05; });
        camera.position.set(Math.sin(t * 0.09) * 0.8, 3.5, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── STOCKCHART (Kadane / Best Stock) ─────────────────────────────────────
  stockchart: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 2, 12]);
      const prices = [42, 38, 55, 48, 65, 72, 58, 80, 74, 90];
      const scale  = 0.05;
      const pts    = prices.map((p, i) => new THREE.Vector3(i * 1.1 - 5, p * scale - 3.5, 0));
      const geo = new THREE.BufferGeometry().setFromPoints(pts);
      const line = new THREE.Line(geo,
        new THREE.LineBasicMaterial({ color: C, linewidth: 2 }));
      scene.add(line);
      prices.forEach((p, i) => {
        const m = sphere(scene, 0.18,
          i === 7 ? matBright(1) : matCyan(0.6),
          i * 1.1 - 5, p * scale - 3.5, 0);
        gsap.from(m.position, { y: -3.5, duration: 0.5, delay: i * 0.08 });
      });
      // Rising fill
      const fillPts = [...pts, new THREE.Vector3(pts[pts.length - 1].x, -3.5, 0), new THREE.Vector3(pts[0].x, -3.5, 0)];
      const fillGeo = new THREE.BufferGeometry().setFromPoints(fillPts);
      scene.add(new THREE.Line(fillGeo,
        new THREE.LineBasicMaterial({ color: DIM, transparent: true, opacity: 0.3 })));
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.08) * 0.6, 2, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── SLIDING WINDOW ────────────────────────────────────────────────────────
  windowslide: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const arr  = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3];
      const winW = 4;
      const boxes = [];
      arr.forEach((v, i) => {
        const m = box(scene, 0.92, 0.92, 0.6, matDark(), i * 1.1 - 4.9, -4, 0);
        boxes.push(m);
        gsap.to(m.position, { y: 0, duration: 0.4, delay: i * 0.06 });
      });
      // Sliding window highlight
      let winPos = 0;
      const highlightWindow = (pos) => {
        boxes.forEach((b, i) => {
          const inWin = i >= pos && i < pos + winW;
          gsap.to(b.material, { emissiveIntensity: inWin ? 0.7 : 0.1, duration: 0.3 });
          b.material.color.setHex(inWin ? C : DEEP);
          b.material.emissive.setHex(inWin ? C : 0x051a20);
        });
      };
      gsap.delayedCall(0.8, () => {
        highlightWindow(0);
        const slideInterval = setInterval(() => {
          if (!renderer.domElement.isConnected) { clearInterval(slideInterval); return; }
          winPos = (winPos + 1) % (arr.length - winW + 1);
          highlightWindow(winPos);
        }, 900);
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.08) * 0.6, 3, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── MIRROR / PALINDROME / XOR ─────────────────────────────────────────────
  mirror: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const vals = [1, 2, 3, 4, 5, 4, 3, 2, 1];
      const mid  = Math.floor(vals.length / 2);
      vals.forEach((v, i) => {
        const isMid  = i === mid;
        const isLeft = i < mid;
        const m = box(scene, 0.92, 0.92, isLeft ? 0.5 : 0.9,
          isMid ? matBright(0.9) : isLeft ? matCyan(0.4) : matDim(0.5),
          (i - mid) * 1.22, -4, 0);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: Math.abs(i - mid) * 0.1, ease: 'back.out(1.5)' });
      });
      // Mirror axis — vertical glowing line
      const axisGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, -3, 0), new THREE.Vector3(0, 3, 0)
      ]);
      scene.add(new THREE.Line(axisGeo,
        new THREE.LineDashedMaterial({ color: BRIGHT, dashSize: 0.2, gapSize: 0.1 })));
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.012;
        camera.position.set(Math.sin(t * 0.1) * 0.8, 3, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── GRID / MATRIX ─────────────────────────────────────────────────────────
  grid: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 7, 14]);
      const data = [
        [1, 0, 1, 1, 0, 1],
        [0, 1, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1]
      ];
      const cubes = [];
      data.forEach((row, r) => {
        row.forEach((v, c) => {
          const m = box(scene, 0.88, 0.88, 0.4,
            v ? matCyan(0.5) : matDark(),
            c * 1.05 - 2.6, r * -1.05 + 1.5, 0);
          cubes.push({ mesh: m, v });
          m.scale.y = 0.01;
          gsap.to(m.scale, { y: 1, duration: 0.4, delay: (r * 6 + c) * 0.04, ease: 'back.out' });
        });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        cubes.forEach(({ mesh, v }) => {
          if (v) mesh.material.emissiveIntensity = 0.4 + Math.sin(t * 2 + mesh.position.x + mesh.position.y) * 0.15;
        });
        camera.position.set(Math.sin(t * 0.08) * 1.5, 7, 14);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── MOUNTAIN / PEAK ───────────────────────────────────────────────────────
  mountain: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [2, 5, 13]);
      const heights = [0.2, 0.5, 1.0, 1.8, 2.8, 3.5, 2.6, 1.5, 0.8, 0.3];
      const bars = [];
      heights.forEach((h, i) => {
        const m = box(scene, 0.95, h, 0.8,
          i === 5 ? matBright(0.9) : matCyan(0.3 + h * 0.1),
          i * 1.1 - 5, h / 2 - 3.2, 0);
        bars.push(m);
        m.scale.y = 0.01;
        gsap.to(m.scale, { y: 1, duration: 0.7, delay: i * 0.07, ease: 'power2.out' });
      });
      // Peak marker
      const peak = sphere(scene, 0.25, matBright(1), 5 * 1.1 - 5, 3.5 - 3.2 + 0.4, 0);
      peak.scale.set(0, 0, 0);
      gsap.to(peak.scale, { x: 1, y: 1, z: 1, duration: 0.5, delay: 1.0, ease: 'elastic.out' });

      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        peak.position.y = (3.5 - 3.2 + 0.4) + Math.sin(t * 2) * 0.08;
        camera.position.set(2 + Math.sin(t * 0.1) * 0.5, 5, 13);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── BINARY SEARCH / LIBRARY ───────────────────────────────────────────────
  library: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const n = 10;
      const books = [];
      let lo = 0, hi = n - 1, mid = 4;
      for (let i = 0; i < n; i++) {
        const isLo = i === lo, isHi = i === hi, isMid = i === mid;
        const mat = isMid ? matBright(0.9) : isLo || isHi ? matCyan(0.6) : matDark();
        const m = box(scene, 0.75, 1.6, 0.22, mat, i * 0.9 - 4, -4, 0);
        books.push(m);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: i * 0.06, ease: 'back.out' });
      }
      // Highlight animation
      let step = 0;
      const bsSteps = [{ lo: 0, hi: 9, mid: 4 }, { lo: 5, hi: 9, mid: 7 }, { lo: 5, hi: 6, mid: 5 }];
      const doStep = () => {
        if (!renderer.domElement.isConnected) return;
        const s = bsSteps[step % bsSteps.length];
        books.forEach((b, i) => {
          const isLo = i === s.lo, isHi = i === s.hi, isMid = i === s.mid;
          const inRange = i >= s.lo && i <= s.hi;
          b.material.color.setHex(isMid ? BRIGHT : isLo || isHi ? C : inRange ? DIM : DEEP);
          b.material.emissive.setHex(isMid ? BRIGHT : isLo || isHi ? C : inRange ? DIM : 0x051a20);
          b.material.emissiveIntensity = isMid ? 0.9 : isLo || isHi ? 0.6 : inRange ? 0.2 : 0.1;
        });
        step++;
        setTimeout(doStep, 1200);
      };
      gsap.delayedCall(0.8, doStep);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.09) * 0.7, 3, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── FRACTAL TREE (Recursion) ──────────────────────────────────────────────
  fractal: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 2, 14]);
      scene.fog = new THREE.Fog(0x04090e, 20, 50);

      const branches = [];
      function addBranch(x1, y1, z1, x2, y2, z2, depth) {
        if (depth === 0) return;
        const pts = [new THREE.Vector3(x1, y1, z1), new THREE.Vector3(x2, y2, z2)];
        const geo = new THREE.BufferGeometry().setFromPoints(pts);
        const alpha = 0.2 + depth * 0.1;
        const line = new THREE.Line(geo,
          new THREE.LineBasicMaterial({ color: depth > 4 ? BRIGHT : C, transparent: true, opacity: alpha }));
        scene.add(line);
        branches.push({ line, depth });

        const dx = x2 - x1, dy = y2 - y1;
        const len = Math.sqrt(dx * dx + dy * dy) * 0.68;
        const angle1 = Math.atan2(dy, dx) + 0.45;
        const angle2 = Math.atan2(dy, dx) - 0.45;
        addBranch(x2, y2, z1, x2 + len * Math.cos(angle1), y2 + len * Math.sin(angle1), z1, depth - 1);
        addBranch(x2, y2, z1, x2 + len * Math.cos(angle2), y2 + len * Math.sin(angle2), z1, depth - 1);
      }

      addBranch(0, -3.5, 0, 0, -0.5, 0, 7);

      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.008;
        branches.forEach(({ line, depth }) => {
          const pulse = 0.2 + depth * 0.1 + Math.sin(t * 1.5 + depth) * 0.08;
          line.material.opacity = Math.max(0.05, Math.min(1, pulse));
        });
        camera.position.set(Math.sin(t * 0.1) * 1.5, 2, 14);
        camera.lookAt(0, 1, 0);
      });
    }
  },

  // ── CIRCUIT / LINKED LIST LOOP ────────────────────────────────────────────
  circuit: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 5, 13]);
      const n = 8, r = 3.2;
      const nodes = [], positions = [];
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2 - Math.PI / 2;
        const x = r * Math.cos(a), y = r * Math.sin(a) - 0.5;
        positions.push([x, y]);
        const m = sphere(scene, 0.42, i === 0 ? matBright(0.9) : matDark(), x, y, 0);
        nodes.push(m);
        m.scale.set(0, 0, 0);
        gsap.to(m.scale, { x: 1, y: 1, z: 1, duration: 0.4, delay: i * 0.1, ease: 'back.out' });
      }
      // Edges
      for (let i = 0; i < n; i++) {
        const [x1, y1] = positions[i];
        const [x2, y2] = positions[(i + 1) % n];
        glowLine(scene, [x1, y1, 0], [x2, y2, 0], DIM);
      }
      // Traveling pulse
      let pulseIdx = 0;
      const pulse = () => {
        if (!renderer.domElement.isConnected) return;
        nodes.forEach((nd, i) => {
          nd.material.color.setHex(i === pulseIdx ? C : DEEP);
          nd.material.emissive.setHex(i === pulseIdx ? C : 0x051a20);
          nd.material.emissiveIntensity = i === pulseIdx ? 0.9 : 0.1;
        });
        pulseIdx = (pulseIdx + 1) % n;
        setTimeout(pulse, 300);
      };
      gsap.delayedCall(1, pulse);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.1) * 0.6, 5, 13);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── DNA STRAND ────────────────────────────────────────────────────────────
  dna: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 0, 12]);
      const group = new THREE.Group();
      scene.add(group);
      const colors = [C, BRIGHT, DIM, 0x44aacc];
      for (let i = 0; i < 20; i++) {
        const t = (i / 20) * Math.PI * 4;
        const x = Math.cos(t) * 2, z = Math.sin(t) * 2, y = i * 0.38 - 3.5;
        sphere(group, 0.22, matColor(colors[i % 4], 0.5), x, y, z);
        sphere(group, 0.22, matColor(colors[(i + 2) % 4], 0.5), -x, y, -z);
        if (i < 19) glowLine(group, [x, y, z], [-x, y, -z], DIM);
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.012;
        group.rotation.y = t * 0.4;
        camera.position.set(Math.sin(t * 0.1) * 0.5, 0, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── BALANCE SCALE ─────────────────────────────────────────────────────────
  balance: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 12]);
      // Fulcrum post
      cylinder(scene, 0.12, 0.22, 4.5, matDim(0.4), 0, -1, 0);
      // Beam
      const beam = box(scene, 7, 0.12, 0.18, matCyan(0.5), 0, 1.5, 0);
      // Left pan & items
      const leftPan  = box(scene, 2.2, 0.1, 1.4, matDark(), -3.2, 0, 0);
      const rightPan = box(scene, 2.2, 0.1, 1.4, matDark(),  3.2, 0.6, 0);
      glowLine(scene, [-3.2, 1.5, 0], [-3.2, 0.1, 0], DIM);
      glowLine(scene, [3.2, 1.5, 0],  [3.2, 0.65, 0], DIM);
      // Weights
      box(scene, 0.7, 0.7, 0.7, matCyan(0.5), -3.2, 0.5, 0);
      box(scene, 0.5, 0.5, 0.5, matDim(0.4), 3.2, 1.2, 0);

      gsap.from(beam.rotation, { z: 0.2, duration: 1.2, ease: 'elastic.out(1, 0.4)' });

      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        beam.rotation.z = Math.sin(t * 0.6) * 0.06;
        leftPan.position.y  = 0 + Math.sin(t * 0.6) * -0.18;
        rightPan.position.y = 0.4 + Math.sin(t * 0.6) * 0.18;
        camera.position.set(Math.sin(t * 0.08) * 1, 4, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── TREE / BINARY TREE ────────────────────────────────────────────────────
  tree: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      const nodes = [
        { x: 0,    y: 2.5 }, { x: -2.5, y: 0.8 }, { x: 2.5,  y: 0.8 },
        { x: -3.6, y: -1 },  { x: -1.5, y: -1 },  { x: 1.5,  y: -1 }, { x: 3.6, y: -1 }
      ];
      const edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]];
      edges.forEach(([a, b]) => glowLine(scene,
        [nodes[a].x, nodes[a].y, 0], [nodes[b].x, nodes[b].y, 0], DIM));
      nodes.forEach((n, i) => {
        const m = sphere(scene, 0.42, i === 0 ? matBright(0.8) : matCyan(0.45), n.x, n.y, 0);
        m.scale.set(0, 0, 0);
        gsap.to(m.scale, { x: 1, y: 1, z: 1, duration: 0.4, delay: i * 0.12, ease: 'back.out(2)' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.09) * 1.2, 4, 14);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── HEAP ─────────────────────────────────────────────────────────────────
  heap: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      const nodes = [
        { x: 0, y: 2.5, v: 1 }, { x: -2.5, y: 0.8, v: 3 }, { x: 2.5, y: 0.8, v: 2 },
        { x: -3.6, y: -1, v: 7 }, { x: -1.5, y: -1, v: 4 }, { x: 1.5, y: -1, v: 5 }, { x: 3.6, y: -1, v: 6 }
      ];
      [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]].forEach(([a,b]) =>
        glowLine(scene, [nodes[a].x, nodes[a].y, 0], [nodes[b].x, nodes[b].y, 0], DIM));
      nodes.forEach((n, i) => {
        const m = sphere(scene, 0.42,
          i === 0 ? matBright(0.9) : i <= 2 ? matCyan(0.5) : matDim(0.4), n.x, n.y, 0);
        m.scale.set(0, 0, 0);
        gsap.to(m.scale, { x: 1, y: 1, z: 1, duration: 0.4, delay: i * 0.1, ease: 'back.out(2)' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.1) * 1.2, 4, 14);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── VENN DIAGRAM (Union / Intersection) ──────────────────────────────────
  venn: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 0, 12]);
      const leftGeo  = new THREE.TorusGeometry(2.2, 0.08, 12, 64);
      const rightGeo = new THREE.TorusGeometry(2.2, 0.08, 12, 64);
      const lTorus = new THREE.Mesh(leftGeo,  new THREE.MeshStandardMaterial({ color: C, emissive: C, emissiveIntensity: 0.5 }));
      const rTorus = new THREE.Mesh(rightGeo, new THREE.MeshStandardMaterial({ color: BRIGHT, emissive: BRIGHT, emissiveIntensity: 0.5 }));
      lTorus.position.x = -1.4; rTorus.position.x = 1.4;
      scene.add(lTorus); scene.add(rTorus);

      // Fill spheres
      for (let i = 0; i < 10; i++) {
        const a = Math.random() * Math.PI * 2, r = Math.random() * 1.6;
        sphere(scene, 0.18, matCyan(0.4), Math.cos(a) * r - 2.2, Math.sin(a) * r, 0.5);
      }
      for (let i = 0; i < 10; i++) {
        const a = Math.random() * Math.PI * 2, r = Math.random() * 1.6;
        sphere(scene, 0.18, matBright(0.4), Math.cos(a) * r + 2.2, Math.sin(a) * r, 0.5);
      }
      // Intersection
      for (let i = 0; i < 6; i++) {
        sphere(scene, 0.22, matColor(0x88ffee, 0.7), (Math.random() - 0.5) * 1.2, (Math.random() - 0.5) * 2.5, 0.5);
      }

      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        lTorus.rotation.z = t * 0.3; rTorus.rotation.z = -t * 0.3;
        camera.position.set(Math.sin(t * 0.1) * 0.5, 0, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── PODIUM (Largest / Top Elements) ──────────────────────────────────────
  podium: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const heights = [2.0, 3.2, 1.4];
      const xPos    = [-2, 0, 2];
      const mats    = [matDim(0.4), matBright(0.9), matCyan(0.4)];
      heights.forEach((h, i) => {
        const m = box(scene, 1.6, h, 1.4, mats[i], xPos[i], h / 2 - 3.2, 0);
        m.scale.y = 0.01;
        gsap.to(m.scale, { y: 1, duration: 0.8, delay: i * 0.2, ease: 'power2.out' });
        gsap.to(m.position, { y: h / 2 - 3.2, duration: 0.8, delay: i * 0.2, ease: 'power2.out' });
        // Trophy on top
        const trophy = sphere(scene, 0.3, mats[i], xPos[i], -4, 0);
        gsap.to(trophy.position, { y: h - 3.2 + 0.5, duration: 0.8, delay: i * 0.2 + 0.5, ease: 'back.out(2)' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t * 0.1) * 1, 3, 12);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── STACK ────────────────────────────────────────────────────────────────
  stack: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [2, 2, 11]);
      const items = [5, 3, 7, 1, 9];
      items.forEach((v, i) => {
        const m = box(scene, 2.6, 0.7, 1.6,
          i === items.length - 1 ? matBright(0.8) : matCyan(0.3 + i * 0.08),
          0, -4, 0);
        gsap.to(m.position, { y: i * 0.85 - 1.8, duration: 0.5, delay: i * 0.1, ease: 'back.out(1.4)' });
      });
      // Base
      box(scene, 3.2, 0.12, 2, matDim(0.3), 0, -2.2, 0);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(2 + Math.sin(t * 0.1) * 0.5, 2, 11);
        camera.lookAt(0, 0, 0);
      });
    }
  },

  // ── GPS / GRAPH NETWORK ───────────────────────────────────────────────────
  gps: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      const nds = [
        { x:-4, y:0 }, { x:-2, y:2.5 }, { x:-2, y:-2 },
        { x:1,  y:3 }, { x:1,  y:-1 },  { x:4, y:1 }
      ];
      const edges = [[0,1],[0,2],[1,3],[1,4],[2,4],[3,5],[4,5]];
      edges.forEach(([a,b]) => glowLine(scene, [nds[a].x,nds[a].y,0],[nds[b].x,nds[b].y,0], DIM));
      const spheres = nds.map((n, i) => {
        const m = sphere(scene, 0.38, i === 0 ? matCyan(0.8) : matDark(), n.x, n.y, 0);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: i*0.1, ease:'back.out(2)' });
        return m;
      });
      // BFS pulse
      const order = [0,1,2,3,4,5];
      let step = 0;
      const doPulse = () => {
        if (!renderer.domElement.isConnected) return;
        spheres.forEach((s, i) => {
          const visited = i <= step;
          s.material.color.setHex(i === step ? BRIGHT : visited ? C : DEEP);
          s.material.emissive.setHex(i === step ? BRIGHT : visited ? DIM : 0x051a20);
          s.material.emissiveIntensity = i === step ? 1 : visited ? 0.4 : 0.1;
        });
        step = (step + 1) % (nds.length + 1);
        if (step === 0) spheres.forEach(s => { s.material.color.setHex(DEEP); s.material.emissiveIntensity = 0.1; });
        setTimeout(doPulse, 500);
      };
      gsap.delayedCall(0.8, doPulse);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*1.2, 4, 14);
        camera.lookAt(0,0,0);
      });
    }
  },
  social: { draw(c,p) { VIZ_SCENES.gps.draw(c,p); } },

  // ── CAROUSEL (Rotate Array) ────────────────────────────────────────────────
  carousel: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 5, 13]);
      const n = 8, r = 3;
      const nodes = [];
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2;
        const x = r * Math.cos(a), z = r * Math.sin(a);
        const m = box(scene, 0.9, 0.9, 0.9, i === 0 ? matBright(0.8) : matCyan(0.35), x, 0, z);
        nodes.push(m);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: i*0.09, ease:'back.out' });
      }
      let t = 0, group = new THREE.Group();
      nodes.forEach(m => { scene.remove(m); group.add(m); });
      scene.add(group);
      animLoop(renderer, scene, camera, () => {
        t += 0.008;
        group.rotation.y = t * 0.5;
        camera.position.set(Math.sin(t*0.1)*0.5, 5, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── ELECTION / VOTES ──────────────────────────────────────────────────────
  votes: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const counts = [6, 9, 4, 7, 3];
      const colors = [C, BRIGHT, DIM, 0x44aacc, 0x2a7f8c];
      counts.forEach((v, i) => {
        const h = v * 0.4;
        const m = box(scene, 1, 0.01, 0.8, matColor(colors[i], 0.5), i * 1.4 - 2.8, -3.2, 0);
        m.scale.y = 0.01;
        gsap.to(m.scale, { y: h / 0.01, duration: 0.8, delay: i * 0.1, ease: 'power2.out' });
        gsap.to(m.position, { y: h / 2 - 3.2, duration: 0.8, delay: i * 0.1, ease: 'power2.out' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.8, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },
  election: { draw(c,p) { VIZ_SCENES.votes.draw(c,p); } },

  // ── SEATS (Missing Number) ────────────────────────────────────────────────
  seats: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      const n = 10, missingIdx = 6;
      for (let i = 0; i < n; i++) {
        const isMissing = i === missingIdx;
        const m = box(scene, 0.85, 0.85, 0.5,
          isMissing
            ? new THREE.MeshStandardMaterial({ color: 0x200808, emissive: 0xff2222, emissiveIntensity: 0.4, metalness: 0.5, roughness: 0.5, wireframe: false })
            : matCyan(0.3),
          i * 1.1 - 5, -4, 0);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: i * 0.07, ease: 'back.out' });
        if (isMissing) {
          gsap.to(m.material, { emissiveIntensity: 0.8, duration: 0.5, delay: 0.9, yoyo: true, repeat: -1 });
        }
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.09)*0.8, 4, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── TIMELINE / SCHEDULER ─────────────────────────────────────────────────
  timeline: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 2, 13]);
      const jobs = [{s:0,e:4},{s:3,e:7},{s:5,e:9},{s:1,e:10}];
      const colors = [C, BRIGHT, DIM, 0x44aacc];
      jobs.forEach((j, i) => {
        const w = (j.e - j.s) * 0.85;
        const x = j.s * 0.85 - 4.2 + w / 2;
        const m = box(scene, w, 0.7, 0.6, matColor(colors[i], 0.5), x, i * 1.0 - 1.5, 0);
        m.scale.x = 0.01;
        gsap.to(m.scale, { x: 1, duration: 0.6, delay: i * 0.2, ease: 'power2.out' });
      });
      // Axis
      glowLine(scene, [-4.5, -2.4, 0], [4.5, -2.4, 0], DIM);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.09)*0.6, 2, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── MAZE ─────────────────────────────────────────────────────────────────
  maze: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 8, 13]);
      const layout = [
        [0,1,0,0,0,1,0],[1,0,0,1,0,0,0],[0,0,1,0,0,1,0],[0,1,0,0,1,0,0],[0,0,0,1,0,0,0]
      ];
      layout.forEach((row, r) => row.forEach((wall, c) => {
        if (wall) {
          box(scene, 1, 1.2, 1, matDim(0.3), c * 1.1 - 3.3, r * -1.1 + 2.2, 0);
        } else {
          box(scene, 1, 0.1, 1, matDark(), c * 1.1 - 3.3, r * -1.1 + 2.2 - 0.55, 0);
        }
      }));
      // Start / End markers
      sphere(scene, 0.36, matCyan(0.9), -3.3, 2.2, 0.6);
      sphere(scene, 0.36, matBright(0.9), 3.3, -2.2, 0.6);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.009;
        camera.position.set(Math.sin(t*0.1)*1, 8, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── SHUFFLE (Permutations) ────────────────────────────────────────────────
  shuffle: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const n = 6;
      const boxes = [];
      for (let i = 0; i < n; i++) {
        const m = box(scene, 0.9, 0.9, 0.9, matCyan(0.4), i * 1.2 - 3, -4, 0);
        boxes.push(m);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: i * 0.08, ease: 'back.out' });
      }
      const doShuffle = () => {
        if (!renderer.domElement.isConnected) return;
        const a = Math.floor(Math.random() * n);
        const b = Math.floor(Math.random() * n);
        const tmpX = boxes[a].position.x;
        boxes[a].material.color.setHex(BRIGHT); boxes[a].material.emissive.setHex(BRIGHT);
        boxes[b].material.color.setHex(BRIGHT); boxes[b].material.emissive.setHex(BRIGHT);
        gsap.to(boxes[a].position, { y: 1.8, duration: 0.3, ease: 'power2.out',
          onComplete: () => {
            boxes[a].position.x = boxes[b].position.x;
            boxes[b].position.x = tmpX;
            gsap.to(boxes[a].position, { y: 0, duration: 0.3, ease: 'power2.in' });
            gsap.to(boxes[b].position, { y: 0, duration: 0.3, ease: 'power2.in',
              onComplete: () => {
                boxes[a].material.color.setHex(C); boxes[a].material.emissive.setHex(C);
                boxes[b].material.color.setHex(C); boxes[b].material.emissive.setHex(C);
                setTimeout(doShuffle, 700);
              }
            });
          }
        });
      };
      gsap.delayedCall(0.9, doShuffle);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── CLOCK (Roman Numerals / Circular) ────────────────────────────────────
  clock: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 0, 11]);
      // Dial
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(3.2, 0.1, 12, 64),
        new THREE.MeshStandardMaterial({ color: C, emissive: C, emissiveIntensity: 0.4 })
      );
      scene.add(ring);
      // Hour ticks
      for (let i = 0; i < 12; i++) {
        const a = (i / 12) * Math.PI * 2;
        box(scene, 0.12, 0.5, 0.12, matDim(0.5), Math.sin(a) * 2.8, Math.cos(a) * 2.8, 0);
      }
      // Hands
      const hourHand = box(scene, 0.12, 1.8, 0.12, matCyan(0.7), 0, 0.9, 0.1);
      const minHand  = box(scene, 0.08, 2.5, 0.08, matBright(0.6), 0, 1.25, 0.1);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.012;
        hourHand.rotation.z = -t * 0.08;
        minHand.rotation.z  = -t * 0.5;
        ring.rotation.z = t * 0.05;
        camera.position.set(Math.sin(t*0.08)*0.4, 0, 11);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── PARTICLES (Centrifuge / Move Zeros) ───────────────────────────────────
  particles: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 2, 13]);
      const pts = [];
      const velocities = [];
      const geo = new THREE.BufferGeometry();
      const n = 120;
      const positions = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        positions[i*3]   = (Math.random() - 0.5) * 8;
        positions[i*3+1] = (Math.random() - 0.5) * 4;
        positions[i*3+2] = (Math.random() - 0.5) * 2;
        velocities.push({ x: (Math.random() - 0.5) * 0.04, y: (Math.random() - 0.5) * 0.03, vx:0, vy:0 });
      }
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      const particles = new THREE.Points(geo,
        new THREE.PointsMaterial({ color: C, size: 0.18, transparent: true, opacity: 0.8 }));
      scene.add(particles);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.014;
        const pos = particles.geometry.attributes.position.array;
        for (let i = 0; i < n; i++) {
          pos[i*3]   += velocities[i].x;
          pos[i*3+1] += velocities[i].y;
          if (Math.abs(pos[i*3]) > 4.5) velocities[i].x *= -1;
          if (Math.abs(pos[i*3+1]) > 2.2) velocities[i].y *= -1;
        }
        particles.geometry.attributes.position.needsUpdate = true;
        particles.rotation.z = t * 0.1;
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── SEARCHBEAM (Linear Search / Flashlight) ───────────────────────────────
  searchbeam: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const n = 10, targetIdx = 6;
      const boxes = [];
      for (let i = 0; i < n; i++) {
        const m = box(scene, 0.85, 0.85, 0.5, matDark(), i * 1.05 - 4.7, -4, 0);
        boxes.push(m);
        gsap.to(m.position, { y: 0, duration: 0.4, delay: i * 0.06 });
      }
      let scanIdx = 0;
      const scan = () => {
        if (!renderer.domElement.isConnected) return;
        boxes.forEach((b, i) => {
          const isCurrent = i === scanIdx;
          const isTarget  = i === targetIdx && scanIdx >= targetIdx;
          b.material.color.setHex(isTarget ? BRIGHT : isCurrent ? C : i < scanIdx ? DIM : DEEP);
          b.material.emissive.setHex(isTarget ? BRIGHT : isCurrent ? C : i < scanIdx ? 0x1a4a50 : 0x051a20);
          b.material.emissiveIntensity = isTarget ? 1 : isCurrent ? 0.9 : i < scanIdx ? 0.2 : 0.08;
        });
        if (scanIdx < n) { scanIdx++; setTimeout(scan, 280); }
        else { scanIdx = 0; setTimeout(() => gsap.delayedCall(0.5, scan), 1500); }
      };
      gsap.delayedCall(0.8, scan);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── RACETRACK (Time Complexity) ───────────────────────────────────────────
  racetrack: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      // Track ring
      scene.add(new THREE.Mesh(
        new THREE.TorusGeometry(3.5, 0.3, 12, 64),
        new THREE.MeshStandardMaterial({ color: DIM, emissive: DIM, emissiveIntensity: 0.2 })
      ));
      // Cars (algorithms)
      const cars = [
        { r: 3.5, speed: 0.04, color: BRIGHT, startAngle: 0 },  // O(1)
        { r: 3.5, speed: 0.025, color: C,     startAngle: 2 },  // O(log n)
        { r: 3.5, speed: 0.012, color: DIM,   startAngle: 4 },  // O(n)
      ];
      const carMeshes = cars.map(c => {
        const m = box(scene, 0.45, 0.25, 0.7, matColor(c.color, 0.8),
          c.r * Math.cos(c.startAngle), 0, c.r * Math.sin(c.startAngle));
        return { mesh: m, ...c, angle: c.startAngle };
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.016;
        carMeshes.forEach(c => {
          c.angle += c.speed;
          c.mesh.position.x = c.r * Math.cos(c.angle);
          c.mesh.position.z = c.r * Math.sin(c.angle);
          c.mesh.rotation.y = -c.angle + Math.PI / 2;
        });
        camera.position.set(Math.sin(t*0.1)*1, 4, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── TRIANGLE (Pascal's Triangle) ─────────────────────────────────────────
  triangle: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      const rows = 5;
      const pascal = [[1]];
      for (let r = 1; r < rows; r++) {
        const prev = pascal[r-1];
        pascal.push([1, ...prev.slice(0,-1).map((v,i) => v + prev[i+1]), 1]);
      }
      pascal.forEach((row, r) => {
        row.forEach((val, c) => {
          const x = (c - row.length / 2 + 0.5) * 1.4;
          const y = (rows - 1 - r) * 1.2 - 1;
          const m = sphere(scene, 0.38, r === 0 ? matBright(0.8) : matCyan(0.3 + r * 0.05), x, y, 0);
          m.scale.set(0,0,0);
          gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: r * 0.15 + c * 0.05, ease:'back.out' });
        });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*1, 4, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── SPIRAL ────────────────────────────────────────────────────────────────
  spiral: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      const pts = [];
      const n = 36;
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 6;
        const r = 0.3 + i * 0.12;
        pts.push(new THREE.Vector3(r * Math.cos(a), i * 0.18 - 2.5, r * Math.sin(a)));
      }
      const geo = new THREE.BufferGeometry().setFromPoints(pts);
      scene.add(new THREE.Line(geo, new THREE.LineBasicMaterial({ color: C })));
      pts.forEach((p, i) => {
        const m = sphere(scene, 0.18, matCyan(0.5 + i * 0.01), p.x, p.y, p.z);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.3, delay: i * 0.04 });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.15)*2, 3 + Math.sin(t*0.12)*1, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── BUILDING (Nesting / Floors) ───────────────────────────────────────────
  building: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [2, 3, 12]);
      const floors = [4.2, 3.1, 2.4, 1.8, 1.2];
      floors.forEach((w, i) => {
        const m = box(scene, w, 0.62, 1.2, matCyan(0.25 + i * 0.06), 0, -4, 0);
        gsap.to(m.position, { y: i * 0.75 - 1.5, duration: 0.5, delay: i * 0.1, ease: 'back.out' });
      });
      // Antenna
      const ant = box(scene, 0.1, 1.4, 0.1, matBright(0.9), 0, -4, 0);
      gsap.to(ant.position, { y: floors.length * 0.75 - 1.5 + 0.8, duration: 0.5, delay: 0.6 });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(2 + Math.sin(t*0.1)*0.5, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── CONVEYOR (For Loop / Factory) ────────────────────────────────────────
  conveyor: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      // Belt
      box(scene, 10, 0.18, 1.4, matDim(0.3), 0, -0.5, 0);
      // Rollers
      for (let i = -4; i <= 4; i++)
        cylinder(scene, 0.22, 0.22, 1.5, matDim(0.2), i * 1.0, -0.7, 0);
      // Items moving
      const items = [];
      for (let i = 0; i < 5; i++) {
        const m = box(scene, 0.7, 0.7, 0.9, matCyan(0.4 + i * 0.06), i * 1.8 - 4, 0.22, 0);
        items.push(m);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: i * 0.12 });
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        items.forEach(m => {
          m.position.x -= 0.018;
          if (m.position.x < -5.5) m.position.x = 5.5;
        });
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── TRAFFIC LIGHT ─────────────────────────────────────────────────────────
  traffic: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 1, 10]);
      // Post
      cylinder(scene, 0.15, 0.15, 5, matDark(), 0, -1, 0);
      // Box
      box(scene, 1.2, 3.2, 0.7, matDark(), 0, 1.2, 0);
      // Lights
      const lightColors = [0xff3333, 0xffaa00, 0x33ff66];
      const emissives   = [0xff0000, 0xff8800, 0x00ff44];
      const lights = lightColors.map((col, i) => {
        const m = sphere(scene, 0.32,
          new THREE.MeshStandardMaterial({ color: i === 0 ? col : 0x111111, emissive: i === 0 ? emissives[i] : 0x000000, emissiveIntensity: i===0?0.9:0, metalness:0.3, roughness:0.5 }),
          0, 2.2 - i * 1.0, 0.3);
        return m;
      });
      let activeLight = 0;
      const cycle = () => {
        if (!renderer.domElement.isConnected) return;
        lights.forEach((l, i) => {
          l.material.color.setHex(i === activeLight ? lightColors[i] : 0x111111);
          l.material.emissive.setHex(i === activeLight ? emissives[i] : 0x000000);
          l.material.emissiveIntensity = i === activeLight ? 0.9 : 0;
        });
        activeLight = (activeLight + 1) % 3;
        setTimeout(cycle, activeLight === 1 ? 800 : 1400);
      };
      gsap.delayedCall(0.5, cycle);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.4, 1, 10);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── ELEVATOR (Floor / Ceil) ────────────────────────────────────────────────
  elevator: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [2, 1, 12]);
      // Shaft
      box(scene, 2.2, 8, 0.1, matDark(), 0, 0, -0.5);
      box(scene, 0.08, 8, 2, matDim(0.2), -1.1, 0, 0);
      box(scene, 0.08, 8, 2, matDim(0.2),  1.1, 0, 0);
      // Floor lines
      for (let f = -3; f <= 3; f++) {
        box(scene, 2.2, 0.06, 2, matDim(0.15), 0, f * 1.15, 0);
      }
      // Car
      const car = box(scene, 1.8, 1.0, 1.6, matCyan(0.5), 0, -4, 0);
      gsap.to(car.position, { y: -1.15, duration: 1.2, ease: 'power2.inOut',
        onComplete: () => gsap.to(car.position, { y: 1.15, duration: 1.0, ease: 'power2.inOut',
          onComplete: () => gsap.to(car.position, { y: 0, duration: 0.8, ease: 'power2.inOut' })
        })
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(2 + Math.sin(t*0.1)*0.3, 1, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── DEDUP (Remove Duplicates) ─────────────────────────────────────────────
  dedup: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const vals      = [1, 1, 2, 3, 3, 3, 4, 5, 5];
      const isDup     = [0, 1, 0, 0, 1, 1, 0, 0, 1];
      const boxes = vals.map((v, i) => {
        const m = box(scene, 0.88, 0.88, 0.5,
          isDup[i] ? new THREE.MeshStandardMaterial({ color: 0x3a1010, emissive: 0xcc3333, emissiveIntensity: 0.4, metalness:0.6, roughness:0.3 })
                   : matCyan(0.4),
          i * 1.08 - 4.3, -4, 0);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: i * 0.07, ease: 'back.out' });
        return { mesh: m, isDup: isDup[i] };
      });
      gsap.delayedCall(1.0, () => {
        boxes.filter(b => b.isDup).forEach(b => {
          gsap.to(b.mesh.scale, { y: 0, duration: 0.4, ease: 'power2.in' });
          gsap.to(b.mesh.position, { y: 3, duration: 0.4, ease: 'power2.in' });
        });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── SPIRAL MATRIX ─────────────────────────────────────────────────────────
  camera: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 6, 14]);
      const n = 5;
      const cubes = [];
      for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
        const m = box(scene, 0.84, 0.84, 0.3, matDark(), c * 1.0 - 2, r * -1.0 + 2, 0);
        cubes.push({ mesh: m, r, c });
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.3, delay: (r*n+c)*0.04 });
      }
      // Spiral highlight
      const spiralOrder = generateSpiral(n);
      let step = 0;
      const doSpiral = () => {
        if (!renderer.domElement.isConnected) return;
        cubes.forEach(({ mesh }, i) => {
          const pos = spiralOrder.indexOf(i);
          const lit = pos <= step;
          mesh.material.color.setHex(pos === step ? BRIGHT : lit ? C : DEEP);
          mesh.material.emissive.setHex(pos === step ? BRIGHT : lit ? DIM : 0x051a20);
          mesh.material.emissiveIntensity = pos === step ? 1 : lit ? 0.4 : 0.08;
        });
        step = (step + 1) % (n * n + 1);
        if (step === n*n) setTimeout(() => { step = 0; }, 1000);
        setTimeout(doSpiral, 160);
      };
      gsap.delayedCall(0.8, doSpiral);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.09)*0.8, 6, 14);
        camera.lookAt(0,0,0);
      });
    }
  },
  spiral: {
    draw(container, problem) { VIZ_SCENES.camera.draw(container, problem); }
  },

  // ── TEAMS (Sign Alternation) ──────────────────────────────────────────────
  teams: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const pattern = [1, -1, 1, -1, 1, -1, 1, -1];
      pattern.forEach((sign, i) => {
        const m = box(scene, 0.9, 0.9, 0.6,
          sign > 0 ? matCyan(0.6) : matBright(0.6),
          i * 1.15 - 4.0, -4, 0);
        gsap.to(m.position, { y: 0, duration: 0.5, delay: i * 0.1, ease: 'back.out(1.5)' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },
  flag: { draw(c,p) { VIZ_SCENES.teams.draw(c,p); } },

  // ── MARKET (Two Sum / k-Sum) ──────────────────────────────────────────────
  market: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      const prices = [2, 7, 4, 3, 8, 5, 1, 6];
      const target = [0, 4]; // indices that sum to target
      prices.forEach((v, i) => {
        const isMatch = target.includes(i);
        const h = v * 0.45;
        const m = box(scene, 0.92, h, 0.7,
          isMatch ? matBright(0.9) : matCyan(0.3),
          i * 1.1 - 4, h / 2 - 3, 0);
        m.scale.y = 0.01;
        gsap.to(m.scale, { y: 1, duration: 0.6, delay: i * 0.08, ease: 'power2.out' });
        gsap.to(m.position, { y: h / 2 - 3, duration: 0.6, delay: i * 0.08 });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── POWERLINE (Consecutive Ones) ──────────────────────────────────────────
  powerline: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      const bits = [1, 1, 0, 1, 1, 1, 1, 0, 1, 1];
      const bestStart = 3, bestEnd = 6;
      bits.forEach((b, i) => {
        const isBest = i >= bestStart && i <= bestEnd;
        const m = cylinder(scene, 0.28, 0.28, b ? (isBest ? 2.2 : 1.4) : 0.3,
          isBest ? matBright(0.9) : b ? matCyan(0.5) : matDark(),
          i * 1.05 - 5, b ? (isBest ? 0.1 : -0.3) : -1.3, 0);
        m.scale.y = 0.01;
        gsap.to(m.scale, { y: 1, duration: 0.5, delay: i * 0.07, ease: 'power2.out' });
        if (b) glowLine(scene, [i * 1.05 - 5, 1, 0], [(i+1) * 1.05 - 5, 1, 0], i >= bestStart && i < bestEnd ? BRIGHT : DIM);
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── CARDS (Insertion Sort) ────────────────────────────────────────────────
  cards: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 12]);
      const vals = [7, 2, 9, 4, 1, 8, 3, 6];
      const boxes = [];
      vals.forEach((v, i) => {
        const m = box(scene, 0.8, 1.2, 0.08, matCyan(0.3 + (i % 3) * 0.1),
          i * 1.1 - 4.3, v * 0.2 - 2, i * 0.05);
        boxes.push(m);
        m.scale.set(0, 0.01, 1);
        gsap.to(m.scale, { y: 1, duration: 0.4, delay: i * 0.1, ease: 'power2.out' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        boxes.forEach((b, i) => { b.rotation.z = Math.sin(t * 0.5 + i * 0.7) * 0.04; });
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── WAREHOUSE / SHELVES ───────────────────────────────────────────────────
  warehouse: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [2, 2, 14]);
      const shelves = 4, cols = 5;
      for (let r = 0; r < shelves; r++) {
        box(scene, cols * 1.3, 0.1, 1.2, matDim(0.2), 0, r * 1.4 - 2, 0);
        for (let c = 0; c < cols; c++) {
          const m = box(scene, 0.9, 0.9, 0.9,
            matColor(r % 2 === 0 ? C : BRIGHT, 0.3 + Math.random() * 0.2),
            c * 1.3 - 2.6, r * 1.4 - 2 + 0.55, 0);
          m.scale.set(0,0,0);
          gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: (r * cols + c) * 0.04 });
        }
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(2 + Math.sin(t*0.1)*0.6, 2, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── POSTAL / RADIX SORT ───────────────────────────────────────────────────
  postal: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 14]);
      const bins = 10;
      for (let i = 0; i < bins; i++) {
        box(scene, 0.95, 1.8, 0.8, matDark(), i * 1.08 - 4.8, -2, 0);
        const n = Math.floor(Math.random() * 3) + 1;
        for (let j = 0; j < n; j++) {
          const m = box(scene, 0.7, 0.55, 0.6, matCyan(0.3 + j * 0.1), i * 1.08 - 4.8, j * 0.62 - 2.2, 0);
          m.scale.set(0,0,0);
          gsap.to(m.scale, { x:1,y:1,z:1, duration:0.3, delay: i * 0.06 + j * 0.1 });
        }
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.8, 3, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── CALENDAR (Streak) ─────────────────────────────────────────────────────
  calendar: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 5, 14]);
      const weeks = 6, days = 7;
      const streak = [14, 15, 16, 17, 18, 19, 20, 21];
      for (let w = 0; w < weeks; w++) for (let d = 0; d < days; d++) {
        const idx = w * days + d;
        const isStreak = streak.includes(idx);
        const m = box(scene, 0.82, 0.82, 0.3,
          isStreak ? matBright(0.8) : matDark(),
          d * 1.0 - 3, w * -1.0 + 2.5, 0);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.3, delay: (w*days+d)*0.02 });
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.09)*1, 5, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── SHIPPING (Container / Capacity) ──────────────────────────────────────
  shipping: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [2, 3, 12]);
      // Container shell
      box(scene, 7, 3.5, 3, matDark(), 0, 0, 0);
      box(scene, 6.8, 3.3, 2.8,
        new THREE.MeshStandardMaterial({ color: 0x04090e, emissive: DIM, emissiveIntensity: 0.05, transparent: true, opacity: 0.3 }),
        0, 0, 0);
      // Packages inside
      const positions = [[-2.2,-0.8,-0.5],[-2.2,-0.8,0.5],[-2.2,0.2,0],[-0.8,-0.8,0],[0.6,-0.8,-0.5],[0.6,-0.8,0.5]];
      positions.forEach((pos, i) => {
        const m = box(scene, 1.0, 0.9, 0.85, matCyan(0.4 + i * 0.06), ...pos);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: i * 0.1, ease: 'back.out' });
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(2 + Math.sin(t*0.08)*0.8, 3, 12);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── FIELD (Aggressive Cows / Spacing) ────────────────────────────────────
  field: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 4, 14]);
      // Ground
      box(scene, 12, 0.1, 4, matDark(), 0, -1.5, 0);
      // Stalls
      const positions = [-5, -3, 0, 2, 4];
      positions.forEach((x, i) => box(scene, 0.5, 1.5, 0.5, matDim(0.3), x, -0.75, 0));
      // Cows placed
      const cowPos = [-5, 0, 4];
      cowPos.forEach((x, i) => {
        const m = sphere(scene, 0.5, matBright(0.7), x, -4, 0);
        gsap.to(m.position, { y: -0.6, duration: 0.6, delay: i * 0.2, ease: 'bounce.out' });
        // Distance indicator
        if (i < cowPos.length - 1) {
          glowLine(scene, [x, 0.2, 0.8], [cowPos[i+1], 0.2, 0.8], C);
        }
      });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*1, 4, 14);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── GARDEN (Flowers / Min Days) ────────────────────────────────────────────
  garden: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      const positions = [[-4,0],[-2.5,0.5],[-1,0],[0.5,0.3],[2,0],[3.5,0.2]];
      const blooms = [0, 1, 3, 4]; // bloomed flowers
      positions.forEach(([x, z], i) => {
        cylinder(scene, 0.08, 0.08, 1.2, matDim(0.4), x, -1.4, z);
        const m = sphere(scene, 0.38, blooms.includes(i) ? matBright(0.8) : matDim(0.2), x, -4, z);
        gsap.to(m.position, { y: -0.6, duration: 0.6, delay: i * 0.15, ease: 'bounce.out' });
      });
      box(scene, 10, 0.12, 4, matDark(), 0, -2, 0);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.12)*0.6, 3, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── TERMINAL (Input/Output) ────────────────────────────────────────────────
  terminal: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 1, 10]);
      // Screen frame
      box(scene, 7, 4.5, 0.3, matDim(0.2), 0, 0.5, 0);
      // Screen inner
      box(scene, 6.5, 4, 0.15,
        new THREE.MeshStandardMaterial({ color: 0x020d08, emissive: C, emissiveIntensity: 0.06 }),
        0, 0.5, 0.1);
      // Text lines (floating boxes)
      for (let i = 0; i < 5; i++) {
        const w = 2 + Math.random() * 2.5;
        const m = box(scene, w, 0.18, 0.05, matCyan(0.5 + i * 0.05),
          -2.5 + w / 2, 2 - i * 0.68, 0.25);
        m.scale.x = 0;
        gsap.to(m.scale, { x: 1, duration: 0.4, delay: 0.3 + i * 0.2, ease: 'power2.out' });
      }
      // Cursor blink
      const cursor = box(scene, 0.14, 0.18, 0.05, matBright(1), -1.5, -1.0, 0.25);
      gsap.to(cursor.material, { emissiveIntensity: 0, duration: 0.5, repeat: -1, yoyo: true });
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.4, 1, 10);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── WATCHMAN (While Loop / Guard) ─────────────────────────────────────────
  watchman: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 2, 11]);
      // Guard body
      cylinder(scene, 0.35, 0.45, 1.8, matDim(0.4), 0, -0.4, 0);
      sphere(scene, 0.45, matCyan(0.5), 0, 0.85, 0);
      // Spotlight beam
      const beamGeo = new THREE.ConeGeometry(1.8, 4, 12, 1, true);
      const beam = new THREE.Mesh(beamGeo,
        new THREE.MeshStandardMaterial({ color: BRIGHT, emissive: BRIGHT, emissiveIntensity: 0.3, transparent: true, opacity: 0.15, side: THREE.DoubleSide }));
      beam.position.set(0, 0.85, 2);
      beam.rotation.x = -Math.PI / 2;
      scene.add(beam);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        beam.rotation.z = Math.sin(t * 0.8) * 0.6;
        camera.position.set(Math.sin(t*0.1)*0.4, 2, 11);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── COURIER (Pass by Value/Ref) ───────────────────────────────────────────
  courier: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      // Two "memory slots"
      box(scene, 2.4, 2.4, 1.2, matDark(), -3, 0, 0);
      box(scene, 2.4, 2.4, 1.2, matDark(),  3, 0, 0);
      // Package (copy)
      const pkg = box(scene, 0.9, 0.9, 0.9, matCyan(0.6), -3, 0, 0.8);
      gsap.to(pkg.position, { x: 3, duration: 1.2, delay: 0.5, ease: 'power2.inOut',
        onComplete: () => gsap.to(pkg.position, { x: -3, duration: 0, delay: 0.5 }) });
      gsap.to(pkg.position, { repeat: -1, x: 3, duration: 1.2, delay: 1.5, ease: 'power2.inOut' });
      // Arrow
      glowLine(scene, [-1.5, 0, 0.8], [1.5, 0, 0.8], DIM);
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        camera.position.set(Math.sin(t*0.1)*0.6, 3, 13);
        camera.lookAt(0,0,0);
      });
    }
  },

  // ── DEFAULT ───────────────────────────────────────────────────────────────
  default: {
    draw(container, problem) {
      const { renderer, scene, camera } = setup3D(container, [0, 3, 13]);
      // Floating nodes connected in a general network
      const n = 9;
      const nodes = [];
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2;
        const r = 2.5 + Math.sin(i * 1.3) * 0.8;
        const x = r * Math.cos(a), y = Math.sin(i * 0.9) * 1.2, z = r * Math.sin(a) * 0.6;
        const m = sphere(scene, 0.35, i % 3 === 0 ? matBright(0.7) : matCyan(0.4), x, y, z);
        m.scale.set(0,0,0);
        gsap.to(m.scale, { x:1,y:1,z:1, duration:0.4, delay: i*0.1, ease:'back.out' });
        nodes.push({ mesh: m, x, y, z });
      }
      for (let i = 0; i < n; i++) {
        const a = nodes[i], b = nodes[(i+1) % n];
        glowLine(scene, [a.x, a.y, a.z], [b.x, b.y, b.z], DIM);
      }
      let t = 0;
      animLoop(renderer, scene, camera, () => {
        t += 0.01;
        nodes.forEach(({ mesh }, i) => {
          mesh.position.y += Math.sin(t * 1.5 + i * 0.7) * 0.004;
        });
        camera.position.set(Math.sin(t*0.15)*2, 3 + Math.sin(t*0.1)*0.5, 13);
        camera.lookAt(0,0,0);
      });
    }
  }

};

// ── ALIASES ──────────────────────────────────────────────────────────────────

const aliases = {
  mergesort: 'mergesort', quicksort: 'quicksort', leaderboard: 'leaderboard',
  bubbles: 'bubbles',     maze: 'maze',           fractal: 'fractal',
  podium: 'podium',       heap: 'heap',           stack: 'stack',
  conveyor: 'conveyor',   racetrack: 'racetrack', dna: 'dna',
  windowslide: 'windowslide', stockchart: 'stockchart', circuit: 'circuit',
  gps: 'gps', social: 'gps', market: 'market', balance: 'balance',
  timeline: 'timeline',   venn: 'venn',           tree: 'tree',
  mountain: 'mountain',   mirror: 'mirror',       grid: 'grid',
  library: 'library',     seats: 'seats',         spiral: 'spiral',
  camera: 'camera',       triangle: 'triangle',   building: 'building',
  carousel: 'carousel',   votes: 'votes',         election: 'votes',
  flag: 'flag',           teams: 'teams',         powerline: 'powerline',
  cards: 'cards',         dedup: 'dedup',         searchbeam: 'searchbeam',
  warehouse: 'warehouse', postal: 'postal',       calendar: 'calendar',
  shipping: 'shipping',   field: 'field',         garden: 'garden',
  terminal: 'terminal',   watchman: 'watchman',   courier: 'courier',
  traffic: 'traffic',     elevator: 'elevator',   clock: 'clock',
  particles: 'particles', train: 'train',         fractal: 'fractal',
  shuffle: 'shuffle',     array: 'array',
};

// Resolve aliases so every key returns a valid scene
Object.keys(aliases).forEach(key => {
  if (!VIZ_SCENES[key] && VIZ_SCENES[aliases[key]]) {
    VIZ_SCENES[key] = VIZ_SCENES[aliases[key]];
  }
});

// ── HELPERS ───────────────────────────────────────────────────────────────────

function generateSpiral(n) {
  const mat = Array.from({ length: n }, () => Array(n).fill(-1));
  const order = [];
  let top = 0, bottom = n - 1, left = 0, right = n - 1, num = 0;
  while (top <= bottom && left <= right) {
    for (let c = left; c <= right; c++) { mat[top][c] = num++; order.push(top * n + c); }
    top++;
    for (let r = top; r <= bottom; r++) { mat[r][right] = num++; order.push(r * n + right); }
    right--;
    if (top <= bottom) { for (let c = right; c >= left; c--) { mat[bottom][c] = num++; order.push(bottom * n + c); } bottom--; }
    if (left <= right) { for (let r = bottom; r >= top; r--) { mat[r][left] = num++; order.push(r * n + left); } left++; }
  }
  return order;
}
