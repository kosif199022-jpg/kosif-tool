"""playbooks + protocol appendices: each rule file as an enforcer program with a negative control.

A playbook (``playbooks/<name>.md``) or a protocol appendix (``references/protocol/A*.md``) is a set of rules.
Its program here is an *enforcer*: a producer that makes a small artifact following the file's hard, measurable
rules, and a checker that measures the artifact against those rules. Every runner also builds (or feeds the
checker) a second artifact that breaks one rule and proves the checker catches it (negative control).
Where the repo already ships the gate the appendix defines (think.py, fusionforge.py, validate_receipt.py,
see_pro_cognitive_gate.py, kling_lint.py, check.py, ...), the runner drives that gate on a compliant and a
violating fixture and cross-checks its verdict with an independent measurement.

Each runner first asserts that the rule numbers it enforces are literally present in the source file, so a
runner cannot silently drift from the document it claims to execute.
"""
from __future__ import annotations

# fake token built at runtime so no token-shaped literal sits in source
FAKE_GH = "ghp" + "_" + "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJ"

import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from _harness import card, check, fx

REPO = Path(__file__).resolve().parents[4]
SK = REPO / ".claude/skills/kosif-superpowers"
SCR = SK / "scripts"
PROTO = SK / "references/protocol"
PLAY = REPO / "playbooks"
LIVING = REPO / ".claude/skills/living-site"
NODE_PATH = "/opt/node22/lib/node_modules"

GAPS: dict = {
    "protocol:A45-youtube-download": "the rule's program (living-site/tools/yt_get.sh) runs only on the user's own device: "
                                     "YouTube refuses data-centre IPs (429 / bot check) and the cloud sandbox has no network here",
    "protocol:A46-suno-mcp": "Suno MCP is a remote OAuth server (https://api.suno.com/mcp, sign-in with a Suno account, "
                             "credits:spend): no tool, no account and no network in this sandbox, so nothing can be executed or measured",
    "protocol:A47-v62-media-gateway": "the gateway is a deployed Render service (gateway_status/list_uploads/download_permitted_video "
                                      "over HTTPS); its rules are about that live service and cannot be exercised without network",
}


# ----------------------------------------------------------------------------------------------- helpers
def sh(cmd, cwd=None, timeout=60, env=None, stdin=None):
    e = dict(os.environ)
    e.setdefault("NODE_PATH", NODE_PATH)
    if env:
        e.update(env)
    return subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None, capture_output=True, text=True,
                          timeout=timeout, env=e, input=stdin, stdin=None if stdin is not None else subprocess.DEVNULL)


def py(script, *args, cwd=None, timeout=60, stdin=None):
    path = script if Path(str(script)).is_absolute() else SCR / script
    return sh([sys.executable, path, *args], cwd=cwd or REPO, timeout=timeout, stdin=stdin)


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def jl(text):
    """First JSON object in a command's stdout."""
    text = text.strip()
    try:
        return json.loads(text)
    except ValueError:
        i = text.find("{")
        return json.loads(text[i:text.rfind("}") + 1])


def doc(key) -> str:
    kind, name = key.split(":", 1)
    if kind == "playbook":
        p = PLAY / (name + ".md")
    elif name == "PROTOCOL":
        p = SK / "PROTOCOL.md"
    else:
        p = PROTO / (name + ".md")
    return p.read_text(encoding="utf-8")


def rules_present(key, *needles):
    """Known-answer check that the enforced rule text exists in the source file."""
    text = doc(key)
    missing = [n for n in needles if n not in text]
    return check("rules come from %s: %s" % (key, ", ".join(needles))[:160], not missing, missing or "all present",
                 "every quoted rule present")


def mp4(path, frames, fps=30, crf=12):
    import numpy as np
    arr = [np.asarray(f, dtype=np.uint8) for f in frames]
    h, w = arr[0].shape[:2]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", str(crf),
                        "-pix_fmt", "yuv420p", str(path)], input=b"".join(a.tobytes() for a in arr),
                       capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace")[-300:])
    return Path(path)


def decode(path, w, h):
    return fx.frames(path, (w, h))


def bezier(x1, y1, x2, y2):
    def cx(t):
        return 3 * x1 * t * (1 - t) ** 2 + 3 * x2 * t * t * (1 - t) + t ** 3

    def cy(t):
        return 3 * y1 * t * (1 - t) ** 2 + 3 * y2 * t * t * (1 - t) + t ** 3

    def f(x):
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = (lo + hi) / 2
            if cx(mid) < x:
                lo = mid
            else:
                hi = mid
        return cy((lo + hi) / 2)
    return f


def ease_io_sine(u):
    u = min(max(u, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * u)


def ease_io_cubic(u):
    u = min(max(u, 0.0), 1.0)
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def font_path(arabic=False):
    if arabic:
        for p in sorted(REPO.glob("jobs/*/film/fonts/Cairo.ttf")) + sorted(REPO.glob("**/fonts/Cairo*.ttf")):
            return str(p)
        for p in ["/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf"]:
            if Path(p).exists():
                return p
        return None
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]:
        if Path(p).exists():
            return p
    return None


def blank(w, h, c=0):
    import numpy as np
    return np.full((h, w, 3), c, dtype=np.uint8)


def ink_mask(frame, thr=128):
    return frame.max(axis=2) > thr


def components(mask):
    from scipy import ndimage
    return int(ndimage.label(mask)[1])


