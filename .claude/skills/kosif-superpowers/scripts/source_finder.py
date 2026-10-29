#!/usr/bin/env python3
"""KOSIF Source Finder — إيجاد اللقطات الأصلية لكل مشهد في فيديو مرجعي.

Finds the ORIGINAL source clips behind the shots of a reference video (an edit, a reel, a montage):
detect the cuts, take clean query frames per shot (cropping burned-in text away), reverse-search each
frame on Yandex Images, collect the Pinterest pins it returns, download the video pins among them and verify
every candidate frame by frame with ORB features, a ratio test and RANSAC homography inliers. Pins go through
the shared helper _pinterest.py (as in fetch_video.py): each is classified first (video, image, gif, embedded
YouTube, deleted, CDN-refused ...) and never retried, only video pins are downloaded, in a temp folder, their
real size is measured with ffprobe, their own audio (usually the creator's music) is stripped unless
--keep-audio, and <work>/cand/p<id>.pin.json records the outcome and a credit line. The inlier count
is what makes a hit trustworthy: on the first real run (a 13-shot dua reel) four exact sources scored
514-1447 inliers, and across six reels unrelated clips scored about 7-36.

  python3 source_finder.py cuts VIDEO [--threshold 27] [--min-shot 0.4] [--out cuts.json]
  python3 source_finder.py frames VIDEO --cuts cuts.json --out q/ [--crop "crop=iw:ih*0.6:0:ih*0.2"]
  python3 source_finder.py search IMAGE... [--pages sites,similar] [--delay 4] [--out search.json]
  python3 source_finder.py match QUERY.jpg... --candidates DIR|FILE|PIN_ID|PIN_URL|search.json ... [--work W]
  python3 source_finder.py run VIDEO --work W [--crop ...] [--shots 0,3-5] [--exact 150] [--candidates DIR]
  python3 source_finder.py doctor

Scores: >= --exact (150) inliers = the same footage (exact source); >= --possible (40) = worth a look;
below = no match. Hit rate depends on whether the source was posted on Pinterest as a video pin and is
indexed by Yandex: on the other reels of the same session it found one shot of four, then none. Yandex and Pinterest
pages change and Yandex may answer with a captcha; the tool waits between Yandex calls and stops at the
first captcha. Found clips belong to their creators: credit and link them, and reuse only with the
owner's permission or a licence. cv2/numpy are imported only inside the commands that need them.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as _dt
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pinterest as pinterest  # noqa: E402 - the shared Pinterest pin helper (fetch_video.py uses it too)
from _pinterest import PIN_RE, pin_url  # noqa: E402,F401 - pin_url is part of this module's interface

SCHEMA = "kosif.source_finder.v1"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
UPLOAD_URL = ("https://yandex.com/images/search?rpt=imageview&format=json&request="
              "%7B%22blocks%22%3A%5B%7B%22block%22%3A%22b-page_type_search-by-image__link%22%7D%5D%7D")
PAGE_URL = "https://yandex.com/images/search?"
PAGES = ("sites", "similar")
MIN_DELAY = 2.0            # seconds between Yandex calls, whatever --delay says
EXACT = 150                # inliers: same footage
POSSIBLE = 40              # inliers: worth a manual look (observed unrelated clips: 7-36)
ORB_FEATURES = 3000
RATIO = 0.75
RANSAC_PX = 6.0
WORK_WIDTH = 540
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
CREDIT = ("Found clips belong to their creators: credit and link each source (url) in the description, and download "
          "or reuse a clip only with the owner's permission or a licence. Pinterest pins are often re-uploads, so "
          "trace the original creator before asking.")
LIMITS = ("Finds a source only when it is posted on Pinterest as a video pin and Yandex indexes it; many reels have no "
          "findable source. Yandex and Pinterest pages can change or answer with a captcha (the run stops there). "
          "Hard cuts only: dissolves and fades are not split. Mirrored, heavily zoomed, re-graded or AI-redrawn "
          "footage scores lower.")

URL_RE = re.compile(r"https?://[^\"'\s<>\\]+")
LEAD_RE = re.compile(r"tiktok\.com/@|instagram\.com/(?:p|reel|reels)/|youtube\.com/(?:watch|shorts)|youtu\.be/|vimeo\.com/\d"
                     r"|pexels\.com|pixabay\.com|vecteezy\.com|shutterstock\.com|istockphoto\.com|storyblocks\.com"
                     r"|mixkit\.co|dreamstime\.com|artgrid\.io|motionarray\.com", re.I)
CROP_RE = re.compile(r"^crop=[A-Za-z0-9_:*/+\-.() ]+$")


class SourceFinderError(Exception):
    """A clear, user-facing failure (missing dependency, bad input, changed page)."""


class CaptchaError(SourceFinderError):
    """Yandex asked for a captcha: stop all further calls."""


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _cv():
    try:
        import cv2  # noqa: PLC0415
        import numpy as np  # noqa: PLC0415
    except ImportError as e:  # pragma: no cover - exercised by the no-cv2 test in a subprocess
        raise SourceFinderError(f"this command needs OpenCV and numpy: pip install opencv-python-headless numpy ({e})")
    return cv2, np


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def parse_shots(spec) -> set | None:
    """'0,3-5' -> {0,3,4,5}; empty -> None (all shots)."""
    if not spec:
        return None
    out = set()
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out


# ----------------------------------------------------------------------------------------------- cuts

def _fps(cap, cv2) -> float:
    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    return fps if 0 < fps < 1000 else 30.0


def detect_cuts(video, threshold: float = 27.0, min_shot: float = 0.4, width: int = 96, keep_scores: bool = False) -> dict:
    """Hard cuts from frame differences: mean HSV change of a small copy of consecutive frames (0-255 scale)."""
    cv2, np = _cv()
    video = Path(video)
    if not video.is_file():
        raise SourceFinderError(f"no such video: {video}")
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise SourceFinderError(f"OpenCV cannot open {video}")
    fps = _fps(cap, cv2)
    min_gap = max(1, int(round(min_shot * fps)))
    prev, i, last, cut_frames, scores = None, 0, 0, [], []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (width, max(1, int(round(h * width / w)))), interpolation=cv2.INTER_AREA)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV).astype(np.int16)
        if prev is not None:
            d = np.abs(hsv - prev)
            d[..., 0] = np.minimum(d[..., 0], 180 - d[..., 0])      # hue is circular (0..179)
            score = float(d.reshape(-1, 3).mean(axis=0).mean())
            if keep_scores:
                scores.append(round(score, 2))
            if score >= threshold and i - last >= min_gap:
                cut_frames.append(i)
                last = i
        prev = hsv
        i += 1
    cap.release()
    if i == 0:
        raise SourceFinderError(f"no frames could be decoded from {video}")
    if cut_frames and i - cut_frames[-1] < min_gap:                   # a flash just before the end
        cut_frames.pop()
    duration = i / fps
    bounds = [0.0] + [round(f / fps, 3) for f in cut_frames] + [round(duration, 3)]
    shots = [{"shot": k, "start": bounds[k], "end": bounds[k + 1], "duration": round(bounds[k + 1] - bounds[k], 3)}
             for k in range(len(bounds) - 1)]
    out = {"schema": SCHEMA + ".cuts", "video": str(video), "fps": round(fps, 3), "frames": i,
           "duration": round(duration, 3), "threshold": threshold, "min_shot": min_shot,
           "cut_frames": cut_frames, "boundaries": bounds, "shots": shots}
    if keep_scores:
        out["scores"] = scores
    return out


def load_cuts(spec) -> list:
    """A cuts.json from `cuts`, a JSON list of boundaries, or '0,1.2,3.4' -> list of shot dicts."""
    p = Path(str(spec))
    if p.is_file():
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("shots"), list):
            return [{"shot": int(s["shot"]), "start": float(s["start"]), "end": float(s["end"])} for s in data["shots"]]
        bounds = data.get("boundaries") if isinstance(data, dict) else data
    else:
        try:
            bounds = [float(x) for x in str(spec).split(",") if x.strip()]
        except ValueError:
            raise SourceFinderError(f"--cuts must be a cuts.json file or comma-separated seconds, got {spec!r}")
    if not isinstance(bounds, list) or len(bounds) < 2:
        raise SourceFinderError("--cuts needs at least two boundaries (start and end of the video)")
    bounds = [float(b) for b in bounds]
    if any(b2 <= b1 for b1, b2 in zip(bounds, bounds[1:])):
        raise SourceFinderError("--cuts boundaries must be strictly increasing")
    return [{"shot": k, "start": bounds[k], "end": bounds[k + 1]} for k in range(len(bounds) - 1)]


# --------------------------------------------------------------------------------------------- frames

def shot_times(start: float, end: float, n: int = 3) -> list:
    """n query times inside a shot, kept away from its cuts (0.35 s, or a quarter of a short shot)."""
    length = max(0.0, end - start)
    if n <= 1 or length <= 0:
        return [round((start + end) / 2, 3)]
    m = min(0.35, length / 4)
    span = length - 2 * m
    return [round(start + m + span * k / (n - 1), 3) for k in range(n)]


def check_crop(crop) -> str | None:
    """An ffmpeg crop filter only ('crop=w:h:x:y' or 'w:h:x:y'); anything else is refused."""
    if not crop:
        return None
    c = str(crop).strip()
    if not c.startswith("crop="):
        c = "crop=" + c
    if not CROP_RE.match(c):
        raise SourceFinderError(f"--crop must be one ffmpeg crop filter such as crop=iw:ih*0.6:0:ih*0.2, got {crop!r}")
    return c


def grab_frame(video, t: float, out: Path, vf: str | None = None) -> None:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SourceFinderError("ffmpeg is not installed (it extracts the query frames)")
    out.parent.mkdir(parents=True, exist_ok=True)
    err = ""
    for tt in (t, max(0.0, t - 0.2)):                 # a seek at the very end can return no frame
        cmd = [exe, "-v", "error", "-y", "-ss", f"{tt:.3f}", "-i", str(video), "-frames:v", "1"]
        if vf:
            cmd += ["-vf", vf]
        cmd += ["-q:v", "3", str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if r.returncode == 0 and out.is_file() and out.stat().st_size > 0:
            return
        err = r.stderr.strip()[:200]
    raise SourceFinderError(f"ffmpeg could not take a frame at {t:.2f}s of {video}: {err}")


def extract_frames(video, shots: list, out_dir, crop=None, per_shot: int = 3, full: bool = True, only=None) -> dict:
    """Per shot: per_shot cropped query frames (s007_0.jpg ...) plus one full mid frame (s007_full.jpg)."""
    video, out_dir = Path(video), Path(out_dir)
    if not video.is_file():
        raise SourceFinderError(f"no such video: {video}")
    vf = check_crop(crop)
    manifest = {"schema": SCHEMA + ".frames", "video": str(video), "crop": vf, "per_shot": per_shot, "shots": []}
    for s in shots:
        k = int(s["shot"])
        if only is not None and k not in only:
            continue
        entry = {"shot": k, "start": s["start"], "end": s["end"], "queries": []}
        for j, t in enumerate(shot_times(s["start"], s["end"], per_shot)):
            p = out_dir / f"s{k:03d}_{j}.jpg"
            grab_frame(video, t, p, vf)
            entry["queries"].append({"t": t, "path": str(p)})
        if full:
            mid = round((s["start"] + s["end"]) / 2, 3)
            p = out_dir / f"s{k:03d}_full.jpg"
            grab_frame(video, mid, p)
            entry["full"] = {"t": mid, "path": str(p)}
        manifest["shots"].append(entry)
    _write_json(out_dir / "frames.json", manifest)
    return manifest


# --------------------------------------------------------------------------------------------- search

_LAST_CALL = [0.0]
_LOCK = threading.Lock()


def _throttle(delay: float) -> None:
    """Wait so that Yandex calls are at least max(delay, MIN_DELAY) seconds apart."""
    delay = max(MIN_DELAY, float(delay))
    with _LOCK:
        wait = _LAST_CALL[0] + delay - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _LAST_CALL[0] = time.monotonic()


def _curl(args: list, delay: float, follow: bool = False, timeout: int = 45) -> str:
    exe = shutil.which("curl")
    if not exe:
        raise SourceFinderError("curl is not installed (the reverse image search uses it)")
    _throttle(delay)
    cmd = [exe, "-sS", "--max-time", str(timeout), "-A", UA] + (["-L"] if follow else []) + list(args)
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        raise SourceFinderError(f"network call failed (curl exit {r.returncode}): {r.stderr.strip()[:200]}")
    return r.stdout


def parse_upload(text: str) -> str:
    """The cbirId of an uploaded image from Yandex's JSON answer; CaptchaError when it asks for a captcha."""
    try:
        data = json.loads(text)
    except ValueError:
        if "captcha" in text.lower():
            raise CaptchaError("Yandex answered the upload with a captcha")
        raise SourceFinderError(f"Yandex upload did not return JSON (starts {text[:80]!r}); the page may have changed")
    if isinstance(data, dict) and (data.get("type") == "captcha" or "captcha" in data):
        raise CaptchaError("Yandex answered the upload with a captcha")
    try:
        return str(data["blocks"][0]["params"]["cbirId"])
    except (KeyError, IndexError, TypeError):
        m = re.search(r"cbir_id=([^&\"\\\s]+)", text)
        if m:
            return urllib.parse.unquote(m.group(1))
        raise SourceFinderError("no cbirId in Yandex's answer; the search-by-image API may have changed")


