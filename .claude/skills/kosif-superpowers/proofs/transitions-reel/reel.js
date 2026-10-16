/* transitions-reel — timeline data (pure, no DOM). Shared by index.html and sound.py (`node reel.js > reel.json`).
 * Every cut lands on a beat of a 120 BPM grid (one cut per bar-half = every 1.0 s); each transition is centred on its cut.
 * Original code, MIT — part of KOSIF TOOL.
 */
(function (root) {
  'use strict';
  const BPM = 120, DURATION = 9.5;
  const CARDS = [
    { ar: 'ثمانية انتقالات', en: '8 TRANSITIONS', bg: ['#141824', '#262c40'], ink: '#ffffff', accent: '#ffcf4a', motif: 'rings' },
    { ar: 'قزحيّة دائرية', en: 'IRIS', bg: ['#ff5a36', '#ff8a3d'], ink: '#ffffff', accent: '#2b0f0a', motif: 'ring' },
    { ar: 'مسح بحافة ناعمة', en: 'SOFT WIPE', bg: ['#ffd23f', '#ffe27a'], ink: '#1d1a12', accent: '#e4572e', motif: 'stripes' },
    { ar: 'عبور بالتقريب', en: 'ZOOM THROUGH', bg: ['#16a69a', '#2ec4b6'], ink: '#ffffff', accent: '#0a3d38', motif: 'tunnel' },
    { ar: 'خلل لوني', en: 'RGB GLITCH', bg: ['#2a0a8a', '#4b1fc2'], ink: '#ffffff', accent: '#36f1cd', motif: 'pixels' },
    { ar: 'سحبة سريعة', en: 'WHIP PAN', bg: ['#e0136f', '#f72585'], ink: '#ffffff', accent: '#ffe066', motif: 'speed' },
    { ar: 'تسرّب ضوئي', en: 'LIGHT LEAK', bg: ['#0b132b', '#1c2541'], ink: '#fff4dc', accent: '#ff9f1c', motif: 'sun' },
    { ar: 'قناع شكل', en: 'SHAPE MASK', bg: ['#57cc99', '#80ed99'], ink: '#0f2a1d', accent: '#1b4332', motif: 'circle' },
    { ar: 'قطع متطابق', en: 'MATCH CUT · MORPH', bg: ['#3a56e0', '#4cc9f0'], ink: '#ffffff', accent: '#ffd166', motif: 'square' },
  ];
  // transition k brings card k in; cut (the instant the incoming card owns the frame) at t = k seconds = every 2 beats
  const TRANSITIONS = [
    null,
    { id: 'iris', dur: 0.5, ease: 'inOutCubic', note: 'circle clip r: 0 → 2100 px from the motif centre' },
    { id: 'wipe', dur: 0.45, ease: 'inOutQuint', note: 'right → left, 15° edge, 220 px feather' },
    { id: 'zoom', dur: 0.5, ease: 'inExpo | outExpo', note: 'out ×1 → ×6 + blur 0 → 18 px; in ×0.6 → ×1' },
    { id: 'glitch', dur: 0.32, ease: 'triangle', note: 'RGB split ±42 px, 9 slices ±140 px, seeded per frame' },
    { id: 'whip', dur: 0.4, ease: 'inOutQuart', note: 'velocity-matched: 12-sample shutter blur' },
    { id: 'leak', dur: 0.7, ease: 'sin(πu)^1.2', note: 'additive warm blobs, whiteout cut at u = 0.5' },
    { id: 'shape', dur: 0.55, ease: 'inOutCubic', note: 'rotating 6-point star mask 0 → 2600 px, 0 → 100°' },
    { id: 'match', dur: 0.6, ease: 'inOutCubic', note: 'circle r230 → rounded square 440/r60, cut at the morph midpoint' },
  ];
  for (let k = 1; k < TRANSITIONS.length; k++) { const tr = TRANSITIONS[k]; tr.cut = k * 1.0; tr.t0 = tr.cut - tr.dur / 2; tr.t1 = tr.cut + tr.dur / 2; }
  const REEL = { BPM, DURATION, CARDS, TRANSITIONS };
  root.REEL = REEL;
  if (typeof window === 'undefined' && typeof process !== 'undefined' && /reel\.js$/.test(process.argv[1] || '')) {
    process.stdout.write(JSON.stringify({ bpm: BPM, duration: DURATION, transitions: TRANSITIONS.slice(1) }, null, 1));
  }
})(typeof window !== 'undefined' ? window : globalThis);
