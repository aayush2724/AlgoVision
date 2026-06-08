import * as THREE from 'three';

const VERTEX_SHADER = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position, 1.0);
  }
`;

const FRAGMENT_SHADER = `
  uniform float uTime;
  uniform vec2 uResolution;
  uniform vec2 uMouse;
  uniform vec3 uColor1;
  uniform vec3 uColor2;
  varying vec2 vUv;

  // Classic Perlin Noise
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

  float snoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
    vec2 i  = floor(v + dot(v, C.yy) );
    vec2 x0 = v -   i + dot(i, C.xx);
    vec2 i1;
    i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;
    i = mod289(i);
    vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 )) + i.x + vec3(0.0, i1.x, 1.0 ));
    vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
    m = m*m ;
    m = m*m ;
    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;
    m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
    vec3 g;
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
  }

  void main() {
    vec2 uv = vUv;
    float time = uTime * 0.1;
    
    // Domain warping
    float n1 = snoise(uv * 3.0 + time);
    float n2 = snoise(uv * 6.0 + n1 + time * 0.5);
    float finalNoise = snoise(uv * 2.0 + n2);
    
    // Mouse halo
    float dist = distance(uv, uMouse);
    float halo = smoothstep(0.4, 0.0, dist) * 0.15;
    
    vec3 color = mix(uColor1, uColor2, finalNoise * 0.5 + 0.5);
    color += halo;
    
    // Vignette
    float vignette = smoothstep(1.5, 0.5, length(uv - 0.5));
    color *= vignette;
    
    // Faint grain
    float grain = (fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) * 0.05;
    color += grain;
    
    gl_FragColor = vec4(color, 1.0);
  }
`;

const THEMES = {
  default: { c1: new THREE.Color(0x060713), c2: new THREE.Color(0x4d7bff) },
  purple: { c1: new THREE.Color(0x0d1020), c2: new THREE.Color(0x8b5cff) },
  cyan: { c1: new THREE.Color(0x060713), c2: new THREE.Color(0x38bdf8) },
  deep: { c1: new THREE.Color(0x050505), c2: new THREE.Color(0xa855f7) }
};

export function initScene(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

  const uniforms = {
    uTime: { value: 0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
    uMouse: { value: new THREE.Vector2(0.5, 0.5) },
    uColor1: { value: THEMES.default.c1 },
    uColor2: { value: THEMES.default.c2 }
  };

  const geometry = new THREE.PlaneGeometry(2, 2);
  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: VERTEX_SHADER,
    fragmentShader: FRAGMENT_SHADER
  });

  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  function resize() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    uniforms.uResolution.value.set(window.innerWidth, window.innerHeight);
  }

  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', (e) => {
    uniforms.uMouse.value.set(e.clientX / window.innerWidth, 1.0 - (e.clientY / window.innerHeight));
  });

  function animate(time) {
    uniforms.uTime.value = time * 0.001;
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);

  return {
    setTheme(name) {
      const theme = THEMES[name] || THEMES.default;
      gsap.to(uniforms.uColor1.value, { r: theme.c1.r, g: theme.c1.g, b: theme.c1.b, duration: 2 });
      gsap.to(uniforms.uColor2.value, { r: theme.c2.r, g: theme.c2.g, b: theme.c2.b, duration: 2 });
    }
  };
}