def page_is_captcha(page: str) -> bool:
    low = page.lower()
    return "showcaptcha" in low[:20000] or ("captcha" in low and len(page) < 60000)


def extract_links(page: str) -> dict:
    """Pinterest pin ids (in page order, unique), their URLs and other video/stock leads from a results page."""
    text = html.unescape(page).replace("\\/", "/")
    urls = []
    for blob in (text, urllib.parse.unquote(text)):
        for u in URL_RE.findall(blob):
            if u not in urls:
                urls.append(u)
    pins, pin_urls, leads = [], [], []
    for u in urls:
        m = PIN_RE.search(u)
        if m:
            if m.group(1) not in pins:
                pins.append(m.group(1))
                pin_urls.append(u)
        elif LEAD_RE.search(u) and "yandex." not in u.split("/")[2] and u not in leads:
            leads.append(u)
    return {"pins": pins, "pinterest": pin_urls, "leads": leads[:25]}


def _safe_upload_path(image: Path):
    """curl -F treats ; , and quotes in a path specially: copy such files to a plain temporary name."""
    if not re.search(r'[;,"]', str(image)):
        return image, None
    tmp = Path(tempfile.mkdtemp(prefix="sf_"))
    dst = tmp / ("q" + image.suffix.lower())
    shutil.copyfile(image, dst)
    return dst, tmp


