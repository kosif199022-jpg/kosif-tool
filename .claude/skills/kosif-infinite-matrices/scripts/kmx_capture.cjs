#!/usr/bin/env node
// KOSIF Infinite Matrices — capture stills and pixel-level A/B/C differences from a scene page.
// Usage: node kmx_capture.cjs --in scene.html --out-dir DIR [--times 1,3.9,6,9.9] [--views grid,A_full,B_no_coupling,C_no_memory]
// Writes DIR/<view>_<t>.png and prints one JSON line with the pixel differences per time.
// Playwright is resolved like tools/render_html.cjs (cwd, /opt/node-tools, $KOSIF_PLAYWRIGHT). Original KOSIF code.
"use strict";
const fs = require("fs"), path = require("path"), url = require("url");

function arg(name, dflt) { const i = process.argv.indexOf("--" + name); return i > 0 ? process.argv[i + 1] : dflt; }
function resolvePlaywright() {
  const tries = [() => require.resolve("playwright", { paths: [process.cwd()] }), () => "/opt/node-tools/node_modules/playwright",
    () => process.env.KOSIF_PLAYWRIGHT, () => "playwright"];
  for (const t of tries) { try { const spec = t(); if (!spec) continue; const m = require(spec); if (m && m.chromium) return m; } catch (e) { /* next */ } }
  throw new Error("Playwright not found (cwd, /opt/node-tools/node_modules/playwright, $KOSIF_PLAYWRIGHT)");
}
(async () => {
  const input = arg("in"), outDir = arg("out-dir");
  if (!input || !outDir || process.argv.includes("--help")) { console.error("usage: node kmx_capture.cjs --in scene.html --out-dir DIR [--times a,b] [--views v1,v2]"); process.exit(input ? 0 : 1); }
  const times = (arg("times", "1,3.9,6,9.9")).split(",").map(Number);
  const views = (arg("views", "grid")).split(",");
  fs.mkdirSync(outDir, { recursive: true });
  const pw = resolvePlaywright();
  const browser = await pw.chromium.launch({ headless: true, args: ["--allow-file-access-from-files"] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 768 }, deviceScaleFactor: 1 });
  const errors = []; page.on("pageerror", (e) => errors.push(String(e)));
  const shots = [];
  let diffs = null, determinism = null;
  for (const view of views) {
    await page.goto(url.pathToFileURL(path.resolve(input)).href + "?view=" + encodeURIComponent(view));
    await page.waitForFunction("window.__ready === true", null, { timeout: 60000 });
    for (const t of times) {
      const png = await page.evaluate((tt) => { window.seek(tt); return document.getElementById("c").toDataURL("image/jpeg", 0.9); }, t);
      const file = path.join(outDir, view + "_" + t.toFixed(2) + ".jpg");
      fs.writeFileSync(file, Buffer.from(png.split(",")[1], "base64"));
      shots.push(file);
    }
    if (!diffs) {
      diffs = {};
      for (const t of times) diffs[t.toFixed(2)] = await page.evaluate((tt) => window.kmxPixelDiff(tt), t);
      determinism = await page.evaluate(() => { window.seek(6.0); const a = document.getElementById("c").toDataURL();
        window.seek(2.0); window.seek(6.0); return a === document.getElementById("c").toDataURL(); });
    }
  }
  let wav = null;
  const wavOut = arg("wav");
  if (wavOut) { // the atlas sound kit renders the score offline; 16-bit stereo 48 kHz WAV
    const b64 = await page.evaluate(async () => {
      const f = await KSound.renderOffline(window.scoreSound, window.DURATION, 48000, { voiceover: false });
      const i16 = new Int16Array(f.length); for (let i = 0; i < f.length; i++) i16[i] = Math.max(-1, Math.min(1, f[i])) * 32767;
      let s = ""; const u8 = new Uint8Array(i16.buffer); for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
      return btoa(s); });
    const pcm = Buffer.from(b64, "base64"), h = Buffer.alloc(44);
    h.write("RIFF", 0); h.writeUInt32LE(36 + pcm.length, 4); h.write("WAVE", 8); h.write("fmt ", 12); h.writeUInt32LE(16, 16);
    h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22); h.writeUInt32LE(48000, 24); h.writeUInt32LE(48000 * 4, 28); h.writeUInt16LE(4, 32);
    h.writeUInt16LE(16, 34); h.write("data", 36); h.writeUInt32LE(pcm.length, 40);
    fs.writeFileSync(wavOut, Buffer.concat([h, pcm])); wav = wavOut;
  }
  await browser.close();
  console.log(JSON.stringify({ stills: shots, pixel_diff: diffs, same_t_same_pixels: determinism, wav, page_errors: errors }));
  process.exit(errors.length ? 1 : 0);
})().catch((e) => { console.error(String(e && e.stack || e)); process.exit(1); });
