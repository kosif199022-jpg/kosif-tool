#!/usr/bin/env python3
"""KOSIF Stream Grabber — التقاط بث DASH وHLS للمونتاج (فكرة IDM، كود أصلي).

Idea learnt from a read-only REA+Ghidra study of IDM 6.43's IDMVMPrs64.dll (a DASH manifest parser built on
libxml2: SegmentTemplate, SegmentTimeline, SegmentList, SegmentBase, indexRange/mediaRange, per-track codecs):
read the manifest, build the full segment list per track, fetch segments in parallel with resume, then merge the
best video and audio tracks into one edit-ready file. Written from the public DASH (ISO/IEC 23009-1) and HLS
(RFC 8216) specifications; no IDM code is used.

  python3 stream_grabber.py find PAGE.html|capture.har|URL           # manifests and media links in a page or HAR export
  python3 stream_grabber.py list MANIFEST_URL_OR_FILE                  # tracks with labels: 1080p · avc1 · 4.50 Mbps · video only
  python3 stream_grabber.py grab MANIFEST_URL -o out.mp4 [--max-height 1080] [--prefer edit|quality] [--threads 8]
                                     [--referer URL]                    # lossless merge to MP4 (MKV for VP8/Vorbis) + .vtt subtitles

Refuses encrypted or DRM-protected streams (HLS #EXT-X-KEY other than NONE, DASH ContentProtection) and live
streams without an end. Python 3.8+ stdlib; ffmpeg for the final merge.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA = {"User-Agent": "KOSIF-StreamGrabber/1.0"}
EXTRA_HEADERS = {}   # set by --referer / --header (e.g. a Referer the site requires); never cookies you do not own
TAIL_PROBE = 4


class Refused(Exception):
    pass


# ------------------------------------------------------------------ fetch
def fetch_text(src: str) -> tuple:
    if re.match(r"^https?://", src):
        with urllib.request.urlopen(urllib.request.Request(src, headers={**UA, **EXTRA_HEADERS}), timeout=60) as r:
            return r.read().decode("utf-8", "replace"), r.geturl()
    p = Path(src).resolve()
    return p.read_text(encoding="utf-8", errors="replace"), p.as_uri()


_FULL = {}
_LOCK = threading.Lock()


def fetch_bytes(url: str, byterange=None, timeout=90) -> bytes:
    """Fetch a URL or a byte range of it. Servers that ignore Range (HTTP 200) are read once, cached and sliced."""
    hdr = {**UA, **EXTRA_HEADERS}
    if byterange:
        hdr["Range"] = f"bytes={byterange[0]}-{byterange[1]}"
        with _LOCK:
            full = _FULL.get(url)
        if full is not None:
            return full[byterange[0]:byterange[1] + 1]
    if url.startswith("file://"):
        data = Path(urllib.request.url2pathname(urllib.parse.urlsplit(url).path)).read_bytes()
        return data[byterange[0]:byterange[1] + 1] if byterange else data
    with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=timeout) as r:
        body = r.read()
        status = getattr(r, "status", 200)
    if byterange and status == 200:
        with _LOCK:
            _FULL[url] = body
        return body[byterange[0]:byterange[1] + 1]
    return body


def join(base: str, ref: str) -> str:
    return urllib.parse.urljoin(base, ref)


# ------------------------------------------------------------------ DASH
def iso_dur(s: str) -> float:
    m = re.match(r"^P(?:(\d+(?:\.\d+)?)D)?(?:T(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?)?$", s or "")
    if not m:
        return 0.0
    d, h, mi, se = (float(x) if x else 0.0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def tpl(t: str, rep_id: str, bw: str, number=None, time=None) -> str:
    def sub(m):
        name, fmt = m.group(1), m.group(2)
        val = {"RepresentationID": rep_id, "Bandwidth": bw, "Number": number, "Time": time}.get(name)
        if name == "" or val is None:
            return "$" if name == "" else m.group(0)
        if fmt:
            return ("%" + fmt[1:]) % int(val)
        return str(val)
    return re.sub(r"\$(RepresentationID|Bandwidth|Number|Time|)(%0\d+d)?\$", sub, t)


def strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return root


def first(*args):
    *els, tag = args
    for el in els:
        x = el.find(tag)
        if x is not None:
            return x
    return None


def parse_br(s):
    a, b = s.split("-")
    return int(a), int(b)


def dash_tracks(text: str, url: str) -> list:
    root = strip_ns(ET.fromstring(text))
    if root.get("type", "static") == "dynamic":
        raise Refused("live DASH (type=dynamic) is not supported")
    total = iso_dur(root.get("mediaPresentationDuration", ""))
    base = url
    b = root.find("BaseURL")
    if b is not None and b.text:
        base = join(base, b.text.strip())
    tracks = []
    for period in root.findall("Period"):
        pbase = join(base, period.find("BaseURL").text.strip()) if period.find("BaseURL") is not None else base
        pdur = iso_dur(period.get("duration", "")) or total
        for aset in period.findall("AdaptationSet"):
            if aset.find("ContentProtection") is not None:
                raise Refused("DRM-protected DASH (ContentProtection) — refused")
            abase = join(pbase, aset.find("BaseURL").text.strip()) if aset.find("BaseURL") is not None else pbase
            for rep in aset.findall("Representation"):
                if rep.find("ContentProtection") is not None:
                    raise Refused("DRM-protected DASH (ContentProtection) — refused")
                rbase = join(abase, rep.find("BaseURL").text.strip()) if rep.find("BaseURL") is not None else abase
                mime = rep.get("mimeType") or aset.get("mimeType") or ""
                ctype = aset.get("contentType") or mime.split("/")[0] or ("video" if rep.get("width") else "audio")
                if ctype == "application" or "vtt" in mime or "ttml" in mime:
                    ctype = "text"
                rid, bw = rep.get("id", ""), rep.get("bandwidth", "0")
                segs = []  # list of (url, byterange or None); first may be init
                # ElementTree elements without children are falsy, so never chain them with `or`
                st = first(rep, aset, period, "SegmentTemplate")
                sl = first(rep, aset, period, "SegmentList")
                if st is not None:
                    ts = int(st.get("timescale", "1"))
                    start = int(st.get("startNumber", "1"))
                    if st.get("initialization"):
                        segs.append((join(rbase, tpl(st.get("initialization"), rid, bw)), None, "init"))
                    media = st.get("media", "")
                    tl = st.find("SegmentTimeline")
                    if tl is not None:
                        t, n = 0, start
                        ss = tl.findall("S")
                        for k, s_ in enumerate(ss):
                            if s_.get("t") is not None:
                                t = int(s_.get("t"))
                            d, r = int(s_.get("d")), int(s_.get("r", "0"))
                            if r < 0:
                                nxt = int(ss[k + 1].get("t")) if k + 1 < len(ss) and ss[k + 1].get("t") else int(pdur * ts)
                                r = max(0, math.ceil((nxt - t) / d) - 1)
                            for _ in range(r + 1):
                                segs.append((join(rbase, tpl(media, rid, bw, n, t)), None, "media"))
                                t += d
                                n += 1
                    else:
                        d = int(st.get("duration", "0"))
                        if not d or not pdur:
                            raise Refused("SegmentTemplate without duration or timeline")
                        # the declared duration is nominal: real segments can be longer (GOP-aligned) or one more exists,
                        # so list a few extra numbers and let the downloader stop at the first missing tail segment
                        count = math.ceil(pdur * ts / d)
                        for k in range(count + TAIL_PROBE):
                            segs.append((join(rbase, tpl(media, rid, bw, start + k, k * d)), None, "media" if k < count else "tail"))
                elif sl is not None:
                    init = sl.find("Initialization")
                    if init is not None:
                        segs.append((join(rbase, init.get("sourceURL", "")) if init.get("sourceURL") else rbase,
                                     parse_br(init.get("range")) if init.get("range") else None, "init"))
                    for su in sl.findall("SegmentURL"):
                        segs.append((join(rbase, su.get("media")) if su.get("media") else rbase,
                                     parse_br(su.get("mediaRange")) if su.get("mediaRange") else None, "media"))
                else:  # SegmentBase or plain BaseURL: one self-indexed file (indexRange is the sidx; the whole file plays)
                    segs.append((rbase, None, "single"))
                tracks.append({"kind": "dash", "type": ctype, "id": rid, "bandwidth": int(bw or 0), "codecs": rep.get("codecs") or aset.get("codecs") or "",
                               "width": int(rep.get("width") or aset.get("width") or 0), "height": int(rep.get("height") or aset.get("height") or 0),
                               "audio_rate": rep.get("audioSamplingRate") or aset.get("audioSamplingRate") or "", "mime": mime, "segments": segs})
    return tracks


# ------------------------------------------------------------------ HLS
def attrs(s: str) -> dict:
    return {k: v.strip('"') for k, v in re.findall(r'([A-Z0-9-]+)=("[^"]*"|[^,]*)', s)}


def hls_media(text: str, url: str) -> list:
    if "#EXT-X-ENDLIST" not in text:
        raise Refused("live HLS playlist (no #EXT-X-ENDLIST) is not supported")
    segs, br_next, last_end = [], None, {}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#EXT-X-KEY"):
            m = attrs(line[len("#EXT-X-KEY:"):])
            if m.get("METHOD", "NONE") != "NONE":
                raise Refused("encrypted HLS (#EXT-X-KEY METHOD=%s) — refused" % m.get("METHOD"))
        elif line.startswith("#EXT-X-MAP"):
            m = attrs(line[len("#EXT-X-MAP:"):])
            br = None
            if m.get("BYTERANGE"):
                n, _, o = m["BYTERANGE"].partition("@")
                br = (int(o or 0), int(o or 0) + int(n) - 1)
            segs.append((join(url, m["URI"]), br, "init"))
        elif line.startswith("#EXT-X-BYTERANGE"):
            n, _, o = line.split(":", 1)[1].partition("@")
            br_next = (int(n), int(o) if o else None)
        elif line and not line.startswith("#"):
            u = join(url, line)
            br = None
            if br_next:
                off = br_next[1] if br_next[1] is not None else last_end.get(u, 0)
                br = (off, off + br_next[0] - 1)
                last_end[u] = off + br_next[0]
                br_next = None
            segs.append((u, br, "media"))
    return segs


def hls_tracks(text: str, url: str) -> list:
    if "#EXT-X-STREAM-INF" not in text:
        return [{"kind": "hls", "type": "muxed", "id": "0", "bandwidth": 0, "codecs": "", "width": 0, "height": 0, "audio_rate": "",
                 "mime": "", "segments": hls_media(text, url)}]
    tracks, lines, audio_groups, subs = [], text.splitlines(), {}, []
    for line in lines:
        if line.startswith("#EXT-X-MEDIA:"):
            m = attrs(line[len("#EXT-X-MEDIA:"):])
            if m.get("TYPE") == "AUDIO" and m.get("URI"):
                audio_groups.setdefault(m.get("GROUP-ID"), []).append(m)
            if m.get("TYPE") == "SUBTITLES" and m.get("URI"):
                subs.append(m)
        if line.startswith("#EXT-X-SESSION-KEY"):
            m = attrs(line.split(":", 1)[1])
            if m.get("METHOD", "NONE") != "NONE":
                raise Refused("encrypted HLS (session key) — refused")
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF:"):
            m = attrs(line[len("#EXT-X-STREAM-INF:"):])
            uri = next((l.strip() for l in lines[i + 1:] if l.strip() and not l.startswith("#")), None)
            if not uri:
                continue
            w, h = (int(x) for x in m["RESOLUTION"].split("x")) if m.get("RESOLUTION") else (0, 0)
            tracks.append({"kind": "hls", "type": "video" if m.get("AUDIO") in audio_groups else "muxed", "id": uri, "bandwidth": int(m.get("BANDWIDTH", 0)),
                           "codecs": m.get("CODECS", ""), "width": w, "height": h, "audio_rate": "", "mime": "", "playlist": join(url, uri),
                           "audio_group": m.get("AUDIO")})
    for s in subs:
        tracks.append({"kind": "hls", "type": "text", "id": s.get("NAME", "sub"), "bandwidth": 0, "codecs": "", "width": 0, "height": 0,
                       "audio_rate": "", "mime": "text/vtt", "playlist": join(url, s["URI"]), "language": s.get("LANGUAGE", "")})
    for gid, items in audio_groups.items():
        for a in items:
            tracks.append({"kind": "hls", "type": "audio", "id": a.get("NAME", gid), "bandwidth": 0, "codecs": "", "width": 0, "height": 0,
                           "audio_rate": "", "mime": "", "playlist": join(url, a["URI"]), "group": gid, "default": a.get("DEFAULT") == "YES"})
    return tracks


# ------------------------------------------------------------------ public API
def list_tracks(src: str) -> list:
    text, url = fetch_text(src)
    if text.lstrip().startswith("#EXTM3U"):
        tr = hls_tracks(text, url)
        for t in tr:
            if "playlist" in t and "segments" not in t:
                t["segments"] = hls_media(fetch_text(t["playlist"])[0], t["playlist"])
        return tr
    if "<MPD" in text[:2000]:
        return dash_tracks(text, url)
    raise Refused("not a DASH (.mpd) or HLS (.m3u8) manifest")


EDIT_FRIENDLY = ("avc1", "avc3", "h264", "mp4a", "aac")


def label(t) -> str:
    """Human quality label in the spirit of download managers: 1080p · avc1 · 4.5 Mbps · video only."""
    parts = []
    if t.get("height"):
        parts.append(f"{t['height']}p")
    if t.get("codecs"):
        parts.append(t["codecs"].split(",")[0].split(".")[0])
    if t.get("bandwidth"):
        parts.append(f"{t['bandwidth'] / 1e6:.2f} Mbps")
    parts.append({"video": "video only", "audio": "audio only", "muxed": "video+audio", "text": "subtitles"}.get(t["type"], t["type"]))
    if t.get("language"):
        parts.append(t["language"])
    return " · ".join(parts)


def pick(tracks, max_height=None, prefer="edit"):
    """Best video under max_height and its audio. prefer='edit' favours H.264/AAC (lossless merge, every editor
    opens it) over AV1/VP9/HEVC at the same height; prefer='quality' takes the highest bandwidth."""
    def ok(t):
        return not max_height or not t["height"] or t["height"] <= max_height

    def friendly(t):
        c = (t.get("codecs") or "").lower()
        return 1 if (not c or any(c.startswith(x) or ("," + x) in c for x in EDIT_FRIENDLY)) else 0
    key_v = (lambda t: (t["height"], friendly(t), t["bandwidth"])) if prefer == "edit" else (lambda t: (t["height"], t["bandwidth"]))
    vids = sorted([t for t in tracks if t["type"] in ("video", "muxed") and ok(t)], key=key_v)
    auds = sorted([t for t in tracks if t["type"] == "audio"], key=lambda t: (t.get("default", False), friendly(t) if prefer == "edit" else 0, t["bandwidth"]))
    v = vids[-1] if vids else None
    a = None
    if v and v.get("audio_group"):
        a = next((t for t in auds[::-1] if t.get("group") == v["audio_group"]), None)
    elif auds and (not v or v["type"] != "muxed"):
        a = auds[-1]
    return v, a


def download_track(track, work: Path, threads=8, retries=3) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    segs = track["segments"]
    errors = []

    failed = {}

    def one(k):
        u, br, kind = segs[k]
        dst = work / f"{k:06d}.seg"
        if dst.exists() and (work / f"{k:06d}.ok").exists():
            return
        for attempt in range(retries):
            try:
                data = fetch_bytes(u, br)
                if br and len(data) != br[1] - br[0] + 1:
                    raise IOError(f"short range {len(data)}")
                dst.write_bytes(data)
                (work / f"{k:06d}.ok").write_text(hashlib.sha256(data).hexdigest())
                return
            except urllib.error.HTTPError as exc:
                if exc.code in (404, 410) and segs[k][2] in ("media", "tail"):
                    failed[k] = exc.code
                    return
                if attempt == retries - 1:
                    errors.append(f"segment {k}: {exc}")
            except Exception as exc:  # noqa: BLE001
                if attempt == retries - 1:
                    errors.append(f"segment {k}: {exc}")
    with cf.ThreadPoolExecutor(max_workers=threads) as ex:
        list(ex.map(one, range(len(segs))))
    if errors:
        raise IOError(f"{len(errors)} segments failed (rerun to resume): {errors[:3]}")
    keep = len(segs)
    if failed:
        first_missing = min(failed)
        probed_tail = any(s[2] == "tail" for s in segs)
        # tolerated only as a contiguous tail of a duration-based template; a hole in the middle is an error
        if not probed_tail or any((work / f"{k:06d}.ok").exists() for k in range(first_missing, len(segs))):
            raise IOError(f"missing segments {sorted(failed)[:5]} inside the stream")
        keep = first_missing
    else:
        tail = [k for k, s in enumerate(segs) if s[2] == "tail"]
        if tail:
            raise IOError("all probe segments exist: the manifest under-declares its length; refusing to guess further")
    if not any(segs[k][2] in ("media", "tail", "single") for k in range(keep)):
        raise IOError("no media segment downloaded")
    out = work / "track.bin"
    track["downloaded_segments"] = keep
    with out.open("wb") as o:
        for k in range(keep):
            o.write((work / f"{k:06d}.seg").read_bytes())
    return out


def merge_vtt(chunks) -> bytes:
    """Join WebVTT segments: one WEBVTT header, each segment's own header block dropped, cues kept in order."""
    out = ["WEBVTT", ""]
    for raw in chunks:
        text = raw.decode("utf-8-sig", "replace").replace("\r\n", "\n")
        blocks = text.split("\n\n")
        if blocks and blocks[0].lstrip().startswith("WEBVTT"):
            blocks = blocks[1:]
        out += [b.strip("\n") for b in blocks if b.strip()]
    return ("\n\n".join(out[:1] + out[2:]) + "\n").replace("WEBVTT\n\n", "WEBVTT\n\n", 1).encode("utf-8")


