/* مركب في البحر ليلاً — Night Boat. Five seconds, one shot.
   · A wooden fishing boat (felucca rig: a slanted yard with the sail furled) rides a slow swell under a low full moon.
   · Two light sources only, as at sea: the moon (4100K, cool, behind the boat: its glitter path runs to the camera and
     rims the hull) and a kerosene lantern (1900K, warm, flickering) whose pool lights the deck and streaks the water.
   · Far shore lights on the horizon give the scale; stars twinkle; a fish breaks the surface at 2.8 s (ring + sound).
   · Camera: a low, slow arc-and-push from the bow quarter (Veo words: "slow push-in, low angle, orbit 10°").
   Everything is a function of t: frames render in any order. Colours the review page can edit live in :root. */
const { THREE, fbm, perlin, smooth, ramp, clamp01, rng, spriteTex, normalFromHeight, makeRenderer, makeSea, makePost, makeFrameLoop,
        makeLookPass, kelvin, lightColor } = window.K3;

const SECONDS = 5.0;
const css = (name, fallback) => { const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim(); return v || fallback; };

/* ───────── the boat: a parametric hull (s along the length 0 stern → 1 bow, φ keel → sheer) ───────── */
const L = 7.2;                                                     // metres
const beam = (s) => 1.12 * Math.pow(Math.sin(Math.PI * clamp01(0.13 + 0.87 * s)), 0.62);
const sheer = (s) => 0.78 + 0.62 * Math.pow(s, 3.2) + 0.22 * Math.pow(1 - s, 5);
const keel = (s) => -0.62 * Math.pow(Math.sin(Math.PI * clamp01(0.04 + 0.96 * s)), 0.45);
const hullPoint = (s, phi, side) => {                               // side ±1: starboard/port
  const b = beam(s), y0 = keel(s), y1 = sheer(s);
  const x = side * b * (1 - Math.pow(1 - phi, 2.4));                // a round bilge, then near-vertical topsides
  return new THREE.Vector3((s - 0.5) * L, y0 + (y1 - y0) * phi, x);
};

