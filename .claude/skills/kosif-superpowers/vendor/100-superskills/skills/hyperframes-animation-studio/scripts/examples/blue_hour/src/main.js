/* الطريق في الساعة الزرقاء — Blue Hour Road. The book lessons as one film:
   · Gurney: aerial perspective (ridges lighten and blue with distance, darks first), reverse aerial perspective toward the
     afterglow, sodium lamps against blue-hour sky, shadows that face up go blue and those that face down go warm,
     a colour corona around every lamp, night vision in the darks.
   · Night Photography: a one-second exposure from a tripod — the cars become light trails, the stars short arcs
     (render with --blur 16 --shutter 30 --stack lighten).
   · Veo 3 shot language: a slow push-in at road height.  · Colour theory: a complementary blue/orange scheme. */
import { THREE, fbm, ridged, smooth, clamp01, rng, spriteTex, makeRenderer, makePost, makeFrameLoop, aerialPerspective, makeLookPass,
         lightColor, skyBounce, fogTowardSun, harmony, trailLength } from "../../../kit/three-kit.js";

const SECONDS = 8.0;
const ROAD_W = 8, LANE = 1.9;
const roadX = (z) => 22 * Math.sin(Math.min(0, z + 60) / 380) + 0.0004 * Math.min(0, z + 60) * Math.min(0, z + 60) * 0.02;

