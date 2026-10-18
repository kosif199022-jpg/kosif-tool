#!/usr/bin/env python3
"""Fetch a permitted reference video for inspection and measure it — جلب مرجع مسموح وقياسه.

KOSIF rule: observe the reference before implementing, never claim to have watched
what you could not open, and never rehost third-party media. This script serves the
first part and protects the last: it downloads media you are allowed to analyse into a
cache directory outside the catalog (``.kosif-cache/`` is git-ignored), then measures
it with ffmpeg — probe, contact sheet, scene cuts, dominant palette — so STYLE.md can
separate "observed" from "assumed".

  python3 fetch_reference.py <page-or-media-url> [--out DIR] [--list] [--pick N]
                             [--frames 8] [--max-mb 400] [--no-analyse] [--scene 0.3]

Inputs   a web page (media URLs are discovered in <video>/<source>, Open Graph and
         Twitter player tags, JSON-LD contentUrl and script text), a direct
         .mp4/.webm/.mov URL, or an HLS .m3u8 playlist (highest-bandwidth variant,
         separate audio rendition when the stream splits audio from video).
Refuses  encrypted or DRM streams (#EXT-X-KEY with a METHOD other than NONE),
         blob:/data: URLs, HTML answers where media was expected, files above --max-mb.
Outputs  DIR/reference.<ext>, DIR/probe.json, DIR/contact.png, DIR/cuts.json,
         DIR/palette.json, DIR/REPORT.md   (DIR defaults to ./.kosif-cache/reference/<slug>/)
Exit     0 ok · 1 nothing found or refused · 2 network or ffmpeg failure

Only fetch content you have the right to analyse or that its site permits; the result
is working material for STYLE.md, never a deliverable and never committed.
لا تجلب إلا ما يُسمح لك بتحليله؛ الناتج مادة عمل لملف STYLE.md ولا يُرفع إلى المستودع أبدًا.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html as htmlmod
import ipaddress
import socket
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) KOSIF-reference-inspector/1.0"
MEDIA_EXT = ("mp4", "webm", "mov", "m4v", "ogv", "m3u8")
MEDIA_RE = re.compile(r"""https?://[^\s"'<>\\]+?\.(?:mp4|webm|mov|m4v|ogv|m3u8)(?:\?[^\s"'<>\\]*)?""", re.I)
TAG_RE = re.compile(r"<(video|source|meta)\b([^>]*)>", re.I)
KV_RE = re.compile(r"""([a-zA-Z_:.-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""")
JSONLD_RE = re.compile(r""""(?:contentUrl|embedUrl)"\s*:\s*"([^"]+)\"""")
META_KEYS = {"og:video", "og:video:url", "og:video:secure_url", "twitter:player:stream"}
PTS_RE = re.compile(r"pts_time:\s*([\d.]+)")


class RefuseError(Exception):
    """The input is not something this tool will download (policy or format)."""


class NetError(Exception):
    """Network or decoding failure."""


# -- small helpers -------------------------------------------------------------
def log(*parts) -> None:
    print(*parts, file=sys.stderr, flush=True)


def ext_of(url: str) -> str:
    path = urllib.parse.urlsplit(url).path.lower()
    tail = path.rsplit("/", 1)[-1]
    return tail.rsplit(".", 1)[-1] if "." in tail else ""


def classify(url: str) -> str:
    e = ext_of(url)
    if e == "m3u8":
        return "hls"
    if e in MEDIA_EXT:
        return "direct"
    return "unknown"


