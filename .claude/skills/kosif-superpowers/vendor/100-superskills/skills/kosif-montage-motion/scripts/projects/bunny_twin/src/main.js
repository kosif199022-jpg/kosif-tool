/* Bunny Structural Twin — 5 s, 1080×1920. A cute plush bunny sculpted with shape-kit (signed distance fields), turned
   into a 3D space truss (structural_twin.py v0.2), loaded, broken at the left ear root, repaired by a swap, ranked.
   Every number on screen comes from assets/twin.js (the solver's output) or is measured here (triangles).
   Everything is a function of t: frames render in any order, in parallel. */
(function () {
  const { THREE, envFromGradient, makeRenderer, makeFrameLoop, smooth, clamp01, lerp } = window.K3;
  const S = window.K3S, TW = window.TWIN;
  const B = { shape: 0, joint: 0.85, load: 1.65, brk: 2.55, swap: 3.35, rank: 4.15, end: 5.0 };
  const T_BREAK = 2.66, LOAD_MAX = 3.0;
  const easeOut = (x) => 1 - Math.pow(1 - clamp01(x), 3);
  const easeInOut = (x) => { x = clamp01(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  /* a damped spring from 0 to 1 starting at t0 (overshoots once, settles): squash, pops, the ear's flop */
  const spring = (t, t0, f = 3.2, z = 0.32) => { const x = t - t0; if (x <= 0) return 0; const w = 2 * Math.PI * f, wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * x) * (Math.cos(wd * x) + (z * w / wd) * Math.sin(wd * x)); };

  /* the load the structure carries, as a multiple of the baseline (the pat + the ear poke) */
  function loadAt(t) {
    if (t < B.load + 0.05) return 0;
    if (t < T_BREAK) return LOAD_MAX * easeInOut((t - B.load - 0.05) / (T_BREAK - B.load - 0.05));
    if (t < B.rank + 0.35) return LOAD_MAX;
    return lerp(LOAD_MAX, 1.0, easeInOut((t - B.rank - 0.35) / 0.4));
  }
  const swapped = (t) => t >= B.swap + 0.32;

  function build(canvas, W, H) {
    const renderer = makeRenderer(canvas, W, H, { tone: "neutral", exposure: 0.9 });
    renderer.shadowMap.type = THREE.PCFShadowMap;
    const scene = new THREE.Scene();
    scene.background = S.studioBackdrop({ inner: "#22504a", mid: "#0d2627", outer: "#040b0c", cy: 0.4 });
    envFromGradient(renderer, scene, { top: 0x8fd6c4, horizon: 0xf4e8e0, ground: 0x1c2a28, sun: new THREE.Vector3(-0.6, 0.8, 0.7), sunColor: 0xfff1e6, sunPower: 2.5 });
    scene.environmentIntensity = 0.5;
    const camera = new THREE.PerspectiveCamera(30, W / H, 0.02, 20);

    /* light: a soft warm key, a cool sky fill, and two neon rims from the HUD's palette */
    const key = new THREE.DirectionalLight(0xfff3ea, 2.3); key.position.set(-0.55, 0.9, 0.85); key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024); key.shadow.camera.near = 0.1; key.shadow.camera.far = 3; key.shadow.radius = 6; key.shadow.bias = -0.0004;
    Object.assign(key.shadow.camera, { left: -0.3, right: 0.3, top: 0.45, bottom: -0.15 });
    scene.add(key, key.target);
    scene.add(new THREE.HemisphereLight(0xd8fff2, 0x1a2624, 0.32));
    const rimA = new THREE.SpotLight(0x9dffb4, 2.4, 3, 0.7, 0.6); rimA.position.set(0.55, 0.45, -0.6); rimA.target.position.set(0, 0.17, 0);
    const rimB = new THREE.SpotLight(0xffb8d0, 1.5, 3, 0.7, 0.6); rimB.position.set(-0.6, 0.35, -0.5); rimB.target.position.set(0, 0.17, 0);
    scene.add(rimA, rimA.target, rimB, rimB.target);

    /* the bunny */
    const t0 = performance.now();
    const bun = S.bunny({ cells: 136 });
    const sculptMs = Math.round(performance.now() - t0);
    const rig = new THREE.Group(); rig.add(bun.group); scene.add(rig);
    const stage = S.stageDisc({ radius: 0.24, color: 0x9dffb4, shadow: 0.5 }); scene.add(stage);
    const P = bun.parts;
    const restEar = { L: P.earL.rotation.clone(), R: P.earR.rotation.clone() };

    /* plush materials go x-ray during the analysis */
    const fadeMats = new Set();
    bun.group.traverse((m) => { if (m.isMesh) { const mats = Array.isArray(m.material) ? m.material : [m.material]; mats.forEach((x) => fadeMats.add(x)); } });
    fadeMats.forEach((m) => { m.transparent = true; m.userData.baseOpacity = m.opacity; });
    const setXray = (a) => fadeMats.forEach((m) => { m.opacity = a * (m.userData.baseOpacity == null ? 1 : m.userData.baseOpacity); m.depthWrite = a > 0.98; });

    /* SHAPE: a wireframe band scanning up the sculpt (same geometry, riding each part) */
    const wireMat = new THREE.ShaderMaterial({ wireframe: true, transparent: true, depthWrite: false, toneMapped: false,
      uniforms: { uScan: { value: -1 }, uAlpha: { value: 0 } },
      vertexShader: `varying float vY; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vY = w.y; gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `uniform float uScan, uAlpha; varying float vY;
        void main(){ float band = smoothstep(0.09, 0.0, uScan - vY) * step(vY, uScan + 0.004); float edge = smoothstep(0.012, 0.0, abs(vY - uScan));
          gl_FragColor = vec4(mix(vec3(0.62, 1.0, 0.72), vec3(0.95, 1.0, 0.8), edge), (band * 0.55 + edge) * uAlpha); }` });
    const sculpted = []; bun.group.traverse((m) => { if (m.isMesh && m.geometry.index && m.geometry.index.count > 3000) sculpted.push(m); });
    for (const m of sculpted) { const w = new THREE.Mesh(m.geometry, wireMat); w.renderOrder = 4; m.add(w); }   // collect first: adding while traversing recurses
    const scanRing = new THREE.Mesh(new THREE.RingGeometry(0.13, 0.136, 96), new THREE.MeshBasicMaterial({ color: 0xd0ff6a, transparent: true, opacity: 0, toneMapped: false, side: THREE.DoubleSide, depthWrite: false }));
    scanRing.rotation.x = -Math.PI / 2; scene.add(scanRing);

    /* the twin: nodes bound to their rig part (head, ears) so the truss bends with the bunny */
    rig.updateMatrixWorld(true);
    const partObj = { body: bun.group, head: P.head, earL: P.earL, earR: P.earR };
    const local = { nodes: {}, elements: TW.model.elements };
    const nodeParts = {}, inv = new THREE.Matrix4();
    for (const [id, p] of Object.entries(TW.model.nodes)) {
      const part = partObj[TW.parts[id]] || bun.group; nodeParts[id] = part;
      const v = new THREE.Vector3(p[0], p[1], p[2]).applyMatrix4(inv.copy(part.matrixWorld).invert()); local.nodes[id] = [v.x, v.y, v.z];
    }
    const twin = S.trussOverlay(local, { nodeParts, radius: 0.0015, jointRadius: 0.0032 }); scene.add(twin.group);
    const weak = TW.rank[0][0], weakNew = TW.rank_after[0][0];
    const order = Object.keys(TW.model.nodes).sort((a, b) => TW.model.nodes[a][1] - TW.model.nodes[b][1]);
    const popAt = {}; order.forEach((id, i) => { popAt[id] = B.joint + 0.04 + 0.42 * i / order.length; });
    const growAt = {}; for (const e of TW.model.elements) growAt[e.id] = Math.max(popAt[e.a], popAt[e.b]) + 0.03;

    /* load arrows: the pat on the crown, the poke at the left ear tip */
    const arrowMat = new THREE.MeshBasicMaterial({ color: 0xffe36b, transparent: true, opacity: 0, toneMapped: false, depthWrite: false });
    const makeArrow = (len) => { const g = new THREE.Group(); const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.0032, 0.0032, len, 12), arrowMat);
      shaft.position.y = len / 2 + 0.018; const head = new THREE.Mesh(new THREE.ConeGeometry(0.011, 0.022, 20), arrowMat); head.rotation.x = Math.PI; head.position.y = 0.011;
      g.add(shaft, head); g.renderOrder = 7; return g; };
    const arrowTop = makeArrow(0.075), arrowEar = makeArrow(0.05); scene.add(arrowTop, arrowEar);

    /* break sparks: deterministic, a function of the time since the snap */
    const sparkN = 26, sparkGeo = new THREE.BufferGeometry(), sparkPos = new Float32Array(sparkN * 3); sparkGeo.setAttribute("position", new THREE.BufferAttribute(sparkPos, 3));
    const sparks = new THREE.Points(sparkGeo, new THREE.PointsMaterial({ color: 0xffb08a, size: 0.0075, transparent: true, opacity: 0, toneMapped: false, depthWrite: false, map: window.K3.spriteTex("soft"), blending: THREE.AdditiveBlending }));
    scene.add(sparks); const R = window.K3.rng(7), sparkV = Array.from({ length: sparkN }, () => [(R() - 0.5) * 0.5, R() * 0.45 + 0.05, (R() - 0.5) * 0.5]);
    const flashRing = new THREE.Mesh(new THREE.TorusGeometry(1, 0.06, 8, 48), new THREE.MeshBasicMaterial({ color: 0xff907a, transparent: true, opacity: 0, toneMapped: false, depthWrite: false }));
    flashRing.renderOrder = 8; scene.add(flashRing);

    const post = S.makeLitePost(renderer, scene, camera, W, H, { bloom: 0.32, radius: 0.4, threshold: 0.93, vignette: 0.45, grain: 0.018 });
    const mid = new THREE.Vector3(), a = new THREE.Vector3(), b = new THREE.Vector3(), proj = new THREE.Vector3();
    const camP = new THREE.Vector3(), camL = new THREE.Vector3();

    function update(t) {
      const L = loadAt(t), sw = swapped(t);
      /* camera: an orbit that pushes in on the ear for the break, and pulls back for the rank */
      const ang = lerp(0.42, -0.3, easeInOut(t / B.end)) + 0.06 * Math.sin(t * 0.9);
      const push = smooth(B.load, B.brk + 0.1, t) * (1 - smooth(B.swap + 0.3, B.rank + 0.4, t));
      const endPull = smooth(B.rank, B.rank + 0.45, t);
      const dist = lerp(1.95, 1.8, push) + 0.08 * (1 - smooth(0, 1.0, t)) + 0.14 * endPull;
      const ly = lerp(0.112, 0.136, push) + 0.026 * endPull;
      camL.set(lerp(0, -0.035, push), ly, 0);
      camP.set(Math.sin(ang) * dist + camL.x, ly + lerp(0.2, 0.1, push), Math.cos(ang) * dist);
      const shake = Math.exp(-(t - T_BREAK) * 9) * (t > T_BREAK ? 1 : 0) * 0.006;
      camP.x += shake * Math.sin(t * 93); camP.y += shake * Math.cos(t * 71);
      camera.position.copy(camP); camera.lookAt(camL);

      /* the bunny: idle breath, squash under load, the hop at the end */
      const breath = 0.006 * Math.sin(t * 2 * Math.PI * 0.9);
      const sq = 0.045 * (L / LOAD_MAX) * (t < B.rank + 0.4 ? 1 : 0);
      const hopT = (t - (B.rank + 0.32)) / 0.42, hop = hopT > 0 && hopT < 1 ? Math.sin(Math.PI * hopT) * 0.026 : 0;
      const land = t > B.rank + 0.74 ? Math.exp(-(t - B.rank - 0.74) * 7) * Math.sin((t - B.rank - 0.74) * 30) * 0.05 : 0;
      rig.scale.set(1 + sq * 0.5 - land * 0.4, 1 - sq + breath + land, 1 + sq * 0.5 - land * 0.4);
      rig.position.y = hop;
      P.head.rotation.set(0.05 * Math.sin(t * 1.7) - 0.08 * (L / LOAD_MAX) + 0.1 * smooth(B.rank + 0.5, B.end, t), 0.12 * Math.sin(t * 1.1 + 0.5) * (1 - push), 0.05 * Math.sin(t * 1.3));
      P.tail.rotation.y = 0.25 * Math.sin(t * 9) * smooth(B.rank, B.rank + 0.3, t);
      /* ears: bend with the poke, flop when the root breaks, spring back after the swap, wiggle on the hop */
      const flop = spring(t, T_BREAK, 1.5, 0.42) * (1 - spring(t, B.swap + 0.32, 1.6, 0.5));
      const poke = 0.12 * (L / LOAD_MAX) * (t < T_BREAK ? 1 : 0);
      const wig = 0.16 * Math.sin((t - B.rank) * 18) * Math.exp(-Math.max(0, t - B.rank - 0.7) * 4) * smooth(B.rank + 0.6, B.rank + 0.7, t);
      P.earL.rotation.set(restEar.L.x + 0.55 * flop + 0.04 * Math.sin(t * 2.3), restEar.L.y, restEar.L.z + poke + 1.25 * flop + wig);
      P.earR.rotation.set(restEar.R.x + 0.04 * Math.sin(t * 2.1 + 1), restEar.R.y, restEar.R.z - 0.03 * (L / LOAD_MAX) - wig);
      // blink once, mid-film
      const bl = Math.max(smooth(1.18, 1.24, t) * (1 - smooth(1.26, 1.34, t)), smooth(4.62, 4.66, t) * (1 - smooth(4.68, 4.76, t)));
      for (const e of [P.eyeL, P.eyeR]) if (e) e.scale.set(1, 1 - 0.85 * bl, 1);

      /* SHAPE scan */
      const scanY = lerp(-0.02, 0.4, easeInOut((t - 0.12) / 0.78));
      wireMat.uniforms.uScan.value = scanY; wireMat.uniforms.uAlpha.value = smooth(0.08, 0.2, t) * (1 - smooth(0.88, 1.05, t));
      scanRing.position.y = scanY; scanRing.material.opacity = wireMat.uniforms.uAlpha.value * 0.9; scanRing.scale.setScalar(lerp(1.15, 0.6, clamp01(scanY / 0.36)));
      stage.userData.mat.uniforms.uScan.value = ((t * 0.75) % 1.25); stage.userData.mat.uniforms.uAlpha.value = 0.55 + 0.45 * smooth(0, 0.4, t);

      /* x-ray during the analysis */
      const xr = smooth(B.joint - 0.05, B.joint + 0.3, t) * (1 - smooth(B.rank + 0.05, B.rank + 0.42, t));
      setXray(1 - 0.66 * xr);

      /* the twin */
      for (const [id, j] of Object.entries(twin.joints)) j.userData.pop = spring(t, popAt[id], 4.2, 0.38);
      for (const [id, m] of Object.entries(twin.members)) {
        m.userData.grow = easeOut((t - growAt[id]) / 0.22);
        if (id === weak) {
          m.userData.hidden = t >= T_BREAK && t < B.swap + 0.12;
          const ins = easeOut((t - B.swap - 0.12) / 0.3);
          m.userData.thick = t >= B.swap + 0.12 ? lerp(3.2, 1.7, ins) : 1 + 0.6 * smooth(T_BREAK - 0.3, T_BREAK, t);
        }
      }
      const twinAlpha = smooth(B.joint, B.joint + 0.15, t) * (1 - 0.9 * smooth(B.rank + 0.15, B.rank + 0.5, t));
      twin.update({ alpha: twinAlpha, jointAlpha: twinAlpha, camera,
        utilOf: (id) => { if (t < B.load) return 0.12; return (sw ? TW.util_after[id] : TW.util[id]) * L; },
        flash: (id) => (id === weak ? Math.max(Math.exp(-Math.max(0, t - T_BREAK + 0.25) * 6) * smooth(T_BREAK - 0.3, T_BREAK - 0.25, t), Math.exp(-Math.max(0, t - B.swap - 0.12) * 5) * (t > B.swap + 0.12 ? 1 : 0)) : 0) });

      /* arrows */
      const arA = smooth(B.load - 0.05, B.load + 0.15, t) * (1 - smooth(B.rank + 0.05, B.rank + 0.3, t));
      arrowMat.opacity = arA; arrowMat.color.setHSL(lerp(0.14, 0.02, clamp01((L - 1.5) / 1.5)), 1, 0.62);
      twin.worldOf("crown", a); arrowTop.position.copy(a).add(new THREE.Vector3(0, 0.012 + 0.03 * (1 - smooth(B.load, B.load + 0.25, t)) - 0.006 * L / LOAD_MAX, 0));
      arrowTop.scale.setScalar(0.8 + 0.25 * L / LOAD_MAX);
      twin.worldOf("earL_tip", b); arrowEar.position.copy(b).add(new THREE.Vector3(0.008, 0, 0)); arrowEar.rotation.set(0, 0, -Math.PI / 2);
      arrowEar.scale.setScalar((0.7 + 0.3 * L / LOAD_MAX) * (t < T_BREAK + 0.15 ? 1 : 1 - smooth(T_BREAK + 0.15, T_BREAK + 0.35, t)));

      /* the snap */
      twin.worldOf(TW.model.elements.find((e) => e.id === weak).a, a); twin.worldOf(TW.model.elements.find((e) => e.id === weak).b, b);
      mid.addVectors(a, b).multiplyScalar(0.5);
      const ts = t - T_BREAK;
      sparks.material.opacity = ts > 0 ? Math.max(0, 1 - ts / 0.6) : 0;
      for (let i = 0; i < sparkN; i++) { const v = sparkV[i], k = Math.max(0, ts);
        sparkPos[i * 3] = mid.x + v[0] * k; sparkPos[i * 3 + 1] = mid.y + v[1] * k - 0.9 * k * k; sparkPos[i * 3 + 2] = mid.z + v[2] * k; }
      sparkGeo.attributes.position.needsUpdate = true;
      const fr = ts > 0 ? clamp01(ts / 0.4) : (t > B.swap + 0.12 ? clamp01((t - B.swap - 0.12) / 0.45) : 0);
      const swapRing = t > B.swap + 0.12;
      flashRing.material.color.set(swapRing ? 0x9dffb4 : 0xff907a);
      flashRing.position.copy(mid); flashRing.quaternion.copy(camera.quaternion); flashRing.scale.setScalar(0.004 + 0.04 * easeOut(fr));
      flashRing.material.opacity = (ts > 0 && ts < 0.4) || (swapRing && t < B.swap + 0.57) ? 1 - fr : 0;

      /* the HUD reads the 3D: where the weak member is on screen */
      camera.updateMatrixWorld(true);                         // project with THIS frame's camera (frames render in any order)
      proj.copy(mid).project(camera);
      window.__hud && window.__hud(t, { L, sw, peak: peakUtil(L, sw), sx: (proj.x * 0.5 + 0.5) * W, sy: (-proj.y * 0.5 + 0.5) * H });
    }
    const peakUtil = (L, sw) => { const u = sw ? TW.util_after : TW.util; let m = 0; for (const k in u) m = Math.max(m, u[k]); return m * L; };
    const render = makeFrameLoop(renderer, post, W, H, update);
    window.__bunnyStats = { triangles: bun.stats.triangles, sculpt_ms: sculptMs, body: bun.stats.body, head: bun.stats.head };
    return { render, ready: Promise.resolve(), scene, camera, renderer };
  }
  window.__three = { build };
})();
