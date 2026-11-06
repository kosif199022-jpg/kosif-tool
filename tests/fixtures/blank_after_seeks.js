// Shared by blank_after_seeks.html and blank_intended.html (tests/test_render_html_blank.mjs): a seek-mode
// canvas film with grain and a moving bar that stops drawing after FAIL_AFTER seeks in one page load and
// fills pure black instead, the same failure heavy JPEG canvas engines show after many frames. It comes
// back on every retry until the page is loaded in a fresh browser.
'use strict';
const FAIL_AFTER = 40;
const intended = !!window.KOSIF_TEST_INTENDED_BLACK;
const c = document.getElementById('c');
c.width = innerWidth; c.height = innerHeight;
const x = c.getContext('2d');
let seeks = 0;
function rng(seed) { let a = seed >>> 0 || 1; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function seek(t) {
  seeks += 1;
  x.fillStyle = '#000'; x.fillRect(0, 0, c.width, c.height);
  if (seeks > FAIL_AFTER) return;              // the failure: pure black, no grain, no watermark
  if (intended && t >= 1 && t < 1.5) return;   // black on purpose
  const r = rng(Math.round(t * 1000) + 1);
  const img = x.createImageData(c.width, c.height);
  for (let i = 0; i < img.data.length; i += 4) { const v = 20 + r() * 40; img.data[i] = v; img.data[i + 1] = v * 0.8; img.data[i + 2] = v * 0.6; img.data[i + 3] = 255; }
  x.putImageData(img, 0, 0);
  x.fillStyle = '#e8c36a'; x.fillRect((t * 120) % c.width, c.height * 0.45, 40, c.height * 0.1);
  x.fillStyle = 'rgba(255,255,255,.5)'; x.font = '16px sans-serif'; x.fillText('KOSIF', 10, c.height - 12);
}
window.__kosif = { duration: 4, fps: 30, seek };