def yandex_search(image, pages=PAGES, delay: float = 4.0) -> dict:
    """Upload one image to Yandex search-by-image, read the requested result pages, return pins and leads."""
    image = Path(image)
    if not image.is_file():
        raise SourceFinderError(f"no such image: {image}")
    upath, tmp = _safe_upload_path(image)
    try:
        cbir = parse_upload(_curl(["-F", f"upfile=@{upath}", UPLOAD_URL], delay))
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    out = {"image": str(image), "cbir_id": cbir, "pages": {}, "pins": [], "pinterest": [], "leads": []}
    for page in pages:
        body = _curl([PAGE_URL + urllib.parse.urlencode({"cbir_id": cbir, "rpt": "imageview", "cbir_page": page})],
                     delay, follow=True)
        if page_is_captcha(body):
            raise CaptchaError(f"Yandex asked for a captcha on the '{page}' page")
        links = extract_links(body)
        out["pages"][page] = {"bytes": len(body), "pins": len(links["pins"]), "leads": len(links["leads"])}
        for pid, u in zip(links["pins"], links["pinterest"]):
            if pid not in out["pins"]:
                out["pins"].append(pid)
                out["pinterest"].append(u)
        out["leads"] += [u for u in links["leads"] if u not in out["leads"]]
    return out


