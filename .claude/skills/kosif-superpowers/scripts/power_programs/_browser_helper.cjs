#!/usr/bin/env node
/* Wave-2 "browser" helper: drive Playwright Chromium through one job file, fully offline.

   node _browser_helper.cjs JOB.json RESULT.json

   JOB = {
     root: "<dir served at https://kosif.test/>",
     extra: {"/lib/gsap.min.js": "<file on disk>"},   // more served paths
     noRange: ["/clip.webm"],                          // served as one 200 body, no byte ranges
     delay: {"/font.woff2": 800},                      // ms before a served file is answered
     status: {"/missing.png": 404},                    // forced status codes
     launch: {args: [...]}, context: {...},            // chromium.launch / newContext options
     persistent: "<profile dir>",                      // launchPersistentContext instead
     cdp: true,                                        // open a CDP session and log console/network events
     initScripts: ["js", ...],
     steps: [{op: "goto"|"eval"|"wait"|"shot"|"pdf"|"click"|"press"|"fill"|"setFiles"|"viewport"|
                  "frames"|"download"|"aria"|"reload"|"sleepFrames"|"focusWalk"|"cdpSend", ...}]
   }
   Every http(s) request outside https://kosif.test/ is aborted (blockedbyclient) and logged.
   RESULT = {values: {...}, console: [...], pageErrors: [...], requests: [...], blocked: [...], cdpEvents: [...]}
*/
"use strict";
const fs = require("fs");
const path = require("path");

function loadPlaywright() {
  const tries = ["playwright", "/opt/node-tools/node_modules/playwright",
    path.resolve(__dirname, "../../../../../starters/remotion/node_modules/playwright")];
  for (const t of tries) { try { return require(t); } catch (e) { /* next */ } }
  throw new Error("playwright not found");
}

const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".cjs": "text/javascript", ".mjs": "text/javascript",
  ".css": "text/css", ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml",
  ".webm": "video/webm", ".mp4": "video/mp4", ".wav": "audio/wav", ".woff2": "font/woff2", ".ttf": "font/ttf", ".txt": "text/plain" };

