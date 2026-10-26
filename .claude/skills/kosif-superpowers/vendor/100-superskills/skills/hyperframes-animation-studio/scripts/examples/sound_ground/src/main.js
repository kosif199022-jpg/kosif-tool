/* الصوت يرسم الأرض — the sound draws the land. Every value on screen is read from the score's analysis (motion.py channels):
   the spectrogram is the canyon, the bass is a lava river, kicks throw sparks and squash the chrome orb, and the whole world
   runs on the tape clock — when the track tape-stops, the land, the sparks and the dust freeze while the camera keeps
   drifting around them (bullet time), the silence flips the picture negative, and the spin-up whips the camera home. */
import { THREE, smooth, clamp01, rng, spriteTex, makeRenderer, makePost, makeFrameLoop, envFromGradient, makeSpectrumGround,
         spectrumOnTape, makeSparks, makeGlitchPass } from "../../../kit/three-kit.js";
import ch from "./channels.json";
import heightURL from "./spectrum_height.png";

const SECONDS = 10.0, SPAN = 8, LEN = 120;                   // 8 tape-seconds of sound across 120 m of canyon
const UNITS = LEN / SPAN;                                     // metres per tape second

export function build(canvas, W, H) {
  const M = window.MOTION, C = M.channels(ch);
  const tape = (t) => C.tape(t);
  const renderer = makeRenderer(canvas, W, H, { exposure: 0.7 });
  renderer.shadowMap.enabled = false;
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x1a0a16, 0.018);
  const camera = new THREE.PerspectiveCamera(36, W / H, 0.1, 900);

  /* the sky: deep violet overhead, a magma horizon, and an eclipse on the vanishing point that breathes with the bass */
  const skyU = { uBass: { value: 0 } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(500, 48, 24), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform float uBass; varying vec3 vD;
      void main(){ vec3 d = normalize(vD); float y = d.y;
        vec3 top = vec3(0.012, 0.006, 0.03), hor = vec3(0.30, 0.06, 0.10), low = vec3(0.04, 0.01, 0.02);
        vec3 c = y > 0.0 ? mix(hor, top, pow(clamp(y * 3.2, 0.0, 1.0), 0.6)) : mix(hor, low, clamp(-y * 6.0, 0.0, 1.0));
        vec3 e = normalize(vec3(1.0, 0.075, 0.0)); float g = max(dot(d, e), 0.0), r = acos(min(1.0, g));
        float disc = 1.0 - smoothstep(0.072, 0.075, r);                          // the moon's black disc
        float corona = exp(-max(0.0, r - 0.074) * (46.0 - 12.0 * uBass)) * (0.55 + 1.1 * uBass);
        c = mix(c + vec3(1.0, 0.42, 0.16) * corona + vec3(0.9, 0.2, 0.3) * pow(g, 24.0) * 0.25, vec3(0.004, 0.0, 0.006), disc);
        gl_FragColor = vec4(c, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  scene.add(sky);
  envFromGradient(renderer, scene, { top: 0x0a0414, horizon: 0x8a2a1a, ground: 0x1a0606, sun: new THREE.Vector3(1, 0.075, 0), sunColor: 0xff8a4a, sunPower: 3 });

  /* the canyon (the texture arrives asynchronously; ready resolves when it is on the GPU) */
  let ground = null;
  const ready = new Promise((res, rej) => { const img = new Image(); img.onload = () => {
      const { texture, seconds } = spectrumOnTape(img, ch);
      ground = makeSpectrumGround(texture, { width: LEN, depth: 90, half: 17, segX: 960, segZ: 420, window: SPAN, seconds, amp: 5.2, glow: 1.0, lava: 0.72,
        light: new THREE.Vector3(1, 0.32, 0.18), lightColor: 0xff8a50, fillColor: 0x5a3a90, rock: 0x30262c });
      ground.position.set(0, -1.2, 0);
      scene.add(ground); res(); }; img.onerror = rej; img.src = heightURL; });

  /* the chrome orb floating over the playhead; a cube camera gives it the real canyon to reflect */
  const cubeRT = new THREE.WebGLCubeRenderTarget(256, { type: THREE.HalfFloatType, generateMipmaps: true, minFilter: THREE.LinearMipmapLinearFilter });
  const cubeCam = new THREE.CubeCamera(0.05, 600, cubeRT); scene.add(cubeCam);
  const orb = new THREE.Mesh(new THREE.SphereGeometry(0.9, 128, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1.0, roughness: 0.06, envMap: cubeRT.texture, envMapIntensity: 1.0 }));
  scene.add(orb);

  /* sparks from the river on every kick; they ride the land and hang in the air when the tape stops */
  const sparks = makeSparks(ch.kicks.map((k) => ({ t: k, x: 0, y: 0.1, z: 0 })), { per: 90, speed: 6.5, gravity: 7, drift: UNITS, size: 4.5, seed: 11 });
  scene.add(sparks);

  /* dust: slow embers in the air, also on the tape clock */
  const ND = 2400, r = rng(29), dpos = new Float32Array(ND * 3), dseed = [];
  for (let i = 0; i < ND; i++) dseed.push([r() * LEN - LEN / 2, 0.2 + r() * 9, (r() - 0.5) * 30, 0.15 + r() * 0.5, r() * 6.28]);
  const dgeo = new THREE.BufferGeometry(); dgeo.setAttribute("position", new THREE.BufferAttribute(dpos, 3));
  const dust = new THREE.Points(dgeo, new THREE.PointsMaterial({ map: spriteTex("soft"), color: 0xff9a5a, size: 0.09, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true }));
  dust.frustumCulled = false; scene.add(dust);

  const post = makePost(renderer, scene, camera, W, H, { bloom: 0.6, bloomThreshold: 0.78, aperture: 0.00006, maxblur: 0.004, vignette: 0.55, grain: 0.12, ca: 1.4 });
  post.bloom.radius = 0.6;
  post.grade.uniforms.uLift.value = 0.08;                        // no pure black: the canyon keeps its shapes in the shadows
  const glitch = makeGlitchPass();
  post.composer.insertPass(glitch, post.composer.passes.length - 1);  // before OutputPass: glitch the graded frame

  /* the camera, one continuous take that changes on the bars: a wide descent through the intro, a drop behind the orb on
     the first kick, a low chase, a crane up on the 4 s downbeat to show the rhythm in the walls, back down before the stop,
     an orbit of the frozen world during the tape stop (wall clock: the only thing still moving), a whip home on the spin-up,
     a low chase with a roll on every kick, and a rise for the end title. Keys: [t, angle, distance, height, lookX, lookY];
     Hermite between keys with finite-difference tangents, so the speed is continuous through every key. */
  const KEYS = [
    [0.0, -0.05, 14.5, 10.5, 16.0, 3.2], [1.2, -0.08, 13.0, 8.0, 13.0, 2.0], [2.0, -0.25, 8.8, 2.4, 10.0, 0.8],
    [3.0, -0.10, 8.4, 2.1, 10.0, 0.8], [4.0, 0.12, 8.6, 2.3, 10.0, 0.8], [4.7, 0.08, 11.5, 5.2, 13.0, 0.2],
    [5.4, 0.02, 12.5, 6.2, 14.0, 0.0], [6.0, -0.05, 9.5, 3.2, 10.0, 0.8], [6.5, 0.55, 8.4, 2.6, 3.0, 1.2],
    [7.2, 1.15, 7.8, 2.4, 1.5, 1.3], [7.85, 0.12, 8.6, 2.2, 8.5, 0.9], [8.4, -0.12, 8.2, 2.0, 10.0, 0.8],
    [8.9, -0.18, 8.8, 2.4, 10.0, 0.8], [10.0, -0.05, 13.5, 6.5, 14.0, 0.4]];
  function camAt(t) {
    let i = 0; while (i < KEYS.length - 2 && t > KEYS[i + 1][0]) i++;
    const k0 = KEYS[Math.max(0, i - 1)], k1 = KEYS[i], k2 = KEYS[i + 1], k3 = KEYS[Math.min(KEYS.length - 1, i + 2)];
    const h = k2[0] - k1[0], u = clamp01((t - k1[0]) / h), u2 = u * u, u3 = u2 * u;
    const out = [];
    for (let j = 1; j < 6; j++) {
      const m1 = (k2[j] - k0[j]) / Math.max(1e-3, k2[0] - k0[0]) * h, m2 = (k3[j] - k1[j]) / Math.max(1e-3, k3[0] - k1[0]) * h;
      out.push((2 * u3 - 3 * u2 + 1) * k1[j] + (u3 - 2 * u2 + u) * m1 + (-2 * u3 + 3 * u2) * k2[j] + (u3 - u2) * m2);
    }
    const [a, dist, hh, lx, ly] = out;
    return [new THREE.Vector3(-Math.cos(a) * dist, hh, Math.sin(a) * dist), new THREE.Vector3(lx, ly, 0)];
  }
  const STOP = 6.0, FREEZE = 6.75, START = 7.2, HOME = 7.85;

  const dpo = new THREE.Vector3();
  function update(t) {
    const tp = tape(t), kick = C.kick(t, 1, 6), on = C.onset(t, 1, 3), bass = C.v("bass", t), speed = C.v("speed", t);
    const silent = C.silent(t), fr = Math.floor(t * 30);
    if (ground) ground.userData.set(t, tp, kick, (0.35 + 0.9 * on) * (silent ? 0 : 1) * smooth(0.3, 1.2, t));
    skyU.uBass.value = clamp01(bass * 1.1 + kick * 0.35);

    /* orb: bobs on the bass, squashes on the kick (volume kept), spins with the tape */
    const sq = 1 - 0.16 * kick, st = 1 / Math.sqrt(sq);
    orb.position.set(0, 1.45 + 0.35 * bass + 0.1 * Math.sin(tp * 2.1), 0);
    orb.scale.set(st, sq, st);
    orb.rotation.y = tp * 0.8;

    sparks.userData.set(t, tape);
    for (let i = 0; i < ND; i++) { const s = dseed[i];
      let x = s[0] - tp * UNITS * 0.85; x = ((x + LEN / 2) % LEN + LEN) % LEN - LEN / 2;
      dpo.set(x, s[1] + Math.sin(tp * s[3] * 2 + s[4]) * 0.25 + tp * s[3] * 0.4, s[2] + Math.cos(tp * s[3] + s[4]) * 0.3);
      dpos[i * 3] = dpo.x; dpos[i * 3 + 1] = (dpo.y % 9.5); dpos[i * 3 + 2] = dpo.z; }
    dgeo.attributes.position.needsUpdate = true;

    const [p, l] = camAt(t);
    const shake = 0.05 * kick;                                       // a short camera kick, seeded per frame
    camera.position.copy(p).add(new THREE.Vector3(0, shake * Math.sin(fr * 12.9898), shake * Math.cos(fr * 78.233)));
    camera.lookAt(l);
    camera.rotateZ(0.026 * kick * (Math.floor(t * 2) % 2 ? 1 : -1) * smooth(7.9, 8.3, t));   // a roll on each kick in the last chase
    camera.fov = 36 + 3.5 * kick - 2.5 * smooth(STOP, FREEZE, t) * (1 - smooth(START, HOME, t)); camera.updateProjectionMatrix();

    /* the cube camera sees the canyon from inside the orb */
    orb.visible = false; cubeCam.position.copy(orb.position); cubeCam.update(renderer, scene); orb.visible = true;

    post.bokeh.uniforms.focus.value = camera.position.distanceTo(orb.position);
    const inFront = post.sunOnScreen(new THREE.Vector3(1, 0.075, 0));
    post.rays.uniforms.uAmount.value = inFront ? 0.35 + 0.45 * kick : 0;
    post.grade.uniforms.uWarm.value = 0.45 + 0.3 * bass;
    renderer.toneMappingExposure = (0.85 + 0.25 * kick) * (0.75 + 0.25 * smooth(0.0, 0.9, t)) * (1 - 0.45 * smooth(9.4, 10.0, t));

    /* glitch keyed to the analysis, as accents: onsets split the colour, the tape's acceleration slices the frame, the first
       frames of silence tear in negative, and while the tape stands still the world turns cold silver (time stopped) */
    const dsp = Math.abs(C.v("speed", t + 1 / 60) - C.v("speed", t - 1 / 60)) * 30;
    const tear = silent && !C.silent(t - 0.1) ? 1 : 0;
    glitch.userData.set({ chroma: 0.35 * on + 0.6 * kick + 0.5 * clamp01(dsp / 2) + tear, slice: 0.35 * clamp01(dsp / 2) + 0.9 * tear,
                          negative: tear ? 0.9 : 0, mono: clamp01((0.25 - speed) / 0.25), warp: (1 - speed) * 0.6, frame: fr });
  }
  const render = makeFrameLoop(renderer, post, W, H, update);
  return { render, ready, scene, camera, renderer };
}

window.__three = { build };
