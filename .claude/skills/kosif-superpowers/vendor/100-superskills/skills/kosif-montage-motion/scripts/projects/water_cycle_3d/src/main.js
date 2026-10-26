/* The water cycle as a cinematic 3D film, written on the KOSIF three-kit. Everything is a function of t (seconds):
   the sun, the sea, the clouds, the rain, the river, the camera. window.__three.render(t) draws one frame. */
import { THREE, rng, fbm, ridged, smooth, clamp01, ramp, lerp, makeRenderer, makeSky, makeSunLight, makeFill, makeTerrain, alpineColour,
         slopeOf, makeForest, makeFlock, makeSea, makeRibbon, makeCloudSlab, makeLensflare, makeVapour, makeRain, makePost, cameraKeys, makeFrameLoop }
  from "../../../kit/three-kit.js";

/* ───────── the land: a mountain range behind a bay, a valley carved by the river ───────── */
const RIVER = (z) => 140 * Math.sin(z / 420) - 220;      // the river's x for a given z (from the peak, z=-900, to the bay, z=700)
function height(x, z) {
  const wx = x + 180 * fbm(x * 0.0009 + 20, z * 0.0009 + 7, 3), wz = z + 180 * fbm(x * 0.0009 + 3, z * 0.0009 + 41, 3);   // domain warp: bent, eroded ridges
  const ridge = 820 * Math.exp(-Math.pow((z + 1250) / 820, 2)) * (0.55 + 0.45 * ridged(wx * 0.0006 + 3.1, wz * 0.0006));
  const hills = 260 * ridged(wx * 0.0011 + 7.7, wz * 0.0011 + 1.2) * Math.exp(-Math.pow((z + 500) / 1100, 2));
  const detail = 55 * fbm(x * 0.004, z * 0.004, 4) + 14 * fbm(x * 0.02 + 9, z * 0.02 + 4, 3);
  const land = smooth(900, 150, z);                         // the land sinks under the sea toward the camera
  let h = (ridge + hills + detail + 60) * land - 45 * (1 - land);
  const d = Math.abs(x - RIVER(z));
  if (z > -950 && z < 800) h -= 150 * Math.exp(-(d * d) / (2 * 55 * 55)) * smooth(-950, -700, z) * land;   // the channel
  return h;
}

