#!/usr/bin/env node
// Wave-2 "remotion" helper: bundle a tiny Remotion project written by a power program and
// render a few frames with the starter's own node_modules (starters/remotion) and a local
// Playwright Chromium. Fully offline: no npm install, no browser download, and every page
// request that is not the local Remotion bundle server is aborted.
//
// Usage: node _remotion_helper.cjs JOB.json      (prints one JSON result line on stdout)
// JOB = {entry, composition, outDir, props?, stills?: [frame], frames?: [start, end],
//        media?: {out, codec, frameRange}, scale?, browser?, imageFormat?, metaOnly?}
"use strict";
const fs = require("fs");
const path = require("path");
const os = require("os");

const REPO = path.resolve(__dirname, "..", "..", "..", "..", "..");
const STARTER = process.env.KOSIF_REMOTION_STARTER || path.join(REPO, "starters", "remotion");
const NM = path.join(STARTER, "node_modules");
const need = (m) => require(path.join(NM, m));

function playwrightChromiums() {
  const roots = [process.env.PLAYWRIGHT_BROWSERS_PATH, "/opt/pw-browsers",
    path.join(os.homedir(), ".cache", "ms-playwright")].filter(Boolean);
  const out = [];
  for (const root of roots) {
    let names = [];
    try { names = fs.readdirSync(root).sort().reverse(); } catch { continue; }
    for (const n of names.filter((x) => /^chromium_headless_shell-\d+$/.test(x))) {
      out.push(path.join(root, n, "chrome-headless-shell-linux64", "chrome-headless-shell"));
      out.push(path.join(root, n, "chrome-linux", "headless_shell"));
    }
  }
  return out;
}

function findBrowser(explicit) {
  if (explicit) return explicit;
  const c = [process.env.KOSIF_BROWSER, ...playwrightChromiums()].filter(Boolean);
  return c.find((p) => fs.existsSync(p)) || null;
}

// Same entry chain as @remotion/bundler's webpack config in production mode
// (setup-environment, sequence stack traces, user root, react shim, studio renderEntry),
// bundled with the starter's esbuild instead of webpack so a render fits in a few seconds.
// index.html comes from the bundler's own BundlerInternals.indexHtml.
async function fastBundle(entry, outDir, publicDir) {
  const esbuild = need("esbuild");
  const B = path.join(NM, "@remotion", "bundler", "dist");
  fs.mkdirSync(path.join(outDir, "public"), { recursive: true });
  const publicFiles = [];
  if (publicDir) {
    for (const name of fs.readdirSync(publicDir).sort()) {
      const src = path.join(publicDir, name);
      if (!fs.statSync(src).isFile()) continue;
      fs.copyFileSync(src, path.join(outDir, "public", name));
      const st = fs.statSync(src);
      publicFiles.push({ name, lastModified: Math.floor(st.mtimeMs), sizeInBytes: st.size, src: "./public/" + name });
    }
  }
  const shim = path.join(outDir, "entry-chain.js");
  const chain = [path.join(B, "setup-environment.js"), path.join(B, "setup-sequence-stack-traces.js"),
    entry, path.join(NM, "@remotion", "bundler", "react-shim.js"),
    path.join(NM, "@remotion", "studio", "dist", "renderEntry.js")];
  fs.writeFileSync(shim, chain.map((p) => `import ${JSON.stringify(p)};`).join("\n") + "\n");
  await esbuild.build({
    entryPoints: [shim], bundle: true, outfile: path.join(outDir, "bundle.js"), format: "iife",
    platform: "browser", target: "chrome85", jsx: "automatic", logLevel: "silent",
    nodePaths: [NM], loader: { ".js": "jsx", ".png": "dataurl", ".wav": "dataurl" },
    define: { "process.env.NODE_ENV": '"production"' },
    // renderEntry lazy-loads the read-only Studio (./internals) only outside a headless
    // browser; a render never reaches it, so it is replaced by a stub that says so.
    plugins: [{ name: "no-studio", setup(b) {
      b.onResolve({ filter: /^\.\/internals$/ }, (a) => a.importer.endsWith("renderEntry.js")
        ? { path: "studio-internals-stub", namespace: "stub" } : undefined);
      b.onLoad({ filter: /.*/, namespace: "stub" }, () => ({ contents:
        "export const StudioInternals = { Studio: () => 'studio not bundled for rendering' };" }));
    } }],
  });
  const { BundlerInternals } = need("@remotion/bundler");
  const { NoReactInternals } = need("remotion/no-react");
  const html = BundlerInternals.indexHtml({
    importMap: null, staticHash: "./public", outputHash: null, publicPath: "./", editorName: null,
    inputProps: null, remotionRoot: STARTER, studioServerCommand: null, renderQueue: null,
    numberOfAudioTags: 0, publicFiles, includeFavicon: false, title: "Remotion Bundle",
    renderDefaults: undefined, publicFolderExists: "./public", fileSystemPlatform: null,
    gitSource: null, projectName: "kosif-power-program", installedDependencies: null,
    packageManager: "unknown", logLevel: "info", mode: "bundle", audioLatencyHint: "playback",
    experimentalKeepAudioContextAlive: false, sampleRate: 48000,
    studioRuntimeConfig: { showPremounting: null, defaultPremountInSeconds: null,
      experimentalSequenceActivityEnabled: false,
      experimentalSequenceActivityLimit: NoReactInternals.DEFAULT_SEQUENCE_ACTIVITY_LIMIT,
      askAIEnabled: false, bufferStateDelayInMilliseconds: null, canvasTabsEnabled: true,
      defaultCodingAgent: null, defaultEditor: null, interactivityEnabled: true,
      keyboardShortcutsEnabled: true, maxTimelineTracks: null, publicLicenseKey: null,
      configFileStudioSettings: null },
  });
  fs.writeFileSync(path.join(outDir, "index.html"), html);
  return outDir;
}