export function build(canvas, W, H) {
  aerialPerspective({ scatter: [0.55, 0.8, 1.3] });            // before any material compiles
  const renderer = makeRenderer(canvas, W, H, { exposure: 1.05, tone: "agx" });
  renderer.shadowMap.enabled = false;
  const scene = new THREE.Scene();
  const COOL = 0x8790b0, WARM = 0xc49a8a;                       // the haze is the horizon sky's colour: far forms end in the sky
  scene.fog = new THREE.FogExp2(COOL, 0.00062);
  const camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 20000);
  const SUN = new THREE.Vector3(-0.55, -0.06, -0.83).normalize();   // the sun just set, left of the road
  const scheme = harmony("complementary", 222);                    // blue sky, orange lamps

  /* sky: zenith blue, a warm afterglow band low toward the set sun, the Earth's shadow rising opposite */
  const skyU = { uSun: { value: SUN } };
  scene.add(new THREE.Mesh(new THREE.SphereGeometry(9000, 64, 32), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: "varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
    fragmentShader: [
      "uniform vec3 uSun; varying vec3 vD;",
      "void main(){ vec3 d = normalize(vD); float y = max(d.y, -0.2);",
      "  vec3 zen = vec3(0.020, 0.045, 0.13), mid = vec3(0.07, 0.15, 0.36), hor = vec3(0.30, 0.34, 0.52);",
      "  vec3 c = mix(hor, mid, smoothstep(0.0, 0.18, y)); c = mix(c, zen, smoothstep(0.15, 0.75, y));",
      "  float g = max(dot(normalize(vec3(d.x, 0.0, d.z)), normalize(vec3(uSun.x, 0.0, uSun.z))), 0.0);",
      "  float band = exp(-max(y, 0.0) * 9.0) * pow(g, 3.0);",
      "  c += vec3(1.0, 0.45, 0.20) * band * 0.9 + vec3(0.9, 0.35, 0.45) * exp(-max(y, 0.0) * 4.0) * pow(g, 1.5) * 0.18;",
      "  c = mix(c, vec3(0.03, 0.03, 0.05), smoothstep(0.0, -0.08, d.y));",
      "  gl_FragColor = vec4(c, 1.0);",
      "  #include <tonemapping_fragment>",
      "  #include <colorspace_fragment>",
      "}"].join("\n") })));

  /* stars: fixed on a sphere that turns about the pole (exaggerated so a 1 s exposure draws arcs) */
  const NS = 1600, sr = rng(41), sp = new Float32Array(NS * 3), sb = new Float32Array(NS);
  for (let i = 0; i < NS; i++) { const u = sr() * 2 - 1, a = sr() * Math.PI * 2, rr = Math.sqrt(1 - u * u);
    sp[i * 3] = rr * Math.cos(a) * 8000; sp[i * 3 + 1] = Math.abs(u) * 8000; sp[i * 3 + 2] = rr * Math.sin(a) * 8000; sb[i] = Math.pow(sr(), 3); }
  const sg = new THREE.BufferGeometry(); sg.setAttribute("position", new THREE.BufferAttribute(sp, 3)); sg.setAttribute("b", new THREE.BufferAttribute(sb, 1));
  const stars = new THREE.Points(sg, new THREE.ShaderMaterial({ transparent: true, depthWrite: false, fog: false, blending: THREE.AdditiveBlending,
    vertexShader: "attribute float b; varying float vB; varying float vY; void main(){ vB = b; vec4 mv = modelViewMatrix * vec4(position, 1.0); vY = normalize(position).y; gl_Position = projectionMatrix * mv; gl_PointSize = 2.0 + 3.5 * b; }",
    fragmentShader: "varying float vB; varying float vY; void main(){ float r = length(gl_PointCoord - 0.5); if (r > 0.5) discard; gl_FragColor = vec4(vec3(0.75, 0.82, 1.0) * (0.6 + 2.2 * vB), (1.0 - r * 2.0) * smoothstep(0.05, 0.35, vY)); }" }));
  const pole = new THREE.Object3D(); pole.rotation.set(-0.45, 0, 0.25); pole.add(stars); scene.add(pole);

  /* ridges: four silhouettes at 0.7, 1.4, 2.6 and 4.5 km — the same dark rock, made blue and pale by the air alone */
  const ridgeMat = new THREE.MeshStandardMaterial({ color: 0x2b2420, roughness: 1 });
  [[700, 140, 1.1], [1400, 260, 2.3], [2600, 420, 3.7], [4500, 650, 5.2]].forEach(([dz, hgt, seed]) => {
    const g = new THREE.PlaneGeometry(dz * 4.2, hgt * 1.6, 400, 1), p = g.attributes.position;
    for (let i = 0; i < p.count; i++) if (p.getY(i) > 0) { const x = p.getX(i) / dz;
      p.setY(i, hgt * (0.35 + 0.65 * ridged(x * 2.2 + seed, seed * 3.1, 5)) - hgt * 0.2); } else p.setY(i, -hgt);
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, ridgeMat); m.position.set(-dz * 0.25, 0, -dz); scene.add(m);
  });

  /* the desert floor and the road (slightly wet asphalt: lamps and headlights glint on it) */
  const gg = new THREE.PlaneGeometry(9000, 9000, 260, 260); gg.rotateX(-Math.PI / 2);
  const gp = gg.attributes.position;
  for (let i = 0; i < gp.count; i++) { const x = gp.getX(i), z = gp.getZ(i), off = Math.abs(x - roadX(z));
    gp.setY(i, (1.6 * fbm(x * 0.004, z * 0.004, 4) + 0.6 * fbm(x * 0.03, z * 0.03, 2)) * smooth(ROAD_W, ROAD_W + 30, off) - 0.05); }
  gg.computeVertexNormals();
  scene.add(new THREE.Mesh(gg, new THREE.MeshStandardMaterial({ color: 0x8f7258, roughness: 0.95 })));
  const pts = []; for (let z = 40; z > -4200; z -= 20) pts.push(new THREE.Vector3(roadX(z), 0.03, z));
  const curve = new THREE.CatmullRomCurve3(pts);
  const N = 800, rpos = new Float32Array((N + 1) * 2 * 3), ridx = [];
  for (let i = 0; i <= N; i++) { const c = curve.getPointAt(i / N), tg = curve.getTangentAt(i / N), nx = -tg.z, nz = tg.x, l = Math.hypot(nx, nz) || 1;
    rpos.set([c.x + nx / l * ROAD_W / 2, 0.04, c.z + nz / l * ROAD_W / 2, c.x - nx / l * ROAD_W / 2, 0.04, c.z - nz / l * ROAD_W / 2], i * 6);
    if (i < N) ridx.push(i * 2, i * 2 + 1, i * 2 + 2, i * 2 + 1, i * 2 + 3, i * 2 + 2); }
  const rg = new THREE.BufferGeometry(); rg.setAttribute("position", new THREE.BufferAttribute(rpos, 3)); rg.setIndex(ridx); rg.computeVertexNormals();
  scene.add(new THREE.Mesh(rg, new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: 0.32, metalness: 0.0, side: THREE.DoubleSide })));

  /* lane markings: the leading lines (dashes on the centre line, solid edge lines) — retro-reflective paint glows a little */
  const paint = new THREE.MeshStandardMaterial({ color: 0xe8e4da, roughness: 0.5, emissive: 0x6a6658, emissiveIntensity: 0.6 });
  const dash = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.16, 3), paint, 340), dm = new THREE.Object3D();
  for (let i = 0; i < 340; i++) { const z = 30 - i * 12, x = roadX(z); dm.position.set(x, 0.05, z); dm.rotation.set(-Math.PI / 2, 0, Math.atan(roadX(z - 1) - x)); dm.updateMatrix(); dash.setMatrixAt(i, dm.matrix); }
  scene.add(dash);
  for (const side of [-1, 1]) { const lp = [], li = [];
    for (let i = 0; i <= N; i++) { const c = curve.getPointAt(i / N), tg = curve.getTangentAt(i / N), nx = -tg.z, nz = tg.x, l = Math.hypot(nx, nz) || 1, o = side * (ROAD_W / 2 - 0.35);
      lp.push(c.x + nx / l * (o - 0.07), 0.05, c.z + nz / l * (o - 0.07), c.x + nx / l * (o + 0.07), 0.05, c.z + nz / l * (o + 0.07));
      if (i < N) li.push(i * 2, i * 2 + 1, i * 2 + 2, i * 2 + 1, i * 2 + 3, i * 2 + 2); }
    const eg = new THREE.BufferGeometry(); eg.setAttribute("position", new THREE.Float32BufferAttribute(lp, 3)); eg.setIndex(li); eg.computeVertexNormals();
    scene.add(new THREE.Mesh(eg, Object.assign(paint.clone(), { side: THREE.DoubleSide }))); }

  /* light: blue sky above, a warm bounce below (upfacing shadows cool, downfacing warm), the last of the afterglow */
  skyBounce(scene, { sky: 0x5a7ab8, ground: 0x6a4a36, intensity: 1.25 });
  const glow = new THREE.DirectionalLight(lightColor("sunrise"), 0.35); glow.position.set(SUN.x * 100, 6, SUN.z * 100); scene.add(glow);

  /* sodium lamps every 45 m on the right shoulder: emissive heads + pools on the asphalt; the six nearest are real lights */
  const sodium = lightColor("sodium"), lampMat = new THREE.MeshBasicMaterial({ color: sodium.clone().multiplyScalar(9) });
  const poleMat = new THREE.MeshStandardMaterial({ color: 0x1a1a1c, roughness: 0.6 }), pool = spriteTex("soft");
  for (let k = 0; k < 24; k++) { const z = -40 - k * 45, x = roadX(z) + ROAD_W / 2 + 1.6;
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 8, 6), poleMat); p.position.set(x, 4, z); scene.add(p);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.08, 0.1), poleMat); arm.position.set(x - 1.1, 8, z); scene.add(arm);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 8), lampMat); head.position.set(x - 2.1, 7.9, z); scene.add(head);
    const pd = new THREE.Mesh(new THREE.PlaneGeometry(16, 16), new THREE.MeshBasicMaterial({ map: pool, color: sodium.clone().multiplyScalar(0.55), transparent: true,
      blending: THREE.AdditiveBlending, depthWrite: false, fog: true })); pd.rotation.x = -Math.PI / 2; pd.position.set(x - 3, 0.06, z); scene.add(pd);
    if (k < 6) { const L = new THREE.PointLight(sodium, 70, 45, 2); L.position.copy(head.position); scene.add(L); } }

  /* cars: tail lights going away in the right lane, headlights coming in the left, 22–27 m/s */
  const cr = rng(13), cars = [], tailMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xff1e1e).multiplyScalar(6) }),
        headMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(0xfff1d8).multiplyScalar(6) }), body = new THREE.MeshStandardMaterial({ color: 0x0c0c0e, roughness: 0.4 });
  for (let i = 0; i < 18; i++) { const away = i % 2 === 0, g = new THREE.Group();
    const b = new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.2, 4.3), body); b.position.y = 0.75; g.add(b);
    const lights = [];
    for (const s of [-0.68, 0.68]) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.16, 10, 8), away ? tailMat : headMat); l.position.set(s, 0.8, 2.2); g.add(l); lights.push(l); }   // tail lights of the cars going away and headlights of those coming both face the camera (+z)
    scene.add(g); cars.push({ g, away, lights, z0: -cr() * 1500, v: 22 + cr() * 5 }); }
  const placeCar = (c, t) => { const span = 1560; let z = c.away ? c.z0 - c.v * t : c.z0 + c.v * t;
    z = ((z + 1500) % span + span) % span - 1500;
    const x = roadX(z) + (c.away ? LANE : -LANE), ahead = roadX(z - 1) - roadX(z);
    c.g.position.set(x, 0, z); c.g.rotation.y = Math.atan(ahead);
    const st = 1 + trailLength(c.v) / (2 * 0.16) * 1.2;           // overlapping sub-samples: a continuous trail, not dots
    for (const l of c.lights) { l.scale.z = st; l.position.z = 2.2 + 0.16 * (st - 1); } };   // the stretched light sits in front of the body, never inside it

  const post = makePost(renderer, scene, camera, W, H, { bloom: 0.75, bloomThreshold: 0.72, aperture: 0.00002, maxblur: 0.002, vignette: 0.5, grain: 0.1, ca: 1.2 });
  post.bloom.radius = 0.7;                                      // the colour corona: each glow takes its source's colour
  const look = makeLookPass({ night: 0.55, split: 0.45, warm: 0xffb36a, cool: 0x4a6aa8 });
  post.composer.insertPass(look, post.composer.passes.length - 1);

  /* the shot: a tripod at the road shoulder, a slow push-in (Veo: "slow push-in, low angle, road-level") */
  const camAt = (t) => { const e = smooth(0, SECONDS, t);
    return [new THREE.Vector3(6.4 - 1.0 * e, 1.5 + 0.2 * e, 16 - 7 * e), new THREE.Vector3(-8, 26.0, -420)]; };

  function update(t) {
    pole.rotation.y = t * 0.011;                                // ≈ 0.6° per second: arcs, not dashes, in a 1 s exposure
    for (const c of cars) placeCar(c, t);
    const [p, l] = camAt(t); camera.position.copy(p); camera.lookAt(l);
    fogTowardSun(scene, camera, SUN, COOL, WARM, 0.9);
    post.bokeh.uniforms.focus.value = 60;
    post.grade.uniforms.uWarm.value = 0.15;
  }
  const render = makeFrameLoop(renderer, post, W, H, update);
  return { render, ready: Promise.resolve(), scene, camera, renderer, scheme };
}

window.__three = { build };
