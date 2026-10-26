/* KOSIF three-kit — the cinematic building blocks behind the 3D films, as an ES module bundled by esbuild
   (motion.py bundle). Everything is deterministic: seeded noise, no clocks; every block is driven by a time t.
   Blocks: noise & textures · renderer · sky + sun · terrain (ridged FBM, detail maps, vertex colours) · forest
   (instanced two-tier conifers) · sea (reflective Water) · cloud slab (raymarched) · vapour / rain points · lens
   flare · post stack (bloom, god rays, DOF, grade + vignette + CA, film grain, ACES) · camera keys · GPU motion blur. */
import * as THREE from "three";
import { Sky } from "three/examples/jsm/objects/Sky.js";
import { Water } from "three/examples/jsm/objects/Water.js";
import { Lensflare, LensflareElement } from "three/examples/jsm/objects/Lensflare.js";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { BokehPass } from "three/examples/jsm/postprocessing/BokehPass.js";
import { FilmPass } from "three/examples/jsm/postprocessing/FilmPass.js";
import { ShaderPass } from "three/examples/jsm/postprocessing/ShaderPass.js";
import { OutputPass } from "three/examples/jsm/postprocessing/OutputPass.js";
import { mergeGeometries, mergeVertices } from "three/examples/jsm/utils/BufferGeometryUtils.js";

export { THREE };

/* ───────── seeded noise (CPU) ───────── */
export function rng(seed) { let a = seed >>> 0 || 1; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const PERM = (() => { const r = rng(1337), p = []; for (let i = 0; i < 256; i++) p[i] = i; for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; } return p.concat(p); })();
const fade = (t) => t * t * t * (t * (t * 6 - 15) + 10);
export const lerp = (a, b, t) => a + (b - a) * t;
function grad(h, x, y) { switch (h & 3) { case 0: return x + y; case 1: return -x + y; case 2: return x - y; default: return -x - y; } }
export function perlin(x, y) {                            // 2D Perlin, [-1, 1]
  const X = Math.floor(x) & 255, Y = Math.floor(y) & 255; x -= Math.floor(x); y -= Math.floor(y);
  const u = fade(x), v = fade(y), A = PERM[X] + Y, B = PERM[X + 1] + Y;
  return lerp(lerp(grad(PERM[A], x, y), grad(PERM[B], x - 1, y), u), lerp(grad(PERM[A + 1], x, y - 1), grad(PERM[B + 1], x - 1, y - 1), u), v);
}
export function fbm(x, y, oct = 5, lac = 2.0, gain = 0.5) { let a = 0, w = 1, s = 0; for (let i = 0; i < oct; i++) { a += w * perlin(x, y); s += w; x *= lac; y *= lac; w *= gain; } return a / s; }
export function ridged(x, y, oct = 5) { let a = 0, w = 1, s = 0; for (let i = 0; i < oct; i++) { a += w * (1 - Math.abs(perlin(x, y))); s += w; x *= 2.1; y *= 2.1; w *= 0.5; } return a / s; }
export const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
export const clamp01 = (x) => Math.min(1, Math.max(0, x));
export const ramp = (t, a, b) => clamp01((t - a) / Math.max(1e-3, b - a));

/* ───────── generated textures (no downloads) ───────── */
export function noiseCanvas(N, fn) {
  const cv = document.createElement("canvas"); cv.width = cv.height = N;
  const ctx = cv.getContext("2d"), img = ctx.createImageData(N, N), d = img.data;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const o = (y * N + x) * 4; const [r, g, b, a] = fn(x, y); d[o] = r; d[o + 1] = g; d[o + 2] = b; d[o + 3] = a == null ? 255 : a; }
  ctx.putImageData(img, 0, 0);
  const tex = new THREE.CanvasTexture(cv); tex.wrapS = tex.wrapT = THREE.RepeatWrapping; return tex;
}
export function normalFromHeight(N, hfn, strength) {
  const h = new Float32Array(N * N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) h[y * N + x] = hfn(x, y);
  return noiseCanvas(N, (x, y) => {
    const l = h[y * N + ((x - 1 + N) % N)], r = h[y * N + ((x + 1) % N)], u = h[((y - 1 + N) % N) * N + x], dn = h[((y + 1) % N) * N + x];
    const nx = (l - r) * strength, ny = (u - dn) * strength, len = Math.hypot(nx, ny, 1);
    return [128 + 127 * nx / len, 128 + 127 * ny / len, 128 + 127 / len];
  });
}
export function spriteTex(kind) {                          // "soft" disc, "ring", or a vertical "streak"
  const S = 128, cv = document.createElement("canvas"); cv.width = cv.height = S; const ctx = cv.getContext("2d");
  if (kind === "soft") {
    const g = ctx.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
    g.addColorStop(0, "rgba(255,255,255,1)"); g.addColorStop(0.35, "rgba(255,255,255,.55)"); g.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
  } else if (kind === "ring") {
    const g = ctx.createRadialGradient(S / 2, S / 2, S * 0.3, S / 2, S / 2, S / 2);
    g.addColorStop(0, "rgba(255,255,255,0)"); g.addColorStop(0.7, "rgba(255,220,180,.35)"); g.addColorStop(0.85, "rgba(255,255,255,.5)"); g.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
  } else {
    const g = ctx.createLinearGradient(0, 0, 0, S);
    g.addColorStop(0, "rgba(255,255,255,0)"); g.addColorStop(0.5, "rgba(255,255,255,.9)"); g.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = g; ctx.fillRect(S / 2 - 3, 0, 6, S);
  }
  return new THREE.CanvasTexture(cv);
}

/* ───────── renderer, sky, lights ───────── */
export function makeRenderer(canvas, W, H, o = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance", preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
  // tone curve: "aces" (punchy toe and shoulder, the default), "agx" (no hue shift in highlights: fire, neon, sunsets stay
  // their colour — the photographic choice), "neutral" (Khronos PBR Neutral: albedo-faithful, products)
  const TM = { aces: THREE.ACESFilmicToneMapping, agx: THREE.AgXToneMapping, neutral: THREE.NeutralToneMapping };
  renderer.toneMapping = TM[o.tone || "aces"] || THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = o.exposure == null ? 0.6 : o.exposure;
  return renderer;
}
export function makeSky(scene, o = {}) {
  const sky = new Sky(); sky.scale.setScalar(o.scale || 45000); scene.add(sky);
  const u = sky.material.uniforms;
  u.turbidity.value = o.turbidity == null ? 3 : o.turbidity; u.rayleigh.value = o.rayleigh == null ? 1.6 : o.rayleigh;
  u.mieCoefficient.value = o.mie == null ? 0.004 : o.mie; u.mieDirectionalG.value = o.mieG == null ? 0.85 : o.mieG;
  const sun = new THREE.Vector3();
  const setSun = (elevDeg, azimDeg) => {
    sun.setFromSphericalCoords(1, THREE.MathUtils.degToRad(90 - elevDeg), THREE.MathUtils.degToRad(azimDeg));
    u.sunPosition.value.copy(sun); return sun;
  };
  return { sky, uniforms: u, sun, setSun };
}
export function makeSunLight(scene, o = {}) {
  const light = new THREE.DirectionalLight(0xffffff, o.intensity == null ? 3.0 : o.intensity);
  light.castShadow = true; light.shadow.mapSize.set(o.shadowSize || 4096, o.shadowSize || 4096);
  const b = o.bounds || 2300, sc = light.shadow.camera; sc.left = -b; sc.right = b; sc.top = b; sc.bottom = -b; sc.near = 100; sc.far = o.far || 9000;
  light.shadow.bias = -0.0005; light.shadow.normalBias = 2.0;
  scene.add(light, light.target);
  return light;
}
export function makeFill(scene, color = 0xcfe0ff) {        // a camera-side fill without shadows: the cinematographer's bounce
  const fill = new THREE.DirectionalLight(color, 0); scene.add(fill, fill.target); return fill;
}

/* ───────── land ───────── */
/* height(x, z) → y; colour(h, slope, x, z, Color) fills the Color; detail = tiled albedo + normal maps */
export function makeTerrain(o) {
  const SEG = o.seg || 560, SIZE = o.size || 4600;
  const geo = new THREE.PlaneGeometry(SIZE, SIZE, SEG, SEG); geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position, col = new Float32Array(pos.count * 3), c = new THREE.Color();
  for (let i = 0; i < pos.count; i++) pos.setY(i, o.height(pos.getX(i), pos.getZ(i)));
  geo.computeVertexNormals();
  const nrm = geo.attributes.normal;
  for (let i = 0; i < pos.count; i++) {
    o.colour(pos.getY(i), 1 - nrm.getY(i), pos.getX(i), pos.getZ(i), c);
    col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
  }
  geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
  const TS = o.texSize || 1024;
  const albedo = noiseCanvas(TS, (x, y) => { const m = 0.78 + 0.22 * (0.5 + 0.5 * fbm(x / 40, y / 40, 4)) + 0.12 * fbm(x / 7 + 3, y / 7, 2); const v = Math.round(255 * Math.min(1, m)); return [v, v, v]; });
  albedo.repeat.set(o.albedoRepeat || 60, o.albedoRepeat || 60);
  const detail = normalFromHeight(TS, (x, y) => fbm(x / 30, y / 30, 4) * 0.5 + fbm(x / 6 + 9, y / 6 + 2, 3) * 0.22, 3.0);
  detail.repeat.set(o.normalRepeat || 90, o.normalRepeat || 90);
  const mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, map: albedo, normalMap: detail,
    normalScale: new THREE.Vector2(o.normalScale || 0.55, o.normalScale || 0.55), roughness: o.roughness == null ? 0.95 : o.roughness, metalness: 0 }));
  mesh.castShadow = true; mesh.receiveShadow = true;
  return mesh;
}
/* the standard alpine palette: sand → grass → rock by height and slope, snow on the tops */
export function alpineColour(h, slope, x, z, c) {
  const snow = alpineColour.snow || (alpineColour.snow = new THREE.Color(0xf4f7fb)), rock = new THREE.Color(0x5d5a58), rock2 = new THREE.Color(0x7a6f66),
        grass = new THREE.Color(0x4e6e34), grass2 = new THREE.Color(0x6b8a3c), sand = new THREE.Color(0xb9a77a), deep = new THREE.Color(0x2f4a3a);
  const v = 0.5 + 0.5 * fbm(x * 0.01 + 11, z * 0.01 + 5, 3);
  if (h < -5) c.copy(deep);
  else if (h < 25) c.copy(sand).lerp(grass, smooth(5, 25, h));
  else c.copy(grass).lerp(grass2, v);
  if (h > 120) c.lerp(rock.clone().lerp(rock2, v), smooth(120, 420, h) * 0.8);
  c.lerp(rock, smooth(0.28, 0.6, slope));
  if (h > 520) c.lerp(snow, smooth(520, 700, h) * (1 - smooth(0.35, 0.7, slope)));
}
export function slopeOf(height, x, z) { const e = 6; const dx = height(x + e, z) - height(x - e, z), dz = height(x, z + e) - height(x, z - e); return Math.hypot(dx, dz) / (2 * e); }

/* a conifer crown: stacked tiers whose rims are pushed in and out by seeded noise, so the silhouette reads as
   layered branches rather than a cone; the top tier is a narrow spire */
export function coniferCrown(tiers = 4, seed = 7) {
  const r = rng(seed), parts = [];
  let y = 9, radius = 9.5, h = 11;
  for (let i = 0; i < tiers; i++) {
    const g = new THREE.ConeGeometry(radius, h, 9, 1, false);
    const p = g.attributes.position;
    for (let k = 0; k < p.count; k++) {
      if (Math.abs(p.getY(k) + h / 2) < 1e-3) {           // rim vertices: jagged, drooping
        const a = Math.atan2(p.getZ(k), p.getX(k)), m = 0.72 + 0.4 * r();
        p.setX(k, p.getX(k) * m); p.setZ(k, p.getZ(k) * m); p.setY(k, p.getY(k) - 1.5 * r());
        void a;
      }
    }
    g.translate(0, y + h / 2 - 2, 0);
    g.computeVertexNormals();
    parts.push(g);
    y += h * 0.55; radius *= 0.74; h *= 0.9;
  }
  const spire = new THREE.ConeGeometry(radius * 0.8, h * 1.1, 7, 1, false); spire.translate(0, y + h * 0.4, 0);
  parts.push(spire);
  return mergeGeometries(parts);
}

/* instanced conifers; accept(x, z, h) decides where they grow */
export function makeForest(o) {
  const r = rng(o.seed || 42), MAX = o.max || 22000, [x0, x1, z0, z1] = o.region;
  const mats = [], cols = [], tmp = new THREE.Object3D(), cc = new THREE.Color();
  let tries = 0;
  while (mats.length < MAX && tries < MAX * 12) {
    tries++;
    const x = x0 + r() * (x1 - x0), z = z0 + r() * (z1 - z0), h = o.height(x, z);
    if (!o.accept(x, z, h)) continue;
    const clump = 0.5 + 0.5 * fbm(x * 0.0025 + 31, z * 0.0025 + 17, 3);
    if (r() > clump * clump * 1.4) continue;
    const s = (o.scale || 1) * (0.65 + r() * 0.75 - 0.35 * smooth(o.thinFrom || 300, o.thinTo || 430, h));
    tmp.position.set(x, h - 1, z); tmp.rotation.y = r() * Math.PI * 2; tmp.scale.set(s * (0.85 + 0.3 * r()), s * (0.8 + 0.5 * r()), s * (0.85 + 0.3 * r())); tmp.updateMatrix();
    mats.push(tmp.matrix.clone());
    cc.setHSL((o.hue == null ? 0.25 : o.hue) + 0.07 * (r() - 0.5), 0.3 + 0.25 * r(), 0.1 + 0.1 * r());
    cols.push(cc.clone());
  }
  const crown = coniferCrown(o.tiers || 4);
  const trunk = new THREE.CylinderGeometry(1.1, 1.6, 10, 5); trunk.translate(0, 5, 0);
  const crowns = new THREE.InstancedMesh(crown, new THREE.MeshStandardMaterial({ roughness: 0.9, metalness: 0 }), mats.length);
  const trunks = new THREE.InstancedMesh(trunk, new THREE.MeshStandardMaterial({ color: 0x4a3524, roughness: 0.95 }), mats.length);
  for (let i = 0; i < mats.length; i++) { crowns.setMatrixAt(i, mats[i]); trunks.setMatrixAt(i, mats[i]); crowns.setColorAt(i, cols[i]); }
  crowns.instanceMatrix.needsUpdate = true; trunks.instanceMatrix.needsUpdate = true; crowns.instanceColor.needsUpdate = true;
  crowns.castShadow = true; crowns.receiveShadow = true; trunks.castShadow = true;
  const g = new THREE.Group(); g.add(crowns, trunks); g.userData.count = mats.length;
  return g;
}