def cached_search(image, cache_dir: Path, pages=PAGES, delay: float = 4.0) -> dict:
    """yandex_search with a JSON cache keyed by the image's bytes (<stem>-<sha256[:16]>.json), so a re-run after a
    captcha with the same frames repeats no call, while a frame that changed under the same name (another --crop,
    shots renumbered by --threshold/--min-shot, another video in the same --work) is searched again."""
    image = Path(image)
    if not image.is_file():
        raise SourceFinderError(f"no such image: {image}")
    digest = hashlib.sha256(image.read_bytes()).hexdigest()
    cache = Path(cache_dir) / f"{image.stem}-{digest[:16]}.json"
    if cache.is_file():
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("sha256") == digest and set(pages) <= set(data.get("pages", {})):
                return data
        except ValueError:
            pass
    data = yandex_search(image, pages, delay)
    data["sha256"] = digest
    _write_json(cache, data)
    return data


# ---------------------------------------------------------------------------------------- candidates

def download_pin(pid: str, cand_dir: Path, timeout: int = 120, strip_audio: bool = True):
    """One Pinterest pin -> cand_dir/p<id>.mp4 through the shared helper (_pinterest.fetch): classified first with
    one yt-dlp -J call, downloaded only when it is a video, in a temp folder (no fragment files left in cand_dir),
    measured with ffprobe and, by default, stripped of the pin's own audio (pins usually carry the creator's music).
    Every outcome is written to cand_dir/p<id>.pin.json with a credit record; a non-video pin returns None."""
    cand_dir = Path(cand_dir)
    out = cand_dir / f"p{pid}.mp4"
    if out.is_file() and not strip_audio:
        return out
    if not out.is_file() and (cand_dir / f"p{pid}.none").exists():   # miss marker of versions before 2026-10-29
        return None
    cmd = pinterest.ytdlp_command()
    if not cmd and not out.is_file():                                 # a finished file is reused without yt-dlp
        raise SourceFinderError("yt-dlp is not installed (pip install yt-dlp); or pass downloaded clips with --candidates DIR")
    rec = pinterest.fetch(pid, cand_dir, name=f"p{pid}", ytdlp=cmd, strip_audio=strip_audio, timeout=timeout)
    if rec.get("file"):
        return Path(rec["file"])
    if not rec.get("cached") and not rec.get("repeated"):
        log(f"pin {pid}: {rec.get('kind')}: {rec.get('reason')}")
    return None


def pin_outcomes(pins, cand_dir) -> dict:
    """What happened to each pin (from its p<id>.pin.json): counts per kind and the unusable ones with their reason."""
    counts, skipped = {}, []
    for pid in pins:
        rec = pinterest.read_record(cand_dir, f"p{pid}") or {}
        kind = rec.get("kind") or ("video" if (Path(cand_dir) / f"p{pid}.mp4").is_file() else "unknown")
        counts[kind] = counts.get(kind, 0) + 1
        if kind != "video":
            skipped.append({"pin": pid, "kind": kind, "reason": rec.get("reason")})
    return {"counts": dict(sorted(counts.items())), "skipped": skipped}


