#!/usr/bin/env node
/* Composite renderer for "مفاتيح الثروة".
 * Captures the deterministic overlay (overlay.html, window.__kosif.seek) as transparent PNGs
 * and pipes them into ffmpeg, which lays them over the b-roll track frame by frame.
 *
 *   node render_film.cjs --broll broll.mp4 --out part.mp4 --from 0 --to 3000      (frame range)
 *   node render_film.cjs --broll broll.mp4 --stills 6.5,22,71 --out sheet_dir     (preview frames)
 */
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
let playwright;
try { playwright = require('playwright'); } catch { playwright = require('/opt/node22/lib/node_modules/playwright'); }

const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => (v.startsWith('--') ? a.concat([[v.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]]) : a), []));
const FPS = 30, W = 1080, H = 1920;
const page_url = 'file://' + path.resolve(__dirname, 'overlay.html');

async function open() {
  const browser = await playwright.chromium.launch({ args: ['--allow-file-access-from-files', '--font-render-hinting=none'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('PAGE ERROR', e.message); process.exit(2); });
  await page.goto(page_url);
  await page.evaluate(() => window.__kosifReady);
  return { browser, page };
}
const shot = async (page, t) => { await page.evaluate((x) => window.__kosif.seek(x), t); return page.screenshot({ type: 'png', omitBackground: true }); };

function ffmpegComposite(broll, start, frames, out) {
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-ss', String(start / FPS), '-i', broll,
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-filter_complex', '[0:v]setpts=PTS-STARTPTS[b];[1:v]format=rgba[o];[b][o]overlay=0:0:shortest=1,format=yuv420p',
    '-frames:v', String(frames), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', String(FPS), '-an', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  return ff;
}

(async () => {
  const broll = path.resolve(args.broll);
  const { browser, page } = await open();
  if (args.stills) {
    fs.mkdirSync(args.out, { recursive: true });
    for (const t of String(args.stills).split(',').map(Number)) {
      const png = path.join(args.out, `ov_${t.toFixed(2)}.png`);
      fs.writeFileSync(png, await shot(page, t));
      const f = Math.round(t * FPS);
      await new Promise((res, rej) => spawn('ffmpeg', ['-v', 'error', '-y', '-ss', String(f / FPS), '-i', broll, '-i', png,
        '-filter_complex', '[0:v][1:v]overlay=0:0', '-frames:v', '1', path.join(args.out, `still_${t.toFixed(2)}.jpg`)], { stdio: 'inherit' })
        .on('exit', (c) => (c ? rej(new Error('ffmpeg ' + c)) : res())));
      fs.unlinkSync(png);
    }
  } else {
    const from = +args.from, to = +args.to, n = to - from;
    const ff = ffmpegComposite(broll, from, n, path.resolve(args.out));
    const done = new Promise((res, rej) => ff.on('exit', (c) => (c ? rej(new Error('ffmpeg exit ' + c)) : res())));
    const t0 = Date.now();
    for (let f = from; f < to; f++) {
      const buf = await shot(page, f / FPS);
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      if ((f - from) % 300 === 0) console.log(`[${args.out}] ${f - from}/${n} frames, ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end();
    await done;
    console.log(`[${args.out}] done ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
