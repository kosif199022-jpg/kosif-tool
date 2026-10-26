/* KOSIF Motion Kit v2 — professional, deterministic motion helpers on top of GSAP, for HyperFrames compositions
   (window.__timelines, seconds) and for KOSIF Studio's own renderer (window.render(t) / window.__ready).
   Everything is keyed to the timeline; nothing uses the wall clock or unseeded randomness.
   Eases: the four named curves (slam / snap / drive / settle) and SPRINGS (snappy / default / heavy / playful):
   expensive motion has mass — it accelerates, overshoots a hair and settles. Word masks use clip-path (not
   overflow:hidden), so HyperFrames' layout check does not report the hidden words as overflowing. */
(function () {
  const ease = { slam: "expo.out", snap: "back.out(1.3)", drive: "power4.inOut", settle: "power4.out", linear: "none" };

  /* ── springs: a damped oscillator normalised to progress 0..1, usable as a GSAP ease function ── */
  const SPRINGS = { snappy: { zeta: 0.62, omega: 20 }, default: { zeta: 0.74, omega: 17 }, heavy: { zeta: 1.0, omega: 13 }, playful: { zeta: 0.45, omega: 18 } };
  function springFn(preset) {
    const s = typeof preset === "string" ? SPRINGS[preset] || SPRINGS.default : preset;
    const z = s.zeta, w = s.omega;
    const f = (t) => {
      if (z < 1) { const wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); }
      return 1 - Math.exp(-w * t) * (1 + w * t);
    };
    const end = f(1);                                       // the tween's duration maps to 1 s of spring time
    return (p) => f(p) / end;
  }
  const spring = (preset) => springFn(preset);
  /* a value that changes target several times (cursor, camera, width): one spring per change, continuous, from t */
  function track(t, keys, preset, settle) {
    const sp = springFn(preset || "default"), T = settle || 0.6;
    let v = keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [kt, kv] = keys[i];
      if (t <= kt) break;
      const p = Math.min(1, (t - kt) / T);
      v = v + (kv - v) * sp(p);
    }
    return v;
  }
  /* camera zoom interpolated in log space: 1x→2x feels as fast as 2x→4x */
  function zoomTrack(t, keys, preset, settle) {
    return Math.exp(track(t, keys.map(([kt, kv]) => [kt, Math.log(kv)]), preset, settle));
  }
  /* beats: picture and sound read the same clock */
  function beats(bpm, offset) { const b = 60 / bpm, o = offset || 0; return { at: (n) => o + n * b, len: (n) => n * b, bpm, beat: b }; }

  function rng(seed) {                                     // mulberry32: the same seed gives the same film
    let a = (seed >>> 0) || 1;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const SVG = "http://www.w3.org/2000/svg";
  function svgEl(tag, attrs, parent) {
    const el = document.createElementNS(SVG, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  }

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
    if (smallText) {
      const s = document.createElement("small");
      el.appendChild(s);
      addWords(s, smallText.trim().split(/\s+/));
    }
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
    tl.to(inners, { yPercent: o.to === "down" ? 115 : -115, opacity: 0, duration: o.dur || 0.45, stagger: o.stagger == null ? 0.04 : o.stagger, ease: ease.drive }, at);
    const num = el.querySelector(".num");
    if (num) tl.to(num, { scale: 0, opacity: 0, duration: 0.4, ease: ease.drive }, at);
    tl.set(el, { visibility: "hidden" }, at + (o.dur || 0.45) + 0.3);
  }

  /* ── strokes drawn on, like a pen ── */
  function drawPath(tl, path, at, dur, o) {
    o = o || {};
    const len = path.getTotalLength();
    path.style.strokeDasharray = len + " " + len;
    path.style.strokeDashoffset = len;
    tl.set(path, { opacity: o.opacity == null ? 1 : o.opacity }, at);          // visible only once the pen starts
    tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: o.ease || ease.drive, immediateRender: false }, at);
    if (o.head) {                                                             // an arrowhead that lands when the stroke arrives
      tl.fromTo(o.head, { scale: 0, opacity: 0, transformOrigin: o.headOrigin || "50% 50%" },
        { scale: 1, opacity: 1, duration: 0.35, ease: spring("snappy"), immediateRender: false }, at + dur - 0.1);
    }
    return len;
  }
  function flowDash(tl, path, at, dur, o) {           // a moving dash pattern along a path (river, current)
    o = o || {};
    const pat = o.pattern || "28 22";
    path.style.strokeDasharray = pat;
    const step = pat.split(" ").map(Number).reduce((a, b) => a + b, 0);
    tl.fromTo(path, { strokeDashoffset: 0 }, { strokeDashoffset: -step * (o.cycles || 6), duration: dur, ease: "none" }, at);
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
      if (ns) {
        d = svgEl("line", { x1: x, y1: y0 - l, x2: x + Math.tan(angle * Math.PI / 180) * l, y2: y0, stroke: o.color || "rgba(220,235,255,.75)", "stroke-width": w, "stroke-linecap": "round" }, container);
      } else {
        d = document.createElement("div");
        d.style.cssText = `position:absolute;left:${x}px;top:${y0 - l}px;width:${w}px;height:${l}px;border-radius:${w}px;background:${o.color || "rgba(220,235,255,.75)"};transform:rotate(${angle}deg)`;
        container.appendChild(d);
      }
      drops.push(d);
      const dur = fall * (0.75 + r() * 0.5), delay = r() * dur;
      tl.fromTo(d, { y: 0, opacity: 0.9 }, { y: (y1 - y0) + l, opacity: 0.6, duration: dur, ease: "none", repeat: Math.ceil(o.dur / dur) + 1 }, o.at - dur + delay);
    }
    tl.fromTo(container, { opacity: 0 }, { opacity: 1, duration: o.fadeIn || 0.6, ease: ease.drive }, o.at);
    tl.to(container, { opacity: 0, duration: o.fadeOut || 0.8, ease: ease.drive }, o.at + o.dur - (o.fadeOut || 0.8));
    return drops;
  }
  function vapour(tl, container, o) {                 // soft puffs rising, drifting, thinning
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
  function sparkle(tl, container, o) {                 // twinkling points (stars, glints)
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
    tl.to(stage, { x: o.x || 0, y: o.y || 0, scale: o.scale || 1, rotation: o.rotation || 0, duration: o.dur || 1.4, ease: o.ease || ease.drive, transformOrigin: o.origin || "50% 50%" }, at);
  }
  function flash(tl, el, at, o) {
    o = o || {};
    tl.fromTo(el, { opacity: 0 }, { opacity: o.peak || 0.85, duration: 0.06, ease: "none" }, at);
    tl.to(el, { opacity: 0, duration: o.dur || 0.35, ease: ease.settle }, at + 0.06);
    if (o.again) { tl.to(el, { opacity: (o.peak || 0.85) * 0.5, duration: 0.05 }, at + 0.16); tl.to(el, { opacity: 0, duration: 0.3 }, at + 0.21); }
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
    window.__duration = duration;
    window.__kosifSeek = seekAll;
    if (!window.__hf) {
      window.render = (t) => { window.__ready = false; seekAll(t); requestAnimationFrame(() => requestAnimationFrame(() => { window.__ready = true; })); };
      const ready = () => { seekAll(0); window.__ready = true; };
      (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(ready, ready);
    }
  }
  function register(id, tl) {
    window.__timelines = window.__timelines || {};
    window.__timelines[id] = tl;
    return tl;
  }

  window.MOTION = { ease, spring, SPRINGS, track, zoomTrack, beats, rng, svgEl, words, revealWords, hideWords, drawPath, flowDash, rain, vapour, sparkle, camera, flash, grain, vignette, shim, register };
})();