/* a flock of birds: instanced V shapes that flap, following a path of [t, x, y, z] keys with seeded offsets;
   visible between t0 and t1 (userData.set(t)) */
export function makeFlock(o) {
  const N = o.n || 18, r = rng(o.seed || 23), keys = o.path;
  const geo = new THREE.BufferGeometry();
  // wings: two triangles spanning local X (the bird flies along local -Z); body: a small vertical sliver so the
  // bird still reads when seen level, where a flat wing would be edge-on
  const verts = new Float32Array([ -1, 0, 0, 0, 0, 0.35, 0, 0, -0.35,   1, 0, 0, 0, 0, -0.35, 0, 0, 0.35,
                                   0, 0.12, 0.45, 0, -0.12, 0.2, 0, 0.12, -0.5,   0, -0.12, 0.2, 0, -0.12, -0.3, 0, 0.12, -0.5 ]);
  geo.setAttribute("position", new THREE.BufferAttribute(verts, 3));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uOn: { value: 0 }, uColor: { value: new THREE.Color(o.color == null ? 0x1a1d22 : o.color) } },
    vertexShader: `attribute float phase; uniform float uT, uOn; varying float vA;
      void main(){ vec3 p = position; float flap = sin(uT * 9.0 + phase * 6.2832) * 0.8;
        p.y += abs(p.x) * (0.3 + flap);                           // dihedral + the wing tips beating up and down
        vec4 mv = modelViewMatrix * instanceMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv; vA = uOn; }`,
    fragmentShader: `uniform vec3 uColor; varying float vA; void main(){ if (vA < 0.01) discard; gl_FragColor = vec4(uColor, 1.0); }`,
    side: THREE.DoubleSide, transparent: true });
  const mesh = new THREE.InstancedMesh(geo, mat, N);
  const phase = new Float32Array(N), offs = [];
  for (let i = 0; i < N; i++) { phase[i] = r(); offs.push(new THREE.Vector3((r() - 0.5) * (o.spread || 120), (r() - 0.5) * (o.spread || 120) * 0.35, (r() - 0.5) * (o.spread || 120))); }
  geo.setAttribute("phase", new THREE.InstancedBufferAttribute(phase, 1));
  mesh.frustumCulled = false;
  const tmp = new THREE.Object3D(), pos = new THREE.Vector3(), nxt = new THREE.Vector3();
  const at = (t, out) => { let i = 0; while (i < keys.length - 2 && t > keys[i + 1][0]) i++;
    const a = keys[i], b = keys[i + 1], u = clamp01((t - a[0]) / Math.max(1e-3, b[0] - a[0]));
    return out.set(lerp(a[1], b[1], u), lerp(a[2], b[2], u), lerp(a[3], b[3], u)); };
  mesh.userData.set = (t) => {
    const on = t >= o.t0 && t <= o.t1 ? 1 : 0;
    mat.uniforms.uT.value = t; mat.uniforms.uOn.value = on;
    if (!on) return;
    at(t, pos); at(t + 0.2, nxt);
    const dir = nxt.clone().sub(pos); if (dir.lengthSq() < 1e-6) dir.set(1, 0, 0);
    for (let i = 0; i < N; i++) {
      tmp.position.copy(pos).add(offs[i]); tmp.position.y += Math.sin(t * 1.3 + phase[i] * 6.28) * 6;
      tmp.lookAt(tmp.position.clone().sub(dir));                // Object3D.lookAt points local +Z at the target; the bird flies along -Z
      tmp.scale.setScalar((o.size || 9) * (0.8 + 0.4 * phase[i])); tmp.updateMatrix(); mesh.setMatrixAt(i, tmp.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
  };
  return mesh;
}

/* ───────── water ───────── */
export function makeSea(o = {}) {
  const normals = o.normals || normalFromHeight(512, (x, y) => fbm(x / 36, y / 36, 4) * 0.6 + fbm(x / 9 + 50, y / 9, 2) * 0.25, 2.2);
  const water = new Water(new THREE.PlaneGeometry(o.size || 30000, o.size || 30000), {
    textureWidth: o.res || 768, textureHeight: o.res || 768, waterNormals: normals, sunDirection: new THREE.Vector3(), sunColor: 0xffffff,
    waterColor: o.color == null ? 0x0e4a63 : o.color, distortionScale: o.distortion == null ? 2.4 : o.distortion, fog: true, size: o.waveSize || 3.0 });
  water.rotation.x = -Math.PI / 2; water.position.y = o.level || 0;
  water.userData.normals = normals;
  return water;
}
/* a flat ribbon of water along a curve (a river): a tube flattened per segment, revealed with setDrawRange */
export function makeRibbon(curve, o = {}) {
  const segs = o.segments || 220, ring = (o.radial || 10) + 1;
  const geo = new THREE.TubeGeometry(curve, segs, o.radius || 11, o.radial || 10, false);
  const rp = geo.attributes.position;
  for (let i = 0; i <= segs; i++) { const cpt = curve.getPointAt(i / segs); for (let j = 0; j < ring; j++) { const k = i * ring + j; rp.setY(k, cpt.y + (rp.getY(k) - cpt.y) * (o.flatten || 0.3)); } }
  rp.needsUpdate = true; geo.computeVertexNormals();
  const tex = (o.normals || normalFromHeight(512, (x, y) => fbm(x / 36, y / 36, 4) * 0.6 + fbm(x / 9 + 50, y / 9, 2) * 0.25, 2.2)).clone();
  tex.needsUpdate = true; tex.repeat.set(1, o.repeat || 14);
  const mat = new THREE.MeshPhysicalMaterial({ color: o.color == null ? 0x6fb4d6 : o.color, roughness: 0.08, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.05,
    normalMap: tex, normalScale: new THREE.Vector2(0.5, 0.5), emissive: o.emissive == null ? 0x1a5f85 : o.emissive, emissiveIntensity: 0.55, transparent: true, opacity: 0.94 });
  const mesh = new THREE.Mesh(geo, mat); mesh.position.y = 0.5; mesh.receiveShadow = true;
  geo.setDrawRange(0, 0);
  mesh.userData.reveal = (p) => geo.setDrawRange(0, Math.floor(geo.index.count * (p * p * (3 - 2 * p))));
  mesh.userData.flow = (t, speed = 0.9) => { tex.offset.y = -t * speed; };
  return mesh;
}

/* ───────── sky things ───────── */
export function makeCloudSlab(o = {}) {
  const size = o.size || [7000, 520, 4200], center = o.center || [0, 1240, -900];
  const min = new THREE.Vector3(center[0] - size[0] / 2, center[1] - size[1] / 2, center[2] - size[2] / 2), max = new THREE.Vector3(center[0] + size[0] / 2, center[1] + size[1] / 2, center[2] + size[2] / 2);
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uCover: { value: 0 }, uDark: { value: 0 }, uSun: { value: new THREE.Vector3(0, 1, 0) }, uCam: { value: new THREE.Vector3() },
                uMin: { value: min }, uMax: { value: max }, uSkyCol: { value: new THREE.Color(0x9fb6cc) }, uSunCol: { value: new THREE.Color(0xfff2d9) } },
    vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `precision highp float; varying vec3 vW; uniform float uT, uCover, uDark; uniform vec3 uSun, uCam, uMin, uMax, uSkyCol, uSunCol;
      float hsh(vec3 p){ return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }
      float vn(vec3 p){ vec3 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
        return mix(mix(mix(hsh(i), hsh(i+vec3(1,0,0)), f.x), mix(hsh(i+vec3(0,1,0)), hsh(i+vec3(1,1,0)), f.x), f.y),
                   mix(mix(hsh(i+vec3(0,0,1)), hsh(i+vec3(1,0,1)), f.x), mix(hsh(i+vec3(0,1,1)), hsh(i+vec3(1,1,1)), f.x), f.y), f.z); }
      float fbm3(vec3 p){ float a = 0.0, w = 0.5; for (int i = 0; i < 4; i++) { a += w * vn(p); p = p * 2.03 + vec3(11.0); w *= 0.5; } return a; }
      float dens(vec3 p){ float hgt = (p.y - uMin.y) / (uMax.y - uMin.y);
        float prof = smoothstep(0.0, 0.25, hgt) * (1.0 - smoothstep(0.55, 1.0, hgt));
        vec3 q = p * 0.0011 + vec3(uT * 0.025, 0.0, uT * 0.012);
        float base = fbm3(q) * 0.75 + fbm3(q * 3.1 + vec3(5.0)) * 0.25;
        float cov = mix(0.72, 0.36, uCover);
        return clamp((base - cov) * 3.2, 0.0, 1.0) * prof * smoothstep(0.0, 0.08, uCover); }
      vec2 boxHit(vec3 ro, vec3 rd){ vec3 t0 = (uMin - ro) / rd, t1 = (uMax - ro) / rd; vec3 a = min(t0, t1), b = max(t0, t1);
        return vec2(max(max(a.x, a.y), a.z), min(min(b.x, b.y), b.z)); }
      void main(){ vec3 rd = normalize(vW - uCam); vec2 h = boxHit(uCam, rd); if (h.y <= max(h.x, 0.0)) discard;
        float tn = max(h.x, 0.0), len = h.y - tn; const int N = 36; float dt = len / float(N);
        float jit = hsh(vec3(gl_FragCoord.xy, 1.0)) * dt;
        vec3 col = vec3(0.0); float T = 1.0; vec3 L = normalize(uSun);
        for (int i = 0; i < N; i++) { vec3 p = uCam + rd * (tn + jit + dt * float(i)); float d = dens(p); if (d < 0.003) continue;
          float lt = 1.0; for (int j = 1; j <= 3; j++) { lt *= exp(-dens(p + L * 70.0 * float(j)) * 70.0 * 0.028); }
          float powder = 1.0 - exp(-d * 2.0);
          vec3 lit = mix(uSkyCol * 0.55, uSunCol, lt * powder) * mix(1.0, 0.42, uDark);
          float a = 1.0 - exp(-d * dt * 0.032); col += T * a * lit; T *= (1.0 - a); if (T < 0.02) break; }
        gl_FragColor = vec4(col, 1.0 - T); }`,
    transparent: true, depthWrite: false, side: THREE.BackSide }));
  mesh.position.set(...center); mesh.frustumCulled = false;
  mesh.userData.set = (t, cover, dark, sun, camPos, sunCol, skyCol) => {
    const u = mesh.material.uniforms; u.uT.value = t; u.uCover.value = clamp01(cover); u.uDark.value = dark; u.uSun.value.copy(sun); u.uCam.value.copy(camPos);
    if (sunCol) u.uSunCol.value.copy(sunCol); if (skyCol) u.uSkyCol.value.copy(skyCol);
  };
  return mesh;
}
export function makeLensflare(o = {}) {
  const soft = spriteTex("soft"), ring = spriteTex("ring");
  const holder = new THREE.Object3D(), flare = new Lensflare();
  flare.addElement(new LensflareElement(soft, 420, 0, new THREE.Color(o.color || 0xffe2b0)));
  flare.addElement(new LensflareElement(ring, 90, 0.35, new THREE.Color(0xffd0a0)));
  flare.addElement(new LensflareElement(soft, 60, 0.55, new THREE.Color(0xaad4ff)));
  flare.addElement(new LensflareElement(ring, 140, 0.75, new THREE.Color(0xffc8a0)));
  flare.addElement(new LensflareElement(soft, 40, 0.95, new THREE.Color(0xffffff)));
  holder.add(flare); holder.userData.flare = flare;
  return holder;
}

