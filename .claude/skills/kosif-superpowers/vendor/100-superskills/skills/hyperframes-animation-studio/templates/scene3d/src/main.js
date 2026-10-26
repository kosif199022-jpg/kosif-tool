/* A cinematic 3D film on the KOSIF three-kit. Replace the land, the beats and the camera; keep everything a function
   of t. window.__three.render(t) draws one frame; index.html calls it from window.render(t). */
import { THREE, fbm, ridged, smooth, ramp, makeRenderer, makeSky, makeSunLight, makeFill, makeTerrain, alpineColour, slopeOf,
         makeForest, makeSea, makeCloudSlab, makeLensflare, makePost, cameraKeys, makeFrameLoop } from "../../../kit/three-kit.js";

const SECONDS = {{SECONDS}};

/* the land: a ridge behind a bay (edit freely; keep it a pure function of x, z) */
function height(x, z) {
  const ridge = 700 * Math.exp(-Math.pow((z + 1200) / 800, 2)) * (0.55 + 0.45 * ridged(x * 0.0006 + 3.1, z * 0.0006));
  const hills = 220 * ridged(x * 0.0011 + 7.7, z * 0.0011 + 1.2) * Math.exp(-Math.pow((z + 500) / 1100, 2));
  const land = smooth(900, 150, z);
  return (ridge + hills + 50 * fbm(x * 0.004, z * 0.004, 4) + 60) * land - 45 * (1 - land);
}

export function build(canvas, W, H) {
  const renderer = makeRenderer(canvas, W, H);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0xc9d6e2, 0.00011);
  const camera = new THREE.PerspectiveCamera(38, W / H, 2, 60000);
  const sky = makeSky(scene), sunLight = makeSunLight(scene), fill = makeFill(scene);
  const hemi = new THREE.HemisphereLight(0xbfd8ff, 0x3a4a2a, 0.6); scene.add(hemi);
  scene.add(makeTerrain({ height, colour: alpineColour }));
  scene.add(makeForest({ height, region: [-2200, 2200, -1900, 700], accept: (x, z, h) => h >= 28 && h <= 430 && slopeOf(height, x, z) <= 0.42 }));
  const water = makeSea(); scene.add(water);
  const clouds = makeCloudSlab(); scene.add(clouds);
  const flare = makeLensflare(); scene.add(flare);
  const post = makePost(renderer, scene, camera, W, H);
  const camAt = cameraKeys([                                // t, camera xyz, look-at xyz
    [0, 1300, 90, 2600, -200, 350, -700],
    [SECONDS * 0.5, 300, 400, 1250, -350, 620, -600],
    [SECONDS, 1300, 540, 2700, 0, 320, -500],
  ]);

  function update(t) {
    const sun = sky.setSun(6 + 20 * smooth(0, SECONDS * 0.4, t), 165 - 50 * smooth(0.1 * SECONDS, 0.5 * SECONDS, t));   // sun off-axis: no white-out
    sunLight.position.copy(sun).multiplyScalar(6000).add(new THREE.Vector3(0, 0, -600)); sunLight.target.position.set(0, 300, -700);
    sunLight.intensity = 3.0 * (0.35 + 0.65 * smooth(0, 4, t));
    sunLight.color.setHSL(0.08, 0.6, 0.5 + 0.5 * smooth(0, 5, t)).lerp(new THREE.Color(0xffffff), smooth(2, 6, t));
    renderer.toneMappingExposure = 0.46 + 0.12 * smooth(0, 5, t);
    const wu = water.material.uniforms; wu.time.value = t * 0.55; wu.sunDirection.value.copy(sun).normalize(); wu.sunColor.value.copy(sunLight.color);
    const [p, l] = camAt(t);
    camera.position.copy(p); camera.lookAt(l);
    fill.position.copy(p).add(new THREE.Vector3(0, 400, 0)); fill.target.position.copy(l); fill.intensity = 0.35;
    post.bokeh.uniforms.focus.value = p.distanceTo(l) * 0.9;
    clouds.userData.set(t, 0.3 * ramp(t, 2, 6), 0, sun, camera.position, sunLight.color, new THREE.Color(0x9fb6cc));
    const inFront = post.sunOnScreen(sun);
    post.rays.uniforms.uAmount.value = inFront ? 0.9 * (1 - smooth(2.5, 5, t)) + 0.3 : 0;
    flare.position.copy(sun).multiplyScalar(9000).add(camera.position); flare.visible = inFront && t < 7.5; flare.userData.flare.visible = flare.visible;
    post.grade.uniforms.uWarm.value = 0.75 * (1 - smooth(0, 5, t)) + 0.2;
  }
  const render = makeFrameLoop(renderer, post, W, H, update);
  const ready = Promise.resolve();                          // async loads (loadModel, textures) resolve this before frame 0
  return { render, ready, scene, camera, renderer };
}

window.__three = { build };