def slug_for(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    tail = re.sub(r"[^A-Za-z0-9]+", "-", parts.path.rsplit("/", 1)[-1] or "index").strip("-")[:40]
    host = re.sub(r"[^A-Za-z0-9.]+", "-", parts.netloc).strip("-")[:40] or "local"
    return f"{host}-{tail}" if tail else host


def _validate_public_url(url: str) -> None:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password:
        raise RefuseError("only public HTTP(S) media URLs without embedded credentials are accepted")
    try:
        addrs = socket.getaddrinfo(parts.hostname, parts.port or (443 if parts.scheme == "https" else 80), type=socket.SOCK_STREAM)
    except (OSError, ValueError) as exc:
        raise NetError(f"unable to resolve public media host: {exc}") from exc
    if not addrs or any(not ipaddress.ip_address(addr[4][0]).is_global for addr in addrs):
        raise RefuseError("private, loopback, link-local or reserved media hosts are not allowed")


class _PublicRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _validate_public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _request(url: str, timeout: int = 30):
    _validate_public_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    return urllib.request.build_opener(_PublicRedirects).open(req, timeout=timeout)


def fetch_bytes(url: str, retries: int = 3, timeout: int = 30, max_bytes: int = 16 * 1048576) -> tuple[bytes, str]:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            with _request(url, timeout) as resp:
                ctype = (resp.headers.get("Content-Type") or "").lower()
                data = resp.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise RefuseError("remote page or segment exceeds the per-response byte limit")
                return data, ctype
        except (urllib.error.URLError, TimeoutError, OSError) as exc:  # pragma: no cover - network
            last = exc
            time.sleep(1.0 * (attempt + 1))
    raise NetError(f"cannot fetch {url}: {last}")


def fetch_text(url: str) -> str:
    data, _ = fetch_bytes(url)
    return data.decode("utf-8", "replace")


# -- discovery on a web page ---------------------------------------------------
def tag_attrs(raw: str) -> dict:
    return {m.group(1).lower(): (m.group(2) or m.group(3) or m.group(4) or "") for m in KV_RE.finditer(raw)}


def find_media_urls(page: str, base: str) -> list[str]:
    """Media URLs on a page: direct files first, then HLS playlists, then untyped <video> sources."""
    direct: list[str] = []
    hls: list[str] = []
    other: list[str] = []

    def add(raw: str, typed: bool) -> None:
        if not raw:
            return
        u = htmlmod.unescape(raw.strip()).replace("\\/", "/")
        if u.startswith(("blob:", "data:", "javascript:")):
            return
        u = urllib.parse.urljoin(base, u)
        if urllib.parse.urlsplit(u).scheme not in ("http", "https"):
            return
        kind = classify(u)
        bucket = direct if kind == "direct" else hls if kind == "hls" else other if typed else None
        if bucket is not None and u not in direct and u not in hls and u not in other:
            bucket.append(u)

    for m in TAG_RE.finditer(page):
        tag, attrs = m.group(1).lower(), tag_attrs(m.group(2))
        if tag in ("video", "source"):
            for key in ("src", "data-src", "data-video"):
                add(attrs.get(key, ""), typed=True)
        else:
            key = (attrs.get("property") or attrs.get("name") or "").lower()
            if key in META_KEYS:
                add(attrs.get("content", ""), typed=True)
    for m in JSONLD_RE.finditer(page):
        add(m.group(1), typed=True)
    for m in MEDIA_RE.finditer(page.replace("\\/", "/")):
        add(m.group(0), typed=False)
    return direct + hls + other


# -- HLS playlists -------------------------------------------------------------
def attr(line: str, name: str) -> str | None:
    m = re.search(r'(?:^|[,:])\s*' + re.escape(name) + r'=(?:"([^"]*)"|([^,]*))', line)
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)


def parse_master(text: str, base: str) -> tuple[list[dict], dict]:
    """Variants (bandwidth, resolution, audio group, url) and audio renditions {group: url}."""
    lines = text.splitlines()
    variants: list[dict] = []
    audio: dict = {}
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith("#")):
                j += 1
            if j < len(lines):
                variants.append({
                    "bandwidth": int(attr(line, "BANDWIDTH") or 0),
                    "resolution": attr(line, "RESOLUTION"),
                    "audio": attr(line, "AUDIO"),
                    "url": urllib.parse.urljoin(base, lines[j].strip()),
                })
        elif line.startswith("#EXT-X-MEDIA") and "TYPE=AUDIO" in line and attr(line, "URI"):
            group = attr(line, "GROUP-ID")
            if group and group not in audio:
                audio[group] = urllib.parse.urljoin(base, attr(line, "URI") or "")
    return variants, audio