def resolve_candidates(items, work, download: bool = True, max_pins: int = 80, jobs: int = 4,
                       strip_audio: bool = True, outcomes: dict | None = None) -> list:
    """Folders, video/image files, search JSON files, pin ids and pin URLs -> [{label, file, url, kind}].
    Pins are downloaded with download_pin (audio stripped unless strip_audio is False); when `outcomes` is a dict
    it receives pin_outcomes() for the pins of this call."""
    files, pins = [], []

    def add_file(p: Path):
        ext = p.suffix.lower()
        if ext not in VIDEO_EXT | IMAGE_EXT:
            return
        m = re.fullmatch(r"p(\d{6,})", p.stem)
        url = pin_url(m.group(1)) if m else None
        files.append({"label": f"pin:{m.group(1)}" if m else p.name, "file": str(p), "url": url,
                      "kind": "video" if ext in VIDEO_EXT else "image"})

    expanded = []
    for raw in items:                                     # "123,456" lists are split unless it is a real path
        raw = str(raw)
        expanded += [x.strip() for x in raw.split(",") if x.strip()] if "," in raw and not Path(raw).exists() else [raw]
    for item in expanded:
        p = Path(item)
        if p.is_dir():
            for f in sorted(p.iterdir()):
                if f.is_file():
                    add_file(f)
        elif p.is_file() and p.suffix.lower() == ".json":
            data = json.loads(p.read_text(encoding="utf-8"))
            for rec in data if isinstance(data, list) else [data]:
                for pid in (rec.get("pins") or []) if isinstance(rec, dict) else []:
                    if pid not in pins:
                        pins.append(str(pid))
        elif p.is_file():
            add_file(p)
        else:
            pid = pinterest.pin_id(item)
            if not pid:
                raise SourceFinderError(f"candidate {item!r} is not a folder, file, pin id or Pinterest pin URL")
            if pid not in pins:
                pins.append(pid)
    pins = pins[:max_pins]
    if pins:
        cand_dir = Path(work) / "cand"
        if download:
            with cf.ThreadPoolExecutor(max(1, jobs)) as ex:
                got = list(ex.map(lambda pid: download_pin(pid, cand_dir, strip_audio=strip_audio), pins))
        else:
            got = [cand_dir / f"p{pid}.mp4" if (cand_dir / f"p{pid}.mp4").is_file() else None for pid in pins]
        for pid, f in zip(pins, got):
            if f:
                files.append({"label": f"pin:{pid}", "file": str(f), "url": pin_url(pid), "kind": "video"})
        if outcomes is not None:
            outcomes.update(pin_outcomes(pins, cand_dir))
    seen, out = set(), []
    for c in files:
        if c["file"] not in seen:
            seen.add(c["file"])
            out.append(c)
    return out


# ---------------------------------------------------------------------------------------------- match

def read_image(path):
    cv2, np = _cv()
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR) if data.size else None
    if img is None:
        raise SourceFinderError(f"cannot read image {path}")
    return img


class Matcher:
    """ORB (3000) on a 540-px-wide grey copy, Lowe ratio 0.75, RANSAC homography (6 px): score = inliers."""

    def __init__(self, nfeatures: int = ORB_FEATURES, ratio: float = RATIO, ransac_px: float = RANSAC_PX,
                 width: int = WORK_WIDTH):
        self.cv2, self.np = _cv()
        self.orb = self.cv2.ORB_create(nfeatures)
        self.bf = self.cv2.BFMatcher(self.cv2.NORM_HAMMING)
        self.ratio, self.ransac_px, self.width = ratio, ransac_px, width

    def features(self, img):
        cv2, np = self.cv2, self.np
        g = img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        s = self.width / g.shape[1]
        g = cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
        kp, des = self.orb.detectAndCompute(g, None)
        pts = np.float32([k.pt for k in kp]) if kp else np.zeros((0, 2), np.float32)
        return pts, des

    def score(self, fa, fb) -> int:
        """RANSAC inliers between two feature sets; the raw good-match count (< 8) when too few to fit."""
        pa, da = fa
        pb, db = fb
        if da is None or db is None or len(pa) < 10 or len(pb) < 10:
            return 0
        good = [m[0] for m in self.bf.knnMatch(da, db, k=2) if len(m) == 2 and m[0].distance < self.ratio * m[1].distance]
        if len(good) < 8:
            return len(good)
        a = pa[[g.queryIdx for g in good]]
        b = pb[[g.trainIdx for g in good]]
        _h, mask = self.cv2.findHomography(a, b, self.cv2.RANSAC, self.ransac_px)
        return int(mask.sum()) if mask is not None else 0

    def score_images(self, a, b) -> int:
        return self.score(self.features(a), self.features(b))


def iter_video_frames(path, step: float = 0.5, max_seconds: float = 180.0):
    """(t, frame) every `step` seconds, decoding sequentially (no seeking) up to max_seconds."""
    cv2, _np = _cv()
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return
    fps = _fps(cap, cv2)
    every = max(1, int(round(fps * step)))
    i = 0
    try:
        while i / fps <= max_seconds and cap.grab():
            if i % every == 0:
                ok, frame = cap.retrieve()
                if ok:
                    yield round(i / fps, 2), frame
            i += 1
    finally:
        cap.release()


def verdict(score: int, exact: int = EXACT, possible: int = POSSIBLE) -> str:
    return "exact" if score >= exact else "possible" if score >= possible else "none"


