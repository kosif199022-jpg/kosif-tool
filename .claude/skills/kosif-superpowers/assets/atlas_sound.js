// KOSIF Atlas Sound — original synthesized SFX kit (plain Web Audio, no audio files).
// Written for kosif-superpowers (A15). Same score function drives live playback and offline render.
//   score(k) { k.bed('room', 0, D); k.play('pop', 1.2); k.play('stroke', 2, { dur: 0.8, material: 'chalk' }); }
// Voice-over mode (k.vo === true): beds/music muted, sounds marked {minor:true} at ~60%, effects a little lower.
(function (root) {
  "use strict";
  const KS = (root.KSound = root.KSound || {});
  const EPS = 1e-4;
  const SEMI = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
  KS.hz = function (n) {
    if (typeof n === "number") return n;
    const m = /^([A-G])([#b]?)(-?\d)$/.exec(n); if (!m) throw new Error("bad note " + n);
    const s = SEMI[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + (parseInt(m[3], 10) + 1) * 12;
    return 440 * Math.pow(2, (s - 69) / 12);
  };
  function seeded(key) { let h = 2166136261 >>> 0; key = String(key); for (let i = 0; i < key.length; i++) { h ^= key.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return () => { h ^= h << 13; h >>>= 0; h ^= h >>> 17; h ^= h << 5; h >>>= 0; return h / 4294967296; }; }

  KS.NAMES = ["pop", "tick", "click", "tock", "blip", "whoosh", "swish", "riser", "thud", "impact", "stamp", "ding", "success", "error", "buzz", "sparkle", "glitch", "shutter", "count", "stroke", "paper", "slap", "tape", "press", "erase", "typing", "bell", "boot", "crtOn", "neon", "coin", "jump", "hurt", "powerup", "select", "drip", "chime"];
  KS.BEDS = ["room", "hiss", "hum", "rain", "projector", "vinyl", "water", "wind"];
  KS.MUSIC = ["pad", "pulse", "chip"];
  KS.MATERIALS = ["marker", "chalk", "pencil", "pen", "brush", "sharpie", "quill", "stylus"];

  KS.kit = function (ctx, opts) {
    const o = opts || {}, VO = !!o.voiceover, T0 = o.from || 0, base = ctx.currentTime + (o.delay || 0.03), SR = ctx.sampleRate;
    // snap starts to the sample grid (avoids level spikes from fractional starts)
    const at = (t) => (Math.round((base + (t - T0)) * SR) + 0.25) / SR;
    let minorDepth = 0;
    const master = ctx.createGain(); master.gain.value = o.master == null ? 0.9 : o.master;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -15; comp.knee.value = 6; comp.ratio.value = 3.5; comp.attack.value = 0.003; comp.release.value = 0.2;
    comp.connect(master); master.connect(o.dest || ctx.destination);
    const bus = {};
    for (const [name, g] of Object.entries({ sfx: VO ? 0.7 : 0.85, amb: 0.5, music: 0.42 })) { bus[name] = ctx.createGain(); bus[name].gain.value = g; bus[name].connect(comp); }
    // shared room reverb from decaying seeded noise
    const verb = ctx.createConvolver(), vlen = Math.floor(SR * 1.6), ir = ctx.createBuffer(2, vlen, SR), vr = seeded("verb");
    for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < vlen; i++) d[i] = (vr() * 2 - 1) * Math.pow(1 - i / vlen, 3.2); }
    verb.buffer = ir; const verbIn = ctx.createGain(); verbIn.gain.value = 0.32; verbIn.connect(verb); verb.connect(comp);
    // noise buffers
    const NB = {};
    for (const color of ["white", "pink", "brown"]) {
      const b = ctx.createBuffer(1, SR * 2, SR), d = b.getChannelData(0), r = seeded("n" + color); let l = 0, p0 = 0, p1 = 0;
      for (let i = 0; i < d.length; i++) { const w = r() * 2 - 1;
        if (color === "white") d[i] = w; else if (color === "pink") { p0 = 0.97 * p0 + w * 0.3; p1 = 0.6 * p1 + w * 0.5; d[i] = (p0 + p1) * 0.6; } else { l = (l + 0.02 * w) / 1.02; d[i] = l * 3.2; } }
      NB[color] = b;
    }
    const gainOf = (p, d) => { let g = p.gain == null ? d : p.gain; if (VO) g *= p.minor || minorDepth > 0 ? 0.6 : 0.85; return g; };
    function env(gn, t, p, peak) {
      const a = Math.max(0.001, p.a == null ? 0.004 : p.a), hold = p.hold || 0, dur = Math.max(a + hold + 0.01, p.dur || 0.2);
      gn.gain.setValueAtTime(EPS, at(t)); gn.gain.linearRampToValueAtTime(peak, at(t + a));
      gn.gain.setValueAtTime(peak, at(t + a + hold)); gn.gain.exponentialRampToValueAtTime(EPS, at(t + dur)); return dur;
    }
    function route(node, p) {
      let n = node;
      if (p.filter) { const f = ctx.createBiquadFilter(); f.type = p.filter; f.frequency.value = p.f2 || 1200; f.Q.value = p.q || 0.8; n.connect(f); n = f; }
      const pan = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
      if (pan) { pan.pan.value = p.pan || 0; n.connect(pan); n = pan; }
      n.connect(bus[p.bus || "sfx"]); if (p.verb) { const s = ctx.createGain(); s.gain.value = p.verb; n.connect(s); s.connect(verbIn); }
    }
    function freqParam(param, t, f) {
      if (Array.isArray(f)) { param.setValueAtTime(Math.max(20, KS.hz(f[0][1])), at(t)); for (const [dt, v] of f.slice(1)) param.exponentialRampToValueAtTime(Math.max(20, KS.hz(v)), at(t + dt)); }
      else param.setValueAtTime(KS.hz(f), at(t));
    }
    // ---- primitives
    function tone(t, p) {
      const osc = ctx.createOscillator(), g = ctx.createGain(); osc.type = p.type || "sine"; freqParam(osc.frequency, t, p.f || 440);
      if (p.detune) osc.detune.value = p.detune; osc.connect(g); route(g, p);
      const d = env(g, t, p, gainOf(p, 0.3)); osc.start(at(t)); osc.stop(at(t + d + 0.05));
    }
    function noise(t, p) {
      const s = ctx.createBufferSource(), g = ctx.createGain(); s.buffer = NB[p.color || "white"]; s.loop = true; s.playbackRate.value = p.rate || 1;
      s.connect(g); route(g, Object.assign({ filter: "bandpass", f2: p.f || 2000 }, p));
      const d = env(g, t, p, gainOf(p, 0.25)); s.start(at(t), (p.offset || 0) % 1.9); s.stop(at(t + d + 0.05));
    }
    // ---- named sounds (original designs)
    const S = {
      pop: (t, g, P) => { tone(t, { f: [[0, 520 * P], [0.06, 260 * P]], type: "sine", dur: 0.09, gain: 0.35 * g }); noise(t, { f: 3000, dur: 0.02, gain: 0.08 * g }); },
      tick: (t, g) => noise(t, { f: 6000, q: 4, dur: 0.018, gain: 0.25 * g }),
      click: (t, g) => { noise(t, { f: 3500, q: 2, dur: 0.012, gain: 0.3 * g }); tone(t, { f: 1800, type: "square", dur: 0.01, gain: 0.04 * g }); },
      tock: (t, g, P) => tone(t, { f: [[0, 700 * P], [0.05, 520 * P]], type: "triangle", dur: 0.08, gain: 0.28 * g }),
      blip: (t, g, P) => tone(t, { f: 880 * P, type: "square", dur: 0.06, gain: 0.07 * g, filter: "lowpass", f2: 3000 }),
      whoosh: (t, g, P, p) => noise(t, { color: "pink", f: [[0, 400], [p.dur || 0.5, 2400]], filter: "bandpass", f2: 900, a: (p.dur || 0.5) * 0.6, dur: p.dur || 0.5, gain: 0.3 * g, pan: p.pan }),
      swish: (t, g) => noise(t, { f: 2500, q: 1.4, a: 0.05, dur: 0.18, gain: 0.22 * g }),
      riser: (t, g, P, p) => { const d = p.dur || 1.2; noise(t, { color: "pink", filter: "highpass", f2: 600, a: d * 0.95, dur: d, gain: 0.18 * g }); tone(t, { f: [[0, 200], [d, 900]], type: "sawtooth", a: d * 0.9, dur: d, gain: 0.04 * g, filter: "lowpass", f2: 1500 }); },
      thud: (t, g, P) => { tone(t, { f: [[0, 120 * P], [0.15, 45]], dur: 0.25, gain: 0.55 * g }); noise(t, { color: "brown", filter: "lowpass", f2: 300, dur: 0.12, gain: 0.3 * g }); },
      impact: (t, g, P) => { tone(t, { f: [[0, 90 * P], [0.3, 38]], dur: 0.45, gain: 0.6 * g, verb: 0.2 }); noise(t, { f: 1200, q: 0.5, dur: 0.25, gain: 0.3 * g, verb: 0.3 }); },
      stamp: (t, g) => { tone(t, { f: [[0, 160], [0.08, 70]], dur: 0.12, gain: 0.5 * g }); noise(t, { f: 900, q: 0.7, dur: 0.07, gain: 0.35 * g }); },
      ding: (t, g, P) => { tone(t, { f: 1318 * P, dur: 1.2, gain: 0.18 * g, verb: 0.35 }); tone(t, { f: 2637 * P, dur: 0.6, gain: 0.05 * g }); },
      success: (t, g, P) => ["C5", "E5", "G5", "C6"].forEach((n, i) => tone(t + i * 0.07, { f: KS.hz(n) * P, type: "triangle", dur: 0.5, gain: 0.13 * g, verb: 0.3 })),
      error: (t, g) => { tone(t, { f: 180, type: "square", dur: 0.16, gain: 0.08 * g, filter: "lowpass", f2: 900 }); tone(t + 0.18, { f: 150, type: "square", dur: 0.22, gain: 0.08 * g, filter: "lowpass", f2: 900 }); },
      buzz: (t, g, P, p) => tone(t, { f: 110, type: "sawtooth", dur: p.dur || 0.4, hold: (p.dur || 0.4) * 0.7, gain: 0.06 * g, filter: "bandpass", f2: 900 }),
      sparkle: (t, g) => { const r = seeded("sp" + t); for (let i = 0; i < 6; i++) tone(t + i * 0.045, { f: 2400 + r() * 2600, dur: 0.18, gain: 0.05 * g, verb: 0.4, pan: r() * 1.4 - 0.7 }); },
      glitch: (t, g) => { const r = seeded("gl" + t); for (let i = 0; i < 5; i++) tone(t + i * 0.025, { f: 200 + r() * 2000, type: "square", dur: 0.02, gain: 0.06 * g }); },
      shutter: (t, g) => { noise(t, { f: 5000, q: 3, dur: 0.02, gain: 0.3 * g }); noise(t + 0.06, { f: 3000, q: 3, dur: 0.03, gain: 0.25 * g }); },
      count: (t, g, P, p) => { const n = p.n || 8, d = p.dur || 1, r = seeded("ct" + t); for (let i = 0; i < n; i++) { const u = i / n, tt = t + d * (1 - Math.pow(1 - u, 1.8)); noise(tt, { f: 4500 + r() * 800, q: 5, dur: 0.015, gain: 0.18 * g }); } },
      // stroke: a drawing stroke over dur seconds; material shapes the band of the scrape
      stroke: (t, g, P, p) => {
        const M = { marker: [2600, 1.2, 0.22], chalk: [3400, 0.6, 0.3], pencil: [5200, 1.5, 0.12], pen: [4200, 2, 0.1], brush: [1400, 0.7, 0.14], sharpie: [2200, 1.4, 0.2], quill: [4800, 2.5, 0.1], stylus: [3000, 3, 0.08] }[p.material || "marker"] || [2600, 1.2, 0.2];
        const d = p.dur || 0.6; noise(t, { f: M[0], q: M[1], a: 0.03, hold: d * 0.8, dur: d, gain: M[2] * g, rate: 0.8 + (p.speed || 0) * 0.4, pan: p.pan });
        if (p.material === "chalk") { const r = seeded("ck" + t); for (let i = 0; i < d * 14; i++) noise(t + r() * d, { f: 5000, q: 6, dur: 0.01, gain: 0.08 * g }); }
      },
      paper: (t, g, P, p) => noise(t, { color: "pink", f: p.kind === "turn" ? 1800 : 2600, q: 0.6, a: 0.04, dur: p.kind === "turn" ? 0.45 : 0.25, gain: 0.25 * g }),
      slap: (t, g) => { noise(t, { f: 1800, q: 0.5, dur: 0.06, gain: 0.45 * g }); tone(t, { f: [[0, 220], [0.05, 90]], dur: 0.08, gain: 0.25 * g }); },
      tape: (t, g) => noise(t, { f: 4200, q: 1.5, a: 0.02, hold: 0.25, dur: 0.35, gain: 0.12 * g }),
      press: (t, g) => { tone(t, { f: [[0, 70], [0.2, 40]], dur: 0.3, gain: 0.45 * g }); noise(t, { color: "brown", filter: "lowpass", f2: 500, dur: 0.2, gain: 0.25 * g }); },
      erase: (t, g, P, p) => noise(t, { color: "pink", f: 1100, q: 0.8, a: 0.05, hold: (p.dur || 0.6) * 0.7, dur: p.dur || 0.6, gain: 0.22 * g }),
      typing: (t, g, P, p) => { const n = p.n || 10, r = seeded("ty" + t); for (let i = 0; i < n; i++) noise(t + i * (p.gap || 0.07) + r() * 0.02, { f: 3000 + r() * 1500, q: 3, dur: 0.02, gain: 0.2 * g }); },
      bell: (t, g) => [1, 2.76, 5.4].forEach((m, i) => tone(t, { f: 880 * m, dur: 1.6 / (i + 1), gain: 0.12 * g / (i + 1), verb: 0.4 })),
      boot: (t, g) => { tone(t, { f: [[0, 60], [0.4, 120]], type: "sawtooth", a: 0.3, dur: 0.6, gain: 0.05 * g, filter: "lowpass", f2: 600 }); tone(t + 0.35, { f: 1046, type: "square", dur: 0.12, gain: 0.05 * g }); },
      crtOn: (t, g) => { noise(t, { f: 9000, q: 1, dur: 0.15, gain: 0.15 * g }); tone(t, { f: 15600, dur: 0.8, gain: 0.015 * g }); tone(t, { f: [[0, 50], [0.1, 30]], dur: 0.2, gain: 0.3 * g }); },
      neon: (t, g, P, p) => { const r = seeded("ne" + t); for (let i = 0; i < 4; i++) noise(t + r() * 0.2, { f: 3000, q: 2, dur: 0.02, gain: 0.15 * g }); tone(t + 0.15, { f: 120, type: "sawtooth", dur: p.dur || 0.8, hold: 0.5, gain: 0.03 * g, filter: "bandpass", f2: 1200 }); },
      coin: (t, g) => { tone(t, { f: 988, type: "square", dur: 0.06, gain: 0.06 * g }); tone(t + 0.06, { f: 1319, type: "square", dur: 0.3, gain: 0.06 * g }); },
      jump: (t, g) => tone(t, { f: [[0, 300], [0.15, 900]], type: "square", dur: 0.18, gain: 0.06 * g }),
      hurt: (t, g) => { tone(t, { f: [[0, 400], [0.2, 90]], type: "square", dur: 0.22, gain: 0.07 * g }); noise(t, { f: 1500, dur: 0.15, gain: 0.08 * g }); },
      powerup: (t, g) => ["C5", "E5", "G5", "C6", "E6"].forEach((n, i) => tone(t + i * 0.05, { f: KS.hz(n), type: "square", dur: 0.08, gain: 0.05 * g })),
      select: (t, g) => tone(t, { f: 1568, type: "square", dur: 0.05, gain: 0.05 * g }),
      drip: (t, g, P) => tone(t, { f: [[0, 900 * P], [0.08, 1700 * P]], dur: 0.12, gain: 0.15 * g, verb: 0.3 }),
      chime: (t, g, P) => ["E5", "B5"].forEach((n, i) => tone(t + i * 0.12, { f: KS.hz(n) * P, dur: 0.9, gain: 0.1 * g, verb: 0.4 })),
    };
    function play(name, t, p) {
      p = p || {}; const fn = S[name]; if (!fn) throw new Error("unknown sound: " + name);
      fn(t, p.gain == null ? 1 : p.gain, p.pitch || 1, p);
    }
    // ---- beds: continuous ambience under [t0,t1]
    function bed(name, t0, t1, p) {
      if (VO) return; p = p || {}; const d = t1 - t0, g = p.gain == null ? 1 : p.gain, fade = Math.min(0.5, d / 4);
      const L = (q) => Object.assign({ dur: d, a: fade, hold: Math.max(0, d - 2 * fade), bus: "amb" }, q);
      const B = {
        room: () => noise(t0, L({ color: "brown", filter: "lowpass", f2: 400, gain: 0.08 * g })),
        hiss: () => noise(t0, L({ color: "white", filter: "highpass", f2: 6000, gain: 0.02 * g })),
        hum: () => { tone(t0, L({ f: 50, gain: 0.03 * g })); tone(t0, L({ f: 100, gain: 0.012 * g })); },
        rain: () => noise(t0, L({ color: "pink", filter: "bandpass", f2: 3500, q: 0.4, gain: 0.07 * g })),
        projector: () => { noise(t0, L({ color: "pink", filter: "bandpass", f2: 1800, gain: 0.03 * g })); for (let x = t0; x < t1; x += 1 / 12) noise(x, { f: 2500, q: 4, dur: 0.02, gain: 0.03 * g, bus: "amb" }); },
        vinyl: () => { noise(t0, L({ color: "brown", filter: "lowpass", f2: 800, gain: 0.03 * g })); const r = seeded("vy"); for (let x = t0; x < t1; x += 0.08 + r() * 0.4) noise(x, { f: 5000, q: 2, dur: 0.008, gain: 0.05 * g, bus: "amb" }); },
        water: () => noise(t0, L({ color: "brown", filter: "lowpass", f2: 260, gain: 0.12 * g, rate: 0.6 })),
        wind: () => noise(t0, L({ color: "pink", filter: "bandpass", f2: 700, q: 0.7, gain: 0.06 * g, rate: 0.5 })),
      };
      if (!B[name]) throw new Error("unknown bed: " + name); B[name]();
    }
    // ---- music: light harmonic beds that sit under the effects
    function music(name, t0, t1, p) {
      if (VO) return; p = p || {}; const bpm = p.bpm || 84, g = p.gain == null ? 0.6 : Math.min(0.6, p.gain), bar = (60 / bpm) * 4;
      const chords = p.chords || [["C4", "E4", "G4", "B4"], ["A3", "C4", "E4", "G4"], ["F3", "A3", "C4", "E4"], ["G3", "B3", "D4", "F4"]];
      for (let k = 0, t = t0; t < t1 - 0.05; k++, t += bar) {
        const ch = chords[k % chords.length], len = Math.min(bar, t1 - t);
        if (name === "pad") ch.forEach((n, i) => tone(t, { f: KS.hz(n), type: "sine", a: 0.4, hold: len * 0.6, dur: len + 0.3, gain: 0.035 * g, bus: "music", pan: (i - 1.5) * 0.25, verb: 0.3 }));
        else if (name === "pulse") for (let s = 0; s < 8 && t + s * bar / 8 < t1; s++) tone(t + s * bar / 8, { f: KS.hz(ch[s % ch.length]) / 2, type: "triangle", dur: bar / 9, gain: 0.05 * g, bus: "music", filter: "lowpass", f2: 1400 });
        else if (name === "chip") for (let s = 0; s < 8 && t + s * bar / 8 < t1; s++) tone(t + s * bar / 8, { f: KS.hz(ch[(s * 3) % ch.length]), type: "square", dur: bar / 10, gain: 0.025 * g, bus: "music" });
        else throw new Error("unknown music: " + name);
      }
    }
    function withMinor(fn) { minorDepth++; try { fn(); } finally { minorDepth--; } }
    return { play, tone, noise, bed, music, withMinor, vo: VO, names: Object.keys(S) };
  };

  // live playback from explainer time fromT; returns stop()
  KS.live = function (score, fromT, opts) {
    const o = opts || {}; const AC = root.AudioContext || root.webkitAudioContext; const ctx = o.ctx || new AC();
    const out = ctx.createGain(); out.connect(ctx.destination);
    const k = KS.kit(ctx, Object.assign({}, o, { from: fromT || 0, dest: out }));
    try { score(k); } catch (e) { console.warn("score error", e); }
    return function stop() { try { out.gain.setValueAtTime(0, ctx.currentTime); out.disconnect(); } catch (e) { /* already stopped */ } };
  };
  // offline render -> interleaved stereo Float32Array (for video muxing)
  KS.renderOffline = async function (score, duration, sampleRate, opts) {
    const sr = sampleRate || 48000, ctx = new OfflineAudioContext(2, Math.ceil(duration * sr), sr);
    const k = KS.kit(ctx, Object.assign({}, opts || {}, { delay: 0 })); score(k);
    const buf = await ctx.startRendering(), L = buf.getChannelData(0), R = buf.getChannelData(1), out = new Float32Array(L.length * 2);
    for (let i = 0; i < L.length; i++) { out[2 * i] = L[i]; out[2 * i + 1] = R[i]; }
    return out;
  };
})(typeof window !== "undefined" ? window : globalThis);