/* ───────── particles (Points with seeded phases; uniforms uT, uOn) ───────── */
export function makeVapour(o) {
  const N = o.n || 1400, r = rng(o.seed || 5), seed = new Float32Array(N), base = new Float32Array(N * 3), [x0, x1, z0, z1] = o.region;
  for (let i = 0; i < N; i++) { seed[i] = r(); base[i * 3] = x0 + r() * (x1 - x0); base[i * 3 + 1] = o.y || 0; base[i * 3 + 2] = z0 + r() * (z1 - z0); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(base, 3)); geo.setAttribute("seed", new THREE.BufferAttribute(seed, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uOn: { value: 0 }, uTex: { value: spriteTex("soft") }, uSun: { value: new THREE.Color(0xfff1d6) } },
    vertexShader: `attribute float seed; uniform float uT, uOn; varying float vA;
      void main(){ float life = 6.0 + seed * 4.0; float ph = mod(uT * 0.9 + seed * 37.0, life) / life;
        vec3 p = position; p.y += ph * (520.0 + seed * 420.0); p.x += sin(uT * 0.4 + seed * 20.0) * 40.0 * ph; p.z -= ph * 260.0;
        vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv;
        vA = uOn * (1.0 - ph) * smoothstep(0.0, 0.15, ph) * (0.35 + 0.65 * seed) * smoothstep(250.0, 700.0, -mv.z);
        gl_PointSize = min(170.0, (90.0 + 160.0 * seed) * (1.0 + ph * 1.6) * 900.0 / max(40.0, -mv.z)); }`,
    fragmentShader: `uniform sampler2D uTex; uniform vec3 uSun; varying float vA;
      void main(){ vec4 s = texture2D(uTex, gl_PointCoord); gl_FragColor = vec4(uSun * 1.1, s.a * vA * 0.16); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  const pts = new THREE.Points(geo, mat); pts.userData.set = (t, on) => { mat.uniforms.uT.value = t; mat.uniforms.uOn.value = on; };
  return pts;
}
export function makeRain(o) {
  const N = o.n || 9000, r = rng(o.seed || 11), seed = new Float32Array(N), base = new Float32Array(N * 3), [x0, x1, z0, z1] = o.region;
  for (let i = 0; i < N; i++) { seed[i] = r(); base[i * 3] = x0 + r() * (x1 - x0); base[i * 3 + 1] = 0; base[i * 3 + 2] = z0 + r() * (z1 - z0); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(base, 3)); geo.setAttribute("seed", new THREE.BufferAttribute(seed, 1));
  const mat = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uOn: { value: 0 }, uTex: { value: spriteTex("streak") }, uTop: { value: o.top || 1500 } },
    vertexShader: `attribute float seed; uniform float uT, uOn, uTop; varying float vA;
      void main(){ float h = uTop; float y = h - mod(uT * (900.0 + seed * 500.0) + seed * 4000.0, h);
        vec3 p = position; p.y = y + 80.0; p.x += (y / h) * 120.0;
        vec4 mv = modelViewMatrix * vec4(p, 1.0); gl_Position = projectionMatrix * mv;
        vA = uOn * (0.35 + 0.65 * seed) * smoothstep(40.0, 160.0, -mv.z); gl_PointSize = min(64.0, (26.0 + 30.0 * seed) * 900.0 / max(60.0, -mv.z)); }`,
    fragmentShader: `uniform sampler2D uTex; varying float vA; void main(){ vec4 s = texture2D(uTex, gl_PointCoord); gl_FragColor = vec4(vec3(0.85, 0.92, 1.0), s.a * vA * 0.55); }`,
    transparent: true, depthWrite: false, blending: THREE.NormalBlending });
  const pts = new THREE.Points(geo, mat); pts.userData.set = (t, on) => { mat.uniforms.uT.value = t; mat.uniforms.uOn.value = on; };
  return pts;
}

/* ───────── post stack ───────── */
export function makePost(renderer, scene, camera, W, H, o = {}) {
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const guard = new ShaderPass({ uniforms: { tDiffuse: { value: null }, uMax: { value: o.clampMax || 48.0 } },
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform sampler2D tDiffuse; uniform float uMax; varying vec2 vUv;
      void main(){ vec4 c = texture2D(tDiffuse, vUv); bvec3 bad = bvec3(!(c.r == c.r) || c.r > 1e30, !(c.g == c.g) || c.g > 1e30, !(c.b == c.b) || c.b > 1e30);
        if (any(bad)) c.rgb = vec3(0.0); gl_FragColor = vec4(min(c.rgb, vec3(uMax)), 1.0); }` });
  composer.addPass(guard);                                  // a NaN or an Inf pixel would otherwise bloom into black rectangles
  const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), o.bloom == null ? 0.22 : o.bloom, 0.6, o.bloomThreshold == null ? 0.9 : o.bloomThreshold);
  composer.addPass(bloom);
  const rays = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uSun: { value: new THREE.Vector2(0.5, 0.5) }, uAmount: { value: 0.0 } },
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform sampler2D tDiffuse; uniform vec2 uSun; uniform float uAmount; varying vec2 vUv;
      float dither(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
      void main(){ vec3 base = texture2D(tDiffuse, vUv).rgb; if (uAmount <= 0.001) { gl_FragColor = vec4(base, 1.0); return; }
        const int N = 64; vec2 d = (vUv - uSun) / float(N) * 0.55;
        vec2 p = vUv - d * dither(gl_FragCoord.xy); float illum = 1.0; vec3 acc = vec3(0.0);
        for (int i = 0; i < N; i++) { p -= d; vec3 s = texture2D(tDiffuse, p).rgb; float l = max(0.0, dot(s, vec3(0.3, 0.59, 0.11)) - 0.7);
          acc += s * l * illum; illum *= 0.972; }
        acc /= float(N) * 0.25;
        float edge = 1.0 - smoothstep(0.6, 1.4, length(uSun - 0.5) * 2.0);
        float sky = smoothstep(uSun.y - 0.04, uSun.y + 0.12, vUv.y);
        gl_FragColor = vec4(base + min(acc, vec3(1.2)) * (uAmount * 0.55) * edge * sky, 1.0); }` });
  composer.addPass(rays);
  const bokeh = new BokehPass(scene, camera, { focus: 900, aperture: o.aperture == null ? 0.00004 : o.aperture, maxblur: o.maxblur == null ? 0.0035 : o.maxblur });
  composer.addPass(bokeh);
  const grade = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uWarm: { value: 0.5 }, uVig: { value: o.vignette == null ? 0.42 : o.vignette }, uLift: { value: 0.0 }, uCA: { value: o.ca == null ? 1.2 : o.ca } },
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform sampler2D tDiffuse; uniform float uWarm, uVig, uLift, uCA; varying vec2 vUv;
      void main(){ vec2 d = vUv - 0.5; vec2 off = d * (uCA / 1920.0) * length(d) * 4.0;
        vec3 c = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);
        float l = dot(c, vec3(0.299, 0.587, 0.114));
        vec3 shadows = vec3(0.92, 0.98, 1.08), highs = vec3(1.08, 1.0, 0.92);
        c *= mix(shadows, highs, smoothstep(0.15, 0.85, l)) * mix(vec3(1.0), vec3(1.05, 0.98, 0.9), uWarm);
        c = c * (1.0 - uLift) + uLift * 0.06;
        c *= 1.0 - uVig * smoothstep(0.35, 0.95, length(d) * 1.4);
        gl_FragColor = vec4(c, 1.0); }` });
  composer.addPass(grade);
  const film = new FilmPass(o.grain == null ? 0.16 : o.grain, false);
  composer.addPass(film);
  composer.addPass(new OutputPass());
  /* the sun on screen, for the rays and a lens flare */
  const ndc = new THREE.Vector3();
  const sunOnScreen = (sun) => { camera.updateMatrixWorld(); ndc.copy(sun).multiplyScalar(20000).add(camera.position).project(camera);
    rays.uniforms.uSun.value.set(ndc.x * 0.5 + 0.5, ndc.y * 0.5 + 0.5); return ndc.z < 1; };
  return { composer, guard, bloom, rays, bokeh, grade, film, sunOnScreen };
}

/* ───────── camera keys and the frame loop with optional GPU motion blur ───────── */
/* keys: [t, camX, camY, camZ, lookX, lookY, lookZ] — smoothstep between keys (still between events) */
export function cameraKeys(keys) {
  return (t) => {
    let i = 0; while (i < keys.length - 2 && t > keys[i + 1][0]) i++;
    const a = keys[i], b = keys[i + 1], u = smooth(a[0], b[0], t);
    return [new THREE.Vector3(lerp(a[1], b[1], u), lerp(a[2], b[2], u), lerp(a[3], b[3], u)),
            new THREE.Vector3(lerp(a[4], b[4], u), lerp(a[5], b[5], u), lerp(a[6], b[6], u))];
  };
}
/* render(t) with window.__blur sub-frames accumulated on the GPU (grain fixed per output frame) */
export function makeFrameLoop(renderer, post, W, H, update) {
  window.__nativeBlur = true;                               // film.py: this page accumulates its own sub-frames
  const accRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, depthBuffer: false, stencilBuffer: false });
  const quadScene = new THREE.Scene(), quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const accMat = new THREE.ShaderMaterial({
    uniforms: { tex: { value: null }, w: { value: 1 } }, depthTest: false, depthWrite: false, transparent: true, blending: THREE.CustomBlending,
    blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendEquation: THREE.AddEquation,     // average; MaxEquation = "lighten" stack
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`,
    fragmentShader: `uniform sampler2D tex; uniform float w; varying vec2 vUv; void main(){ gl_FragColor = vec4(texture2D(tex, vUv).rgb * w, 1.0); }` });
  const copyMat = new THREE.ShaderMaterial({
    uniforms: { tex: { value: null } }, depthTest: false, depthWrite: false,
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`,
    fragmentShader: `uniform sampler2D tex; varying vec2 vUv; void main(){ gl_FragColor = vec4(texture2D(tex, vUv).rgb, 1.0); }` });
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), accMat); quadScene.add(quad);
  const { composer, film } = post;
  return function render(t) {
    const k = Math.max(1, Math.floor(window.__blur || 1));
    if (k === 1) { update(t); film.uniforms.time.value = t; composer.renderToScreen = true; composer.render(0); return; }
    const fps = window.__fps || 30, shutter = window.__shutter == null ? 0.5 : window.__shutter;
    // window.__stack = "lighten" keeps each pixel's brightest sample (star trails, light painting, car trails at night);
    // the default averages (motion blur; a long shutter > 1 frame gives silky water and soft crowds)
    const lighten = window.__stack === "lighten";
    accMat.blendEquation = lighten ? THREE.MaxEquation : THREE.AddEquation;
    composer.renderToScreen = false;
    const oldClear = renderer.autoClear;
    renderer.setRenderTarget(accRT); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.setRenderTarget(null);
    for (let i = 0; i < k; i++) {
      update(Math.max(0, t - (shutter / fps) * (i / k)));
      film.uniforms.time.value = t;
      composer.render(0);
      quad.material = accMat; accMat.uniforms.tex.value = composer.readBuffer.texture; accMat.uniforms.w.value = lighten ? 1 : 1 / k;
      renderer.setRenderTarget(accRT); renderer.autoClear = false; renderer.render(quadScene, quadCam); renderer.autoClear = oldClear;
      renderer.setRenderTarget(null);
    }
    quad.material = copyMat; copyMat.uniforms.tex.value = accRT.texture;
    renderer.setRenderTarget(null); renderer.render(quadScene, quadCam);
  };
}

/* ═════════ v3 realism blocks: shallow water, caustics, absorption, wind sway, koi, petals, pebbles, dappled light ═════════
   Scale: metres. Everything is a function of t, so frames render in any order. */

/* GLSL value noise shared by the blocks below */
const GLSL_NOISE = `
  float kh(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float kvn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
    return mix(mix(kh(i), kh(i + vec2(1.0, 0.0)), f.x), mix(kh(i + vec2(0.0, 1.0)), kh(i + vec2(1.0, 1.0)), f.x), f.y); }
  float kridge(vec2 p){ return 1.0 - abs(kvn(p) * 2.0 - 1.0); }
  /* caustic network: two warped ridged layers; their crossings are the bright cells sunlight focuses into */
  float kcaustic(vec2 p, float t){
    vec2 w = vec2(kvn(p * 0.7 + t * 0.15), kvn(p * 0.7 + 17.0 - t * 0.12));
    float a = kridge(p + w * 1.6 + vec2(t * 0.10, -t * 0.07));
    float b = kridge(p * 1.37 - w * 1.2 + vec2(-t * 0.08, t * 0.09) + 5.0);
    return pow(a * b, 6.0) * 3.0 + pow(a, 14.0) * 0.5; }`;

/* an environment map from a bounded sky gradient: top, horizon and ground colours plus a soft sun glow. Use this rather
   than a PMREM of the Sky shader, whose sun disk (~1e4) overflows half-float buffers and turns reflections into NaN */