def match_candidates(queries, candidates, matcher: Matcher | None = None, step: float = 0.5,
                     max_seconds: float = 180.0, exact: int = EXACT, possible: int = POSSIBLE) -> list:
    """Best (score, time, query) per candidate, sorted by score; score = max over queries and sampled frames.
    A candidate that cannot be decoded (a corrupt image, a video OpenCV cannot open) scores 0 with an "error"
    and the others are still checked; an unreadable query image stops the whole call."""
    matcher = matcher or Matcher()
    qfeats = [(str(q), matcher.features(read_image(q))) for q in queries]
    results = []
    for c in candidates:
        best, error = (0, None, None), None
        if c["kind"] == "image":
            try:
                frames = [(None, read_image(c["file"]))]
            except SourceFinderError as e:
                frames, error = [], str(e)
        else:
            frames = iter_video_frames(c["file"], step, max_seconds)
        sampled = 0
        for t, frame in frames:
            sampled += 1
            cf_ = matcher.features(frame)
            for qpath, qf in qfeats:
                s = matcher.score(qf, cf_)
                if s > best[0]:
                    best = (s, t, qpath)
        if sampled == 0 and error is None:
            error = f"no frame could be decoded from {c['file']}"
        rec = {"candidate": c["label"], "url": c.get("url"), "file": c["file"], "score": best[0],
               "t": best[1], "query": best[2], "frames_checked": sampled, "verdict": verdict(best[0], exact, possible)}
        if error:
            rec["error"] = error
            log(f"skipped candidate {c['label']}: {error}")
        results.append(rec)
    results.sort(key=lambda r: (-r["score"], r["candidate"]))
    return results


# ------------------------------------------------------------------------------------------------ run

def run(video, work, crop=None, shots=None, threshold: float = 27.0, min_shot: float = 0.4, per_shot: int = 3,
        full: bool = True, pages=PAGES, delay: float = 4.0, max_pins: int = 80, jobs: int = 4, step: float = 0.5,
        max_seconds: float = 180.0, exact: int = EXACT, possible: int = POSSIBLE, candidates=None,
        download: bool = True, top: int = 5, strip_audio: bool = True) -> dict:
    """cuts -> frames -> search (or fixed --candidates) -> download -> match; writes <work>/report.json."""
    video, work = Path(video), Path(work)
    work.mkdir(parents=True, exist_ok=True)
    cuts = detect_cuts(video, threshold, min_shot)
    _write_json(work / "cuts.json", cuts)
    log(f"cuts: {len(cuts['shots'])} shots in {cuts['duration']} s")
    frames = extract_frames(video, cuts["shots"], work / "queries", crop, per_shot, full and not candidates, shots)
    matcher = Matcher()
    fixed = resolve_candidates(candidates, work, download, max_pins, jobs, strip_audio=strip_audio) if candidates else None
    report = {"schema": SCHEMA, "video": str(video), "work": str(work), "created": _now(),
              "settings": {"crop": frames["crop"], "per_shot": per_shot, "pages": list(pages), "delay": max(MIN_DELAY, delay),
                           "max_pins": max_pins, "step": step, "cut_threshold": threshold, "pin_audio":
                           "stripped" if strip_audio else "kept", "mode": "fixed-candidates" if candidates else "yandex+pinterest"},
              "thresholds": {"exact": exact, "possible": possible,
                             "meaning": "RANSAC homography inliers between a query frame and the best candidate frame"},
              "shots": [], "ranked": [], "summary": {}, "stopped": None, "credit": CREDIT, "limits": LIMITS}
    for entry in frames["shots"]:
        k = entry["shot"]
        qpaths = [q["path"] for q in entry["queries"]]
        rec = {"shot": k, "start": entry["start"], "end": entry["end"], "queries": qpaths, "searched": False,
               "pins_found": 0, "pin_kinds": {}, "pins_skipped": [], "candidates": 0, "verdict": "none", "best": None,
               "top": [], "leads": [], "errors": []}
        if fixed is not None:
            cands = fixed
            rec["searched"] = True
        else:
            pins, leads = [], []
            try:
                for img in qpaths + ([entry["full"]["path"]] if entry.get("full") else []):
                    try:
                        res = cached_search(img, work / "search", pages, delay)
                    except CaptchaError:
                        raise
                    except SourceFinderError as e:
                        rec["errors"].append(f"{Path(img).name}: {e}")
                        continue
                    pins += [p for p in res.get("pins", []) if p not in pins]
                    leads += [u for u in res.get("leads", []) if u not in leads]
            except CaptchaError as e:
                report["stopped"] = (f"captcha at shot {k}: {e}. Stopped all Yandex calls. Wait (hours), or solve it in a "
                                     "browser, then re-run the same command: finished searches are cached in "
                                     f"{work / 'search'}.")
                report["shots"].append(rec)
                log(report["stopped"])
                break
            rec.update(searched=True, pins_found=len(pins), leads=leads[:10])
            oc = {}
            cands = resolve_candidates(pins, work, download, max_pins, jobs, strip_audio=strip_audio, outcomes=oc) if pins else []
            rec.update(pin_kinds=oc.get("counts", {}), pins_skipped=oc.get("skipped", [])[:20])
        rec["candidates"] = len(cands)
        results = match_candidates(qpaths, cands, matcher, step, max_seconds, exact, possible) if cands else []
        rec["top"] = results[:top]
        if results:
            rec["best"] = results[0]
            rec["verdict"] = results[0]["verdict"]
        report["shots"].append(rec)
        b = rec["best"]
        log(f"shot {k}: {rec['verdict']}" + (f" {b['candidate']} score {b['score']} at {b['t']} s" if b else "")
            + f" ({rec['candidates']} candidates)")
        _write_json(work / "report.json", report)                    # partial report after every shot
    hits = [dict(shot=s["shot"], **s["best"]) for s in report["shots"] if s["best"] and s["verdict"] != "none"]
    report["ranked"] = sorted(hits, key=lambda h: -h["score"])
    counts = {v: sum(1 for s in report["shots"] if s["searched"] and s["verdict"] == v) for v in ("exact", "possible", "none")}
    report["summary"] = {"shots": len(frames["shots"]), "searched": sum(1 for s in report["shots"] if s["searched"]), **counts}
    _write_json(work / "report.json", report)
    return report