async function main() {
  const job = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const outFile = process.argv[3];
  const res = { values: {}, console: [], pageErrors: [], requests: [], blocked: [], cdpEvents: [], downloads: [] };
  const { chromium } = loadPlaywright();
  const ORIGIN = "https://kosif.test";
  let browser = null, context;
  // uncapped compositor frames: screenshots no longer wait for a 60 Hz vsync (about 4x faster frame capture)
  const launch = Object.assign({}, job.launch || {});
  if (!job.vsync) launch.args = ["--disable-gpu-vsync", "--disable-frame-rate-limit", ...(launch.args || [])];
  if (job.persistent) {
    context = await chromium.launchPersistentContext(job.persistent, Object.assign({}, launch, job.context || {}));
  } else {
    browser = await chromium.launch(launch);
    context = await browser.newContext(Object.assign({ acceptDownloads: true }, job.context || {}));
  }
  for (const s of job.initScripts || []) await context.addInitScript({ content: s });
  const fileFor = (p) => {
    if (job.extra && job.extra[p]) return job.extra[p];
    if (!job.root) return null;
    const f = path.join(job.root, decodeURIComponent(p));
    return f.startsWith(path.resolve(job.root)) ? f : null;
  };
  await context.route("**/*", async (route) => {
    const req = route.request(), url = req.url();
    if (!url.startsWith(ORIGIN + "/")) {
      if (/^https?:/.test(url)) { res.blocked.push(url); return route.abort("blockedbyclient"); }
      return route.continue();
    }
    let p = new URL(url).pathname; if (p.endsWith("/")) p += "index.html";
    const forced = job.status && job.status[p];
    const f = fileFor(p);
    if (job.delay && job.delay[p]) await new Promise((r) => setTimeout(r, job.delay[p]));
    if (forced || !f || !fs.existsSync(f)) {
      res.requests.push({ url, status: forced || 404 });
      return route.fulfill({ status: forced || 404, body: "not found", contentType: "text/plain" });
    }
    const body = fs.readFileSync(f), ct = MIME[path.extname(f).toLowerCase()] || "application/octet-stream";
    const range = req.headers()["range"];
    const noRange = (job.noRange || []).includes(p);
    if (range && !noRange) {
      const m = /bytes=(\d*)-(\d*)/.exec(range); const a = m[1] ? +m[1] : 0; const b = m[2] ? Math.min(+m[2], body.length - 1) : body.length - 1;
      res.requests.push({ url, status: 206, range });
      return route.fulfill({ status: 206, body: body.subarray(a, b + 1), headers: { "Content-Type": ct, "Accept-Ranges": "bytes",
        "Content-Range": `bytes ${a}-${b}/${body.length}`, "Content-Length": String(b - a + 1) } });
    }
    res.requests.push({ url, status: 200, range: range || null });
    const headers = { "Content-Type": ct }; if (!noRange) headers["Accept-Ranges"] = "bytes";
    return route.fulfill({ status: 200, body, headers });
  });
  const page = context.pages()[0] || await context.newPage();
  page.on("console", (m) => res.console.push({ type: m.type(), text: m.text() }));
  page.on("pageerror", (e) => res.pageErrors.push(String(e && e.message || e)));
  if (job.downloadDir) page.on("download", async (d) => { const to = path.join(job.downloadDir || job.root || ".", d.suggestedFilename());
    await d.saveAs(to); res.downloads.push({ name: d.suggestedFilename(), path: to, bytes: fs.statSync(to).size }); });
  let cdp = null;
  if (job.cdp) {
    cdp = await context.newCDPSession(page);
    await cdp.send("Runtime.enable"); await cdp.send("Network.enable"); await cdp.send("Log.enable");
    cdp.on("Runtime.consoleAPICalled", (e) => res.cdpEvents.push({ kind: "console", level: e.type, text: (e.args || []).map((a) => a.value).join(" ") }));
    cdp.on("Runtime.exceptionThrown", (e) => res.cdpEvents.push({ kind: "exception", text: e.exceptionDetails && (e.exceptionDetails.exception && e.exceptionDetails.exception.description || e.exceptionDetails.text) }));
    cdp.on("Network.responseReceived", (e) => res.cdpEvents.push({ kind: "response", url: e.response.url, status: e.response.status }));
    cdp.on("Network.loadingFailed", (e) => res.cdpEvents.push({ kind: "failed", error: e.errorText }));
  }
  const ev = (js) => page.evaluate(js);
  const t0 = Date.now();
  for (const st of job.steps || []) {
    const to = st.timeout || 8000;
    switch (st.op) {
      case "goto": await page.goto(st.url.startsWith("/") ? ORIGIN + st.url : st.url, { waitUntil: st.waitUntil || "load", timeout: to }); break;
      case "reload": await page.reload({ waitUntil: "load" }); break;
      case "eval": { const v = await ev(st.js); if (st.as) res.values[st.as] = v; break; }
      case "wait": await page.waitForFunction(st.js, null, { timeout: to }); break;
      case "shot": {
        const o = { path: st.path, animations: st.animations || "allow" };
        if (st.selector) await page.locator(st.selector).screenshot(o);
        else { if (st.fullPage) o.fullPage = true; if (st.clip) o.clip = st.clip; await page.screenshot(o); }
        break; }
      case "pdf": await page.pdf(Object.assign({ path: st.path }, st.options || {})); break;
      case "click": await page.locator(st.selector).first().click({ timeout: to }); break;
      case "press": await page.keyboard.press(st.key); break;
      case "fill": await page.locator(st.selector).fill(st.value); break;
      case "setFiles": await page.locator(st.selector).setInputFiles(st.files); break;
      case "viewport": await page.setViewportSize({ width: st.width, height: st.height }); break;
      case "sleepFrames": await ev(`new Promise(r=>{let n=${st.n || 2};const f=()=>--n<=0?r():requestAnimationFrame(f);requestAnimationFrame(f)})`); break;
      case "aria": { const v = await page.locator(st.selector || "body").ariaSnapshot(); if (st.as) res.values[st.as] = v; if (st.path) fs.writeFileSync(st.path, v); break; }
      case "focusWalk": {   // press Tab n times and record the focused element each time
        const seq = [];
        for (let i = 0; i < st.n; i++) { await page.keyboard.press(st.key || "Tab");
          seq.push(await ev(`(()=>{const a=document.activeElement;const cs=getComputedStyle(a);return {id:a.id||a.tagName,tag:a.tagName,outline:cs.outlineStyle+' '+cs.outlineWidth,shadow:cs.boxShadow}})()`)); }
        res.values[st.as || "focus"] = seq; break; }
      case "frames": {      // window.render(t) per frame, wait for readiness, screenshot each frame
        fs.mkdirSync(st.dir, { recursive: true });
        let count = st.count;
        if (count == null && st.durationJs) { const d = await ev(st.durationJs); res.values[(st.as || "frames") + "_seconds"] = d; count = Math.round(d * st.fps); }
        const times = st.times || Array.from({ length: count }, (_, i) => (st.start || 0) + i / st.fps);
        const shots = [];
        const fcdp = st.fast ? await context.newCDPSession(page) : null;
        let clip = st.clip || null;
        if (st.selector) { const bb = await page.locator(st.selector).boundingBox(); clip = { x: bb.x, y: bb.y, width: bb.width, height: bb.height }; }
        const step = `async (t) => { ${st.readyFlag !== false ? "window.__ready=false;" : ""} await (${st.renderJs || "(t)=>window.render(t)"})(t);
          ${st.waitJs ? `const t0=performance.now(); while(!(${st.waitJs})) { if (performance.now()-t0>${to}) throw new Error('frame not ready at '+t); await new Promise(r=>requestAnimationFrame(r)); }` : ""} return true; }`;
        await ev(`window.__kosifStep = ${step}; true`);
        for (let i = 0; i < times.length; i++) {
          const t = times[i];
          await page.evaluate((tt) => window.__kosifStep(tt), t);
          const name = path.join(st.dir, (st.pattern || "f_%04d.png").replace("%04d", String(st.indexFromTime ? Math.round(t * st.fps) : i).padStart(4, "0")));
          if (fcdp) {
            const o = { format: "png", fromSurface: true }; if (clip) o.clip = Object.assign({ scale: 1 }, clip);
            const { data } = await fcdp.send("Page.captureScreenshot", o); fs.writeFileSync(name, Buffer.from(data, "base64"));
          } else {
            const o = { path: name, animations: "allow" }; if (clip) o.clip = clip; await page.screenshot(o);
          }
          shots.push(name);
          if (st.progressEvery && (i + 1) % st.progressEvery === 0) res.console.push({ type: "progress", text: `frame ${i + 1}/${times.length}` });
        }
        res.values[st.as || "frames"] = shots; break; }
      case "download": {
        const [d] = await Promise.all([page.waitForEvent("download", { timeout: to }), page.locator(st.selector).click()]);
        const dest = path.join(st.dir, d.suggestedFilename()); await d.saveAs(dest);
        res.values[st.as || "download"] = { name: d.suggestedFilename(), path: dest, bytes: fs.statSync(dest).size }; break; }
      case "tryClick": { let err = null; try { await page.locator(st.selector).first().click({ timeout: st.timeout || 600 }); } catch (e) { err = String(e.message || e).split("\n")[0]; }
        res.values[st.as || "tryClick"] = err; break; }
      case "saveState": await context.storageState({ path: st.path }); break;
      case "count": res.values[st.as] = await page.locator(st.selector).count(); break;
      case "text": { const v = await page.locator(st.selector).first().innerText(); res.values[st.as] = st.cap ? v.slice(0, st.cap) : v; break; }
      case "cdpSend": {
        const waiter = st.waitEvent ? new Promise((r, j) => { cdp.once(st.waitEvent, r); setTimeout(() => j(new Error("no " + st.waitEvent)), to); }) : null;
        const v = await cdp.send(st.method, st.params || {}); if (st.as) res.values[st.as] = v;
        if (waiter) await waiter; break; }
      default: throw new Error("unknown op " + st.op);
    }
  }
  res.ms = Date.now() - t0;
  try { res.executable = chromium.executablePath(); } catch (e) { res.executable = ""; }
  res.userAgent = await page.evaluate("navigator.userAgent");
  fs.writeFileSync(outFile, JSON.stringify(res, null, 1));
  // a page left under a paused virtual clock can stall a clean close for seconds: cap it, then exit (Playwright kills the browser)
  const closing = browser ? browser.close() : context.close();
  await Promise.race([closing, new Promise((r) => setTimeout(r, 1500))]);
  process.exit(0);
}

main().catch((e) => { console.error(String(e && e.stack || e)); process.exit(1); });
