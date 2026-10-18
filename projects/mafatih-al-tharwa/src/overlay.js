/* مفاتيح الثروة — deterministic motion overlay.
 * Every frame is a pure function of t (seconds): window.__kosif.seek(t) draws it.
 * The voice is the master clock; all times below come from words.json. */
(function () {
  'use strict';
  const DURATION = 640.29, FPS = 30;
  const CAPS = window.CAPTIONS || [], CUTS = window.CUTS || [];
  const $ = (s) => document.querySelector(s);

  /* ---------- easing & timing ---------- */
  const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
  const E = {
    lin: (x) => x,
    out3: (x) => 1 - Math.pow(1 - x, 3),
    out5: (x) => 1 - Math.pow(1 - x, 5),
    inOut3: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    back: (x) => { const s = 1.6; return x >= 1 ? 1 : 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); },
    spring: (x) => { if (x >= 1) return 1; const w = 13, z = 0.38, wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * x) * (Math.cos(wd * x) + (z * w / wd) * Math.sin(wd * x)); },
  };
  const P = (t, a, d, e = E.out3) => e(clamp01((t - a) / d));          // progress from a over d seconds
  const env = (t, a, b, fi = 0.35, fo = 0.35) => Math.min(P(t, a, fi, E.out3), 1 - P(t, b - fo, fo, E.inOut3));
  const lerp = (a, b, p) => a + (b - a) * p;
  function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let z = s; z = Math.imul(z ^ (z >>> 15), z | 1); z ^= z + Math.imul(z ^ (z >>> 7), z | 61); return ((z ^ (z >>> 14)) >>> 0) / 4294967296; }; }
  const fmt = (n) => Math.round(n).toLocaleString('en-US');

  /* ---------- tiny DOM helpers ---------- */
  function el(tag, cls, parent, html, style) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    if (style) Object.assign(e.style, style);
    if (parent) parent.appendChild(e);
    return e;
  }
  const SVGNS = 'http://www.w3.org/2000/svg';
  function svg(parent, vb, w, h, inner, style) {
    const s = document.createElementNS(SVGNS, 'svg');
    s.setAttribute('viewBox', vb); s.setAttribute('width', w); s.setAttribute('height', h);
    s.innerHTML = inner; s.style.position = 'absolute'; s.style.overflow = 'visible';
    Object.assign(s.style, style || {}); parent.appendChild(s);
    s.querySelectorAll('.draw').forEach((p) => { p.setAttribute('pathLength', '1'); p.style.strokeDasharray = '1 1'; p.style.strokeDashoffset = '1'; });
    return s;
  }
  const drawPaths = (s, t, a, d, stagger = 0.12) => s.querySelectorAll('.draw').forEach((p, i) => { p.style.strokeDashoffset = String(1 - P(t, a + i * stagger, d, E.inOut3)); });
  const wipe = (e, p) => { e.style.clipPath = `inset(-30% 0 -30% ${(1 - clamp01(p)) * 100}%)`; };     // reveal right → left
  const pop = (e, p, y = 26) => { e.style.opacity = clamp01(p * 1.6); e.style.transform = `translateY(${(1 - E.back(clamp01(p))) * y}px) scale(${lerp(0.82, 1, E.back(clamp01(p)))})`; };
  const rise = (e, p, y = 40) => { e.style.opacity = p; e.style.transform = `translateY(${(1 - p) * y}px)`; };

  /* ---------- hero framework ---------- */
  const heroesRoot = $('#heroes');
  const HEROES = [];
  function hero(t0, t1, scrim, build) {
    const root = el('div', 'hero abs card', heroesRoot);
    const h = { t0, t1, scrim, root, update: build(root, t0, t1) };
    HEROES.push(h); return h;
  }
  const text = (parent, html, cls, style) => el('div', 'abs ' + (cls || ''), parent, html, style);

  /* reusable hero types */
  function nameCard(t0, t1, name, sub, subT, chips = []) {
    return hero(t0, t1, 0, (r) => {
      const panel = text(r, '', '', { left: '-60px', top: '430px', width: '1080px', height: '330px', background: 'linear-gradient(rgba(8,6,4,0), rgba(8,6,4,.85) 40%, rgba(8,6,4,.6))' });
      const bar = text(r, '', '', { right: '44px', top: '548px', width: '10px', height: '150px', background: 'var(--gold)', transformOrigin: '50% 100%' });
      const n = text(r, name, 'kufi', { right: '76px', top: '532px', fontSize: '92px', lineHeight: '1.25', color: 'var(--cream)', whiteSpace: 'nowrap' });
      const s = text(r, sub, '', { right: '80px', top: '650px', font: '700 38px/1.2 var(--sans)', color: 'var(--gold)', whiteSpace: 'nowrap' });
      const cs = chips.map(([c, ct], i) => [text(r, c, 'pill', { left: `${44 + i * 0}px`, top: `${44 + i * 96}px`, fontSize: '40px' }), ct]);
      return (t) => {
        panel.style.opacity = P(t, t0, 0.4);
        bar.style.transform = `scaleY(${P(t, t0 + 0.05, 0.45, E.out5)})`;
        wipe(n, P(t, t0 + 0.15, 0.6, E.out3));
        n.style.transform = `translateX(${(1 - P(t, t0 + 0.15, 0.8)) * -30}px)`;
        rise(s, P(t, subT, 0.45), 18);
        cs.forEach(([c, ct]) => pop(c, P(t, ct - 0.08, 0.4)));
      };
    });
  }

  function quote(t0, t1, lines, opts = {}) {
    // lines: [html, time, {size, cls, color, top}]
    return hero(t0, t1, opts.scrim ?? 0.82, (r) => {
      if (opts.ornament !== false) svg(r, '0 0 400 40', 400, 40, '<path class="draw" d="M0 20 H160 M240 20 H400" stroke-width="3"/><path class="draw" d="M200 4 L216 20 L200 36 L184 20 Z" stroke-width="3"/>', { left: '280px', top: `${opts.ornTop ?? 70}px` });
      const orn = r.querySelector('svg');
      const els = lines.map(([h, lt, o = {}]) => [text(r, h, 'center ' + (o.cls || 'kufi'), { top: `${o.top}px`, fontSize: `${o.size || 92}px`, lineHeight: '1.3', color: o.color || 'var(--cream)' }), lt, o]);
      return (t) => {
        if (orn) drawPaths(orn, t, t0, 0.8);
        els.forEach(([e, lt, o]) => {
          const p = P(t, lt - 0.1, 0.55, E.out3);
          if (o.wipe === false) rise(e, p, 30); else { wipe(e, p); e.style.opacity = clamp01(p * 3); e.style.transform = `translateY(${(1 - p) * 18}px)`; }
        });
      };
    });
  }

  function counter(r, t, { from = 0, to, a, b, top, size = 190, prefix = '', suffix = '', cls = 'goldText' }) {
    if (!r._ctr) r._ctr = {};
    const key = `${top}-${to}`;
    const e = r._ctr[key] || (r._ctr[key] = text(r, '<bdi class="num"></bdi><span></span>', 'center ' + cls, { top: `${top}px`, fontSize: `${size}px`, lineHeight: '1.15', fontWeight: '900', whiteSpace: 'nowrap' }));
    const p = P(t, a, b - a, E.out5);
    e.firstChild.textContent = prefix + fmt(lerp(from, to, p));
    e.lastChild.textContent = suffix ? ' ' + suffix.trim() : '';
    e.style.opacity = P(t, a - 0.25, 0.3);
    e.style.transform = `scale(${lerp(0.9, 1, E.back(P(t, a - 0.25, 0.5)))})`;
    return e;
  }

  function stampEl(r, label, top, color = 'var(--red)') {
    return text(r, label, 'center kufi', { top: `${top}px`, fontSize: '150px', color, lineHeight: '1.2' });
  }
  function stamp(e, t, a) {
    const p = P(t, a, 0.32, E.lin);
    const s = lerp(2.4, 1, E.out5(p));
    const shake = p >= 1 ? Math.sin((t - a) * 60) * 6 * Math.exp(-(t - a - 0.32) * 9) : 0;
    e.style.opacity = clamp01(p * 2.5);
    e.style.transform = `translateX(${shake}px) rotate(-7deg) scale(${s})`;
    e.style.filter = `drop-shadow(0 0 ${lerp(40, 10, p)}px rgba(217,87,63,.55))`;
  }

  function book(r, { title, author, left = 300, top = 70, w = 360, h = 500 }) {
    const scene = text(r, '', '', { left: `${left}px`, top: `${top}px`, width: `${w}px`, height: `${h}px`, perspective: '1400px' });
    const b = el('div', '', scene, '', { position: 'absolute', inset: '0', transformStyle: 'preserve-3d' });
    el('div', '', b, '', { position: 'absolute', top: '0', width: '46px', height: `${h}px`, right: '-46px', background: 'linear-gradient(90deg,#3a2a12,#6d5022,#2a1e0d)', transform: 'rotateY(90deg)', transformOrigin: '0 50%' });
    const cover = el('div', '', b, `
      <div style="position:absolute;inset:18px;border:3px solid #e2b65c;border-radius:6px"></div>
      <div style="position:absolute;inset:30px;border:1px solid rgba(226,182,92,.6);border-radius:4px"></div>
      <svg viewBox="0 0 80 80" style="position:absolute;left:${w / 2 - 44}px;top:60px;width:88px;height:88px"><g fill="none" stroke="#e2b65c" stroke-width="5" stroke-linecap="round"><circle cx="24" cy="40" r="15"/><path d="M39 40 H72 M62 40 V52 M70 40 V49"/></g></svg>
      <div class="naskh goldText" style="position:absolute;left:30px;right:30px;top:${h * 0.36}px;text-align:center;font-size:${w * 0.19}px;line-height:1.35">${title}</div>
      <div style="position:absolute;left:30px;right:30px;bottom:56px;text-align:center;font:700 ${w * 0.085}px var(--sans);color:#e9d3a0">${author}</div>
      <div class="shine" style="position:absolute;inset:0;background:linear-gradient(105deg,transparent 35%,rgba(255,240,200,.38) 50%,transparent 65%);background-size:300% 100%"></div>`,
      { position: 'absolute', inset: '0', borderRadius: '8px 4px 4px 8px', overflow: 'hidden', background: 'radial-gradient(ellipse at 40% 30%, #3b2a14, #120c06 75%)', boxShadow: '0 40px 90px rgba(0,0,0,.7), 0 0 60px rgba(226,182,92,.18)' });
    const shine = cover.querySelector('.shine');
    return (t, a) => {
      const p = P(t, a, 1.1, E.out5);
      scene.style.opacity = clamp01(p * 2);
      const idle = Math.sin((t - a) * 0.8) * 4;
      b.style.transform = `translateY(${(1 - p) * 80}px) rotateY(${lerp(-75, -16, p) + idle}deg) rotateX(${lerp(14, 4, p)}deg)`;
      shine.style.backgroundPosition = `${lerp(120, -40, P(t, a + 0.6, 1.4, E.inOut3))}% 0`;
    };
  }

  /* ---------- the edit: hero moments keyed to the voice ---------- */
  // 1. Title
  hero(3.9, 14.45, 0.92, (r, t0) => {
    const key = svg(r, '0 0 300 120', 420, 168, '<circle class="draw" cx="62" cy="60" r="44" stroke-width="10"/><circle class="draw" cx="62" cy="60" r="14" stroke-width="7"/><path class="draw" d="M106 60 H286 M246 60 V94 M272 60 V86" stroke-width="10"/>', { left: '270px', top: '70px', filter: 'drop-shadow(0 0 22px rgba(226,182,92,.5))' });
    const row = text(r, '', 'center', { top: '240px', display: 'flex', justifyContent: 'center', gap: '0 40px' });
    const w1 = el('div', 'kufi goldText', row, 'مفاتيح', { fontSize: '170px', lineHeight: '1.25' });
    const w2 = el('div', 'kufi goldText', row, 'الثروة', { fontSize: '170px', lineHeight: '1.25' });
    const tags = [['معرفة منظمة', 9.75], ['عالمية', 10.6]].map(([s, a], i) => [text(r, s, 'pill', { [i ? 'left' : 'right']: i ? '230px' : '170px', top: '500px' }), a]);
    const lbl = text(r, 'عمرها أكثر من', 'center', { top: '600px', font: '700 40px var(--sans)', color: 'var(--muted)' });
    return (t) => {
      drawPaths(key, t, t0 + 0.2, 1.2, 0.25);
      key.style.transform = `rotate(${lerp(-14, 0, P(t, t0 + 0.2, 1.6, E.out5))}deg)`;
      wipe(w1, P(t, 5.95, 0.55)); wipe(w2, P(t, 6.42, 0.6));
      const up = P(t, 9.4, 0.6, E.inOut3);
      [w1, w2].forEach((w) => { w.style.transform = `translateY(${-up * 60}px) scale(${1 - up * 0.18})`; });
      key.style.top = `${70 - up * 40}px`;
      tags.forEach(([e, a]) => { pop(e, P(t, a, 0.45)); e.style.top = `${lerp(500, 400, up)}px`; });
      const c = P(t, 11.9, 0.3);
      lbl.style.opacity = c; lbl.style.top = '520px';
      [w1, w2, key, ...tags.map((x) => x[0])].forEach((e) => { e.style.filter = `blur(${c * 0}px)`; });
      counter(r, t, { to: 100, a: 12.2, b: 14.05, top: 560, size: 120, prefix: '+', suffix: ' عام', cls: 'goldText' });
    };
  });
  // 2. Andrew Carnegie
  nameCard(19.9, 28.2, 'أندرو كارنيجي', 'رجل أعمال مليونير', 23.4, [['المناجم', 25.87], ['الحديد', 26.45]]);
  // 3. wisdom dies with them
  quote(28.6, 41.0, [
    ['الأثرياء وأصحاب الملايين', 28.85, { top: 150, size: 70, cls: 'kufi' }],
    ['يموتون…', 33.27, { top: 260, size: 84, color: 'var(--muted)' }],
    ['وتموت <span class="goldText">الحكمة</span> معهم', 35.55, { top: 370, size: 104 }],
    ['والجيل القادم يحتاج لهذه المعرفة', 37.5, { top: 540, size: 50, cls: 'sans', color: 'var(--gold)' }],
  ]);
  // 4. give me a young man
  quote(48.9, 55.9, [
    ['«أعطوني شابًّا»', 49.0, { top: 200, size: 120, cls: 'naskh goldText' }],
    ['أعلّمه… وأعرّفه على هؤلاء', 51.0, { top: 400, size: 64 }],
  ]);
  // 5. Napoleon Hill
  nameCard(58.3, 66.5, 'نابليون هيل', 'أخذ العلم والمعرفة من كارنيجي نفسه', 63.9);
  // 6. 500 millionaires
  hero(69.3, 86.2, 0.88, (r, t0) => {
    const R = rng(500), n = 500, cols = 50;
    const field = text(r, '', '', { left: '58px', top: '345px', width: '850px', height: '260px' });
    const order = Array.from({ length: n }, (_, i) => i).sort(() => R() - 0.5);
    const rank = new Array(n); order.forEach((v, i) => { rank[v] = i; });
    const dots = Array.from({ length: n }, (_, i) => el('i', '', field, '', { position: 'absolute', left: `${(i % cols) * 17}px`, top: `${Math.floor(i / cols) * 25}px`, width: '9px', height: '9px', borderRadius: '50%', background: 'var(--gold)' }));
    const lbl = text(r, 'التقى مع', 'center', { top: '40px', font: '700 46px var(--sans)', color: 'var(--muted)' });
    const sfx = text(r, 'مليونير', 'center kufi', { top: '265px', fontSize: '56px', color: 'var(--cream)' });
    const chips = [['ثري', 81.39], ['رجل أعمال', 81.79], ['ناجح', 82.67]].map(([s, a], i) => [text(r, s, 'pill', { top: '420px', left: `${[640, 330, 110][i]}px` }), a]);
    const q = text(r, 'ما أسباب النجاح؟', 'center kufi goldText', { top: '540px', fontSize: '96px' });
    return (t) => {
      rise(lbl, P(t, t0 + 0.1, 0.5), 20);
      counter(r, t, { to: 500, a: 69.8, b: 71.5, top: 90, size: 180 });
      rise(sfx, P(t, 71.1, 0.4), 20);
      const fill = P(t, 69.8, 1.7, E.out3) * n, phase2 = P(t, 79.0, 0.6, E.inOut3);
      dots.forEach((d, i) => {
        const on = rank[i] < fill;
        d.style.opacity = on ? (0.55 + 0.45 * Math.sin(t * 2 + i)) * (1 - phase2 * 0.7) : 0.08;
        d.style.transform = `scale(${on ? 1 : 0.6})`;
      });
      field.style.transform = `translateY(${phase2 * -40}px) scale(${1 - phase2 * 0.15})`;
      chips.forEach(([e, a]) => pop(e, P(t, a - 0.05, 0.45)));
      wipe(q, P(t, 84.8, 0.6)); q.style.opacity = P(t, 84.7, 0.2);
    };
  });
  // 7. how they act, think, talk
  hero(88.7, 95.4, 0.86, (r, t0) => {
    const head = svg(r, '0 0 200 220', 260, 286, '<path class="draw" stroke-width="6" d="M100 20 C55 20 35 55 38 92 C40 120 52 135 52 160 L52 200 L140 200 L140 172 C160 172 170 160 168 140 L180 132 L166 110 C168 60 145 20 100 20 Z"/><path class="draw" stroke-width="5" d="M82 70 C95 58 120 60 128 78 C138 80 140 100 126 106 C120 120 92 118 88 104 C72 102 70 80 82 70 Z"/>', { left: '350px', top: '200px', filter: 'drop-shadow(0 0 18px rgba(226,182,92,.45))' });
    const items = [['أفعاله؟', 89.65, 640, 120], ['الطرق؟', 91.23, 90, 160], ['كيف يفكر؟', 92.61, 640, 520], ['كيف يتكلم؟', 93.37, 60, 540]].map(([s, a, x, y]) => [text(r, s, 'pill', { left: `${x}px`, top: `${y}px` }), a]);
    return (t) => {
      drawPaths(head, t, t0, 1.0, 0.3);
      items.forEach(([e, a], i) => { pop(e, P(t, a - 0.05, 0.45)); e.style.translate = `0 ${Math.sin(t * 1.4 + i) * 6}px`; });
    };
  });
  // 8. massive information → one book
  hero(97.5, 104.85, 0.86, (r, t0) => {
    const R = rng(77);
    const bits = Array.from({ length: 64 }, () => ({ x: R() * 820 + 40, y: R() * 560 + 110, r: R() * 60 - 30, d: R() * 0.8 }));
    const els = bits.map(() => el('i', '', r, '', { position: 'absolute', width: '46px', height: '30px', border: '2px solid var(--gold)', borderRadius: '3px', background: 'rgba(226,182,92,.12)' }));
    const l1 = text(r, 'معلومات هائلة جدًا', 'center kufi', { top: '24px', fontSize: '74px' });
    const l2 = text(r, 'في كتاب واحد', 'center kufi goldText', { top: '560px', fontSize: '96px' });
    const bk = svg(r, '0 0 120 150', 170, 212, '<path class="draw" stroke-width="6" d="M14 10 H96 a10 10 0 0 1 10 10 V140 H24 a10 10 0 0 1 -10 -10 Z"/><path class="draw" stroke-width="5" d="M14 130 a10 10 0 0 1 10 -10 H106 M36 44 H86 M36 64 H76"/>', { left: '395px', top: '250px', filter: 'drop-shadow(0 0 26px rgba(226,182,92,.6))' });
    return (t) => {
      rise(l1, P(t, t0 + 0.1, 0.5), 20);
      const g = P(t, 100.1, 3.0, E.inOut3);
      els.forEach((e, i) => {
        const b = bits[i], appear = P(t, t0 + b.d, 0.5);
        const gx = lerp(b.x, 457, g), gy = lerp(b.y, 340, g);
        e.style.opacity = appear * (1 - P(t, 102.6 + b.d * 0.5, 0.4));
        e.style.transform = `translate(${gx}px, ${gy + Math.sin(t * 2 + i) * 8 * (1 - g)}px) rotate(${b.r * (1 - g)}deg) scale(${1 - g * 0.5})`;
      });
      drawPaths(bk, t, 102.7, 0.8, 0.2);
      bk.style.transform = `scale(${lerp(0.7, 1, E.back(P(t, 102.7, 0.6)))})`;
      wipe(l2, P(t, 103.0, 0.6));
    };
  });
  // 9. Think and Grow Rich, 100 million copies
  hero(104.85, 116.6, 0.9, (r) => {
    const bk = book(r, { title: 'فكّر<br>وازدد ثراءً', author: 'نابليون هيل', left: 300, top: 28, w: 360, h: 470 });
    const lbl = text(r, 'غيّر حياة ملايين الناس', 'center kufi', { top: '520px', fontSize: '62px', color: 'var(--cream)' });
    return (t) => {
      bk(t, 104.9);
      const sw = P(t, 112.0, 0.4, E.inOut3);
      rise(lbl, P(t, 110.3, 0.5) * (1 - sw), 20);
      counter(r, t, { to: 100, a: 113.0, b: 114.2, top: 525, size: 112, prefix: '+', suffix: ' مليون نسخة' });
    };
  });
  // 10-12. Bob Proctor & Ray Stanford
  nameCard(124.9, 131.6, 'بوب بروكتر', 'شاب عادي', 128.13);
  nameCard(131.7, 137.95, 'راي ستانفورد', 'آمن ببوب: يستطيع فعلها', 135.5);
  hero(142.1, 147.7, 0.84, (r, t0) => {
    const nm = text(r, 'بوب بروكتر', 'center kufi goldText', { top: '70px', fontSize: '120px' });
    const rows = [['شاب عادي', 142.27], ['21 سنة', 144.17], ['يعمل في البحرية الكندية', 146.4]].map(([s, a], i) => [text(r, s, 'center', { top: `${270 + i * 120}px`, font: '800 64px var(--sans)', color: i === 1 ? 'var(--gold)' : 'var(--cream)' }), a]);
    return (t) => { wipe(nm, P(t, t0, 0.6)); rows.forEach(([e, a]) => rise(e, P(t, a - 0.05, 0.45), 30)); };
  });
  // 13. take this book
  quote(148.1, 153.2, [
    ['«خذ هذا الكتاب»', 148.27, { top: 130, size: 110, cls: 'naskh goldText' }],
    ['اقرأه…', 150.15, { top: 320, size: 80 }],
    ['وسيغيّر حياتك', 150.87, { top: 440, size: 100, color: 'var(--gold)' }],
  ]);
  // 14. impossible
  hero(157.9, 161.0, 0.8, (r) => { const s = stampEl(r, 'مستحيل', 230); return (t) => stamp(s, t, 158.1); });
  // 15. two years, every day
  hero(161.0, 176.3, 0.86, (r, t0) => {
    const lbl = text(r, 'لمدة سنتين… كل يوم', 'center kufi', { top: '60px', fontSize: '72px' });
    const sub = text(r, 'يوم', 'center', { top: '380px', font: '800 54px var(--sans)', color: 'var(--muted)' });
    const tail = text(r, '«اقرأ الكتاب»', 'center naskh goldText', { top: '490px', fontSize: '110px' });
    return (t) => {
      rise(lbl, P(t, t0, 0.5), 20);
      counter(r, t, { to: 730, a: 161.6, b: 171.8, top: 170, size: 200 });
      sub.style.opacity = P(t, 161.8, 0.4);
      wipe(tail, P(t, 173.4, 0.6));
    };
  });
  // 16. debt 6,000 vs income 4,000
  hero(186.0, 197.9, 0.88, (r, t0) => {
    const ttl = text(r, 'الوضع عندي مستحيل', 'center kufi', { top: '30px', fontSize: '70px' });
    const mk = (y, label, color) => {
      const l = text(r, label, '', { right: '60px', top: `${y}px`, font: '800 52px/1.2 var(--sans)', color });
      const track = text(r, '', '', { right: '230px', top: `${y + 14}px`, width: '640px', height: '46px', borderRadius: '23px', background: 'rgba(244,234,214,.08)' });
      const bar = el('div', '', track, '', { position: 'absolute', right: '0', top: '0', height: '46px', borderRadius: '23px', background: color });
      const v = text(r, '', 'num', { left: '70px', top: `${y + 70}px`, fontSize: '64px', color });
      return { l, bar, v };
    };
    const debt = mk(170, 'الدَّين', 'var(--red)'), inc = mk(350, 'الدخل', 'var(--gold)');
    const s = stampEl(r, 'مستحيل', 470); s.style.fontSize = '110px';
    const mir = text(r, '…إلا معجزة من السماء', 'center kufi goldText', { top: '560px', fontSize: '74px' });
    return (t) => {
      rise(ttl, P(t, t0 + 0.1, 0.5), 20);
      [[debt, 189.3, 6000, 1], [inc, 191.6, 4000, 4000 / 6000]].forEach(([o, a, val, w]) => {
        const p = P(t, a, 0.9, E.out5);
        rise(o.l, P(t, a - 0.1, 0.4), 20);
        o.bar.style.width = `${p * w * 640}px`;
        o.v.textContent = '$' + fmt(val * p); o.v.style.opacity = P(t, a, 0.3);
      });
      stamp(s, t, 193.85); s.style.opacity = Number(s.style.opacity) * (1 - P(t, 195.3, 0.3));
      wipe(mir, P(t, 195.6, 0.7));
    };
  });
  // 17. the miracle is in your hands
  hero(201.9, 215.0, 0.9, (r, t0) => {
    const rays = svg(r, '-300 -300 600 600', 900, 900, Array.from({ length: 24 }, (_, i) => `<path d="M0 0 L${Math.cos(i * Math.PI / 12) * 300} ${Math.sin(i * Math.PI / 12) * 300}" stroke="rgba(226,182,92,.16)" stroke-width="${i % 2 ? 6 : 14}"/>`).join(''), { left: '30px', top: '-90px' });
    const w1 = text(r, 'المعجزة', 'center kufi goldText', { top: '90px', fontSize: '190px' });
    const w2 = text(r, 'بين يديك', 'center kufi', { top: '320px', fontSize: '110px' });
    const l3 = text(r, 'اقرأ كتاب نابليون هيل… وطبّق', 'center', { top: '470px', font: '800 52px var(--sans)', color: 'var(--cream)' });
    const l4 = text(r, 'وستتغيّر حياتك', 'center kufi goldText', { top: '550px', fontSize: '96px' });
    return (t) => {
      rays.style.opacity = P(t, t0, 1.0) * 0.9;
      rays.style.transform = `rotate(${(t - t0) * 6}deg) scale(${lerp(0.6, 1, P(t, t0, 1.5))})`;
      wipe(w1, P(t, 202.0, 0.6)); w1.style.transform = `scale(${lerp(1.15, 1, P(t, 202.0, 0.9))})`;
      wipe(w2, P(t, 202.75, 0.5));
      const fade = P(t, 206.6, 0.4);
      w1.style.opacity = 1 - fade * 0.25;
      rise(l3, P(t, 207.0, 0.5), 20);
      wipe(l4, P(t, 211.8, 0.7));
    };
  });
  // 18. his deep belief in me
  quote(216.7, 224.7, [
    ['إيمانه العميق فيّ', 216.94, { top: 150, size: 108, cls: 'kufi goldText' }],
    ['وثقته', 218.5, { top: 320, size: 70 }],
    ['«أنا حعملها… وأسويها»', 221.5, { top: 440, size: 90, cls: 'naskh' }],
  ]);
  // 19. set a goal
  hero(233.8, 238.95, 0.86, (r, t0) => {
    const tg = svg(r, '0 0 200 200', 360, 360, '<circle class="draw" cx="100" cy="100" r="88" stroke-width="7"/><circle class="draw" cx="100" cy="100" r="58" stroke-width="7"/><circle class="draw" cx="100" cy="100" r="26" stroke-width="7"/><circle cx="100" cy="100" r="9" fill="#e2b65c"/>', { left: '300px', top: '60px' });
    const arrow = svg(r, '0 0 300 40', 330, 44, '<path d="M0 20 H250" stroke="#f4ead6" stroke-width="8" stroke-linecap="round"/><path d="M240 4 L292 20 L240 36 Z" fill="#f4ead6"/><path d="M0 20 L-24 2 M0 20 L-24 38" stroke="#e2b65c" stroke-width="7"/>', { left: '0px', top: '218px' });
    const l = text(r, 'أول شيء: وضعت هدف', 'center kufi goldText', { top: '470px', fontSize: '96px' });
    return (t) => {
      drawPaths(tg, t, t0, 0.7, 0.15);
      const a = P(t, 234.7, 0.32, E.inOut3);
      arrow.style.transform = `translateX(${lerp(-420, 170, a)}px)`; arrow.style.opacity = P(t, 234.5, 0.15);
      const hit = t > 235.02 ? Math.sin((t - 235.02) * 50) * 5 * Math.exp(-(t - 235.02) * 8) : 0;
      tg.style.transform = `translateX(${hit}px)`;
      wipe(l, P(t, 235.0, 0.6));
    };
  });
  // 20. five hours a day
  hero(238.95, 244.2, 0.86, (r) => {
    const ck = svg(r, '0 0 200 200', 300, 300, '<circle class="draw" cx="100" cy="100" r="86" stroke-width="8"/><path class="draw" d="M100 22 V34 M178 100 H166 M100 178 V166 M22 100 H34" stroke-width="6"/>', { left: '330px', top: '40px' });
    const hands = svg(r, '0 0 200 200', 300, 300, '<path id="hh" d="M100 100 V58" stroke="#f4ead6" stroke-width="9" stroke-linecap="round"/><path id="mh" d="M100 100 V36" stroke="#e2b65c" stroke-width="6" stroke-linecap="round"/>', { left: '330px', top: '40px' });
    const hh = hands.querySelector('#hh'), mh = hands.querySelector('#mh');
    const l = text(r, '<span class="num">5</span> ساعات في اليوم', 'center kufi', { top: '380px', fontSize: '100px', color: 'var(--cream)' });
    const s = text(r, 'يقرأ الكتاب… ويسمع', 'center', { top: '540px', font: '800 52px var(--sans)', color: 'var(--gold)' });
    return (t) => {
      drawPaths(ck, t, 238.95, 0.6, 0.1);
      const sweep = P(t, 239.0, 1.8, E.inOut3);
      hh.setAttribute('transform', `rotate(${sweep * 150} 100 100)`); mh.setAttribute('transform', `rotate(${sweep * 1800} 100 100)`);
      hands.style.opacity = P(t, 238.95, 0.3);
      wipe(l, P(t, 239.0, 0.6)); rise(s, P(t, 241.6, 0.5), 20);
    };
  });
  // 21. Earl Nightingale's record, in the car
  hero(244.2, 252.5, 0.86, (r, t0) => {
    const disc = svg(r, '-100 -100 200 200', 380, 380, '<circle r="96" fill="#0d0b08" stroke="#3a3122" stroke-width="2"/>' + [84, 74, 64, 54, 44].map((x) => `<circle r="${x}" fill="none" stroke="rgba(244,234,214,.12)" stroke-width="1.5"/>`).join('') + '<circle r="32" fill="#e2b65c"/><path d="M-20 -6 H20 M-14 6 H14" stroke="#3b2a12" stroke-width="4"/><circle r="4" fill="#0d0b08"/><path d="M60 -60 A86 86 0 0 1 86 0" stroke="rgba(255,240,200,.35)" stroke-width="6" fill="none"/>', { left: '290px', top: '30px' });
    const nm = text(r, 'إيرل نايتنجيل', 'center kufi goldText', { top: '430px', fontSize: '96px' });
    const car = svg(r, '0 0 220 90', 230, 94, '<path class="draw" stroke-width="6" d="M10 64 V48 L40 44 L66 18 H150 L180 44 L208 50 V64 Z"/><circle class="draw" cx="56" cy="68" r="15" stroke-width="6"/><circle class="draw" cx="166" cy="68" r="15" stroke-width="6"/>', { left: '365px', top: '590px' });
    const cl = text(r, 'في السيارة', '', { right: '60px', top: '600px', font: '800 46px var(--sans)', color: 'var(--cream)' });
    return (t) => {
      disc.style.opacity = P(t, t0, 0.5);
      disc.style.transform = `rotate(${(t - t0) * 200}deg) scale(${lerp(0.8, 1, P(t, t0, 0.7, E.back))})`;
      wipe(nm, P(t, 246.3, 0.6));
      drawPaths(car, t, 248.2, 0.7, 0.1);
      car.style.transform = `translateX(${(1 - P(t, 248.2, 1.0)) * 120}px) translateY(${Math.sin(t * 9) * 1.5}px)`;
      rise(cl, P(t, 248.4, 0.4), 18);
    };
  });
  // 22. goal: $25,000
  hero(254.5, 262.5, 0.88, (r, t0) => {
    const l = text(r, 'الهدف: دخل يصل إلى', 'center kufi', { top: '60px', fontSize: '68px' });
    const c1 = text(r, 'رقم كبير', 'pill', { left: '560px', top: '470px' });
    const c2 = text(r, 'وهو مديون!', 'pill red', { left: '170px', top: '470px' });
    return (t) => {
      rise(l, P(t, 254.7, 0.5), 20);
      counter(r, t, { to: 25000, a: 257.5, b: 258.9, top: 190, size: 200, prefix: '$' });
      pop(c1, P(t, 260.0, 0.45)); pop(c2, P(t, 261.2, 0.45));
    };
  });
  // 23. debt vs goal
  hero(266.2, 336.05, 0.86, (r, t0) => {
    const ttl = text(r, 'ما الفرق بين <span style="color:var(--red)">الدَّين</span> و<span class="goldText">الهدف</span>؟', 'center kufi', { top: '18px', fontSize: '66px' });
    const div = text(r, '', '', { left: '479px', top: '140px', width: '2px', height: '540px', background: 'linear-gradient(transparent, rgba(244,234,214,.4), transparent)', transformOrigin: '50% 0' });
    const hd = (s, x, c) => text(r, s, 'kufi', { left: `${x}px`, top: '130px', width: '440px', textAlign: 'center', fontSize: '84px', color: c });
    const hDebt = hd('الدَّين', 500, 'var(--red)'), hGoal = hd('الهدف', 20, 'var(--gold)');
    const col = (items, x, red) => items.map(([s, a], i) => [text(r, s, 'pill' + (red ? ' red' : ''), { left: `${x + 220}px`, top: `${245 + i * 62}px`, fontSize: '33px', padding: '2px 24px 7px', transform: 'translateX(-50%)' }), a, i]);
    const debts = col([['كيف أسدّدهم؟', 279.5], ['كيف أهرب منهم؟', 281.6], ['من وين أجيب؟', 286.4], ['الخوف من الناس', 293.3], ['خوف', 305.39], ['قلق', 305.79], ['توتر', 306.3]], 500, true);
    const goals = col([['النجاح', 313.42], ['الوفرة', 315.46], ['الخروج من الدين', 317.1], ['كيف أحقق؟', 318.8], ['إيش أسوي؟', 324.1], ['تفكير إيجابي', 326.6]], 20, false);
    const ban = text(r, 'لا تفكّر في الدَّين…<br>فكّر كيف تنجح', 'center kufi goldText', { top: '220px', fontSize: '96px', lineHeight: '1.45' });
    const banBg = text(r, '', '', { left: '-60px', top: '-300px', width: '1080px', height: '1920px', background: 'radial-gradient(ellipse at 50% 34%, rgba(8,6,4,.9), rgba(8,6,4,.6) 70%)' });
    r.appendChild(ban);
    return (t) => {
      wipe(ttl, P(t, 269.2, 0.7));
      div.style.transform = `scaleY(${P(t, 270.5, 0.8, E.inOut3)})`;
      rise(hDebt, P(t, 270.5, 0.5), 20); rise(hGoal, P(t, 270.95, 0.5), 20);
      const debtPhase = env(t, 273.0, 309.5, 0.6, 0.8), goalPhase = P(t, 309.3, 0.8);
      hDebt.style.textShadow = `0 0 ${debtPhase * 40}px rgba(217,87,63,.8)`;
      hGoal.style.textShadow = `0 0 ${goalPhase * 40}px rgba(226,182,92,.8)`;
      debts.forEach(([e, a, i]) => {
        const p = P(t, a - 0.05, 0.4);
        const jit = t > a ? Math.sin(t * 23 + i * 7) * 2.5 * (1 - goalPhase * 0.8) : 0;
        e.style.opacity = clamp01(p * 1.6) * (1 - goalPhase * 0.6);
        e.style.transform = `translateX(-50%) translate(${jit}px, ${(1 - E.back(p)) * 24}px) scale(${lerp(0.85, 1, E.back(p))})`;
      });
      goals.forEach(([e, a, i]) => {
        const p = P(t, a - 0.05, 0.5);
        e.style.opacity = clamp01(p * 1.6);
        e.style.transform = `translateX(-50%) translateY(${(1 - E.out5(p)) * 40 + Math.sin(t * 1.3 + i) * 3}px)`;
        if (i === goals.length - 1) e.classList.add('solid');
      });
      const b = P(t, 329.4, 0.6, E.inOut3);
      banBg.style.opacity = b * 0.92; wipe(ban, P(t, 329.6, 0.8)); ban.style.opacity = b;
    };
  });
  // 24. the cleaning sign
  hero(344.9, 352.1, 0.82, (r, t0) => {
    const rope = svg(r, '0 0 400 120', 400, 120, '<path d="M60 0 L120 110 M340 0 L280 110" stroke="#9a7432" stroke-width="5"/>', { left: '280px', top: '20px' });
    const sign = text(r, '<div class="kufi" style="font-size:78px;line-height:1.3">مطلوب</div><div style="font:900 70px/1.3 var(--sans)">عمّال نظافة</div>', 'center', { left: '210px', width: '540px', top: '130px', padding: '26px 0 34px', borderRadius: '18px', background: 'linear-gradient(#f4ead6,#e5d6b6)', color: '#2a1d0b', border: '8px solid #9a7432', boxShadow: '0 30px 60px rgba(0,0,0,.6)', transformOrigin: '50% -110px' });
    return (t) => {
      const p = P(t, 345.7, 0.5, E.out3), sw = t > 345.7 ? 9 * Math.exp(-(t - 345.7) * 1.6) * Math.cos((t - 345.7) * 6) : 0;
      sign.style.opacity = clamp01(p * 2); rope.style.opacity = clamp01(p * 2);
      sign.style.transform = `translateY(${(1 - p) * -420}px) rotate(${sw}deg)`;
      rope.style.transform = `translateY(${(1 - p) * -420}px)`;
    };
  });
  // 25. decided to work in cleaning / be patient
  quote(356.8, 363.4, [
    ['قررت أن أشتغل في النظافة', 356.9, { top: 170, size: 82 }],
    ['أجر إضافي', 362.2, { top: 380, size: 96, cls: 'kufi goldText' }],
  ]);
  quote(366.0, 371.4, [
    ['رسالة لكل من يبغى دخلًا إضافيًا', 366.1, { top: 120, size: 56, cls: 'sans', color: 'var(--muted)' }],
    ['لا تقول: «ما أبغى»', 367.13, { top: 240, size: 96 }],
    ['اصبر', 369.35, { top: 420, size: 150, cls: 'kufi goldText' }],
  ]);
  // 26. mop and tools
  hero(373.5, 380.4, 0.84, (r) => {
    const ic = svg(r, '0 0 300 220', 420, 308, '<path class="draw" stroke-width="7" d="M70 10 L120 150"/><path class="draw" stroke-width="7" d="M95 150 H150 L165 205 H80 Z"/><path class="draw" stroke-width="5" d="M90 170 V200 M108 170 V200 M126 170 V200 M144 170 V200"/><path class="draw" stroke-width="7" d="M190 90 H280 L268 205 H202 Z"/><path class="draw" stroke-width="6" d="M196 90 C196 50 274 50 274 90"/>', { left: '270px', top: '40px' });
    const l = text(r, 'ممسحة وأدوات نظافة', 'center kufi goldText', { top: '430px', fontSize: '92px' });
    return (t) => { drawPaths(ic, t, 373.7, 0.9, 0.15); wipe(l, P(t, 374.4, 0.6)); };
  });
  // 27. the company grows: staff, 5 countries, 5 years, $1M a year
  hero(384.2, 401.7, 0.88, (r, t0) => {
    const bld = svg(r, '0 0 200 200', 230, 230, '<path class="draw" stroke-width="6" d="M30 190 V40 L100 12 V190 M100 60 H170 V190 M10 190 H190"/><path class="draw" stroke-width="5" d="M50 60 H80 M50 90 H80 M50 120 H80 M50 150 H80 M120 90 H150 M120 120 H150 M120 150 H150"/>', { left: '365px', top: '20px' });
    const l1 = text(r, 'صار عندي شركة', 'center kufi', { top: '255px', fontSize: '72px' });
    const chips = [['محامين', 389.05, 600], ['موظفين', 390.2, 340], ['صيانة ونظافة', 391.69, 50]].map(([s, a, x]) => [text(r, s, 'pill', { left: `${x}px`, top: '380px' }), a]);
    const world = text(r, '', '', { left: '80px', top: '120px', width: '800px', height: '300px' });
    const arc = svg(world, '0 0 800 300', 800, 300, '<path class="draw" stroke-width="3" d="M20 260 C200 40 600 40 780 260" stroke-dasharray="1 1"/>', { left: '0', top: '0' });
    const pts = [[700, 196], [560, 106], [400, 80], [240, 106], [100, 196]].map(([x, y]) => el('i', '', world, '', { position: 'absolute', left: `${x - 18}px`, top: `${y - 18}px`, width: '36px', height: '36px', borderRadius: '50%', background: 'var(--gold)', boxShadow: '0 0 30px var(--gold)' }));
    const c5 = text(r, '<span class="num">5</span> دول', 'kufi goldText', { right: '120px', top: '430px', fontSize: '100px' });
    const y5 = text(r, 'خلال <span class="num">5</span> سنوات', 'kufi', { left: '110px', top: '445px', fontSize: '76px' });
    const inc = text(r, 'دخل سنوي', 'center kufi', { top: '560px', fontSize: '60px', color: 'var(--muted)' });
    return (t) => {
      const a = env(t, t0, 394.3, 0.3, 0.45);
      drawPaths(bld, t, 386.9, 0.8, 0.1); bld.style.opacity = a;
      rise(l1, P(t, 387.1, 0.5) * a, 20); l1.style.opacity = P(t, 387.1, 0.5) * a;
      chips.forEach(([e, s]) => { pop(e, P(t, s - 0.05, 0.4)); e.style.opacity = Number(e.style.opacity) * a; });
      const b = env(t, 394.3, 398.4, 0.4, 0.4);
      world.style.opacity = b; drawPaths(arc, t, 394.4, 0.8);
      pts.forEach((d, i) => { const p = P(t, 395.6 + i * 0.1, 0.35, E.back); d.style.transform = `scale(${p})`; });
      c5.style.opacity = b; wipe(c5, P(t, 395.9, 0.5)); y5.style.opacity = b; wipe(y5, P(t, 397.6, 0.5));
      const c = P(t, 398.3, 0.3);
      counter(r, t, { to: 1000000, a: 399.3, b: 400.8, top: 300, size: 150, prefix: '$' }).style.opacity = c;
      inc.style.opacity = c * P(t, 399.0, 0.4);
    };
  });
  // 28. how did you become a millionaire / the equation
  function equation(t0, t1, q, parts, resultHtml, resT, red) {
    return hero(t0, t1, 0.88, (r) => {
      const qq = text(r, q[0], 'center kufi', { top: '50px', fontSize: '84px' });
      const row = text(r, '', '', { left: '0', top: '270px', width: '960px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '22px', direction: 'rtl' });
      const ps = parts.map(([s, a]) => [el('div', s.startsWith('+') || s.startsWith('=') ? 'kufi' : 'pill', row, s, s.startsWith('+') || s.startsWith('=') ? { fontSize: '70px', color: 'var(--gold)' } : {}), a]);
      const res = text(r, resultHtml, 'center kufi ' + (red ? '' : 'goldText'), { top: '450px', fontSize: '110px', color: red ? 'var(--red)' : undefined });
      return (t) => {
        wipe(qq, P(t, q[1], 0.6));
        ps.forEach(([e, a]) => pop(e, P(t, a - 0.05, 0.45)));
        if (red) stamp(res, t, resT); else { wipe(res, P(t, resT, 0.6)); res.style.transform = `scale(${lerp(1.2, 1, P(t, resT, 0.8, E.back))})`; }
      };
    });
  }
  equation(407.2, 416.5, ['كيف صرت مليونير؟', 407.5], [['الكتاب', 412.6], ['+', 413.9], ['الأسطوانة', 414.6], ['=', 415.6]], 'نجحت', 415.87, false);
  equation(419.5, 433.4, ['الناس: «نسوي مثله»', 419.6], [['اشتروا الكتاب', 423.8], ['+', 424.9], ['الأسطوانات', 425.3], ['=', 426.0]], 'ما نجحوا', 426.2, true);
  // 29. the hidden lesson
  hero(433.3, 446.2, 0.88, (r, t0) => {
    const kh = svg(r, '0 0 120 160', 150, 200, '<circle class="draw" cx="60" cy="52" r="34" stroke-width="7"/><path class="draw" stroke-width="7" d="M44 80 L32 150 H88 L76 80"/>', { left: '405px', top: '20px', filter: 'drop-shadow(0 0 24px rgba(226,182,92,.55))' });
    const ttl = text(r, 'درس خفي', 'center kufi goldText', { top: '200px', fontSize: '130px' });
    const items = [['الإصرار', 437.59], ['الإيمان المسبق أنك ستسويها', 440.1]].map(([s, a], i) => { const w = text(r, '', 'center', { top: `${400 + i * 100}px` }); return [el('div', 'pill', w, s, { fontSize: '44px' }), a]; });
    const sec = text(r, 'أحد الأسرار', 'center', { top: '610px', font: '800 50px var(--sans)', color: 'var(--gold)' });
    return (t) => {
      drawPaths(kh, t, t0 + 0.2, 0.8, 0.2);
      wipe(ttl, P(t, 435.45, 0.6));
      items.forEach(([e, a]) => pop(e, P(t, a - 0.05, 0.45)));
      rise(sec, P(t, 444.2, 0.5), 20);
    };
  });
  // 30. most rich people vs Bob
  hero(451.6, 472.7, 0.88, (r, t0) => {
    const ttl = text(r, 'المليونيرات والأثرياء…', 'center kufi', { top: '30px', fontSize: '72px' });
    const L = (s, x, top, a, c) => [text(r, s, 'kufi', { left: `${x}px`, top: `${top}px`, width: '440px', textAlign: 'center', fontSize: '60px', color: c }), a];
    const rows = [
      L('أغلبهم', 500, 170, 452.4, 'var(--muted)'), L('يعيش حياته', 500, 290, 459.9, 'var(--cream)'), L('ما عنده استعداد يعلّم', 500, 410, 463.5, 'var(--cream)'),
      L('بوب', 20, 170, 465.9, 'var(--gold)'), L('كيف أصير ثري', 20, 290, 468.7, 'var(--gold)'), L('وأعلّم الناس', 20, 410, 470.4, 'var(--gold)'),
    ];
    const div = text(r, '', '', { left: '479px', top: '170px', width: '2px', height: '360px', background: 'rgba(244,234,214,.35)', transformOrigin: '50% 0' });
    return (t) => {
      wipe(ttl, P(t, 452.3, 0.6));
      rows.forEach(([e, a]) => wipe(e, P(t, a, 0.6)));
      div.style.transform = `scaleY(${P(t, 465.6, 0.6)})`;
    };
  });
  // 31. Nightingale-Conant
  nameCard(481.9, 490.7, 'نايتنجيل وكونانت', 'أكبر مكتبة لتطوير الذات في العالم', 485.8);
  // 32. not the salary — to learn
  hero(503.0, 511.4, 0.86, (r) => {
    const s = text(r, 'الراتب؟', 'center kufi', { top: '110px', fontSize: '150px', color: 'var(--muted)' });
    const line = text(r, '', '', { left: '250px', top: '215px', width: '460px', height: '12px', borderRadius: '6px', background: 'var(--red)', transformOrigin: '100% 50%', transform: 'rotate(-6deg) scaleX(0)' });
    const l = text(r, 'أبغى أتعلّم', 'center kufi goldText', { top: '400px', fontSize: '140px' });
    return (t) => {
      wipe(s, P(t, 504.5, 0.5));
      line.style.transform = `rotate(-6deg) scaleX(${P(t, 505.2, 0.4, E.inOut3)})`;
      wipe(l, P(t, 508.75, 0.6));
    };
  });
  // 33. sales rise
  hero(512.4, 516.6, 0.86, (r) => {
    const ch = svg(r, '0 0 600 300', 640, 320, '<path d="M0 290 H600 M0 0 V290" stroke="rgba(244,234,214,.25)" stroke-width="3"/><path class="draw" stroke-width="12" d="M10 270 L120 230 L220 245 L320 170 L420 150 L520 70 L590 20"/><path d="M560 10 L600 14 L588 52" fill="none" stroke="#e2b65c" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" class="tip"/>', { left: '160px', top: '60px' });
    const tip = ch.querySelector('.tip');
    const l = text(r, 'مبيعاتكم ترتفع', 'center kufi goldText', { top: '450px', fontSize: '110px' });
    return (t) => { drawPaths(ch, t, 512.8, 1.2); tip.style.opacity = P(t, 513.9, 0.2); wipe(l, P(t, 513.7, 0.6)); };
  });
  // 34. the secret: a key turning
  hero(520.9, 526.4, 0.88, (r, t0) => {
    const lock = svg(r, '0 0 200 240', 240, 288, '<path class="draw" stroke-width="10" d="M50 100 V70 a50 50 0 0 1 100 0 V100"/><rect class="draw" x="20" y="100" width="160" height="130" rx="18" stroke-width="10"/><circle cx="100" cy="155" r="14" fill="#e2b65c"/><path d="M93 160 L88 196 H112 L107 160" fill="#e2b65c"/>', { left: '360px', top: '20px' });
    const shackle = lock.querySelector('.draw');
    const l = text(r, 'السر', 'center kufi goldText', { top: '360px', fontSize: '200px' });
    return (t) => {
      drawPaths(lock, t, t0, 0.6, 0.1);
      const open = P(t, 521.6, 0.5, E.back);
      shackle.setAttribute('transform', `translate(0 ${-open * 26})`);
      wipe(l, P(t, 521.5, 0.6)); l.style.textShadow = `0 0 ${40 * open}px rgba(226,182,92,.6)`;
    };
  });
  // 35. You Were Born Rich
  hero(526.4, 536.1, 0.9, (r) => {
    const bk = book(r, { title: 'وُلدتَ<br>ثريًا', author: 'بوب بروكتر', left: 330, top: 40, w: 330, h: 440 });
    const l = text(r, 'موجود الآن على الإنترنت مجانًا', 'center', { top: '520px', font: '800 52px var(--sans)', color: 'var(--cream)' });
    return (t) => { bk(t, 527.3); rise(l, P(t, 531.4, 0.5), 20); };
  });
  // 36. timeline 1981 — 2002
  hero(549.8, 559.3, 0.88, (r, t0) => {
    const ln = svg(r, '0 0 800 60', 800, 60, '<path class="draw" stroke-width="6" d="M790 30 H10"/>', { left: '80px', top: '300px' });
    const node = (x, yr, lbl, a, top) => {
      const d = text(r, '', '', { left: `${x - 22}px`, top: '308px', width: '44px', height: '44px', borderRadius: '50%', background: 'var(--gold)', boxShadow: '0 0 30px var(--gold)' });
      const y = text(r, yr, 'num goldText', { left: `${x - 150}px`, width: '300px', textAlign: 'center', top: `${top}px`, fontSize: '100px' });
      const l = text(r, lbl, '', { left: `${x - 220}px`, width: '440px', textAlign: 'center', top: `${top === 150 ? 400 : 410}px`, font: '800 46px var(--sans)', color: 'var(--cream)' });
      return [d, y, l, a];
    };
    const n1 = node(780, '1981', 'وُلدتَ ثريًا', 556.1, 160), n2 = node(180, '2002', 'التقى بساندي', 550.95, 160);
    const span = text(r, 'عشرين سنة من المعرفة', 'center kufi goldText', { top: '540px', fontSize: '72px' });
    return (t) => {
      drawPaths(ln, t, t0 + 0.2, 0.9);
      [n2, n1].forEach(([d, y, l, a]) => { d.style.transform = `scale(${P(t, a, 0.4, E.back)})`; wipe(y, P(t, a, 0.5)); rise(l, P(t, a + (a === 550.95 ? 1.4 : 0.3), 0.5), 16); });
      wipe(span, P(t, 558.1, 0.6));
    };
  });
  // 37. a new program for individuals and companies
  hero(564.9, 570.6, 0.86, (r) => {
    const l = text(r, 'برنامج جديد', 'center kufi goldText', { top: '120px', fontSize: '150px' });
    const c1 = text(r, 'للأفراد', 'pill', { left: '540px', top: '400px', fontSize: '60px' });
    const c2 = text(r, 'والشركات', 'pill', { left: '170px', top: '400px', fontSize: '60px' });
    return (t) => { wipe(l, P(t, 565.4, 0.6)); pop(c1, P(t, 567.8, 0.45)); pop(c2, P(t, 568.3, 0.45)); };
  });
  // 38. Thinking Into Results — 12 lessons
  hero(571.1, 601.6, 0.9, (r, t0) => {
    const ttl = text(r, 'التفكير المؤدي للنتائج', 'center kufi goldText', { top: '40px', fontSize: '96px' });
    const exp = [['كل خبرته', 576.4, 560], ['كل أفكاره', 579.0, 190]].map(([s, a, x]) => [text(r, s, 'pill', { left: `${x}px`, top: '220px' }), a]);
    const nh = text(r, 'أفكار نابليون هيل… مطوَّرة ومرتّبة', 'center', { top: '340px', font: '800 50px var(--sans)', color: 'var(--cream)' });
    const grid = text(r, '', '', { left: '150px', top: '210px', width: '660px', height: '360px' });
    const tiles = Array.from({ length: 12 }, (_, i) => el('div', 'num', grid, String(i + 1), { position: 'absolute', right: `${(i % 4) * 168}px`, top: `${Math.floor(i / 4) * 122}px`, width: '148px', height: '102px', borderRadius: '16px', border: '3px solid var(--gold)', display: 'grid', placeItems: 'center', fontSize: '54px', color: 'var(--gold)' }));
    const tl = text(r, '<span class="num">12</span> درسًا', 'center kufi', { top: '590px', fontSize: '80px' });
    const last = text(r, 'ليس كتابًا… بل <span class="goldText">برنامج</span>', 'center kufi', { top: '590px', fontSize: '80px' });
    return (t) => {
      wipe(ttl, P(t, 572.1, 0.8));
      const ph1 = 1 - P(t, 589.8, 0.5);
      exp.forEach(([e, a]) => { pop(e, P(t, a - 0.05, 0.45)); e.style.opacity = Number(e.style.opacity) * ph1; });
      nh.style.opacity = P(t, 585.3, 0.5) * ph1; nh.style.transform = `translateY(${(1 - P(t, 585.3, 0.5)) * 20}px)`;
      grid.style.opacity = P(t, 590.0, 0.5);
      tiles.forEach((e, i) => {
        const p = P(t, 593.2 + i * 0.25, 0.35, E.back), lit = t >= 593.2 + i * 0.25;
        e.style.transform = `scale(${lerp(0.6, 1, p)})`; e.style.opacity = 0.25 + 0.75 * p;
        e.style.background = lit ? 'rgba(226,182,92,.22)' : 'transparent';
      });
      const sw = P(t, 597.9, 0.4);
      tl.style.opacity = P(t, 593.2, 0.4) * (1 - sw); last.style.opacity = sw; wipe(last, P(t, 597.9, 0.7));
    };
  });
  // 39. Coach Abu Faisal
  nameCard(606.6, 616.6, 'كوتش أبو فيصل', 'يقدّم لك برنامج مفاتيح الثروة', 608.8);
  // 40. simple, Sharia-compliant, Arab mindset
  hero(619.1, 633.1, 0.88, (r, t0) => {
    const ttl = text(r, 'أقدّمها لك', 'center kufi', { top: '30px', fontSize: '70px', color: 'var(--muted)' });
    const items = [['بطريقة مبسّطة وسهلة', 622.4], ['بمعايير الشريعة الإسلامية', 627.2], ['وبالعقلية العربية', 630.7]].map(([s, a], i) => {
      const row = text(r, '', '', { right: '90px', top: `${170 + i * 150}px`, width: '780px', height: '120px' });
      const k = svg(row, '0 0 80 80', 80, 80, '<circle class="draw" cx="40" cy="40" r="34" stroke-width="6"/><path class="draw" d="M24 41 L36 53 L58 28" stroke-width="7"/>', { right: '0', top: '18px' });
      const s1 = el('div', 'kufi', row, s, { position: 'absolute', right: '110px', top: '8px', fontSize: '68px', whiteSpace: 'nowrap' });
      return [k, s1, a];
    });
    return (t) => {
      rise(ttl, P(t, 619.3, 0.5), 20);
      items.forEach(([k, s, a]) => { drawPaths(k, t, a - 0.1, 0.5, 0.15); wipe(s, P(t, a, 0.6)); });
    };
  });
  // 41. end card
  hero(633.1, DURATION + 1, 0.95, (r, t0) => {
    const key = svg(r, '0 0 300 120', 360, 144, '<circle class="draw" cx="62" cy="60" r="44" stroke-width="10"/><circle class="draw" cx="62" cy="60" r="14" stroke-width="7"/><path class="draw" d="M106 60 H286 M246 60 V94 M272 60 V86" stroke-width="10"/>', { left: '300px', top: '80px', filter: 'drop-shadow(0 0 22px rgba(226,182,92,.5))' });
    const ttl = text(r, 'مفاتيح الثروة', 'center kufi goldText', { top: '250px', fontSize: '150px' });
    const who = text(r, 'مع كوتش أبو فيصل', 'center', { top: '450px', font: '800 56px var(--sans)', color: 'var(--cream)' });
    const bye = text(r, 'حيّاك الله', 'center naskh goldText', { top: '540px', fontSize: '100px' });
    return (t) => {
      drawPaths(key, t, t0 + 0.2, 1.2, 0.25);
      wipe(ttl, P(t, t0 + 0.6, 0.9));
      rise(who, P(t, t0 + 1.6, 0.6), 20);
      wipe(bye, P(t, 638.0, 0.7));
    };
  });

  /* ---------- chapters (header label + progress ticks) ---------- */
  const CHAPTERS = [
    [0, 'المقدمة'], [14.5, 'أندرو كارنيجي'], [56.8, 'نابليون هيل'], [117.8, 'بوب بروكتر'], [226.7, 'الهدف'],
    [266.2, 'الدَّين أم الهدف؟'], [336.0, 'البداية من الصفر'], [402.2, 'الدرس الخفي'], [473.6, 'نايتنجيل كونانت'],
    [548.8, 'التفكير المؤدي للنتائج'], [606.6, 'مفاتيح الثروة'],
  ];
  const chapterEl = $('#chapter'), header = $('#header');
  const progress = $('#progress'), fill = $('#progressFill');
  const ticks = CHAPTERS.slice(1).map(([c]) => el('i', 'tick abs', progress, '', { right: `${(c / DURATION) * 900 - 2}px` }));
  let lastChapter = -1;

  /* ---------- captions ---------- */
  const KEYWORDS = /كارنيجي|نابليون|هيل|بروكتر|مليونير|الثروة|المعجزة|هدف|الدين|الدَّين|السر|راي|نايتنجيل|ثراءً|ثريًا|^\d/;
  const capBox = $('#captions');
  let capIdx = -2, capSpans = [];
  function captionAt(t) {
    for (let i = CAPS.length - 1; i >= 0; i--) {
      const c = CAPS[i];
      if (t >= c.start - 0.15) {
        const next = CAPS[i + 1];
        const hold = Math.min(c.end + 0.9, next ? next.start - 0.15 : Infinity);
        return t <= hold ? i : -1;
      }
    }
    return -1;
  }
  function drawCaptions(t) {
    const i = captionAt(t);
    if (i !== capIdx) {
      capIdx = i; capBox.innerHTML = '';
      capSpans = i < 0 ? [] : CAPS[i].w.map(([w]) => { const s = el('span', KEYWORDS.test(w) ? 'key' : '', capBox, ''); s.textContent = w; el('i', '', s); return s; });
    }
    if (i < 0) return;
    const c = CAPS[i], next = CAPS[i + 1];
    const pin = P(t, c.start - 0.15, 0.22);
    const outT = Math.min(c.end + 0.9, next ? next.start - 0.15 : Infinity);
    const pout = P(t, outT - 0.14, 0.14, E.lin);
    capBox.style.opacity = pin * (1 - pout);
    capBox.style.transform = `translateY(${(1 - pin) * 26}px)`;
    c.w.forEach(([, a, b], k) => {
      const s = capSpans[k], nb = k + 1 < c.w.length ? c.w[k + 1][1] : b;
      const on = t >= a - 0.06 && t < Math.max(b, nb - 0.02);
      const isKey = s.classList.contains('key');
      s.classList.toggle('on', on); s.classList.toggle('done', t >= a - 0.06);
      const pk = P(t, a - 0.06, 0.18, E.back);
      s.style.transform = on ? `scale(${lerp(1, 1.07, pk)})` : 'scale(1)';
      s.firstElementChild.style.transform = `scaleX(${isKey ? P(t, a - 0.06, Math.max(0.15, b - a), E.out3) : 0})`;
    });
  }

  /* ---------- ambient gold dust + cut flashes ---------- */
  const fx = $('#fx'), ctx = fx.getContext('2d');
  const DR = rng(2026);
  const dust = Array.from({ length: 80 }, () => ({ x: DR() * 1080, y: DR() * 1920, v: 6 + DR() * 22, r: 0.8 + DR() * 2.6, ph: DR() * 6.28, a: 0.15 + DR() * 0.45 }));
  function drawFx(t) {
    ctx.clearRect(0, 0, 1080, 1920);
    for (const d of dust) {
      const y = ((d.y - t * d.v) % 1920 + 1920) % 1920, x = d.x + Math.sin(t * 0.4 + d.ph) * 24;
      ctx.globalAlpha = d.a * (0.55 + 0.45 * Math.sin(t * 1.7 + d.ph * 3));
      ctx.fillStyle = '#f0cf86';
      ctx.beginPath(); ctx.arc(x, y, d.r, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
  const flash = $('#flash');
  function cutFlash(t) {
    let v = 0;
    for (const [c] of CUTS) { if (c > 0.1 && t >= c && t < c + 0.4) v = Math.max(v, Math.exp(-(t - c) * 11)); }
    flash.style.opacity = v * 0.33;
  }

  /* ---------- frame ---------- */
  function seek(t) {
    let scrim = 0;
    for (const h of HEROES) {
      const vis = t >= h.t0 - 0.02 && t <= h.t1 + 0.02;
      h.root.style.display = vis ? 'block' : 'none';
      if (!vis) continue;
      const e = env(t, h.t0, h.t1, 0.3, 0.35);
      h.root.style.opacity = e;
      scrim = Math.max(scrim, h.scrim * e);
      h.update(t);
    }
    $('#scrim').style.opacity = scrim;
    // header: hidden behind the title and end card, chapter label wipes in on each change
    const hv = Math.min(P(t, 14.3, 0.6), 1 - P(t, 633.0, 0.5));
    header.style.opacity = hv;
    let ci = 0; CHAPTERS.forEach(([c], i) => { if (t >= c) ci = i; });
    if (ci !== lastChapter) { lastChapter = ci; chapterEl.innerHTML = `<b>${String(ci).padStart(2, '0')}</b>${CHAPTERS[ci][1]}`; }
    wipe(chapterEl, P(t, Math.max(CHAPTERS[ci][0], 14.3), 0.7));
    fill.style.width = `${(t / DURATION) * 900}px`;
    ticks.forEach((k, i) => k.classList.toggle('past', t >= CHAPTERS[i + 1][0]));
    drawCaptions(t);
    drawFx(t);
    cutFlash(t);
  }

  window.__kosif = { duration: DURATION, fps: FPS, seek };
  window.__kosifReady = document.fonts.ready.then(() => Promise.all(['700 40px "Reem Kufi"', '800 40px Cairo', '700 40px Amiri'].map((f) => document.fonts.load(f, 'مفاتيح'))));
  if (/dev/.test(location.search)) {
    document.body.classList.add('dev');
    const m = location.search.match(/t=([\d.]+)/); window.__kosifReady.then(() => seek(m ? +m[1] : 6.5));
  }
})();