export function envFromGradient(renderer, scene, o = {}) {
  const pm = new THREE.PMREMGenerator(renderer), s = new THREE.Scene();
  const mat = new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false,
    uniforms: { uTop: { value: new THREE.Color(o.top || 0x7da2cc) }, uHor: { value: new THREE.Color(o.horizon || 0xf0cfa0) }, uGround: { value: new THREE.Color(o.ground || 0x3a3a2a) },
                uSun: { value: (o.sun || new THREE.Vector3(0, 0.3, -1)).clone().normalize() }, uSunCol: { value: new THREE.Color(o.sunColor || 0xffd29a) }, uSunPow: { value: o.sunPower == null ? 6 : o.sunPower } },
    vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform vec3 uTop, uHor, uGround, uSun, uSunCol; uniform float uSunPow; varying vec3 vD;
      void main(){ vec3 d = normalize(vD); vec3 c = d.y > 0.0 ? mix(uHor, uTop, pow(d.y, 0.55)) : mix(uHor, uGround, pow(-d.y, 0.4));
        float g = max(dot(d, uSun), 0.0); c += uSunCol * (pow(g, 64.0) * uSunPow + pow(g, 6.0) * 0.35); gl_FragColor = vec4(c, 1.0); }` });
  s.add(new THREE.Mesh(new THREE.SphereGeometry(100, 48, 24), mat));
  const rt = pm.fromScene(s, 0, 0.1, 1000);
  scene.environment = rt.texture; pm.dispose();
  return rt.texture;
}

/* the sky's light as an environment map (PMREM of the Sky). Beware: the sun disk overflows half floats; prefer envFromGradient */
export function envFromSky(renderer, scene, skyObj) {
  const pm = new THREE.PMREMGenerator(renderer), s = new THREE.Scene(), clone = new THREE.Mesh(skyObj.sky.geometry, skyObj.sky.material);
  clone.scale.copy(skyObj.sky.scale); s.add(clone);
  const rt = pm.fromScene(s, 0, 1, 100000);
  scene.environment = rt.texture; pm.dispose();
  return rt.texture;
}

/* shallow water: sum-of-sines swell with analytic normals, ripple rings (petals, drops, fish), Fresnel sky reflection,
   a GGX sun glint, and see-through transmission whose tint deepens with the viewing angle. o.ripples: max rings. */
export function makeShallowWater(o = {}) {
  const R = o.ripples || 24;
  const geo = new THREE.PlaneGeometry(o.width || 30, o.depth || 30, o.seg || 256, o.seg || 256); geo.rotateX(-Math.PI / 2);
  const uniforms = { uT: { value: 0 }, uSun: { value: new THREE.Vector3(0.3, 0.4, -0.8).normalize() }, uSunCol: { value: new THREE.Color(1, 0.86, 0.62) },
    uSkyTop: { value: new THREE.Color(o.skyTop || 0x6f9cc8) }, uSkyHor: { value: new THREE.Color(o.skyHorizon || 0xf2d6b0) }, uBank: { value: new THREE.Color(o.bank == null ? 0x26301c : o.bank) }, uBankH: { value: o.bankHeight == null ? 0.12 : o.bankHeight },
    uDeep: { value: new THREE.Color(o.deep || 0x0d3b3a) }, uShallow: { value: new THREE.Color(o.shallow || 0x2f6f62) },
    uAmp: { value: o.amp == null ? 0.012 : o.amp }, uRip: { value: Array.from({ length: R }, () => new THREE.Vector4(0, 0, -99, 0)) },
    uEnv: { value: null }, uUseEnv: { value: 0 }, uGlint: { value: o.glint == null ? 1 : o.glint }, uClarity: { value: o.clarity == null ? 0.62 : o.clarity },
    uDapple: { value: null }, uDappleOn: { value: 0 }, uDappleM: { value: new THREE.Matrix4() } };
  const mat = new THREE.ShaderMaterial({ uniforms, transparent: true, depthWrite: false,
    vertexShader: `uniform float uT, uAmp; uniform vec4 uRip[${R}]; varying vec3 vW; varying vec3 vN;
      vec3 swell(vec2 p){ float h = 0.0; vec2 g = vec2(0.0);
        vec2 D[6]; D[0]=vec2(.86,.5); D[1]=vec2(-.36,.93); D[2]=vec2(.2,-.98); D[3]=vec2(-.95,-.3); D[4]=vec2(.64,-.77); D[5]=vec2(-.5,.86);
        for (int i = 0; i < 6; i++){ float k = 2.4 + float(i) * 1.7, w = sqrt(9.81 * k), a = uAmp / (1.0 + float(i) * 0.55);
          float ph = dot(D[i], p) * k - w * uT * 0.55 + float(i) * 1.9; h += a * sin(ph); g += a * k * cos(ph) * D[i]; }
        for (int i = 0; i < ${R}; i++){ vec4 r = uRip[i]; float age = uT - r.z; if (age <= 0.0 || age > 3.5) continue;
          vec2 d = p - r.xy; float dist = length(d) + 1e-4; float front = age * 0.34; float x = dist - front;
          float env = exp(-x * x * 90.0) * exp(-age * 1.15) * r.w / (1.0 + dist * 3.0);
          h += env * sin(x * 52.0); g += env * 52.0 * cos(x * 52.0) * d / dist; }
        return vec3(h, g); }
      void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vec3 s = swell(w.xz); w.y += s.x; vW = w.xyz; vN = normalize(vec3(-s.y, 1.0, -s.z));
        gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform float uT, uGlint, uClarity, uUseEnv, uDappleOn, uBankH; uniform vec3 uSun, uSunCol, uSkyTop, uSkyHor, uDeep, uShallow, uBank;
      uniform samplerCube uEnv; uniform sampler2D uDapple; uniform mat4 uDappleM; varying vec3 vW; varying vec3 vN; ${GLSL_NOISE}
      void main(){ vec3 V = normalize(cameraPosition - vW);
        vec2 q = vW.xz * 3.1; vec2 mn = vec2(kvn(q + uT * 0.35) - kvn(q + 3.7 - uT * 0.31), kvn(q * 1.9 + 9.0 - uT * 0.42) - kvn(q * 1.9 + 4.0 + uT * 0.38));
        vec3 N = normalize(vN + vec3(mn.x, 0.0, mn.y) * 0.09);
        float cosv = clamp(dot(N, V), 0.0, 1.0); float F = 0.02 + 0.98 * pow(1.0 - cosv, 5.0);
        vec3 Rd = reflect(-V, N); Rd.y = abs(Rd.y);
        vec3 refl = mix(uSkyHor, uSkyTop, smoothstep(0.0, 0.55, Rd.y));
        refl = mix(uBank, refl, smoothstep(uBankH * 0.5, uBankH * 1.6, Rd.y));          // near the horizon a pond mirrors its banks, not the sky
        if (uUseEnv > 0.5) refl = mix(refl, textureCube(uEnv, Rd).rgb, 0.7);
        vec3 L = normalize(uSun), H = normalize(L + V); float nh = max(dot(N, H), 0.0), nl = max(dot(N, L), 0.0);
        float a2 = 0.0064; float D = a2 / (3.14159 * pow(nh * nh * (a2 - 1.0) + 1.0, 2.0)); float glint = D * F * nl * 0.09 * uGlint; glint = glint / (1.0 + glint / 0.7);
        float lit = 1.0; if (uDappleOn > 0.5) { vec4 lp = uDappleM * vec4(vW, 1.0); vec2 uv = lp.xy / lp.w * 0.5 + 0.5; lit = texture2D(uDapple, uv).r; }
        float trans = uClarity * pow(cosv, 0.6);
        vec3 body = mix(uDeep, uShallow, cosv) * (0.55 + 0.45 * lit);
        float alpha = clamp(F + (1.0 - F) * (1.0 - trans), 0.0, 1.0);
        vec3 col = (refl * F + body * (1.0 - F) * (1.0 - trans)) / max(alpha, 1e-3) + uSunCol * glint * lit;
        gl_FragColor = vec4(col, alpha);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  const mesh = new THREE.Mesh(geo, mat); mesh.position.y = o.level || 0; mesh.renderOrder = 5; mesh.frustumCulled = false;
  const rings = [];
  mesh.userData.ripple = (x, z, t0, amp = 1) => { rings.push([x, z, t0, amp]); };
  mesh.userData.set = (t, sun, sunCol) => { uniforms.uT.value = t; if (sun) uniforms.uSun.value.copy(sun).normalize(); if (sunCol) uniforms.uSunCol.value.copy(sunCol);
    const live = rings.filter((r) => t - r[2] > -0.01 && t - r[2] < 3.5).sort((a, b) => b[2] - a[2]).slice(0, R);
    for (let i = 0; i < R; i++) { const r = live[i]; uniforms.uRip.value[i].set(r ? r[0] : 0, r ? r[1] : 0, r ? r[2] : -99, r ? r[3] : 0); } };
  mesh.userData.uniforms = uniforms;
  return mesh;
}

/* caustics + water absorption on any MeshStandard/Physical material below the water line (onBeforeCompile).
   Caustics brighten only the direct sunlight (shadows and ambient stay natural); absorption tints with depth. */
export function addCaustics(material, o = {}) {
  const u = { uCT: o.time || { value: 0 }, uCLevel: { value: o.level || 0 }, uCStr: { value: o.strength == null ? 1.6 : o.strength }, uCScale: { value: o.scale || 1.6 },
              uAbs: { value: new THREE.Vector3(...(o.absorb || [1.6, 0.55, 0.42])) }, uCSun: o.sun || { value: new THREE.Vector3(0, 1, 0) } };
  const prev = material.onBeforeCompile;
  material.onBeforeCompile = (sh, r) => {
    if (prev) prev(sh, r);
    Object.assign(sh.uniforms, u);
    sh.vertexShader = "varying vec3 vCW;\n" + sh.vertexShader.replace("#include <worldpos_vertex>", `#include <worldpos_vertex>
      vec4 cwp = vec4(transformed, 1.0);
      #ifdef USE_INSTANCING
        cwp = instanceMatrix * cwp;
      #endif
      vCW = (modelMatrix * cwp).xyz;`);
    sh.fragmentShader = `varying vec3 vCW; uniform float uCT, uCLevel, uCStr, uCScale; uniform vec3 uAbs, uCSun; ${GLSL_NOISE}\n` + sh.fragmentShader.replace("#include <opaque_fragment>", `
      float cdepth = uCLevel - vCW.y;
      if (cdepth > 0.0) {
        vec2 cp = (vCW.xz + normalize(uCSun).xz * cdepth * 0.6) * uCScale;
        float cc = kcaustic(cp, uCT) * smoothstep(0.0, 0.12, cdepth) * (1.0 - smoothstep(1.2, 3.0, cdepth));
        outgoingLight += reflectedLight.directDiffuse * cc * uCStr;
        outgoingLight *= exp(-uAbs * cdepth);
      }
      #include <opaque_fragment>`);
  };
  const key = material.customProgramCacheKey ? material.customProgramCacheKey.bind(material) : () => "";
  material.customProgramCacheKey = () => key() + "|caustics";
  material.userData.caustics = u;
  return u;
}

/* wind sway for plants (reeds, grass, leaves): bend grows with height², phase from the instance's position */
export function addSway(material, o = {}) {
  const u = { uST: o.time || { value: 0 }, uSAmp: { value: o.amp == null ? 0.06 : o.amp }, uSFreq: { value: o.freq || 1.3 } };
  const prev = material.onBeforeCompile;
  material.onBeforeCompile = (sh, r) => {
    if (prev) prev(sh, r);
    Object.assign(sh.uniforms, u);
    sh.vertexShader = "uniform float uST, uSAmp, uSFreq;\n" + sh.vertexShader.replace("#include <begin_vertex>", `#include <begin_vertex>
      float sph = 0.0;
      #ifdef USE_INSTANCING
        sph = instanceMatrix[3].x * 1.7 + instanceMatrix[3].z * 2.3;
      #endif
      float gust = 0.6 + 0.4 * sin(uST * 0.37 + sph * 0.21);
      transformed.x += sin(uST * uSFreq + sph + position.y * 2.0) * position.y * position.y * uSAmp * gust;
      transformed.z += cos(uST * uSFreq * 0.8 + sph * 1.3) * position.y * position.y * uSAmp * 0.45 * gust;`);
  };
  const key = material.customProgramCacheKey ? material.customProgramCacheKey.bind(material) : () => "";
  material.customProgramCacheKey = () => key() + "|sway";
  return u;
}

/* a koi: a lofted body (ellipse sections), caudal, dorsal and pectoral fins, a seeded scale-patterned skin
   (kohaku / sanke / showa / ogon) and a swim bend in the vertex shader that grows toward the tail. +X is the head. */
function koiSkin(seed, kind) {
  const r = rng(seed), N = 256;
  const base = kind === "ogon" ? [232, 190, 90] : [244, 238, 228], red = kind === "showa" ? [196, 52, 28] : [226, 86, 32], black = [24, 22, 24];
  const ox = r() * 50, oy = r() * 50;
  return noiseCanvas(N, (x, y) => {
    const u = x / N, v = y / N;                                       // u: tail 0 → head 1; v: around the body, 0.5 = belly
    const back = Math.max(0, -Math.cos(v * Math.PI * 2));
    const n = fbm(u * 5 + ox, v * 3 + oy, 3) + 0.25 * back;
    let c = base.slice();
    if (kind !== "ogon" && n > 0.08) c = red.slice();
    if ((kind === "sanke" || kind === "showa") && fbm(u * 9 + oy, v * 6 + ox, 2) > (kind === "showa" ? 0.12 : 0.32) && back > 0.2) c = black.slice();
    const belly = 1 - back; c = c.map((k, i) => k + (base[i] - k) * belly * 0.55);
    const scale = 0.9 + 0.1 * Math.abs(Math.sin(u * 140 + Math.sin(v * 60) * 2) * Math.sin(v * 90));
    return c.map((k) => Math.max(0, Math.min(255, k * scale)));
  });
}
export function makeKoi(o = {}) {
  const L = o.length || 0.62, seed = o.seed || 3, kind = o.kind || ["kohaku", "sanke", "showa", "ogon"][seed % 4];
  const rings = 28, segs = 18, pos = [], uv = [], idx = [];
  const prof = (s) => 0.105 * Math.pow(Math.max(0, Math.sin(Math.PI * Math.pow(s, 0.72))), 0.9) + 0.012;   // s: tail 0 → head 1
  for (let i = 0; i <= rings; i++) {
    const s = i / rings, x = (s - 0.55) * L, rr = prof(s) * L;
    for (let j = 0; j <= segs; j++) {
      const a = (j / segs) * Math.PI * 2;
      pos.push(x, Math.cos(a) * rr * 0.92, Math.sin(a) * rr * 0.62); uv.push(s, j / segs);
      if (i < rings && j < segs) { const k = i * (segs + 1) + j; idx.push(k, k + segs + 1, k + 1, k + 1, k + segs + 1, k + segs + 2); }
    }
  }
  const body = new THREE.BufferGeometry(); body.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); body.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); body.setIndex(idx);
  const fin = (pts) => { const g = new THREE.BufferGeometry(), p = [], u2 = [], [ax, ay, az] = pts[0];
    for (let k = 1; k < pts.length - 1; k++) { p.push(ax, ay, az, ...pts[k], ...pts[k + 1]); u2.push(0.02, 0.5, 0.0, 0.48, 0.0, 0.52); }
    g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(u2, 2)); return g; };
  const tx = -0.55 * L;
  const parts = [body.toNonIndexed(),
    fin([[tx + 0.02 * L, 0, 0], [tx - 0.10 * L, 0.11 * L, 0], [tx - 0.20 * L, 0.13 * L, 0], [tx - 0.15 * L, 0.02 * L, 0], [tx - 0.21 * L, -0.11 * L, 0], [tx - 0.10 * L, -0.09 * L, 0]]),
    fin([[0.12 * L, 0.06 * L, 0], [0.05 * L, 0.11 * L, 0], [-0.12 * L, 0.10 * L, 0], [-0.22 * L, 0.055 * L, 0]]),
    fin([[0.2 * L, -0.03 * L, 0.04 * L], [0.12 * L, -0.06 * L, 0.13 * L], [0.06 * L, -0.05 * L, 0.11 * L]]),
    fin([[0.2 * L, -0.03 * L, -0.04 * L], [0.12 * L, -0.06 * L, -0.13 * L], [0.06 * L, -0.05 * L, -0.11 * L]])];
  const geom = mergeGeometries(parts); geom.computeVertexNormals();
  const swim = { uPh: { value: 0 }, uAmpK: { value: o.amp == null ? 0.11 : o.amp }, uTurn: { value: 0 }, uLen: { value: L } };
  const mat = new THREE.MeshPhysicalMaterial({ map: koiSkin(seed, kind), roughness: 0.32, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.25, side: THREE.DoubleSide });
  mat.map.colorSpace = THREE.SRGBColorSpace;
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, swim);
    sh.vertexShader = `uniform float uPh, uAmpK, uTurn, uLen;
      float koiBendAt(float x){ float s = clamp((x / uLen) + 0.55, 0.0, 1.0); float tail = pow(1.0 - smoothstep(0.0, 0.85, s), 1.6);
        return (sin(uPh - x / uLen * 7.0) * uAmpK * tail + uTurn * tail * tail) * uLen; }
      ` + sh.vertexShader.replace("#include <beginnormal_vertex>", `#include <beginnormal_vertex>
      float bs = (koiBendAt(position.x + 0.004) - koiBendAt(position.x - 0.004)) / 0.008; objectNormal.x -= bs * objectNormal.z;`)
      .replace("#include <begin_vertex>", `#include <begin_vertex>
      transformed.z += koiBendAt(position.x);
      float finSpread = smoothstep(0.08, 0.2, abs(position.z) / uLen); transformed.y += sin(uPh * 0.6 + abs(position.z) * 30.0) * finSpread * 0.02 * uLen;`); };
  mat.customProgramCacheKey = () => "koi";
  const caus = addCaustics(mat, o.caustics || {});
  const mesh = new THREE.Mesh(geom, mat); mesh.castShadow = true;
  mesh.userData.swim = swim; mesh.userData.caustics = caus; mesh.userData.kind = kind;
  /* follow a path(t, out) in metres; heading from the tangent, the bend leans into turns */
  const tmp = new THREE.Vector3(), ahead = new THREE.Vector3(), behind = new THREE.Vector3();
  mesh.userData.set = (t, path, speedHz = 1.6) => {
    path(t, tmp); path(t + 0.08, ahead); path(t - 0.08, behind);
    mesh.position.copy(tmp);
    const dir = ahead.clone().sub(tmp), back = tmp.clone().sub(behind);
    mesh.rotation.set(0, Math.atan2(-dir.z, dir.x), Math.atan2(dir.y, Math.hypot(dir.x, dir.z)) * 0.8, "YZX");
    const turn = Math.atan2(back.x * dir.z - back.z * dir.x, back.x * dir.x + back.z * dir.z);
    swim.uTurn.value = THREE.MathUtils.clamp(-turn * 1.6, -0.5, 0.5);
    swim.uPh.value = t * Math.PI * 2 * speedHz;
  };
  return mesh;
}