export function build(canvas, W, H) {
  const renderer = makeRenderer(canvas, W, H);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0xc9d6e2, 0.00011);
  const camera = new THREE.PerspectiveCamera(38, W / H, 2, 60000);

  const sky = makeSky(scene);
  const sunLight = makeSunLight(scene);
  const hemi = new THREE.HemisphereLight(0xbfd8ff, 0x3a4a2a, 0.55); scene.add(hemi);
  const flashLight = new THREE.PointLight(0xdfe9ff, 0, 5000, 1.2); flashLight.position.set(-300, 1100, -900); scene.add(flashLight);
  const fill = makeFill(scene);

  scene.add(makeTerrain({ height, colour: alpineColour }));
  scene.add(makeForest({ height, region: [-2200, 2100, -1950, 700], seed: 42,
    accept: (x, z, h) => h >= 28 && h <= 430 && slopeOf(height, x, z) <= 0.42 && !(Math.abs(x - RIVER(z)) < 40 && z > -900 && z < 800) }));
  const water = makeSea(); scene.add(water);
  const flare = makeLensflare(); scene.add(flare);
  // a flock crosses the bay at dawn (scale and life), and another drifts past the final wide shot
  // flocks fly near the focus plane (≈ the look-at distance) so depth of field keeps them crisp
  // heights chosen by projecting them in-page: ≈ 150–240 px from the top — sky above the ridge, below the titles
  const flock1 = makeFlock({ n: 16, seed: 23, t0: 2.9, t1: 4.8, size: 16, spread: 220, path: [[2.9, 1500, 560, 1200], [4.8, -1000, 660, 200]] }); scene.add(flock1);
  const flock2 = makeFlock({ n: 11, seed: 51, t0: 15.4, t1: 17.0, size: 18, spread: 240, path: [[15.4, -1300, 760, 900], [17.0, 1200, 800, 500]] }); scene.add(flock2);
  const vapour = makeVapour({ region: [-900, 600, -50, 900], seed: 5 }); scene.add(vapour);
  const rain = makeRain({ region: [-1500, 700, -1700, 300], seed: 11 }); scene.add(rain);
  const clouds = makeCloudSlab(); scene.add(clouds);
  const pts = [];
  for (let z = -880; z <= 840; z += 40) { const x = RIVER(z); pts.push(new THREE.Vector3(x, Math.max(height(x, z), -3) + 3.5, z)); }
  const river = makeRibbon(new THREE.CatmullRomCurve3(pts), { normals: water.userData.normals }); scene.add(river);

  const post = makePost(renderer, scene, camera, W, H);
  const camAt = cameraKeys([                                // t, camera xyz, look-at xyz — three slow moves, stillness between
    [0.0, 1300, 90, 2600, -200, 350, -700],
    [3.0, 900, 170, 2000, -250, 380, -650],
    [6.5, 300, 400, 1250, -350, 620, -600],
    [9.5, -100, 660, 500, -400, 980, -1000],
    [12.8, -520, 640, 560, -300, 300, -600],
    [15.2, 380, 560, 1350, -150, 20, 420],
    [17.0, 1300, 540, 2700, 0, 320, -500],
  ]);
  const state = {};

  function update(t) {
    // sun: dawn → day → overcast → clearing; it rises in front of the lens, then swings to a side key light
    const elev = 2.5 + 24 * smooth(0, 6.5, t) - 8 * smooth(8, 10, t) + 12 * smooth(12.5, 15.5, t);
    const azim = 195 - 80 * smooth(1.5, 7.5, t) + 12 * smooth(12, 17, t);
    const sun = sky.setSun(elev, azim);
    const overcast = smooth(8, 10, t) * (1 - smooth(12.6, 15.5, t));
    sky.uniforms.turbidity.value = 3 + 7 * overcast; sky.uniforms.rayleigh.value = 1.6 - 0.9 * overcast; sky.uniforms.mieCoefficient.value = 0.004 + 0.02 * overcast;
    sunLight.position.copy(sun).multiplyScalar(6000).add(new THREE.Vector3(0, 0, -600)); sunLight.target.position.set(0, 300, -700);
    const flash = Math.max(0, 1 - Math.abs(t - 10.6) / 0.09) + 0.55 * Math.max(0, 1 - Math.abs(t - 10.82) / 0.07);
    sunLight.intensity = (3.0 - 2.1 * overcast) * (0.35 + 0.65 * smooth(0, 4, t)) + flash * 0.5;
    sunLight.color.setHSL(0.08, 0.6, 0.5 + 0.5 * smooth(0, 5, t)).lerp(new THREE.Color(0xffffff), smooth(2, 6, t));
    hemi.intensity = 0.45 + 0.35 * smooth(0, 5, t) - 0.1 * overcast;
    flashLight.intensity = flash * 9000;
    renderer.toneMappingExposure = 0.5 + 0.12 * smooth(0, 5, t) - 0.08 * overcast + flash * 0.05;
    scene.fog.color.setHex(0xc9d6e2).lerp(new THREE.Color(0x9aa6b2), overcast).lerp(new THREE.Color(0xd9a57a), 1 - smooth(0, 4, t));
    scene.fog.density = 0.00011 + 0.00012 * overcast;
    // sea
    const wu = water.material.uniforms;
    wu.time.value = t * 0.55; wu.sunDirection.value.copy(sun).normalize(); wu.sunColor.value.copy(sunLight.color);
    wu.waterColor.value.setHex(0x0e4a63).lerp(new THREE.Color(0x24414f), overcast);
    // vapour, clouds, rain, river
    vapour.userData.set(t, ramp(t, 2.6, 3.6) * (1 - ramp(t, 6.2, 7.2)));
    const cover = 0.42 * ramp(t, 5.8, 7.6) + 0.5 * ramp(t, 7.4, 9.4) - 0.55 * ramp(t, 12.8, 15.2) - 0.22 * ramp(t, 15.2, 17);
    rain.userData.set(t, ramp(t, 9.5, 10.3) * (1 - ramp(t, 12.6, 13.4)));
    river.userData.reveal(ramp(t, 12.6, 14.4)); river.userData.flow(t);
    flock1.userData.set(t); flock2.userData.set(t);
    // camera, fill and focus
    const [p, l] = camAt(t);
    camera.position.copy(p); camera.lookAt(l);
    camera.fov = 38 - 4 * smooth(9.5, 12.8, t) + 4 * smooth(12.8, 15.2, t); camera.updateProjectionMatrix();
    fill.position.copy(p).add(new THREE.Vector3(0, 400, 0)); fill.target.position.copy(l);
    const valley = smooth(12.4, 13.4, t) * (1 - smooth(15.0, 16.0, t));
    fill.intensity = 0.35 + 2.0 * valley; hemi.intensity += 0.5 * valley; renderer.toneMappingExposure += 0.16 * valley;
    post.bokeh.uniforms.focus.value = p.distanceTo(l) * 0.9;
    clouds.userData.set(t, cover, overcast, sun, camera.position, sunLight.color.clone().multiplyScalar(1.0 + flash * 1.6),
      new THREE.Color(0x9fb6cc).lerp(new THREE.Color(0x56616d), overcast));
    // the sun on screen: god rays and the lens flare follow it
    const inFront = post.sunOnScreen(sun);
    const rayAmt = inFront ? (0.9 * (1 - smooth(2.5, 5, t)) + 0.3 + 0.35 * overcast * (1 - smooth(13, 15, t))) : 0;
    post.rays.uniforms.uAmount.value = rayAmt * (1 - flash * 0.5);
    flare.position.copy(sun).multiplyScalar(9000).add(camera.position);
    flare.visible = inFront && t < 7.5; flare.userData.flare.visible = flare.visible;
    post.grade.uniforms.uWarm.value = 0.75 * (1 - smooth(0, 5, t)) + 0.2;
    post.grade.uniforms.uLift.value = 0.08 * overcast;
    state.t = t;
  }
  const render = makeFrameLoop(renderer, post, W, H, update);
  return { render, scene, camera, renderer, state };
}

window.__three = { build };