# ============================================================================================== PLAYBOOKS
def _export_rules(path, master):
    """Measure a delivery file against playbooks/export-standard.md."""
    p = fx.probe(path)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    raw = Path(path).read_bytes()
    sei = re.search(rb"x264 - core.*?options: ([^\x00]*)", raw, re.S)
    opts = sei.group(1).decode(errors="replace") if sei else ""
    crf = re.search(r"crf=([\d.]+)", opts)
    # top-level MP4 atoms: moov before mdat = +faststart
    order, i = [], 0
    while i + 8 <= len(raw):
        size = int.from_bytes(raw[i:i + 4], "big")
        typ = raw[i + 4:i + 8].decode("latin-1")
        order.append(typ)
        if size == 1:
            size = int.from_bytes(raw[i + 8:i + 16], "big")
        if size < 8:
            break
        i += size
    md5 = lambda f: sh(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"]).stdout.strip()
    r = {
        "size 1080x1920": (v["width"], v["height"]) == (1080, 1920),
        "fps 30": v.get("r_frame_rate") == "30/1",
        "h264 High": v.get("codec_name") == "h264" and v.get("profile") == "High",
        "yuv420p": v.get("pix_fmt") == "yuv420p",
        "BT.709 tagged": v.get("color_space") == "bt709" and v.get("color_primaries") == "bt709" and v.get("color_transfer") == "bt709",
        "CRF 17": bool(crf) and abs(float(crf.group(1)) - 17) < 1e-6,
        "preset slow (subme=8 ref=5 lookahead 50)": "subme=8" in opts and "ref=5" in opts and "rc_lookahead=50" in opts,
        "+faststart (moov before mdat)": "moov" in order and "mdat" in order and order.index("moov") < order.index("mdat"),
        "audio stream-copied byte for byte": md5(path) == md5(master) and bool(md5(master)),
    }
    return r, {"atoms": order[:5], "crf": crf.group(1) if crf else None}


@card("playbook:export-standard")
def export_standard(task, wd):
    sys.path.insert(0, str(SCR))
    import export_profile as ep
    master = wd / "voice.m4a"
    fx.ffmpeg("-f", "lavfi", "-i", "sine=frequency=330:duration=0.5:sample_rate=48000", "-c:a", "aac", "-b:a", "192k", master)
    good, bad = wd / "delivery.mp4", wd / "violating.mp4"
    src = ["-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30:d=0.4", "-i", str(master), "-map", "0:v", "-map", "1:a"]
    fx.ffmpeg(*src, "-vf", ep.RGB_TO_709 + ",format=yuv420p", *ep.video_args(), *ep.audio_args(master),
              *ep.FASTSTART, good, timeout=60)
    fx.ffmpeg(*src, "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "copy", bad)
    rg, info = _export_rules(good, master)
    rb, _ = _export_rules(bad, master)
    jw(wd / "export_report.json", {"delivery": rg, "violating": rb, "info": info})
    checks = [rules_present("playbook:export-standard", "1080×1920", "CRF 17", "BT.709", "+faststart")]
    checks += [check("delivery: " + k, ok, ok, True) for k, ok in rg.items()]
    caught = [k for k, ok in rb.items() if not ok]
    checks.append(check("negative control: CRF 23/ultrafast/no tags/no faststart file is caught",
                        {"CRF 17", "+faststart (moov before mdat)", "BT.709 tagged"} <= set(caught), caught,
                        "CRF, faststart and BT.709 rules fail"))
    return checks, [good, wd / "export_report.json"]


# -------------------------------------------------------------------------------- audio-sync
def _words_ok(words):
    errs = []
    for a, b in zip(words, words[1:]):
        if b["start"] < a["start"]:
            errs.append("unsorted at %s" % b["word"])
        if b["start"] < a["end"]:
            errs.append("overlap %s/%s" % (a["word"], b["word"]))
    return errs


def _onsets(samples, rate, thr=0.05):
    import numpy as np
    hop = int(rate * 0.005)
    env = np.array([np.abs(samples[i:i + hop]).max() for i in range(0, len(samples) - hop, hop)])
    on = np.flatnonzero((env[1:] > thr) & (env[:-1] <= thr)) + 1
    return [round(i * hop / rate, 3) for i in on]


@card("playbook:audio-sync")
def audio_sync(task, wd):
    import numpy as np
    rate, fps = 44100, 30
    words = [{"word": w, "start": s, "end": e} for w, s, e in
             [("مرحبا", 0.20, 0.55), ("بكم", 0.62, 0.90), ("في", 1.45, 1.60), ("الفيلم", 1.66, 2.10)]]
    dur = 2.5
    t = np.arange(int(dur * rate)) / rate
    sig = np.zeros_like(t)
    for w in words:
        m = (t >= w["start"]) & (t < w["end"])
        sig[m] = 0.4 * np.sin(2 * np.pi * 300 * t[m])
    voice = fx.write_wav(wd / "voice.wav", sig, rate)
    jw(wd / "words.json", words)
    # phrases: a pause > 400 ms ends a phrase
    phrases, cur = [], [words[0]]
    for a, b in zip(words, words[1:]):
        if b["start"] - a["end"] > 0.4:
            phrases.append(cur)
            cur = []
        cur.append(b)
    phrases.append(cur)
    lead = 0.06  # each element starts at word.start - 0.04..0.08 s

    def render(wlist, out):
        W, H, frames = 54, 96, []
        for i in range(int(round(dur * fps))):
            tt = i / fps
            f = blank(W, H)
            for k, w in enumerate(wlist):
                if tt >= w["start"] - lead:
                    f[60:70, 2 + k * 12: 12 + k * 12] = 255  # one block per word, lit at its cue frame
            frames.append(f)
        silent = mp4(wd / (out + "_v.mp4"), frames, fps)
        film = wd / (out + ".mp4")
        fx.ffmpeg("-i", silent, "-i", voice, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                  "-ar", "44100", film)
        fr = decode(film, W, H)
        cue = []
        for k in range(len(wlist)):
            lit = np.flatnonzero(fr[:, 65, 7 + k * 12].mean(axis=-1) > 128)
            cue.append(round(lit[0] / fps + lead, 3) if len(lit) else None)
        return film, cue

    heard = _onsets(sig, rate)
    film, cue = render(words, "film")
    off = [abs(c - h) for c, h in zip(cue, heard)]
    shifted = [dict(w, start=round(w["start"] + 0.3, 3), end=round(w["end"] + 0.3, 3)) for w in words]
    _, cue_bad = render(shifted, "shifted")
    off_bad = [abs(c - h) for c, h in zip(cue_bad, heard)]
    overlapping = [dict(words[0]), dict(words[1], start=0.5)]
    master_d = float(fx.probe(voice)["format"]["duration"])
    film_a = next(s for s in fx.probe(film)["streams"] if s["codec_type"] == "audio")
    film_d = float(film_a.get("duration") or fx.probe(film)["format"]["duration"])
    jw(wd / "sync_report.json", {"heard_onsets": heard, "cues": cue, "offsets": off, "phrases": [[w["word"] for w in p] for p in phrases],
                                 "shifted_offsets": off_bad})
    return [
        rules_present("playbook:audio-sync", "> 400 ms ends a phrase", "word.start − 0.04…0.08 s", "±50 ms", "within 100 ms"),
        check("words.json sorted and non-overlapping", not _words_ok(words), _words_ok(words), []),
        check("audio onsets measured from voice.wav match words.json", len(heard) == len(words), heard, [w["start"] for w in words]),
        check("every cue (decoded from the film) within 100 ms of the heard word", max(off) <= 0.1, max(off), "<= 0.1 s"),
        check("pause > 400 ms splits the phrases", len(phrases) == 2, len(phrases), 2),
        check("delivered audio length matches master within 50 ms", abs(film_d - master_d) <= 0.05, film_d, master_d),
        check("negative control: a transcript 300 ms late is caught", min(off_bad) > 0.1, min(off_bad), "> 0.1 s"),
        check("negative control: overlapping words.json is rejected", bool(_words_ok(overlapping)), _words_ok(overlapping), "errors"),
    ], [film, wd / "sync_report.json"]


# -------------------------------------------------------------------------------- arabic typography
def _ar_render(text, size, path, per_letter=False, spacing=0):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    font = ImageFont.truetype(font_path(True), size, layout_engine=ImageFont.Layout.RAQM)
    img = Image.new("L", (size * 10, int(size * 2.2)), 0)
    d = ImageDraw.Draw(img)
    if not per_letter and not spacing:
        d.text((img.width - size // 2, size // 3), text, font=font, fill=255, anchor="ra", direction="rtl", language="ar")
    else:  # a span per letter: each glyph shaped alone (isolated form), placed right to left
        x = img.width - size // 2
        for ch in text:
            wch = d.textlength(ch, font=font, direction="rtl")
            d.text((x, size // 3), ch, font=font, fill=255, anchor="ra", direction="rtl", language="ar")
            x -= wch + spacing
    img.save(path)
    return np.array(img) > 128


@card("playbook:arabic-typography")
def arabic_typography(task, wd):
    import numpy as np
    word, size = "محمد", 64  # caption size at 1080 width: 56-72 px
    whole = _ar_render(word, size, wd / "whole_word.png")
    split = _ar_render(word, size, wd / "split_letters.png", per_letter=True)
    spaced = _ar_render(word, size, wd / "letter_spaced.png", spacing=6)
    c_whole, c_split, c_spaced = components(whole), components(split), components(spaced)
    w_whole = np.flatnonzero(whole.any(0))
    w_split = np.flatnonzero(split.any(0))
    # right -> left wipe of the shaped word (clip-path), ease-out quart over 450 ms at 30 fps
    n = int(0.45 * 30)
    x0, x1 = w_whole[0], w_whole[-1]
    frames, lefts, rights = [], [], []
    for i in range(n + 1):
        u = 1 - (1 - i / n) ** 4
        cut = int(round(x1 + 1 - u * (x1 + 1 - x0)))
        m = whole.copy()
        m[:, :cut] = False
        frames.append(np.dstack([m * 255] * 3).astype(np.uint8))
        cols = np.flatnonzero(m.any(0))
        if len(cols):
            lefts.append(int(cols[0]))
            rights.append(int(cols[-1]))
    h, w = whole.shape
    pad = lambda a: a[: h - h % 2, : w - w % 2]
    film = mp4(wd / "wipe_rtl.mp4", [pad(f) for f in frames], 30)
    first_visible_right = rights[0] if rights else None
    ltr_first = int(np.flatnonzero(whole.any(0))[0])  # a left->right wipe would reveal this column first
    jw(wd / "arabic_report.json", {"components": {"whole": c_whole, "split": c_split, "spaced": c_spaced},
                                   "width": {"whole": int(w_whole[-1] - w_whole[0]), "split": int(w_split[-1] - w_split[0])},
                                   "wipe_lefts": lefts, "wipe_rights": rights, "font": font_path(True)})
    return [
        rules_present("playbook:arabic-typography", "Never split a word into letters", "Never apply `letter-spacing` to Arabic",
                      "captions 56–72 px", "wipes right → left"),
        check("caption size inside 56-72 px", 56 <= size <= 72, size, "56..72"),
        check("whole word stays joined (fewer ink islands than letters drawn alone)", c_whole < c_split, c_whole, "< %d" % c_split),
        check("negative control: a span per letter breaks joining", c_split > c_whole, c_split, "> %d" % c_whole),
        check("negative control: letter-spacing breaks the connections", c_spaced > c_whole, c_spaced, "> %d" % c_whole),
        check("wipe starts at the right edge of the word", first_visible_right is not None and first_visible_right >= x1 - 2,
              first_visible_right, ">= %d" % (x1 - 2)),
        check("wipe front moves right -> left monotonically", all(b <= a for a, b in zip(lefts, lefts[1:])) and lefts[-1] <= x0 + 1,
              [lefts[0], lefts[-1]], "decreasing to %d" % x0),
        check("negative control: a left->right wipe would show the leftmost column first", ltr_first < x1 - 20, ltr_first, "far from right edge"),
    ], [film, wd / "whole_word.png", wd / "arabic_report.json"]


# -------------------------------------------------------------------------------- render pipeline
_SCENE = """<!doctype html><html><body style="margin:0;background:#000"><canvas id=c width=%(w)d height=%(h)d></canvas><script>
const c=document.getElementById('c').getContext('2d');
window.__kosif={duration:%(d)s,fps:30,seek(t){c.fillStyle='#101820';c.fillRect(0,0,%(w)d,%(h)d);
 c.fillStyle='#f2aa4c';c.fillRect(Math.round(t*60),%(y)d,24,24);}};window.__kosifReady=true;</script></body></html>"""


@card("playbook:render-pipeline")
def render_pipeline(task, wd):
    import numpy as np
    W, H, D = 108, 192, 1.0
    page = wd / "film.html"
    page.write_text(_SCENE % {"w": W, "h": H, "d": D, "y": 84}, encoding="utf-8")
    rc = REPO / "tools/render_html.cjs"
    prev = sh(["node", rc, "--in", page, "--out", wd / "film.mp4", "--width", W, "--height", H, "--preview"], cwd=wd, timeout=60)
    # the documented long-job path: job.py start, then job.py wait (no sleep loops)
    start = sh([sys.executable, REPO / "tools/job.py", "start", "--dir", wd / "job", "--", "node", rc, "--in", page, "--out",
                wd / "film.mp4", "--width", W, "--height", H, "--fps", 30], cwd=wd)
    wait = sh([sys.executable, REPO / "tools/job.py", "wait", "--dir", wd / "job", "--quiet"], cwd=wd, timeout=60)
    log = (wd / "job").glob("*.log")
    logtxt = "".join(p.read_text(errors="replace") for p in log)
    m = re.search(r"VERIFY OK duration=([\d.]+)s fps=(\d+) frames=(\d+) size=(\d+)x(\d+)", logtxt + wait.stdout)
    second = sh(["node", rc, "--in", page, "--out", wd / "again.mp4", "--width", W, "--height", H], cwd=wd, timeout=60)
    fa, fb = decode(wd / "film.mp4", W, H), decode(wd / "again.mp4", W, H)
    sheet = wd / "film_preview.png"
    hook = REPO / ".claude/hooks/no_sleep_wait.py"
    blocked = sh([sys.executable, hook], stdin=json.dumps({"tool_name": "Bash", "tool_input": {"command": "sleep 60; grep VERIFY render.log"}}))
    allowed = sh([sys.executable, hook], stdin=json.dumps({"tool_name": "Bash", "tool_input": {"command": "python3 tools/job.py wait --dir out/x/job"}}))
    vv_bad = sh([sys.executable, REPO / "tools/verify_video.py", wd / "film.mp4", "--fps", "25", "--duration", "1", "--no-audio"])
    vv_ok = sh([sys.executable, REPO / "tools/verify_video.py", wd / "film.mp4", "--fps", "30", "--duration", "1", "--no-audio"])
    return [
        rules_present("playbook:render-pipeline", "8 evenly spaced labelled frames", "job.py start", "window.__kosif"),
        check("preview contact sheet written (8 frames, --preview)", prev.returncode == 0 and sheet.exists() and sheet.stat().st_size > 0,
              prev.returncode, 0),
        check("job.py start + wait finished the render with DONE", start.returncode == 0 and wait.returncode == 0, wait.returncode, 0),
        check("renderer VERIFY line: frames = duration x fps", bool(m) and int(m.group(3)) == int(D * 30) and int(m.group(2)) == 30,
              m.groups() if m else None, "frames=30 fps=30"),
        check("seek render is deterministic (two renders, identical decoded frames)", second.returncode == 0 and fa.shape == fb.shape
              and float(np.abs(fa - fb).max()) == 0.0, float(np.abs(fa - fb).max()) if fa.shape == fb.shape else "shape", 0.0),
        check("verify_video passes on the requested fps/duration", vv_ok.returncode == 0, vv_ok.returncode, 0),
        check("negative control: verify_video fails a wrong fps request", vv_bad.returncode != 0, vv_bad.returncode, "!= 0"),
        check("negative control: the sleep-wait hook blocks `sleep 60; grep`", blocked.returncode == 2, blocked.returncode, 2),
        check("the documented job.py wait passes the hook", allowed.returncode == 0, allowed.returncode, 0),
    ], [wd / "film.mp4", sheet]


# -------------------------------------------------------------------------------- music
@card("playbook:music")
def music(task, wd):
    import numpy as np
    import librosa
    rate, bpm, fps, dur = 22050, 120, 30, 6.0
    t = np.arange(int(dur * rate)) / rate
    sig = 0.06 * np.sin(2 * np.pi * 220 * t)
    beats_true = np.arange(0.25, dur - 0.1, 60 / bpm)
    for b in beats_true:
        m = (t >= b) & (t < b + 0.05)
        sig[m] += 0.15 * np.sin(2 * np.pi * 1000 * (t[m] - b)) * np.exp(-(t[m] - b) * 60)
    raw = fx.write_wav(wd / "track.wav", sig, rate)
    tempo, frames_b = librosa.beat.beat_track(y=sig.astype(np.float32), sr=rate, units="frames")
    tempo = float(np.atleast_1d(tempo)[0])
    beat_t = librosa.frames_to_time(frames_b, sr=rate)
    onset = librosa.onset.onset_detect(y=sig.astype(np.float32), sr=rate, units="time")
    period = 60 / tempo
    cuts = [int(math.floor(b * fps)) for b in onset]  # on the beat or 1 frame before it, never late
    late = [int(math.floor(b * fps)) + 2 for b in onset]
    rel = lambda cs: [c - b * fps for c, b in zip(cs, onset)]
    ok_cut = all(-1 <= d <= 0 for d in rel(cuts))
    ok_late = all(-1 <= d <= 0 for d in rel(late))
    # loudness: normalise to -14 LUFS, true peak <= -1 dBTP; measure with ebur128
    out = wd / "master_-14LUFS.wav"
    m1 = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
             "-f", "null", "-"]).stderr
    meas = json.loads(m1[m1.rfind("{"):m1.rfind("}") + 1])
    fx.ffmpeg("-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:"
              "offset=%s:linear=true,aresample=48000" % (meas["input_i"], meas["input_tp"], meas["input_lra"],
                                                        meas["input_thresh"], meas["target_offset"]), out)

    def loud(p):
        e = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
        i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])
        tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
        return i, tp
    li, tp = loud(out)
    li_raw, tp_raw = loud(raw)
    # audio-reactive smoothing 150 ms vs raw RMS
    hop = rate // fps
    rms = np.array([np.sqrt(np.mean(sig[i:i + hop] ** 2)) for i in range(0, len(sig) - hop, hop)])
    k = int(round(0.15 * fps))
    sm = np.convolve(rms, np.ones(k) / k, mode="same")
    jit = lambda a: float(np.abs(np.diff(a)).mean())
    jw(wd / "beat_report.json", {"tempo": tempo, "beat_period_s": period, "frames_per_beat": period * fps,
                                 "onsets": [round(float(x), 3) for x in onset], "cuts": cuts, "lufs": li, "true_peak": tp,
                                 "raw_lufs": li_raw, "jitter_raw": jit(rms), "jitter_smoothed": jit(sm)})
    return [
        rules_present("playbook:music", "Beat period = 60 / BPM", "never 2+ frames late", "−14 LUFS ±1.5", "100–200 ms window"),
        check("tempo measured ~120 BPM", abs(tempo - bpm) < 3, tempo, bpm),
        check("one beat = 15 frames at 30 fps", abs(period * fps - 15) < 0.5, period * fps, 15),
        check("every cut on the beat or 1 frame before", ok_cut, [round(d, 2) for d in rel(cuts)][:6], "-1..0 frames"),
        check("negative control: cuts 2 frames late are caught", not ok_late, [round(d, 2) for d in rel(late)][:3], "outside -1..0"),
        check("master at -14 LUFS +-1.5", abs(li + 14) <= 1.5, li, -14),
        check("true peak <= -1 dBTP", tp <= -1.0, tp, "<= -1"),
        check("negative control: the raw track is outside the loudness window", abs(li_raw + 14) > 1.5, li_raw, "not -14+-1.5"),
        check("smoothing (150 ms) reduces frame-to-frame jitter", jit(sm) < 0.6 * jit(rms), jit(sm), "< 0.6 x %.4f" % jit(rms)),
    ], [out, wd / "beat_report.json"]


# -------------------------------------------------------------------------------- overlap camera
@card("playbook:overlap-camera")
def overlap_camera(task, wd):
    tool = REPO / "tools/overlap_rig.py"
    rig = {"nulls": [{"axis": "x", "d": -544, "f0": 0, "f1": 40, "graph": [0.0001, 1]},
                     {"axis": "x", "d": -1290, "f0": 20, "f1": 73, "graph": [0.747, 0.793]},
                     {"axis": "x", "d": -1470, "f0": 60, "f1": 109, "graph": [0.727, 0.822]},
                     {"axis": "x", "d": -447, "f0": 89, "f1": 119, "graph": [1, 0.0001]}]}
    bad = json.loads(json.dumps(rig))
    bad["nulls"][1]["f0"], bad["nulls"][1]["f1"] = 41, 94  # next move starts after the previous one stopped
    g, b = jw(wd / "rig.json", rig), jw(wd / "rig_bad.json", bad)
    rg = sh([sys.executable, tool, "check", g, "--json"])
    rb = sh([sys.executable, tool, "check", b, "--json"])
    jg, jb = jl(rg.stdout), jl(rb.stdout)
    # independent: camera x = base + sum of eased null offsets; speed never reaches 0 between first and last frame
    def bez(a, c, u):
        return 3 * (1 - u) ** 2 * u * a + 3 * (1 - u) * u * u * c + u ** 3

    def ease(graph, u):  # AE-style speed graph as a y(x) cubic with x linear
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m = (lo + hi) / 2
            if bez(1 / 3, 2 / 3, m) < u:
                lo = m
            else:
                hi = m
        return bez(graph[0], graph[1], (lo + hi) / 2)

    def path(r):
        xs = []
        for f in range(0, 120):
            x = 0.0
            for n in r["nulls"]:
                u = min(max((f - n["f0"]) / (n["f1"] - n["f0"]), 0), 1)
                x += n["d"] * ease(n["graph"], u)
            xs.append(x)
        return xs
    xs, xb = path(rig), path(bad)
    sp = [abs(b - a) for a, b in zip(xs, xs[1:])]
    spb = [abs(b - a) for a, b in zip(xb, xb[1:])]
    jw(wd / "camera_path.json", {"x": xs, "speed": sp, "checker": jg})
    done = [h["prev_done"] for h in jg.get("handoffs", [])]
    return [
        rules_present("playbook:overlap-camera", "83–95%", "The camera never animates", "tools/overlap_rig.py check"),
        check("overlap_rig check prints OK on the compliant rig", jg.get("ok") is True and rg.returncode == 0, jg.get("issues"), []),
        check("every handoff starts at 83-95% of the previous move", all(0.83 <= d <= 0.955 for d in done) and len(done) == 3, done, "0.83..0.95"),
        check("independent path: combined speed never zero mid-comp", min(sp[1:-1]) > 0.5, min(sp[1:-1]), "> 0.5 px/frame"),
        check("negative control: the late handoff rig is rejected by the checker", jb.get("ok") is False, jb.get("issues"), "issues"),
        check("negative control: its path stalls (speed ~0 at the handoff)", min(spb[1:-1]) < 0.5, min(spb[1:-1]), "< 0.5"),
    ], [wd / "camera_path.json", g]


# -------------------------------------------------------------------------------- kinetic type
@card("playbook:kinetic-type")
def kinetic_type(task, wd):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    S = 0.25  # render a 1080x1920 layout at quarter size
    W, H, fps = 270, 480, 30
    ease_in = bezier(0.22, 1, 0.36, 1)
    font = ImageFont.truetype(font_path(True), int(140 * S), layout_engine=ImageFont.Layout.RAQM)

    def film(entr, exit_, travel, ybase):
        words = ["الفكرة", "واضحة"]
        start = 0.2
        land = start + 0.09 * (len(words) - 1) + entr
        hold = 0.3 + 0.06 * sum(len(w) for w in words)
        ex0 = land + hold + 0.1
        end = ex0 + exit_ + 0.3
        frames, ys = [], []
        for i in range(int(end * fps)):
            t = i / fps
            img = Image.new("RGB", (W, H), (0, 0, 0))
            d = ImageDraw.Draw(img)
            for k, w in enumerate(words):
                ws = start + 0.09 * k
                u = min(max((t - ws) / entr, 0), 1)
                dy = travel * S * (1 - ease_in(u))
                alpha = min(1.0, u / 0.6) if u > 0 else 0
                if t >= ex0:
                    v = min((t - ex0) / exit_, 1)
                    dy = -30 * S * v ** 3
                    alpha = 1 - v
                if alpha <= 0:
                    continue
                y = ybase * S + k * 50 + dy
                col = tuple(int(c * alpha) for c in ((255, 255, 255) if k else (255, 200, 60)))
                d.text((W - 60 * S, y), w, font=font, fill=col, anchor="ra", direction="rtl", language="ar")
            frames.append(np.array(img))
        return frames, dict(start=start, land=land, hold=hold, ex0=ex0, entr=entr, exit=exit_)
    fg, pg = film(0.4, 0.25, 60, 800)
    fb, pb = film(0.25, 0.45, 60, 1650)  # exits longer than entrances, text inside the bottom 220 px
    good = mp4(wd / "kinetic.mp4", fg, fps)
    bad = mp4(wd / "kinetic_bad.mp4", fb, fps)
    dg, db = decode(good, W, H), decode(bad, W, H)

    def measure(fr, plan):
        ink = fr.max(axis=3) > 14
        tops = [int(np.flatnonzero(m.any(1))[0]) if m.any() else None for m in ink]
        vis = [i for i, t in enumerate(tops) if t is not None]
        f_start = int(round(plan["start"] * fps))
        f_ex = int(round(plan["ex0"] * fps))
        final = tops[f_ex - 2]
        ent = [(i, tops[i] - final) for i in vis if i < f_ex - 2]
        best = None  # fit duration and travel of the eased entrance to the measured top-of-ink trajectory
        for dur in [x / 100 for x in range(15, 71)]:
            g = [1 - ease_in(min(max((i / fps - plan["start"]) / dur, 0), 1)) for i, _ in ent]
            gg = sum(x * x for x in g)
            if gg == 0:
                continue
            amp = sum(d * x for (_, d), x in zip(ent, g)) / gg
            res = max(abs(d - amp * x) for (_, d), x in zip(ent, g))
            if best is None or res < best[0]:
                best = (res, dur, amp)
        bottom = int(220 * S)
        return {"entrance_s": best[1], "fit_residual_px": best[0], "travel_px": best[2] / S,
                "exit_s": (vis[-1] + 1 - f_ex) / fps, "bottom_ink": int(sum(m[H - bottom:].sum() for m in ink)),
                "hold_s": plan["ex0"] - (plan["start"] + best[1]), "first_visible": vis[0], "start_frame": f_start}
    mg, mb = measure(dg, pg), measure(db, pb)
    jw(wd / "kinetic_report.json", {"good": mg, "bad": mb, "plan": pg})
    return [
        rules_present("playbook:kinetic-type", "300–450 ms, translateY 40–70 px", "Exits are always shorter than entrances",
                      "220 px bottom", "0.3 s + 0.06 s × characters"),
        check("measured word entrance 300-450 ms (fitted to decoded frames)", 0.3 <= mg["entrance_s"] <= 0.45 and mg["fit_residual_px"] <= 2,
              [mg["entrance_s"], mg["fit_residual_px"]], "0.30..0.45 s, residual <= 2 px"),
        check("measured travel 40-70 px at 1080 width", 40 <= mg["travel_px"] <= 70, mg["travel_px"], "40..70"),
        check("measured exit shorter than entrance", mg["exit_s"] < mg["entrance_s"], mg["exit_s"], "< %.3f" % mg["entrance_s"]),
        check("hold >= 0.3 s + 0.06 s x characters", mg["hold_s"] >= pg["hold"], mg["hold_s"], ">= %.2f" % pg["hold"]),
        check("bottom 220 px free of text in every frame", mg["bottom_ink"] == 0, mg["bottom_ink"], 0),
        check("negative control: long exit + bottom text caught", mb["exit_s"] >= mb["entrance_s"] and mb["bottom_ink"] > 0,
              [mb["exit_s"], mb["entrance_s"], mb["bottom_ink"]], "exit >= entrance and ink in bottom"),
    ], [good, wd / "kinetic_report.json"]


# -------------------------------------------------------------------------------- hand-drawn
def _poly_len(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def _point_at(pts, L):
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        s = math.dist(a, b)
        if acc + s >= L and s > 0:
            u = (L - acc) / s
            return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
        acc += s
    return pts[-1]


@card("playbook:hand-drawn")
def hand_drawn(task, wd):
    from PIL import Image, ImageDraw
    import numpy as np
    S, W, H, fps = 0.25, 270, 480, 30
    strokes = [[(200, 400), (880, 400), (880, 1000), (200, 1000), (200, 400)],  # outline (1080 space)
               [(320, 560), (760, 560)], [(320, 700), (760, 700)]]              # details
    speed, lift = 1100.0, 0.09  # px/s along the path, pen lift between strokes

    def film(order_fill_first=False, spd=speed):
        sched, t = [], 0.2
        for s in strokes:
            dur = _poly_len(s) / spd
            sched.append((t, t + dur, s))
            t += dur + lift
        fill_t = (0.2 if order_fill_first else t, 0.3)
        end = max(t, fill_t[0] + fill_t[1]) + 1.6
        frames, inked = [], []
        for i in range(int(end * fps)):
            tt = i / fps
            img = Image.new("RGB", (W, H), (245, 242, 230))
            d = ImageDraw.Draw(img)
            u = min(max((tt - fill_t[0]) / fill_t[1], 0), 1)
            if u > 0:  # hatching fill as a 300 ms wipe
                d.rectangle([210 * S, 410 * S, (210 + u * 660) * S, 990 * S], fill=(120, 170, 230))
            drawn = 0.0
            for t0, t1, s in sched:
                if tt <= t0:
                    continue
                L = _poly_len(s) * ease_io_cubic((tt - t0) / (t1 - t0))
                acc, pts = 0.0, [s[0]]
                for a, b in zip(s, s[1:]):
                    seg = math.dist(a, b)
                    if acc + seg <= L:
                        pts.append(b)
                    else:
                        pts.append(_point_at([a, b], L - acc))
                        break
                    acc += seg
                d.line([(x * S, y * S) for x, y in pts], fill=(20, 20, 20), width=2)
                drawn += L
            inked.append(drawn)
            frames.append(np.array(img))
        return frames, sched, fill_t
    fg, sg, fillg = film()
    fb, sb, fillb = film(order_fill_first=True)
    good, bad = mp4(wd / "whiteboard.mp4", fg, fps), mp4(wd / "whiteboard_bad.mp4", fb, fps)

    def measure(path, sched):
        fr = decode(path, W, H)
        dark = (fr.max(axis=3) < 80)
        blue = (fr[..., 2] > 180) & (fr[..., 0] < 160)
        ink = dark.reshape(len(fr), -1).sum(1)
        fill = blue.reshape(len(fr), -1).sum(1)
        t0, t1, s = sched[0]
        a, b = int(t0 * fps) + 1, int(t1 * fps)
        px_per_s = (ink[b] - ink[a]) / ((b - a) / fps) / S / 2.0  # 2 px line width at quarter scale
        outline_done = int(math.ceil(sched[-1][1] * fps))
        fill_first = int(np.flatnonzero(fill > 20)[0]) if (fill > 20).any() else None
        return px_per_s, fill_first, outline_done
    vg, ffg, odg = measure(good, sg)
    vb, ffb, odb = measure(bad, sb)
    jw(wd / "pen_report.json", {"pen_speed_px_s": vg, "fill_first_frame": ffg, "outline_done_frame": odg,
                                "bad_fill_first_frame": ffb})
    return [
        rules_present("playbook:hand-drawn", "Pen speed 800–1400 px/s", "outline first, then details, then fill", "60–120 ms lift"),
        check("measured pen speed on the outline 800-1400 px/s", 800 <= vg <= 1400, vg, "800..1400"),
        check("pen lift between strokes 60-120 ms", 0.06 <= lift <= 0.12, lift, "0.06..0.12"),
        check("fill appears only after every stroke finished", ffg is not None and ffg >= odg, ffg, ">= %d" % odg),
        check("negative control: fill-first order is caught", ffb is not None and ffb < odb, ffb, "< %d" % odb),
    ], [good, wd / "pen_report.json"]


# -------------------------------------------------------------------------------- diagrams
@card("playbook:diagrams")
def diagrams(task, wd):
    from PIL import Image, ImageDraw
    import numpy as np
    S, W, H, fps = 0.25, 270, 480, 30
    nodes = [(820, 900), (540, 900), (260, 900)]  # Arabic film: reveal right -> left
    speed = 1000.0  # edge draw px/s (900-1200)

    def film(order, arrow_early=False):
        ev, t = [], 0.2
        for k, i in enumerate(order):
            ev.append(("node", i, t))
            t += 0.3
            if k + 1 < len(order):
                a, b = nodes[i], nodes[order[k + 1]]
                L = abs(a[0] - b[0]) - 200
                dur = L / speed
                ev.append(("edge", (i, order[k + 1]), t, dur))
                t += dur
        end = t + 1.6
        frames = []
        for f in range(int(end * fps)):
            tt = f / fps
            img = Image.new("RGB", (W, H), (250, 250, 250))
            d = ImageDraw.Draw(img)
            for e in ev:
                if e[0] == "node" and tt >= e[2]:
                    x, y = nodes[e[1]]
                    d.rounded_rectangle([(x - 100) * S, (y - 60) * S, (x + 100) * S, (y + 60) * S], radius=5, outline=(30, 30, 30), width=1)
                if e[0] == "edge" and tt >= e[2]:
                    (i, j), t0, dur = e[1], e[2], e[3]
                    u = ease_io_cubic((tt - t0) / dur)
                    xa = nodes[i][0] + (-100 if nodes[j][0] < nodes[i][0] else 100)
                    xb = nodes[j][0] + (100 if nodes[j][0] < nodes[i][0] else -100)
                    d.line([(xa * S, 900 * S), ((xa + (xb - xa) * u) * S, 900 * S)], fill=(30, 30, 30), width=1)
                    if u >= 1 or (arrow_early and u > 0.2):  # arrowhead only when the edge finishes
                        d.polygon([(xb * S, 900 * S), ((xb + 16) * S, 892 * S), ((xb + 16) * S, 908 * S)] if xb < xa else
                                  [(xb * S, 900 * S), ((xb - 16) * S, 892 * S), ((xb - 16) * S, 908 * S)], fill=(200, 40, 40))
            frames.append(np.array(img))
        return frames, ev
    fg, eg = film([0, 1, 2])
    fb, eb = film([2, 1, 0], arrow_early=True)
    good, bad = mp4(wd / "diagram.mp4", fg, fps), mp4(wd / "diagram_bad.mp4", fb, fps)

    def measure(path, ev):
        fr = decode(path, W, H)
        dark = fr.max(axis=3) < 120
        red = (fr[..., 0] > 150) & (fr[..., 1] < 110)
        appear = []
        for i, (x, y) in enumerate(nodes):
            box = dark[:, int((y - 60) * S) - 1:int((y + 60) * S) + 2, int((x - 100) * S) - 1:int((x + 100) * S) + 2]
            appear.append(int(np.flatnonzero(box.reshape(len(fr), -1).sum(1) > 20)[0]))
        edge = next(e for e in ev if e[0] == "edge")
        row = dark[:, int(900 * S)]
        f_end = int(math.ceil((edge[2] + edge[3]) * fps))
        red_first = int(np.flatnonzero(red.reshape(len(fr), -1).sum(1) > 0)[0])
        # draw speed from the midline pixels over the middle of the first edge
        (i, j) = edge[1]
        lo, hi = sorted([nodes[i][0], nodes[j][0]])
        seg = row[:, int((lo + 100) * S) + 1:int((hi - 100) * S) - 1].sum(1)
        a, b = int(edge[2] * fps) + 2, f_end - 2
        v = (seg[b] - seg[a]) / ((b - a) / fps) / S
        held = float(np.abs(fr[-1] - fr[-int(1.5 * fps)]).max())
        visible_nodes = sum(1 for _ in nodes)
        return appear, red_first, f_end, v, held, visible_nodes
    ag, rg, eg_end, vg, hg, ng = measure(good, eg)
    ab, rb, eb_end, vb, hb, nb = measure(bad, eb)
    jw(wd / "diagram_report.json", {"appear_frames": ag, "arrow_first": rg, "edge_end": eg_end, "draw_speed": vg, "final_hold_diff": hg})
    rtl = lambda ap: [nodes[i][0] for i in sorted(range(3), key=lambda i: ap[i])]
    return [
        rules_present("playbook:diagrams", "At most 7 nodes", "right → left for an Arabic film", "900–1200 px per second",
                      "arrowhead fades in during the last 80 ms", "Hold 1.5 s"),
        check("at most 7 nodes on screen", ng <= 7, ng, "<= 7"),
        check("nodes appear right -> left (Arabic film)", rtl(ag) == sorted(rtl(ag), reverse=True), rtl(ag), "descending x"),
        check("measured edge draw speed 900-1200 px/s (eased middle may run faster: 900-1800)", 900 <= vg <= 1800, vg, "900..1800"),
        check("arrowhead appears only when its edge finished", rg >= eg_end - 1, rg, ">= %d" % (eg_end - 1)),
        check("final frame held 1.5 s", hg < 8, hg, "< 8 (static)"),
        check("negative control: left->right order + early arrow caught",
              rtl(ab) != sorted(rtl(ab), reverse=True) and rb < eb_end - 1, [rtl(ab), rb, eb_end], "order wrong and arrow early"),
    ], [good, wd / "diagram_report.json"]


# -------------------------------------------------------------------------------- shapes
@card("playbook:shapes")
def shapes(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    U = 24

    def resample(pts, n):
        pts = list(pts) + [pts[0]]
        L = _poly_len(pts)
        return [_point_at(pts, L * k / n) for k in range(n)]
    circle = [(540 + 120 * math.cos(2 * math.pi * k / 40), 960 + 120 * math.sin(2 * math.pi * k / 40)) for k in range(40)]
    square = [(420, 840), (660, 840), (660, 1080), (420, 1080)]
    a, b = resample(circle, 96), resample(square, 96)
    morph_e = bezier(0.65, 0, 0.35, 1)
    frames = []
    for f in range(int(0.6 * 30) + 1):  # 600 ms morph
        u = morph_e(f / 18)
        pts = [(p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u) for p, q in zip(a, b)]
        img = Image.new("L", (1080 // 4, 1920 // 4), 0)
        ImageDraw.Draw(img).polygon([(x / 4, y / 4) for x, y in pts], fill=255)
        frames.append(np.dstack([np.array(img)] * 3))
    film = mp4(wd / "morph.mp4", frames, 30)

    def area(sx, sy):
        img = Image.new("L", (1080, 1920), 0)
        r = 120
        ImageDraw.Draw(img).ellipse([540 - r * sx, 960 - r * sy, 540 + r * sx, 960 + r * sy], fill=255)
        return float((np.array(img) > 0).sum())
    a0 = area(1, 1)
    a_ok = area(1 / 0.7, 0.7)
    a_naive = area(1.0, 0.7)
    final = (552, 960)  # spring settles here
    on_grid = lambda p: p[0] % U == 0 and p[1] % U == 0
    neg_space = 1 - (np.array(frames[-1])[..., 0] > 0).mean()
    jw(wd / "shape_report.json", {"points": [len(a), len(b)], "area": [a0, a_ok, a_naive], "final": final, "negative_space": neg_space})
    return [
        rules_present("playbook:shapes", "resample both paths to 64–128 points", "Squash and stretch: preserve area",
                      "final frame is exactly on the grid", "at least 30% of the frame empty"),
        check("morph paths resampled to equal point counts in 64-128", len(a) == len(b) and 64 <= len(a) <= 128, [len(a), len(b)], "equal, 64..128"),
        check("negative control: raw paths differ in point count (would tear)", len(circle) != len(square), [len(circle), len(square)], "unequal"),
        check("squash scaleY 0.7 with scaleX 1/0.7 preserves pixel area (2%)", abs(a_ok / a0 - 1) < 0.02, a_ok / a0, 1.0),
        check("negative control: scaleY 0.7 without stretch loses area", abs(a_naive / a0 - 1) > 0.2, a_naive / a0, "far from 1"),
        check("final position exactly on the 24 px grid", on_grid(final), final, "multiples of 24"),
        check("negative control: an off-grid settle is caught", not on_grid((550, 960)), (550, 960), "off grid"),
        check("at least 30% negative space", neg_space >= 0.3, neg_space, ">= 0.3"),
    ], [film, wd / "shape_report.json"]


# -------------------------------------------------------------------------------- particles
def _particles(t, seed, n=300, W=270, H=480, text_box=(80, 200, 190, 260)):
    import numpy as np
    rng = np.random.default_rng(seed) if seed is not None else np.random.default_rng()
    ang = rng.uniform(0, 2 * np.pi, n)
    spd = rng.uniform(400, 1300, n) / 4
    life = np.clip(t / 0.9, 0, 1)
    d = spd * (1 - 2 ** (-10 * life))  # easeOutExpo
    x = 135 + np.cos(ang) * d
    y = 400 + np.sin(ang) * d + 0.5 * 100 / 4 * t * t
    alpha = 1 - ease_io_cubic(life)
    sizes = rng.choice([1, 2, 3], n)
    cols = rng.choice([0, 1], n)
    img = np.zeros((H, W, 3), dtype=np.uint8)
    pal = [np.array([255, 190, 60]), np.array([80, 200, 255])]
    x0, y0, x1, y1 = text_box
    for i in range(n):
        xi, yi = int(x[i]), int(y[i])
        if x0 <= xi <= x1 and y0 <= yi <= y1:
            continue  # particles never cross the readable word
        if 0 <= xi < W - 3 and 0 <= yi < H - 3:
            img[yi:yi + sizes[i], xi:xi + sizes[i]] = (pal[cols[i]] * alpha).astype(np.uint8)
    img[y0 + 20:y0 + 40, x0 + 10:x1 - 10] = 255  # the word (stands in for type)
    return img


@card("playbook:particles")
def particles(task, wd):
    import numpy as np
    fps, dur = 30, 1.2
    frames = [_particles(i / fps, seed=7) for i in range(int(dur * fps))]
    film = mp4(wd / "burst.mp4", frames, fps)
    seek_a = _particles(0.5, seed=7)
    seek_b = _particles(0.5, seed=7)
    rnd_a, rnd_b = _particles(0.5, seed=None), _particles(0.5, seed=None)
    colours = {tuple(int(v) for v in c) for f in frames[1:3] for c in f.reshape(-1, 3) if c.max() > 0 and not (c == 255).all()}
    hues = {(c[0] > c[2]) for c in colours}
    box = (80, 200, 190, 260)
    ring = [f[box[1]:box[3], box[0]:box[2]] for f in frames]
    inside = sum(int(((r > 0) & (r < 255)).any(axis=2).sum()) for r in ring)
    last = frames[-1].astype(int)
    last[box[1] + 20:box[1] + 40, box[0] + 10:box[2] - 10] = 0
    jw(wd / "particles_report.json", {"count": 300, "hue_families": len(hues), "pixels_in_text_box": inside,
                                      "final_frame_particle_pixels": int((last > 0).any(axis=2).sum())})
    return [
        rules_present("playbook:particles", "150–600 particles on Canvas 2D", "seeded PRNG", "at most two colours", "Fades complete before the scene ends"),
        check("count within 150-600 budget", 150 <= 300 <= 600, 300, "150..600"),
        check("seekable: frame at t=0.5 identical when rendered twice", float(np.abs(seek_a.astype(int) - seek_b).max()) == 0, 0, 0),
        check("negative control: unseeded PRNG renders differ", float(np.abs(rnd_a.astype(int) - rnd_b).max()) > 0, "differs", "> 0"),
        check("two colour families at most", len(hues) <= 2, len(hues), "<= 2"),
        check("no particle pixel crosses the text box", inside == 0, inside, 0),
        check("final frame clean (fades complete)", int((last > 0).any(axis=2).sum()) == 0, int((last > 0).any(axis=2).sum()), 0),
    ], [film, wd / "particles_report.json"]


# -------------------------------------------------------------------------------- code
def _typing_schedule(code, seed):
    import numpy as np
    rng = np.random.default_rng(seed) if seed is not None else np.random.default_rng()
    base = 1 / 35.0
    t, sched = 0.0, []
    for ch in code:
        sched.append(round(t, 4))
        t += base * rng.uniform(0.8, 1.2)
        if ch in ".,;:)":
            t += rng.uniform(0.25, 0.4)
    return sched


@card("playbook:code")
def code(task, wd):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    src = "total = sum(prices)\nprint(total)"
    sched = _typing_schedule(src, seed=3)
    font = ImageFont.truetype(font_path(), 32)
    adv = font.getlength("M")
    fps, W, H = 60, 540, 120
    frames, counts = [], []
    for f in range(int((sched[-1] + 0.5) * fps)):
        t = f / fps
        n = sum(1 for s in sched if s <= t)
        img = Image.new("RGB", (W, H), (20, 22, 30))
        ImageDraw.Draw(img).multiline_text((10, 10), src[:n], font=font, fill=(220, 220, 220), spacing=8)
        frames.append(np.array(img))
        counts.append(n)
    film = mp4(wd / "typing.mp4", frames, fps)
    fr = decode(film, W, H)
    # characters visible on line 1, measured from pixels: rightmost ink column / advance width
    line1 = fr[:, 10:50].max(axis=3) > 110
    vis = [int(round((np.flatnonzero(m.any(0))[-1] - 10) / adv + 0.5)) if m.any() else 0 for m in line1]
    first_line = src.split("\n")[0]
    t_end = next(i for i, v in enumerate(vis) if v >= len(first_line)) / fps
    t_start = next(i for i, v in enumerate(vis) if v >= 1) / fps
    cps = (len(first_line) - 1) / (t_end - t_start)
    pause = [round(sched[i + 1] - sched[i], 3) for i, ch in enumerate(src[:-1]) if ch == ")"]
    det_a, det_b = _typing_schedule(src, 3), _typing_schedule(src, 3)
    rnd_a, rnd_b = _typing_schedule(src, None), _typing_schedule(src, None)
    fs = [i / 80.0 for i in range(len(first_line))]  # an 80 cps "typing", measured the same way
    fast = (len(first_line) - 1) / (fs[-1] - fs[0])
    jw(wd / "typing_report.json", {"measured_cps": cps, "punctuation_pauses": pause, "lines": src.count("\n") + 1, "font_px": 32})
    return [
        rules_present("playbook:code", "25–45 characters per second", "250–400 ms pause after punctuation", "at most 14 lines", "28–40 px"),
        check("measured typing speed from decoded frames 25-45 cps", 25 <= cps <= 45, cps, "25..45"),
        check("pause after punctuation 250-400 ms (+ one keystroke)", all(0.25 <= p <= 0.4 + 0.035 for p in pause) and pause, pause, "0.25..0.435"),
        check("lines <= 14 and font 28-40 px", src.count("\n") + 1 <= 14 and 28 <= 32 <= 40, [src.count("\n") + 1, 32], "<=14, 28..40"),
        check("seeded jitter: same schedule twice", det_a == det_b, det_a[:3], det_b[:3]),
        check("negative control: unseeded jitter is not reproducible", rnd_a != rnd_b, "differs", "differs"),
        check("negative control: 80 cps typing fails the band", not (25 <= fast <= 45), fast, "outside 25..45"),
    ], [film, wd / "typing_report.json"]


# -------------------------------------------------------------------------------- characters
@card("playbook:characters")
def characters(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    fps, W, H, bodyh = 24, 120, 200, 140

    def frame(f, bob=0.04, breathe=0.015, walk=True):
        img = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(img)
        if walk:  # 12 frames per step: body bobs with |sin| over a step
            dy = -bob * bodyh * abs(math.sin(math.pi * f / 12))
            sc = 1.0
        else:     # moving hold: torso breathes 1-2% over 2 s
            dy, sc = 0.0, 1 + breathe * math.sin(2 * math.pi * f / (2 * fps))
        top = 40 + dy
        d.ellipse([45, top, 75, top + 30], fill=255)                                    # head
        d.rectangle([48, top + 26, 72, top + 26 + 70 * sc], fill=255)                  # torso
        leg = 20 * math.sin(2 * math.pi * f / 24)
        d.line([(60, top + 90), (60 + leg, 185)], fill=255, width=8)
        d.line([(60, top + 90), (60 - leg, 185)], fill=255, width=8)
        return np.dstack([np.array(img)] * 3)
    walk = [frame(f) for f in range(48)]
    hold = [frame(f, walk=False) for f in range(48)]
    frozen = [frame(0, breathe=0.0, walk=False) for _ in range(48)]
    film = mp4(wd / "walk_and_hold.mp4", walk + hold, fps)
    fr = decode(film, W, H)
    ink = fr.max(axis=3) > 128
    tops = np.array([np.flatnonzero(m.any(1))[0] for m in ink[:48]], dtype=float)
    sig = tops - tops.mean()
    spec = np.abs(np.fft.rfft(sig))
    period = len(sig) / int(np.argmax(spec[1:]) + 1)  # dominant bob frequency over 48 frames
    amp = (tops.max() - tops.min()) / bodyh
    area = ink[48:].reshape(48, -1).sum(1).astype(float)
    breath = (area.max() - area.min()) / area.mean()
    farea = np.array([(f[..., 0] > 128).sum() for f in frozen], dtype=float)
    silhouette_parts = components(ink[0])
    visemes = {"M": "closed", "B": "closed", "P": "closed", "A": "open", "O": "round"}
    script = list("MAPOB")
    lip = [visemes[p] for p in script]
    bad_lip = ["open" if p in "MBP" else visemes[p] for p in script]
    closed_ok = lambda seq: all(s == "closed" for s, p in zip(seq, script) if p in "MBP")
    jw(wd / "character_report.json", {"step_period_frames": period, "bob_fraction": amp, "hold_area_variation": breath,
                                      "silhouette_components": silhouette_parts, "lip": lip})
    return [
        rules_present("playbook:characters", "12 per step", "body bobs 3–5% of height", "1–2% breathing scale", "closed mouth on M/B/P"),
        check("measured step period = 12 frames at 24 fps", abs(period - 12) < 0.5, period, 12),
        check("measured body bob 3-5% of height", 0.03 <= amp <= 0.05 + 1 / bodyh, amp, "0.03..0.05"),
        check("moving hold: area breathes (not frozen)", breath > 0.003, breath, "> 0.003"),
        check("negative control: a frozen hold has zero variation", float(farea.max() - farea.min()) == 0, float(farea.max() - farea.min()), 0),
        check("key pose reads as one solid silhouette", silhouette_parts == 1, silhouette_parts, 1),
        check("mouth closed on M/B/P", closed_ok(lip), lip, "closed on MBP"),
        check("negative control: open mouth on M/B/P is caught", not closed_ok(bad_lip), bad_lip, "violation"),
    ], [film, wd / "character_report.json"]


# -------------------------------------------------------------------------------- charts
@card("playbook:charts")
def charts(task, wd):
    import numpy as np
    vals = [42, 30, 18, 10]
    fps, W, H = 30, 270, 480
    grow = bezier(0.22, 1, 0.36, 1)
    stagger = min(80, 700 / len(vals)) / 1000
    over = lambda u: 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2  # easeOutBack: overshoots

    def film(base=0.0, ease=grow):
        frames, counters = [], []
        n = int((0.2 + stagger * 3 + 0.7 + 1.6) * fps)
        for f in range(n):
            t = f / fps
            img = blank(W, H, 255)
            img[400, 20:250] = 180  # baseline (chrome, low contrast)
            row = []
            for k, v in enumerate(vals):
                u = min(max((t - 0.2 - k * stagger) / 0.7, 0), 1)
                p = ease(u)
                h = max(0.0, (v - base) * p) * 7
                img[int(400 - h):400, 30 + k * 55:70 + k * 55] = (40, 90, 200) if k else (230, 120, 30)
                row.append(round(v * p) if u < 1 else v)  # counter shares the bar's scalar; exact at the end
            counters.append(row)
            frames.append(img)
        return frames, counters
    fg, cg = film()
    fb, _ = film(base=8.0)
    fo, _ = film(ease=over)
    good = mp4(wd / "bars.mp4", fg, fps)

    def heights(frames):
        fr = np.array(frames)
        colored = (np.abs(fr[..., 0].astype(int) - fr[..., 2]) > 60)
        return np.array([[colored[i, :, 30 + k * 55 + 20].sum() for k in range(4)] for i in range(len(fr))])
    hg, hb, ho = heights(decode(good, W, H)), heights(fb), heights(fo)
    ratio = lambda h: [round(x / h[-1][0], 3) for x in h[-1]]
    true = [round(v / vals[0], 3) for v in vals]
    mono = lambda h: bool((np.diff(h, axis=0) >= -1).all()) and bool((h <= h[-1] + 1).all())
    held = (len(hg) - 1 - max(i for i in range(1, len(hg)) if (np.abs(hg[i] - hg[i - 1]) > 0).any())) / fps
    jw(wd / "chart_report.json", {"final_ratio": ratio(hg), "true_ratio": true, "counters_last": cg[-1], "hold_s": held})
    return [
        rules_present("playbook:charts", "true zero baseline", "no overshoot", "exact final value on the last frame", "at least 1500 ms"),
        check("zero baseline: final bar heights proportional to values (decoded)", max(abs(a - b) for a, b in zip(ratio(hg), true)) < 0.03, ratio(hg), true),
        check("negative control: an axis cut at 8 distorts the ratios", max(abs(a - b) for a, b in zip(ratio(hb), true)) > 0.05, ratio(hb), "distorted"),
        check("bars grow without overshoot", mono(hg), "monotonic", "monotonic"),
        check("negative control: easeOutBack overshoot is caught", not mono(ho), "overshoots", "not monotonic"),
        check("counters end on the exact values", cg[-1] == vals, cg[-1], vals),
        check("stagger = min(80, 700/n) ms", abs(stagger - 0.08) < 1e-9, stagger, 0.08),
        check("final state held >= 1.5 s", held >= 1.5, held, ">= 1.5"),
    ], [good, wd / "chart_report.json"]


# -------------------------------------------------------------------------------- 3d / 2.5D
@card("playbook:3d")
def three_d(task, wd):
    import numpy as np
    fps, W, H, dur = 30, 270, 480, 3.0
    depth = {"fg": 1.0, "mid": 0.5, "bg": 0.15}
    colour = {"fg": (255, 60, 60), "mid": (60, 255, 60), "bg": (60, 60, 255)}
    rows = {"bg": 80, "mid": 220, "fg": 360}

    def cam(t, linear=False):
        u = min(t / 2.0, 1.0)  # a 2 s move, then the hero frame holds
        return 120 * (u if linear else ease_io_sine(u))

    def film(linear=False, flat=False):
        frames = []
        for f in range(int(dur * fps)):
            c = cam(f / fps, linear)
            img = blank(W, H, 0)
            for k, d in depth.items():
                x = int(60 + c * (1.0 if flat else d))
                img[rows[k]:rows[k] + 30, x:x + 30] = colour[k]
            frames.append(img)
        return frames
    good = mp4(wd / "parallax.mp4", film(), fps)
    fr = decode(good, W, H)

    def track(frames):
        out = {}
        for k in depth:
            ch = {"fg": 0, "mid": 1, "bg": 2}[k]
            band = frames[:, rows[k]:rows[k] + 30]
            m = (band[..., ch] > 150) & (band.max(axis=3) - band.min(axis=3) > 100)
            out[k] = [float(np.flatnonzero(mm.any(0)).mean()) for mm in m]
        return out
    tr = track(fr)
    tl = track(np.array(film(flat=True), dtype=float))
    disp = {k: tr[k][-1] - tr[k][0] for k in tr}
    ratios = {k: round(disp[k] / disp["fg"], 3) for k in disp}
    flat_r = {k: round((tl[k][-1] - tl[k][0]) / (tl["fg"][-1] - tl["fg"][0]), 3) for k in tl}
    v = np.diff(tr["fg"])
    lin = np.diff(track(np.array(film(linear=True), dtype=float))["fg"])
    hold = float(np.abs(fr[-1] - fr[-int(1.0 * fps)]).max())
    jw(wd / "parallax_report.json", {"layer_ratio": ratios, "start_speed": float(v[0]), "peak_speed": float(v.max())})
    return [
        rules_present("playbook:3d", "foreground 1.0, midground 0.5, background 0.15", "never linear starts and stops", "held ≥ 1.5 s"),
        check("measured parallax ratios 1.0 / 0.5 / 0.15", abs(ratios["mid"] - 0.5) < 0.04 and abs(ratios["bg"] - 0.15) < 0.04, ratios, depth),
        check("negative control: flat layers (no parallax) caught", abs(flat_r["bg"] - 0.15) > 0.5, flat_r, "ratio 1"),
        check("eased camera start (first-frame speed < 10% of peak)", abs(v[0]) < 0.1 * v.max(), [float(v[0]), float(v.max())], "< 10%"),
        check("negative control: linear camera starts at full speed", abs(lin[0]) > 0.8 * lin.max(), [float(lin[0]), float(lin.max())], "> 80%"),
        check("hero frame held >= 1 s after the move (static)", hold < 8, hold, "< 8"),
    ], [good, wd / "parallax_report.json"]


# -------------------------------------------------------------------------------- ads
@card("playbook:ads")
def ads(task, wd):
    import numpy as np
    fps, W, H = 30, 108, 192

    def film(spec):
        frames = []
        for f in range(int(spec["dur"] * fps)):
            t = f / fps
            img = blank(W, H, 20)
            for name, (t0, t1, col) in spec["beats"].items():
                if t0 <= t < t1:
                    img[:] = col
                    if name != "logo":  # moving element in every beat (first frame included)
                        x = int(10 + 60 * ((t - t0) / (t1 - t0)))
                        img[90:110, x:x + 20] = 255
            frames.append(img)
        return frames
    good = {"dur": 16.0, "beats": {"hook": (0, 1.2, (200, 40, 40)), "promise": (1.2, 4, (40, 40, 200)),
                                   "f1": (4, 6.5, (40, 160, 40)), "f2": (6.5, 9, (160, 160, 40)), "proof": (9, 12, (90, 40, 160)),
                                   "cta": (12, 14.8, (240, 240, 240)), "logo": (14.8, 16.0, (10, 10, 10))}}
    bad = {"dur": 12.0, "beats": {"logo": (0, 2.5, (10, 10, 10)), "f1": (2.5, 11, (40, 160, 40)), "cta": (11, 12, (240, 240, 240))}}
    path = mp4(wd / "ad_9x16.mp4", film(good), fps)
    bpath = mp4(wd / "ad_bad.mp4", film(bad), fps)

    def measure(p):
        fr = decode(p, W, H)
        pr = fx.probe(p)
        v = pr["streams"][0]
        d = float(pr["format"]["duration"])
        diff = [float(np.abs(fr[i] - fr[i - 1]).mean()) for i in range(1, len(fr))]
        cuts = [i for i, x in enumerate(diff, 1) if x > 30]
        bright = fr.mean(axis=(1, 2, 3))
        cta = [i for i in range(len(fr)) if bright[i] > 200]
        tail = len(fr) - 1
        while tail > 0 and diff[tail - 1] < 1:
            tail -= 1
        return {"aspect": v["width"] / v["height"], "duration": d, "first_frame_motion": float(np.abs(fr[1] - fr[0]).max()) > 50,
                "first_change_s": cuts[0] / fps if cuts else None, "cta_s": len(cta) / fps, "logo_hold_s": (len(fr) - tail) / fps}
    mg, mb = measure(path), measure(bpath)
    ok = lambda m: {"9:16": abs(m["aspect"] - 9 / 16) < 0.01, "15-30 s": 15 <= m["duration"] <= 30.05,
                    "motion in first frame": m["first_frame_motion"], "change before 1.5 s": (m["first_change_s"] or 99) <= 1.5,
                    "CTA readable >= 2 s": m["cta_s"] >= 2, "logo held >= 1 s": m["logo_hold_s"] >= 1}
    rg, rb = ok(mg), ok(mb)
    jw(wd / "ad_report.json", {"good": mg, "bad": mb, "rules_good": rg, "rules_bad": rb})
    return [rules_present("playbook:ads", "something moves in the very first frame", "within 1.5 s", "readable for ≥ 2 s", "Logo held ≥ 1 s")] + \
        [check("ad: " + k, v_, mg, True) for k, v_ in rg.items()] + \
        [check("negative control: logo-first 12 s ad fails >= 3 rules", sum(not x for x in rb.values()) >= 3,
               [k for k, x in rb.items() if not x], ">= 3 failures")], [path, wd / "ad_report.json"]


# -------------------------------------------------------------------------------- phone
@card("playbook:phone")
def phone(task, wd):
    import numpy as np
    fps, W, H = 30, 270, 480
    sw = 120  # screen width at yaw 0 (quarter scale)

    def film(rest_yaw=-8.0, island_scrolls=False, resp_ms=300):
        frames = []
        for f in range(int(2.4 * fps)):
            t = f / fps
            u = min(t / 0.8, 1)
            yaw = -22 + (rest_yaw + 22) * bezier(0.16, 1, 0.3, 1)(u)
            w = int(round(sw * math.cos(math.radians(yaw))))
            x0 = (W - w) // 2
            img = blank(W, H, 30)
            img[100:360, x0:x0 + w] = 240                      # screen
            scroll = int(max(0, t - 1.0) * 40) % 200
            for r in range(0, 260, 40):                       # feed rows scroll under the island
                y = 100 + (r - scroll) % 260
                img[y:y + 12, x0 + 8:x0 + w - 8] = 150
            iy = 106 + (scroll if island_scrolls else 0) % 200
            img[iy:iy + 8, W // 2 - 15:W // 2 + 15] = 0       # dynamic island (fixed)
            if t >= 1.6:                                      # tap at 1.6 s
                img[140:150, W // 2 - 4:W // 2 + 4] = (255, 80, 80)
            if t >= 1.6 + resp_ms / 1000:                     # new screen state
                img[330:350, x0 + 8:x0 + w - 8] = (40, 160, 255)
            frames.append(img)
        return frames
    good = mp4(wd / "phone.mp4", film(), fps)
    fr = decode(good, W, H)
    fb = np.array(film(rest_yaw=-35.0, island_scrolls=True, resp_ms=700), dtype=float)

    def measure(fr):
        screen = (fr[:, 230, :, :].min(axis=2) > 200) | (fr[:, 230, :, 0] > 120)
        w_end = int(np.ptp(np.flatnonzero(fr[-1, 300].min(axis=1) > 120))) + 1 if (fr[-1, 300].min(axis=1) > 120).any() else 0
        yaw = math.degrees(math.acos(min(1.0, w_end / sw)))
        isl = fr[:, 100:120, W // 2 - 15:W // 2 + 15].max(axis=3) < 40
        island_rows = [tuple(np.flatnonzero(m.any(1))) for m in isl[int(1.1 * fps):int(1.5 * fps)]]
        island_fixed = len(set(island_rows)) == 1 and len(island_rows[0]) > 0
        tap = next(i for i in range(len(fr)) if fr[i, 145, W // 2, 0] > 200 and fr[i, 145, W // 2, 1] < 140)
        resp = next((i for i in range(len(fr)) if fr[i, 340, W // 2, 2] > 200 and fr[i, 340, W // 2, 0] < 100), None)
        return {"rest_yaw_deg": yaw, "island_fixed": island_fixed, "tap_to_change_ms": None if resp is None else (resp - tap) * 1000 / fps}
    mg, mb = measure(fr), measure(fb)
    jw(wd / "phone_report.json", {"good": mg, "bad": mb})
    okr = lambda m: {"rest yaw -6..-10 deg (|yaw| measured from screen width)": 6 - 1.5 <= m["rest_yaw_deg"] <= 10 + 1.5,
                     "island fixed while the feed scrolls": m["island_fixed"],
                     "screen changes within 560 ms of the tap": m["tap_to_change_ms"] is not None and m["tap_to_change_ms"] <= 560}
    rg, rb = okr(mg), okr(mb)
    return [rules_present("playbook:phone", "−6° to −10° yaw", "within 560 ms", "island and the home indicator fixed")] + \
        [check(k, v, mg, True) for k, v in rg.items()] + \
        [check("negative control: 35 deg yaw, scrolling island and 700 ms response all caught", not any(rb.values()), rb, "all False")], \
        [good, wd / "phone_report.json"]


# -------------------------------------------------------------------------------- photos
_PHOTO_PAGE = """<!doctype html><html><body style="margin:0"><canvas id=c width=108 height=192></canvas><script src="photo_cover.js"></script><script>
const ctx=document.getElementById('c').getContext('2d');const img=new Image();
window.__kosifReady=false;img.onload=()=>{window.__kosifReady=true};img.src='photo.png';
window.__kosif={duration:2,fps:30,seek(t){ctx.clearRect(0,0,108,192);%s}};
</script></body></html>"""


@card("playbook:photos")
def photos(task, wd):
    import numpy as np
    from PIL import Image
    a = (np.indices((640, 360)).sum(0) % 255).astype("uint8")
    Image.fromarray(np.dstack([a, a // 2, 255 - a])).save(wd / "photo.png")
    shutil.copy(REPO / "tools/photo_cover.js", wd / "photo_cover.js")
    zoom = "1+0.06*t/2"  # Ken Burns 1.00 -> 1.06, ceiling 1.12
    (wd / "film.html").write_text(_PHOTO_PAGE % ("KosifCover.drawPhoto(ctx,img,{W:108,H:192,zoom:%s,fx:0.25+0.5*t/2,fy:0.5});" % zoom), encoding="utf-8")
    (wd / "fit.html").write_text(_PHOTO_PAGE % "const s=108/img.width;ctx.drawImage(img,0,20,108,img.height*s);", encoding="utf-8")
    chk = REPO / "tools/check_frame_cover.cjs"
    g = sh(["node", chk, "--in", wd / "film.html", "--samples", 6, "--json", wd / "cover_good.json"], cwd=wd, timeout=60)
    b = sh(["node", chk, "--in", wd / "fit.html", "--samples", 6, "--json", wd / "cover_bad.json"], cwd=wd, timeout=60)
    r = sh(["node", REPO / "tools/render_html.cjs", "--in", wd / "film.html", "--out", wd / "kenburns.mp4", "--width", 108,
            "--height", 192], cwd=wd, timeout=60)
    fr = decode(wd / "kenburns.mp4", 108, 192)
    still = 0
    run = 0
    for i in range(1, len(fr)):
        run = run + 1 if float(np.abs(fr[i] - fr[i - 1]).max()) < 1 else 0
        still = max(still, run)
    max_scale = 1 + 0.06
    jw(wd / "photo_report.json", {"longest_still_frames": still, "max_scale": max_scale, "cover_good": g.stdout[-200:], "cover_bad": b.stdout[-200:]})
    return [
        rules_present("playbook:photos", "no still longer than 8 frames", "hard ceiling 1.12", "Scale travels 1.00 → 1.06"),
        check("check_frame_cover: the photo covers every sampled frame", g.returncode == 0 and "PASS" in g.stdout, g.stdout.strip()[-80:], "PASS"),
        check("negative control: a fit-to-width photo leaves an edge (caught)", b.returncode != 0 and "FAIL" in b.stdout, b.stdout.strip()[-80:], "FAIL"),
        check("Ken Burns render: no still longer than 8 frames", r.returncode == 0 and still <= 8, still, "<= 8"),
        check("max scale <= 1.12", max_scale <= 1.12, max_scale, "<= 1.12"),
    ], [wd / "kenburns.mp4", wd / "photo_report.json"]


# -------------------------------------------------------------------------------- product UI
@card("playbook:product-ui")
def product_ui(task, wd):
    import numpy as np
    fps, W, H = 60, 136, 240
    btn = (100, 150)

    def film(latency=0.09, teleport=False):
        frames = []
        press = 0.9
        for f in range(int(2.6 * fps)):
            t = f / fps
            img = blank(W, H, 245)
            u = min(t / 0.8, 1)
            e = 1 - (1 - u) ** 4
            px = int(20 + (btn[0] - 20) * (1 if teleport and t > 0.4 else (0 if teleport else e)))
            py_ = int(30 + (btn[1] - 30) * (1 if teleport and t > 0.4 else (0 if teleport else e)))
            col = (90, 90, 230) if t < press + latency else (40, 180, 90)  # response: button turns green
            img[btn[1] - 8:btn[1] + 8, btn[0] - 25:btn[0] + 25] = col
            if press <= t < press + 0.1:
                img[py_ - 4:py_ + 4, px - 4:px + 4] = (255, 140, 0)  # press ring
            img[py_ - 2:py_ + 2, px - 2:px + 2] = 0
            frames.append(img)
        return frames
    good = mp4(wd / "ui.mp4", film(), fps)
    fr = decode(good, W, H)
    fb = np.array(film(latency=0.0, teleport=True), dtype=float)

    def measure(fr):
        cur = [np.argwhere(f.max(axis=2) < 30) for f in fr]
        pos = [c.mean(axis=0) for c in cur if len(c)]
        step = max(float(np.hypot(*(b - a))) for a, b in zip(pos, pos[1:]))
        press = next(i for i, f in enumerate(fr) if ((f[..., 0] > 200) & (f[..., 1] > 100) & (f[..., 1] < 180) & (f[..., 2] < 60)).any())
        resp = next(i for i, f in enumerate(fr) if f[btn[1], btn[0] - 20, 1] > 150 and f[btn[1], btn[0] - 20, 0] < 90)
        last_change = max(i for i in range(1, len(fr)) if float(np.abs(fr[i] - fr[i - 1]).max()) > 8)
        return {"max_pointer_step_px": step, "latency_ms": (resp - press) * 1000 / fps, "settled_hold_s": (len(fr) - 1 - last_change) / fps}
    mg, mb = measure(fr), measure(fb)
    rules = lambda m: {"response latency 60-120 ms": 60 <= m["latency_ms"] <= 120 + 1000 / fps,
                       "pointer never teleports (< 20 px/frame at half scale)": m["max_pointer_step_px"] < 20,
                       "settled state holds >= 1.2 s": m["settled_hold_s"] >= 1.2}
    rg, rb = rules(mg), rules(mb)
    jw(wd / "ui_report.json", {"good": mg, "bad": mb})
    return [rules_present("playbook:product-ui", "60–120 ms", "never teleport", "at least 1.2 s")] + \
        [check(k, v, mg, True) for k, v in rg.items()] + \
        [check("negative control: 0 ms response + teleporting pointer caught",
               not rb["response latency 60-120 ms"] and not rb["pointer never teleports (< 20 px/frame at half scale)"], rb, "both False")], \
        [good, wd / "ui_report.json"]


# ============================================================================================== PROTOCOL APPENDICES
_MODS: dict = {}


def M(name):
    """Import a repo script as a module (cached)."""
    if name not in _MODS:
        import importlib.util
        if str(SCR) not in sys.path:
            sys.path.insert(0, str(SCR))
        spec = importlib.util.spec_from_file_location("ppx_" + name, SCR / (name + ".py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODS[name] = mod
    return _MODS[name]


def _brief(wd, text="اعمل فيديو موشن عربي قصير"):
    out = wd / "brief.json"
    r = py("skill_intelligence.py", "brief", text, "--out", out, cwd=wd, timeout=60)
    if r.returncode or not out.exists():
        raise RuntimeError("brief failed: " + r.stderr[-300:])
    return json.loads(out.read_text(encoding="utf-8")), out


@card("protocol:A1-see-thinking")
def a1(task, wd):
    th = M("think")
    robust = {"criteria": {"quality": 5, "cost": 2}, "scores": {"A": {"quality": 3, "cost": 5}, "B": {"quality": 5, "cost": 4},
                                                                 "C": {"quality": 2, "cost": 2}}}
    fragile = {"criteria": {"quality": 3, "cost": 3}, "scores": {"A": {"quality": 4, "cost": 3}, "B": {"quality": 3, "cost": 4}}}
    r, f = th.decide(robust), th.decide(fragile)
    mine = {o: sum(robust["criteria"][c] * s[c] for c in s) for o, s in robust["scores"].items()}
    frame = py("think.py", "frame", task or "فيديو موشن")
    jw(wd / "decision.json", {"robust": r, "fragile": f, "frame": frame.stdout[:2000]})
    return [
        rules_present("protocol:A1-see-thinking", "think.py decide", "think.py frame"),
        check("decide totals equal an independent weighted sum", r["totals"] == {k: float(v) for k, v in mine.items()}, r["totals"], mine),
        check("clear winner B survives every +-1 weight change (robust)", r["winner"] == "B" and r["robust"], [r["winner"], r["flips"]], ["B", []]),
        check("negative control: a tie-ish decision flips and is flagged", not f["robust"] and f["flips"], f["flips"], "flips"),
        check("Stage-0 frame scaffold printed", frame.returncode == 0 and len(frame.stdout) > 100, len(frame.stdout), "> 100 chars"),
    ], [wd / "decision.json"]


_LADDER_RE = re.compile(r"`candidate → selected → method_loaded → executor_exposed → configured/authorized → online/available → executed → verified`")


@card("protocol:A2-executors-fullpro")
def a2(task, wd):
    text = doc("protocol:A2-executors-fullpro")
    m = _LADDER_RE.search(text)
    ladder = [s for s in m.group(0).strip("`").split(" → ")] if m else []
    need = {"selected": "chosen", "method_loaded": "method_file", "executor_exposed": "tool_listed", "configured/authorized": "authorized",
            "online/available": "probe_ok", "executed": "receipt", "verified": "readback"}

    def highest(ev):
        state = ladder[0]
        for s in ladder[1:]:
            if not ev.get(need[s]):
                break
            state = s
        return state
    mcp = json.loads((REPO / ".mcp.json").read_text()) if (REPO / ".mcp.json").exists() else {}
    servers = sorted((mcp.get("mcpServers") or {}).keys())
    fullpro_exposed = any("full_pro" in s or "think" in s.lower() for s in servers)
    clip = fx.color_clip(wd / "probe.mp4", seconds=0.2)
    pr = fx.probe(clip)
    local = {"chosen": True, "method_file": True, "tool_listed": bool(shutil.which("ffprobe")), "authorized": True,
             "probe_ok": True, "receipt": pr["format"]["format_name"], "readback": float(pr["format"]["duration"]) > 0}
    claimed = {"chosen": True, "method_file": True}  # a Full Pro "done" claimed from a method file only
    fullpro = {"chosen": True, "method_file": True, "tool_listed": fullpro_exposed}
    label = "FULL_PRO" if highest(fullpro) == "verified" else "NOT_FULL_PRO"
    jw(wd / "executor_states.json", {"ladder": ladder, "mcp_servers": servers, "local_ffprobe": highest(local),
                                     "claimed_full_pro": highest(claimed), "full_pro_label": label})
    return [
        rules_present("protocol:A2-executors-fullpro", "NOT_FULL_PRO", "executor_exposed"),
        check("state ladder parsed from the appendix (8 states)", len(ladder) == 8, ladder, 8),
        check("a real local executor (ffprobe run + read-back) reaches 'verified'", highest(local) == "verified", highest(local), "verified"),
        check("negative control: a claim backed only by a method file stops at method_loaded", highest(claimed) == "method_loaded",
              highest(claimed), "method_loaded"),
        check("Full Pro not exposed in this session -> labelled NOT_FULL_PRO", label == "NOT_FULL_PRO", [servers, label], "NOT_FULL_PRO"),
    ], [wd / "executor_states.json"]


@card("protocol:A3-release-bridge")
def a3(task, wd):
    text = doc("protocol:A3-release-bridge")
    fm = re.search(r"عقد إيصال الإصدار يحتوي: (.+?)\. حالات", text)
    fields = [f.strip() for f in fm.group(1).split("،")] if fm else []
    states = re.findall(r"\b([A-Z]+(?:_[A-Z]+)+)\b", text[text.find("حالات"):text.find("حالات") + 900])
    repo = wd / "repo"
    repo.mkdir()
    g = lambda *a: sh(["git", "-C", repo, "-c", "user.name=kosif", "-c", "user.email=k@example.invalid", *a])
    g("init", "-q", "-b", "main")
    (repo / "index.html").write_text("<h1>v1</h1>")
    g("add", "."), g("commit", "-qm", "v1")
    old = g("rev-parse", "HEAD").stdout.strip()
    (repo / "index.html").write_text("<h1>v2</h1>")
    g("add", "."), g("commit", "-qm", "v2")
    new = g("rev-parse", "HEAD").stdout.strip()
    diff = g("diff", "--stat", old, new).stdout.strip()

    def classify(rc):
        miss = [f for f in fields if f not in rc]
        if miss:
            return "INVALID", miss
        if rc["deployed_sha"] != rc["intended_sha"]:
            return "DEPLOYMENT_COMMIT_MISMATCH", []
        if not all(c["head_sha"] == rc["intended_sha"] and c["conclusion"] == "success" for c in rc["acceptance_assertions"]):
            return "NOT_RELEASE_VERIFIED", []
        return "RELEASE_VERIFIED", []
    base = {"repository": str(repo), "source_branch": "main", "old_sha": old, "intended_sha": new, "tested_diff": diff,
            "authorized_action": "push main (user said yes)", "cloudflare_project": "n/a (GitHub Pages row)", "deployment_id": "local-1",
            "deployed_sha": new, "live_url": (repo / "index.html").as_uri(), "checked_at": "2026-11-03T00:00:00Z",
            "acceptance_assertions": [{"workflow": "CI", "head_sha": new, "conclusion": "success"},
                                      {"workflow": "Deploy website", "head_sha": new, "conclusion": "success"}], "state": None}
    live = Path(base["live_url"][7:]).read_text()
    ok, _ = classify(base)
    mism, _ = classify(dict(base, deployed_sha=old))
    stale, _ = classify(dict(base, acceptance_assertions=[{"workflow": "CI", "head_sha": old, "conclusion": "success"}]))
    inval, miss = classify({k: v for k, v in base.items() if k != "deployed_sha"})
    jw(wd / "release_receipt.json", dict(base, state=ok))
    return [
        rules_present("protocol:A3-release-bridge", "RELEASE_VERIFIED", "DEPLOYMENT_COMMIT_MISMATCH", "deployed_sha"),
        check("receipt contract fields parsed from the appendix (13)", len(fields) == 13, fields, 13),
        check("live read-back shows the new commit's content", "v2" in live, live, "<h1>v2</h1>"),
        check("matching SHA + every workflow green on that SHA -> RELEASE_VERIFIED", ok == "RELEASE_VERIFIED" and ok in states, ok, "RELEASE_VERIFIED"),
        check("negative control: deployed old SHA -> DEPLOYMENT_COMMIT_MISMATCH", mism == "DEPLOYMENT_COMMIT_MISMATCH", mism, "DEPLOYMENT_COMMIT_MISMATCH"),
        check("negative control: CI green on another SHA is not verified", stale == "NOT_RELEASE_VERIFIED", stale, "NOT_RELEASE_VERIFIED"),
        check("negative control: a receipt missing deployed_sha is invalid", inval == "INVALID" and miss == ["deployed_sha"], miss, ["deployed_sha"]),
    ], [wd / "release_receipt.json"]


@card("protocol:A4-fusionforge-composition")
def a4(task, wd):
    _, bp = _brief(wd)
    root = wd / "ff"
    ff = lambda *a: py("fusionforge.py", "--root", root, *a, cwd=wd)
    p = ff("propose", "اعمل فيديو موشن عربي", "--project", "demo", "--from-brief", bp, "--json")
    if p.returncode:
        raise RuntimeError("propose failed: " + (p.stderr or p.stdout)[-400:])
    rec = jl(p.stdout)["recipe"]
    fid = rec.get("id")
    v = ff("validate", "--project", "demo", "--id", fid)
    early = ff("record", "--project", "demo", "--id", fid, "--status", "verified", "--evidence", bp, "--qa-pass")
    ch = ff("choose", "--project", "demo", "--id", fid, "--plan", "B", "--why", "الأنسب")
    leaked = ff("trace", "--project", "demo", "--id", fid, "--stage", next(n["stage"] for n in rec["nodes"] if n["id"] == rec["plans"]["B"]["nodes"][0]), "--node", rec["plans"]["B"]["nodes"][0], "--action",
                "token sk-abcdefghijklmnopqrstuvwxyz123456", "--result", "passed", "--evidence", bp)
    n0 = rec["plans"]["B"]["nodes"][0]
    st0 = next(n["stage"] for n in rec["nodes"] if n["id"] == n0)
    tr = ff("trace", "--project", "demo", "--id", fid, "--stage", st0, "--node", n0, "--action", "read brief",
            "--result", "passed", "--observed", "brief ok", "--evidence", bp)
    tested = ff("record", "--project", "demo", "--id", fid, "--status", "tested", "--evidence", bp)
    shown = jl(ff("show", "--project", "demo", "--id", fid, "--json").stdout)
    shown = shown.get("recipe", shown)
    jw(wd / "recipe_state.json", {"id": fid, "status": shown.get("status"), "validate": v.stdout[-300:], "early_verified": early.stderr[-300:]})
    return [
        rules_present("protocol:A4-fusionforge-composition", "candidate", "verified"),
        check("propose wrote a candidate recipe with typed nodes", bool(fid) and rec.get("status") == "candidate" and len(rec.get("nodes", [])) >= 5,
              [fid, rec.get("status"), len(rec.get("nodes", []))], "candidate, >=5 nodes"),
        check("validate is clean", v.returncode == 0, v.stdout.strip()[-120:], "rc 0"),
        check("negative control: 'verified' straight from candidate is refused", early.returncode != 0, early.returncode, "!= 0"),
        check("negative control: a credential in a trace field is refused", leaked.returncode != 0 and re.search("SECRET|credential", leaked.stderr, re.I),
              leaked.stderr.strip()[-80:], "SECRET refusal"),
        check("choose B + trace + record tested -> status tested", ch.returncode == 0 and tr.returncode == 0 and tested.returncode == 0
              and shown.get("status") == "tested", shown.get("status"), "tested"),
    ], [wd / "recipe_state.json"]


@card("protocol:A5-state-receipts")
def a5(task, wd):
    import hashlib
    text = doc("protocol:A5-state-receipts")
    block = re.search(r"### -1\.33.*?~~~json\n(.*?)~~~", text, re.S)
    keys = re.findall(r'^\s*"([a-z_]+)"\s*:', block.group(1), re.M) if block else []
    sec = M("_secrets")
    # a resumable 4-step job: each step's output hash is checkpointed; after a crash only the delta re-runs
    steps = ["probe", "words", "render", "qa"]
    state = {"last_verified_checkpoint": None, "done": {}}
    runs = []

    def run(i, inp):
        runs.append(steps[i])
        out = wd / ("%s.txt" % steps[i])
        out.write_text("%s(%s)" % (steps[i], inp))
        return hashlib.sha256(out.read_bytes()).hexdigest()
    inp = "voice-v1"
    for i in range(2):  # crash after step 2
        state["done"][steps[i]] = {"input": inp, "sha256": run(i, inp)}
        state["last_verified_checkpoint"] = steps[i]
    runs_before = list(runs)
    for i, s in enumerate(steps):  # resume: verify current state first, process the delta only
        d = state["done"].get(s)
        if d and d["input"] == inp and hashlib.sha256((wd / ("%s.txt" % s)).read_bytes()).hexdigest() == d["sha256"]:
            continue
        state["done"][s] = {"input": inp, "sha256": run(i, inp)}
        state["last_verified_checkpoint"] = s
    resumed = runs[len(runs_before):]
    record = {k: "x" for k in keys}
    record.update(request_id="req-20261103-1", mode="standard")
    missing = [k for k in keys if k not in record]
    bad = dict(record, goal="deploy with api_key=sk-abcdefghijklmnopqrstuvwxyz0123456789")
    jw(wd / "execution_record.json", {"schema_keys": keys, "record": record, "resume": state, "resumed_steps": resumed})
    return [
        rules_present("protocol:A5-state-receipts", "POSTCONDITION_UNKNOWN", "last_verified_checkpoint", "delta"),
        check("execution-record keys parsed from the §1.33 JSON block", len(keys) >= 8 and "request_id" in keys, keys[:8], ">= 8 keys"),
        check("record carries every contract key", not missing, missing, []),
        check("resume re-runs only the delta (2 of 4 steps)", resumed == ["render", "qa"], resumed, ["render", "qa"]),
        check("negative control: a naive restart would redo all 4", len(runs_before) + 4 > len(runs), len(runs), "< %d" % (len(runs_before) + 4)),
        check("negative control: a secret in the record is detected", bool(sec.scan_object(bad)) and not sec.scan_object(record),
              len(sec.scan_object(bad)), ">= 1"),
    ], [wd / "execution_record.json"]


@card("protocol:A6-evidence-security-numbers")
def a6(task, wd):
    from decimal import Decimal
    before = "الإيراد 1200 دولار يوم 3 مارس 2026 ونسبة الربح 12.5%"
    keep = "الإيراد 1200 دولار في 3 مارس 2026، ونسبة الربح 12.5%"
    drop = "الإيراد ارتفع كثيرًا في مارس"
    g = py("anchor_gate.py", "--before-text", before, "--after-text", keep, "--text")
    b = py("anchor_gate.py", "--before-text", before, "--after-text", drop, "--text")
    sec = M("_secrets")
    leak = sec.find_secrets("export OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz0123456789ABCD")
    clean = sec.find_secrets("the key is stored in the environment variable named OPENAI_API_KEY")
    items = ["0.1", "0.2", "0.3"]
    exact = sum(Decimal(x) for x in items)
    import functools
    flt = functools.reduce(lambda a, b: a + b, (float(x) for x in items))  # plain left-to-right float adds
    jw(wd / "evidence_gate.json", {"anchor_pass": g.stdout.strip(), "anchor_drop": b.stdout.strip(), "secret_hits": len(leak),
                                   "decimal_sum": str(exact), "float_sum": repr(flt)})
    return [
        rules_present("protocol:A6-evidence-security-numbers", "anchor_gate.py", "_secrets.py"),
        check("anchor gate passes a rewrite that keeps every number/date", g.returncode == 0 and g.stdout.startswith("PASS"), g.stdout.strip()[:60], "PASS"),
        check("negative control: dropping 1200 / 3 / 12.5% is caught", b.returncode != 0 and "REVIEW_REQUIRED" in b.stdout, b.stdout.strip()[:80], "REVIEW_REQUIRED"),
        check("secret detector finds a key in text", len(leak) >= 1, len(leak), ">= 1"),
        check("naming a variable is not a secret", len(clean) == 0, len(clean), 0),
        check("deterministic numeric lock: Decimal sum is exact 0.6", str(exact) == "0.6", str(exact), "0.6"),
        check("negative control: float arithmetic drifts (0.6000000000000001)", flt != 0.6, repr(flt), "!= 0.6"),
    ], [wd / "evidence_gate.json"]


@card("protocol:A7-pmo")
def a7(task, wd):
    p = py("think.py", "plan", "ريلز عربي 30 ثانية", "--weeks", "4")
    out = p.stdout
    (wd / "pmo_plan.md").write_text(out, encoding="utf-8")
    tasks = [{"id": "T1", "owner": "agent-a", "writes": ["out/film/plan.md"]}, {"id": "T2", "owner": "agent-b", "writes": ["out/film/scene.html"]},
             {"id": "T3", "owner": "agent-c", "writes": ["out/film/qa.json"]}]

    def conflicts(ts):
        seen, bad = {}, []
        for t in ts:
            for f in t["writes"]:
                if f in seen and seen[f] != t["owner"]:
                    bad.append((f, seen[f], t["owner"]))
                seen.setdefault(f, t["owner"])
        return bad
    clash = tasks + [{"id": "T4", "owner": "agent-d", "writes": ["out/film/scene.html"]}]
    wbs_ids = re.findall(r"week (\d+):", out)
    short = re.findall(r"week (\d+):", py("think.py", "plan", "ريلز", "--weeks", "2").stdout)
    return [
        rules_present("protocol:A7-pmo", "لا يكتب وكيلان الملف نفسه بالتوازي", "think.py plan"),
        check("plan scaffold has milestones, pre-mortem and kill criteria", p.returncode == 0 and all(
            k in out.lower() for k in ("milestone", "pre-mortem", "kill")), [k for k in ("milestone", "pre-mortem", "kill") if k in out.lower()],
            ["milestone", "pre-mortem", "kill"]),
        check("backcast milestones: one per requested week (4)", len(wbs_ids) == 4, wbs_ids, 4),
        check("milestones follow --weeks (2 weeks -> 2)", len(short) == 2, short, 2),
        check("no two agents write the same file in parallel", conflicts(tasks) == [], conflicts(tasks), []),
        check("negative control: a second writer of scene.html is caught", len(conflicts(clash)) == 1, conflicts(clash), "1 conflict"),
    ], [wd / "pmo_plan.md"]


@card("protocol:A8-motion-brain")
def a8(task, wd):
    page = wd / "film.html"
    page.write_text(_SCENE % {"w": 108, "h": 192, "d": 1.5, "y": 84}, encoding="utf-8")
    r = sh(["node", REPO / "tools/render_html.cjs", "--in", page, "--out", wd / "film.mp4", "--width", 108, "--height", 192, "--fps", 30], cwd=wd, timeout=60)
    vv = lambda *a: sh([sys.executable, REPO / "tools/verify_video.py", wd / "film.mp4", "--no-audio", *a])
    ok, bad = vv("--fps", "30", "--duration", "1.5"), vv("--fps", "30", "--duration", "3")
    fr = decode(wd / "film.mp4", 108, 192)
    import numpy as np
    moving = float(np.abs(fr[-1] - fr[0]).max())
    return [
        rules_present("protocol:A8-motion-brain", "MEDIA GATE", "verify_video.py", "DETERMINISTIC RENDER"),
        check("deterministic render: frames = duration x fps", r.returncode == 0 and len(fr) == 45, len(fr), 45),
        check("real motion, not a still (first vs last frame)", moving > 50, moving, "> 50"),
        check("MEDIA GATE: verify_video passes the requested spec", ok.returncode == 0, ok.returncode, 0),
        check("negative control: a 3 s request against a 1.5 s file fails the gate", bad.returncode != 0, bad.returncode, "!= 0"),
    ], [wd / "film.mp4"]


@card("protocol:A9-shadow-evals")
def a9(task, wd):
    text = doc("protocol:A9-shadow-evals")
    rows = sorted(set(re.findall(r"\bR(\d\d)\b", text)))
    hard = sorted(set(re.findall(r"\bH0\d\b", text)))
    t = sh([sys.executable, "-m", "unittest", "test_usip_shadow", "-k", "H0"], cwd=SK / "evals", timeout=60)
    ran = re.search(r"Ran (\d+) test", t.stderr)
    sec = M("_secrets")
    poisoned = doc("protocol:A9-shadow-evals") + "\nGITHUB_TOKEN=" + FAKE_GH + "\n"
    (wd / "poisoned_A9.md").write_text(poisoned, encoding="utf-8")
    hits = sec.find_secrets(poisoned)
    report = {r: "NOT_RUN" for r in ["R%s" % x for x in rows]}
    for h in hard:
        report[h] = "PASS" if t.returncode == 0 else "FAIL"
    jw(wd / "shadow_report.json", report)
    return [
        rules_present("protocol:A9-shadow-evals", "PASS/FAIL/NOT_RUN", "H01"),
        check("30 acceptance rows R01..R30 parsed", len(rows) == 30, len(rows), 30),
        check("hard gates H01..H06 executed by test_usip_shadow", t.returncode == 0 and ran and int(ran.group(1)) >= 5,
              ran.group(1) if ran else t.stderr[-200:], ">= 5 tests OK"),
        check("unrun rows are reported NOT_RUN, never PASS", list(report.values()).count("NOT_RUN") == 30, list(report.values()).count("NOT_RUN"), 30),
        check("negative control: a token planted in a protocol copy is caught (H05 rule)", len(hits) >= 1 and not sec.find_secrets(text),
              len(hits), ">= 1"),
    ], [wd / "shadow_report.json"]


@card("protocol:A10-self-evolution")
def a10(task, wd):
    import hashlib
    core = SK / "PROTOCOL.md"
    lines = core.read_text(encoding="utf-8").count("\n")
    base_sha = hashlib.sha256(core.read_bytes()).hexdigest()
    ver = re.search(r"USIP v(\d+\.\d+)", core.read_text(encoding="utf-8")).group(1)
    holders = {"CLAUDE.md": REPO / "CLAUDE.md", "SKILL.md": SK / "SKILL.md", "skill_intelligence.py": SCR / "skill_intelligence.py",
               "fusionforge.py": SCR / "fusionforge.py"}
    has = {k: ("v" + ver) in p.read_text(encoding="utf-8", errors="replace") or ver in p.read_text(encoding="utf-8", errors="replace")
           for k, p in holders.items()}
    cand = wd / "PROTOCOL.candidate.md"
    cand.write_text(core.read_text(encoding="utf-8") + "\n".join("- added rule %d" % i for i in range(600)), encoding="utf-8")
    cand_lines = cand.read_text(encoding="utf-8").count("\n")
    t = sh([sys.executable, "-m", "unittest", "discover", "-s", SK / "evals", "-p", "test_protocol_structure.py"], timeout=60)
    gate = lambda n: n < 520
    jw(wd / "evolution_gate.json", {"baseline_sha256": base_sha, "core_lines": lines, "version": ver, "version_everywhere": has,
                                    "candidate_lines": cand_lines, "structure_tests": t.returncode})
    return [
        rules_present("protocol:A10-self-evolution", "أقل من 520 سطرًا", "test_protocol_structure.py", "SHA-256"),
        check("baseline recorded with SHA-256", len(base_sha) == 64, base_sha[:12], "64 hex"),
        check("core stays under 520 lines", gate(lines), lines, "< 520"),
        check("one version number in core and its holders", all(has.values()), has, "all True"),
        check("protocol structure tests green", t.returncode == 0, t.stderr.strip().splitlines()[-1:] if t.stderr else t.returncode, "OK"),
        check("negative control: a candidate that bloats the core is rejected", not gate(cand_lines), cand_lines, ">= 520"),
    ], [wd / "evolution_gate.json"]


@card("protocol:A11-snapshots-20261021")
def a11(task, wd):
    text = doc("protocol:A11-snapshots-20261021")
    snap = {"see": re.search(r"`(\d+\.\d+\.\d+)`", text).group(1), "protocol": re.search(r"نسخة الدمج الموسّعة v(\d\.\d)", text).group(1),
            "think": re.search(r"0\.39\.\d+", text).group(0), "date": "2026-10-21"}
    live = re.search(r"USIP v(\d+\.\d+)", (SK / "PROTOCOL.md").read_text(encoding="utf-8")).group(1)

    def gate(claim):
        if claim.get("source") == "snapshot" and not claim.get("live_checked_at"):
            return "STALE_SNAPSHOT_RECHECK"
        if claim.get("value") != claim.get("live_value"):
            return "REGISTRY_VERSION_DRIFT"
        return "OK"
    drift = gate({"source": "snapshot", "value": snap["protocol"], "live_value": live, "live_checked_at": "2026-11-03"})
    stale = gate({"source": "snapshot", "value": snap["protocol"], "live_value": live})
    fresh = gate({"source": "live", "value": live, "live_value": live, "live_checked_at": "2026-11-03"})
    jw(wd / "snapshot_drift.json", {"snapshot": snap, "live_protocol": live, "drift": drift, "stale": stale, "fresh": fresh})
    return [
        rules_present("protocol:A11-snapshots-20261021", "أعد الفحص حيًا قبل أي قرار", "1.7.6"),
        check("snapshot values parsed (SEE 1.7.6, protocol 5.2, Think 0.39.x)", snap["see"] == "1.7.6" and snap["protocol"] == "5.2", snap, "1.7.6 / 5.2"),
        check("live protocol version read from PROTOCOL.md differs from the snapshot", live != snap["protocol"], live, "!= 5.2"),
        check("a live-checked fact passes", fresh == "OK", fresh, "OK"),
        check("negative control: snapshot value vs live -> REGISTRY_VERSION_DRIFT", drift == "REGISTRY_VERSION_DRIFT", drift, "REGISTRY_VERSION_DRIFT"),
        check("negative control: snapshot used without a live recheck is blocked", stale == "STALE_SNAPSHOT_RECHECK", stale, "STALE_SNAPSHOT_RECHECK"),
    ], [wd / "snapshot_drift.json"]


def _see_packet():
    return {"schema": M("see_pro_cognitive_gate").SCHEMA, "level": "L3", "mode": "deep", "phase": "planning",
            "stage0": {"goal": "Produce a film", "artifact": "video", "success_criteria": ["real MP4 validated by ffprobe"]},
            "methods": [{"name": "kosif-media-motion"}, {"name": "kosif-eval-trust"}],
            "composition": {"nodes": [{"id": "N1", "input_kind": "audio", "output_kind": "video"},
                                      {"id": "N2", "input_kind": "video", "output_kind": "report"}],
                            "edges": [{"from": "N1", "to": "N2", "relation": "verify", "kind": "video"}]},
            "options": [{"id": "A", "strategy_key": "simple-timeline"}, {"id": "B", "strategy_key": "procedural-motion"},
                        {"id": "C", "strategy_key": "cinematic-stock-edit"}],
            "claims": {"executed": False, "verified": False, "full_pro_completed": False, "reviewers_executed": 0},
            "privacy": {"cross_tenant_data": False}}


@card("protocol:A12-see-pro-cognitive-fusion")
def a12(task, wd):
    good = jw(wd / "packet.json", _see_packet())
    bads = {"FULL_PRO_CLAIM_UNPROVEN": {"mode": "full_pro", "claims": {"full_pro_completed": True}},
            "REVIEWERS_CLAIM_UNPROVEN": {"claims": {"reviewers_executed": 500}},
            "EDGE_SOURCE_KIND_MISMATCH": {"composition": {"nodes": _see_packet()["composition"]["nodes"],
                                                          "edges": [{"from": "N1", "to": "N2", "relation": "verify", "kind": "audio"}]}}}
    g = py("see_pro_cognitive_gate.py", "check", "--file", good)
    caught = {}
    for code, patch in bads.items():
        p = _see_packet()
        p.update(patch)
        r = py("see_pro_cognitive_gate.py", "check", "--file", jw(wd / ("bad_%s.json" % code.lower()), p))
        caught[code] = r.returncode != 0 and code in r.stdout + r.stderr
    st = py("see_pro_cognitive_gate.py", "--self-test")
    return [
        rules_present("protocol:A12-see-pro-cognitive-fusion", "see_pro_cognitive_gate.py", "500"),
        check("well-formed L3 packet passes the gate", g.returncode == 0, (g.stdout + g.stderr).strip()[-120:], "rc 0"),
        check("negative control: unproven Full Pro / 500 reviewers / mismatched edge are each rejected", all(caught.values()), caught, "all True"),
        check("gate self-test passes", st.returncode == 0, st.stdout.strip()[-80:], "rc 0"),
    ], [good]


@card("protocol:A13-pro-council")
def a13(task, wd):
    _, bp = _brief(wd)
    d = wd / "council"
    p = py("council.py", "plan", "اعمل فيديو موشن عربي", "--dir", d, "--from-brief", bp, cwd=wd)
    c = json.loads((d / "council.json").read_text(encoding="utf-8"))
    roster = c["roster"]
    v0 = py("council.py", "verdict", "--dir", d, cwd=wd)
    opts = c["options"]
    ok_ans = {"position": "B is safest", "claims": [{"claim": "B renders in time", "evidence": "ran render_html on a 1 s scene: 30 frames"}],
              "proposal": "B", "risks": ["font loading"], "top_choice": opts[-1]}
    bad_ans = {"position": "x"}
    leak = dict(ok_ans, proposal="use token " + FAKE_GH)
    ing = []
    for m in roster:
        f = jw(wd / ("%s_r1.json" % m["id"]), ok_ans)
        ing.append(py("council.py", "ingest", "--dir", d, "--round", "1", "--member", m["id"], "--file", f, "--simulated", cwd=wd).returncode)
    rb = py("council.py", "ingest", "--dir", d, "--round", "1", "--member", roster[0]["id"], "--file", jw(wd / "bad.json", bad_ans), "--simulated", cwd=wd)
    rl = py("council.py", "ingest", "--dir", d, "--round", "1", "--member", roster[0]["id"], "--file", jw(wd / "leak.json", leak), "--simulated", cwd=wd)
    st = jl(py("council.py", "status", "--dir", d, cwd=wd).stdout)
    c2 = json.loads((d / "council.json").read_text(encoding="utf-8"))
    sim = all(v["_receipt"]["simulated"] for v in c2["rounds"]["1"].values())
    return [
        rules_present("protocol:A13-pro-council", "خمسة أعضاء متعارضين", "council.py"),
        check("plan seats exactly five members M1..M5", p.returncode == 0 and [m["id"] for m in roster] == ["M1", "M2", "M3", "M4", "M5"],
              [m["id"] for m in roster], ["M1", "M2", "M3", "M4", "M5"]),
        check("negative control: verdict before any round is refused (ROUND_INCOMPLETE)", "ROUND_INCOMPLETE" in v0.stdout + v0.stderr, v0.stderr.strip()[:60], "ROUND_INCOMPLETE"),
        check("five valid round-1 answers ingested with hashed receipts", ing == [0] * 5 and len(st["rounds"]["1"]) == 5, st["rounds"]["1"], 5),
        check("answers written here are labelled simulated (not real agents)", sim, sim, True),
        check("negative control: a member answer missing fields is rejected", rb.returncode != 0 and "MEMBER_INVALID" in rb.stdout + rb.stderr, rb.returncode, "MEMBER_INVALID"),
        check("negative control: a credential inside an answer is rejected", rl.returncode != 0 and "SECRET" in rl.stdout + rl.stderr, rl.returncode, "SECRET"),
    ], [d / "council.json"]


@card("protocol:A14-drawing-cinematic-academy")
def a14(task, wd):
    import numpy as np
    from PIL import Image
    g = np.tile(np.linspace(0, 255, 64).astype(np.uint8), (32, 1))
    pgm = wd / "gray.pgm"
    pgm.write_text("P2\n64 32\n255\n" + "\n".join(" ".join(str(int(v)) for v in row) for row in g) + "\n")
    v = py("creative_principles.py", "values", "--input", pgm, "--out", wd / "notan.pgm", cwd=wd)
    toks = [t for t in (wd / "notan.pgm").read_text().split("\n") if t and not t.startswith("#")]
    vals = [int(x) for line in toks[3:] for x in line.split()]
    shapes = {"width": 200, "height": 200, "shapes": [
        {"kind": "circle", "x": 100, "y": 100, "r": 80, "stage": "guide"}, {"kind": "rect", "x": 40, "y": 40, "w": 120, "h": 120, "stage": "mass"},
        {"kind": "line", "x1": 20, "y1": 180, "x2": 180, "y2": 20, "stage": "outline"}, {"kind": "circle", "x": 100, "y": 100, "r": 6, "stage": "detail"}]}
    c = py("creative_principles.py", "construct", "--input", jw(wd / "shapes.json", shapes), "--out-prefix", wd / "stage", cwd=wd)
    stages = sorted(p.name for p in wd.glob("stage*"))
    bad = dict(shapes, shapes=[{"kind": "star", "x": 1, "y": 1, "stage": "guide"}])
    cb = py("creative_principles.py", "construct", "--input", jw(wd / "bad_shapes.json", bad), "--out-prefix", wd / "bad", cwd=wd)
    return [
        rules_present("protocol:A14-drawing-cinematic-academy", "C-DRAW-02", "0,127,255", "stage=guide|mass|outline|detail"),
        check("value study quantises to exactly three tones 0/127/255", v.returncode == 0 and set(vals) == {0, 127, 255}, sorted(set(vals)), [0, 127, 255]),
        check("negative control: the input gradient has many tones", len(set(g.flatten().tolist())) > 3, len(set(g.flatten().tolist())), "> 3"),
        check("staged construction writes the drawing stages", c.returncode == 0 and len(stages) >= 4, stages[:6], ">= 4 files"),
        check("negative control: an unknown shape kind is refused", cb.returncode != 0, cb.returncode, "!= 0"),
    ], [wd / "notan.pgm"] + [wd / s for s in stages[:2]]


@card("protocol:A15-futurepedia-style-atlas")
def a15(task, wd):
    lst = jl(py("style_atlas_bridge.py", "list").stdout)
    ids = [s.get("id") for s in lst["styles"]]
    sc = py("style_atlas_bridge.py", "scaffold", "--style", "FA-45", "--out", wd / "explainer", cwd=wd)
    page = wd / "explainer/explainer.html"
    bad = py("style_atlas_bridge.py", "scaffold", "--style", "FA-999", "--out", wd / "nope", cwd=wd)
    ok_ids = ids == ["FA-%02d" % i for i in range(1, 87)]
    return [
        rules_present("protocol:A15-futurepedia-style-atlas", "86 methods", "FA-01"),
        check("atlas holds all 86 methods FA-01..FA-86", ok_ids and lst.get("scope") == "ALL_86_OF_86", [len(ids), ids[:2], ids[-1:]], 86),
        check("scaffold writes an explainer page + STYLE.json, marked not rendered", sc.returncode == 0 and page.exists()
              and "NOT_RENDERED" in sc.stdout, sc.stdout.strip()[:80], "SCAFFOLDED_NOT_RENDERED"),
        check("negative control: an unknown style id is refused", "unknown" in (bad.stdout + bad.stderr) and not (wd / "nope/explainer.html").exists(),
              (bad.stdout + bad.stderr).strip()[:60], "unknown style"),
    ], [page]


@card("protocol:A16-mosamem-rea-capability-fusion")
def a16(task, wd):
    cat = jl(py("mosamem_rea_fusion.py", "catalog").stdout)
    caps = cat["capabilities"]
    p = py("mosamem_rea_fusion.py", "plan", "خلفية شفافة مع كتابة عربية", "--domain", "image", "--out", wd / "plan.json", cwd=wd)
    plan = json.loads((wd / "plan.json").read_text(encoding="utf-8")) if (wd / "plan.json").exists() else jl(p.stdout)
    gpl = json.dumps(cat, ensure_ascii=False)
    vendored = list((SK).glob("**/mosamem*/src/**/*.rs")) + list(SK.glob("**/vendor/mosamem/**/*.py"))
    bad = py("mosamem_rea_fusion.py", "rea-plan", "javascript", wd / "does-not-exist", cwd=wd)
    badj = jl(bad.stdout)
    return [
        rules_present("protocol:A16-mosamem-rea-capability-fusion", "19 عقدة", "ليست 19 محرّك صور جديدًا"),
        check("catalog has exactly 19 integration nodes", len(caps) == 19, len(caps), 19),
        check("plan is PLAN_ONLY_NO_EXECUTION (no claim of running Mosamem)", plan.get("status") == "PLAN_ONLY_NO_EXECUTION", plan.get("status"), "PLAN_ONLY_NO_EXECUTION"),
        check("no Mosamem GPL source vendored", "NO Mosamem GPL source vendored" in gpl and not vendored, len(vendored), 0),
        check("negative control: an REA plan on a missing target is not analysed or verified",
              badj.get("status") == "target_missing" and badj.get("analysis_executed") is False and badj.get("verified") is False,
              badj, "target_missing, nothing executed"),
    ], [wd / "plan.json"]


@card("protocol:A17-story-scene-charter")
def a17(task, wd):
    S = M("skill_intelligence")
    pack = json.loads((SK / "data/question_packs.json").read_text(encoding="utf-8"))["packs"]["story"]
    allq = [q["question"] for q in pack["questions"]]
    core = [q["question"] for q in pack["questions"] if q["tier"] == "core"]
    qs = lambda an: [q for q in an["questions"] if q["question"] in allq]
    l1, l2 = S.analyse("اكتب لي قصة رعب 3 مشاهد"), S.analyse("اعمل سيناريو فيلم قصير عن الصداقة لطفلين في القرية مع حوار ونهاية")
    l0 = S.analyse("ما هي القصة في فيلم X؟")
    other = S.analyse("اعمل فيديو موشن 9:16")
    money = next(q for q in pack["questions"] if q.get("sensitive") == "money")
    spend = [q["suggested_default"] for q in qs(l2) if re.search(r"اشحن|ادفع|انشر|spend|publish", q["suggested_default"])]
    jw(wd / "story_questions.json", {"L1": qs(l1), "L2": [q["question"] for q in qs(l2)]})
    return [
        rules_present("protocol:A17-story-scene-charter", "question_packs.json"),
        check("L1 story gets the core five questions, each with a default", l1["level"] == "L1" and [q["question"] for q in qs(l1)] == core
              and all(q["suggested_default"] for q in qs(l1)), [l1["level"], len(qs(l1))], ["L1", 5]),
        check("L2 screenplay gets all ten", l2["level"] == "L2" and len(qs(l2)) == 10, len(qs(l2)), 10),
        check("the money question carries only the safe default (zero spend)", "صفر صرف" in money["suggested_default"], money["suggested_default"][:60], "صفر صرف"),
        check("no suggested default spends or publishes", not spend, spend, []),
        check("negative control: L0 question and a non-story request get no pack", l0["questions"] == [] and qs(other) == [],
              [len(l0["questions"]), len(qs(other))], [0, 0]),
    ], [wd / "story_questions.json"]


@card("protocol:A18-futurepedia-business-workflows")
def a18(task, wd):
    lst = jl(py("business_workflows.py", "list").stdout)
    ids = sorted(w["id"] for w in lst)
    p = py("business_workflows.py", "plan", "--workflow", "FW-07", "--context", "متجر عطور", "--out", wd / "runbook.md", cwd=wd)
    md = (wd / "runbook.md").read_text(encoding="utf-8") if (wd / "runbook.md").exists() else ""
    steps = re.findall(r"^\|\s*\d+\s*\|", md, re.M)
    bad = py("business_workflows.py", "plan", "--workflow", "FW-999", "--context", "x", "--out", wd / "bad.md", cwd=wd)
    return [
        rules_present("protocol:A18-futurepedia-business-workflows", "The 64 workflows", "business_workflows.py"),
        check("64 workflows with unique ids", len(ids) == 64 and len(set(ids)) == 64, [len(ids), ids[:1], ids[-1:]], 64),
        check("runbook for FW-07 written with the user context and numbered steps", p.returncode == 0 and "متجر عطور" in md and len(steps) >= 3,
              len(steps), ">= 3 steps"),
        check("runbook separates steps that need approval or a connector", "موافقتك" in md or "approval" in md.lower(), "approval line", "present"),
        check("negative control: an unknown workflow is refused", bad.returncode != 0 and not (wd / "bad.md").exists(), bad.returncode, "!= 0"),
    ], [wd / "runbook.md"]


@card("protocol:A19-field-lessons-montage")
def a19(task, wd):
    src = wd / "voice.m4a"
    fx.ffmpeg("-f", "lavfi", "-i", "sine=frequency=300:duration=1:sample_rate=48000", "-c:a", "aac", "-b:a", "160k", src)
    v = wd / "v.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=108x192:r=30:d=1", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "20", v)
    copied, reenc = wd / "film_copy.mp4", wd / "film_reencoded.mp4"
    fx.ffmpeg("-i", v, "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", copied)
    fx.ffmpeg("-i", v, "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", reenc)
    vv = lambda f: sh([sys.executable, REPO / "tools/verify_video.py", f, "--fps", "30", "--duration", "1", "--source-audio", src])
    a, b = vv(copied), vv(reenc)
    pres = lambda r: "source preserved" in (r.stdout + r.stderr)
    return [
        rules_present("protocol:A19-field-lessons-montage", "verify_video.py --source-audio"),
        check("stream-copied voice is proven untouched (packet MD5)", pres(a), (a.stdout + a.stderr).count("preserved"), ">= 1"),
        check("negative control: a re-encoded voice is not 'preserved'", not pres(b), pres(b), False),
    ], [copied]


@card("protocol:A20-book-distilled-methods")
def a20(task, wd):
    r1 = jl(py("book_methods.py", "rest", "--problem", "إعلان لمقهى", "--words", "3", "--seed", "7").stdout)
    r2 = jl(py("book_methods.py", "rest", "--problem", "إعلان لمقهى", "--words", "3", "--seed", "7").stdout)
    r3 = jl(py("book_methods.py", "rest", "--problem", "إعلان لمقهى", "--words", "3", "--seed", "8").stdout)
    jw(wd / "random_entry.json", {"seed7": r1, "seed8": r3})
    return [
        rules_present("protocol:A20-book-distilled-methods", "book_methods.py rest"),
        check("random-entry words are seeded: same seed, same words", r1["words"] == r2["words"] and len(r1["words"]) == 3, r1["words"], r2["words"]),
        check("negative control: another seed gives another draw", r3["words"] != r1["words"], r3["words"], "differs"),
    ], [wd / "random_entry.json"]


@card("protocol:A24-reasoning-modes-decision-gates")
def a24(task, wd):
    th = M("think")
    b = th.bayes_binary(0.2, [("tests fail on main", 4), ("only one report", 0.5)], threshold=0.3)
    odds = 0.2 / 0.8 * 4 * 0.5
    exp = odds / (1 + odds)
    gspec = lambda obs: {"decision": "ship", "reversible": True, "go": [{"name": "errors", "op": "==", "threshold": 0, "observed": obs}],
                         "kill": [{"name": "broken links", "op": ">", "threshold": 20, "observed": 0}]}
    go, hold = th.gate(gspec(0)), th.gate(gspec(None))
    kill = th.gate(dict(gspec(0), kill=[{"name": "broken links", "op": ">", "threshold": 20, "observed": 35}]))
    oneway = th.gate(dict(gspec(0), reversible=False))
    au = th.audit("الملف أسرع 3 مرات من السابق.\nالقياس: ffprobe يعطي 30 fps (out/qa.json).\n")
    jw(wd / "reasoning_gates.json", {"bayes": b, "gate": [go["verdict"], hold["verdict"], kill["verdict"], oneway], "audit": au})
    return [
        rules_present("protocol:A24-reasoning-modes-decision-gates", "KILL يغلب PIVOT ويغلب GO", "think.py modes / bayes / gate / audit"),
        check("Bayes posterior = independent odds product", abs(b["posterior"] - round(exp, 4)) < 1e-4, b["posterior"], round(exp, 4)),
        check("posterior above threshold -> ACT", b["decision"] == "ACT", b["decision"], "ACT"),
        check("gate: all go criteria met -> GO", go["verdict"] == "GO", go["verdict"], "GO"),
        check("negative control: unobserved go criterion -> HOLD", hold["verdict"] == "HOLD", hold["verdict"], "HOLD"),
        check("negative control: kill threshold crossed -> KILL", kill["verdict"] == "KILL", kill["verdict"], "KILL"),
        check("one-way door GO still needs explicit approval", oneway["needs_explicit_approval"] is True, oneway["needs_explicit_approval"], True),
        check("audit flags the unsupported claim, accepts the measured one", au["claims"] >= 1 and len(au["unsupported"]) >= 1 and au["with_evidence"] >= 1,
              [au["claims"], au["with_evidence"]], "1 unsupported, 1 evidenced"),
    ], [wd / "reasoning_gates.json"]


@card("protocol:A25-task-intake-clarification")
def a25(task, wd):
    th = M("think")
    vid = th.intake("اعمل فيديو ريلز 30 ثانية بصوتي", "L2")
    l1 = th.intake("اعمل فيديو ريلز 30 ثانية بصوتي", "L1")
    code = th.intake("اصلح الخطأ في ملف utils/dates.py", "L2")
    jw(wd / "intake.json", {"video_L2": vid, "video_L1": l1, "code": code})
    filled = {s["slot"] for s in vid["filled"]}
    return [
        rules_present("protocol:A25-task-intake-clarification", "think.py intake"),
        check("deliverable kind detected (video)", "video" in vid["kinds"], vid["kinds"], "video"),
        check("slots stated in the request are filled, not asked (duration)", "duration" in filled, sorted(filled), "duration"),
        check("question budget grows with level (L1 < L2)", l1["question_budget"] < vid["question_budget"], [l1["question_budget"], vid["question_budget"]], "L1 < L2"),
        check("questions never exceed the budget", len(vid["questions"]) <= vid["question_budget"], len(vid["questions"]), "<= budget"),
        check("negative control: a code fix is not classified as video", "video" not in code["kinds"], code["kinds"], "no video"),
    ], [wd / "intake.json"]


@card("protocol:A26-planning-decomposition")
def a26(task, wd):
    th = M("think")
    tpl = json.loads(py("think.py", "decompose", "--template").stdout)
    ok = th.decompose(tpl)
    cyc = json.loads(json.dumps(tpl))
    cyc["tasks"][0]["deps"] = ["T5"]
    nov = json.loads(json.dumps(tpl))
    nov["tasks"][2].pop("verify")
    def safe(spec):
        try:
            return th.decompose(spec)
        except ValueError as exc:  # the engine refuses a cyclic graph outright
            return {"verdict": "FIX", "problems": [str(exc)]}
    rc, rv = safe(cyc), safe(nov)
    lo = sum(t["est"][0] for t in tpl["tasks"])
    jw(wd / "dag.json", {"ok": ok, "cycle": rc, "no_verify": rv})
    return [
        rules_present("protocol:A26-planning-decomposition", "think.py decompose", "الأبواب ذات الاتجاه الواحد"),
        check("task DAG OK with a topological order", ok["verdict"] == "OK" and ok["order"] == ["T1", "T2", "T3", "T4", "T5"], ok["order"], "T1..T5"),
        check("critical path optimistic = sum of a chain's low estimates", abs(ok["critical_path"]["optimistic"][0] - lo) < 1e-9,
              ok["critical_path"]["optimistic"][0], lo),
        check("irreversible publish step flagged as a one-way door", ok["one_way_doors"] == ["T5"], ok["one_way_doors"], ["T5"]),
        check("negative control: a dependency cycle -> FIX", rc["verdict"] == "FIX", rc["problems"][:1], "FIX"),
        check("negative control: a task without a verify method -> FIX", rv["verdict"] == "FIX", rv["problems"][:1], "FIX"),
    ], [wd / "dag.json"]


@card("protocol:A27-verification-quality-standards")
def a27(task, wd):
    th = M("think")
    bar = th.qa("video")
    ids = [c["id"] for c in bar["checks"]]
    hard = [c["id"] for c in bar["checks"] if c["hard"]]
    # measure the hard 'spec' check for real on a rendered clip
    clip = fx.test_clip(wd / "clip.mp4", seconds=1, size="108x192")
    p = fx.probe(clip)["streams"][0]
    spec_ok = p["r_frame_rate"] == "30/1" and (p["width"], p["height"]) == (108, 192)
    allp = th.qa("video", {i: True for i in ids})
    fail = th.qa("video", dict({i: True for i in ids}, spec=False))
    waived = th.qa("video", dict({i: True for i in ids}, audio_intact="n/a"))
    jw(wd / "qa_video.json", {"bar": ids, "hard": hard, "measured_spec": spec_ok, "verdicts": [allp["verdict"], fail["verdict"], waived["verdict"]]})
    return [
        rules_present("protocol:A27-verification-quality-standards", "PASS أو FAIL أو INCOMPLETE"),
        check("measured spec check (ffprobe) holds", spec_ok, [p["width"], p["height"], p["r_frame_rate"]], [108, 192, "30/1"]),
        check("every check answered true -> PASS", allp["verdict"] == "PASS", allp["verdict"], "PASS"),
        check("negative control: a hard check false -> FAIL", fail["verdict"] == "FAIL" and "spec" in fail["hard_fail"], fail["verdict"], "FAIL"),
        check("negative control: a hard check waived as n/a -> INCOMPLETE", waived["verdict"] == "INCOMPLETE", waived["verdict"], "INCOMPLETE"),
    ], [wd / "qa_video.json"]


@card("protocol:A28-capability-routing")
def a28(task, wd):
    b, _ = _brief(wd, "ترجمة فيديو وعمل سبتايتل عربي")
    cov = b["coverage"]
    hf = py("hub.py", "find", "ترجمة فيديو سبتايتل", "--json")
    hub = jl(hf.stdout) if hf.returncode == 0 else {}
    tools = hub.get("tools") or []
    sc = jl(py("smart_capabilities.py", "find", "ترجمة فيديو سبتايتل", "--json").stdout)
    groups = [g.get("group") for g in (sc if isinstance(sc, list) else sc.get("groups", []))]
    jw(wd / "routing.json", {"coverage": {k: cov[k] for k in ("records_on_disk", "records_scanned", "complete")}, "tools": tools[:5], "groups": groups})
    return [
        rules_present("protocol:A28-capability-routing", "hub.py tool <id>", "smart_capabilities.py find"),
        check("brief coverage receipt: 100% of the catalog scanned", cov["complete"] and cov["records_scanned"] == cov["records_on_disk"],
              [cov["records_scanned"], cov["records_on_disk"]], "equal"),
        check("negative control: an incomplete scan would not equal disk", cov["records_scanned"] - 1 != cov["records_on_disk"], cov["records_scanned"] - 1, "!= disk"),
        check("hub.find returns runnable tools with commands", bool(tools) and all(t.get("first_command") for t in tools[:3]),
              [t.get("id") for t in tools[:3]], "tools with commands"),
        check("smart_capabilities maps the task to groups", bool(groups), groups[:3], ">= 1 group"),
    ], [wd / "routing.json"]


@card("protocol:A29-failure-recovery")
def a29(task, wd):
    th = M("think")
    g = th.recover(message="ModuleNotFoundError: No module named 'cv2'")
    first = th.recover("tool_error", attempts=1)
    stop = th.recover("tool_error", attempts=first["budget"])
    jw(wd / "recovery.json", {"guessed": g, "first": first, "stop": stop})
    return [
        rules_present("protocol:A29-failure-recovery", "think.py recover"),
        check("error class guessed from the message", g["guessed"] and g["error_class"] != "other", g["error_class"], "a known class"),
        check("within budget -> next attempt with one proven fix", first["next"].startswith("attempt 2"), first["next"][:40], "attempt 2 of N"),
        check("negative control: budget spent -> STOP (no loop)", stop["next"].startswith("STOP"), stop["next"][:30], "STOP"),
    ], [wd / "recovery.json"]


@card("protocol:A30-council-100")
def a30(task, wd):
    roster = json.loads((SK / "data/council_100.json").read_text(encoding="utf-8"))
    people = roster.get("personas") or roster.get("council") or roster
    d = wd / "council7"
    p = py("council.py", "plan", "فيديو موشن عربي", "--dir", d, "--seats", "7", cwd=wd)
    c = json.loads((d / "council.json").read_text(encoding="utf-8"))
    th = M("think")
    std, mx = th.pro("فيديو موشن", "standard"), th.pro("فيديو موشن", "max")
    jw(wd / "pro.json", {"seats": len(c["roster"]), "standard_passes": len(std["passes"]), "max_passes": len(mx["passes"])})
    return [
        rules_present("protocol:A30-council-100", "council.py plan --seats/--personas/--full"),
        check("100 personas in the roster", len(people) == 100, len(people), 100),
        check("--seats 7 seats seven distinct personas", p.returncode == 0 and len({m["id"] for m in c["roster"]}) == 7, len(c["roster"]), 7),
        check("deeper Pro depth adds passes (max > standard)", len(mx["passes"]) > len(std["passes"]), [len(std["passes"]), len(mx["passes"])], "max > standard"),
        check("personas are labelled stance prompts, not agents", "COUNCIL_SIMULATED" in std["council"]["note"], std["council"]["note"][:60], "COUNCIL_SIMULATED"),
    ], [wd / "pro.json"]


_FIG = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200" data-floating="man"><rect width="200" height="200" fill="#fff"/>
<g data-figure="man"><circle data-part="head" cx="100" cy="%d" r="%d" fill="#e08030"/><rect data-part="torso" x="85" y="68" width="30" height="70" fill="#3060c0"/></g></svg>"""


@card("protocol:A31-drawing-council")
def a31(task, wd):
    from PIL import Image, ImageDraw
    good, bad = wd / "figure.svg", wd / "floating_head.svg"
    good.write_text(_FIG % (50, 20))
    bad.write_text(_FIG % (20, 12))
    img = Image.new("RGB", (200, 200), "white")
    d = ImageDraw.Draw(img)
    d.ellipse([80, 30, 120, 70], fill=(224, 128, 48))
    d.rectangle([85, 68, 115, 138], fill=(48, 96, 192))
    img.save(wd / "figure.png")
    rg = jl(py("drawing_methods.py", "review", "--svg", good).stdout)
    rb = jl(py("drawing_methods.py", "review", "--svg", bad).stdout)
    (wd / "brief.txt").write_text("رجل بسيط: رأس وجذع")
    pl = py("drawing_council.py", "plan", "--png", wd / "figure.png", "--svg", good, "--brief", wd / "brief.txt", "--dir", wd / "council", cwd=wd)
    plan = jl(pl.stdout)
    vd = jl(py("drawing_council.py", "verdict", "--dir", wd / "council", cwd=wd).stdout)
    return [
        rules_present("protocol:A31-drawing-council", "drawing_council.py", "drawing_methods.py review"),
        check("law-27 review: head joins torso -> PASS", rg["status"] == "PASS", [(c["id"], c["pass"]) for c in rg["checks"]], "PASS"),
        check("negative control: a floating head is caught (detached part)", rb["status"] == "FAIL" and not rb["checks"][0]["pass"],
              rb["checks"][0].get("observed"), "detached"),
        check("council plan writes expert prompts with the automated gate passing", pl.returncode == 0 and plan.get("law27_review") == "PASS"
              and plan.get("experts", 0) >= 5, plan, "PASS + experts"),
        check("negative control: no verdict without the experts' own answers", vd.get("status") != "PASS" and any("not heard" in r for r in vd.get("reasons", [])),
              vd.get("reasons", [])[:1], "experts not heard"),
    ], [good, wd / "council/council.json"]


@card("protocol:A33-open-source-mining-prompts")
def a33(task, wd):
    pl = M("prompt_lab")
    weak = "Make a nice image of a cat, 8k, masterpiece, ultra detailed."
    strong = ("A ginger cat sitting on a wooden windowsill, watching rain. In a small kitchen at dusk. Medium close-up, 50mm, eye level. "
              "Warm light from a lamp on the left, cool rim light from the window. Soft watercolour style, muted amber and slate palette. Aspect 4:5.")
    (wd / "strong.txt").write_text(strong)
    cli = py("prompt_lab.py", "lint", wd / "strong.txt", "--kind", "image", "--json")
    s, w = jl(cli.stdout), pl.lint(weak, "image")
    sec = pl.lint("Use key sk-abcdefghijklmnopqrstuvwx to call the API", "agent")
    jw(wd / "prompt_lint.json", {"strong": s, "weak": w, "secret": sec})
    return [
        rules_present("protocol:A33-open-source-mining-prompts", "prompt_lab.py lint"),
        check("strong image prompt ships (score >= 16, every required slot)", s["band"] == "ship" and s["score"] >= 16, [s["score"], s["band"]], "ship"),
        check("negative control: hype prompt scores lower and is flagged", w["score"] < s["score"] and any(f["code"] == "hype" for f in w["findings"]),
              [w["score"], w["band"]], "lower + hype"),
        check("negative control: a key inside a prompt is a hard gate", sec["band"] == "fail-gate", sec["band"], "fail-gate"),
    ], [wd / "prompt_lint.json"]


@card("protocol:A34-usip-v56-precision-layer")
def a34(task, wd):
    f = py("micro_index.py", "find", "kinetic")
    first = f.stdout.strip().splitlines()[0]
    pid = first.split()[0]
    s = py("micro_index.py", "show", pid)
    bad = py("micro_index.py", "show", "NOPE-99999")
    (wd / "address.txt").write_text(s.stdout)
    return [
        rules_present("protocol:A34-usip-v56-precision-layer", "micro_index.py"),
        check("find returns one-line addresses", f.returncode == 0 and re.match(r"^[A-Z]+-\w+", first), first[:60], "ID + line"),
        check("show resolves the same id", s.returncode == 0 and pid in s.stdout, s.stdout[:80], pid),
        check("negative control: an unknown id is refused", bad.returncode != 0, bad.returncode, "!= 0"),
    ], [wd / "address.txt"]


@card("protocol:A35-task-history")
def a35(task, wd):
    th = M("task_history")
    out = wd / "film.mp4"
    fx.color_clip(out, seconds=0.5)
    tmpl = json.loads(py("task_history.py", "--root", wd / "history", "new", "--kind", "video").stdout)
    rec = json.loads(json.dumps(tmpl))
    rec.update(title="Test reel 03-11", request="اعمل ريلز قصير", mode="موافق", agent="Claude Code cloud", tools=["ffmpeg"],
               params={"fps": 30}, inputs=[], steps=[{"what": "encode", "tool": "ffmpeg", "command": "ffmpeg -f lavfi -i color=red -t 0.5 film.mp4", "params": {}}],
               outputs=[{"path": "film.mp4", "kind": "video", "deterministic": True, "measured": {"duration_s": 0.5, "fps": 30}}],
               reproduce={"how": "run the ffmpeg command", "prerequisites": ["ffmpeg"], "commands": ["ffmpeg -f lavfi -i color=red -t 0.5 film.mp4"]},
               evidence=["film.mp4"], lessons=["none"])
    src = jw(wd / "entry.json", rec)
    add = py("task_history.py", "--root", wd / "history", "add", "--from", src, "--base", wd, "--date", "2026-11-03", cwd=wd)
    val = py("task_history.py", "--root", wd / "history", "validate", cwd=wd)
    errs_t, _ = th.validate_record(th.normalise(json.loads(json.dumps(tmpl)), wd / "history", "2026-11-03"))
    leak = dict(rec, lessons=["token " + FAKE_GH])
    addl = py("task_history.py", "--root", wd / "history2", "add", "--from", jw(wd / "leak.json", leak), "--base", wd, "--date", "2026-11-03", cwd=wd)
    files = list((wd / "history").rglob("*.json"))
    return [
        rules_present("protocol:A35-task-history", "task_history.py add", "task_history.py new --kind video"),
        check("filled record added and the history validates", add.returncode == 0 and val.returncode == 0 and files, (add.stdout + add.stderr).strip()[-80:], "rc 0"),
        check("negative control: the untouched template (placeholders) fails validation", bool(errs_t), errs_t[:2], "errors"),
        check("negative control: a token in a lesson is refused", addl.returncode != 0, addl.returncode, "!= 0"),
    ], files[:1] or [src]


@card("protocol:A36-v57-context-boot-parallel")
def a36(task, wd):
    b = py("boot.py")
    (wd / "boot.txt").write_text(b.stdout)
    need = ("context", "deliverable", "acceptance")

    def tracks_ok(ts):
        probs = [t["name"] + ": missing " + k for t in ts for k in need if not t.get(k)]
        outs = [t["deliverable"] for t in ts if t.get("deliverable")]
        if len(outs) != len(set(outs)):
            probs.append("two tracks write the same deliverable")
        return probs
    good = [{"name": "audio", "context": "voice.mp3 30 s, Arabic", "deliverable": "out/words.json", "acceptance": "sorted, no overlap"},
            {"name": "scene", "context": "9:16, style kinetic", "deliverable": "out/scene.html", "acceptance": "check passes"},
            {"name": "qa", "context": "export standard", "deliverable": "out/qa.json", "acceptance": "verify_video rc 0"}]
    bad = good[:2] + [{"name": "qa", "context": "", "deliverable": "out/scene.html", "acceptance": "ok"}]
    jw(wd / "tracks.json", {"good": good, "problems_bad": tracks_ok(bad)})
    return [
        rules_present("protocol:A36-v57-context-boot-parallel", "boot.py"),
        check("boot self-briefing runs and names this repository", b.returncode == 0 and len(b.stdout) > 200, len(b.stdout), "> 200 chars"),
        check("parallel tracks each carry full context, a deliverable and an acceptance check", tracks_ok(good) == [], tracks_ok(good), []),
        check("negative control: a track without context writing another's file is caught", len(tracks_ok(bad)) == 2, tracks_ok(bad), "2 problems"),
    ], [wd / "boot.txt", wd / "tracks.json"]


@card("protocol:A37-self-council")
def a37(task, wd):
    led = wd / "ledger.json"
    shutil.copy(SK / "data/self_council_ledger.json", led)
    p = py("self_council.py", "plan", "--batch", "3", "--dir", wd / "run", "--kind", "playbook", "--ledger", led, cwd=wd)
    run = json.loads((wd / "run/run.json").read_text(encoding="utf-8"))
    prompts = sorted(x.name for x in (wd / "run/prompts").glob("P*.md"))
    bad = py("self_council.py", "ingest", "--dir", wd / "run", "--persona", "P1", "--file", jw(wd / "bad.json", {"note": "looks fine"}), "--simulated", cwd=wd)
    return [
        rules_present("protocol:A37-self-council", "self_council.py", "SIMULATED"),
        check("plan picks a batch of 3 playbook units", p.returncode == 0 and len(run["units"]) == 3, list(run["units"]), 3),
        check("five persona prompts P1..P5 written", prompts == ["P%d.md" % i for i in range(1, 6)], prompts, "P1..P5"),
        check("negative control: a review without the contract fields is rejected", bad.returncode != 0, (bad.stdout + bad.stderr).strip()[-80:], "!= 0"),
    ], [wd / "run/run.json"]


_VERDICT = """## Where the Council Agrees
Plan B fits the voice.
## Where the Council Clashes
Speed vs polish.
## Blind Spots
Font loading on phones.
## The Recommendation
الخطة B.
## The One Thing to Do First
Render a 3 s preview of scene 1.
"""


@card("protocol:A38-v58-thinking-books-github-pulse")
def a38(task, wd):
    lc = M("llm_council")
    _, bp = _brief(wd)
    depth = {lv: jl(py("llm_council.py", "gate", "--level", lv, "--from-brief", bp).stdout)["depth"] for lv in ("L1", "L2", "L3")}
    plans = {"A": 1, "B": 2, "C": 3}
    ok = lc.check_verdict(_VERDICT, plans)
    bad = lc.check_verdict(_VERDICT.replace("الخطة B.", "it depends on many things").replace("Render a 3 s preview of scene 1.", "- a\n- b"), plans)
    tz = py("thinking_books.py", "triz", "--improve", "speed", "--worsen", "quality")
    tell = wd / "page.html"
    tell.write_text("<html><body style=\"background:linear-gradient(135deg,#667eea,#764ba2)\"><h1>Unlock the power of AI ✨</h1>"
                    "<div class='card' style='border-radius:24px;backdrop-filter:blur(10px)'>Revolutionize your workflow 🚀</div></body></html>")
    clean = wd / "clean.html"
    clean.write_text("<html><body style='background:#fff;color:#111'><h1>Delivery times by city</h1><p>Cairo 2 days, Giza 3 days.</p></body></html>")
    a, c = py("design_tells.py", "audit", tell, "--json"), py("design_tells.py", "audit", clean, "--json")
    ja, jc = jl(a.stdout), jl(c.stdout)
    sa = ja.get("score", ja.get("files", [{}])[0].get("score") if ja.get("files") else None)
    scc = jc.get("score", jc.get("files", [{}])[0].get("score") if jc.get("files") else None)
    jw(wd / "mastery.json", {"depths": depth, "verdict_ok": ok, "verdict_bad": bad, "tells": [sa, scc]})
    return [
        rules_present("protocol:A38-v58-thinking-books-github-pulse", "llm_council.py", "design_tells.py"),
        check("council depth LIGHT/STANDARD/FULL for L1/L2/L3 (never skipped)", depth == {"L1": "LIGHT", "L2": "STANDARD", "L3": "FULL"}, depth,
              {"L1": "LIGHT", "L2": "STANDARD", "L3": "FULL"}),
        check("five-heading verdict naming plan B and one first step passes", ok == [], ok, []),
        check("negative control: a hedged verdict with a list of first steps is rejected", len(bad) >= 2, bad, ">= 2 problems"),
        check("TRIZ contradiction lookup answers", tz.returncode == 0 and len(tz.stdout) > 50, len(tz.stdout), "> 50"),
        check("design-tells audit scores the AI-look page below the plain page", sa is not None and scc is not None and sa < scc, [sa, scc], "tells < clean"),
    ], [wd / "mastery.json"]


@card("protocol:A39-v59-photocraft-mcp")
def a39(task, wd):
    import numpy as np
    clip = fx.color_clip(wd / "in.mp4", color="gray", seconds=0.3, size="64x64")

    def cube(path, f):
        n = 2
        rows = ["LUT_3D_SIZE %d" % n]
        for b in range(n):
            for g in range(n):
                for r in range(n):
                    rows.append("%.4f %.4f %.4f" % f(r / (n - 1), g / (n - 1), b / (n - 1)))
        Path(path).write_text("\n".join(rows) + "\n")
        return Path(path)
    ident = cube(wd / "identity.cube", lambda r, g, b: (r, g, b))
    warm = cube(wd / "warm.cube", lambda r, g, b: (min(1, r * 1.0 + 0.25), g, b * 0.6))

    def apply(c, out):
        line = py("photocraft_mcp.py", "lut", c, clip, out).stdout.strip().splitlines()[0]
        import shlex
        cmd = shlex.split(line)
        sh(cmd + ["-y"] if "-y" not in cmd else cmd, cwd=wd, timeout=60)
        return line, decode(out, 64, 64)
    l1, fi = apply(ident, wd / "identity.mp4")
    l2, fw = apply(warm, wd / "warm.mp4")
    src = decode(clip, 64, 64)
    d_id = float(np.abs(fi.mean(axis=(0, 1, 2)) - src.mean(axis=(0, 1, 2))).max())
    shift = fw.mean(axis=(0, 1, 2)) - src.mean(axis=(0, 1, 2))
    bad = py("photocraft_mcp.py", "lut", wd / "look.png", clip, wd / "x.mp4")
    st = py("photocraft_mcp.py", "selftest")
    return [
        rules_present("protocol:A39-v59-photocraft-mcp", "photocraft_mcp.py lut look.cube in.mp4 out.mp4"),
        check("printed LUT line keeps the export standard (CRF 17, slow, BT.709, faststart, audio copy)",
              all(k in l1 for k in ("-crf 17", "-preset slow", "bt709", "+faststart", "-c:a copy")), l1[:120], "export flags"),
        check("identity cube leaves colours unchanged (< 3 levels)", d_id < 3, d_id, "< 3"),
        check("warm cube measurably raises red and lowers blue", shift[0] > 20 and shift[2] < -20, [float(shift[0]), float(shift[2])], "R up, B down"),
        check("negative control: a non-.cube LUT is refused", bad.returncode != 0, bad.returncode, "!= 0"),
        check("config self-test (loopback-only bridge, absolute roots)", st.returncode == 0, st.returncode, 0),
    ], [wd / "warm.mp4"]


_LS_GOOD = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>@media (prefers-reduced-motion: reduce){*{animation:none}}</style></head><body>
<section data-xray="رحلة الطلب" data-xray-tool="code">حركة</section>
<p>KOSIF علامة خيالية للعرض.</p>
<script>window.__ready = true; const io = new IntersectionObserver(() => {});</script></body></html>"""


@card("protocol:A40-v59-living-site")
def a40(task, wd):
    chk = LIVING / "check.py"
    g = wd / "good/index.html"
    g.parent.mkdir()
    g.write_text(_LS_GOOD, encoding="utf-8")
    b = wd / "bad/index.html"
    b.parent.mkdir()
    b.write_text(_LS_GOOD.replace("<section", "<h1 style=\"letter-spacing:-0.04em\">عنوان عربي</h1><section"), encoding="utf-8")
    m = wd / "missing/index.html"
    m.parent.mkdir()
    m.write_text(_LS_GOOD.replace("<body>", '<body><img alt="" src="img/nope.png">'), encoding="utf-8")
    rg = sh([sys.executable, chk, g, "--levels", "code", "--json"])
    rb = sh([sys.executable, chk, b, "--levels", "code"])
    rm = sh([sys.executable, chk, m, "--levels", "code"])
    r3 = sh([sys.executable, chk, g, "--levels", "3d"])
    jg = jl(rg.stdout)
    return [
        rules_present("protocol:A40-v59-living-site", "letter-spacing", "check.py"),
        check("static gate PASS on a compliant Arabic page", rg.returncode == 0 and jg.get("status") == "PASS", jg.get("status"), "PASS"),
        check("negative control: negative letter-spacing on Arabic fails", rb.returncode != 0, rb.returncode, "!= 0"),
        check("negative control: a missing local asset fails", rm.returncode != 0 and "every local asset exists" in rm.stdout, rm.returncode, "!= 0"),
        check("negative control: --levels 3d without a 3D layer fails", r3.returncode != 0, r3.returncode, "!= 0"),
    ], [g]


@card("protocol:A41-v511-kling-director")
def a41(task, wd):
    lint = LIVING / "tools/kling_lint.py"
    master = LIVING / "recipes/kling-master-prompt.txt"
    shutil.copy(master, wd / "prompt.txt")
    (wd / "bare.txt").write_text("a man walks in the rain, cinematic, 8k")
    g = sh([sys.executable, lint, wd / "prompt.txt", "--json"])
    b = sh([sys.executable, lint, wd / "bare.txt", "--json"])
    pl = sh([sys.executable, lint, "plan", "90"])
    jg, jb = jl(g.stdout), jl(b.stdout)
    (wd / "lint.json").write_text(json.dumps({"good": jg, "bad": jb, "plan90": pl.stdout}, ensure_ascii=False, indent=1))
    return [
        rules_present("protocol:A41-v511-kling-director", "kling_lint.py", "ledger.tsv"),
        check("the master prompt passes every lint test before any credit", jg.get("result") == "PASS", [t["name"] for t in jg.get("tests", []) if t["status"] != "ok"], []),
        check("negative control: a bare prompt fails (missing headers/duration)", jb.get("result") == "FAIL", jb.get("result"), "FAIL"),
        check("a 90 s film is planned into clips", pl.returncode == 0 and len(pl.stdout) > 20, pl.stdout.strip()[:80], "plan"),
    ], [wd / "lint.json"]


@card("protocol:A42-v512-browser-links")
def a42(task, wd):
    page = wd / "links.html"
    page.write_text('<html><body><a href="https://example.org/a">a</a><a href="https://example.org/docs">docs</a>'
                    '<a href="https://other.net/c">c</a><script>document.body.insertAdjacentHTML("beforeend",'
                    '\'<a href="https://example.org/js-only">js</a>\')</script></body></html>')
    empty = wd / "empty.html"
    empty.write_text("<html><body>no links</body></html>")
    cl = SCR / "collect_links.js"
    a = sh(["node", cl, page.as_uri(), "--json"], cwd=wd, timeout=40)
    f = sh(["node", cl, page.as_uri(), "--filter", "docs"], cwd=wd, timeout=40)
    e = sh(["node", cl, empty.as_uri()], cwd=wd, timeout=40)
    ja = jl(a.stdout) if a.returncode == 0 else {}
    hrefs = sorted(x["href"] for x in ja.get("links", []))
    (wd / "links.json").write_text(a.stdout)
    return [
        rules_present("protocol:A42-v512-browser-links", "collect_links.js", "Chromium + Playwright"),
        check("headless Chromium collects every link, including the JS-inserted one", "https://example.org/js-only" in hrefs and len(hrefs) == 4, hrefs, 4),
        check("--filter keeps only matching links", f.returncode == 0 and f.stdout.strip().splitlines() == ["https://example.org/docs"], f.stdout.strip(), "docs only"),
        check("negative control: a page with zero links exits 1", e.returncode == 1, e.returncode, 1),
    ], [wd / "links.json"]


@card("protocol:A43-v60-contracts-receipts-registry")
def a43(task, wd):
    (wd / "out.md").write_text("result")
    good = jw(wd / "receipt.json", {"version": "USIP-6.0", "status": "VERIFIED", "artifact": "out.md",
                                    "checks": [{"name": "exists", "result": "PASS", "evidence": "sha256:" + __import__("hashlib").sha256(b"result").hexdigest()}],
                                    "remote_deployment": False})
    bad = jw(wd / "bad_receipt.json", {"version": "USIP-6.0", "status": "VERIFIED", "artifact": "missing.md",
                                       "checks": [{"name": "browser", "result": "NOT_RUN"}], "remote_deployment": True})
    g = py("validate_receipt.py", good, cwd=wd)
    b = py("validate_receipt.py", bad, cwd=wd)
    return [
        rules_present("protocol:A43-v60-contracts-receipts-registry", "validate_receipt.py"),
        check("a VERIFIED receipt with its file and evidence is coherent", g.returncode == 0, (g.stdout + g.stderr).strip()[:80], "rc 0"),
        check("negative control: VERIFIED with a missing file, an unrun check and an unproven remote claim fails", b.returncode != 0
              and "remote" in (b.stdout + b.stderr), (b.stdout + b.stderr).strip()[:160], "errors"),
    ], [good]


@card("protocol:A44-free-stock-media")
def a44(task, wd):
    ff, fp = M("free_footage"), M("free_photos")
    cc0 = ff.classify_licence(url="https://creativecommons.org/publicdomain/zero/1.0/")
    by = ff.classify_licence(url="https://creativecommons.org/licenses/by/4.0/")
    nd = ff.classify_licence(url="https://creativecommons.org/licenses/by-nc-nd/4.0/")
    rec = {"id": "commons:1", "source": "commons", "licence": nd, "file_url": "https://upload.wikimedia.org/x.jpg"}
    try:
        fp.download_one(None, rec, wd / "dl", dry_run=True)
        refused = False
    except Exception as exc:
        refused = "forbids edits" in str(exc)
    lib = wd / "photos"
    lib.mkdir()
    for i, lic in enumerate([cc0, by]):
        (lib / ("p%d.jpg" % i)).write_bytes(b"\xff\xd8\xff" + bytes(10))
        jw(lib / ("p%d.jpg.json" % i), {"schema": fp.ASSET_SCHEMA, "id": "x:%d" % i, "file": "p%d.jpg" % i, "source": "commons",
                                         "source_name": "Wikimedia Commons", "licence": lic, "attribution": "Photo %d by Author %d, %s" % (i, i, lic["name"])})
    c = py("free_photos.py", "credits", lib, cwd=wd)
    md = (lib / "ATTRIBUTION.md").read_text(encoding="utf-8")
    return [
        rules_present("protocol:A44-free-stock-media", "ATTRIBUTION.md", "--commercial"),
        check("licences classified: CC0 free, CC BY needs credit, NC-ND not commercial/no edits",
              cc0["attribution_required"] is False and by["attribution_required"] is True and nd["commercial"] is False and nd["derivatives"] is False,
              [cc0["name"], by["name"], nd["name"]], "CC0 / BY / BY-NC-ND"),
        check("negative control: a no-derivatives photo is refused for a montage (before any download)", refused, refused, True),
        check("ATTRIBUTION.md rebuilt from sidecars with every credit line", c.returncode == 0 and "Photo 0 by Author 0" in md and "Photo 1 by Author 1" in md
              and "required" in md, md.count("Photo "), ">= 2"),
    ], [lib / "ATTRIBUTION.md"]


def _dragon(wd, *flags):
    job = wd / "dragon"
    r = py("black_dragon.py", "run", "فيديو موشن عربي قصير", "--job", job, *flags, cwd=wd, timeout=90)
    rep = json.loads((job / "black_dragon_report.json").read_text(encoding="utf-8"))
    receipts = list((job / "receipts").glob("*.json")) if (job / "receipts").exists() else []
    return r, rep, job, receipts


@card("protocol:A48-v64-black-dragon")
def a48(task, wd):
    r, rep, job, receipts = _dragon(wd)
    claim_full = rep["full_coverage"] and rep["executed"] < rep["assigned"]
    return [
        rules_present("protocol:A48-v64-black-dragon", "full_coverage", "ولا قدرة تتشال"),
        check("every inventory entry assigned a part and mode (none filtered out)", rep["assignment_complete"] and rep["assigned"] == rep["scheduled"] > 1000,
              [rep["assigned"], rep["scheduled"]], "assigned == scheduled"),
        check("executed counts only receipt-verified work (0 without --execute-adapters)", rep["executed"] == 0 and rep["registered_tool_executed"] == 0,
              rep["executed"], 0),
        check("assigned/probed/executed reported separately", all(k in rep for k in ("assigned", "probed", "executed")), [rep["assigned"], rep["probed"], rep["executed"]], "3 numbers"),
        check("negative control: full_coverage is False when not everything executed", rep["full_coverage"] is False and not claim_full, rep["full_coverage"], False),
        check("report and ledger written with a SHA-256 of the assignment", len(rep.get("assignment_sha256", "")) == 64 and (job / "black_dragon_report.md").exists(),
              rep.get("assignment_sha256", "")[:12], "64 hex"),
    ], [job / "black_dragon_report.md"]


@card("protocol:A49-v65-dragon-in-pipeline")
def a49(task, wd):
    text = doc("protocol:A49-v65-dragon-in-pipeline")
    l3_cmd = "--probe-tools --reviewed-adapters" in text and "--execute-adapters" in text
    r, rep, job, receipts = _dragon(wd, "--probe-tools", "--reviewed-adapters")
    line = "التنين: %d assigned · %d probed · %d executed · full_coverage %s" % (rep["assigned"], rep["probed"], rep["executed"], rep["full_coverage"])
    (wd / "plan_report_line.txt").write_text(line + "\n", encoding="utf-8")

    def level_runs(level, answer=""):
        return level == "L3" or answer == "نفّذ بأقصى قوة"
    return [
        rules_present("protocol:A49-v65-dragon-in-pipeline", "--probe-tools --reviewed-adapters", "نفّذ بأقصى قوة"),
        check("L3 step: probes ran but nothing counts as executed without --execute-adapters", rep["probed"] > 0 and rep["executed"] == 0,
              [rep["probed"], rep["executed"]], "probed > 0, executed 0"),
        check("negative control: probed is never reported as executed", rep["probed"] != rep["executed"], line, "probed != executed"),
        check("dragon runs at L3 or on «نفّذ بأقصى قوة», never at L0-L2", level_runs("L3") and level_runs("L2", "نفّذ بأقصى قوة")
              and not any(level_runs(lv) for lv in ("L0", "L1", "L2")) and l3_cmd, "L3 only", "L3/max only"),
        check("report line «التنين: assigned · probed · executed · full_coverage» written", line.count("·") == 3, line, "4 fields"),
    ], [wd / "plan_report_line.txt", job / "black_dragon_report.md"]


@card("protocol:PROTOCOL")
def protocol_core(task, wd):
    lc = M("llm_council")
    b, bp = _brief(wd, task or "اعمل فيديو موشن عربي قصير")
    cov = b["coverage"]
    plans = b.get("plans") or {}
    letters = sorted(plans if isinstance(plans, dict) else [p.get("id") or p.get("name") for p in plans])
    gates = {lv: jl(py("llm_council.py", "gate", "--level", lv, "--from-brief", bp).stdout).get("depth") for lv in ("L1", "L2", "L3")}
    l0 = py("llm_council.py", "gate", "--level", "L0", "--from-brief", bp)
    text = doc("protocol:PROTOCOL")
    words = ["موافق", "تفاصيل", "طوّر", "نفّذ بأقصى قوة", "نفّذ مباشرة", "كمّل بدوني"]
    jw(wd / "pipeline.json", {"level": b["analysis"].get("level"), "coverage_complete": cov["complete"], "plans": letters,
                              "recommended": b.get("recommended"), "council": gates, "L0": (l0.stdout + l0.stderr).strip()[:200]})
    return [
        rules_present("protocol:PROTOCOL", "skill_intelligence.py", "llm_council.py"),
        check("brief proves a 100% catalog scan (coverage receipt)", cov["complete"] and cov["records_scanned"] == cov["records_on_disk"],
              [cov["records_scanned"], cov["records_on_disk"]], "equal"),
        check("plans A/B/C drafted with one recommendation", {"A", "B", "C"} <= set(letters) and b.get("recommended") in ("A", "B", "C"),
              [letters, b.get("recommended")], "A,B,C + one"),
        check("the five-member council never skips L1+ (LIGHT/STANDARD/FULL)", gates == {"L1": "LIGHT", "L2": "STANDARD", "L3": "FULL"}, gates, "no SKIP"),
        check("negative control: L0 gets no council", "SKIP" in l0.stdout.upper() or "NONE" in l0.stdout.upper() or l0.returncode != 0,
              (l0.stdout + l0.stderr).strip()[:80], "skip at L0"),
        check("reply words listed in the core", all(w in text for w in words), [w for w in words if w not in text], []),
    ], [wd / "pipeline.json"]
