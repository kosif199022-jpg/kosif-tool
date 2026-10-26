/* KOSIF lab-kit — the "product lab" look on top of the three-kit (loads after three-kit.bundle.js, extends window.K3).
   Learned from the 2026 "3D schematic" wave: one fuzzy hero object on a cream studio sweep, a lens that walks the whole
   circle and stops at parts, extreme close-ups with dashed callouts and tiny measurement cards, an instrument-panel
   HUD (title strip, timeline, charts) framing the picture. Everything is deterministic: seeded noise, no clocks, every
   value a function of t.
   Blocks: shell fur · glossy eyes · procedural characters (rabbit, lion) with named joints · schematic modes (wire,
   exploded, joint markers) · orbit walk with stops · studio sweep + rig · HUD with projected callouts and charts. */
(function () {
  const K3 = window.K3;
  if (!K3 || !K3.THREE) throw new Error("lab-kit needs three-kit.bundle.js loaded first (window.K3)");
  const THREE = K3.THREE, rng = K3.rng, lerp = K3.lerp, smooth = K3.smooth, clamp01 = K3.clamp01;
  const ease = (x) => x * x * (3 - 2 * x);

  /* ───────── materials ───────── */
  let _furTex = null;
  function furAlphaTex(seed = 11, N = 256, density = 0.55) {        // white dots on black: each dot is one hair's cross-section
    if (_furTex) return _furTex;
    const c = document.createElement("canvas"); c.width = c.height = N;
    const g = c.getContext("2d"), r = rng(seed);
    g.fillStyle = "#000"; g.fillRect(0, 0, N, N);
    const n = Math.round(N * N * density * 0.09);
    for (let i = 0; i < n; i++) { const x = r() * N, y = r() * N, s = 0.5 + r() * 1.1, v = 150 + r() * 105;
      g.fillStyle = `rgb(${v},${v},${v})`; g.beginPath(); g.arc(x, y, s, 0, 6.283); g.fill(); }
    _furTex = new THREE.CanvasTexture(c); _furTex.wrapS = _furTex.wrapT = THREE.RepeatWrapping; return _furTex;
  }
  /* Shell fur: `layers` copies of the mesh pushed along the normal, each keeping fewer hairs (alphaTest rises), roots
     darker than tips, a little gravity. 8–12 layers read as plush at 540p; 16 at 1080p. */
  function makeFur(mesh, o = {}) {
    const layers = o.layers || 10, length = o.length || 0.12, repeat = o.repeat || 14, base = new THREE.Color(o.color || 0xa7ff2a), root = o.rootShade == null ? 0.72 : o.rootShade;
    const tex = furAlphaTex(o.seed || 11, 256, o.density || 0.55);
    const group = new THREE.Group(); group.name = (mesh.name || "part") + "_fur";
    for (let i = 1; i <= layers; i++) {
      const s = i / layers;
      const mat = new THREE.MeshStandardMaterial({ color: base.clone().multiplyScalar(root + (1 - root) * s), roughness: 0.92, metalness: 0,
        alphaMap: tex, transparent: false, alphaTest: 0.1 + 0.68 * s, side: THREE.DoubleSide, depthWrite: true });
      mat.alphaMap.repeat.set(repeat, repeat);
      mat.onBeforeCompile = (sh) => {
        sh.uniforms.uShell = { value: s * length }; sh.uniforms.uGrav = { value: (o.gravity == null ? 0.35 : o.gravity) * length * s * s };
        sh.vertexShader = "uniform float uShell; uniform float uGrav;\n" + sh.vertexShader.replace("#include <begin_vertex>",
          "#include <begin_vertex>\n transformed += normal * uShell; transformed.y -= uGrav;");
      };
      mat.customProgramCacheKey = () => "fur" + i;
      const m = new THREE.Mesh(mesh.geometry, mat); m.castShadow = false; m.receiveShadow = true; group.add(m);
    }
    mesh.add(group);
    mesh.userData.fur = group;
    return group;
  }
  function plushMaterial(color) { return new THREE.MeshStandardMaterial({ color, roughness: 0.95, metalness: 0 }); }
  function glossMaterial(color, o = {}) { return new THREE.MeshPhysicalMaterial({ color, roughness: o.roughness == null ? 0.08 : o.roughness, metalness: 0,
    clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 1.2 }); }
  function leatherMaterial(color = 0x15171a) { return new THREE.MeshStandardMaterial({ color, roughness: 0.55, metalness: 0.05 }); }
  function metalMaterial(color = 0xd8dde3) { return new THREE.MeshStandardMaterial({ color, roughness: 0.25, metalness: 0.95 }); }

  /* ───────── eyes ───────── */
  function makeEye(r, o = {}) {
    const g = new THREE.Group(); g.name = "eye";
    const sclera = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 24), new THREE.MeshStandardMaterial({ color: 0xf4f6f2, roughness: 0.35 }));
    const iris = new THREE.Mesh(new THREE.SphereGeometry(r * 0.56, 32, 24), new THREE.MeshStandardMaterial({ color: o.iris || 0x8fe02a, roughness: 0.5, emissive: new THREE.Color(o.iris || 0x8fe02a).multiplyScalar(0.12) }));
    iris.scale.set(1, 1, 0.45); iris.position.z = r * 0.72;
    const pupil = new THREE.Mesh(new THREE.SphereGeometry(r * 0.3, 24, 16), new THREE.MeshStandardMaterial({ color: 0x05070a, roughness: 0.4 }));
    pupil.scale.set(1, 1, 0.5); pupil.position.z = r * 0.9;
    const cornea = new THREE.Mesh(new THREE.SphereGeometry(r * 1.02, 32, 24), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.22,
      roughness: 0.02, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.02, depthWrite: false }));
    g.add(sclera, iris, pupil, cornea);
    g.userData.blink = (k) => { g.scale.y = 1 - 0.92 * k; };    // k 0..1
    return g;
  }

  /* ───────── characters: groups with named joints (pivot groups) and parts (meshes) ───────── */
  function part(geo, mat, name, pos = [0, 0, 0]) { const m = new THREE.Mesh(geo, mat); m.name = name; m.position.set(...pos); m.castShadow = true; m.receiveShadow = true; return m; }
  function joint(name, pos = [0, 0, 0]) { const g = new THREE.Group(); g.name = name; g.position.set(...pos); g.userData.joint = true; return g; }

  function makeRabbit(o = {}) {
    const C = o.color || 0xf1f0ea, inner = o.inner || 0xf3b6c0, iris = o.iris || 0x3a7bd5, fur = o.fur !== false, L = o.furLength || 0.1;
    const root = new THREE.Group(); root.name = "rabbit";
    const J = {};
    const body = part(new THREE.SphereGeometry(0.62, 40, 30), plushMaterial(C), "body", [0, 0.62, 0]); body.scale.set(1, 1.1, 0.9); root.add(body);
    J.head = joint("head", [0, 1.28, 0.05]); root.add(J.head);
    const head = part(new THREE.SphereGeometry(0.5, 40, 30), plushMaterial(C), "head", [0, 0.3, 0]); head.scale.set(1.05, 0.95, 1); J.head.add(head);
    const muzzle = part(new THREE.SphereGeometry(0.22, 24, 18), plushMaterial(0xffffff), "muzzle", [0, 0.18, 0.42]); muzzle.scale.set(1.3, 0.8, 0.8); J.head.add(muzzle);
    const nose = part(new THREE.SphereGeometry(0.06, 16, 12), glossMaterial(inner, { roughness: 0.3 }), "nose", [0, 0.26, 0.58]); J.head.add(nose);
    ["L", "R"].forEach((side, i) => {
      const sx = i ? -1 : 1;
      J["ear" + side] = joint("ear" + side, [sx * 0.2, 0.68, -0.05]);
      const ear = part(new THREE.CapsuleGeometry(0.11, 0.62, 8, 20), plushMaterial(C), "ear" + side, [0, 0.38, 0]); ear.scale.set(1, 1, 0.55);
      const earIn = part(new THREE.CapsuleGeometry(0.06, 0.5, 6, 16), plushMaterial(inner), "earInner" + side, [0, 0.38, 0.06]); earIn.scale.set(1, 1, 0.4);
      J["ear" + side].add(ear, earIn); J["ear" + side].rotation.z = sx * -0.16; J.head.add(J["ear" + side]);
      const eye = makeEye(0.1, { iris }); eye.position.set(sx * 0.19, 0.34, 0.41); eye.rotation.y = sx * 0.08; eye.name = "eye" + side; J.head.add(eye); J["eye" + side] = eye;
      J["arm" + side] = joint("arm" + side, [sx * 0.5, 0.78, 0.15]);
      const arm = part(new THREE.CapsuleGeometry(0.11, 0.34, 8, 16), plushMaterial(C), "arm" + side, [0, -0.2, 0]); J["arm" + side].add(arm); J["arm" + side].rotation.z = sx * 0.6; root.add(J["arm" + side]);
      J["foot" + side] = joint("foot" + side, [sx * 0.3, 0.14, 0.25]);
      const foot = part(new THREE.CapsuleGeometry(0.14, 0.36, 8, 16), plushMaterial(C), "foot" + side, [0, 0, 0.1]); foot.rotation.x = Math.PI / 2; J["foot" + side].add(foot); root.add(J["foot" + side]);
    });
    J.tail = joint("tail", [0, 0.5, -0.56]); J.tail.add(part(new THREE.SphereGeometry(0.16, 20, 14), plushMaterial(0xffffff), "tail")); root.add(J.tail);
    if (fur) root.traverse((m) => { if (m.isMesh && /^(body|head|arm|foot|ear[LR]$|tail)/.test(m.name) && !m.name.startsWith("earInner")) makeFur(m, { color: m.material.color.getHex(), length: L, layers: o.layers || 8, seed: 11 }); });
    root.userData.joints = J; root.userData.kind = "rabbit";
    return root;
  }

  function makeLion(o = {}) {
    const C = o.color || 0xe3b05a, mane = o.mane || 0x8a4a1c, iris = o.iris || 0xd9a21b, fur = o.fur !== false, L = o.furLength || 0.08;
    const root = new THREE.Group(); root.name = "lion";
    const J = {};
    const body = part(new THREE.CapsuleGeometry(0.55, 0.9, 10, 28), plushMaterial(C), "body", [0, 0.9, 0]); body.rotation.x = Math.PI / 2; root.add(body);
    J.head = joint("head", [0, 1.25, 0.75]); root.add(J.head);
    const maneM = part(new THREE.SphereGeometry(0.78, 40, 30), plushMaterial(mane), "mane", [0, 0.05, -0.15]); maneM.scale.set(1, 1, 0.75); J.head.add(maneM);
    const head = part(new THREE.SphereGeometry(0.5, 40, 30), plushMaterial(C), "head", [0, 0.1, 0.25]); J.head.add(head);
    const muzzle = part(new THREE.SphereGeometry(0.26, 24, 18), plushMaterial(0xf5e2b8), "muzzle", [0, -0.05, 0.62]); muzzle.scale.set(1.25, 0.8, 0.8); J.head.add(muzzle);
    const nose = part(new THREE.SphereGeometry(0.08, 16, 12), glossMaterial(0x2b1d16, { roughness: 0.35 }), "nose", [0, 0.06, 0.82]); nose.scale.set(1.3, 0.8, 0.8); J.head.add(nose);
    ["L", "R"].forEach((side, i) => {
      const sx = i ? -1 : 1;
      J["ear" + side] = joint("ear" + side, [sx * 0.42, 0.5, 0.05]);
      J["ear" + side].add(part(new THREE.SphereGeometry(0.15, 18, 12), plushMaterial(C), "ear" + side), part(new THREE.SphereGeometry(0.08, 14, 10), plushMaterial(0xf3b6c0), "earInner" + side, [0, 0, 0.09]));
      J.head.add(J["ear" + side]);
      const eye = makeEye(0.1, { iris }); eye.position.set(sx * 0.2, 0.2, 0.66); eye.rotation.y = sx * 0.06; eye.name = "eye" + side; J.head.add(eye); J["eye" + side] = eye;
      J["legF" + side] = joint("legF" + side, [sx * 0.36, 0.72, 0.5]);
      J["legF" + side].add(part(new THREE.CapsuleGeometry(0.14, 0.5, 8, 16), plushMaterial(C), "legF" + side, [0, -0.33, 0])); root.add(J["legF" + side]);
      J["legB" + side] = joint("legB" + side, [sx * 0.38, 0.7, -0.55]);
      J["legB" + side].add(part(new THREE.CapsuleGeometry(0.16, 0.46, 8, 16), plushMaterial(C), "legB" + side, [0, -0.33, 0])); root.add(J["legB" + side]);
    });
    J.tail = joint("tail", [0, 1.05, -0.95]);
    const tail = part(new THREE.CapsuleGeometry(0.05, 0.9, 6, 12), plushMaterial(C), "tail", [0, 0.2, -0.3]); tail.rotation.x = -0.7;
    const tuft = part(new THREE.SphereGeometry(0.13, 16, 12), plushMaterial(mane), "tuft", [0, 0.6, -0.62]);
    J.tail.add(tail, tuft); root.add(J.tail);
    if (fur) root.traverse((m) => { if (m.isMesh && /^(mane|tuft)$/.test(m.name)) makeFur(m, { color: m.material.color.getHex(), length: L * 2.6, layers: o.layers || 10, seed: 23, gravity: 0.5 });
      else if (m.isMesh && /^(body|head|leg|ear[LR]$)/.test(m.name)) makeFur(m, { color: m.material.color.getHex(), length: L, layers: Math.max(5, (o.layers || 10) - 3), seed: 29 }); });
    root.userData.joints = J; root.userData.kind = "lion";
    return root;
  }

  /* ───────── schematic modes ───────── */
  /* Every part gets a hidden edge overlay (lime lines) and remembers its rest position; `schematic.set(amount)` fades
     fur/solids toward wireframe, `explode(k)` pushes parts away from the body, `joints(k)` shows dashed rings at pivots. */
  function schematic(root, o = {}) {
    const color = new THREE.Color(o.color || 0xa8ff3c);
    const lineMat = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0 });
    const ghostMat = new THREE.MeshBasicMaterial({ color: o.ghost || 0xf7f8f2, transparent: true, opacity: 0, depthWrite: false });
    const maxLine = o.lineOpacity == null ? 0.42 : o.lineOpacity;
    const items = [], meshes = [], pivots = [];
    root.traverse((m) => { if (m.isMesh && !m.parent?.name?.endsWith("_fur") && m.parent?.name !== "eye") meshes.push(m); if (m.userData.joint) pivots.push(m); });
    meshes.forEach((m) => {                                    // (collected first: adding children while traversing recurses forever)
      const edges = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry, o.angle == null ? 1 : o.angle), lineMat); edges.name = m.name + "_edges"; edges.renderOrder = 5;
      const ghost = new THREE.Mesh(m.geometry, ghostMat); ghost.name = m.name + "_ghost"; ghost.renderOrder = 4;
      m.add(edges, ghost);
      items.push({ mesh: m, mats: [], edges, ghost });
      const it = items[items.length - 1]; it.mats.push(m.material);
      if (m.userData.fur) m.userData.fur.children.forEach((x) => it.mats.push(x.material));
      it.mats.forEach((mat) => { if (mat.userData.__op == null) mat.userData.__op = mat.opacity; });
    });
    const joints = [];
    pivots.forEach((g) => { { const ring = new THREE.Mesh(new THREE.RingGeometry(0.1, 0.125, 40, 1), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, side: THREE.DoubleSide, depthTest: false }));
      ring.renderOrder = 10; const dot = new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 8), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, depthTest: false })); dot.renderOrder = 10;
      g.add(ring, dot); g.userData.rest = g.position.clone(); joints.push({ g, ring, dot }); } });
    const camDir = new THREE.Vector3();
    return {
      set(k, camera) {                                      // 0 = plush, 1 = full schematic
        k = clamp01(k); lineMat.opacity = maxLine * ease(k); ghostMat.opacity = 0.55 * ease(k);
        items.forEach((it) => it.mats.forEach((mat) => { if (!mat.transparent) { mat.transparent = true; } mat.opacity = (mat.userData.__op == null ? 1 : mat.userData.__op) * (1 - 0.92 * ease(k)); mat.depthWrite = k < 0.5; }));
        if (camera) { camera.getWorldDirection(camDir); joints.forEach((j) => { const wp = j.ring.getWorldPosition(new THREE.Vector3()); j.ring.lookAt(wp.clone().sub(camDir));
          const sc = Math.max(0.25, wp.distanceTo(camera.position) * 0.33); j.ring.scale.setScalar(sc); j.dot.scale.setScalar(sc); }); }
      },
      explode(k) { k = clamp01(k); joints.forEach((j) => { const r = j.g.userData.rest; j.g.position.set(r.x * (1 + 1.1 * k), r.y + (r.y - 0.9) * 0.6 * k, r.z * (1 + 1.1 * k)); }); },
      joints(k) { k = clamp01(k); joints.forEach((j) => { j.ring.material.opacity = k; j.dot.material.opacity = k; }); },
      items, jointList: joints,
    };
  }

  /* ───────── camera: a lens that walks the circle and stops at parts ───────── */
  /* stops: [{t, angle (deg), dist, height, look: [x,y,z] | object3d, hold}] — between stops the camera eases; at a stop it
     holds (micro drift so nothing freezes). Returns (t) => sets camera; and .look(t) for DOF. */
  function orbitWalk(camera, stops, o = {}) {
    const S = stops.map((s) => ({ ...s, look: Array.isArray(s.look) ? new THREE.Vector3(...s.look) : s.look }));
    const drift = o.drift == null ? 0.012 : o.drift, tmp = new THREE.Vector3(), look = new THREE.Vector3();
    function lookOf(i) { const s = S[i]; return s.look.isObject3D ? s.look.getWorldPosition(look.clone()) : s.look.clone(); }
    const fn = function (t) {
      let i = 0; while (i < S.length - 1 && t >= S[i + 1].t) i++;
      const a = S[i], b = S[Math.min(i + 1, S.length - 1)];
      const hold = a.hold || 0, span = Math.max(1e-3, b.t - a.t - hold);
      const k = a === b ? 0 : ease(clamp01((t - a.t - hold) / span));
      // walk the shorter way round the circle
      let da = b.angle - a.angle; da = ((da + 540) % 360) - 180;
      const ang = (a.angle + da * k) * Math.PI / 180, dist = lerp(a.dist, b.dist, k), h = lerp(a.height, b.height, k);
      tmp.copy(lookOf(i)).lerp(lookOf(Math.min(i + 1, S.length - 1)), k);          // the circle is walked around the thing being looked at
      camera.position.set(tmp.x + Math.sin(ang) * dist + drift * Math.sin(t * 0.7), h + drift * Math.cos(t * 0.9), tmp.z + Math.cos(ang) * dist);
      camera.lookAt(tmp); fn.lookPoint.copy(tmp); fn.fov = lerp(a.fov || o.fov || 32, b.fov || o.fov || 32, k);
      if (camera.fov !== fn.fov) { camera.fov = fn.fov; camera.updateProjectionMatrix(); }
    };
    fn.lookPoint = new THREE.Vector3(); fn.stops = S;
    return fn;
  }

  /* ───────── the studio: a cream sweep, a soft three-light rig, a contact shadow, a faint grid ───────── */
  function studio(scene, o = {}) {
    const bg = new THREE.Color(o.bg || 0xf1efe8); scene.background = bg;
    const sweep = new THREE.Mesh(new THREE.SphereGeometry(40, 32, 16), new THREE.MeshBasicMaterial({ color: bg, side: THREE.BackSide })); sweep.position.y = 10; scene.add(sweep);
    const floor = new THREE.Mesh(new THREE.CircleGeometry(30, 48), new THREE.ShadowMaterial({ opacity: 0.22 })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
    const grid = new THREE.GridHelper(16, 32, o.grid || 0xc9d8c2, o.grid || 0xd9e4d4); grid.material.transparent = true; grid.material.opacity = 0.35; grid.position.y = 0.002; scene.add(grid);
    const key = new THREE.DirectionalLight(0xffffff, 2.6); key.position.set(3, 6, 4); key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.camera.left = -4; key.shadow.camera.right = 4; key.shadow.camera.top = 4; key.shadow.camera.bottom = -4; key.shadow.radius = 4; key.shadow.bias = -0.0004; scene.add(key);
    const fill = new THREE.DirectionalLight(0xdfe8ff, 0.9); fill.position.set(-5, 3, 2); scene.add(fill);
    const rim = new THREE.DirectionalLight(0xffffff, 1.4); rim.position.set(-2, 4, -5); scene.add(rim);
    scene.add(new THREE.HemisphereLight(0xffffff, 0xcfd8c8, 0.9));
    return { sweep, floor, grid, key, fill, rim };
  }

  /* ───────── HUD: the instrument panel around the picture, with callouts projected from 3D ───────── */
  function hud(root, W, H, o = {}) {
    const lime = o.accent || "#a8ff3c", ink = o.ink || "#0f1512", paper = o.paper || "#f4f2ec";
    const el = document.createElement("div"); el.id = "lab-hud";
    el.style.cssText = `position:absolute;inset:0;pointer-events:none;font-family:${o.font || '"IBM Plex Mono","Consolas","Courier New",monospace'};color:${ink};direction:ltr`;
    const top = H * 0.085, bottom = H * 0.2, side = W * 0.03;
    el.innerHTML = `
<div id="hud-top" style="position:absolute;left:0;right:0;top:0;height:${top}px;background:${paper};border-bottom:1px solid #d9d6cc;display:flex;align-items:center;gap:${W * 0.02}px;padding:0 ${side}px;font-size:${Math.round(H * 0.018)}px;letter-spacing:.06em;text-transform:uppercase">
  <span style="font-weight:700">${o.title || "KOSIF LAB"}</span><span style="opacity:.55">${o.subtitle || ""}</span>
  <span style="margin-left:auto;display:flex;gap:${W * 0.015}px"><span id="hud-stage" style="background:${ink};color:${lime};padding:2px 8px;border-radius:3px">SHAPE</span><span id="hud-clock" style="opacity:.6">00:00.00</span></span></div>
<div id="hud-strip" style="position:absolute;left:${side}px;right:${side}px;top:${top + 6}px;height:${H * 0.05}px;display:flex;align-items:flex-end;gap:2px"></div>
<div id="hud-bottom" style="position:absolute;left:0;right:0;bottom:0;height:${bottom}px;background:${paper};border-top:1px solid #d9d6cc;display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:${W * 0.012}px;padding:${H * 0.015}px ${side}px;font-size:${Math.round(H * 0.016)}px"></div>
<div id="hud-side" style="position:absolute;left:${side}px;top:${top + H * 0.07}px;font-size:${Math.round(H * 0.016)}px;line-height:1.5;opacity:.85"></div>
<div id="hud-callouts" style="position:absolute;inset:0"></div>
<div id="hud-frame" style="position:absolute;left:${side}px;right:${side}px;top:${top + H * 0.062}px;bottom:${bottom + H * 0.012}px;border:1px solid rgba(15,21,18,.18);border-radius:6px"></div>`;
    root.appendChild(el);
    const strip = el.querySelector("#hud-strip"), r = rng(o.seed || 5), bars = [];
    const nBars = Math.round(W / 7);
    for (let i = 0; i < nBars; i++) { const b = document.createElement("div"); const h = 20 + 80 * Math.pow(r(), 1.6); b.style.cssText = `flex:1;height:${h}%;background:#cfd3c7`; strip.appendChild(b); bars.push(b); }
    const bottomEl = el.querySelector("#hud-bottom");
    const panels = (o.panels || [["STOP BELT", "stops · hold time"], ["HOLD RATE", "what a stop buys"], ["FAR SIDE", "seen from behind"]]).map(([t, s]) => {
      const p = document.createElement("div"); p.style.cssText = "border:1px solid #d9d6cc;border-radius:6px;padding:8px 10px;background:#fbfaf6;overflow:hidden;position:relative";
      p.innerHTML = `<div style="font-weight:700;letter-spacing:.08em;font-size:.95em">${t} <span style="font-weight:400;opacity:.55;margin-left:8px">${s}</span></div><svg viewBox="0 0 200 48" preserveAspectRatio="none" style="width:100%;height:60%;margin-top:6px;display:block"></svg>`;
      bottomEl.appendChild(p); return p.querySelector("svg");
    });
    const callouts = [], clockEl = el.querySelector("#hud-clock"), stageEl = el.querySelector("#hud-stage"), sideEl = el.querySelector("#hud-side");
    const v = new THREE.Vector3();
    function addCallout(spec) {                               // {anchor: object3d | [x,y,z], label, title, text, side: "left"|"right", radius}
      const c = document.createElement("div"); c.style.cssText = "position:absolute;left:0;top:0;opacity:0;will-change:transform";
      const rad = spec.radius || Math.round(H * 0.045);
      c.innerHTML = `<div class="co-ring" style="position:absolute;width:${rad * 2}px;height:${rad * 2}px;left:${-rad}px;top:${-rad}px;border:2px dashed ${lime};border-radius:50%;box-shadow:0 0 0 1px rgba(0,0,0,.25) inset"></div>
<svg class="co-lead" style="position:absolute;left:0;top:0;overflow:visible;width:1px;height:1px"><path d="" fill="none" stroke="${ink}" stroke-width="1.5"/></svg>
<div class="co-card" style="position:absolute;min-width:${W * 0.14}px;max-width:${W * 0.22}px;background:${paper};color:${ink};border:1px solid #cfccc2;border-radius:5px;padding:8px 10px;font-size:${Math.round(H * 0.017)}px;line-height:1.35;box-shadow:0 6px 18px rgba(0,0,0,.12)">
  <div style="font-size:.78em;letter-spacing:.1em;opacity:.55">${spec.label || ""}</div><div style="font-weight:700;margin:2px 0">${spec.title || ""}</div><div style="opacity:.8">${spec.text || ""}</div></div>
<div class="co-meas" style="position:absolute;background:${ink};color:${lime};padding:2px 7px;border-radius:3px;font-size:${Math.round(H * 0.017)}px;font-variant-numeric:tabular-nums"></div>`;
      el.querySelector("#hud-callouts").appendChild(c);
      const item = { el: c, spec, show: 0, rad };
      callouts.push(item); return item;
    }
    function update(t, camera, state = {}) {
      clockEl.textContent = `${String(Math.floor(t / 60)).padStart(2, "0")}:${(t % 60).toFixed(2).padStart(5, "0")}`;
      if (state.stage) stageEl.textContent = state.stage;
      if (state.side != null) sideEl.innerHTML = state.side;
      const pos = Math.floor(clamp01(t / (state.duration || 30)) * bars.length);
      bars.forEach((b, i) => { b.style.background = i < pos ? lime : i === pos ? ink : "#cfd3c7"; });
      // charts: deterministic curves that move with t
      panels.forEach((svg, k) => { const pts = []; for (let i = 0; i <= 40; i++) { const x = i / 40; const y = k === 0 ? (x < clamp01(t / (state.duration || 30)) ? 36 - 26 * Math.pow(x, 0.7) : 44) : k === 1 ? 24 + 14 * Math.sin(x * 25 + t * 1.3) * Math.exp(-x * 0.6) : 40 - 30 * ease(clamp01((x - 0.2) * 1.4)) * (0.6 + 0.4 * Math.sin(t * 0.5)); pts.push(`${(x * 200).toFixed(1)},${y.toFixed(1)}`); }
        svg.innerHTML = `<polyline points="${pts.join(" ")}" fill="none" stroke="${k === 1 ? ink : lime}" stroke-width="2"/>` + (k === 0 ? `<rect x="0" y="40" width="${(clamp01(t / (state.duration || 30)) * 200).toFixed(1)}" height="8" fill="${lime}" opacity=".6"/>` : ""); });
      callouts.forEach((c) => {
        const a = c.spec.anchor; if (a && a.isObject3D) a.getWorldPosition(v); else v.set(...a);
        v.project(camera); const x = (v.x + 1) / 2 * W, y = (1 - v.y) / 2 * H, inView = v.z < 1 && x > 0 && x < W && y > 0 && y < H;
        const s = c.show * (inView ? 1 : 0);
        c.el.style.opacity = s.toFixed(3); c.el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`;
        const dir = c.spec.side === "left" ? -1 : 1, dx = dir * (W * 0.09), dy = -H * 0.14;
        const card = c.el.querySelector(".co-card"), lead = c.el.querySelector(".co-lead path"), meas = c.el.querySelector(".co-meas"), ring = c.el.querySelector(".co-ring");
        card.style.left = (dir > 0 ? dx + 18 : dx - 18 - W * 0.2) + "px"; card.style.top = dy + "px";
        ring.style.transform = `scale(${0.6 + 0.4 * ease(s)})`;
        const L = ease(s); lead.setAttribute("d", `M ${(dir * c.rad * 0.72).toFixed(1)} ${(-c.rad * 0.72).toFixed(1)} L ${(dx * L).toFixed(1)} ${(dy * L + 10).toFixed(1)} l ${(dir * 18 * L).toFixed(1)} 0`);
        meas.style.left = (dir > 0 ? -c.rad - 60 : c.rad + 10) + "px"; meas.style.top = (c.rad * 0.4) + "px";
        meas.textContent = c.spec.measure ? c.spec.measure(t) : "";
      });
    }
    return { el, addCallout, update, callouts };
  }

  /* ───────── a lightweight post for the lab (bloom/rays/DOF off: fast on software GL) ───────── */
  function labPost(renderer, scene, camera, W, H, o = {}) {
    const post = K3.makePost(renderer, scene, camera, W, H, { bloom: o.bloom == null ? 0.08 : o.bloom, bloomThreshold: 0.95, grain: o.grain == null ? 0.05 : o.grain, vignette: o.vignette == null ? 0.18 : o.vignette, ca: 0.4 });
    post.rays.enabled = false; post.bokeh.enabled = o.dof === true; if (o.bloom === 0) post.bloom.enabled = false;
    post.grade.uniforms.uWarm.value = 0.25;
    return post;
  }

  /* ───────── simple idle animation for a character: breath, blink, ear/tail life ───────── */
  function idle(root, t, o = {}) {
    const J = root.userData.joints, k = o.amount == null ? 1 : o.amount, ph = o.phase || 0;
    root.scale.setScalar(1 + 0.012 * k * Math.sin(t * 2.2 + ph));
    if (J.head) J.head.rotation.set(0.04 * k * Math.sin(t * 1.1 + ph), 0.08 * k * Math.sin(t * 0.7 + ph), 0.03 * k * Math.sin(t * 1.7 + ph));
    const blink = (() => { const c = (t + ph) % 3.7; return c > 3.4 ? Math.sin((c - 3.4) / 0.3 * Math.PI) : 0; })();
    ["eyeL", "eyeR"].forEach((e) => J[e] && J[e].userData.blink(blink));
    ["earL", "earR"].forEach((e, i) => { if (J[e]) J[e].rotation.x = 0.12 * k * Math.sin(t * 2.6 + i * 1.3 + ph); });
    if (J.tail) J.tail.rotation.y = 0.35 * k * Math.sin(t * 3.1 + ph);
  }

  // drafts (film.py --draft) set window.__draftScale: the GL buffers shrink with the page so a 3D draft is really quicker
  const _makeRenderer = K3.makeRenderer;
  K3.makeRenderer = function (canvas, W, H, o) { const r = _makeRenderer(canvas, W, H, o); const ds = window.__draftScale || 1;
    if (ds !== 1) { r.setPixelRatio(ds); r.setSize(W, H, false); } return r; };
  Object.assign(K3, { makeFur, furAlphaTex, plushMaterial, glossMaterial, leatherMaterial, metalMaterial, makeEye, makeRabbit, makeLion,
    schematic, orbitWalk, studio, hud, labPost, idle, LAB_VERSION: 1 });
})();