def container_for(v, a) -> str:
    """MP4 when every codec is MP4-friendly, otherwise MKV — a lossless remux either way (no re-encode)."""
    codecs = ",".join(((v or {}).get("codecs") or "", (a or {}).get("codecs") or "")).lower()
    bad = any(x in codecs for x in ("vp8", "vorbis", "theora"))
    return ".mkv" if bad else ".mp4"


def grab(src: str, out: Path, max_height=None, threads=8, work: Path = None, prefer="edit", subtitles=True) -> dict:
    tracks = list_tracks(src)
    v, a = pick(tracks, max_height, prefer)
    if not v and not a:
        raise Refused("no playable track")
    work = work or out.with_name(out.stem + ".grab")
    files = {}
    for name, t in (("video", v), ("audio", a)):
        if t:
            files[name] = download_track(t, work / name, threads)
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg needed for the final merge")
    ext = container_for(v, a)
    if out.suffix.lower() != ext and ext == ".mkv":
        out = out.with_suffix(ext)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files.values():
        cmd += ["-i", str(f)]
    maps = []
    for i, name in enumerate(files):
        maps += ["-map", f"{i}:v:0?" if name == "video" else f"{i}:a:0?"]
    if "video" in files and not a:
        maps += ["-map", "0:a:0?"]
    cmd += maps + ["-c", "copy"] + (["-movflags", "+faststart"] if out.suffix == ".mp4" else []) + [str(out)]
    rc = subprocess.run(cmd, capture_output=True, text=True)
    if rc.returncode:
        raise SystemExit("merge failed: " + rc.stderr[-400:])
    subs = []
    if subtitles:
        for t in [x for x in tracks if x["type"] == "text"]:
            try:
                if t.get("segments") is None and t.get("playlist"):
                    t["segments"] = hls_media(fetch_text(t["playlist"])[0], t["playlist"])
                body = merge_vtt([fetch_bytes(u, br) for u, br, _k in (t.get("segments") or [])])
                dst = out.with_name(f"{out.stem}.{re.sub(r'[^A-Za-z0-9_-]+', '_', t.get('language') or t['id'])[:20]}.vtt")
                dst.write_bytes(body)
                subs.append(str(dst))
            except Exception as exc:  # noqa: BLE001
                subs.append(f"failed {t['id']}: {exc}")
    pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height", "-of", "json", str(out)],
                        capture_output=True, text=True)
    info = json.loads(pr.stdout or "{}")
    return {"output": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "container": out.suffix, "remux": "lossless (-c copy)",
            "video": {**{k: v[k] for k in ("id", "codecs", "width", "height", "bandwidth")}, "label": label(v)} if v else None,
            "audio": {**{k: a[k] for k in ("id", "codecs", "bandwidth")}, "label": label(a)} if a else None,
            "segments": {k: t.get("downloaded_segments", len(t["segments"])) for k, t in (("video", v), ("audio", a)) if t},
            "subtitles": subs, "probe": info}