function hullTexture() {
  const W = 1024, H = 256, c = document.createElement("canvas"); c.width = W; c.height = H;
  const g = c.getContext("2d"), r = rng(5);
  const bands = [[0, 0.30, "#4a1f17"], [0.30, 0.78, "#1d5f78"], [0.78, 0.84, "#e9e2cf"], [0.84, 0.92, "#b5432c"], [0.92, 1.0, "#c89a52"]];
  for (const [a, b, col] of bands) { g.fillStyle = col; g.fillRect(0, H * (1 - b), W, H * (b - a)); }
  for (let y = 0; y < H; y += 9) { g.fillStyle = "rgba(0,0,0,0.22)"; g.fillRect(0, y, W, 1.2); }              // plank seams
  const img = g.getImageData(0, 0, W, H);
  for (let i = 0; i < W * H; i++) { const x = i % W, y = (i / W) | 0;
    const n = fbm(x / 60, y / 5, 3) * 0.10 + (r() - 0.5) * 0.05 + (fbm(x / 9, y / 140 + 3, 2) < -0.35 ? -0.12 : 0);  // grain, chipped paint
    for (let k = 0; k < 3; k++) img.data[i * 4 + k] = Math.max(0, Math.min(255, img.data[i * 4 + k] * (1 + n))); }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

function makeBoat(lanternColor) {
  const boat = new THREE.Group();
  const NS = 72, NP = 16, pos = [], uv = [], idx = [];
  for (const side of [1, -1]) {
    const base = pos.length / 3;
    for (let i = 0; i <= NS; i++) for (let j = 0; j <= NP; j++) {
      const s = i / NS, phi = j / NP, p = hullPoint(s, phi, side); pos.push(p.x, p.y, p.z); uv.push(s, phi); }
    for (let i = 0; i < NS; i++) for (let j = 0; j < NP; j++) {
      const a = base + i * (NP + 1) + j, b = a + NP + 1;
      if (side > 0) idx.push(a, b, a + 1, b, b + 1, a + 1); else idx.push(a, a + 1, b, b, a + 1, b + 1); }
  }
  const hg = new THREE.BufferGeometry(); hg.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  hg.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); hg.setIndex(idx); hg.computeVertexNormals();
  const hullMat = new THREE.MeshStandardMaterial({ map: hullTexture(), roughness: 0.62, metalness: 0.0, side: THREE.DoubleSide });
  const hull = new THREE.Mesh(hg, hullMat); boat.add(hull);
  /* transom: the flat stern board */
  const tp = [new THREE.Vector2(0, keel(0))];
  for (let j = 0; j <= NP; j++) { const p = hullPoint(0, j / NP, 1); tp.push(new THREE.Vector2(p.z, p.y)); }
  for (let j = NP; j >= 0; j--) { const p = hullPoint(0, j / NP, -1); tp.push(new THREE.Vector2(p.z, p.y)); }
  const tr = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(tp)), new THREE.MeshStandardMaterial({ color: 0x1d5f78, roughness: 0.7, side: THREE.DoubleSide }));
  tr.rotation.y = Math.PI / 2; tr.position.x = -L / 2; boat.add(tr);
  /* gunwale rails and the floor boards */
  const wood = new THREE.MeshStandardMaterial({ color: 0x8a6136, roughness: 0.7 });
  for (const side of [1, -1]) {
    const pts = []; for (let i = 0; i <= 40; i++) pts.push(hullPoint(i / 40, 1, side).add(new THREE.Vector3(0, 0.03, 0)));
    boat.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 0.055, 6), wood)); }
  const fl = []; for (let i = 0; i <= 30; i++) { const s = 0.04 + 0.86 * i / 30; fl.push(new THREE.Vector2((s - 0.5) * L, beam(s) * 0.8)); }
  for (let i = 30; i >= 0; i--) { const s = 0.04 + 0.86 * i / 30; fl.push(new THREE.Vector2((s - 0.5) * L, -beam(s) * 0.8)); }
  const floor = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(fl)), new THREE.MeshStandardMaterial({ color: 0x5b4027, roughness: 0.85 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = 0.18; boat.add(floor);
  /* thwarts (bench boards) */
  for (const s of [0.3, 0.52, 0.72]) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.05, beam(s) * 1.9), wood); b.position.set((s - 0.5) * L, sheer(s) - 0.28, 0); boat.add(b); }
  /* mast, the long slanted yard with the sail furled along it (felucca), rigging */
  const mastX = (0.64 - 0.5) * L;
  const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.085, 5.2, 10), wood); mast.position.set(mastX, 2.75, 0); boat.add(mast);
  const yard = new THREE.Group(); yard.position.set(mastX + 0.05, 4.6, 0.12); yard.rotation.z = -1.02; boat.add(yard);
  const yl = 8.6;
  const spar = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, yl, 8), wood); yard.add(spar);
  const sailMat = new THREE.MeshStandardMaterial({ color: 0xd9cdb0, roughness: 0.95 });
  for (let k = 0; k < 9; k++) { const u = (k - 4) / 9; const roll = new THREE.Mesh(new THREE.CylinderGeometry(0.13 - Math.abs(u) * 0.14, 0.15 - Math.abs(u) * 0.14, yl / 9 + 0.05, 10), sailMat);
    roll.position.set(0.11, u * yl * 0.92, 0); roll.scale.set(1, 1, 1.25); yard.add(roll); }
  const ropeMat = new THREE.LineBasicMaterial({ color: 0x241d16, transparent: true, opacity: 0.85 });
  const line = (a, b) => boat.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([a, b]), ropeMat));
  const top = new THREE.Vector3(mastX, 5.3, 0);
  line(top, hullPoint(1.0, 1, 0)); line(top, hullPoint(0.5, 1, 1)); line(top, hullPoint(0.5, 1, -1)); line(top, hullPoint(0.08, 1, 1));
  /* the lantern: hung from the mast at head height; glass + flame + a real point light + a glow card */
  const lantern = new THREE.Group(); lantern.position.set(mastX - 0.22, 2.05, 0.0); boat.add(lantern);
  const frame = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.09, 0.26, 8, 1, true), new THREE.MeshStandardMaterial({ color: 0x1a1612, roughness: 0.5, metalness: 0.6, wireframe: true }));
  lantern.add(frame);
  const flameMat = new THREE.MeshBasicMaterial({ color: lanternColor.clone().multiplyScalar(14) });
  const flame = new THREE.Mesh(new THREE.SphereGeometry(0.045, 12, 10), flameMat); flame.scale.y = 1.6; lantern.add(flame);
  const glass = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), new THREE.MeshBasicMaterial({ color: lanternColor.clone().multiplyScalar(1.6), transparent: true, opacity: 0.45, depthWrite: false }));
  glass.scale.y = 1.4; lantern.add(glass);
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: spriteTex("soft"), color: lanternColor.clone().multiplyScalar(1.4), transparent: true, opacity: 0.55,
    blending: THREE.AdditiveBlending, depthWrite: false })); glow.scale.set(0.9, 0.9, 1); lantern.add(glow);
  const lamp = new THREE.PointLight(lanternColor, 9, 26, 1.6); lamp.castShadow = false; lantern.add(lamp);
  const hook = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.45, 4), ropeMat.clone()); hook.position.y = 0.33; lantern.add(hook);
  /* a fisherman sits at the stern, his back to us: a silhouette against the moonlit water */
  const cloth = new THREE.MeshStandardMaterial({ color: 0x2a2622, roughness: 0.95 });
  const man = new THREE.Group(); man.position.set((0.2 - 0.5) * L, sheer(0.2) - 0.25, -0.15); boat.add(man);
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.2, 0.42, 6, 12), cloth); torso.position.y = 0.42; torso.rotation.z = -0.18; torso.scale.set(1, 1, 1.15); man.add(torso);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 12), new THREE.MeshStandardMaterial({ color: 0x3a2a20, roughness: 0.8 })); head.position.set(0.06, 0.92, 0); man.add(head);
  const cap = new THREE.Mesh(new THREE.SphereGeometry(0.135, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xcfc6b2, roughness: 0.9 }));
  cap.position.copy(head.position).add(new THREE.Vector3(0, 0.03, 0)); man.add(cap);
  const legs = new THREE.Mesh(new THREE.CapsuleGeometry(0.1, 0.42, 4, 8), cloth); legs.position.set(0.28, 0.12, 0.1); legs.rotation.z = Math.PI / 2; man.add(legs);
  const legs2 = legs.clone(); legs2.position.z = -0.12; man.add(legs2);
  /* fishing line: a rod over the starboard side */
  const rodBase = man.position.clone().add(new THREE.Vector3(0.25, 0.55, 0.3)), rodTip = new THREE.Vector3((0.1 - 0.5) * L - 0.4, 2.0, 2.1);
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.02, rodBase.distanceTo(rodTip), 5), wood);
  rod.position.copy(rodBase).lerp(rodTip, 0.5);
  rod.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), rodTip.clone().sub(rodBase).normalize()); boat.add(rod);
  line(rodTip, new THREE.Vector3(rodTip.x - 0.3, -0.2, rodTip.z + 0.6));          // the line drops into the water
  return { boat, lantern, lamp, flameMat, glow, glass, rodTip };
}