# ----------------------------------------------------------------------------------------------- CLI

def _emit(obj, out=None) -> None:
    text = json.dumps(obj, ensure_ascii=False, indent=1)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(text + "\n", encoding="utf-8")
        log(f"wrote {out}")
    else:
        print(text)


def cmd_cuts(a) -> int:
    _emit(detect_cuts(a.video, a.threshold, a.min_shot, keep_scores=a.scores), a.out)
    return 0


def cmd_frames(a) -> int:
    m = extract_frames(a.video, load_cuts(a.cuts), a.out, a.crop, a.per_shot, not a.no_full, parse_shots(a.shots))
    _emit({"frames": str(Path(a.out) / "frames.json"), "shots": len(m["shots"]),
           "images": sum(len(s["queries"]) + (1 if s.get("full") else 0) for s in m["shots"])})
    return 0


def cmd_search(a) -> int:
    images = a.images[: a.max_images]
    if len(a.images) > a.max_images:
        log(f"only the first {a.max_images} images are searched (--max-images)")
    pages = tuple(p for p in a.pages.split(",") if p)
    results, code = [], 0
    for img in images:
        try:
            results.append(yandex_search(img, pages, a.delay))
            log(f"{img}: {len(results[-1]['pins'])} pins, {len(results[-1]['leads'])} other leads")
        except CaptchaError as e:
            log(f"STOPPED: {e}. No further Yandex calls were made; wait or solve the captcha in a browser, then retry "
                "the remaining images.")
            code = 3
            break
    _emit(results, a.out)
    return code


def cmd_match(a) -> int:
    oc = {}
    cands = resolve_candidates(a.candidates, a.work, not a.no_download, a.max_pins, a.jobs,
                               strip_audio=not a.keep_audio, outcomes=oc)
    if not cands:
        raise SourceFinderError("no usable candidates (no video/image files, or no pin was a downloadable video: "
                                f"{oc.get('counts') or 'no pins'}; reasons in <work>/cand/p<id>.pin.json)")
    res = match_candidates(a.queries, cands, None, a.step, a.max_seconds, a.exact, a.possible)
    _emit({"schema": SCHEMA + ".match", "queries": a.queries, "thresholds": {"exact": a.exact, "possible": a.possible},
           "results": res[: a.top], "candidates": len(cands), "pin_kinds": oc.get("counts", {}),
           "pins_skipped": oc.get("skipped", [])[:20], "credit": CREDIT}, a.out)
    return 0


def cmd_run(a) -> int:
    rep = run(a.video, a.work, a.crop, parse_shots(a.shots), a.threshold, a.min_shot, a.per_shot, not a.no_full,
              tuple(p for p in a.pages.split(",") if p), a.delay, a.max_pins, a.jobs, a.step, a.max_seconds,
              a.exact, a.possible, a.candidates, not a.no_download, a.top, strip_audio=not a.keep_audio)
    _emit({"report": str(Path(a.work) / "report.json"), "summary": rep["summary"], "stopped": rep["stopped"],
           "ranked": [{k: h[k] for k in ("shot", "candidate", "url", "score", "t", "verdict")} for h in rep["ranked"]]})
    return 3 if rep["stopped"] else 0


