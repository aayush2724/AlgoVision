import * as THREE from 'three';

/* ── DESIGN TOKENS ───────────────────────────────────────────── */
const C       = 0x5fd6e6;   // cyan
const CBRIGHT = 0xa9f0fa;   // bright cyan
const CDIM    = 0x2a7f8c;   // muted cyan
const CDEEP   = 0x0c2a31;   // deep cyan
const CACC    = 0xff6b00;   // orange accent
const BG      = 0x03080f;   // near-black
const GREEN   = 0x4ade80;
const YELLOW  = 0xfbbf24;
const RED     = 0xf87171;
const WHITE   = 0xdffafe;

/* ── SHARED RENDERER SETUP ───────────────────────────────────── */
function createRenderer(container) {
  // Dispose any existing Three.js scene on this container
  if (container._vizDispose) {
    container._vizDispose();
    container._vizDispose = null;
  }
  container.innerHTML = '';

  const w = container.offsetWidth  ||
            container.parentElement?.offsetWidth || 640;
  const h = Math.max(320, Math.round(w * 0.52));

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setSize(w, h, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(BG, 1);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type    = THREE.PCFSoftShadowMap;

  Object.assign(renderer.domElement.style, {
    width: '100%', height: `${h}px`,
    display: 'block', maxWidth: '100%',
  });
  container.appendChild(renderer.domElement);

  // Resize observer
  let resizeTimer;
  const ro = new ResizeObserver(() => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      const nw = container.offsetWidth;
      if (!nw) return;
      const nh = Math.max(320, Math.round(nw * 0.52));
      renderer.setSize(nw, nh, false);
      renderer.domElement.style.height = `${nh}px`;
    }, 100);
  });
  ro.observe(container);

  return { renderer, w, h, ro };
}

function createCamera(w, h, pos = [0, 12, 22], target = [0, 0, 0]) {
  const cam = new THREE.PerspectiveCamera(50, w / h, 0.1, 500);
  cam.position.set(...pos);
  cam.lookAt(...target);
  return cam;
}

function addLights(scene) {
  scene.add(new THREE.AmbientLight(0x0d1f2d, 3));
  const sun = new THREE.DirectionalLight(WHITE, 0.8);
  sun.position.set(10, 20, 10);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  scene.add(sun);
  const fill = new THREE.PointLight(C, 60, 40);
  fill.position.set(-8, 8, 8);
  scene.add(fill);
  const rim = new THREE.PointLight(CACC, 20, 30);
  rim.position.set(0, -4, -10);
  scene.add(rim);
}

function addGrid(scene, size = 30, color = CDEEP) {
  const g = new THREE.GridHelper(size, size, color, 0x080f14);
  g.position.y = -0.01;
  scene.add(g);
  return g;
}

function mat(color, emissive = 0, intensity = 0.4, opts = {}) {
  return new THREE.MeshStandardMaterial({
    color, emissive: emissive || color,
    emissiveIntensity: intensity,
    roughness: 0.6, metalness: 0.3,
    ...opts
  });
}

function box(scene, w, h, d, material, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
  m.position.set(x, y + h / 2, z);
  m.castShadow = true;
  m.receiveShadow = true;
  scene.add(m);
  return m;
}

function sphere(scene, r, material, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), material);
  m.position.set(x, y, z);
  m.castShadow = true;
  scene.add(m);
  return m;
}

function cylinder(scene, rTop, rBot, h, material, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rTop, rBot, h, 16), material);
  m.position.set(x, y, z);
  m.castShadow = true;
  scene.add(m);
  return m;
}

function tube(scene, from, to, radius = 0.08, color = CDIM) {
  const dir   = new THREE.Vector3().subVectors(
    new THREE.Vector3(...to), new THREE.Vector3(...from)
  );
  const len   = dir.length();
  const mid   = new THREE.Vector3(...from).addScaledVector(dir, 0.5);
  const m     = new THREE.Mesh(
    new THREE.CylinderGeometry(radius, radius, len, 8),
    mat(color, color, 0.3)
  );
  m.position.copy(mid);
  m.quaternion.setFromUnitVectors(
    new THREE.Vector3(0, 1, 0),
    dir.clone().normalize()
  );
  scene.add(m);
  return m;
}

function label3D(text, color = CBRIGHT, scale = 1) {
  const canvas = document.createElement('canvas');
  canvas.width = 256; canvas.height = 64;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = `#${color.toString(16).padStart(6,'0')}`;
  ctx.font = `bold ${28 * scale}px "VT323", monospace`;
  ctx.textAlign = 'center';
  ctx.fillText(text, 128, 44);
  const tex = new THREE.CanvasTexture(canvas);
  const sp  = new THREE.Sprite(
    new THREE.SpriteMaterial({ map: tex, transparent: true })
  );
  sp.scale.set(2.4 * scale, 0.6 * scale, 1);
  return sp;
}

function animLoop(renderer, scene, camera, onUpdate) {
  let id;
  const tick = () => {
    id = requestAnimationFrame(tick);
    if (onUpdate) onUpdate();
    renderer.render(scene, camera);
  };
  tick();
  return () => cancelAnimationFrame(id);
}

function lerpColor(mesh, targetHex, duration = 0.4) {
  if (typeof gsap !== 'undefined') {
    const from = new THREE.Color(mesh.material.color);
    const to   = new THREE.Color(targetHex);
    gsap.to(from, {
      r: to.r, g: to.g, b: to.b, duration,
      onUpdate: () => mesh.material.color.copy(from),
    });
    gsap.to({}, {
      duration,
      onUpdate: function() {
        mesh.material.emissive.copy(from);
      }
    });
  } else {
    mesh.material.color.set(targetHex);
    mesh.material.emissive.set(targetHex);
  }
}

function moveTo(obj, x, y, z, duration = 0.6) {
  if (typeof gsap !== 'undefined') {
    gsap.to(obj.position, { x, y, z, duration, ease: 'power2.inOut' });
  } else {
    obj.position.set(x, y, z);
  }
}

/* ═══════════════════════════════════════════════════════════════
   SCENE LIBRARY — one scene per viz type
   Each exports: draw(container, prob) → { step(n), totalSteps(), dispose() }
═══════════════════════════════════════════════════════════════ */

