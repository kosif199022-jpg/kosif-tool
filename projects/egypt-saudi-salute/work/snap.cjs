// usage: node work/snap.cjs out.png t1 t2 ...  → labelled grid of frames (half size)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path'); const { execFileSync } = require('child_process'); const fs = require('fs');
(async () => {
  const [out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve('index.html')); await p.evaluate(() => window.__kosifReady);
  const files = [];
  for (const t of ts) { await p.evaluate((t) => window.__kosif.seek(+t), t); const f = `/tmp/snap_${t}.png`; await p.screenshot({ path: f }); files.push([f, t]); }
  await b.close();
  const args = []; files.forEach(([f]) => args.push('-i', f));
  const n = files.length, cols = Math.min(n, 4), rows = Math.ceil(n / cols);
  const lab = files.map(([f, t], i) => `[${i}:v]scale=540:960,drawtext=text='${t}s':x=10:y=10:fontsize=36:fontcolor=white:box=1:boxcolor=black@0.6[v${i}]`).join(';');
  const pads = []; for (let i = n; i < rows * cols; i++) pads.push(`color=black:s=540x960:d=1[v${i}]`);
  const layout = Array.from({ length: rows * cols }, (_, i) => `${(i % cols) * 540}_${Math.floor(i / cols) * 960}`).join('|');
  const fc = [lab, ...pads, Array.from({ length: rows * cols }, (_, i) => `[v${i}]`).join('') + `xstack=inputs=${rows * cols}:layout=${layout}`].join(';');
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...args, '-filter_complex', fc, '-frames:v', '1', out]);
  console.log(out);
})();