/* petals: they fall with a seeded flutter, land on the water (each landing rings the water) and float, drifting and
   bobbing. Instanced; o.region [x0, x1, z0, z1]; o.times [t0, t1]; o.floating: share already on the water at t = 0. */
export function makePetals(o = {}) {
  const N = o.n || 120, r = rng(o.seed || 9), [x0, x1, z0, z1] = o.region || [-4, 4, -3, 3], [ta, tb] = o.times || [0, 8], lvl = o.level || 0;
  // a sakura petal: a long oval, widest past the middle, with only a shallow notch at the tip
  const shape = new THREE.Shape(); shape.moveTo(0, 0); shape.bezierCurveTo(0.010, 0.006, 0.016, 0.022, 0.012, 0.036); shape.bezierCurveTo(0.009, 0.042, 0.004, 0.043, 0, 0.040);
  shape.bezierCurveTo(-0.004, 0.043, -0.009, 0.042, -0.012, 0.036); shape.bezierCurveTo(-0.016, 0.022, -0.010, 0.006, 0, 0);
  const geo = new THREE.ShapeGeometry(shape, 6); const gp = geo.attributes.position;
  for (let i = 0; i < gp.count; i++) gp.setZ(i, -Math.pow(Math.abs(gp.getX(i)) * 40, 2) * 0.004);
  geo.computeVertexNormals(); geo.scale(o.size || 1.4, o.size || 1.4, o.size || 1.4);
  const mat = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: 0.55 });
  const mesh = new THREE.InstancedMesh(geo, mat, N); mesh.castShadow = true; mesh.frustumCulled = false;
  const P = [], c = new THREE.Color();
  for (let i = 0; i < N; i++) {
    const land = ta + r() * (tb - ta), fall = 2.4 + r() * 2.2;
    P.push({ x: x0 + r() * (x1 - x0), z: z0 + r() * (z1 - z0), land, start: land - fall, h: 1.6 + r() * 2.4, drift: [(r() - 0.5) * 0.9, (r() - 0.5) * 0.5], ph: r() * 6.28, spin: 1.5 + r() * 3, pre: !!(o.floating && r() < o.floating) });
    c.setHSL(0.96 + r() * 0.03, 0.35 + r() * 0.3, 0.84 + r() * 0.09); mesh.setColorAt(i, c);
  }
  mesh.instanceColor.needsUpdate = true;
  if (o.water) P.forEach((p) => { if (!p.pre) o.water.userData.ripple(p.x, p.z, p.land, 0.0016 + 0.0008 * Math.sin(p.ph)); });
  const tmp = new THREE.Object3D();
  mesh.userData.set = (t) => {
    for (let i = 0; i < N; i++) {
      const p = P[i];
      if (p.pre || t >= p.land) {
        const a = p.pre ? t + p.ph * 3 : t - p.land;
        tmp.position.set(p.x + p.drift[0] * 0.08 * a + Math.sin(a * 0.4 + p.ph) * 0.03, lvl + 0.004 + Math.sin(a * 1.7 + p.ph) * 0.003, p.z + p.drift[1] * 0.08 * a);
        tmp.rotation.set(-Math.PI / 2 + Math.sin(a * 1.3 + p.ph) * 0.06, p.ph + a * 0.05, Math.sin(a * 0.9) * 0.05); tmp.scale.setScalar(1);
      } else if (t >= p.start) {
        const u = (t - p.start) / (p.land - p.start), e = 1 - Math.pow(1 - u, 1.15);
        tmp.position.set(p.x - p.drift[0] * (1 - u) * 1.2 + Math.sin(t * p.spin + p.ph) * 0.12 * (1 - u), lvl + p.h * (1 - e), p.z - p.drift[1] * (1 - u) * 1.2 + Math.cos(t * p.spin * 0.7 + p.ph) * 0.08 * (1 - u));
        tmp.rotation.set(Math.sin(t * p.spin + p.ph) * 1.2 - Math.PI / 2 * u, p.ph + t * 0.8, Math.cos(t * p.spin * 1.3 + p.ph) * 0.9 * (1 - u)); tmp.scale.setScalar(1);
      } else { tmp.position.set(0, -50, 0); tmp.scale.setScalar(0.0001); }
      tmp.updateMatrix(); mesh.setMatrixAt(i, tmp.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
  };
  return mesh;
}

/* pebbles and stones: instanced, deformed icosahedra; accept(x, z) places them; caustics + absorption included */
export function makePebbles(o = {}) {
  const N = o.n || 2400, r = rng(o.seed || 31), [x0, x1, z0, z1] = o.region;
  let g = new THREE.IcosahedronGeometry(1, 3); g.deleteAttribute("normal"); g.deleteAttribute("uv"); g = mergeVertices(g);      // shared vertices → smooth, water-worn stones
  const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) { const v = new THREE.Vector3().fromBufferAttribute(p, i); const k = 0.82 + 0.36 * (0.5 + 0.5 * fbm(v.x * 1.3 + 3, v.z * 1.3 + v.y * 0.7, 2)); p.setXYZ(i, v.x * k, v.y * k * (o.flat || 0.5), v.z * k); }
  g.computeVertexNormals();
  const speck = noiseCanvas(256, (x, y) => { const v = 0.78 + 0.22 * (0.5 + 0.5 * fbm(x / 9, y / 9, 3)) - (fbm(x / 2.2 + 7, y / 2.2, 1) > 0.42 ? 0.18 : 0); const k = Math.round(255 * v); return [k, k, k]; });
  const mat = new THREE.MeshStandardMaterial({ roughness: 0.55, metalness: 0, map: speck });
  const caus = addCaustics(mat, o.caustics || {});
  const mesh = new THREE.InstancedMesh(g, mat, N), tmp = new THREE.Object3D(), c = new THREE.Color(); let n = 0, tries = 0;
  while (n < N && tries < N * 20) { tries++;
    const x = x0 + r() * (x1 - x0), z = z0 + r() * (z1 - z0); if (!o.accept(x, z)) continue;
    if (o.clump && r() > 0.25 + 0.75 * clamp01(0.5 + 1.6 * fbm(x * o.clump + 13, z * o.clump + 5, 2))) continue;   // stones gather in drifts
    const s = (o.size || 0.06) * (0.4 + Math.pow(r(), 2.2) * 2.4);
    tmp.position.set(x, o.height(x, z) + s * 0.15, z); tmp.rotation.set(r() * 0.4, r() * 6.28, r() * 0.4); tmp.scale.set(s * (0.8 + r() * 0.5), s, s * (0.8 + r() * 0.5)); tmp.updateMatrix();
    mesh.setMatrixAt(n, tmp.matrix); const kind = r(); if (kind < 0.45) c.setHSL(0.08 + r() * 0.04, 0.05 + r() * 0.08, 0.3 + r() * 0.25); else if (kind < 0.75) c.setHSL(0.09 + r() * 0.03, 0.25 + r() * 0.2, 0.32 + r() * 0.2); else if (kind < 0.92) c.setHSL(0.05 + r() * 0.03, 0.3 + r() * 0.2, 0.18 + r() * 0.12); else c.setHSL(0.1, 0.05, 0.62 + r() * 0.2); mesh.setColorAt(n, c); n++; }
  mesh.count = n; mesh.instanceMatrix.needsUpdate = true; mesh.instanceColor.needsUpdate = true; mesh.castShadow = true; mesh.receiveShadow = true;
  mesh.userData.caustics = caus;
  return mesh;
}

/* reeds / grass blades: instanced tapered strips with wind sway (addSway) */
export function makeBlades(o = {}) {
  const N = o.n || 1500, r = rng(o.seed || 17), [x0, x1, z0, z1] = o.region, tall = o.tall || 0.9;
  const g = new THREE.PlaneGeometry(o.width || 0.02, tall, 1, 6); g.translate(0, tall / 2, 0);
  const gp = g.attributes.position; for (let i = 0; i < gp.count; i++) { const y = gp.getY(i) / tall; gp.setX(i, gp.getX(i) * (1 - y * 0.92)); gp.setZ(i, y * y * tall * 0.18); }
  g.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, roughness: 0.7 });
  const sway = addSway(mat, { amp: o.amp == null ? 0.06 : o.amp, freq: o.freq || 1.4, time: o.time });
  const mesh = new THREE.InstancedMesh(g, mat, N), tmp = new THREE.Object3D(), c = new THREE.Color(); let n = 0, tries = 0;
  while (n < N && tries < N * 20) { tries++;
    const x = x0 + r() * (x1 - x0), z = z0 + r() * (z1 - z0); if (!o.accept(x, z)) continue;
    tmp.position.set(x, o.height(x, z) - 0.02, z); tmp.rotation.set((r() - 0.5) * 0.25, r() * 6.28, (r() - 0.5) * 0.25); tmp.scale.set(1, 0.55 + r() * 0.9, 1); tmp.updateMatrix();
    mesh.setMatrixAt(n, tmp.matrix); c.setHSL((o.hue == null ? 0.24 : o.hue) + (r() - 0.5) * 0.05, 0.35 + r() * 0.25, 0.2 + r() * 0.18); mesh.setColorAt(n, c); n++; }
  mesh.count = n; mesh.instanceMatrix.needsUpdate = true; mesh.instanceColor.needsUpdate = true; mesh.castShadow = true; mesh.receiveShadow = true;
  mesh.userData.sway = sway;
  return mesh;
}

/* dappled light (komorebi): a leafy cookie projected by a SpotLight standing in for the sun through a canopy.
   The canopy texture is generated once at 4× the projected area and slides a little with t, so leaves seem to move. */
export function makeDappledSun(scene, o = {}) {
  const N = o.texSize || 512, seed = o.seed || 4;
  const tex = noiseCanvas(N, (x, y) => {
    const u = x / N, v = y / N;
    const leaf = fbm(u * 14 + seed, v * 14, 4) + 0.35 * fbm(u * 38 + 7, v * 38 + seed, 2);
    const gap = smooth(-0.02 + (o.density || 0) * 0.3, 0.16, leaf);
    const k = Math.round(255 * Math.max(o.floor == null ? 0.16 : o.floor, gap)); return [k, k, k];
  });
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(0.5, 0.5);
  const light = new THREE.SpotLight(o.color || 0xffd9a6, o.intensity == null ? 4 : o.intensity, 0, o.angle || 0.24, 0.35, 0);   // no falloff: intensity reads like a sun's (≈3–5)
  light.castShadow = true; light.shadow.mapSize.set(o.shadowSize || 4096, o.shadowSize || 4096); light.shadow.bias = -0.0002; light.shadow.normalBias = 0.02;
  light.shadow.camera.near = 10; light.shadow.camera.far = 200;
  light.map = tex;
  scene.add(light, light.target);
  const cam = new THREE.PerspectiveCamera(), m = new THREE.Matrix4();
  return { light, texture: tex,
    place(sunDir, target = new THREE.Vector3(), dist = 60) { light.position.copy(sunDir).normalize().multiplyScalar(dist).add(target); light.target.position.copy(target); light.target.updateMatrixWorld(); },
    setDapple(t) { tex.offset.set(0.25 + Math.sin(t * 0.21) * 0.012 + t * 0.002, 0.25 + Math.cos(t * 0.17) * 0.01); },
    matrix() { light.updateMatrixWorld(); cam.position.copy(light.position); cam.lookAt(light.target.position); cam.fov = THREE.MathUtils.radToDeg(light.angle) * 2; cam.aspect = 1; cam.near = 1; cam.far = 400;
      cam.updateMatrixWorld(); cam.updateProjectionMatrix(); return m.multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse); } };
}