def cmd_doctor(_a) -> int:
    def has(mod):
        try:
            __import__(mod)
            return True
        except ImportError:
            return False
    rep = {"opencv": has("cv2"), "numpy": has("numpy"), "ffmpeg": bool(shutil.which("ffmpeg")),
           "ffprobe": bool(shutil.which("ffprobe")), "curl": bool(shutil.which("curl")),
           "yt-dlp": bool(pinterest.ytdlp_command())}
    rep["can"] = {"cuts/match (local files)": rep["opencv"] and rep["numpy"], "frames": rep["ffmpeg"],
                  "search": rep["curl"],
                  "download pins (classified, measured, audio stripped)": rep["yt-dlp"] and rep["ffmpeg"] and rep["ffprobe"]}
    _emit(rep)
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="source_finder.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def matching(p):
        p.add_argument("--step", type=float, default=0.5, help="seconds between sampled candidate frames (default 0.5)")
        p.add_argument("--max-seconds", type=float, default=180.0, help="check at most this much of each candidate")
        p.add_argument("--exact", type=int, default=EXACT, help=f"inliers for an exact source (default {EXACT})")
        p.add_argument("--possible", type=int, default=POSSIBLE, help=f"inliers worth a look (default {POSSIBLE})")
        p.add_argument("--max-pins", type=int, default=80, help="download at most this many pins (default 80)")
        p.add_argument("--jobs", type=int, default=4, help="parallel pin downloads (default 4)")
        p.add_argument("--no-download", action="store_true", help="use only pins already in <work>/cand/")
        p.add_argument("--keep-audio", action="store_true",
                       help="keep each pin's own audio (default: stripped on intake, pins usually carry the creator's music)")

    p = sub.add_parser("cuts", help="scene cuts from OpenCV frame differences -> JSON")
    p.add_argument("video")
    p.add_argument("--threshold", type=float, default=27.0, help="mean HSV change (0-255) that counts as a cut (default 27)")
    p.add_argument("--min-shot", type=float, default=0.4, help="shortest shot in seconds (default 0.4)")
    p.add_argument("--scores", action="store_true", help="include the per-frame change scores")
    p.add_argument("--out", help="write the JSON here instead of stdout")
    p.set_defaults(func=cmd_cuts)

    p = sub.add_parser("frames", help="per-shot query frames (cropped) plus one full frame, with frames.json")
    p.add_argument("video")
    p.add_argument("--cuts", required=True, help="cuts.json from `cuts`, or boundaries such as 0,1.2,3.5,6")
    p.add_argument("--out", required=True, help="folder for the JPEGs and frames.json")
    p.add_argument("--crop", help="ffmpeg crop that removes burned-in text, e.g. crop=iw:ih*0.6:0:ih*0.2")
    p.add_argument("--per-shot", type=int, default=3, help="query frames per shot (default 3)")
    p.add_argument("--shots", help="only these shots, e.g. 0,3-5")
    p.add_argument("--no-full", action="store_true", help="skip the uncropped mid frame")
    p.set_defaults(func=cmd_frames)

    p = sub.add_parser("search", help="Yandex reverse image search by upload -> Pinterest pins and other leads")
    p.add_argument("images", nargs="+")
    p.add_argument("--pages", default="sites,similar", help="result pages to read (default sites,similar)")
    p.add_argument("--delay", type=float, default=4.0, help=f"seconds between Yandex calls (min {MIN_DELAY})")
    p.add_argument("--max-images", type=int, default=40, help="search at most this many images per run (default 40)")
    p.add_argument("--out", help="write the JSON here instead of stdout")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("match", help="score query frames against candidate clips (ORB + RANSAC inliers)")
    p.add_argument("queries", nargs="+", help="query images (frames of the reference shot)")
    p.add_argument("--candidates", nargs="+", required=True,
                   help="folders, video/image files, search JSON files, pin ids or Pinterest pin URLs")
    p.add_argument("--work", default="out/source_finder", help="where downloaded pins go (<work>/cand/)")
    p.add_argument("--top", type=int, default=10, help="results to print (default 10)")
    p.add_argument("--out", help="write the JSON here instead of stdout")
    matching(p)
    p.set_defaults(func=cmd_match)

    p = sub.add_parser("run", help="cuts -> frames -> search -> download -> match; writes <work>/report.json")
    p.add_argument("video")
    p.add_argument("--work", required=True, help="work folder (cuts.json, queries/, search/, cand/, report.json)")
    p.add_argument("--crop", help="ffmpeg crop for the query frames (remove captions and logos)")
    p.add_argument("--shots", help="only these shots, e.g. 0,3-5")
    p.add_argument("--threshold", type=float, default=27.0, help="cut threshold (default 27)")
    p.add_argument("--min-shot", type=float, default=0.4, help="shortest shot in seconds (default 0.4)")
    p.add_argument("--per-shot", type=int, default=3, help="query frames per shot (default 3)")
    p.add_argument("--no-full", action="store_true", help="do not also search the uncropped mid frame")
    p.add_argument("--pages", default="sites,similar", help="Yandex result pages (default sites,similar)")
    p.add_argument("--delay", type=float, default=4.0, help=f"seconds between Yandex calls (min {MIN_DELAY})")
    p.add_argument("--candidates", nargs="+",
                   help="skip the search and match every shot against these (folders, files, pin ids); offline with a folder")
    p.add_argument("--top", type=int, default=5, help="candidates kept per shot (default 5)")
    matching(p)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("doctor", help="which parts can run here (OpenCV, numpy, ffmpeg, curl, yt-dlp)")
    p.set_defaults(func=cmd_doctor)
    return ap


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    try:
        return a.func(a)
    except CaptchaError as e:
        log(f"STOPPED (captcha): {e}")
        return 3
    except SourceFinderError as e:
        log(f"error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