def pick_variant(variants: list[dict]) -> dict | None:
    return max(variants, key=lambda v: v["bandwidth"]) if variants else None


def parse_media(text: str, base: str) -> dict:
    lines = text.splitlines()
    key_lines = [l for l in lines if l.startswith("#EXT-X-KEY") or l.startswith("#EXT-X-SESSION-KEY")]
    encrypted = any((attr(l, "METHOD") or "NONE").upper() != "NONE" for l in key_lines)
    map_line = next((l for l in lines if l.startswith("#EXT-X-MAP")), None)
    init = urllib.parse.urljoin(base, attr(map_line, "URI") or "") if map_line else None
    segments = [urllib.parse.urljoin(base, l.strip()) for l in lines if l.strip() and not l.startswith("#")]
    target = next((l for l in lines if l.startswith("#EXT-X-TARGETDURATION")), None)
    return {
        "encrypted": encrypted,
        "init": init,
        "segments": segments,
        "target_duration": float(target.split(":", 1)[1]) if target and ":" in target else None,
    }


def _download_segments(media: dict, dest: Path, max_bytes: int, workers: int = 6) -> Path:
    urls = ([media["init"]] if media["init"] else []) + media["segments"]
    total = 0
    # Sequential, bounded requests: pool.map previously downloaded the entire
    # stream before the size check, bypassing --max-mb and exhausting memory.
    with dest.open("wb") as fh:
        for i, url in enumerate(urls):
            budget = max_bytes - total
            if budget <= 0:
                raise RefuseError("stream exceeds the configured total size limit")
            data, _ctype = fetch_bytes(url, max_bytes=min(16 * 1048576, budget))
            total += len(data)
            fh.write(data)
            if i % 20 == 0:
                log(f"  segments {i + 1}/{len(urls)} · {total / 1048576:.1f} MB")
    return dest


def download_hls(url: str, dest_dir: Path, name: str, max_bytes: int, workers: int = 6) -> tuple[Path, Path | None]:
    text = fetch_text(url)
    media_url, audio_url = url, None
    if "#EXT-X-STREAM-INF" in text:
        variants, audio_groups = parse_master(text, url)
        best = pick_variant(variants)
        if not best:
            raise RefuseError("master playlist lists no playable variant")
        log(f"  variant: {best.get('resolution') or '?'} @ {best['bandwidth'] // 1000} kbps")
        media_url = best["url"]
        if best.get("audio") and best["audio"] in audio_groups:
            audio_url = audio_groups[best["audio"]]
        text = fetch_text(media_url)
    media = parse_media(text, media_url)
    if media["encrypted"]:
        raise RefuseError("the stream is encrypted (EXT-X-KEY); protected content is not supported")
    if not media["segments"]:
        raise RefuseError("the media playlist has no segments")
    video = _download_segments(media, dest_dir / f"{name}.{'mp4' if media['init'] else 'ts'}", max_bytes, workers)
    audio = None
    if audio_url:
        amedia = parse_media(fetch_text(audio_url), audio_url)
        if not amedia["encrypted"] and amedia["segments"]:
            audio = _download_segments(amedia, dest_dir / f"{name}-audio.{'mp4' if amedia['init'] else 'ts'}", max_bytes - video.stat().st_size, workers)
    return video, audio


