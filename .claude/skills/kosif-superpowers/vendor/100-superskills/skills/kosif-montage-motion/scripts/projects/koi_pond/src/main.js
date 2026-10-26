/* A koi pond at golden hour, written on the KOSIF three-kit v3 realism blocks. Metres. Everything is a function of t:
   the swell and the rings petals leave, caustics on the bed, seven koi bending as they swim, petals falling and
   floating, reeds in the wind, the sun through a canopy, and one slow camera move. */
import { THREE, rng, fbm, smooth, clamp01, lerp, makeRenderer, makeSky, envFromGradient, makeTerrain, makeShallowWater, addCaustics, makeKoi,
         makePetals, makePebbles, makeBlades, makeDappledSun, makePost, cameraPath, makeFrameLoop } from "../../../kit/three-kit.js";

const RX = 6.4, RZ = 4.1;                                    // the pond's ellipse
const rOf = (x, z) => Math.hypot(x / RX, z / RZ);            // 1 at the waterline
function height(x, z) {
  const r = rOf(x, z), n = fbm(x * 0.35 + 3, z * 0.35 + 7, 4), m = fbm(x * 1.8 + 11, z * 1.8 + 2, 3);
  const bowl = -0.92 * Math.pow(clamp01(1 - r * r), 0.65) - 0.04;                  // deepest in the middle, a shelf at the edge
  const bank = 0.1 + 0.18 * smooth(1.0, 2.2, r) + 0.12 * n;                         // the bank rises gently, uneven
  return lerp(bowl + 0.05 * m, bank + 0.03 * m, smooth(0.93, 1.06, r));
}
function groundColour(h, slope, x, z, c) {
  const n = 0.5 + 0.5 * fbm(x * 0.9 + 5, z * 0.9 + 1, 3), r = rOf(x, z);
  const silt = new THREE.Color(0x4a4532), sand = new THREE.Color(0x857a5c), mud = new THREE.Color(0x2e2a20), moss = new THREE.Color(0x3d5a26), moss2 = new THREE.Color(0x5f7a33);
  if (h < -0.02) c.copy(silt).lerp(sand, smooth(-0.5, -0.05, h) * 0.6 + 0.25 * n);
  else c.copy(mud).lerp(moss, smooth(1.0, 1.25, r)).lerp(moss2, n * smooth(1.2, 2, r) * 0.7);
}

