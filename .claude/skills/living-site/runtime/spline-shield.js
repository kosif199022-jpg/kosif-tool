/* spline-shield.js: keeps the page scrollable over Spline embeds.
   Our own scenes (my.spline.design): a transparent shield passes the cursor in by postMessage,
   so the wheel always scrolls the page. Community previews (app.spline.design): a plain shield,
   the scene plays its own animation behind it. No "click to play" pill, no hint (page law).
   KOSIF v5.10: only Spline iframes are shielded (a YouTube or map iframe is left alone), iframes
   added later (lazy data-src) are picked up, and messages go to the Spline origin, not '*'. */
(() => {
  const SPLINE = /^https:\/\/(my|app|prod)\.spline\.design\//;
  const OURS = /^https:\/\/my\.spline\.design\//;
  const css = document.createElement('style');
  css.textContent = '.sp-shield{position:absolute;inset:0;z-index:1}';
  document.head.appendChild(css);
  const done = new WeakSet();
  function wrap(f) {
    const src = f.getAttribute('src') || f.dataset.src || '';
    if (done.has(f) || !SPLINE.test(src)) return;
    done.add(f);
    const host = f.parentElement;
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    const sh = document.createElement('div'); sh.className = 'sp-shield'; sh.setAttribute('aria-hidden', 'true');
    f.after(sh);
    if (!OURS.test(src)) return;
    const origin = new URL(src).origin;
    const send = (sp, e) => {
      const r = f.getBoundingClientRect();
      if (f.contentWindow) f.contentWindow.postMessage({ sp, x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height }, origin);
    };
    for (const [ev, sp] of [['pointermove', 'move'], ['pointerleave', 'leave'], ['pointerdown', 'down'], ['pointerup', 'up'], ['click', 'click']])
      sh.addEventListener(ev, e => send(sp, e), { passive: true });
  }
  const scan = () => document.querySelectorAll('iframe').forEach(wrap);
  scan();
  new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['src'] });
})();