def download_direct(url: str, dest_dir: Path, name: str, max_bytes: int) -> Path:
    try:
        resp = _request(url, timeout=60)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise NetError(f"cannot open {url}: {exc}")
    with resp:
        ctype = (resp.headers.get("Content-Type") or "").lower()
        if ctype.startswith("text/html"):
            raise RefuseError("the URL answers with an HTML page, not media; pass the page URL without --pick to discover its media")
        length = int(resp.headers.get("Content-Length") or 0)
        if length > max_bytes:
            raise RefuseError(f"file is {length / 1048576:.0f} MB, above the cap ({max_bytes // 1048576} MB)")
        ext = ext_of(url) or (ctype.split("/")[-1].split(";")[0] if ctype.startswith("video/") else "bin")
        dest = dest_dir / f"{name}.{ext}"
        total = 0
        with dest.open("wb") as fh:
            while True:
                chunk = resp.read(1 << 18)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise RefuseError(f"download exceeded the cap ({max_bytes // 1048576} MB)")
                fh.write(chunk)
    return dest


# -- measurement with ffmpeg -----------------------------------------------------
def have_ffmpeg() -> bool:
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    if not cmd or cmd[0] not in ("ffmpeg", "ffprobe"):
        raise RefuseError("only the local ffmpeg and ffprobe tools are permitted")
    if cmd[0] == "ffprobe":
        safe = cmd[:1] + ["-protocol_whitelist", "file,pipe"] + cmd[1:]
    else:
        safe = []
        for arg in cmd:
            if arg == "-i":
                safe += ["-protocol_whitelist", "file,pipe"]
            safe.append(arg)
    return subprocess.run(safe, capture_output=True, text=True, timeout=900)


def remux(video: Path, audio: Path | None, out: Path) -> Path:
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(video)]
    if audio:
        cmd += ["-i", str(audio)]
    cmd += ["-c", "copy", "-movflags", "+faststart", str(out)]
    proc = run(cmd)
    if proc.returncode != 0 or not out.exists():
        log("  remux failed, keeping the raw download:", proc.stderr.strip()[:200])
        return video
    return out


def aspect_label(w: int, h: int) -> str | None:
    if not w or not h:
        return None
    ratio = w / h
    table = {"9:16": 9 / 16, "16:9": 16 / 9, "1:1": 1.0, "4:5": 0.8, "4:3": 4 / 3, "21:9": 21 / 9}
    label, diff = min(((k, abs(ratio - v)) for k, v in table.items()), key=lambda kv: kv[1])
    return label if diff < 0.03 else f"{w}:{h}"


def probe(path: Path) -> dict:
    proc = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)])
    if proc.returncode != 0:
        raise NetError(f"ffprobe failed: {proc.stderr.strip()[:200]}")
    data = json.loads(proc.stdout or "{}")
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    audio = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    rate = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"
    num, _, den = rate.partition("/")
    fps = float(num) / float(den) if den not in ("", "0") else float(num or 0)
    duration = float(data.get("format", {}).get("duration") or video.get("duration") or 0)
    w, h = int(video.get("width") or 0), int(video.get("height") or 0)
    return {
        "duration_s": round(duration, 3),
        "fps": round(fps, 3),
        "width": w,
        "height": h,
        "aspect": aspect_label(w, h),
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name") if audio else None,
        "audio_channels": audio.get("channels") if audio else None,
        "size_bytes": int(data.get("format", {}).get("size") or path.stat().st_size),
    }


