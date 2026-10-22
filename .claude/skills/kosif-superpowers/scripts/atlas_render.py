#!/usr/bin/env python3
"""KOSIF Atlas render: turn an A15 explainer page into real frames, storyboard, audio and MP4.

The page contract (templates/atlas_explainer.html) exposes window.seek(t), window.DURATION and
window.scoreSound; every frame is a pure function of t. This tool drives headless Chromium
(Playwright) frame by frame, renders the synthesized score offline (KSound.renderOffline) and
muxes both with ffmpeg. Original KOSIF code; no network, no third-party media.

Commands
  check       determinism + timing probe (same t -> same pixels, ms per frame, duration)
  storyboard  PNG of the storyboard grid (?storyboard=1) for approval before the full build
  still       PNG of one frame at --t
  render      MP4 (H.264 + AAC) at --fps, optional --start/--end, --no-audio
  bundle      one self-contained HTML (scripts + font inlined) to share or open anywhere
"""
import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


def _fresh(path, force=False):
    p = Path(path)
    if p.exists() and not force:
        raise SystemExit("refusing to overwrite %s (pass --force)" % p)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _browser(html, query=""):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("needs: pip install playwright (Chromium must be available)")
    pw = sync_playwright().start()
    br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required", "--allow-file-access-from-files"])
    page = br.new_page(viewport={"width": 1280, "height": 768}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(Path(html).resolve().as_uri() + query)
    page.wait_for_function("window.__ready === true", timeout=30000)
    if errors:
        raise SystemExit("page error: " + errors[0])
    return pw, br, page


def _frame_png(page, t):
    page.evaluate("t => window.seek(t)", t)
    data = page.evaluate("() => document.getElementById('c').toDataURL('image/png')")
    return base64.b64decode(data.split(",", 1)[1])


def cmd_check(a):
    pw, br, page = _browser(a.input)
    try:
        dur = float(page.evaluate("window.DURATION"))
        probes = [0, dur * 0.31, dur * 0.67, max(0, dur - 0.05)]
        same = True
        for t in probes:
            h1 = hashlib.sha256(_frame_png(page, t)).hexdigest()
            _frame_png(page, t * 0.5)
            h2 = hashlib.sha256(_frame_png(page, t)).hexdigest()
            same &= h1 == h2
        t0 = time.perf_counter()
        n = 12
        for i in range(n):
            page.evaluate("t => window.seek(t)", dur * i / n)
        ms = (time.perf_counter() - t0) * 1000 / n
        has_score = page.evaluate("typeof window.scoreSound === 'function'")
        beats = page.evaluate("(window.ATLAS && window.ATLAS.BEATS || []).length")
        rep = {"duration": dur, "deterministic": same, "ms_per_frame": round(ms, 1), "has_scoreSound": has_score,
               "beats": beats, "fast_enough": ms < 100}
        print(json.dumps(rep, ensure_ascii=False))
        return 0 if same and has_score and dur > 0 else 1
    finally:
        br.close(); pw.stop()


def cmd_still(a):
    out = _fresh(a.out, a.force)
    pw, br, page = _browser(a.input)
    try:
        out.write_bytes(_frame_png(page, a.t))
    finally:
        br.close(); pw.stop()
    print(out)


def cmd_storyboard(a):
    out = _fresh(a.out, a.force)
    pw, br, page = _browser(a.input, "?storyboard=1")
    try:
        page.set_viewport_size({"width": 1400, "height": 900})
        page.wait_for_selector("#sb figure")
        page.locator("#sb").screenshot(path=str(out))
    finally:
        br.close(); pw.stop()
    print(out)


def _audio(page, wav_path, dur, sr=48000, voiceover=False):
    b64 = page.evaluate("""async ([d, sr, vo]) => {
        const f = await KSound.renderOffline(window.scoreSound, d, sr, { voiceover: vo });
        const i16 = new Int16Array(f.length);
        for (let i = 0; i < f.length; i++) { const v = Math.max(-1, Math.min(1, f[i])); i16[i] = v * 32767; }
        let s = ''; const u8 = new Uint8Array(i16.buffer);
        for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
        return btoa(s); }""", [dur, sr, voiceover])
    raw = base64.b64decode(b64)
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(raw)
    peak = max(abs(int.from_bytes(raw[i:i + 2], "little", signed=True)) for i in range(0, len(raw), 2 * 97)) if raw else 0
    return peak / 32767


def cmd_render(a):
    out = _fresh(a.out, a.force)
    if not shutil.which("ffmpeg"):
        raise SystemExit("needs ffmpeg on PATH")
    pw, br, page = _browser(a.input)
    try:
        dur = float(page.evaluate("window.DURATION"))
        start = max(0.0, a.start)
        end = min(dur, a.end) if a.end else dur
        n = max(1, int(round((end - start) * a.fps)))
        with tempfile.TemporaryDirectory() as td:
            vid = Path(td) / "v.mp4"
            enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps), "-i", "-",
                                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(a.crf), "-preset", "medium", str(vid)],
                                   stdin=subprocess.PIPE)
            for i in range(n):
                enc.stdin.write(_frame_png(page, start + i / a.fps))
                if a.progress and i % max(1, n // 10) == 0:
                    print("frame %d/%d" % (i, n), file=sys.stderr)
            enc.stdin.close()
            if enc.wait() != 0:
                raise SystemExit("ffmpeg video encode failed")
            peak = None
            if a.no_audio:
                shutil.copy(vid, out)
            else:
                wav = Path(td) / "a.wav"
                peak = _audio(page, wav, dur, voiceover=a.voiceover)
                cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-ss", "%.3f" % start, "-t", "%.3f" % (end - start), "-i", str(wav),
                       "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
                if subprocess.run(cmd).returncode != 0:
                    raise SystemExit("ffmpeg mux failed")
    finally:
        br.close(); pw.stop()
    print(json.dumps({"out": str(out), "frames": n, "fps": a.fps, "seconds": round(n / a.fps, 3), "audio_peak": peak}))


def cmd_bundle(a):
    out = _fresh(a.out, a.force)
    src = Path(a.input).resolve()
    html = src.read_text(encoding="utf-8")

    def inline_script(m):
        p = (src.parent / m.group(1)).resolve()
        return "<script>\n" + p.read_text(encoding="utf-8").replace("</script", "<\\/script") + "\n</script>"
    html = re.sub(r'<script src="([^"]+)"></script>', inline_script, html)

    def inline_font(m):
        p = (src.parent / m.group(1)).resolve()
        if not p.exists():
            return m.group(0)
        mime = "font/woff2" if p.suffix == ".woff2" else "font/ttf"
        return 'url("data:%s;base64,%s")' % (mime, base64.b64encode(p.read_bytes()).decode())
    html = re.sub(r'url\("([^"]+\.(?:woff2|ttf))"\)', inline_font, html)
    out.write_text(html, encoding="utf-8")
    print(json.dumps({"out": str(out), "bytes": out.stat().st_size, "external_refs": len(re.findall(r'src="(?!data:)', html))}))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "still", "storyboard", "render", "bundle"):
        p = sub.add_parser(name)
        p.add_argument("--in", dest="input", default=str(SKILL / "templates" / "atlas_explainer.html"))
        if name != "check":
            p.add_argument("--out", required=True)
            p.add_argument("--force", action="store_true")
        if name == "still":
            p.add_argument("--t", type=float, default=0.0)
        if name == "render":
            p.add_argument("--fps", type=int, default=30)
            p.add_argument("--crf", type=int, default=18)
            p.add_argument("--start", type=float, default=0.0)
            p.add_argument("--end", type=float, default=0.0)
            p.add_argument("--no-audio", action="store_true")
            p.add_argument("--voiceover", action="store_true", help="duck the mix for a narration track")
            p.add_argument("--progress", action="store_true")
    a = ap.parse_args(argv)
    return {"check": cmd_check, "still": cmd_still, "storyboard": cmd_storyboard, "render": cmd_render, "bundle": cmd_bundle}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
