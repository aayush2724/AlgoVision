import * as THREE from "three";

const COL = {
  c: 0x5fd6e6,
  cBright: 0xa9f0fa,
  cDim: 0x2a7f8c,
  cDeep: 0x0c2a31,
  bg0: 0x06121a,
  bg1: 0x030a10,
  scene: 0x040d14
};

function lerp(a, b, t) { return a + (b - a) * t; }

export function initScene(canvas) {
  // 1. Setup Renderer with Pixelation
  const dpr = Math.min(window.devicePixelRatio, 2);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true });
  renderer.setPixelRatio(dpr * 0.4); // Downscale for pixelated look
  renderer.setClearColor(COL.bg1, 1);
  
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(COL.bg1, 22, 72);

  const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 200);
  camera.position.set(0, 2, 26);
  camera.lookAt(0, -1, 0);

  // 2. Lights
  const pLight = new THREE.PointLight(COL.c, 120, 100);
  pLight.position.set(0, 10, 10);
  scene.add(pLight);
  scene.add(new THREE.AmbientLight(COL.cDeep, 0.5));

  // 3. Grid Floor & Ceiling
  const gridGroup = new THREE.Group();
  scene.add(gridGroup);

  const createGrid = (y, opacity) => {
    const group = new THREE.Group();
    const g1 = new THREE.GridHelper(160, 80, COL.c, COL.cDim);
    g1.material.transparent = true;
    g1.material.opacity = opacity;
    const g2 = g1.clone();
    g2.position.z = -160;
    group.add(g1, g2);
    group.position.y = y;
    return group;
  };

  const floorGrid = createGrid(-7, 0.62);
  const ceilingGrid = createGrid(16, 0.18);
  gridGroup.add(floorGrid, ceilingGrid);

  // 4. Dust Particles
  const partCount = 150;
  const partPos = new Float32Array(partCount * 3);
  for(let i=0; i<partCount*3; i++) partPos[i] = (Math.random()-0.5) * 100;
  const partGeo = new THREE.BufferGeometry();
  partGeo.setAttribute('position', new THREE.BufferAttribute(partPos, 3));
  const partMat = new THREE.PointsMaterial({ color: COL.c, size: 0.1, transparent: true, opacity: 0.3 });
  const particles = new THREE.Points(partGeo, partMat);
  scene.add(particles);

  // 5. Block-Build Centerpiece (16 Cubes)
  const cubeCount = 16;
  const cubes = [];
  const cubeGroup = new THREE.Group();
  cubeGroup.position.set(0, -5, -3.5);
  cubeGroup.scale.set(0.56, 0.56, 0.56);
  scene.add(cubeGroup);

  const cubeGeo = new THREE.BoxGeometry(1, 1, 1);
  for(let i=0; i<cubeCount; i++) {
    const lightness = 0.34 + (i / cubeCount) * 0.24;
    const color = new THREE.Color().setHSL(0.52, 0.5, lightness);
    const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.2, metalness: 0.8 });
    const mesh = new THREE.Mesh(cubeGeo, mat);
    
    // Wireframe overlay
    const edges = new THREE.EdgesGeometry(cubeGeo);
    const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: COL.c, transparent: true, opacity: 0.3 }));
    mesh.add(line);
    
    cubeGroup.add(mesh);
    cubes.push(mesh);
  }

  // 6. Layouts
  const layouts = [
    // 0: HERO SPIRAL
    (i) => {
      const r = 2.2;
      const th = i * 0.8;
      const y = (i - 8) * 0.75;
      return new THREE.Vector3(r * Math.cos(th), y, r * Math.sin(th));
    },
    // 1: ARRAY
    (i) => new THREE.Vector3((i - 7.5) * 1.12, 0, 0),
    // 2: MATRIX (4x4)
    (i) => new THREE.Vector3((i % 4 - 1.5) * 1.5, (Math.floor(i / 4) - 1.5) * 1.5, 0),
    // 3: TREE (Binary)
    (i) => {
      const depth = Math.floor(Math.log2(i + 1));
      const posInLevel = i - (Math.pow(2, depth) - 1);
      const levelWidth = Math.pow(2, depth);
      return new THREE.Vector3((posInLevel + 0.5 - levelWidth/2) * (16 / levelWidth), 6 - depth * 3, 0);
    },
    // 4: GRAPH (Ring + Jitter)
    (i) => {
      const r = 5;
      const th = (i / 16) * Math.PI * 2;
      return new THREE.Vector3(r * Math.cos(th), r * Math.sin(th), (Math.random()-0.5)*4);
    }
  ];

  // Static positions for layout 4 to avoid flickering
  const layout4Positions = Array.from({length: 16}, (_, i) => layouts[4](i));

  const getTargetPos = (i, layoutIdx) => {
    if (layoutIdx === 4) return layout4Positions[i];
    return layouts[layoutIdx](i);
  };

  // 7. Edges System
  const edgeGeo = new THREE.BufferGeometry();
  const edgePos = new Float32Array(100 * 2 * 3); // Max 100 edges
  edgeGeo.setAttribute('position', new THREE.BufferAttribute(edgePos, 3));
  const edgeMat = new THREE.LineBasicMaterial({ color: COL.c, transparent: true, opacity: 0.3 });
  const edgeLines = new THREE.LineSegments(edgeGeo, edgeMat);
  cubeGroup.add(edgeLines);

  // 8. Interaction State
  const mouse = new THREE.Vector2(0, 0);
  window.addEventListener('mousemove', (e) => {
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  });

  const scrollData = { progress: 0, target: 0 };
  window.addEventListener('scroll', () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    scrollData.target = max > 0 ? window.scrollY / max : 0;
  });

  // 9. Animation Loop
  let lastTime = 0;
  const loop = (time) => {
    const dt = (time - lastTime) / 1000 || 0;
    lastTime = time;

    // Scroll smoothing
    scrollData.progress = lerp(scrollData.progress, scrollData.target, 0.1);
    const layoutF = scrollData.progress * (layouts.length - 1);
    const l0 = Math.floor(layoutF);
    const l1 = Math.min(l0 + 1, layouts.length - 1);
    const lFrac = layoutF - l0;

    // Morph Cubes
    cubes.forEach((cube, i) => {
      const p0 = getTargetPos(i, l0);
      const p1 = getTargetPos(i, l1);
      cube.position.lerpVectors(p0, p1, lFrac);
      
      // Gentle wobble
      cube.rotation.x += dt * 0.2 + i * 0.01;
      cube.rotation.y += dt * 0.3;
      const scale = 1 + Math.sin(time * 0.001 + i) * 0.05;
      cube.scale.set(scale, scale, scale);
    });

    // Update Edges
    let eIdx = 0;
    const addEdge = (a, b) => {
      const pA = cubes[a].position;
      const pB = cubes[b].position;
      edgePos[eIdx++] = pA.x; edgePos[eIdx++] = pA.y; edgePos[eIdx++] = pA.z;
      edgePos[eIdx++] = pB.x; edgePos[eIdx++] = pB.y; edgePos[eIdx++] = pB.z;
    };

    if (l0 === 1 || l1 === 1) { // Array edges
      for(let i=0; i<15; i++) addEdge(i, i+1);
    } else if (l0 === 3 || l1 === 3) { // Tree edges
      for(let i=1; i<16; i++) addEdge(i, Math.floor((i-1)/2));
    } else if (l0 === 4 || l1 === 4) { // Graph edges
      for(let i=0; i<16; i++) {
        for(let j=i+1; j<16; j++) {
          if (cubes[i].position.distanceTo(cubes[j].position) < 4.6) addEdge(i, j);
        }
      }
    }
    edgeGeo.attributes.position.needsUpdate = true;
    edgeGeo.setDrawRange(0, eIdx / 3);

    // Grid Leapfrog
    floorGrid.position.z += 0.05;
    if (floorGrid.position.z > 80) floorGrid.position.z -= 80;
    ceilingGrid.position.z += 0.02;
    if (ceilingGrid.position.z > 80) ceilingGrid.position.z -= 80;

    // Camera Parallax
    camera.position.x = lerp(camera.position.x, mouse.x * 3, 0.05);
    camera.position.y = lerp(camera.position.y, 2 - mouse.y * 2, 0.05);
    camera.lookAt(0, -1, 0);
    scene.rotation.y = lerp(scene.rotation.y, mouse.x * 0.05, 0.05);

    renderer.render(scene, camera);
    requestAnimationFrame(loop);
  };

  // Intro Animation
  gridGroup.position.y = -13;
  gridGroup.children.forEach(g => {
    g.children.forEach(gh => {
      gh.material.opacity = 0;
    });
  });

  gsap.to(gridGroup.position, { y: 0, duration: 0.8, ease: "power3.out" });
  gridGroup.children.forEach(g => {
    const targetOpacity = g === floorGrid ? 0.62 : 0.18;
    g.children.forEach(gh => {
      gsap.to(gh.material, { opacity: targetOpacity, duration: 0.8 });
    });
  });

  const resize = () => {
    const w = window.innerWidth, h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  window.addEventListener("resize", resize);
  resize();

  requestAnimationFrame(loop);

  return {
    setTheme: () => {} // Kept for compatibility
  };
}