/* a camera through keys with centripetal Catmull-Rom position and look target: moves never stop dead between keys.
   keys: [t, x, y, z, lx, ly, lz] */
export function cameraPath(keys) {
  const P = new THREE.CatmullRomCurve3(keys.map((k) => new THREE.Vector3(k[1], k[2], k[3])), false, "centripetal");
  const Lc = new THREE.CatmullRomCurve3(keys.map((k) => new THREE.Vector3(k[4], k[5], k[6])), false, "centripetal");
  const T = keys.map((k) => k[0]), n = keys.length - 1;
  const ease = (u) => u * u * (3 - 2 * u) * 0.35 + u * 0.65;
  return (t) => { let i = 0; while (i < n - 1 && t > T[i + 1]) i++;
    const u = clamp01((t - T[i]) / Math.max(1e-3, T[i + 1] - T[i])), s = clamp01((i + ease(u)) / n);
    return [P.getPoint(s), Lc.getPoint(s)]; };
}

/* ═════════ v3.1: the sound drives the world, real motion drives bodies, ready-made models ═════════ */

/* the ground is the sound: a spectrogram (motion.py channels → spectrum_height.png, time across, log-frequency up) displaced
   into a canyon and coloured with a magma ramp; bass becomes a glowing river along the middle, harmonics rise into ridges.
   set(t, tape) scrolls it with the tape clock, so it freezes when the track stops. heightTex: a THREE.Texture. */
export function makeSpectrumGround(heightTex, o = {}) {
  const W = o.width || 60, D = o.depth || 30, seconds = o.seconds || 10;
  const geo = new THREE.PlaneGeometry(W, D, o.segX || 480, o.segZ || 240); geo.rotateX(-Math.PI / 2);
  heightTex.wrapS = THREE.ClampToEdgeWrapping; heightTex.wrapT = THREE.ClampToEdgeWrapping; heightTex.minFilter = THREE.LinearFilter;
  const u = { uH: { value: heightTex }, uScroll: { value: 0 }, uSpan: { value: o.window || 4 }, uSec: { value: seconds }, uAmp: { value: o.amp || 6 },
              uT: { value: 0 }, uKick: { value: 0 }, uGlow: { value: o.glow == null ? 1.2 : o.glow }, uLava: { value: o.lava == null ? 0.62 : o.lava },
              uLight: { value: (o.light || new THREE.Vector3(1, 0.35, 0.2)).clone().normalize() }, uLightCol: { value: new THREE.Color(o.lightColor || 0xff9a6a) },
              uFillCol: { value: new THREE.Color(o.fillColor || 0x2a1a4a) }, uRock: { value: new THREE.Color(o.rock || 0x1a1216) },
              uHead: { value: o.head == null ? 0 : o.head }, uHeadAmt: { value: 0 }, uHalf: { value: o.half || D / 2 } };
  const mat = new THREE.ShaderMaterial({ uniforms: THREE.UniformsUtils.merge([THREE.UniformsLib.fog, {}]), fog: o.fog !== false,
    vertexShader: `#include <fog_pars_vertex>
      uniform sampler2D uH; uniform float uScroll, uSpan, uSec, uAmp, uKick, uHalf; varying float vH; varying vec2 vUv; varying float vBass; varying vec3 vW; varying float vLX; varying float vFy;
      // the canyon: low frequencies in the middle, highs on the walls; past uHalf the top wall carries on to the plane's edge
      float fyOf(vec3 p){ return min(1.0, abs(p.z) / uHalf); }
      float hAt(vec2 uv, float fy){ float tx = clamp((uScroll + (uv.x - 0.5) * uSpan) / uSec, 0.0, 1.0);
        return texture2D(uH, vec2(tx, 1.0 - fy)).r; }
      void main(){ vUv = uv; float fy = fyOf(position); float h = hAt(uv, fy); vFy = fy;
        vec3 p = position; p.y += (h * h) * uAmp * (0.25 + fy * 1.4) + fy * fy * uAmp * 0.6 - (1.0 - fy) * (1.0 - fy) * uAmp * 0.25 * (1.0 + uKick * 0.6);
        vH = h; vBass = (1.0 - smoothstep(0.0, 0.18, fy)) * h; vLX = p.x;
        vec4 wp = modelMatrix * vec4(p, 1.0); vW = wp.xyz;
        vec4 mvPosition = viewMatrix * wp; gl_Position = projectionMatrix * mvPosition;
        #include <fog_vertex>
      }`,
    fragmentShader: `#include <fog_pars_fragment>
      uniform float uGlow, uKick, uLava, uHead, uHeadAmt; uniform vec3 uLight, uLightCol, uFillCol, uRock;
      varying float vH; varying vec2 vUv; varying float vBass; varying vec3 vW; varying float vLX; varying float vFy;
      vec3 magma(float x){ x = clamp(x, 0.0, 1.0);
        vec3 a = mix(vec3(0.0, 0.0, 0.016), vec3(0.157, 0.043, 0.33), smoothstep(0.0, 0.2, x));
        a = mix(a, vec3(0.47, 0.11, 0.43), smoothstep(0.2, 0.4, x)); a = mix(a, vec3(0.75, 0.23, 0.46), smoothstep(0.4, 0.6, x));
        a = mix(a, vec3(0.93, 0.41, 0.35), smoothstep(0.6, 0.75, x)); a = mix(a, vec3(0.98, 0.65, 0.29), smoothstep(0.75, 0.88, x));
        a = mix(a, vec3(0.99, 0.99, 0.75), smoothstep(0.88, 1.0, x)); return pow(a, vec3(2.2)); }   // the ramp is sRGB; light is linear
      void main(){
        vec3 n = normalize(cross(dFdx(vW), dFdy(vW))); if (n.y < 0.0) n = -n;   // faceted normal from the displaced surface
        vec3 v = normalize(cameraPosition - vW);
        float dif = max(dot(n, uLight), 0.0), up = 0.5 + 0.5 * n.y, rim = pow(1.0 - max(dot(n, v), 0.0), 4.0);
        vec3 rock = uRock * (uLightCol * dif * 1.6 + uFillCol * up * 1.2) + uLightCol * rim * 0.06 * (0.4 + vH);
        float fyy = vFy;
        float lava = smoothstep(uLava, 1.0, vH) * mix(1.0, 0.2, smoothstep(0.4, 0.85, fyy));   // the loudest cells melt; the high walls stay rock
        vec3 c = mix(rock, magma(0.35 + 0.65 * vH) * uGlow * 1.25, lava);
        c += magma(0.72 + 0.28 * vBass) * vBass * vBass * (1.4 + 2.2 * uKick);   // the bass river, punched by kicks
        float head = exp(-pow((vLX - uHead) / 0.07, 2.0)) * uHeadAmt;             // the playhead traces the sound's cross-section
        c += vec3(1.0, 0.62, 0.32) * head * (0.4 + 0.9 * vH) * (1.0 - smoothstep(0.45, 0.85, vFy));   // on the floor and lower slopes only
        gl_FragColor = vec4(c, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
        #include <fog_fragment>
      }` });
  Object.assign(mat.uniforms, u);
  const mesh = new THREE.Mesh(geo, mat); mesh.frustumCulled = false;
  mesh.userData.set = (t, tape, kick = 0, head = 0) => { u.uT.value = t; u.uScroll.value = tape == null ? t : tape; u.uKick.value = kick; u.uHeadAmt.value = head; };
  mesh.userData.uniforms = u;
  return mesh;
}

/* the spectrogram re-sampled onto the tape clock: column j is tape position τ_j, read from the wall-clock column where
   tape(t) = τ_j. Scroll the ground by tape(t) and the line under the camera is always what is heard, while the land still
   slows, freezes and spins up with the track. img: a loaded Image of spectrum_height.png; ch: channels JSON.
   Returns { texture, seconds } — pass seconds as the ground's `seconds`. */
export function spectrumOnTape(img, ch, o = {}) {
  const fps = ch.fps || 30, tape = ch.tape || [], n = tape.length, W0 = img.width, H0 = img.height;
  const src = document.createElement("canvas"); src.width = W0; src.height = H0;
  const sx = src.getContext("2d"); sx.drawImage(img, 0, 0); const S = sx.getImageData(0, 0, W0, H0).data;
  const end = n ? tape[n - 1] : W0 / fps, W = o.width || Math.max(64, Math.round(end * fps * 2));
  const dst = document.createElement("canvas"); dst.width = W; dst.height = H0;
  const dx = dst.getContext("2d"), D = dx.createImageData(W, H0);
  let k = 0;
  for (let j = 0; j < W; j++) {
    const tau = (j / (W - 1)) * end;
    while (k < n - 2 && tape[k + 1] < tau) k++;
    const a = tape[k], b = tape[Math.min(n - 1, k + 1)], f = b > a ? clamp01((tau - a) / (b - a)) : 0;
    const col = Math.min(W0 - 1, ((k + f) / fps) * (W0 / Math.max(1e-6, n / fps)));
    const c0 = Math.floor(col), c1 = Math.min(W0 - 1, c0 + 1), w = col - c0;
    for (let y = 0; y < H0; y++) { const v = S[(y * W0 + c0) * 4] * (1 - w) + S[(y * W0 + c1) * 4] * w, q = (y * W + j) * 4;
      D.data[q] = D.data[q + 1] = D.data[q + 2] = v; D.data[q + 3] = 255; }
  }
  dx.putImageData(D, 0, 0);
  const texture = new THREE.CanvasTexture(dst); texture.colorSpace = THREE.NoColorSpace;
  return { texture, seconds: end };
}

/* sparks thrown by events and moving on the tape clock (they hang in the air when the track stops).
   events: [{ t, x, y, z }] in wall seconds; tape(t) maps wall → tape seconds; drift: the ground's units per tape second. */
