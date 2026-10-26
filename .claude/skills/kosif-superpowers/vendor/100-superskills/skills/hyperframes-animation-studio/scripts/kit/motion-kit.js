/* KOSIF Motion Kit v3 — professional, deterministic motion helpers on top of GSAP, for HyperFrames compositions
   (window.__timelines, seconds) and for KOSIF Studio's own renderer (window.render(t) / window.__ready).
   Everything is keyed to the timeline; nothing uses the wall clock or unseeded randomness, and nothing relies on
   tween callbacks that a paused seek suppresses: discrete state (typed text, counters, morphs) is driven through
   GSAP modifiers, which run on every render.
   v3 adds the house motion system measured from top-tier launch films (see references/craft-numbers.md):
   easing tokens E (cubic-bezier, one curve family per role), physical springs SPR (critically damped by default),
   hitPulse, log-space zoom, a cursor with real physics, typeOn / scramble / counter, iris and flood seams, a rack
   focus that never animates a large blur, a 3D roll, SVG path morphs, directional speed blur, contact squash,
   the U-speed shot (enter fast, cruise, accelerate into the cut) and polarity flips at act boundaries. */
(function () {
  const ease = { slam: "expo.out", snap: "back.out(1.3)", drive: "power4.inOut", settle: "power4.out", linear: "none" };

  /* ── cubic-bezier → ease function (GSAP accepts functions), the tokens one curve family per role ── */
  function bezier(x1, y1, x2, y2) {
    const A = (a, b) => 1 - 3 * b + 3 * a, B = (a, b) => 3 * b - 6 * a, C = (a) => 3 * a;
    const calc = (t, a, b) => ((A(a, b) * t + B(a, b)) * t + C(a)) * t;
    const slope = (t, a, b) => 3 * A(a, b) * t * t + 2 * B(a, b) * t + C(a);
    const solve = (x) => { let t = x; for (let i = 0; i < 8; i++) { const s = slope(t, x1, x2); if (Math.abs(s) < 1e-6) break; t -= (calc(t, x1, x2) - x) / s; } return Math.min(1, Math.max(0, t)); };
    return (p) => (p <= 0 ? 0 : p >= 1 ? 1 : calc(solve(p), y1, y2));
  }
  const E = {
    out: bezier(.16, 1, .3, 1),           // arrivals, reveals: peak velocity on the first frame, long settle
    outSoft: bezier(.22, 1, .36, 1),      // gentle settles, secondary arrivals
    in: bezier(.7, 0, .84, 0),            // implosions, hard snaps out
    exit: bezier(.55, .055, .675, .19),   // exits into a cut: about ×1.14 per frame over the last 10–24 f
    inOut: bezier(.87, 0, .13, 1),        // whips, lockup slides, morphs
    smooth: bezier(.65, 0, .35, 1),       // fades (10–14 f), drifts, breath
    ui: bezier(.4, 0, .2, 1),             // small UI changes
    cam: bezier(.48, .1, 0, .9),          // camera pushes: slow start, peak at ~27%, long settle
    glide: bezier(.47, .2, .15, 1),       // 150–350 px element moves
    rest: bezier(.45, 0, .1, 1),          // moves that end at rest; chaining after another move
    contact: bezier(.55, 0, .9, .55),     // accelerating into an impact
    whip: bezier(.6, 0, .15, 1),          // feature-to-feature whips
    dolly: bezier(.35, 0, .65, 1),        // slow push through a hold
    type: bezier(.5, 1, .89, 1),          // an eased typewriter's character count
    iris: bezier(.4, 0, .7, .92),         // an iris in log space, landing with a little speed
    shutter: bezier(.2, .7, .2, 1),       // a collapse already moving on its first frame
    hop: bezier(.35, 0, .7, .85),         // ballistic hops: eases off, lands with speed
    linear: (p) => p,
  };
  /* an ease that moves a linear tween through log space: scale/zoom feel constant from a to b */
  const logEase = (a, b, fn) => (p) => (Math.exp((fn || E.linear)(p) * (Math.log(b) - Math.log(a)) + Math.log(a)) - a) / (b - a);
  const lmix = (a, b, t) => Math.exp(Math.log(a) + (Math.log(b) - Math.log(a)) * t);
  const clamp01 = (x) => Math.min(1, Math.max(0, x));
  /* hitPulse: the one envelope for punches and ticks (attack, tau in 60 fps frames; t in seconds) */
  function hitPulse(t, attack = 2, tau = 5) { const u = t * 60; return u <= 0 || u > attack + 6 * tau ? 0 : u < attack ? Math.sin((u / attack) * Math.PI / 2) : Math.exp(-(u - attack) / tau); }
  /* duration grows with distance: 0.35 s + 1.35 ms per px (camera clamped to 0.6–2.4 s) */
  const durFor = (px, camera) => { const s = 0.35 + 0.00135 * px; return camera ? Math.min(2.4, Math.max(0.6, s)) : s; };

  /* ── springs: the v2 normalised oscillator (a GSAP ease) and v3 physical springs (closed form, retargetable) ── */
  const SPRINGS = { snappy: { zeta: 0.62, omega: 20 }, default: { zeta: 0.74, omega: 17 }, heavy: { zeta: 1.0, omega: 13 }, playful: { zeta: 0.45, omega: 18 } };
  function springFn(preset) {
    const s = typeof preset === "string" ? SPRINGS[preset] || SPRINGS.default : preset;
    const z = s.zeta, w = s.omega;
    const f = (t) => {
      if (z < 1) { const wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); }
      return 1 - Math.exp(-w * t) * (1 + w * t);
    };
    const end = f(1);
    return (p) => f(p) / end;
  }
  const spring = (preset) => springFn(preset);
  /* physical presets (damping / stiffness / mass): critically damped by default; overshoot only on a true landing */
  const SPR = { snap: { damping: 18, stiffness: 260, mass: 0.7 }, pop: { damping: 11, stiffness: 180, mass: 0.6 }, land: { damping: 14.5, stiffness: 200, mass: 1 },
                micro: { damping: 30, stiffness: 500, mass: 0.6 }, firm: { damping: 24, stiffness: 140, mass: 1 }, soft: { damping: 26, stiffness: 120, mass: 1 }, heavy: { damping: 30, stiffness: 90, mass: 1.4 } };
  function springStep(t, cfg) {                              // step response 0 → 1 of a damped spring let go at t = 0
    if (t <= 0) return 0;
    const m = cfg.mass || 1, w0 = Math.sqrt(cfg.stiffness / m), z = cfg.damping / (2 * Math.sqrt(cfg.stiffness * m));
    let v;
    if (z < 1) { const wd = w0 * Math.sqrt(1 - z * z); v = 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t)); }
    else if (z === 1) v = 1 - Math.exp(-w0 * t) * (1 + w0 * t);
    else { const wd = w0 * Math.sqrt(z * z - 1); v = 1 - Math.exp(-z * w0 * t) * (Math.cosh(wd * t) + (z * w0 / wd) * Math.sinh(wd * t)); }
    return cfg.clamp ? Math.min(v, 1) : v;
  }
  /* a value with many targets: the first value plus one spring per change (continuous, seekable) */
  function track(t, keys, preset, settle) {
    if (preset && typeof preset === "object" && preset.stiffness) {
      let v = keys[0][1];
      for (let i = 1; i < keys.length; i++) v += (keys[i][1] - keys[i - 1][1]) * springStep(t - keys[i][0], preset);
      return v;
    }
    const sp = springFn(preset || "default"), T = settle || 0.6;
    let v = keys[0][1];
    for (let i = 1; i < keys.length; i++) { const [kt, kv] = keys[i]; if (t <= kt) break; v = v + (kv - v) * sp(Math.min(1, (t - kt) / T)); }
    return v;
  }
  function zoomTrack(t, keys, preset, settle) { return Math.exp(track(t, keys.map(([kt, kv]) => [kt, Math.log(kv)]), preset, settle)); }
  /* beats: picture and sound read the same clock; beats(bpm) or beats(json from motion.py beats) */
  function beats(bpm, offset) {
    if (bpm && typeof bpm === "object") { const list = bpm.beats || []; return { at: (n) => list[Math.min(list.length - 1, n)], len: (n) => n * 60 / bpm.bpm, bpm: bpm.bpm, beat: 60 / bpm.bpm, list, hits: bpm.hits || [], downbeats: bpm.downbeats || list.filter((_, i) => i % 4 === 0) }; }
    const b = 60 / bpm, o = offset || 0; return { at: (n) => o + n * b, len: (n) => n * b, bpm, beat: b, downbeats: null };
  }
  /* the soundtrack as per-frame channels (motion.py channels TRACK.wav → JSON): every visual can come from the sound.
     ch.v("bass", t) interpolates a channel; ch.kick(t) is a hitPulse summed over the measured kicks; ch.tape(t) is the
     tape clock (slows, freezes and overdrives with the track: drive the world with it); ch.silent(t), ch.near("onsets", t) */
  function channels(json) {
    const fps = json.fps || 30, n = json.frames || 0;
    const v = (name, t) => { const a = json[name]; if (!a || !a.length) return 0; const x = Math.max(0, Math.min(a.length - 1, t * fps)), i = Math.floor(x), f = x - i; return a[i] + ((a[Math.min(a.length - 1, i + 1)] - a[i]) * f); };
    const pulse = (list, t, attack, tau) => { let m = 0; for (const k of list || []) { if (k > t) break; m = Math.max(m, hitPulse(t - k, attack, tau)); } return m; };
    return { fps, frames: n, bpm: json.bpm, v, raw: json,
      kick: (t, attack = 1, tau = 5) => pulse(json.kicks, t, attack, tau),
      onset: (t, attack = 1, tau = 4) => pulse(json.onsets, t, attack, tau),
      beat: (t) => pulse(json.beats, t, 1, 6),
      tape: (t) => v("tape", t), silent: (t) => v("silence", t) > 0.5,
      near: (name, t, win = 0.05) => (json[name] || []).some((k) => Math.abs(k - t) <= win) };
  }
  /* a tween value sampled from a function of time, as GSAP keyframes (60 per second): seek-safe motion from code */
  function sampled(fn, t0, t1, fps) { const f = fps || 60, out = []; for (let i = 0, n = Math.max(1, Math.round((t1 - t0) * f)); i <= n; i++) { const v = fn(t0 + i / f); out.push(Object.assign({ duration: i ? 1 / f : 0, ease: "none" }, v)); } return out; }

  /* colour harmonies (colour-theory cheat sheet; Gurney's advice: one family dominates, its complement only as an accent).
     palette("split", 210) → { hues, css: ["hsl(...)", ...] }; o.sat, o.light (list) set saturation and the value plan */
  function palette(scheme, baseHue, o) {
    o = o || {};
    const off = { complementary: [0, 180], analogous: [-30, 0, 30], triadic: [0, 120, 240], split: [0, 150, 210], tetradic: [0, 60, 180, 240] }[scheme] || [0];
    const hues = off.map((d) => ((baseHue + d) % 360 + 360) % 360), L = o.light || [50], S = o.sat == null ? 60 : o.sat;
    return { hues, css: hues.map((h, i) => `hsl(${Math.round(h)} ${S}% ${L[i % L.length]}%)`) };
  }
  function rng(seed) {                                     // mulberry32: the same seed gives the same film
    let a = (seed >>> 0) || 1;
    return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  const hash = (i, j) => { let h = (i * 374761393 + j * 668265263) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };

  const SVG = "http://www.w3.org/2000/svg";
  function svgEl(tag, attrs, parent) { const el = document.createElementNS(SVG, tag); for (const k in attrs) el.setAttribute(k, attrs[k]); if (parent) parent.appendChild(el); return el; }

  /* ── text: words revealed through clip-path masks (RTL-safe: whole words move, letters stay joined) ── */
  function words(el) {
    if (el.dataset.split) return Array.from(el.querySelectorAll(".mk-wi"));
    const keep = Array.from(el.children).filter((c) => c.classList && c.classList.contains("num"));
    const text = Array.from(el.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent).join(" ").trim().split(/\s+/).filter(Boolean);
    const small = el.querySelector("small");
    const smallText = small ? small.textContent : null;
    el.textContent = "";
    keep.forEach((k) => el.appendChild(k));
    const inners = [];
    const addWords = (target, list) => list.forEach((w, i) => {
      const mask = document.createElement("span");
      mask.className = "mk-w";
      mask.style.cssText = "display:inline-block;vertical-align:bottom;padding:.06em .04em .18em;margin-bottom:-.18em;clip-path:inset(-0.05em -0.05em 0 -0.05em)";
      const inner = document.createElement("span");
      inner.className = "mk-wi";
      inner.style.cssText = "display:inline-block";
      inner.textContent = w;
      mask.appendChild(inner);
      target.appendChild(mask);
      if (i < list.length - 1) target.appendChild(document.createTextNode(" "));
      inners.push(inner);
    });
    addWords(el, text);
    if (smallText) { const s = document.createElement("small"); el.appendChild(s); addWords(s, smallText.trim().split(/\s+/)); }
    el.dataset.split = "1";
    return inners;
  }
  function revealWords(tl, el, at, o) {
    o = o || {};
    const inners = words(el);
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(inners, { yPercent: o.from === "top" ? -115 : 115, opacity: 0 },
      { yPercent: 0, opacity: 1, duration: o.dur || 0.7, stagger: o.stagger == null ? 0.07 : o.stagger, ease: o.ease || ease.slam }, at);
    const num = el.querySelector(".num");
    if (num) tl.fromTo(num, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: o.numEase || spring("snappy") }, at);
    return inners;
  }
  function hideWords(tl, el, at, o) {
    o = o || {};
    const inners = words(el);
    tl.to(inners, { yPercent: o.to === "down" ? 115 : -115, opacity: 0, duration: o.dur || 0.45, stagger: o.stagger == null ? 0.04 : o.stagger, ease: o.ease || ease.drive }, at);
    const num = el.querySelector(".num");
    if (num) tl.to(num, { scale: 0, opacity: 0, duration: 0.4, ease: ease.drive }, at);
    tl.set(el, { visibility: "hidden" }, at + (o.dur || 0.45) + 0.3);
  }
  /* words arrive from a partial state (40% opacity, a 9% rise, blur clearing early) and settle on one constant */
  function riseWords(tl, el, at, o) {
    o = o || {};
    const inners = words(el);
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(inners, { y: o.rise || 26, opacity: 0.4, filter: `blur(${o.blur == null ? 6 : o.blur}px)` },
      { y: 0, opacity: 1, filter: "blur(0px)", duration: o.dur || 0.4, stagger: o.stagger == null ? 0.1 : o.stagger, ease: E.out }, at);
    return inners;
  }
  /* lines (any elements) rising out of a clip under their baseline: the mask-rise reveal */
  function maskRise(tl, els, at, o) {
    o = o || {};
    const list = Array.from(els.length != null ? els : [els]);
    list.forEach((el) => { if (!el.dataset.mkMask) { el.style.clipPath = "inset(-0.1em -0.1em 0 -0.1em)"; el.dataset.mkMask = "1"; } });
    tl.fromTo(list, { yPercent: 110, opacity: 1 }, { yPercent: 0, duration: o.dur || 0.5, stagger: o.stagger == null ? 0.08 : o.stagger, ease: E.out, immediateRender: false }, at);
    if (o.out != null) tl.to(list, { yPercent: -110, duration: o.outDur || 0.27, stagger: (o.stagger == null ? 0.08 : o.stagger) / 2, ease: E.in }, o.out);
    return list;
  }
  /* typewriter with an eased character count (55–75% of the characters in the first fifth) and a caret; seek-safe */
  function typeOn(tl, el, text, at, o) {
    o = o || {};
    const caret = o.caret !== false;
    const proxy = { n: 0 };
    const dur = o.dur || Math.min(1.2, Math.max(0.5, text.length / (o.cps || 46)));
    const write = (v) => { const n = Math.round(v); el.textContent = text.slice(0, n) + (caret && n < text.length ? "|" : ""); return v; };
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(proxy, { n: 0 }, { n: text.length, duration: dur, ease: o.ease || E.type, modifiers: { n: write }, immediateRender: false }, at);
    if (caret && o.blink !== false) {                       // the caret blinks at 2 Hz while the line is read
      const bp = { b: 0 }, hold = o.hold || 1.0;
      tl.fromTo(bp, { b: 0 }, { b: hold, duration: hold, ease: "none", immediateRender: false, modifiers: { b: (v) => { el.textContent = text + (Math.floor(v * 2) % 2 ? "" : "|"); return v; } } }, at + dur);
    }
    return dur;
  }
  /* decode reveal: glyphs cycle through same-class glyphs, then lock left to right (seeded, seek-safe) */
  function scramble(tl, el, text, at, o) {
    o = o || {};
    const proxy = { p: 0 }, pool = o.pool || "ABCDEFGHJKLMNPQRSTUVWXYZ023456789";
    const dur = o.dur || 0.9;
    const write = (p) => {
      const lock = p * text.length * 1.15;
      let s = "";
      for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        if (ch === " " || i < lock) s += ch;
        else { const k = Math.floor(p * 40) * 7 + i; s += /\d/.test(ch) ? String(Math.floor(hash(k, i) * 10)) : pool[Math.floor(hash(k, i + 99) * pool.length)]; }
      }
      el.textContent = s; return p;
    };
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(proxy, { p: 0 }, { p: 1, duration: dur, ease: "none", modifiers: { p: write }, immediateRender: false }, at);
    return dur;
  }
  /* a rolling counter with tabular figures: starts near the final value, eases out, holds (seek-safe) */
  function counter(tl, el, from, to, at, dur, o) {
    o = o || {};
    const proxy = { v: from }, dec = o.decimals || 0;
    const fmt = (v) => { const s = v.toFixed(dec); return o.sep === false ? (o.prefix || "") + s + (o.suffix || "") : (o.prefix || "") + s.replace(/\B(?=(\d{3})+(?!\d))/g, o.sep || ",") + (o.suffix || ""); };
    el.style.fontVariantNumeric = "tabular-nums";
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(proxy, { v: from }, { v: to, duration: dur || 1.0, ease: o.ease || E.out, modifiers: { v: (v) => { el.textContent = fmt(v); return v; } }, immediateRender: false }, at);
  }

  /* ── strokes drawn on, like a pen ── */
  function drawPath(tl, path, at, dur, o) {
    o = o || {};
    const len = path.getTotalLength();
    path.style.strokeDasharray = len + " " + len;
    path.style.strokeDashoffset = len;
    tl.set(path, { opacity: o.opacity == null ? 1 : o.opacity }, at);
    tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: o.ease || ease.drive, immediateRender: false }, at);
    if (o.head) tl.fromTo(o.head, { scale: 0, opacity: 0, transformOrigin: o.headOrigin || "50% 50%" }, { scale: 1, opacity: 1, duration: 0.35, ease: spring("snappy"), immediateRender: false }, at + dur - 0.1);
    return len;
  }
  function flowDash(tl, path, at, dur, o) {
    o = o || {};
    const pat = o.pattern || "28 22";
    path.style.strokeDasharray = pat;
    const step = pat.split(" ").map(Number).reduce((a, b) => a + b, 0);
    tl.fromTo(path, { strokeDashoffset: 0 }, { strokeDashoffset: -step * (o.cycles || 6), duration: dur, ease: "none" }, at);
  }
  /* an SVG path morphs into another: both are sampled to N points, the proxy drives the in-between (seek-safe) */
  function morphPath(tl, pathEl, fromD, toD, at, o) {
    o = o || {};
    const N = o.points || 120;
    const sample = (d) => { const p = svgEl("path", { d }, pathEl.ownerSVGElement || document.body); const L = p.getTotalLength(), pts = []; for (let i = 0; i <= N; i++) { const q = p.getPointAtLength(L * i / N); pts.push([q.x, q.y]); } p.remove(); return pts; };
    const A = sample(fromD), B = sample(toD), proxy = { p: 0 };
    const write = (p) => { let d = ""; for (let i = 0; i <= N; i++) { const x = A[i][0] + (B[i][0] - A[i][0]) * p, y = A[i][1] + (B[i][1] - A[i][1]) * p; d += (i ? " L" : "M") + x.toFixed(2) + " " + y.toFixed(2); } pathEl.setAttribute("d", d + (o.open ? "" : " Z")); return p; };
    tl.fromTo(proxy, { p: 0 }, { p: 1, duration: o.dur || 0.66, ease: o.ease || E.inOut, modifiers: { p: write }, immediateRender: false }, at);
  }

  /* ── particles ── */
  function rain(tl, container, o) {
    const r = rng(o.seed || 11), drops = [];
    const n = o.n || 240, x0 = o.x0 || 0, x1 = o.x1 || 1920, y0 = o.y0 || 0, y1 = o.y1 || 1080;
    const fall = o.fall || 0.55, len = o.len || 46, angle = o.angle || -8;
    const ns = container.namespaceURI === SVG;
    for (let i = 0; i < n; i++) {
      const x = x0 + r() * (x1 - x0), l = len * (0.6 + r() * 0.8), w = 1 + r() * 1.6;
      let d;
      if (ns) d = svgEl("line", { x1: x, y1: y0 - l, x2: x + Math.tan(angle * Math.PI / 180) * l, y2: y0, stroke: o.color || "rgba(220,235,255,.75)", "stroke-width": w, "stroke-linecap": "round" }, container);
      else { d = document.createElement("div"); d.style.cssText = `position:absolute;left:${x}px;top:${y0 - l}px;width:${w}px;height:${l}px;border-radius:${w}px;background:${o.color || "rgba(220,235,255,.75)"};transform:rotate(${angle}deg)`; container.appendChild(d); }
      drops.push(d);
      const dur = fall * (0.75 + r() * 0.5), delay = r() * dur;
      tl.fromTo(d, { y: 0, opacity: 0.9 }, { y: (y1 - y0) + l, opacity: 0.6, duration: dur, ease: "none", repeat: Math.ceil(o.dur / dur) + 1 }, o.at - dur + delay);
    }
    tl.fromTo(container, { opacity: 0 }, { opacity: 1, duration: o.fadeIn || 0.6, ease: ease.drive }, o.at);
    tl.to(container, { opacity: 0, duration: o.fadeOut || 0.8, ease: ease.drive }, o.at + o.dur - (o.fadeOut || 0.8));
    return drops;
  }
  function vapour(tl, container, o) {
    const r = rng(o.seed || 5), puffs = [];
    const n = o.n || 70;
    for (let i = 0; i < n; i++) {
      const x = o.x0 + r() * (o.x1 - o.x0), y = o.y0 + r() * (o.yJitter || 30);
      const rad = (o.r || 18) * (0.6 + r() * 1.1);
      const p = svgEl("circle", { cx: x, cy: y, r: rad, fill: o.color || "rgba(255,255,255,.55)" }, container);
      puffs.push(p);
      const dur = (o.rise || 2.6) * (0.75 + r() * 0.6), delay = r() * (o.spread || 1.2);
      const reps = Math.max(0, Math.ceil(o.dur / dur) - 1);
      tl.fromTo(p, { opacity: 0, scale: 0.5, transformOrigin: "50% 50%", x: 0, y: 0 },
        { opacity: 0.9, scale: 1.4, y: -(o.height || 320) * (0.7 + r() * 0.6), x: (r() - 0.5) * (o.drift || 120), duration: dur, ease: "sine.out", repeat: reps }, o.at + delay);
      tl.to(p, { opacity: 0, duration: dur * 0.35, ease: "sine.in", repeat: reps, repeatDelay: dur * 0.65 }, o.at + delay + dur * 0.65);
    }
    tl.to(container, { opacity: 0, duration: 0.8, ease: ease.drive }, o.at + o.dur);
    return puffs;
  }
  function sparkle(tl, container, o) {
    const r = rng(o.seed || 3), pts = [];
    for (let i = 0; i < (o.n || 40); i++) {
      const p = svgEl("circle", { cx: o.x0 + r() * (o.x1 - o.x0), cy: o.y0 + r() * (o.y1 - o.y0), r: 1 + r() * 2.2, fill: o.color || "#fff" }, container);
      pts.push(p);
      tl.fromTo(p, { opacity: 0.15 }, { opacity: 1, duration: 0.6 + r() * 1.2, yoyo: true, repeat: 40, ease: "sine.inOut" }, o.at + r() * 2);
    }
    return pts;
  }

  /* ── camera: the stage moves as one thing; count the moves, keep it still in between ── */
  function camera(tl, stage, at, o) {
    o = o || {};
    tl.to(stage, { x: o.x || 0, y: o.y || 0, scale: o.scale || 1, rotation: o.rotation || 0, duration: o.dur || 1.4, ease: o.ease || E.cam, transformOrigin: o.origin || "50% 50%" }, at);
  }
  /* a push in log space: 1 → 2.4× feels constant; peak about 5% scale per frame, never more */
  function push(tl, stage, at, from, to, dur, o) {
    o = o || {};
    tl.fromTo(stage, { scale: from }, { scale: to, duration: dur || durFor(Math.abs(to - from) * 600, true), ease: logEase(from, to, o.ease || E.cam), transformOrigin: o.origin || "50% 50%", immediateRender: false }, at);
  }
  /* a hold that stays alive: a creep of ~4% per second, or a drift of 0.3–2.5 px/f */
  function breathe(tl, stage, at, dur, o) {
    o = o || {};
    tl.to(stage, { scale: `+=${(o.creep == null ? 0.04 : o.creep) * dur}`, x: `+=${(o.drift || 0) * dur * 60}`, duration: dur, ease: "none" }, at);
  }
  function flash(tl, el, at, o) {
    o = o || {};
    tl.fromTo(el, { opacity: 0 }, { opacity: o.peak || 0.85, duration: 0.06, ease: "none" }, at);
    tl.to(el, { opacity: 0, duration: o.dur || 0.35, ease: ease.settle }, at + 0.06);
    if (o.again) { tl.to(el, { opacity: (o.peak || 0.85) * 0.5, duration: 0.05 }, at + 0.16); tl.to(el, { opacity: 0, duration: 0.3 }, at + 0.21); }
  }

  /* ── seams ── */
  /* iris: reveal (or hide, o.close) an element through a circle from a point, radius in log space */
  function iris(tl, el, at, o) {
    o = o || {};
    const x = o.x == null ? "50%" : o.x + "px", y = o.y == null ? "50%" : o.y + "px", R = o.r || 2300, r0 = o.r0 || 1;
    const from = `circle(${o.close ? R : r0}px at ${x} ${y})`, to = `circle(${o.close ? r0 : R}px at ${x} ${y})`;
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(el, { clipPath: from, webkitClipPath: from }, { clipPath: to, webkitClipPath: to, duration: o.dur || 0.4, ease: o.close ? logEase(R, r0, E.in) : logEase(r0, R, E.out), immediateRender: false }, at);
  }
  /* flood: a full-frame accent from a point (the one flood a film gets), already opening on its cue */
  function flood(tl, stage, at, o) {
    o = o || {};
    const d = document.createElement("div");
    d.style.cssText = `position:absolute;inset:0;background:${o.color || "#e4342f"};z-index:${o.z || 60};pointer-events:none;visibility:hidden`;
    stage.appendChild(d);
    iris(tl, d, at - 1 / 60, { x: o.x, y: o.y, r: o.r || 2400, dur: o.dur || 0.3 });
    if (o.out != null) tl.to(d, { opacity: 0, duration: o.outDur || 0.2, ease: E.smooth }, o.out);
    return d;
  }
  /* rack focus: cross-fade a sharp element and a constant-blur copy (an animated large blur steps; this does not) */
  function rackFocus(tl, el, at, o) {
    o = o || {};
    let twin = el.__mkTwin;
    if (!twin) { twin = el.cloneNode(true); twin.style.filter = `blur(${o.blur || 18}px)`; twin.style.pointerEvents = "none"; twin.style.opacity = "0"; el.parentNode.insertBefore(twin, el.nextSibling); el.__mkTwin = twin; }
    const toBlur = o.to !== "sharp";
    tl.to(el, { opacity: toBlur ? 0 : 1, duration: o.dur || 0.3, ease: E.smooth }, at);
    tl.to(twin, { opacity: toBlur ? 1 : 0, duration: o.dur || 0.3, ease: E.smooth }, at);
    return twin;
  }
  /* a 3D roll: 35% of the rotation in the first frame, done in 10 f (front-loaded), with perspective on the parent */
  function roll(tl, el, at, o) {
    o = o || {};
    if (el.parentNode && !el.parentNode.style.perspective) el.parentNode.style.perspective = (o.perspective || 2200) + "px";
    tl.fromTo(el, { rotationX: o.from == null ? -90 : o.from, transformOrigin: o.origin || "50% 100%", opacity: 1 }, { rotationX: 0, duration: o.dur || 0.17, ease: E.out, immediateRender: false }, at);
  }
  /* polarity: the stage flips ink ↔ paper at an act boundary, riding the cut (6 f, never on a static frame) */
  function polarity(tl, stage, at, bg, fg) {
    tl.to(stage, { backgroundColor: bg, color: fg || "", duration: 0.1, ease: E.smooth }, at);
  }
  /* contact squash on impact: widen and flatten against the edge it hit (8 f), anchored at that edge */
  function squash(tl, el, at, o) {
    o = o || {};
    const origin = o.edge === "top" ? "50% 0%" : o.edge === "left" ? "0% 50%" : o.edge === "right" ? "100% 50%" : "50% 100%";
    tl.fromTo(el, { scaleX: 1 + (o.across || 0.08), scaleY: 1 - (o.along || 0.10), transformOrigin: origin }, { scaleX: 1, scaleY: 1, duration: o.dur || 0.13, ease: E.outSoft, immediateRender: false }, at);
  }
  /* directional speed blur during a fast move: an SVG filter whose stdDeviation follows a bell over the move */
  function speedBlur(tl, el, at, dur, o) {
    o = o || {};
    let f = document.getElementById("mk-sb-" + (o.id || 1));
    if (!f) {
      const svg = svgEl("svg", { width: 0, height: 0, style: "position:absolute" }, document.body);
      f = svgEl("filter", { id: "mk-sb-" + (o.id || 1), x: "-50%", y: "-50%", width: "200%", height: "200%" }, svgEl("defs", {}, svg));
      svgEl("feGaussianBlur", { stdDeviation: "0 0" }, f);
    }
    const blur = f.firstChild, px = o.px || 12, axis = o.axis || "x";
    tl.set(el, { filter: `url(#${f.id})` }, at);
    tl.fromTo(blur, { attr: { stdDeviation: "0 0" } }, { attr: { stdDeviation: axis === "x" ? `${px} 0` : `0 ${px}` }, duration: dur * 0.45, ease: E.in, immediateRender: false }, at);
    tl.to(blur, { attr: { stdDeviation: "0 0" }, duration: dur * 0.55, ease: E.out }, at + dur * 0.45);
    tl.set(el, { filter: "none" }, at + dur + 0.01);
  }
  /* the U-speed shot: enters fast and decays, cruises slowly while it reads, accelerates into the cut */
  function shot(tl, el, at, o) {
    o = o || {};
    const enter = o.enter == null ? 0.45 : o.enter, exit = o.exit == null ? 0.3 : o.exit, cut = o.cut, dir = o.dir || "x", d = o.dist || 220, cruise = o.cruise == null ? 1.2 : o.cruise;
    tl.set(el, { opacity: 1, visibility: "visible" }, at);
    tl.fromTo(el, { [dir]: d, opacity: o.fade === false ? 1 : 0.4 }, { [dir]: 0, opacity: 1, duration: enter, ease: E.out, immediateRender: false }, at);
    const until = (cut == null ? at + enter + 2 : cut) - exit;
    if (until > at + enter) tl.to(el, { [dir]: -cruise * 60 * (until - at - enter), duration: until - at - enter, ease: "none" }, at + enter);
    if (cut != null) tl.to(el, { [dir]: `-=${o.exitDist || d * 1.4}`, duration: exit, ease: E.exit }, cut - exit);
  }

  /* ── cursor with physics: arcs 15–25% of the path, 36–48 f travel, press to 0.88 over 4 f, hover scale ── */
  function cursor(stage, o) {
    o = o || {};
    const c = document.createElement("div");
    c.className = "mk-cursor";
    c.style.cssText = `position:absolute;left:0;top:0;opacity:0;width:${o.size || 28}px;height:${(o.size || 28) * 1.22}px;z-index:${o.z || 70};pointer-events:none;transform-origin:20% 10%;filter:drop-shadow(0 6px 8px rgba(0,0,0,.28))`;
    c.innerHTML = `<svg viewBox="0 0 28 34" width="100%" height="100%"><path d="M4 2 L4 26 L10 20 L14 31 L19 29 L15 18 L24 18 Z" fill="${o.fill || "#111"}" stroke="${o.stroke || "#fff"}" stroke-width="2" stroke-linejoin="round"/></svg>`;
    stage.appendChild(c);
    return c;
  }
  /* a cursor path through timed stops (Hermite in time; `hold` stops rest at zero velocity), sampled to keyframes */
  function cursorPath(stops, t, hold) {
    hold = hold || [];
    if (t <= stops[0].t) return { x: stops[0].x, y: stops[0].y };
    const last = stops[stops.length - 1];
    if (t >= last.t) return { x: last.x, y: last.y };
    let i = 0; while (i < stops.length - 2 && t >= stops[i + 1].t) i++;
    const p0 = stops[i], p1 = stops[i + 1], span = p1.t - p0.t, u = (t - p0.t) / span;
    const vel = (k, ax) => { if (hold.includes(stops[k].t)) return 0; const a = stops[Math.max(0, k - 1)], b = stops[Math.min(stops.length - 1, k + 1)]; return (b[ax] - a[ax]) / (b.t - a.t); };
    const h00 = 2 * u ** 3 - 3 * u ** 2 + 1, h10 = u ** 3 - 2 * u ** 2 + u, h01 = -2 * u ** 3 + 3 * u ** 2, h11 = u ** 3 - u ** 2;
    const along = (ax) => h00 * p0[ax] + h10 * span * vel(i, ax) + h01 * p1[ax] + h11 * span * vel(i + 1, ax);
    return { x: along("x"), y: along("y") };
  }
  function moveCursor(tl, c, stops, o) {
    o = o || {};
    const t0 = stops[0].t, t1 = stops[stops.length - 1].t;
    tl.set(c, { x: stops[0].x, y: stops[0].y, opacity: 1 }, t0);
    tl.to(c, { keyframes: sampled((t) => cursorPath(stops, t, o.hold || []), t0, t1, o.fps || 60) }, t0);
  }
  function press(tl, c, at, o) {
    o = o || {};
    tl.to(c, { scale: 0.88, duration: 4 / 60, ease: E.ui }, at);
    tl.to(c, { scale: 1, duration: 8 / 60, ease: E.out }, at + 4 / 60);
    if (o.target) { tl.to(o.target, { scale: o.down == null ? 0.97 : o.down, duration: 4 / 60, ease: E.ui }, at); tl.to(o.target, { scale: 1, duration: 10 / 60, ease: E.out }, at + 4 / 60 + 1 / 60); }
  }

  /* ── finishing: film grain (stepped, seekable CSS) and vignette ── */
  function grain(stage, o) {
    o = o || {};
    const id = "mk-grain-" + Math.floor((o.seed || 1) * 1000);
    const svg = svgEl("svg", { width: "100%", height: "100%", style: `position:absolute;inset:0;pointer-events:none;opacity:${o.opacity == null ? 0.09 : o.opacity};mix-blend-mode:${o.blend || "soft-light"};z-index:${o.z || 90}` }, stage);
    const filter = svgEl("filter", { id }, svgEl("defs", {}, svg));
    svgEl("feTurbulence", { type: "fractalNoise", baseFrequency: o.freq || "0.9", numOctaves: "2", seed: String(o.seed || 1), stitchTiles: "stitch" }, filter);
    svgEl("feColorMatrix", { type: "saturate", values: "0" }, filter);
    const rect = svgEl("rect", { width: "200%", height: "200%", x: "-50%", y: "-50%", filter: `url(#${id})` }, svg);
    rect.style.animation = "mk-grain-jump 0.6s steps(1) infinite";
    if (!document.getElementById("mk-grain-style")) {
      const st = document.createElement("style");
      st.id = "mk-grain-style";
      st.textContent = "@keyframes mk-grain-jump{0%{transform:translate(0,0)}17%{transform:translate(-3%,2%)}33%{transform:translate(2%,-3%)}50%{transform:translate(-2%,-2%)}67%{transform:translate(3%,1%)}83%{transform:translate(-1%,3%)}100%{transform:translate(0,0)}}";
      document.head.appendChild(st);
    }
    return svg;
  }
  function vignette(stage, o) {
    o = o || {};
    const d = document.createElement("div");
    d.style.cssText = `position:absolute;inset:0;pointer-events:none;z-index:${o.z || 89};background:radial-gradient(ellipse at center, rgba(0,0,0,0) ${o.inner || 55}%, rgba(0,0,0,${o.strength == null ? 0.42 : o.strength}) 100%)`;
    stage.appendChild(d);
    return d;
  }

  /* ── the bridge to KOSIF Studio's renderer when HyperFrames' runtime is not driving the page ── */
  function shim(rootId, duration) {
    const seekAll = (t) => {
      const tls = window.__timelines || {};
      for (const k in tls) tls[k].pause(t);
      document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t * 1000; });
    };
    /* real footage: <video data-start data-duration muted> clips (motion.py footage makes them all-intra) are sought
       to the composition's time and shown only inside their span; the frame is ready once every clip has sought */
    const seekVideos = (t) => Array.from(document.querySelectorAll("video[data-start]")).map((v) => {
      const st = +v.dataset.start || 0, du = +v.dataset.duration || v.duration || 0, on = t >= st && t < st + du;
      v.style.visibility = on ? "" : "hidden";
      const lt = Math.max(0, Math.min(Math.max(0, du - 0.001), t - st));
      if (!on || (Math.abs(v.currentTime - lt) < 0.0005 && v.readyState >= 2)) return null;
      return new Promise((res) => { const done = () => { v.removeEventListener("seeked", done); res(); }; v.addEventListener("seeked", done); v.currentTime = lt; setTimeout(res, 4000); });
    }).filter(Boolean);
    window.__duration = duration;
    window.__kosifSeek = seekAll;
    if (!window.seek) window.seek = (t) => { seekAll(t); return true; };          // the seek(t) contract of the canvas route
    if (!window.__hf) {
      window.render = (t) => { window.__ready = false; seekAll(t);
        Promise.all(seekVideos(t)).then(() => requestAnimationFrame(() => requestAnimationFrame(() => { window.__ready = true; }))); };
      window.__shimRender = window.render;
      const loaded = Array.from(document.querySelectorAll("video[data-start]")).map((v) => v.readyState >= 2 ? null : new Promise((res) => { v.addEventListener("loadeddata", res, { once: true }); v.load(); setTimeout(res, 15000); })).filter(Boolean);
      const ready = () => Promise.all(loaded).then(() => Promise.all(seekVideos(0))).then(() => { seekAll(0); window.__ready = true; });
      (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(ready, ready).then(() => player(rootId, duration));
    }
  }
  /* preview: opened in an ordinary browser (not under the renderer), a composition plays itself in real time with its
     audio and footage, scaled to the window, with play/pause and a scrub bar. Renderers (navigator.webdriver, ?render,
     HyperFrames) never see it, so the frame-exact path is untouched. Wall clock here is preview-only by design. */
  function player(rootId, duration) {
    if (navigator.webdriver || window.__hf || /[?&]render\b/.test(location.search) || document.getElementById("mk-player")) return;
    const root = document.querySelector(`[data-composition-id="${rootId}"]`) || document.getElementById(rootId);
    if (!root) return;
    const W = +root.dataset.width || root.offsetWidth, H = +root.dataset.height || root.offsetHeight;
    document.documentElement.style.cssText += ";overflow:hidden;background:#0b0c0e;width:100%;height:100%";
    document.body.style.cssText += ";margin:0;overflow:hidden;background:#0b0c0e;width:auto;height:auto";
    const fit = () => { const s = Math.min(innerWidth / W, (innerHeight - 56) / H);
      root.style.position = "fixed"; root.style.left = "0px"; root.style.top = "0px"; root.style.margin = "0";
      root.style.transformOrigin = "0 0"; root.style.transform = `translate(${(innerWidth - W * s) / 2}px, 8px) scale(${s})`; };
    fit(); addEventListener("resize", fit);
    const bar = document.createElement("div"); bar.id = "mk-player";
    bar.style.cssText = "position:fixed;left:0;right:0;bottom:0;height:48px;display:flex;align-items:center;gap:12px;padding:0 16px;background:#14161a;color:#eee;font:14px system-ui,sans-serif;z-index:99999;direction:ltr";
    bar.innerHTML = '<button id="mk-pp" style="width:36px;height:32px;border:0;border-radius:6px;background:#E7B65A;color:#111;font-size:16px;cursor:pointer">▶</button>'
      + '<input id="mk-scrub" type="range" min="0" max="1000" value="0" style="flex:1">'
      + '<span id="mk-t" style="min-width:92px;text-align:right;font-variant-numeric:tabular-nums">0.00 / ' + duration.toFixed(2) + '</span>';
    document.body.appendChild(bar);
    const pp = bar.querySelector("#mk-pp"), scrub = bar.querySelector("#mk-scrub"), label = bar.querySelector("#mk-t");
    const media = Array.from(document.querySelectorAll("audio[data-start], video[data-start]"));
    let playing = false, t = 0, t0 = 0, raf = 0;
    const draw = (tt) => (window.render && window.render !== window.__shimRender ? window.render(tt) : window.__kosifSeek(tt));   // 3D pages draw through their own render
    const show = (tt) => { draw(tt); scrub.value = Math.round(tt / duration * 1000); label.textContent = tt.toFixed(2) + " / " + duration.toFixed(2); };
    const syncMedia = (tt, play) => media.forEach((m) => { const st = +m.dataset.start || 0, du = +m.dataset.duration || m.duration || duration;
      const on = tt >= st && tt < st + du; if (m.tagName === "VIDEO") m.style.visibility = on ? "" : "hidden";
      m.volume = Math.min(1, +m.dataset.volume || 1);
      if (on) { m.currentTime = Math.max(0, tt - st); if (play) m.play().catch(() => {}); else m.pause(); } else m.pause(); });
    // the clock: a playing media element when there is one (it keeps real time even when frames are throttled), else the wall clock
    const clock = (now) => { const m = media.find((x) => !x.paused && !x.ended && x.readyState >= 2);
      return m ? (+m.dataset.start || 0) + m.currentTime : (now - t0) / 1000; };
    const tick = (now) => { if (!playing) return; t = Math.min(duration, clock(now)); show(t);
      if (t >= duration) { playing = false; pp.textContent = "↺"; media.forEach((m) => m.pause()); return; } raf = requestAnimationFrame(tick); };
    const play = () => { if (t >= duration) t = 0; playing = true; pp.textContent = "❚❚"; t0 = performance.now() - t * 1000; syncMedia(t, true); raf = requestAnimationFrame(tick); };
    const pause = () => { playing = false; pp.textContent = "▶"; cancelAnimationFrame(raf); media.forEach((m) => m.pause()); };
    pp.onclick = () => (playing ? pause() : play());
    scrub.oninput = () => { pause(); t = scrub.value / 1000 * duration; show(t); syncMedia(t, false); };
    addEventListener("keydown", (e) => { if (e.code === "Space") { e.preventDefault(); playing ? pause() : play(); } });
    show(0);
  }
  function register(id, tl) { window.__timelines = window.__timelines || {}; window.__timelines[id] = tl; return tl; }

  window.MOTION = { version: 3, ease, E, bezier, logEase, lmix, clamp01, hitPulse, durFor, spring, SPRINGS, SPR, springStep, track, zoomTrack, beats, channels, sampled, rng, hash, svgEl,
    palette, words, revealWords, hideWords, riseWords, maskRise, typeOn, scramble, counter, drawPath, flowDash, morphPath, rain, vapour, sparkle,
    camera, push, breathe, flash, iris, flood, rackFocus, roll, polarity, squash, speedBlur, shot, cursor, cursorPath, moveCursor, press, grain, vignette, shim, register };
})();