const meta = (c) => ({ id: c.id, width: c.width, height: c.height, fps: c.fps,
  durationInFrames: c.durationInFrames, props: c.props });

async function main() {
  const job = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const t0 = Date.now();
  const { bundle } = need("@remotion/bundler");
  const R = need("@remotion/renderer");
  const outDir = path.resolve(job.outDir);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = findBrowser(job.browser);
  const result = { browser, starter: STARTER, files: [], timings: {} };
  if (job.browser && !fs.existsSync(job.browser)) {
    throw new Error("browser executable does not exist: " + job.browser);
  }
  const bundleDir = path.join(outDir, ".bundle");
  const serveUrl = job.bundler === "webpack"
    ? await bundle({
      entryPoint: path.resolve(job.entry), outDir: bundleDir, enableCaching: false,
      webpackOverride: (cfg) => ({ ...cfg, cache: false,
        resolve: { ...cfg.resolve, modules: [NM, "node_modules"] } }),
    })
    : await fastBundle(path.resolve(job.entry), bundleDir, job.publicDir ? path.resolve(job.publicDir) : null);
  result.bundler = job.bundler === "webpack" ? "@remotion/bundler (webpack)" : "esbuild (starter) + @remotion/bundler indexHtml";
  result.timings.bundle_ms = Date.now() - t0;
  const common = {
    serveUrl, browserExecutable: browser, chromeMode: "headless-shell",
    logLevel: "error", inputProps: job.props || {},
    onBrowserDownload: () => { throw new Error("browser download refused (offline)"); },
  };
  const pup = await R.openBrowser("chrome", { browserExecutable: browser, chromeMode: "headless-shell",
    logLevel: "error", onBrowserDownload: common.onBrowserDownload });
  common.puppeteerInstance = pup;
  try {
    const comp = await R.selectComposition({ ...common, id: job.composition });
    result.composition = meta(comp);
    const onBrowserLog = () => {};
    const scale = job.scale || 1;
    const imageFormat = job.imageFormat || "png";
    // Extra props variants: each one re-resolves the composition (calculateMetadata included).
    result.variants = {};
    for (const v of job.variants || []) {
      const vc = await R.selectComposition({ ...common, id: job.composition, inputProps: v.props });
      result.variants[v.name] = meta(vc);
      if (v.frame === undefined || v.frame === null) continue;
      const out = path.join(outDir, `variant-${v.name}.${imageFormat}`);
      await R.renderStill({ ...common, inputProps: v.props, composition: vc, frame: v.frame, output: out,
        scale, imageFormat, onBrowserLog, overwrite: true });
      result.files.push(out);
    }
    if (!job.metaOnly) {
      for (const frame of job.stills || []) {
        const out = path.join(outDir, `still-${String(frame).padStart(4, "0")}.${imageFormat}`);
        await R.renderStill({ ...common, composition: comp, frame, output: out, scale, imageFormat,
          onBrowserLog, overwrite: true });
        result.files.push(out);
      }
      if (job.frames) {
        const res = await R.renderFrames({ ...common, composition: comp, imageFormat,
          frameRange: job.frames, outputDir: outDir, scale, concurrency: 1,
          onStart: () => {}, onFrameUpdate: () => {}, onBrowserLog,
          jpegQuality: imageFormat === "jpeg" ? 90 : undefined });
        result.framesRendered = res.frameCount;
        for (const f of fs.readdirSync(outDir).sort()) {
          if (/^element-\d+\.(png|jpeg)$/.test(f)) result.files.push(path.join(outDir, f));
        }
      }
      if (job.media) {
        const out = path.resolve(job.media.out);
        await R.renderMedia({ ...common, composition: comp, codec: job.media.codec || "h264",
          outputLocation: out, frameRange: job.media.frameRange, scale, concurrency: 1,
          imageFormat: job.media.imageFormat || "jpeg", onBrowserLog, overwrite: true,
          crf: job.media.crf });
        result.files.push(out);
      }
    }
  } finally {
    await pup.close({ silent: true });
  }
  if (!process.env.KEEP) fs.rmSync(path.join(outDir, ".bundle"), { recursive: true, force: true });
  result.timings.total_ms = Date.now() - t0;
  console.log(JSON.stringify(result));
}

main().catch((e) => {
  console.log(JSON.stringify({ error: String(e && e.message || e).slice(0, 800) }));
  process.exit(1);
});