export function makeSparks(events, o = {}) {
  const per = o.per || 60, N = events.length * per, r = rng(o.seed || 5);
  const pos = new Float32Array(N * 3), alpha = new Float32Array(N), vel = new Float32Array(N * 3), life = new Float32Array(N), size = new Float32Array(N);
  for (let i = 0; i < N; i++) { const a = r() * Math.PI * 2, up = 0.4 + r() * 0.6, sp = (o.speed || 5) * (0.35 + r() * 0.9);
    vel[i * 3] = Math.cos(a) * sp * 0.55; vel[i * 3 + 1] = up * sp; vel[i * 3 + 2] = Math.sin(a) * sp * 0.55; life[i] = 0.5 + r() * 1.1; size[i] = 0.5 + r(); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("alpha", new THREE.BufferAttribute(alpha, 1)); geo.setAttribute("size", new THREE.BufferAttribute(size, 1));
  const mat = new THREE.ShaderMaterial({ uniforms: { uTex: { value: spriteTex("soft") }, uCol: { value: new THREE.Color(o.color || 0xffa040) }, uSize: { value: o.size || 9 } },
    vertexShader: `attribute float alpha; attribute float size; uniform float uSize; varying float vA;
      void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_Position = projectionMatrix * mv; vA = alpha;
        gl_PointSize = uSize * size * 10.0 / max(0.5, -mv.z); }`,
    fragmentShader: `uniform sampler2D uTex; uniform vec3 uCol; varying float vA;
      void main(){ vec4 s = texture2D(uTex, gl_PointCoord); gl_FragColor = vec4(uCol * (1.0 + 2.5 * vA), s.a * vA); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  const pts = new THREE.Points(geo, mat); pts.frustumCulled = false;
  const g = o.gravity == null ? 6 : o.gravity, drift = o.drift || 0;
  pts.userData.set = (t, tape) => {
    const now = tape(t);
    events.forEach((e, ei) => { const age = now - tape(e.t), born = t >= e.t;
      for (let q = 0; q < per; q++) { const i = ei * per + q, u = born ? age : -1;
        if (u < 0 || u > life[i]) { alpha[i] = 0; pos[i * 3 + 1] = -999; continue; }
        pos[i * 3] = e.x + vel[i * 3] * u - drift * u; pos[i * 3 + 1] = e.y + vel[i * 3 + 1] * u - 0.5 * g * u * u; pos[i * 3 + 2] = e.z + vel[i * 3 + 2] * u;
        const k = u / life[i]; alpha[i] = (1 - k) * (1 - k) * Math.min(1, u * 30); } });
    geo.attributes.position.needsUpdate = true; geo.attributes.alpha.needsUpdate = true;
  };
  return pts;
}

/* glitch post keyed to the analysis: chroma split, slice displacement, a negative tear, a freeze monochrome and a tape-speed warp. One pass,
   deterministic (the slices come from a hash of the frame index, not a clock). glitch.set({ chroma, slice, negative, mono, warp, frame }) */
export function makeGlitchPass(o = {}) {
  const pass = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uChroma: { value: 0 }, uSlice: { value: 0 }, uNegative: { value: 0 }, uMono: { value: 0 }, uWarp: { value: 0 }, uFrame: { value: 0 } },
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform sampler2D tDiffuse; uniform float uChroma, uSlice, uNegative, uMono, uWarp, uFrame; varying vec2 vUv;
      float h1(float x){ return fract(sin(x * 91.345 + uFrame * 7.13) * 43758.5453); }
      void main(){ vec2 uv = vUv;
        float band = floor(uv.y * 24.0); float r = h1(band);
        uv.x += (r > 0.72 ? (h1(band + 3.0) - 0.5) * 0.12 * uSlice : 0.0);            // slice displacement on chosen bands
        uv.y += sin(uv.x * 6.2832 + uFrame * 0.3) * 0.01 * uWarp;                      // a breathing tape warp
        vec2 d = (uv - 0.5) * 0.012 * uChroma;
        vec3 c = vec3(texture2D(tDiffuse, uv + d).r, texture2D(tDiffuse, uv).g, texture2D(tDiffuse, uv - d).b);
        float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
        c = mix(c, pow(vec3(l) * 1.35, vec3(1.25)) * vec3(0.78, 0.88, 1.0), uMono);            // freeze: cold silver monochrome (time stopped)
        c = mix(c, (vec3(1.0) - c) * 0.8, uNegative);                                           // negative tear: keep it to a few frames
        gl_FragColor = vec4(c, 1.0); }` });
  pass.userData = { set: (g) => { const u = pass.uniforms; for (const k in g) { const key = "u" + k[0].toUpperCase() + k.slice(1); if (u[key]) u[key].value = g[k]; } } };
  return pass;
}

/* a body made of particles that moves exactly like a real performer: motion.py mocap VIDEO → JSON of per-frame points (the
   measured silhouette), drawn as glowing sprites on a plane with a little depth, plus tracer ghosts of earlier frames. */
export function makeParticleBody(data, o = {}) {
  const fps = data.fps || 30, frames = data.frames, N = data.points || frames[0].length / 2, ghosts = o.ghosts == null ? 3 : o.ghosts;
  const total = N * (ghosts + 1), pos = new Float32Array(total * 3), alpha = new Float32Array(total), seed = new Float32Array(total);
  const r = rng(o.seed || 21); for (let i = 0; i < total; i++) seed[i] = r();
  const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos, 3)); geo.setAttribute("alpha", new THREE.BufferAttribute(alpha, 1)); geo.setAttribute("seed", new THREE.BufferAttribute(seed, 1));
  const mat = new THREE.ShaderMaterial({ uniforms: { uTex: { value: spriteTex("soft") }, uCol: { value: new THREE.Color(o.color || 0xffb36b) }, uSize: { value: o.size || 26 }, uPulse: { value: 0 } },
    vertexShader: `attribute float alpha; attribute float seed; uniform float uSize, uPulse; varying float vA;
      void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_Position = projectionMatrix * mv; vA = alpha;
        gl_PointSize = uSize * (0.6 + 0.8 * seed) * (1.0 + uPulse * 0.6) * 10.0 / max(1.0, -mv.z); }`,
    fragmentShader: `uniform sampler2D uTex; uniform vec3 uCol; varying float vA; void main(){ vec4 s = texture2D(uTex, gl_PointCoord); gl_FragColor = vec4(uCol * 1.6, s.a * vA); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  const pts = new THREE.Points(geo, mat); pts.frustumCulled = false;
  const H = o.height || 4, aspect = data.aspect || 1, sc = data.scale || 1;
  const fill = (k, f, a) => { const P = frames[Math.max(0, Math.min(frames.length - 1, f))]; for (let i = 0; i < N; i++) { const j = (k * N + i);
      const x = (P[i * 2] / sc - 0.5) * H * aspect, y = (1 - P[i * 2 + 1] / sc) * H, z = (seed[j] - 0.5) * (o.depth || 0.35);
      pos[j * 3] = x; pos[j * 3 + 1] = y; pos[j * 3 + 2] = z; alpha[j] = P[i * 2] < 0 ? 0 : a; } };
  pts.userData.set = (t, pulse = 0) => {
    const f = Math.floor(t * fps);
    for (let k = 0; k <= ghosts; k++) fill(k, f - k * (o.ghostStep || 3), k === 0 ? 0.9 : 0.35 / k);
    geo.attributes.position.needsUpdate = true; geo.attributes.alpha.needsUpdate = true; mat.uniforms.uPulse.value = pulse;
  };
  return pts;
}

/* ready-made or Blender-made models: a GLB (bundled as a data URL by motion.py bundle, so file:// renders work) with its
   skeletal or object animation sought to an absolute time — mixer.setTime(t) — so any frame renders in any order. */
export async function loadModel(url, o = {}) {
  const { GLTFLoader } = await import("three/examples/jsm/loaders/GLTFLoader.js");
  const gltf = await new GLTFLoader().loadAsync(url);
  const root = gltf.scene;
  root.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; if (o.caustics) addCaustics(m.material, o.caustics); } });
  const mixer = gltf.animations.length ? new THREE.AnimationMixer(root) : null;
  if (mixer) gltf.animations.forEach((c, i) => { if (o.clip == null || o.clip === c.name || o.clip === i) mixer.clipAction(c).play(); });
  root.userData.clips = gltf.animations.map((c) => c.name);
  root.userData.set = (t) => { if (mixer) mixer.setTime((t + (o.offset || 0)) * (o.speed || 1)); };
  return root;
}

/* cloth, flags, signs and banners in the wind: a travelling wave anchored at one edge (local x = 0) */
export function addWave(material, o = {}) {
  const u = { uWT: o.time || { value: 0 }, uWAmp: { value: o.amp == null ? 0.08 : o.amp }, uWFreq: { value: o.freq || 2.4 }, uWLen: { value: o.wavelength || 0.9 }, uWSpan: { value: o.span || 1.0 } };
  const prev = material.onBeforeCompile;
  material.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r); Object.assign(sh.uniforms, u);
    sh.vertexShader = "uniform float uWT, uWAmp, uWFreq, uWLen, uWSpan;\n" + sh.vertexShader.replace("#include <begin_vertex>", `#include <begin_vertex>
      float wa = smoothstep(0.0, uWSpan, position.x);
      transformed.z += (sin(uWT * uWFreq - position.x / uWLen * 6.2832) + 0.35 * sin(uWT * uWFreq * 1.7 - position.x / uWLen * 11.0 + position.y * 3.0)) * uWAmp * wa;`); };
  const key = material.customProgramCacheKey ? material.customProgramCacheKey.bind(material) : () => "";
  material.customProgramCacheKey = () => key() + "|wave";
  return u;
}

/* ═════════ v3.2: light the way a cinematographer measures it (from KOSIF Lighting's calculator) ═════════ */

/* colour temperature → linear RGB (Tanner Helland's fit of the Planckian locus, 1000–40000 K) */
export function kelvin(K) {
  const t = Math.min(400, Math.max(10, K / 100));
  const r = t <= 66 ? 255 : 329.698727446 * Math.pow(t - 60, -0.1332047592);
  const g = t <= 66 ? 99.4708025861 * Math.log(t) - 161.1195681661 : 288.1221695283 * Math.pow(t - 60, -0.0755148492);
  const b = t >= 66 ? 255 : t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307;
  const c = (v) => Math.min(255, Math.max(0, v)) / 255;
  return new THREE.Color().setRGB(c(r), c(g), c(b), THREE.SRGBColorSpace);
}
/* mired shift between two colour temperatures and the gel that makes it (positive = warmer, CTO; negative = cooler, CTB) */
export function gel(fromK, toK) {
  const shift = 1e6 / toK - 1e6 / fromK;
  const G = [[-159, "Full CTB"], [-68, "1/2 CTB"], [-30, "1/4 CTB"], [-12, "1/8 CTB"], [0, "none"], [20, "1/8 CTO"], [42, "1/4 CTO"], [81, "1/2 CTO"], [159, "Full CTO"]];
  return { mired: Math.round(shift), gel: G.reduce((a, g) => (Math.abs(g[0] - shift) < Math.abs(a[0] - shift) ? g : a))[1] };
}
/* a three-point rig specified in stops, as on set: fill N stops under the key (2 stops = 4:1 → a 5:1 lighting ratio),
   rim M stops over or under it, each with its own Kelvin. Directions are azimuth/elevation in degrees around the subject.
   rig.set({ key, fillStops, rimStops }) re-balances it on any frame. */
export function lightRig(scene, o = {}) {
  const at = o.target || new THREE.Vector3(), key = o.key == null ? 3.0 : o.key;
  const dirFrom = (az, el, d) => new THREE.Vector3(Math.sin(az * Math.PI / 180) * Math.cos(el * Math.PI / 180), Math.sin(el * Math.PI / 180),
    Math.cos(az * Math.PI / 180) * Math.cos(el * Math.PI / 180)).multiplyScalar(d).add(at);
  const mk = (K, az, el, shadow) => { const l = new THREE.DirectionalLight(kelvin(K), 1); l.position.copy(dirFrom(az, el, o.distance || 10));
    l.target.position.copy(at); l.castShadow = !!shadow; scene.add(l, l.target); return l; };
  const keyL = mk(o.keyK || 5600, o.keyAz == null ? -40 : o.keyAz, o.keyEl == null ? 35 : o.keyEl, o.shadows !== false);
  const fillL = mk(o.fillK || 6500, o.fillAz == null ? 45 : o.fillAz, o.fillEl == null ? 10 : o.fillEl, false);
  const rimL = mk(o.rimK || 4300, o.rimAz == null ? 160 : o.rimAz, o.rimEl == null ? 40 : o.rimEl, false);
  const rig = { key: keyL, fill: fillL, rim: rimL };
  rig.set = (p = {}) => { const k = p.key == null ? key : p.key;
    keyL.intensity = k; fillL.intensity = k * Math.pow(2, -(p.fillStops == null ? (o.fillStops == null ? 2 : o.fillStops) : p.fillStops));
    rimL.intensity = k * Math.pow(2, p.rimStops == null ? (o.rimStops == null ? 0.5 : o.rimStops) : p.rimStops); return rig; };
  rig.ratio = () => (keyL.intensity + fillL.intensity) / fillL.intensity;   // the lighting ratio a meter would read
  return rig.set();
}
/* inverse square for point and spot lights: how many stops darker the background falls when it is d2 away and the subject d1 */
export const falloffStops = (d1, d2) => 2 * Math.log2(d2 / d1);

/* ═════════ v3.3: what the books teach, as code ═════════
   Sources: the Veo 3 prompt guide (shot vocabulary), the 360° character sheet (turnarounds), Joel Grimes' Photographer's
   Guide to Lighting (cross light, clamshell, edge lights; softness = source size relative to the subject), James Gurney's
   Color and Light (aerial perspective, warm light / cool shadow, gamut masks, night colour), Night Photography (long
   exposures, light trails, star-trail stacking), a colour-theory cheat sheet (harmonies, value). */

/* ── shot language: the words directors and video-model prompts use, as deterministic cameras ──
   shot(kind, o) → (t) => { pos, look, fov, roll, focus }.  o.subject (Vector3), o.size (subject height, m), o.t0/o.t1.
   kinds: establishing · wide · medium · closeup · extreme_closeup · low_angle · high_angle · birds_eye · dutch ·
   tracking · crane_up · crane_down · push_in · pull_back · orbit · arc · handheld · dolly_zoom · whip_pan · turntable */
export function shot(kind, o = {}) {
  const S = o.subject || new THREE.Vector3(0, 1, 0), size = o.size || 1.7, t0 = o.t0 || 0, t1 = o.t1 == null ? t0 + 4 : o.t1;
  const u = (t) => clamp01((t - t0) / Math.max(1e-3, t1 - t0)), ez = (x) => x * x * (3 - 2 * x);
  const fov0 = o.fov || 35, az0 = (o.azimuth == null ? -20 : o.azimuth) * Math.PI / 180;
  // the distance that frames the subject at a given fraction of the frame height with this fov
  const distFor = (frac, fov) => (size / frac) / (2 * Math.tan((fov * Math.PI / 180) / 2));
  const FR = { establishing: 0.06, wide: 0.25, medium: 0.55, closeup: 1.6, extreme_closeup: 4.0 };
  const around = (az, d, h) => new THREE.Vector3(S.x + Math.sin(az) * d, S.y + h, S.z + Math.cos(az) * d);
  const r = rng(o.seed || 7), ph = Array.from({ length: 6 }, () => r() * 100);
  const shake = (t, amp) => {                                  // handheld: three octaves of smooth noise around a ~1.3 Hz sway
    const n = (f, k) => Math.sin(t * f + ph[k]) * 0.6 + Math.sin(t * f * 2.17 + ph[k + 1]) * 0.3 + Math.sin(t * f * 4.9 + ph[k]) * 0.1;
    return [n(1.3, 0) * amp, n(1.1, 2) * amp * 0.7, n(0.9, 4) * amp * 0.25];
  };
  return (t) => {
    const k = u(t), e = ez(k); let fov = fov0, roll = 0, pos, look = S.clone();
    const d = o.distance || distFor(FR[kind] || FR[o.frame] || 0.55, fov);
    switch (kind) {
      case "low_angle": pos = around(az0, d, -size * 0.45); look = S.clone().add(new THREE.Vector3(0, size * 0.15, 0)); break;
      case "high_angle": pos = around(az0, d * 0.9, size * 1.6); break;
      case "birds_eye": pos = new THREE.Vector3(S.x + 0.01, S.y + d * 1.4, S.z); break;
      case "dutch": pos = around(az0, d, size * 0.05); roll = (o.roll || 12) * Math.PI / 180; break;
      case "tracking": { const v = o.velocity || new THREE.Vector3(1.2, 0, 0); const S2 = S.clone().addScaledVector(v, t - t0);
        pos = new THREE.Vector3(S2.x + Math.sin(az0) * d, S2.y + size * 0.1, S2.z + Math.cos(az0) * d); look = S2; break; }
      case "crane_up": pos = around(az0, d * (1 + 0.6 * e), size * (0.2 + 2.2 * e)); break;
      case "crane_down": pos = around(az0, d * (1.6 - 0.6 * e), size * (2.4 - 2.2 * e)); break;
      case "push_in": pos = around(az0, d * (1.8 - 0.8 * e), size * 0.1); break;             // slow push: tension rises
      case "pull_back": pos = around(az0, d * (1.0 + 1.6 * e), size * (0.1 + 0.4 * e)); break;  // reveal: context arrives
      case "orbit": pos = around(az0 + (o.degrees || 360) * Math.PI / 180 * k, d, size * 0.25); break;
      case "arc": pos = around(az0 + (o.degrees || 60) * Math.PI / 180 * e, d, size * 0.15); break;
      case "turntable": {                                        // the 360° character sheet: front, side, back, side holds
        const q = Math.min(3, Math.floor(k * 4)), w = k * 4 - q, hold = w < 0.7 ? 0 : ez((w - 0.7) / 0.3);
        pos = around(az0 + (q + hold) * Math.PI / 2, distFor(0.8, fov), 0); break; }
      case "dolly_zoom": {                                       // Vertigo: dolly while zooming so the subject keeps its size
        const dA = o.from || d, dB = o.to || d * 0.45, dd = dA + (dB - dA) * e, h = 2 * dA * Math.tan(fov0 * Math.PI / 360);
        pos = around(az0, dd, size * 0.05); fov = 2 * Math.atan(h / (2 * dd)) * 180 / Math.PI; break; }
      case "whip_pan": { const a = az0 + (o.degrees || 90) * Math.PI / 180 * ez(clamp01((k - 0.4) / 0.2));
        pos = around(az0, d, size * 0.1); look = new THREE.Vector3(pos.x - Math.sin(a) * d, S.y, pos.z - Math.cos(a) * d); break; }
      default: pos = around(az0, d, size * 0.1);
    }
    if (o.low && kind !== "low_angle") { pos.y -= size * 0.5; look.y += size * 0.12; }        // compound words: "low angle tracking"
    if (o.high && kind !== "high_angle") pos.y += size * 1.4;
    if (o.dutch && kind !== "dutch") roll += 10 * Math.PI / 180;
    if (kind === "handheld" || o.handheld) { const [sx, sy, sr] = shake(t, (o.shake || 1) * 0.012 * d);
      pos.x += sx; pos.y += sy; roll += sr * 0.08; }
    return { pos, look, fov, roll, focus: pos.distanceTo(look) };
  };
}
/* apply a shot sample to a camera (and to the depth-of-field pass, when given) */
export function applyShot(camera, s, post) {
  camera.position.copy(s.pos); camera.lookAt(s.look); if (s.roll) camera.rotateZ(s.roll);
  if (Math.abs(camera.fov - s.fov) > 1e-4) { camera.fov = s.fov; camera.updateProjectionMatrix(); }
  if (post && post.bokeh) post.bokeh.uniforms.focus.value = s.focus;
}
/* words → shot: "low angle tracking shot", "slow push-in", "crane up", "orbit", "dolly zoom" … (the Veo vocabulary) */
export const SHOT_WORDS = [["dolly zoom", "dolly_zoom"], ["vertigo", "dolly_zoom"], ["whip", "whip_pan"], ["turntable", "turntable"],
  ["360", "turntable"], ["orbit", "orbit"], ["arc shot", "arc"], ["crane up", "crane_up"], ["crane down", "crane_down"], ["push", "push_in"],
  ["pull back", "pull_back"], ["pull-back", "pull_back"], ["tracking", "tracking"], ["bird", "birds_eye"], ["top down", "birds_eye"],
  ["low angle", "low_angle"], ["high angle", "high_angle"], ["dutch", "dutch"], ["extreme close", "extreme_closeup"], ["close-up", "closeup"],
  ["close up", "closeup"], ["establishing", "establishing"], ["wide", "wide"], ["medium", "medium"], ["handheld", "handheld"]];
export function shotFromWords(text, o = {}) {
  const w = String(text).toLowerCase(), hit = SHOT_WORDS.find(([k]) => w.includes(k));
  return shot(hit ? hit[1] : "medium", Object.assign({ handheld: w.includes("handheld"), low: w.includes("low angle"), high: w.includes("high angle"),
    dutch: w.includes("dutch") }, o));
}

/* ── lighting the way portrait and film photographers do (Joel Grimes) ──
   "rembrandt" (cross light ~70–90° to the camera and high: the triangle on the shadow cheek) · "clamshell" (top-down over
   the camera + a bounce below) · "edgy" (two edge lights behind left and right + overhead) · "ultrasoft" (huge sources
   close) · "short" / "broad" · "sun" (a hard low sun + blue sky fill). Softness is the source's apparent size. */
export const softnessDeg = (sizeM, distM) => 2 * Math.atan(sizeM / (2 * distM)) * 180 / Math.PI;
export function lightPreset(scene, preset = "rembrandt", o = {}) {
  const P = {
    rembrandt: { keyAz: -75, keyEl: 40, fillStops: 2.5, rimStops: -0.5, rimAz: 150, size: 1.0 },
    clamshell: { keyAz: 0, keyEl: 55, fillAz: 0, fillEl: -25, fillStops: 1.0, rimStops: -1.5, size: 0.9 },
    edgy: { keyAz: 0, keyEl: 60, fillStops: 4, rimStops: 0.8, rimAz: 140, size: 0.6, twoEdges: true },
    ultrasoft: { keyAz: -35, keyEl: 30, fillStops: 0.8, rimStops: -0.3, size: 2.1 },
    short: { keyAz: 55, keyEl: 30, fillStops: 2.5, rimStops: 0, size: 0.9 },
    broad: { keyAz: -55, keyEl: 30, fillStops: 2.0, rimStops: -1, size: 0.9 },
    sun: { keyAz: -60, keyEl: 18, fillStops: 2.3, keyK: 3600, fillK: 9000, rimStops: -1, size: 0.05 },
  }[preset] || {};
  const c = Object.assign({}, P, o);
  const rig = lightRig(scene, c);
  if (c.twoEdges) { const l2 = rig.rim.clone(); l2.position.x = 2 * (c.target ? c.target.x : 0) - l2.position.x; scene.add(l2); rig.rim2 = l2; }
  const deg = softnessDeg(c.size || 0.9, c.distance || 2);
  rig.key.shadow.radius = Math.max(1, deg / 3); rig.key.shadow.blurSamples = 16;   // with VSM/PCFSoft shadows this reads as size
  rig.softness = deg;
  return rig;
}

/* ── colour, after Gurney ──
   aerialPerspective(): air scatters blue more than red, so far things lose contrast and drift toward the sky colour while
   distant lights warm. Replaces three's grey fog with three-channel extinction for every built-in material; call it before
   the first render. scatter = per-channel multipliers of the scene fog density. */
export function aerialPerspective(o = {}) {
  const k = (o.scatter || [0.62, 0.85, 1.25]).map((x) => Number(x).toFixed(4));
  THREE.ShaderChunk.fog_fragment = [
    "#ifdef USE_FOG",
    "  #ifdef FOG_EXP2",
    "    vec3 fogK = vec3(" + k.join(", ") + ") * fogDensity * vFogDepth;",
    "    vec3 fogFactor3 = 1.0 - exp(-fogK * fogK);",
    "  #else",
    "    vec3 fogFactor3 = clamp(vec3(smoothstep(fogNear, fogFar, vFogDepth)) * vec3(" + k.join(", ") + "), 0.0, 1.0);",
    "  #endif",
    "  gl_FragColor.rgb = mix(gl_FragColor.rgb, fogColor, fogFactor3);",
    "#endif", ""].join("\n");
}
/* the look pass: Gurney's gamut mask (hues outside a chosen wedge lose saturation, so the palette holds together), night
   vision (Purkinje: the darks go rod-grey and blue-shifted, reds sink first) and split toning (warm lights, cool shadows).
   look.userData.set({ gamut: [centreHueDeg, widthDeg, strength], night: 0–1, split: 0–1 }) */
export function makeLookPass(o = {}) {
  const pass = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uGamC: { value: 0 }, uGamW: { value: 360 }, uGamS: { value: 0 }, uNight: { value: 0 }, uSplit: { value: 0 },
                uWarm: { value: new THREE.Color(o.warm || 0xffc98a) }, uCool: { value: new THREE.Color(o.cool || 0x5a7fb8) } },
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
    fragmentShader: [
      "uniform sampler2D tDiffuse; uniform float uGamC, uGamW, uGamS, uNight, uSplit; uniform vec3 uWarm, uCool; varying vec2 vUv;",
      "vec3 rgb2hsv(vec3 c){ vec4 K = vec4(0., -1./3., 2./3., -1.); vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));",
      "  vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r)); float d = q.x - min(q.w, q.y); float e = 1e-10;",
      "  return vec3(abs(q.z + (q.w - q.y) / (6. * d + e)), d / (q.x + e), q.x); }",
      "vec3 hsv2rgb(vec3 c){ vec3 p = abs(fract(c.xxx + vec3(1., 2./3., 1./3.)) * 6. - 3.); return c.z * mix(vec3(1.), clamp(p - 1., 0., 1.), c.y); }",
      "void main(){ vec3 c = texture2D(tDiffuse, vUv).rgb;",
      "  if (uGamS > 0.0) { vec3 h = rgb2hsv(max(c, vec3(0.0))); float dh = abs(mod(h.x * 360.0 - uGamC + 540.0, 360.0) - 180.0);",
      "    float inside = 1.0 - smoothstep(uGamW * 0.5, uGamW * 0.5 + 25.0, dh); h.y *= mix(1.0, inside, uGamS); c = hsv2rgb(h); }",
      "  float l = dot(c, vec3(0.2126, 0.7152, 0.0722));",
      "  if (uSplit > 0.0) { vec3 w = uWarm / max(0.01, dot(uWarm, vec3(0.3333))), k = uCool / max(0.01, dot(uCool, vec3(0.3333)));",
      "    c *= mix(vec3(1.0), mix(k, w, smoothstep(0.1, 0.7, l)), uSplit * 0.35); }",
      "  if (uNight > 0.0) { float rod = dot(c, vec3(0.05, 0.55, 0.40));            // the scotopic response peaks in blue-green",
      "    float dark = 1.0 - smoothstep(0.02, 0.35, l);                              // only the dim parts switch to rods",
      "    c = mix(c, vec3(rod) * vec3(0.72, 0.86, 1.12), uNight * dark); c *= 1.0 - 0.25 * uNight * dark; }",
      "  gl_FragColor = vec4(c, 1.0); }"].join("\n") });
  pass.userData = { set: (g) => { const u = pass.uniforms;
    if (g.gamut) { u.uGamC.value = g.gamut[0]; u.uGamW.value = g.gamut[1]; u.uGamS.value = g.gamut[2] == null ? 1 : g.gamut[2]; }
    if (g.night != null) u.uNight.value = g.night;
    if (g.split != null) u.uSplit.value = g.split; } };
  pass.userData.set(o);
  return pass;
}
/* the colour-theory harmonies as hues (degrees) and THREE colours: complementary, analogous, triadic, split, tetradic */
export function harmony(scheme, baseHue, o = {}) {
  const off = { complementary: [0, 180], analogous: [-30, 0, 30], triadic: [0, 120, 240], split: [0, 150, 210], tetradic: [0, 60, 180, 240] }[scheme] || [0];
  const hues = off.map((d) => ((baseHue + d) % 360 + 360) % 360), L = o.light || [0.5];
  return { hues, colors: hues.map((h, i) => new THREE.Color().setHSL(h / 360, o.sat == null ? 0.6 : o.sat, L[i % L.length])) };
}

/* named light sources (Gurney: "each has a distinctive spectral power distribution"; Night Photography: white balance) */
export const LIGHT_SOURCES = {
  candle: 1850, firelight: 1900, sodium: 0xffa040, tungsten: 2700, halogen: 3200, sunrise: 3000, golden_hour: 3500,
  led_warm: 3000, led_neutral: 4000, mercury_vapor: 0xbff0dc, metal_halide: 4300, fluorescent: 0xe8f5e6, moonlight: 0x9fb4d9,
  daylight: 5600, overcast: 6500, open_shade: 8000, blue_sky: 11000, neon_red: 0xff2a3a, neon_blue: 0x3a7bff,
};
export function lightColor(name) {
  const v = LIGHT_SOURCES[name]; if (v == null) return new THREE.Color(0xffffff);
  return v > 40000 || v < 1000 ? new THREE.Color(v) : kelvin(v);
}
/* Gurney's reflected-light rule: in shadow, upfacing planes are cool (they see the sky) and downfacing planes are warm
   (they see the lit ground). A hemisphere light with a sky colour above and the bounce colour below does exactly that. */
export function skyBounce(scene, o = {}) {
  const h = new THREE.HemisphereLight(o.sky == null ? lightColor("blue_sky") : o.sky, o.ground == null ? 0xb07a4a : o.ground, o.intensity == null ? 0.6 : o.intensity);
  scene.add(h); return h;
}
/* reverse atmospheric perspective: looking toward a low sun through moist or dusty air the haze turns orange, away from it
   the haze stays blue. Call every frame: fogTowardSun(scene, camera, sunDir, cool, warm, amount) */
const _fv = new THREE.Vector3();
export function fogTowardSun(scene, camera, sunDir, cool, warm, amount = 1) {
  if (!scene.fog) return;
  camera.getWorldDirection(_fv);
  const k = Math.pow(Math.max(0, _fv.dot(sunDir.clone().normalize())), 3) * amount;
  scene.fog.color.copy(new THREE.Color(cool)).lerp(new THREE.Color(warm), k);
}

/* a shot list as a camera: [{ at: 0, shot: "establishing" }, { at: 2.5, shot: "low angle tracking" }, …] → (t) => sample.
   Hard cuts between entries (no crossfades); each entry's t0/t1 default to its own span, so moves start at the cut. */
export function sequence(list, o = {}) {
  const items = list.map((e, i) => { const t0 = e.at, t1 = i + 1 < list.length ? list[i + 1].at : (o.seconds || t0 + 4);
    const opt = Object.assign({}, o, e.options || {}, { t0, t1 });
    return { t0, cam: typeof e.shot === "function" ? e.shot : (SHOT_WORDS.some(([k, v]) => v === e.shot) || ["establishing", "wide", "medium", "closeup", "extreme_closeup"].includes(e.shot)
      ? shot(e.shot, opt) : shotFromWords(e.shot, opt)) }; });
  return (t) => { let i = 0; while (i < items.length - 1 && t >= items[i + 1].t0) i++; return items[i].cam(t); };
}

/* a light that moves d metres between two sub-samples of a lighten-stacked long exposure leaves a dotted trail unless the
   dots overlap. trailLength(speed) is that gap for the current render (0 outside a lighten stack); stretch the light along
   its motion by it — mesh.scale.z = 1 + trailLength(v) / (2 * radius) — and the trail is continuous. */
export function trailLength(speed) {
  if (typeof window === "undefined" || window.__stack !== "lighten") return 0;
  const k = Math.max(1, Math.floor(window.__blur || 1)), sh = window.__shutter == null ? 0.5 : window.__shutter, fps = window.__fps || 30;
  return Math.abs(speed) * (sh / fps) / k;
}