def contact_sheet(path: Path, out: Path, duration: float, frames: int = 8) -> Path | None:
    frames = max(2, frames)
    cols = 4 if frames >= 4 else frames
    rows = -(-frames // cols)
    step = max(duration / frames, 0.04) if duration else 1.0
    vf = f"fps=1/{step:.6f},scale=480:-2,tile={cols}x{rows}"
    proc = run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", vf, "-frames:v", "1", str(out)])
    return out if proc.returncode == 0 and out.exists() else None


def scene_cuts(path: Path, threshold: float = 0.3) -> list[float]:
    proc = run(["ffmpeg", "-v", "info", "-i", str(path), "-an", "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
    return [round(float(t), 3) for t in PTS_RE.findall(proc.stderr)]


def palette(path: Path, colors: int = 8) -> list[str]:
    vf = f"fps=2,scale=160:-2,palettegen=max_colors={colors + 1}:reserve_transparent=0:stats_mode=full"
    proc = subprocess.run(["ffmpeg", "-v", "error", "-protocol_whitelist", "file,pipe", "-i", str(path), "-vf", vf, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, timeout=900)
    raw = proc.stdout
    out: list[str] = []
    for i in range(0, min(len(raw), 256 * 3) - 2, 3):
        hexv = "#%02x%02x%02x" % (raw[i], raw[i + 1], raw[i + 2])
        if hexv not in out:
            out.append(hexv)
        if len(out) >= colors:
            break
    return out


def write_report(out_dir: Path, source: str, media_url: str, info: dict, cuts: list[float], colors: list[str], files: dict) -> Path:
    lines = [
        "# Reference inspection report — تقرير فحص المرجع",
        "",
        f"- Source page / الصفحة: {source}",
        f"- Media / الوسيط: {media_url}",
        f"- Fetched / جُلب: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}",
        "",
        "## Measured / المقاس",
        "",
        "| field | value |",
        "|---|---|",
    ]
    for key in ("duration_s", "fps", "width", "height", "aspect", "video_codec", "audio_codec", "audio_channels", "size_bytes"):
        if key in info:
            lines.append(f"| {key} | {info[key]} |")
    lines += ["", f"## Scene cuts / القطعات ({len(cuts)})", ""]
    lines.append(", ".join(f"{t:.2f}s" for t in cuts[:60]) if cuts else "none detected at this threshold / لم تُكتشف قطعات عند هذا الحد")
    lines += ["", "## Dominant colours / الألوان الغالبة", ""]
    lines.append(" · ".join(colors) if colors else "n/a")
    lines += ["", "## Files / الملفات", ""]
    for k, v in files.items():
        if v:
            lines.append(f"- {k}: `{v}`")
    lines += [
        "",
        "## Next / التالي",
        "",
        "Copy the measured values into STYLE.md under *Observed from the reference*; everything you infer from the contact sheet (easing, camera, type) goes under *Assumed* until you confirm it frame by frame.",
        "",
        "**بالعربية:** انقل القيم المقاسة إلى STYLE.md تحت «ما لاحظته»، وكل ما تستنتجه من لوحة الإطارات (التسارع، الكاميرا، الخط) يبقى تحت «ما افترضته» حتى تؤكده إطارًا بإطار.",
        "",
        "This material is for analysis only: never commit it, never rehost it, never cut it into the deliverable.",
        "هذه المادة للتحليل فقط: لا تُرفع إلى المستودع ولا تُعاد استضافتها ولا تُستخدم داخل الفيلم.",
    ]
    report = out_dir / "REPORT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


# -- CLI --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fetch_reference.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url", help="page URL, direct media URL or .m3u8 playlist / رابط صفحة أو وسيط أو قائمة HLS")
    p.add_argument("--out", help="output directory (default ./.kosif-cache/reference/<slug>/)")
    p.add_argument("--list", action="store_true", help="only list the media URLs found on the page / اعرض الروابط فقط")
    p.add_argument("--pick", type=int, default=1, help="which discovered URL to fetch (1-based, default 1)")
    p.add_argument("--frames", type=int, default=8, help="frames in the contact sheet (default 8)")
    p.add_argument("--scene", type=float, default=0.3, help="scene-cut threshold 0..1 (default 0.3)")
    p.add_argument("--max-mb", type=int, default=400, help="size cap in MB (default 400)")
    p.add_argument("--workers", type=int, default=6, help="parallel HLS segment downloads (default 6)")
    p.add_argument("--no-analyse", action="store_true", help="download only, skip ffmpeg measurements")
    p.add_argument("--json", action="store_true", help="print the summary as JSON on stdout")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    log("تنبيه / notice: fetch only media you may analyse; outputs are working material, never committed or rehosted.")
    url = args.url.strip()
    if url.startswith(("blob:", "data:")):
        log("refused / مرفوض: blob:/data: URLs exist only inside the browser tab; read the network panel or a page-scanning extension, then pass the real media URL")
        return 1
    max_bytes = args.max_mb * 1048576
    try:
        kind = classify(url)
        source_page = url
        media_url = url
        if kind == "unknown":
            data, ctype = fetch_bytes(url)
            if ctype.startswith("text/html") or data[:512].lower().lstrip().startswith((b"<!doctype", b"<html")):
                found = find_media_urls(data.decode("utf-8", "replace"), url)
                if not found:
                    log("no media URL found on the page; play the video and read its network requests, or pass a direct media URL")
                    return 1
                for i, u in enumerate(found, 1):
                    log(f"  [{i}] {classify(u):7} {u}")
                if args.list:
                    if args.json:
                        print(json.dumps(found, ensure_ascii=False, indent=2))
                    return 0
                if not 1 <= args.pick <= len(found):
                    log(f"--pick must be between 1 and {len(found)}")
                    return 1
                media_url = found[args.pick - 1]
                kind = classify(media_url)
                if kind == "unknown":
                    kind = "direct"
            else:
                if args.list:
                    log("--list requires a discoverable HTML page or a recognized direct media URL")
                    return 1
                kind = "direct"
        elif args.list:
            print(json.dumps([url], ensure_ascii=False) if args.json else url)
            return 0
        out_dir = Path(args.out).expanduser().resolve() if args.out else (Path.cwd() / ".kosif-cache" / "reference" / slug_for(source_page))
        out_dir.mkdir(parents=True, exist_ok=True)
        log(f"→ {kind} · {media_url}")
        audio_path: Path | None = None
        if kind == "hls":
            video_path, audio_path = download_hls(media_url, out_dir, "stream", max_bytes, args.workers)
        else:
            video_path = download_direct(media_url, out_dir, "download", max_bytes)
        files = {"download": str(video_path)}
        if audio_path:
            files["audio_download"] = str(audio_path)
        summary: dict = {"source": source_page, "media": media_url, "kind": kind, "out_dir": str(out_dir)}
        if args.no_analyse or not have_ffmpeg():
            if not have_ffmpeg():
                log("ffmpeg/ffprobe not found: downloaded only, no measurements (install ffmpeg to analyse)")
            summary["files"] = files
        else:
            reference = remux(video_path, audio_path, out_dir / "reference.mp4")
            files["reference"] = str(reference)
            info = probe(reference)
            (out_dir / "probe.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
            sheet = contact_sheet(reference, out_dir / "contact.png", info["duration_s"], args.frames)
            cuts = scene_cuts(reference, args.scene)
            colors = palette(reference)
            (out_dir / "cuts.json").write_text(json.dumps({"threshold": args.scene, "cuts_s": cuts}, indent=2), encoding="utf-8")
            (out_dir / "palette.json").write_text(json.dumps({"colors": colors}, indent=2), encoding="utf-8")
            files.update({"probe": str(out_dir / "probe.json"), "contact_sheet": str(sheet) if sheet else "", "cuts": str(out_dir / "cuts.json"), "palette": str(out_dir / "palette.json")})
            files["report"] = str(write_report(out_dir, source_page, media_url, info, cuts, colors, files))
            summary.update({"probe": info, "cuts_s": cuts, "colors": colors, "files": files})
            log(f"✓ {info['width']}×{info['height']} {info['aspect']} · {info['duration_s']} s · {info['fps']} fps · {len(cuts)} cuts · palette {' '.join(colors)}")
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print(out_dir)
        return 0
    except RefuseError as exc:
        log(f"refused / مرفوض: {exc}")
        return 1
    except NetError as exc:
        log(f"failed / فشل: {exc}")
        return 2
    except KeyboardInterrupt:  # pragma: no cover
        log("interrupted")
        return 2


if __name__ == "__main__":
    sys.exit(main())