MEDIA_URL = re.compile(r"""https?://[^\s"'<>\\]+?(?:\.(?:m3u8|mpd)(?:\?[^\s"'<>\\]*)?|\.(?:mp4|m4v|webm|mov|mkv|m4a|mp3|aac|wav|flac|ogg)(?:\?[^\s"'<>\\]*)?)""", re.I)


def find_streams(src: str) -> list:
    """Find stream manifests and direct media links in a saved page, a HAR export or a URL (the page's own text
    only; nothing is executed). Like a download manager's 'grab this video' panel, without network sniffing."""
    text = Path(src).read_text(encoding="utf-8", errors="replace") if Path(src).exists() else fetch_text(src)[0]
    found = []
    if text.lstrip().startswith("{") and '"log"' in text[:200]:
        try:
            har = json.loads(text)
            for e in har.get("log", {}).get("entries", []):
                u = e.get("request", {}).get("url", "")
                ct = next((h.get("value", "") for h in e.get("response", {}).get("headers", []) if h.get("name", "").lower() == "content-type"), "")
                if MEDIA_URL.match(u) or any(x in ct for x in ("mpegurl", "dash+xml", "video/", "audio/")):
                    found.append((u, ct or "har"))
        except ValueError:
            pass
    for m in MEDIA_URL.finditer(text.replace("\\/", "/")):   # JSON-escaped slashes in inline player data
        found.append((m.group(0), "text"))
    seen, out = set(), []
    for u, how in found:
        if u in seen:
            continue
        seen.add(u)
        kind = "manifest" if re.search(r"\.(m3u8|mpd)(\?|$)", u, re.I) else "file"
        out.append({"url": u, "kind": kind, "found_by": how})
    out.sort(key=lambda x: (x["kind"] != "manifest", x["url"]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--referer", help="Referer header some hosts require for their own player")
    ap.add_argument("--header", action="append", default=[], help="extra 'Name: value' header (repeatable); never someone else's cookies")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find"); f.add_argument("src", help="saved page .html, browser HAR export, or a URL")
    l = sub.add_parser("list"); l.add_argument("src")
    g = sub.add_parser("grab"); g.add_argument("src"); g.add_argument("-o", "--out", type=Path, required=True)
    g.add_argument("--max-height", type=int); g.add_argument("--threads", type=int, default=8); g.add_argument("--work", type=Path)
    g.add_argument("--prefer", choices=["edit", "quality"], default="edit"); g.add_argument("--no-subtitles", action="store_true")
    a = ap.parse_args(argv)
    if a.referer:
        EXTRA_HEADERS["Referer"] = a.referer
    for h in a.header:
        k, _, v = h.partition(":")
        if k.strip().lower() == "cookie":
            print("refused: pass cookies only through yt-dlp --cookies with your own browser profile", file=sys.stderr)
            return 3
        EXTRA_HEADERS[k.strip()] = v.strip()
    try:
        if a.cmd == "find":
            for x in find_streams(a.src):
                print(f"{x['kind']:<9} {x['url']}")
            return 0
        if a.cmd == "list":
            for t in list_tracks(a.src):
                print(f"{t['type']:<6} {label(t):<40} id={t['id'][:24]:<24} segments={len(t.get('segments') or [])}")
            return 0
        print(json.dumps(grab(a.src, a.out, a.max_height, a.threads, a.work, a.prefer, not a.no_subtitles), ensure_ascii=False, indent=1))
        return 0
    except Refused as exc:
        print("refused: " + str(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