export function build(canvas, W, H) {
  const renderer = makeRenderer(canvas, W, H, { exposure: 0.62 });
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0xcbb08a, 0.011);
  const camera = new THREE.PerspectiveCamera(36, W / H, 0.05, 600);
  const time = { value: 0 };

  /* light: a low golden sun seen through a canopy; the sky lights everything else */
  const sky = makeSky(scene, { turbidity: 5, rayleigh: 1.4, mie: 0.006, mieG: 0.86, scale: 450 });
  const sun = sky.setSun(17, 142);
  envFromGradient(renderer, scene, { top: 0x8fb1d6, horizon: 0xf2c894, ground: 0x34402a, sun, sunColor: 0xffcf8f, sunPower: 5 });
  scene.environmentIntensity = 0.55;
  const hemi = new THREE.HemisphereLight(0xffe2bf, 0x2d3a22, 0.35); scene.add(hemi);
  const dapple = makeDappledSun(scene, { intensity: 4.2, angle: 0.19, color: 0xffcf96, seed: 6, density: 0.15, shadowSize: 4096 });
  dapple.place(sun, new THREE.Vector3(0, 0, 0), 70);

  /* the land, the bed and the stones */
  const ground = makeTerrain({ height, colour: groundColour, size: 44, seg: 320, albedoRepeat: 10, normalRepeat: 22, normalScale: 0.8, roughness: 0.9, texSize: 512 });
  const groundCaus = addCaustics(ground.material, { time, level: 0, strength: 3.2, scale: 5.5, absorb: [1.35, 0.42, 1.0], sun: { value: sun.clone() } });
  scene.add(ground);
  const pebbles = makePebbles({ n: 2600, seed: 31, size: 0.038, clump: 0.55, region: [-RX, RX, -RZ, RZ], height, accept: (x, z) => rOf(x, z) < 0.97,
    caustics: { time, level: 0, strength: 3.2, scale: 5.5, absorb: [1.35, 0.42, 1.0], sun: { value: sun.clone() } } });
  scene.add(pebbles);
  const rim = makePebbles({ n: 170, seed: 77, size: 0.24, region: [-RX * 1.2, RX * 1.2, -RZ * 1.2, RZ * 1.2], height, accept: (x, z) => { const r = rOf(x, z); return r > 0.97 && r < 1.12; },
    caustics: { time, level: 0, strength: 2.2, scale: 5.5, absorb: [1.35, 0.42, 1.0], sun: { value: sun.clone() } } });
  rim.material.color = new THREE.Color(0xb7ad9c); scene.add(rim);

  /* reeds at the edge and grass on the bank, both in the wind */
  const reeds = makeBlades({ n: 2200, seed: 17, tall: 0.95, width: 0.018, amp: 0.07, freq: 1.2, time, hue: 0.2, region: [-RX * 1.4, RX * 1.4, -RZ * 1.4, RZ * 1.4], height,
    accept: (x, z) => { const r = rOf(x, z); return r > 1.0 && r < 1.3 && fbm(x * 0.6 + 9, z * 0.6, 2) > 0.02; } });
  scene.add(reeds);
  const grass = makeBlades({ n: 6000, seed: 19, tall: 0.22, width: 0.012, amp: 0.25, freq: 1.7, time, hue: 0.23, region: [-14, 14, -10, 10], height,
    accept: (x, z) => rOf(x, z) > 1.08 });
  scene.add(grass);

  /* the water */
  const water = makeShallowWater({ width: 2 * RX + 1, depth: 2 * RZ + 1, seg: 300, amp: 0.006, clarity: 0.72, deep: 0x1c3a22, shallow: 0x4d6a45,
    skyTop: 0x8fb3d8, skyHorizon: 0xe9c48e, bank: 0x232d1a, bankHeight: 0.14, ripples: 28 });
  water.material.uniforms.uDapple.value = dapple.texture; water.material.uniforms.uDappleOn.value = 1;
  scene.add(water);
  // the water surface only exists inside the pond: a soft alpha edge via a depth test against the bank is enough here
  water.scale.set(1, 1, 1);

  /* lily pads: notched discs floating in clusters, bobbing on the swell */
  const padGeo = new THREE.CircleGeometry(0.2, 28, 0.25, Math.PI * 2 - 0.25); padGeo.rotateX(-Math.PI / 2);
  const pads = new THREE.InstancedMesh(padGeo, new THREE.MeshStandardMaterial({ roughness: 0.42, side: THREE.DoubleSide }), 34);
  const pr = rng(12), padState = [], pc = new THREE.Color();
  for (let i = 0; i < 34; i++) {
    const cl = [[-3.6, 1.8], [3.2, -1.9], [-1.2, -2.7]][i % 3];
    const x = cl[0] + (pr() - 0.5) * 1.6, z = cl[1] + (pr() - 0.5) * 1.1;
    padState.push({ x, z, s: 0.7 + pr() * 0.7, ry: pr() * 6.28, ph: pr() * 6.28 });
    pc.setHSL(0.27 + pr() * 0.05, 0.45 + pr() * 0.2, 0.22 + pr() * 0.1); pads.setColorAt(i, pc);
  }
  pads.receiveShadow = true; pads.castShadow = true; scene.add(pads);

  /* koi: seven fish on looping paths at different depths and speeds */
  const koi = [], paths = [];
  const kr = rng(5);
  for (let i = 0; i < 7; i++) {
    const k = makeKoi({ seed: 3 + i, length: 0.62 + kr() * 0.3, amp: 0.1 + kr() * 0.04, caustics: { time, level: 0, strength: 2.0, scale: 5.5, absorb: [1.35, 0.42, 1.0], sun: { value: sun.clone() } } });
    scene.add(k); koi.push(k);
    const ax = 2.2 + kr() * 1.6, az = 1.3 + kr() * 1.1, w = 0.11 + kr() * 0.07, ph = kr() * 6.28, ph2 = kr() * 6.28, d = -0.22 - kr() * 0.3, cx = (kr() - 0.5) * 1.6, cz = (kr() - 0.5) * 1.0, dir = kr() < 0.5 ? 1 : -1;
    paths.push((t, out) => out.set(cx + ax * Math.sin(dir * w * t + ph), d + 0.05 * Math.sin(t * 0.7 + ph2), cz + az * Math.sin(dir * 2 * w * t + ph2)));
  }

  /* petals: some already afloat, the rest falling through the light, each landing rings the water */
  const petals = makePetals({ n: 170, seed: 9, region: [-4.5, 4.5, -2.8, 2.8], times: [-2, 11], floating: 0.45, water, size: 1.5 });
  scene.add(petals);

  const post = makePost(renderer, scene, camera, W, H, { bloom: 0.32, bloomThreshold: 0.86, aperture: 0.00022, maxblur: 0.006, grain: 0.1, vignette: 0.38, ca: 1.0 });
  post.rays.uniforms.uAmount.value = 0;
  const cam = cameraPath([                                       // t, camera xyz, look-at xyz: one continuous move, no stops
    [0.0, 4.5, 0.42, 2.3, -2.6, -0.12, -1.6],
    [3.4, 2.9, 0.62, 1.7, -0.8, -0.3, -0.6],
    [6.6, 1.3, 1.45, 1.7, 0.2, -0.36, -0.15],
    [10.0, -2.6, 2.5, 5.2, 0.0, -0.15, -0.6],
  ]);
  const tmp = new THREE.Object3D();

  function update(t) {
    time.value = t;
    water.userData.set(t, sun, new THREE.Color(1.0, 0.82, 0.58));
    dapple.setDapple(t);
    water.material.uniforms.uDappleM.value.copy(dapple.matrix());
    for (let i = 0; i < koi.length; i++) koi[i].userData.set(t, paths[i], 1.1 + 0.25 * (i % 3));
    petals.userData.set(t);
    for (let i = 0; i < padState.length; i++) { const p = padState[i];
      tmp.position.set(p.x + Math.sin(t * 0.15 + p.ph) * 0.03, 0.006 + Math.sin(t * 1.1 + p.ph) * 0.004, p.z); tmp.rotation.set(Math.sin(t * 0.9 + p.ph) * 0.015, p.ry + Math.sin(t * 0.2 + p.ph) * 0.05, 0);
      tmp.scale.setScalar(p.s); tmp.updateMatrix(); pads.setMatrixAt(i, tmp.matrix); }
    pads.instanceMatrix.needsUpdate = true;
    const [p, l] = cam(t);
    camera.position.copy(p); camera.lookAt(l); camera.updateMatrixWorld();
    post.bokeh.uniforms.focus.value = p.distanceTo(l);
    post.grade.uniforms.uWarm.value = 0.55; post.grade.uniforms.uLift.value = 0.02;
    renderer.toneMappingExposure = 0.6 + 0.05 * smooth(5, 9, t);
  }
  const DBG = window.__dbg || {};
  const hide = { water, pads, petals, grass, reeds, pebbles, rim, ground };
  for (const k in hide) if (DBG["no" + k]) hide[k].visible = false;
  if (DBG.nokoi) koi.forEach((k) => (k.visible = false));
  const render = DBG.nopost ? (t) => { update(t); renderer.render(scene, camera); } : makeFrameLoop(renderer, post, W, H, update);
  return { render, scene, camera, renderer };
}

window.__three = { build };