/* ───────── sky dome, moon, stars, far shore ───────── */
function moonTexture() {
  const N = 512, c = document.createElement("canvas"); c.width = c.height = N; const g = c.getContext("2d"), img = g.createImageData(N, N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const u = (x + 0.5) / N * 2 - 1, v = (y + 0.5) / N * 2 - 1, r = Math.hypot(u, v), i = (y * N + x) * 4;
    if (r > 1) { img.data[i + 3] = 0; continue; }
    const limb = Math.pow(1 - r * r, 0.22);                                     // limb darkening
    const maria = smooth(0.05, 0.35, fbm(u * 2.2 + 4, v * 2.2 + 1, 5)) * 0.32;   // the dark seas
    const crater = Math.max(0, fbm(u * 14, v * 14, 3)) * 0.12;
    const l = limb * (1 - maria - crater * 0.6);
    img.data[i] = 255 * l; img.data[i + 1] = 250 * l; img.data[i + 2] = 236 * l; img.data[i + 3] = 255 * smooth(1, 0.985, r); }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

function build(canvas, W, H) {
  const renderer = makeRenderer(canvas, W, H, { exposure: 0.95, tone: "agx" });
  renderer.shadowMap.enabled = false;
  const scene = new THREE.Scene();
  const HORIZON = new THREE.Color(0x0d1626);
  scene.fog = new THREE.FogExp2(HORIZON, 0.00016);
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 30000);
  const MOON_DIR = new THREE.Vector3(-0.731, 0.17, -0.674).normalize();       // low (≈ 10°) behind the mast: the boat sits on its glitter path
  const MOONLIGHT = kelvin(4100), LANTERN = new THREE.Color(css("--lantern", "#ff9a3c"));

  /* sky: deep navy zenith, a lighter band at the horizon, a wide moon glow (Mie) */
  scene.add(new THREE.Mesh(new THREE.SphereGeometry(12000, 64, 32), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { uMoon: { value: MOON_DIR } },
    vertexShader: "varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
    fragmentShader: [
      "uniform vec3 uMoon; varying vec3 vD;",
      "void main(){ vec3 d = normalize(vD); float y = max(d.y, -0.1);",
      "  vec3 zen = vec3(0.004, 0.008, 0.024), hor = vec3(0.035, 0.058, 0.105);",
      "  vec3 c = mix(hor, zen, smoothstep(0.0, 0.55, y));",
      "  float m = max(dot(d, uMoon), 0.0);",
      "  c += vec3(0.55, 0.62, 0.78) * (pow(m, 900.0) * 1.2 + pow(m, 60.0) * 0.16 + pow(m, 8.0) * 0.05);",
      "  c = mix(c, hor * 0.6, smoothstep(0.0, -0.06, d.y));",
      "  gl_FragColor = vec4(c, 1.0);",
      "  #include <tonemapping_fragment>",
      "  #include <colorspace_fragment>",
      "}"].join("\n") })));

  /* moon: a disc 2.1° wide, bright enough to bloom, with a soft halo card */
  const moon = new THREE.Mesh(new THREE.CircleGeometry(1, 64), new THREE.MeshBasicMaterial({ map: moonTexture(), color: new THREE.Color(1, 0.98, 0.93).multiplyScalar(1.35),
    transparent: true, fog: false, depthWrite: false }));
  const MOON_D = 9000; moon.position.copy(MOON_DIR).multiplyScalar(MOON_D); moon.scale.setScalar(MOON_D * Math.tan(THREE.MathUtils.degToRad(1.05))); scene.add(moon);
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: spriteTex("soft"), color: new THREE.Color(0.55, 0.62, 0.8), transparent: true, opacity: 0.35,
    blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
  halo.position.copy(moon.position); halo.scale.setScalar(moon.scale.x * 7); halo.material.opacity = 0.28; scene.add(halo);

  /* stars: a seeded sphere; each twinkles at its own rate (scintillation is stronger near the horizon) */
  const NSt = 2600, sr = rng(29), sp = new Float32Array(NSt * 3), sb = new Float32Array(NSt), sf = new Float32Array(NSt);
  for (let i = 0; i < NSt; i++) { const u = 0.03 + sr() * 0.97, a = sr() * Math.PI * 2, rr = Math.sqrt(1 - u * u);
    sp.set([rr * Math.cos(a) * 10000, u * 10000, rr * Math.sin(a) * 10000], i * 3); sb[i] = Math.pow(sr(), 4); sf[i] = sr() * 40; }
  const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.BufferAttribute(sp, 3)); sg.setAttribute("b", new THREE.BufferAttribute(sb, 1)); sg.setAttribute("f", new THREE.BufferAttribute(sf, 1));
  const starU = { uT: { value: 0 }, uMoon: { value: MOON_DIR } };
  scene.add(new THREE.Points(sg, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, fog: false, blending: THREE.AdditiveBlending, uniforms: starU,
    vertexShader: "attribute float b; attribute float f; uniform float uT; uniform vec3 uMoon; varying float vA; void main(){ vec3 d = normalize(position);"
      + " float tw = 0.75 + 0.25 * sin(uT * (3.0 + f * 0.2) + f) * (1.0 - d.y);"
      + " float moonWash = smoothstep(0.995, 0.93, dot(d, uMoon));"
      + " vA = (0.25 + 1.8 * b) * tw * moonWash * smoothstep(0.02, 0.12, d.y);"
      + " vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_Position = projectionMatrix * mv; gl_PointSize = 1.4 + 2.2 * b; }",
    fragmentShader: "varying float vA; void main(){ float r = length(gl_PointCoord - 0.5); if (r > 0.5) discard; gl_FragColor = vec4(vec3(0.8, 0.86, 1.0) * vA, (1.0 - r * 2.0)); }" })));

  /* the far shore: a dark low strip with a scatter of warm and white lights 6–7 km off (they streak in the water) */
  const NL = 150, lr = rng(77), lp = new Float32Array(NL * 3), lc = new Float32Array(NL * 3);
  for (let i = 0; i < NL; i++) { const x = -5200 + Math.pow(lr(), 0.8) * 7000; lp.set([x, 4 + lr() * 14 * lr(), -6480 + lr() * 30], i * 3);
    const c = lr() < 0.7 ? kelvin(2200 + lr() * 900) : kelvin(5200); lc.set([c.r, c.g, c.b], i * 3); }
  const lg = new THREE.BufferGeometry(); lg.setAttribute("position", new THREE.BufferAttribute(lp, 3)); lg.setAttribute("color", new THREE.BufferAttribute(lc, 3));
  scene.add(new THREE.Points(lg, new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true, transparent: true, opacity: 0.75, fog: false,
    blending: THREE.AdditiveBlending, depthWrite: false })));

  /* the sea: three.js Water (planar reflection) with a long low swell normal map; the moon is its "sun" */
  const water = makeSea({ size: 24000, res: 1024, color: 0x061525, distortion: 3.2, waveSize: 2.4,
    normals: normalFromHeight(512, (x, y) => fbm(x / 48, y / 48, 4) * 0.7 + fbm(x / 11 + 9, y / 11, 3) * 0.3, 2.6) });
  water.material.uniforms.sunDirection.value.copy(MOON_DIR);
  water.material.uniforms.sunColor.value.copy(MOONLIGHT).multiplyScalar(0.9);
  water.material.uniforms.alpha.value = 1.0;
  scene.add(water);

  /* light: moon key from behind-left, a dim cool sky fill, the lantern */
  const key = new THREE.DirectionalLight(MOONLIGHT, 0.85); key.position.copy(MOON_DIR).multiplyScalar(100); scene.add(key);
  scene.add(new THREE.HemisphereLight(0x2a3c5e, 0x0a1220, 0.8));
  const bounce = new THREE.DirectionalLight(0x7f9cc8, 0.55); bounce.position.set(14, 1.5, 15); scene.add(bounce);   // the sea's glitter bounced onto the near side
  const { boat, lantern, lamp, flameMat, glow, glass } = makeBoat(LANTERN);
  scene.add(boat);

  /* the lantern's warm pool on the water and its broken reflection column (the Water reflection carries the flame) */
  const pool = new THREE.Mesh(new THREE.PlaneGeometry(9, 9), new THREE.MeshBasicMaterial({ map: spriteTex("soft"), color: LANTERN.clone().multiplyScalar(0.22), transparent: true,
    blending: THREE.AdditiveBlending, depthWrite: false })); pool.rotation.x = -Math.PI / 2; pool.position.set(0.9, 0.02, 0.6); scene.add(pool);

  /* the fish: at 2.8 s a splash and two expanding rings, 6 m off the bow */
  const FX = 2.1, FZ = 6.5, ringTex = spriteTex("ring"), rings = [];
  for (let k = 0; k < 2; k++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: ringTex, color: new THREE.Color(0.75, 0.8, 0.9), transparent: true,
    opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); m.rotation.x = -Math.PI / 2; m.position.set(FX, 0.03, FZ); scene.add(m); rings.push(m); }
  const sprayN = 60, spr = rng(9), sprayPos = new Float32Array(sprayN * 3), sprayV = [];
  for (let i = 0; i < sprayN; i++) sprayV.push([(spr() - 0.5) * 1.6, 1.4 + spr() * 2.0, (spr() - 0.5) * 1.6]);
  const sprayG = new THREE.BufferGeometry(); sprayG.setAttribute("position", new THREE.BufferAttribute(sprayPos, 3));
  const sprayM = new THREE.PointsMaterial({ size: 0.07, color: 0xbfd0e8, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  scene.add(new THREE.Points(sprayG, sprayM));
  const FISH_T = 2.8;

  const post = makePost(renderer, scene, camera, W, H, { bloom: 0.6, bloomThreshold: 0.78, aperture: 0.00012, maxblur: 0.004, vignette: 0.55, grain: 0.11, ca: 1.0 });
  post.bloom.radius = 0.75;
  const look = makeLookPass({ night: 0.35, split: 0.55, warm: 0xffa860, cool: 0x4f6fa8 });
  post.composer.insertPass(look, post.composer.passes.length - 1);

  /* the shot: low over the water off the port bow, arcing 10° and pushing in */
  const camAt = (t) => { const e = smooth(-0.6, SECONDS + 0.4, t), a = THREE.MathUtils.degToRad(132 - 12 * e), r = 19 - 5.5 * e;
    return [new THREE.Vector3(Math.cos(a) * r * -1 + 1.2, 1.55 + 0.35 * e, Math.sin(a) * r), new THREE.Vector3(-0.2, 1.75 - 0.15 * e, -0.4)]; };

  function update(t) {
    /* the swell: heave, pitch and roll from a few slow sines (the hull rides, never jitters) */
    const heave = 0.09 * Math.sin(1.25 * t + 0.4) + 0.035 * Math.sin(2.3 * t + 1.7);
    boat.position.set(0, heave - 0.02, 0);
    boat.rotation.set(0.05 * Math.sin(0.95 * t + 2.0) + 0.015 * Math.sin(2.1 * t), 0.18, 0.032 * Math.sin(1.1 * t + 0.9));
    /* kerosene flicker: a few octaves of noise, never below 80 % */
    const fl = 0.9 + 0.07 * perlin(t * 7.0, 1.3) + 0.04 * perlin(t * 19.0, 4.1);
    lamp.intensity = 9 * fl; glow.material.opacity = 0.32 * fl; flameMat.color.copy(LANTERN).multiplyScalar(13 * fl);
    lantern.rotation.z = 0.06 * Math.sin(1.1 * t + 0.9 + 0.4);                  // the lantern swings against the roll
    pool.material.opacity = 0.85 * fl;
    water.material.uniforms.time.value = 0.55 * t;
    starU.uT.value = t;
    /* the fish */
    const ft = t - FISH_T;
    rings.forEach((m, k) => { const u = ft - k * 0.35; const on = u > 0;
      m.material.opacity = on ? 0.9 * Math.exp(-u * 0.9) : 0; m.scale.setScalar(on ? 0.6 + 3.4 * u : 0.01); });
    for (let i = 0; i < sprayN; i++) { const v = sprayV[i], u = Math.max(0, Math.min(ft, 0.7));
      sprayPos.set([FX + v[0] * u, 0.05 + v[1] * u - 4.9 * u * u, FZ + v[2] * u], i * 3); }
    sprayG.attributes.position.needsUpdate = true; sprayM.opacity = ft > 0 && ft < 0.7 ? 0.8 * (1 - ft / 0.7) : 0;
    /* camera, fade-in, focus on the boat */
    const [p, l] = camAt(t); camera.position.copy(p); camera.lookAt(l);
    moon.lookAt(camera.position);
    renderer.toneMappingExposure = 0.95 * (0.12 + 0.88 * smooth(0.0, 1.1, t));
    post.bokeh.uniforms.focus.value = p.distanceTo(new THREE.Vector3(0, 1.2, 0));
    post.grade.uniforms.uWarm.value = 0.05;
  }
  const render = makeFrameLoop(renderer, post, W, H, update);
  return { render, ready: Promise.resolve(), scene, camera, renderer };
}

window.__three = { build };