/* ──────────────────────────────────────────────────────────────
   SCENE: dijkstra / gps
   World: 3D city — car drives the shortest path through streets
   Steps: Initialize → Visit each node → Relax edges → Arrive
────────────────────────────────────────────────────────────── */
function sceneDijkstra(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 35, 80);
  const camera = createCamera(w, h, [0, 22, 30], [0, 0, 0]);
  addLights(scene);
  addGrid(scene, 40);

  // City layout — intersections + roads
  const CITY = [
    { id:'A', x:-8,  z:-6,  name:'Home'       },
    { id:'B', x:-2,  z:-8,  name:'School'      },
    { id:'C', x:-8,  z: 0,  name:'Park'        },
    { id:'D', x: 2,  z:-6,  name:'Mall'        },
    { id:'E', x:-2,  z: 2,  name:'Hospital'    },
    { id:'F', x: 6,  z:-2,  name:'Airport'     },
    { id:'G', x: 6,  z: 6,  name:'Office'      },
  ];
  const EDGES = [
    ['A','B',4], ['A','C',2], ['B','D',5],
    ['B','E',10],['C','E',3], ['D','F',2],
    ['E','F',4], ['F','G',1],
  ];

  const nodeMap = {};
  const edgeMeshes = {};

  // Draw road segments
  EDGES.forEach(([s, t, w]) => {
    const a = CITY.find(n => n.id === s);
    const b = CITY.find(n => n.id === t);
    const road = tube(scene, [a.x, 0, a.z], [b.x, 0, b.z], 0.18, CDEEP);
    edgeMeshes[`${s}-${t}`] = road;
    // Weight label
    const mid = label3D(`${w}m`, CDIM, 0.7);
    mid.position.set((a.x+b.x)/2, 0.5, (a.z+b.z)/2);
    scene.add(mid);
  });

  // Draw buildings at intersections
  CITY.forEach(n => {
    const h = 1.5 + Math.random() * 3;
    const building = box(scene, 1.4, h, 1.4, mat(CDEEP, CDEEP, 0.15), n.x, 0, n.z);
    // Rooftop glow cube
    const roofLight = box(scene, 0.4, 0.3, 0.4, mat(CDIM, CDIM, 0.3), n.x, h, n.z);
    // Name label above building
    const lbl = label3D(n.name, CDIM, 0.75);
    lbl.position.set(n.x, h + 1.2, n.z);
    scene.add(lbl);
    nodeMap[n.id] = { building, roofLight, h, ...n };
  });

  // Car — a small orange box that drives the path
  const carBody  = box(scene, 0.8, 0.4, 1.4, mat(CACC, CACC, 0.8), -8, 0.3, -6);
  const carTop   = box(scene, 0.6, 0.3, 0.8, mat(CACC, CACC, 0.6), -8, 0.7, -6);
  const headlightL = sphere(scene, 0.1, mat(YELLOW, YELLOW, 1.5), -8.3, 0.35, -6.7);
  const headlightR = sphere(scene, 0.1, mat(YELLOW, YELLOW, 1.5), -7.7, 0.35, -6.7);

  // Dijkstra step sequence
  const PATH    = ['A','B','D','F','G'];   // shortest path A→G
  const VISITED = ['A','C','B','E','D','F','G'];
  const STEPS = [
    { narration: 'GPS initialised at Home (A). Distance = 0, all others = ∞.',
      highlight: null, active: 'A', car: 'A', visitRoad: null },
    { narration: 'Exploring Home → Park (2 min) and Home → School (4 min).',
      highlight: ['A-C','A-B'], active: 'A', car: 'A', visitRoad: null },
    { narration: 'Park is nearest (2 min). GPS locks it in.',
      highlight: null, active: 'C', car: 'A', visitRoad: null },
    { narration: 'Park → Hospital (3 min). Total: 5 min. Better than ∞.',
      highlight: ['C-E'], active: 'C', car: 'A', visitRoad: null },
    { narration: 'School is next (4 min). GPS locks it in.',
      highlight: null, active: 'B', car: 'A', visitRoad: null },
    { narration: 'School → Mall (5 min). Total: 9 min.',
      highlight: ['B-D'], active: 'B', car: 'A', visitRoad: null },
    { narration: 'Hospital locked (5 min). School → Hospital was 14 — too slow.',
      highlight: null, active: 'E', car: 'A', visitRoad: null },
    { narration: 'Mall locked (9 min). Mall → Airport (2 min). Total: 11 min.',
      highlight: ['D-F'], active: 'D', car: 'A', visitRoad: null },
    { narration: 'Hospital → Airport (4 min). Total: 9 min. Faster! Route updated.',
      highlight: ['E-F'], active: 'E', car: 'A', visitRoad: null },
    { narration: 'Airport locked (9 min). Airport → Office (1 min). Total: 10 min.',
      highlight: ['F-G'], active: 'F', car: null, visitRoad: null },
    { narration: 'Optimal route found! Park → Hospital → Airport → Office = 10 min.',
      highlight: ['A-C','C-E','E-F','F-G'], active: 'G', car: 'G', visitRoad: 'PATH' },
  ];

  // Track visited buildings
  const visitedSet = new Set();

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length - 1)];

    // Reset all road colours
    Object.values(edgeMeshes).forEach(m => lerpColor(m, CDEEP, 0.3));
    // Reset all buildings
    Object.values(nodeMap).forEach(n => {
      lerpColor(n.building, visitedSet.has(n.id) ? CDIM : CDEEP, 0.3);
      lerpColor(n.roofLight, visitedSet.has(n.id) ? C : CDIM, 0.3);
    });

    // Mark visited
    if (s.active) visitedSet.add(s.active);

    // Highlight active node — glow cyan
    if (s.active && nodeMap[s.active]) {
      lerpColor(nodeMap[s.active].building, C, 0.35);
      lerpColor(nodeMap[s.active].roofLight, CBRIGHT, 0.2);
    }

    // Highlight edges
    if (s.highlight === 'PATH') {
      ['A-C','C-E','E-F','F-G'].forEach(k => {
        const m = edgeMeshes[k] || edgeMeshes[k.split('-').reverse().join('-')];
        if (m) lerpColor(m, CACC, 0.3);
      });
    } else if (Array.isArray(s.highlight)) {
      s.highlight.forEach(k => {
        const m = edgeMeshes[k] || edgeMeshes[k.split('-').reverse().join('-')];
        if (m) lerpColor(m, C, 0.3);
      });
    }

    // Move car to node
    if (s.car && nodeMap[s.car]) {
      const dest = nodeMap[s.car];
      moveTo(carBody, dest.x, 0.3, dest.z, 0.8);
      moveTo(carTop,  dest.x, 0.7, dest.z, 0.8);
      moveTo(headlightL, dest.x - 0.3, 0.35, dest.z - 0.7, 0.8);
      moveTo(headlightR, dest.x + 0.3, 0.35, dest.z - 0.7, 0.8);
    }

    // Pan camera toward active node
    if (s.active && nodeMap[s.active]) {
      const t = nodeMap[s.active];
      if (typeof gsap !== 'undefined') {
        gsap.to(camera.position, {
          x: t.x + 4, y: 18, z: t.z + 18,
          duration: 0.9, ease: 'power2.inOut'
        });
      }
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.008;
    // Gentle camera sway when idle
    camera.position.x += Math.sin(t * 0.3) * 0.005;
  });

  const dispose = () => {
    stopLoop();
    ro.disconnect();
    renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;

  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: bfs / social
   World: 3D social network — glowing people spheres, ripple spread
────────────────────────────────────────────────────────────── */
function sceneBFS(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 30, 60);
  const camera = createCamera(w, h, [0, 18, 24], [0, 0, 3]);
  addLights(scene);
  addGrid(scene, 30, CDEEP);

  const PEOPLE = [
    { id:'you',    x: 0,   z: 0,  name:'You'      },
    { id:'alice',  x:-4,   z: 4,  name:'Alice'     },
    { id:'bob',    x: 4,   z: 4,  name:'Bob'       },
    { id:'carol',  x:-7,   z: 9,  name:'Carol'     },
    { id:'dave',   x:-1,   z: 9,  name:'Dave'      },
    { id:'eve',    x: 3,   z: 9,  name:'Eve'       },
    { id:'frank',  x: 7,   z: 9,  name:'Frank'     },
    { id:'grace',  x:-4,   z:14,  name:'Grace'     },
    { id:'henry',  x: 2,   z:14,  name:'Henry'     },
  ];
  const CONNECTIONS = [
    ['you','alice'],['you','bob'],
    ['alice','carol'],['alice','dave'],
    ['bob','eve'],['bob','frank'],
    ['carol','grace'],['dave','henry'],
  ];

  const nodeMap = {};
  PEOPLE.forEach(p => {
    // Person body
    const body = sphere(scene, 0.7, mat(CDEEP, CDEEP, 0.2), p.x, 0.7, p.z);
    // Head
    const head = sphere(scene, 0.4, mat(CDIM, CDIM, 0.3), p.x, 1.9, p.z);
    // Name label
    const lbl = label3D(p.name, CDIM, 0.8);
    lbl.position.set(p.x, 3.1, p.z);
    scene.add(lbl);
    nodeMap[p.id] = { body, head, lbl, ...p };
  });

  // Friendship lines
  const connectionMeshes = {};
  CONNECTIONS.forEach(([a, b]) => {
    const pa = PEOPLE.find(p => p.id === a);
    const pb = PEOPLE.find(p => p.id === b);
    const line = tube(scene, [pa.x, 0.7, pa.z], [pb.x, 0.7, pb.z], 0.05, CDEEP);
    connectionMeshes[`${a}-${b}`] = line;
  });

  const STEPS = [
    { active:'you',   discovered:[],
      narration: 'Starting at your profile. Queue: [You].' },
    { active:'you',   discovered:['alice','bob'],
      connections:['you-alice','you-bob'],
      narration: 'Level 1: Found Alice and Bob — your direct friends.' },
    { active:'alice', discovered:['carol','dave'],
      connections:['alice-carol','alice-dave'],
      narration: 'Processing Alice. Discovered Carol and Dave (friends of Alice).' },
    { active:'bob',   discovered:['eve','frank'],
      connections:['bob-eve','bob-frank'],
      narration: 'Processing Bob. Discovered Eve and Frank (friends of Bob).' },
    { active:'carol', discovered:['grace'],
      connections:['carol-grace'],
      narration: 'Level 2: Processing Carol. Grace is a friend of a friend.' },
    { active:'dave',  discovered:['henry'],
      connections:['dave-henry'],
      narration: 'Processing Dave. Henry is a friend of a friend.' },
    { active:'eve',   discovered:[],
      narration: 'Processing Eve. No new connections found.' },
    { active:'frank', discovered:[],
      narration: 'Processing Frank. No new connections found.' },
    { active:'grace', discovered:[],
      narration: 'Level 3: Grace reached. All connections within 3 degrees mapped.' },
    { active:'henry', discovered:[],
      narration: 'Henry reached. BFS complete — entire reachable network discovered.' },
  ];

  const discoveredSet = new Set(['you']);

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    s.discovered?.forEach(id => discoveredSet.add(id));

    // Colour everyone
    PEOPLE.forEach(p => {
      const isActive     = p.id === s.active;
      const isDiscovered = discoveredSet.has(p.id);
      const color = isActive ? CBRIGHT : isDiscovered ? C : CDEEP;
      const emInt = isActive ? 1.2 : isDiscovered ? 0.5 : 0.15;
      lerpColor(nodeMap[p.id].body, color, 0.35);
      lerpColor(nodeMap[p.id].head, color, 0.35);
      nodeMap[p.id].body.material.emissiveIntensity = emInt;
      if (isActive && typeof gsap !== 'undefined') {
        gsap.to(nodeMap[p.id].body.position, { y: 1.4, duration: 0.3,
          yoyo: true, repeat: 1, ease: 'power2.out' });
      }
    });

    // Light up connections
    Object.values(connectionMeshes).forEach(m => lerpColor(m, CDEEP, 0.3));
    s.connections?.forEach(k => {
      const m = connectionMeshes[k] || connectionMeshes[k.split('-').reverse().join('-')];
      if (m) lerpColor(m, C, 0.3);
    });

    // Pan camera
    if (nodeMap[s.active] && typeof gsap !== 'undefined') {
      gsap.to(camera.position, {
        x: nodeMap[s.active].x + 2,
        z: nodeMap[s.active].z + 16,
        duration: 0.8, ease: 'power2.inOut',
      });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.006;
    PEOPLE.forEach(p => {
      if (discoveredSet.has(p.id)) {
        nodeMap[p.id].body.position.y = 0.7 + Math.sin(t + p.x) * 0.06;
      }
    });
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: mergesort / sorting
   World: 3D bar chart leaderboard — bars swap and merge
────────────────────────────────────────────────────────────── */
function sceneSorting(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 25, 55);
  const camera = createCamera(w, h, [0, 10, 20], [0, 3, 0]);
  addLights(scene);
  addGrid(scene, 24);

  const VALUES = [64, 34, 25, 12, 22, 11, 90, 45];
  const MAX    = Math.max(...VALUES);
  const N      = VALUES.length;
  const SPACE  = 2.4;
  const START  = -(N-1) * SPACE / 2;

  const bars   = [];
  const labels = [];
  VALUES.forEach((v, i) => {
    const bh = (v / MAX) * 8 + 0.3;
    const b  = box(scene, 1.8, bh, 1.8, mat(CDIM, CDIM, 0.25),
                   START + i * SPACE, 0, 0);
    bars.push(b);
    const lbl = label3D(String(v), CDIM, 0.9);
    lbl.position.set(START + i * SPACE, bh + 0.9, 0);
    scene.add(lbl);
    labels.push(lbl);
  });

  // Merge sort step-by-step state
  const STEPS = [
    { compare:[], sorted:[], swap:null,
      narration:'Leaderboard unsorted. Merge Sort divides it in half.' },
    { compare:[0,1], sorted:[], swap:[0,1],
      narration:'Comparing players 0 and 1. 34 < 64, they swap positions.' },
    { compare:[2,3], sorted:[], swap:[2,3],
      narration:'Comparing players 2 and 3. 12 < 25, they swap.' },
    { compare:[4,5], sorted:[], swap:[4,5],
      narration:'Comparing players 4 and 5. 11 < 22, they swap.' },
    { compare:[6,7], sorted:[], swap:null,
      narration:'Comparing players 6 and 7. 45 < 90, already in order.' },
    { compare:[0,1,2,3], sorted:[], swap:null,
      narration:'Merging left half: [34,64] with [12,25]. Result: [12,25,34,64].' },
    { compare:[4,5,6,7], sorted:[], swap:null,
      narration:'Merging right half: [11,22] with [45,90]. Result: [11,22,45,90].' },
    { compare:[], sorted:[0,1,2,3,4,5,6,7], swap:null,
      narration:'Final merge complete! Leaderboard sorted: 11,12,22,25,34,45,64,90.' },
  ];

  const SORTED_VALS = [11,12,22,25,34,45,64,90];

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    const isFinal = s.sorted.length === N;

    bars.forEach((b, i) => {
      const isCompare = s.compare.includes(i);
      const isSorted  = s.sorted.includes(i);
      const color = isFinal ? GREEN : isCompare ? CACC : CDIM;
      lerpColor(b, color, 0.35);

      if (isFinal) {
        const targetH = (SORTED_VALS[i] / MAX) * 8 + 0.3;
        if (typeof gsap !== 'undefined') {
          gsap.to(b.scale, { y: targetH / ((VALUES[i]/MAX)*8+0.3),
            duration: 0.6, delay: i * 0.06 });
          labels[i].position.y = targetH + 0.9;
        }
      }
    });

    if (s.swap && typeof gsap !== 'undefined') {
      const [a, b2] = s.swap;
      const xa = bars[a].position.x;
      const xb = bars[b2].position.x;
      gsap.to(bars[a].position, { x: xb, duration: 0.5, ease:'power2.inOut' });
      gsap.to(bars[b2].position,{ x: xa, duration: 0.5, ease:'power2.inOut' });
      gsap.to(labels[a].position,{ x: xb, duration: 0.5 });
      gsap.to(labels[b2].position,{ x: xa, duration: 0.5 });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.007;
    camera.position.x = Math.sin(t * 0.15) * 3;
    camera.lookAt(0, 3, 0);
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: array / train
   World: 3D train with carriages — pointer moves along carriages
────────────────────────────────────────────────────────────── */
function sceneArray(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 28, 55);
  const camera = createCamera(w, h, [0, 8, 18], [0, 1, 0]);
  addLights(scene);
  addGrid(scene, 26);

  const VALUES = prob.demo || [7, 2, 9, 4, 1, 6, 3, 8, 5];
  const N = VALUES.length;
  const SPACE = 2.2;
  const START = -(N-1)*SPACE/2;

  // Train track
  const track = new THREE.Mesh(
    new THREE.BoxGeometry(N*SPACE+1, 0.12, 0.5),
    mat(CDIM, CDIM, 0.2)
  );
  track.position.set(0, 0.06, 0);
  scene.add(track);

  // Carriages
  const carriages = [];
  const valLabels = [];
  const idxLabels = [];
  VALUES.forEach((v, i) => {
    const c = box(scene, 1.8, 1.4, 1.6, mat(CDEEP, CDEEP, 0.2),
                  START + i*SPACE, 0.12, 0);
    // Carriage window (lighter panel)
    const win = box(scene, 1.2, 0.6, 0.2,
      mat(CDIM, CDIM, 0.4), START+i*SPACE, 0.82, 0.75);
    carriages.push(c);
    const vl = label3D(String(v), CBRIGHT, 0.9);
    vl.position.set(START+i*SPACE, 2.2, 0);
    scene.add(vl);
    valLabels.push(vl);
    const il = label3D(`[${i}]`, CDIM, 0.65);
    il.position.set(START+i*SPACE, -0.5, 0);
    scene.add(il);
    idxLabels.push(il);
  });

  // Pointer arrow
  const pointer = new THREE.Mesh(
    new THREE.ConeGeometry(0.25, 0.8, 8),
    mat(CACC, CACC, 1.0)
  );
  pointer.rotation.z = Math.PI;
  pointer.position.set(START, 3.2, 0);
  scene.add(pointer);

  // Steps: linear search for a target
  const TARGET = 6;
  const STEPS = VALUES.map((v, i) => ({
    pointer: i,
    found: v === TARGET,
    highlight: i,
    narration: v === TARGET
      ? `Found ${TARGET} at carriage [${i}]! Linear Search complete.`
      : `Checking carriage [${i}]: value is ${v}. Not ${TARGET}, continue.`,
  }));

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    carriages.forEach((c, i) => {
      const color = i === s.highlight
        ? (s.found ? GREEN : CACC)
        : i < s.pointer ? CDIM : CDEEP;
      lerpColor(c, color, 0.3);
    });
    const tx = START + s.pointer * SPACE;
    moveTo(pointer, tx, 3.2, 0, 0.45);
    if (typeof gsap !== 'undefined') {
      gsap.to(camera.position, {
        x: tx * 0.4, duration: 0.6, ease: 'power2.inOut',
      });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.01;
    pointer.position.y = 3.2 + Math.sin(t * 3) * 0.1;
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: binarysearch
   World: 3D library — robot arm searches sorted book shelves
────────────────────────────────────────────────────────────── */
function sceneBinarySearch(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 30, 60);
  const camera = createCamera(w, h, [0, 9, 20], [0, 2, 0]);
  addLights(scene);
  addGrid(scene, 28);

  const BOOKS = [1,3,5,7,9,11,13,15,17,19,23,27,31,35,42];
  const TARGET = 23;
  const N = BOOKS.length;
  const SPACE = 1.5;
  const START = -(N-1)*SPACE/2;

  // Bookshelf base
  const shelf = box(scene, N*SPACE+1, 0.2, 1.2, mat(0x3d1a00, 0x3d1a00, 0.1), 0, 0, 0);
  box(scene, N*SPACE+1, 0.2, 1.2, mat(0x3d1a00, 0x3d1a00, 0.1), 0, 2.8, 0);
  box(scene, 0.15, 3.2, 1.2, mat(0x3d1a00, 0x3d1a00, 0.1), START-0.8, 1.6, 0);
  box(scene, 0.15, 3.2, 1.2, mat(0x3d1a00, 0x3d1a00, 0.1), -START+0.8, 1.6, 0);

  // Books as colored boxes
  const books = [];
  BOOKS.forEach((v, i) => {
    const isTarget = v === TARGET;
    const bk = box(scene, 1.1, 2.2, 0.9,
      mat(isTarget ? 0x1a3a1a : CDEEP, CDIM, 0.2),
      START + i*SPACE, 0.3, 0);
    books.push(bk);
    const lbl = label3D(String(v), CDIM, 0.65);
    lbl.position.set(START+i*SPACE, 2.8, 0);
    scene.add(lbl);
  });

  // Robot arm (pointer)
  const arm = cylinder(scene, 0.08, 0.08, 2.5, mat(CACC, CACC, 1.0), 0, 4.5, 0);
  const armHead = sphere(scene, 0.22, mat(CBRIGHT, CBRIGHT, 1.2), 0, 3.2, 0);

  // Binary search steps
  let lo = 0, hi = N-1;
  const STEPS = [];
  let loCur = 0, hiCur = N-1;
  while (loCur <= hiCur) {
    const mid = Math.floor((loCur + hiCur) / 2);
    const v   = BOOKS[mid];
    STEPS.push({
      lo: loCur, hi: hiCur, mid,
      found: v === TARGET,
      narration: v === TARGET
        ? `Found ${TARGET} at shelf position [${mid}]! Binary Search complete in ${STEPS.length+1} steps vs ${N} linear.`
        : v < TARGET
          ? `Book [${mid}]=${v} < ${TARGET}. Discard left half. Search right: [${mid+1}..${hiCur}].`
          : `Book [${mid}]=${v} > ${TARGET}. Discard right half. Search left: [${loCur}..${mid-1}].`,
    });
    if (v === TARGET) break;
    if (v < TARGET) loCur = mid + 1;
    else hiCur = mid - 1;
  }

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    books.forEach((b, i) => {
      const inRange = i >= s.lo && i <= s.hi;
      const isMid   = i === s.mid;
      const isFound = s.found && isMid;
      lerpColor(b,
        isFound ? GREEN : isMid ? CACC : inRange ? CDIM : 0x080f14,
        0.3);
    });
    const midX = START + s.mid * SPACE;
    moveTo(arm, midX, 4.5, 0, 0.5);
    moveTo(armHead, midX, 3.2, 0, 0.5);
    if (typeof gsap !== 'undefined') {
      gsap.to(camera.position, { x: midX * 0.3, duration:0.7 });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.01;
    armHead.position.y = 3.2 + Math.sin(t*2)*0.07;
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: tree / bst
   World: 3D family tree — glowing orbs, branches, camera flies between nodes
────────────────────────────────────────────────────────────── */
function sceneTree(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 28, 60);
  const camera = createCamera(w, h, [0, 10, 20], [0, 2, 0]);
  addLights(scene);

  const NODES = [
    { id:1, val:50, x:0,   y:9,  parent:null },
    { id:2, val:30, x:-5,  y:6,  parent:1 },
    { id:3, val:70, x: 5,  y:6,  parent:1 },
    { id:4, val:20, x:-7.5,y:3,  parent:2 },
    { id:5, val:35, x:-2.5,y:3,  parent:2 },
    { id:6, val:60, x: 2.5,y:3,  parent:3 },
    { id:7, val:80, x: 7.5,y:3,  parent:3 },
    { id:8, val:15, x:-9,  y:0,  parent:4 },
    { id:9, val:25, x:-6,  y:0,  parent:4 },
  ];
  const lookup = Object.fromEntries(NODES.map(n => [n.id, n]));

  const orbs   = {};
  const edges  = {};

  NODES.forEach(n => {
    const orb = sphere(scene, n.parent ? 0.55 : 0.8,
      mat(CDEEP, CDEEP, 0.2), n.x, n.y, 0);
    orbs[n.id] = orb;
    const lbl = label3D(String(n.val), CDIM, 0.75);
    lbl.position.set(n.x, n.y + 1.2, 0);
    scene.add(lbl);

    if (n.parent) {
      const p = lookup[n.parent];
      const e = tube(scene, [p.x, p.y, 0], [n.x, n.y, 0], 0.07, CDEEP);
      edges[`${n.parent}-${n.id}`] = e;
    }
  });

  // Inorder traversal steps
  const INORDER = [8,4,9,2,5,1,6,3,7];
  const STEPS = INORDER.map((id, i) => ({
    active: id,
    visited: INORDER.slice(0, i+1),
    narration: `Visiting node ${lookup[id].val}. ` +
      (i === 0 ? 'Starting at leftmost leaf (smallest value).'
       : i === INORDER.length-1 ? 'Last node — inorder traversal complete! Result: sorted ascending.'
       : `Inorder position ${i+1}/${INORDER.length}.`),
  }));

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    const visitedSet = new Set(s.visited);
    NODES.forEach(n => {
      const isActive  = n.id === s.active;
      const isVisited = visitedSet.has(n.id);
      lerpColor(orbs[n.id],
        isActive ? CBRIGHT : isVisited ? C : CDEEP, 0.3);
      orbs[n.id].material.emissiveIntensity = isActive ? 1.4 : isVisited ? 0.5 : 0.15;
    });
    // Light up edge to active
    Object.entries(edges).forEach(([k, m]) => {
      const [pid, cid] = k.split('-').map(Number);
      lerpColor(m, visitedSet.has(cid) ? C : CDEEP, 0.3);
    });
    const active = lookup[s.active];
    if (active && typeof gsap !== 'undefined') {
      gsap.to(camera.position, {
        x: active.x + 2, y: active.y + 6,
        duration: 0.75, ease: 'power2.inOut',
      });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.007;
    Object.values(orbs).forEach((o, i) => {
      o.position.y += Math.sin(t + i) * 0.001;
    });
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: dp / vault
   World: 3D vault grid — cells light up as subproblems are solved
────────────────────────────────────────────────────────────── */
function sceneDP(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 28, 55);
  const camera = createCamera(w, h, [0, 16, 18], [0, 0, 0]);
  addLights(scene);

  // Fibonacci DP table as glowing floor tiles
  const FIBS = [0,1,1,2,3,5,8,13,21,34];
  const N = FIBS.length;
  const SPACE = 2.2;
  const START = -(N-1)*SPACE/2;

  const cells  = [];
  const valLbl = [];
  FIBS.forEach((v, i) => {
    const c = box(scene, 1.8, 0.3, 1.8, mat(CDEEP, CDEEP, 0.1),
                  START + i*SPACE, 0, 0);
    cells.push(c);
    const lbl = label3D(String(v), CDIM, 0.85);
    lbl.position.set(START+i*SPACE, 1.0, 0);
    scene.add(lbl);
    valLbl.push(lbl);

    const il = label3D(`F(${i})`, CDIM, 0.6);
    il.position.set(START+i*SPACE, -0.5, 0);
    scene.add(il);
  });

  // Arrow showing dependency
  const arrow = new THREE.Mesh(
    new THREE.ConeGeometry(0.2, 0.7, 8),
    mat(CACC, CACC, 1.0)
  );
  arrow.rotation.z = Math.PI;
  arrow.position.set(START, 2.2, 0);
  scene.add(arrow);

  const STEPS = FIBS.map((v, i) => ({
    active: i,
    filled: Array.from({length: i+1}, (_, k) => k),
    narration: i < 2
      ? `Base case: F(${i}) = ${v}. Stored in memo table.`
      : `F(${i}) = F(${i-1}) + F(${i-2}) = ${FIBS[i-1]} + ${FIBS[i-2]} = ${v}. Cache it — never recalculate!`,
  }));

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    const filledSet = new Set(s.filled);
    cells.forEach((c, i) => {
      const isActive = i === s.active;
      const isFilled = filledSet.has(i);
      lerpColor(c,
        isActive ? CBRIGHT : isFilled ? C : CDEEP, 0.3);
      if (isActive && typeof gsap !== 'undefined') {
        gsap.to(c.scale, { y: 2.5, duration: 0.25,
          yoyo: true, repeat: 1 });
      }
    });
    moveTo(arrow, START + s.active*SPACE, 2.2, 0, 0.45);
    if (typeof gsap !== 'undefined') {
      gsap.to(camera.position, {
        x: START + s.active*SPACE * 0.35,
        duration: 0.7, ease: 'power2.inOut',
      });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.008;
    camera.position.x += Math.sin(t * 0.2) * 0.003;
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: stack
   World: 3D stack of plates — push/pop animation
────────────────────────────────────────────────────────────── */
function sceneStack(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 22, 48);
  const camera = createCamera(w, h, [5, 10, 16], [0, 4, 0]);
  addLights(scene);
  addGrid(scene, 20);

  const OPERATIONS = [
    { op:'PUSH', val:3 }, { op:'PUSH', val:7 },
    { op:'PUSH', val:2 }, { op:'PUSH', val:9 },
    { op:'PUSH', val:1 }, { op:'POP',  val:null },
    { op:'PUSH', val:5 }, { op:'POP',  val:null },
  ];

  const plates   = [];
  let   stackArr = [];

  // Table base
  box(scene, 3.5, 0.3, 3.5, mat(0x1a0d00, 0x1a0d00, 0.1), 0, 0, 0);

  // TOP label
  const topLabel = label3D('TOP ↑', CACC, 0.9);
  topLabel.position.set(2.8, 1, 0);
  scene.add(topLabel);

  const STEPS = [];
  const tempStack = [];
  OPERATIONS.forEach((op, i) => {
    if (op.op === 'PUSH') {
      tempStack.push(op.val);
      STEPS.push({
        stack: [...tempStack],
        highlight: tempStack.length - 1,
        op: `PUSH ${op.val}`,
        narration: `PUSH ${op.val} onto stack. Stack: [${tempStack.join(', ')}]. Top = ${op.val}.`,
      });
    } else {
      const popped = tempStack.pop();
      STEPS.push({
        stack: [...tempStack],
        highlight: -1,
        op: `POP → ${popped}`,
        narration: `POP returns ${popped} (LIFO — Last In, First Out). Stack: [${tempStack.join(', ')}].`,
      });
    }
  });

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    // Remove old plates
    plates.forEach(p => scene.remove(p));
    plates.length = 0;

    s.stack.forEach((v, i) => {
      const isTop = i === s.stack.length - 1;
      const p = new THREE.Mesh(
        new THREE.CylinderGeometry(1.5, 1.5, 0.5, 32),
        mat(isTop ? C : CDIM, isTop ? C : CDIM, isTop ? 0.9 : 0.3)
      );
      p.position.set(0, 0.3 + i * 0.6, 0);
      p.castShadow = true;
      scene.add(p);
      plates.push(p);

      const lbl = label3D(String(v), isTop ? CBRIGHT : CDIM, 0.75);
      lbl.position.set(0, 0.3 + i*0.6 + 0.55, 0);
      scene.add(lbl);
      plates.push(lbl); // so it gets cleaned too
    });

    topLabel.position.y = Math.max(1, 0.3 + s.stack.length * 0.6 + 0.4);

    if (typeof gsap !== 'undefined') {
      gsap.to(camera.position, {
        y: 4 + s.stack.length * 0.5,
        duration: 0.5, ease: 'power2.inOut',
      });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.008;
    camera.position.x = 5 + Math.sin(t*0.3) * 1.5;
    camera.lookAt(0, 4, 0);
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: linkedlist
   World: 3D chain — glowing capsules connected by beams
────────────────────────────────────────────────────────────── */
function sceneLinkedList(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 25, 52);
  const camera = createCamera(w, h, [0, 7, 16], [0, 1, 0]);
  addLights(scene);
  addGrid(scene, 22);

  const VALS   = [10, 20, 30, 40, 50, 60];
  const N      = VALS.length;
  const SPACE  = 3.2;
  const START  = -(N-1)*SPACE/2;

  const nodes  = [];
  const arrows = [];

  VALS.forEach((v, i) => {
    // Node box
    const nd = box(scene, 1.8, 1.2, 1.2,
      mat(CDEEP, CDEEP, 0.2), START+i*SPACE, 0.7, 0);
    nodes.push(nd);
    const vl = label3D(String(v), CBRIGHT, 0.85);
    vl.position.set(START+i*SPACE, 2.3, 0);
    scene.add(vl);

    // Arrow to next
    if (i < N-1) {
      const ar = tube(scene,
        [START+i*SPACE+1.0, 1.3, 0],
        [START+(i+1)*SPACE-1.0, 1.3, 0],
        0.07, CDEEP);
      arrows.push(ar);
      // Arrowhead
      const ah = new THREE.Mesh(
        new THREE.ConeGeometry(0.15, 0.4, 8),
        mat(CDIM, CDIM, 0.4)
      );
      ah.rotation.z = -Math.PI/2;
      ah.position.set(START+(i+1)*SPACE-1.05, 1.3, 0);
      scene.add(ah);
      arrows.push(ah);
    }
  });

  // NULL terminator
  const nullLbl = label3D('NULL', RED, 0.8);
  nullLbl.position.set(-START+SPACE*0.5, 2.3, 0);
  scene.add(nullLbl);

  // Traversal steps
  const STEPS = VALS.map((v, i) => ({
    current: i,
    narration: i === N-1
      ? `Node ${v} → NULL. End of linked list. Traversal complete.`
      : `Current node: ${v}. Following pointer → node ${VALS[i+1]}.`,
  }));

  // Bonus: reverse step
  STEPS.push({
    current: -1,
    reversed: true,
    narration: 'Reversing pointers in-place. O(n) time, O(1) space — no extra memory needed.',
  });

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    nodes.forEach((nd, i) => {
      const isActive = i === s.current;
      const isPast   = i < s.current;
      lerpColor(nd,
        isActive ? C : isPast ? CDIM : CDEEP, 0.3);
    });
    if (s.reversed) {
      // Flash all nodes orange to show reversal
      nodes.forEach((nd, i) => {
        if (typeof gsap !== 'undefined') {
          gsap.to({}, { duration: 0.1*i, onComplete: () => lerpColor(nd, CACC, 0.2) });
        }
      });
      arrows.forEach(a => lerpColor(a, CACC, 0.4));
    } else {
      arrows.forEach((a, i) => {
        lerpColor(a,
          i/2 <= s.current ? C : CDEEP, 0.3);
      });
    }
    if (s.current >= 0 && typeof gsap !== 'undefined') {
      gsap.to(camera.position, {
        x: (START + s.current*SPACE) * 0.3,
        duration: 0.6, ease: 'power2.inOut',
      });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.007;
    nodes.forEach((nd, i) => {
      nd.rotation.y = Math.sin(t + i*0.4) * 0.04;
    });
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: windowslide / twopointers
   World: 3D conveyor belt — sensor window slides along packages
────────────────────────────────────────────────────────────── */
function sceneWindow(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 26, 52);
  const camera = createCamera(w, h, [0, 9, 18], [0, 2, 0]);
  addLights(scene);
  addGrid(scene, 24);

  const VALUES = [2, 1, 5, 1, 3, 2, 6, 4];
  const K      = 3;  // window size
  const N      = VALUES.length;
  const SPACE  = 2.1;
  const START  = -(N-1)*SPACE/2;

  // Conveyor belt base
  box(scene, N*SPACE+1, 0.15, 1.6, mat(0x1a1000, 0x1a1000, 0.1), 0, 0, 0);

  const packages = [];
  VALUES.forEach((v, i) => {
    const pkg = box(scene, 1.7, 1.5, 1.4,
      mat(CDEEP, CDEEP, 0.2), START+i*SPACE, 0.15, 0);
    packages.push(pkg);
    const vl = label3D(String(v), CBRIGHT, 0.85);
    vl.position.set(START+i*SPACE, 2.1, 0);
    scene.add(vl);
  });

  // Window frame — 3 glowing bars forming a bracket
  const winMat = mat(CACC, CACC, 0.9);
  const winTop  = new THREE.Mesh(new THREE.BoxGeometry(K*SPACE-0.1,0.12,0.12), winMat.clone());
  const winBotL = new THREE.Mesh(new THREE.BoxGeometry(0.12,1.8,0.12), winMat.clone());
  const winBotR = new THREE.Mesh(new THREE.BoxGeometry(0.12,1.8,0.12), winMat.clone());
  [winTop, winBotL, winBotR].forEach(m => { m.castShadow=false; scene.add(m); });

  // Max sum label
  const maxLabel = label3D('MAX: 0', CBRIGHT, 1.0);
  maxLabel.position.set(0, 4.5, 0);
  scene.add(maxLabel);

  // Sliding window steps
  const STEPS = [];
  let maxSum = 0;
  for (let i = 0; i <= N-K; i++) {
    const sum = VALUES.slice(i, i+K).reduce((a,b)=>a+b, 0);
    maxSum = Math.max(maxSum, sum);
    STEPS.push({
      left: i, right: i+K-1,
      sum, maxSum,
      narration: `Window [${i}..${i+K-1}]: values [${VALUES.slice(i,i+K).join(', ')}] = sum ${sum}. ` +
        (sum === maxSum ? `New maximum! Max sum = ${maxSum}.` : `Max so far = ${maxSum}.`),
    });
  }

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    packages.forEach((p, i) => {
      const inWin = i >= s.left && i <= s.right;
      lerpColor(p, inWin ? (s.sum === s.maxSum ? GREEN : CACC) : CDEEP, 0.3);
    });
    const cx = (START+s.left*SPACE + START+s.right*SPACE) / 2;
    winTop.position.set(cx, 2.0, 0.8);
    winBotL.position.set(START+s.left*SPACE - SPACE*0.45, 1.1, 0.8);
    winBotR.position.set(START+s.right*SPACE + SPACE*0.45, 1.1, 0.8);

    // Update max label texture
    maxLabel.material.map.dispose();
    const c2 = document.createElement('canvas');
    c2.width=256; c2.height=64;
    const ct = c2.getContext('2d');
    ct.fillStyle='#a9f0fa';
    ct.font='bold 26px VT323, monospace';
    ct.textAlign='center';
    ct.fillText(`MAX: ${s.maxSum}`, 128, 44);
    maxLabel.material.map = new THREE.CanvasTexture(c2);
    maxLabel.material.needsUpdate = true;

    if (typeof gsap !== 'undefined') {
      gsap.to(camera.position, { x: cx*0.3, duration:0.55 });
    }
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.009;
    winTop.position.y  = 2.0 + Math.sin(t*2)*0.04;
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: dfs / maze
   World: 3D maze — robot explores corridors, backtracking shown
────────────────────────────────────────────────────────────── */
function sceneDFS(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 22, 48);
  const camera = createCamera(w, h, [0, 20, 16], [0, 0, 0]);
  addLights(scene);

  // 6x6 maze grid — 0=path, 1=wall
  const MAZE = [
    [0,0,1,0,0,0],
    [1,0,1,0,1,0],
    [0,0,0,0,1,0],
    [0,1,1,0,0,0],
    [0,0,0,1,0,1],
    [1,1,0,0,0,0],
  ];
  const ROWS = MAZE.length, COLS = MAZE[0].length;
  const CS   = 2.2;
  const OX   = -(COLS-1)*CS/2, OZ = -(ROWS-1)*CS/2;

  const cellMeshes = {};
  MAZE.forEach((row, r) => {
    row.forEach((v, c) => {
      if (v === 1) {
        const wall = box(scene, CS*0.9, 1.8, CS*0.9,
          mat(0x0d1a20, 0x0d1a20, 0.1),
          OX+c*CS, 0, OZ+r*CS);
      } else {
        const floor = new THREE.Mesh(
          new THREE.BoxGeometry(CS*0.9, 0.12, CS*0.9),
          mat(CDEEP, CDEEP, 0.08)
        );
        floor.position.set(OX+c*CS, 0.06, OZ+r*CS);
        scene.add(floor);
        cellMeshes[`${r}-${c}`] = floor;
      }
    });
  });

  // Robot
  const robot = box(scene, 0.7, 1.1, 0.7, mat(CACC, CACC, 0.9), OX, 0.55, OZ);
  const robotHead = sphere(scene, 0.3, mat(CBRIGHT, CBRIGHT, 1.0), OX, 1.55, OZ);

  // DFS path through maze from (0,0) to (5,5)
  const DFS_PATH = [
    [0,0],[0,1],[1,1],[2,1],[2,2],[2,3],[3,3],[3,4],[3,5],[4,4],[4,5],[5,2],[5,3],[5,4],[5,5]
  ];

  const STEPS = DFS_PATH.map(([r,c], i) => ({
    pos: [r,c],
    visited: DFS_PATH.slice(0,i+1),
    isBacktrack: i > 0 && !(
      Math.abs(r-DFS_PATH[i-1][0])+Math.abs(c-DFS_PATH[i-1][1]) === 1
    ),
    narration: r===5&&c===5
      ? 'Exit found! DFS explored every reachable path. Total steps: '+DFS_PATH.length
      : `Entering room (${r},${c}). ` +
        (i > 0 && Math.abs(r-DFS_PATH[i-1][0])+Math.abs(c-DFS_PATH[i-1][1]) > 1
          ? 'Dead end — backtracking to last junction.'
          : `Marking visited. ${DFS_PATH.length-i-1} more rooms to explore.`),
  }));

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    const visitedSet = new Set(s.visited.map(([r,c])=>`${r}-${c}`));

    Object.entries(cellMeshes).forEach(([k, m]) => {
      const isVisited = visitedSet.has(k);
      const [r,c]     = k.split('-').map(Number);
      const isCurrent = r === s.pos[0] && c === s.pos[1];
      lerpColor(m,
        isCurrent ? CBRIGHT : isVisited ? C : CDEEP, 0.3);
      m.material.emissiveIntensity = isCurrent ? 1.0 : isVisited ? 0.4 : 0.08;
    });

    const [r,c] = s.pos;
    moveTo(robot, OX+c*CS, 0.55, OZ+r*CS, 0.4);
    moveTo(robotHead, OX+c*CS, 1.55, OZ+r*CS, 0.4);
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.007;
    camera.position.x = Math.sin(t*0.2)*3;
    camera.lookAt(0,0,0);
    robotHead.position.y = 1.55 + Math.sin(t*3)*0.06;
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ──────────────────────────────────────────────────────────────
   SCENE: generic fallback
   World: 3D floating nodes with pulsing glow
────────────────────────────────────────────────────────────── */
function sceneDefault(container, prob) {
  const { renderer, w, h, ro } = createRenderer(container);
  const scene  = new THREE.Scene();
  scene.fog    = new THREE.Fog(BG, 22, 50);
  const camera = createCamera(w, h, [0, 8, 16], [0, 0, 0]);
  addLights(scene);
  addGrid(scene, 22);

  const NODES = Array.from({length:7}, (_, i) => {
    const angle = (i / 7) * Math.PI * 2;
    return { x: Math.cos(angle)*5, z: Math.sin(angle)*5 };
  });

  const orbs = NODES.map(n => sphere(scene, 0.6, mat(CDEEP, CDEEP, 0.2), n.x, 1, n.z));
  orbs.forEach((o, i) => {
    NODES.forEach((n, j) => {
      if (j > i) tube(scene, [NODES[i].x,1,NODES[i].z], [n.x,1,n.z], 0.04, CDEEP);
    });
  });

  const STEPS = Array.from({length:7}, (_, i) => ({
    active: i,
    narration: prob?.title
      ? `${prob.title}: processing element ${i+1} of 7.`
      : `Step ${i+1}: processing node ${i+1}.`,
  }));

  function applyStep(idx) {
    const s = STEPS[Math.min(idx, STEPS.length-1)];
    orbs.forEach((o, i) => {
      lerpColor(o, i === s.active ? C : i < s.active ? CDIM : CDEEP, 0.3);
    });
  }

  let t = 0;
  const stopLoop = animLoop(renderer, scene, camera, () => {
    t += 0.007;
    orbs.forEach((o, i) => {
      o.position.y = 1 + Math.sin(t + i) * 0.12;
    });
    camera.position.x = Math.sin(t*0.2)*3;
    camera.lookAt(0,1,0);
  });

  const dispose = () => {
    stopLoop(); ro.disconnect(); renderer.dispose();
    if (container.contains(renderer.domElement))
      container.removeChild(renderer.domElement);
  };
  container._vizDispose = dispose;
  applyStep(0);

  return {
    step: (n) => applyStep(n),
    totalSteps: () => STEPS.length,
    narration: (n) => STEPS[Math.min(n, STEPS.length-1)].narration,
    dispose,
  };
}

/* ═══════════════════════════════════════════════════════════════
   SCENE ROUTER
   Maps every viz type from data.js to a scene builder
═══════════════════════════════════════════════════════════════ */
const BUILDERS = {
  // Graph algorithms
  dijkstra:    sceneDijkstra,
  gps:         sceneDijkstra,
  graphs:      sceneBFS,
  bfs:         sceneBFS,
  social:      sceneBFS,
  dfs:         sceneDFS,
  maze:        sceneDFS,
  backtrack:   sceneDFS,

  // Sorting
  mergesort:   sceneSorting,
  quicksort:   sceneSorting,
  bubbles:     sceneSorting,
  leaderboard: sceneSorting,
  sorting:     sceneSorting,
  cards:       sceneSorting,
  votes:       sceneSorting,
  postal:      sceneSorting,
  podium:      sceneSorting,

  // Arrays
  array:       sceneArray,
  train:       sceneArray,
  terminal:    sceneArray,
  warehouse:   sceneArray,
  conveyor:    sceneArray,
  racetrack:   sceneArray,
  carousel:    sceneArray,
  particles:   sceneArray,
  seats:       sceneArray,
  powerline:   sceneArray,
  dedup:       sceneArray,
  searchbeam:  sceneArray,
  venn:        sceneArray,
  mirror:      sceneArray,
  stockchart:  sceneArray,
  traffic:     sceneArray,
  watchman:    sceneArray,

  // Binary Search
  binarysearch: sceneBinarySearch,
  mountain:    sceneBinarySearch,

  // Trees
  tree:        sceneTree,
  bst:         sceneTree,
  treeviz:     sceneTree,
  fractal:     sceneTree,
  balance:     sceneTree,
  heap:        sceneTree,
  heapviz:     sceneTree,
  trie:        sceneTree,

  // Linked List
  linkedlist:  sceneLinkedList,
  dna:         sceneLinkedList,
  courier:     sceneLinkedList,
  circuit:     sceneLinkedList,

  // Stack / Queue
  stackviz:    sceneStack,
  stack:       sceneStack,

  // Sliding Window / Two Pointers
  windowslide: sceneWindow,
  twopointers: sceneWindow,
  twoptr:      sceneWindow,
  window:      sceneWindow,

  // Dynamic Programming
  dp:          sceneDP,
  vault:       sceneDP,
  dpgrid:      sceneDP,
  grid:        sceneDP,
  chess:       sceneDP,
  canyon:      sceneDP,
  timeline:    sceneDP,

  // Fallback
  default:     sceneDefault,
};

export function mountScene(container, vizType, prob) {
  const key     = (vizType || 'default').toLowerCase().replace(/[\s-]/g,'');
  const builder = BUILDERS[key] || BUILDERS.default;
  try {
    return builder(container, prob);
  } catch (err) {
    console.error(`vizScenes: failed to mount "${vizType}"`, err);
    return sceneDefault(container, prob);
  }
}

// Keep backward-compatible VIZ_SCENES export so any old code doesn't break
export const VIZ_SCENES = new Proxy({}, {
  get(_, vizType) {
    return {
      draw(container, prob) {
        const ctrl = mountScene(container, vizType, prob);
        // Auto-advance through all steps for passive viewing
        let n = 0;
        const iv = setInterval(() => {
          n++;
          if (n >= ctrl.totalSteps()) clearInterval(iv);
          else ctrl.step(n);
        }, 2200);
        container._vizAutoInterval = iv;
      }
    };
  }
});
