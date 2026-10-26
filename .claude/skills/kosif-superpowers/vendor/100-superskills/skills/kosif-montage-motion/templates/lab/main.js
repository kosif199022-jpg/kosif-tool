/* أرنب وأسد — KOSIF LAB 01. A plush rabbit and a plush lion on a cream studio sweep; one lens walks the whole circle and
   stops at parts; the HUD names each stop (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK). Everything is a function of t. */
const { THREE, smooth, ramp, clamp01, makeRenderer, makeRabbit, makeLion, schematic, orbitWalk, studio, hud, labPost, idle, makeFrameLoop } = window.K3;
const SECONDS = {{SECONDS}};
const ease = (x) => x * x * (3 - 2 * x);
const pulse = (t, a, b) => ramp(t, a, a + 0.5) * (1 - ramp(t, b - 0.5, b));   // 0→1 at a, back to 0 at b

function build(canvas, W, H) {
  const renderer = makeRenderer(canvas, W, H, { tone: "neutral", exposure: 1.0 });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, W / H, 0.05, 100);
  studio(scene);

  const rabbit = makeRabbit({ color: 0xf2f0ea, inner: 0xf1b7c3, iris: 0x3a7bd5, layers: 7, furLength: 0.09 });
  rabbit.position.set(-1.15, 0, 0.1); rabbit.rotation.y = 0.35; scene.add(rabbit);
  const lion = makeLion({ color: 0xe6b35b, mane: 0x8a4a1c, iris: 0xd9a21b, layers: 8, furLength: 0.07 });
  lion.position.set(0.95, 0, -0.2); lion.rotation.y = -0.55; scene.add(lion);
  const RJ = rabbit.userData.joints, LJ = lion.userData.joints;
  const schemR = schematic(rabbit), schemL = schematic(lion);

  const walk = orbitWalk(camera, [
    { t: 0.0, angle: 28, dist: 6.4, height: 2.1, look: [0, 1.0, 0], fov: 30 },                          // SHAPE: the pair, wide
    { t: 3.0, angle: -35, dist: 2.3, height: 1.75, look: RJ.head, fov: 30, hold: 1.2 },                   // JOINT: the rabbit's head
    { t: 6.5, angle: -5, dist: 1.0, height: 1.9, look: RJ.eyeL, fov: 26, hold: 1.2 },                  // the eye, extreme close
    { t: 9.5, angle: -25, dist: 2.3, height: 1.7, look: LJ.head, fov: 30, hold: 1.2 },                  // LOAD: the lion's mane
    { t: 13.0, angle: 175, dist: 4.2, height: 1.4, look: [0, 1.0, 0], fov: 32, hold: 0.8 },             // BREAK: the far side
    { t: 16.0, angle: 300, dist: 1.6, height: 1.2, look: RJ.tail, fov: 30, hold: 1.0 },                 // SWAP: the tail
    { t: 18.0, angle: 388, dist: 6.0, height: 2.2, look: [0, 1.0, 0], fov: 30 },                        // RANK: back to the wide
  ]);

  const root = document.getElementById("root");
  const H1 = hud(root, W, H, { title: "KOSIF LAB 01", subtitle: "ARNAB × ASAD · one lens, walking the whole circle", seed: 5 });
  const co = {
    ear: H1.addCallout({ anchor: RJ.earL, label: "THE EAR · الأذن", title: "two-layer capsule, pink inner", text: "pivot at the skull; swings ±7°", side: "right", measure: (t) => (0.42 + 0.03 * Math.sin(t * 2.6)).toFixed(2) + " m" }),
    eye: H1.addCallout({ anchor: RJ.eyeL, label: "THE EYE · العين", title: "sclera · iris · pupil · cornea", text: "a clearcoat shell over a flattened iris", side: "right", measure: (t) => "Ø 0.20 m" }),
    mane: H1.addCallout({ anchor: LJ.head, label: "THE MANE · اللبدة", title: "10 fur shells, 0.18 m long", text: "roots dark, tips light; gravity on the shells", side: "left", measure: (t) => (0.18 + 0.02 * Math.sin(t * 1.3)).toFixed(2) + " m" }),
    tail: H1.addCallout({ anchor: RJ.tail, label: "THE TAIL · الذيل", title: "one joint, one sphere", text: "swapped for a lion tuft and re-run", side: "left", measure: (t) => "swap #1" }),
  };

  const stageAt = (t) => t < 3 ? "SHAPE" : t < 9.5 ? "JOINT" : t < 13 ? "LOAD" : t < 16 ? "BREAK" : t < 18 ? "SWAP" : "RANK";
  const sideAt = (t) => ({ SHAPE: "SHAPE — the object rebuilt as parts<br>الشكل — أجزاء بأبعاد حقيقية", JOINT: "JOINT — every pivot, what it permits<br>المفصل — ما يُسمح له أن يتحرك",
    LOAD: "LOAD — the mane carries 10 shells<br>الحمل — اللبدة تحمل عشر طبقات", BREAK: "BREAK — the far side, the weakest path<br>الكسر — الجهة البعيدة", SWAP: "SWAP — one part changed, whole run again<br>التبديل — جزء واحد، التجربة كلها", RANK: "RANK — sorted by how little it takes<br>الترتيب — من الأضعف" })[stageAt(t)];

  // the swap: the rabbit's tail becomes a lion tuft (colour and size) after 16 s
  const tailMesh = RJ.tail.children.find((m) => m.name === "tail");
  const tailBase = tailMesh.material.color.clone(), tuft = new THREE.Color(0x8a4a1c);

  const post = labPost(renderer, scene, camera, W, H, { bloom: 0 });

  function update(t) {
    walk(t);
    // SHAPE: the pair forms from wireframe to plush over the first 3 s; JOINT markers glow while the lens visits the pivots
    const form = 1 - ease(ramp(t, 0.4, 2.8));
    schemR.set(form, camera); schemL.set(form, camera);
    schemR.explode(0.35 * pulse(t, 3.2, 6.2)); schemR.joints(pulse(t, 3.0, 9.0));
    schemL.joints(pulse(t, 9.6, 12.8));
    // life
    idle(rabbit, t, { amount: 1, phase: 0 }); idle(lion, t, { amount: 0.8, phase: 1.7 });
    RJ.head.rotation.y += 0.25 * smooth(3, 4.5, t) - 0.25 * smooth(9, 10, t);           // the rabbit looks at the lens at its stop
    LJ.head.rotation.y += -0.3 * smooth(9.8, 11, t) + 0.3 * smooth(12.5, 13.5, t);
    LJ.head.rotation.x += 0.12 * Math.sin(t * 0.9) * smooth(9.8, 11, t) * (1 - smooth(12.5, 13.5, t));
    // BREAK: on the far side the rabbit's ears flop and recover, one after the other
    RJ.earL.rotation.x += 0.9 * pulse(t, 13.4, 15.2); RJ.earR.rotation.x += 0.9 * pulse(t, 13.9, 15.7);
    // SWAP
    const sw = ease(ramp(t, 16.4, 17.2));
    tailMesh.material.color.copy(tailBase).lerp(tuft, sw); RJ.tail.scale.setScalar(1 + 0.45 * sw);
    if (tailMesh.userData.fur) tailMesh.userData.fur.children.forEach((m, i, a) => m.material.color.copy(tailBase).lerp(tuft, sw).multiplyScalar(0.55 + 0.45 * (i + 1) / a.length));
    // callouts
    co.ear.show = pulse(t, 3.4, 6.3); co.eye.show = pulse(t, 6.9, 9.3); co.mane.show = pulse(t, 10.0, 12.8); co.tail.show = pulse(t, 16.2, 18.0);
    H1.update(t, camera, { stage: stageAt(t), side: sideAt(t), duration: SECONDS });
    // RANK: the two step forward a touch for the final wide
    const rk = ease(ramp(t, 18.2, 19.6));
    rabbit.position.z = 0.1 + 0.25 * rk; lion.position.z = -0.2 + 0.25 * rk;
  }
  const render = makeFrameLoop(renderer, post, W, H, update);
  return { render, ready: Promise.resolve(), scene, camera, renderer };
}
window.__three = { build };
