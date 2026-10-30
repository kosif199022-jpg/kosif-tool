#!/usr/bin/env python3
"""Download videos from links for montage — تحميل فيديوهات من الروابط للمونتاج.

A Linux/macOS port of the ideas in the owner's "Cinema C V32" a-Shell script
(yt-dlp wrapper): format fallback chain, browser-impersonation retry, cookies
file, audio-only, concurrent fragments, and an edit-safe H.264/AAC MP4.
Only the standard library is imported; yt-dlp and ffmpeg are used if present.

  python3 fetch_video.py URL [URL ...] [-o DIR] [--quality 1080|720|best|audio]
  python3 fetch_video.py --urls links.txt -o clips/
  python3 fetch_video.py URL --cookies cookies.txt      # private/age-gated, your own account
  python3 fetch_video.py URL --cookies-from-browser chrome   # same, read from your local browser
  python3 fetch_video.py URL --safe                     # also build an edit-safe MP4 copy
  python3 fetch_video.py URL --strip-audio              # drop the clip's own audio on intake (Quran/dignified jobs);
                                                        # a clip whose audio cannot be removed is not kept (FAIL)
  python3 fetch_video.py PIN_URL [PIN_URL ...] --classify   # Pinterest: say what each pin is, download nothing
  python3 fetch_video.py --doctor | --update

Writes <DIR>/<title> [<id>].<ext> and a manifest.json (url, file, duration, title, uploader,
license field if the site exposes one). Use only content you have the right to use.

Pinterest pin links (pinterest.<tld>/pin/<id>, pin.it/<code>) go through the shared helper _pinterest.py
(source_finder.py uses it too): one yt-dlp -J call classifies the pin first (video, image, gif, embedded
YouTube, other embed, deleted, CDN-refused, blocked), only a video pin is downloaded, into a temp folder,
its real size is measured with ffprobe (Pinterest's "1080x1920" label is the display size; files are 720p
at most), and <DIR>/pinterest-<id>.pin.json keeps the verdict and a credit record (the same name for a pin.it
link and a full link). Pins are never retried. With --quality audio a pin is classified the same way and only a
video pin's audio is fetched, in one yt-dlp attempt (no .pin.json then).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import urllib.parse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pinterest as pinterest  # noqa: E402 - the shared Pinterest pin helper (source_finder.py uses it too)
import _cobalt_provider as cobalt  # noqa: E402 - internal authorized gateway, opt-in only


def find_ytdlp(install: bool = True) -> list[str] | None:
    """yt-dlp as a command; in a cloud session a missing yt-dlp (and curl_cffi) is pip-installed once, quietly."""
    cmd = pinterest.ytdlp_command()
    if cmd or not install:
        return cmd
    try:
        from _deps import ensure  # noqa: PLC0415
        ensure(["yt_dlp", "yt_dlp_ejs", "curl_cffi"], quiet=False)
    except Exception:  # noqa: BLE001 — install is best effort; the message below covers the rest
        pass
    return pinterest.ytdlp_command()


def blocked(err: str, url: str) -> dict | None:
    """When a site refuses the cloud machine (bot check, IP block), say so plainly with the two honest ways forward."""
    try:
        from _deps import blocked_hint, drm_hint, is_blocked, is_drm  # noqa: PLC0415
    except ImportError:
        return None
    if is_drm(err):   # a publisher lock, not a cloud block: no cookies or own-computer route either
        return {"drm": True, "hint": drm_hint(url)}
    return {"blocked": True, "hint": blocked_hint(url)} if is_blocked(err) else None


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


QUALITY_ALIASES = {"4k": "2160", "2k": "1440", "uhd": "2160", "fhd": "1080", "hd": "720"}


def norm_quality(q: str) -> str:
    q = (q or "").strip().lower()
    q = QUALITY_ALIASES.get(q, q)
    if q.endswith("p"):
        q = q[:-1]
    if q in ("best", "audio") or q.isdigit():
        return q
    raise argparse.ArgumentTypeError(f"--quality must be best, audio, a height such as 1080 or 1080p, or 4k (got {q!r})")


def is_url(u: str) -> bool:
    try:
        parts = urllib.parse.urlsplit(u)
    except ValueError:
        return False
    return parts.scheme in ("http", "https") and bool(parts.netloc)


def selector(quality: str) -> tuple[str, list[str]]:
    """Cinema V34-aware portrait quality preferences and iOS-friendly formats.

    yt-dlp's [height<=1080] rejects portrait 1080x1920. Its -S res:1080
    evaluates the shorter side, then prefers H.264 and AAC for Photos.
    Sorting is a preference, not a guarantee of a strict size cap.
    """
    if quality == "audio":
        return "ba/b", ["-x", "--audio-format", "m4a"]
    ios_video = "[vcodec~='^(avc|h264|hvc|hev|h265|bytevc1)']"
    ios_audio = "[acodec~='^(mp4a|aac)']"
    if quality != "best" and int(quality) > 1080:
        fmt = "bv*+ba/b/best"
    else:
        fmt = f"bv*{ios_video}+ba{ios_audio}/bv*+ba/b{ios_video}/b[ext=mp4]/best"
    sorting = "res,fps,vcodec:h264,acodec:aac" if quality == "best" else (
        f"res:{quality},fps,vcodec:h264,acodec:aac"
    )
    return fmt, ["-S", sorting, "--merge-output-format", "mp4"]


def impersonation(ytdlp: list[str]) -> str | None:
    out = sh(ytdlp + ["--list-impersonate-targets"]).stdout
    for want in ("Safari", "Chrome"):
        for line in out.splitlines():
            if line.startswith(want) and "unavailable" not in line.lower():
                return want.lower()
    return None


def attempt(ytdlp, url, out_dir, fmt, extra, cookies, imp, connections, proxy, browser=None):
    cmd = ytdlp + ["--no-playlist", "--continue", "--newline", "--no-part", "--no-progress",
                   "--concurrent-fragments", str(connections), "--retries", "10",
                   "--fragment-retries", "10", "--extractor-retries", "3", "--socket-timeout", "30",
                   "-f", fmt, "-o", str(out_dir / "%(title).120B [%(id)s].%(ext)s"),
                   "--print", "after_move:filepath", "--write-info-json", "--no-clean-info-json"]
    cmd += extra
    if shutil.which("node"):  # YouTube needs a JS runtime for full-quality formats
        cmd += ["--js-runtimes", "node"]
    if cookies:
        cmd += ["--cookies", cookies]
    if browser:  # read the user's own login from a local browser; the cookies never leave this machine
        cmd += ["--cookies-from-browser", browser]
    if imp:
        cmd += ["--impersonate", imp]
    if proxy:
        cmd += ["--proxy", proxy]
    cmd += ["--", url]  # "--" stops a URL that starts with "-" from being read as a yt-dlp option
    p = sh(cmd)
    paths = [l for l in p.stdout.splitlines() if l.strip() and Path(l.strip()).is_file()]
    return (paths[-1].strip() if p.returncode == 0 and paths else None), p.stderr[-600:]


def edit_safe(src: Path) -> Path | None:
    """Cinema V34 Photos-safe MP4: lossless remux when possible; encode only if needed.

    Verify a video frame decodes before delivery. Keep the source untouched.
    A bad or interrupted attempt never leaves a file labelled .safe.mp4.
    """
    if not shutil.which("ffmpeg"):
        return None
    dst = src.with_name(src.stem + ".safe.mp4")
    temp = dst.with_name(dst.stem + ".pending.mp4")
    formats = None
    if shutil.which("ffprobe"):
        try:
            p = sh(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(src)], timeout=35)
            if p.returncode == 0:
                formats = json.loads(p.stdout).get("streams", [])
        except (ValueError, OSError, subprocess.TimeoutExpired):
            pass
    video = next((s for s in formats or [] if s.get("codec_type") == "video"), {})
    audio = next((s for s in formats or [] if s.get("codec_type") == "audio"), {})
    compatible = (
        (video.get("codec_name") == "h264" and video.get("pix_fmt") in ("yuv420p", "yuvj420p"))
        or (video.get("codec_name") == "hevc" and video.get("pix_fmt") in ("yuv420p", "yuv420p10le"))
    ) and (not audio or audio.get("codec_name") == "aac")
    base = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(src),
            "-map", "0:v:0", "-map", "0:a:0?", "-sn", "-dn"]
    trials = []
    if compatible:
        tag = "hvc1" if video["codec_name"] == "hevc" else "avc1"
        trials.append(base + ["-c:v", "copy", "-tag:v", tag, "-c:a", "copy",
                              "-movflags", "+faststart", str(temp)])
    # Fallback for unreadable/unsupported codecs. No hidden quality loss when a
    # stream copy succeeds; iPhone a-Shell's hardware encoder isn't required.
    trials.append(base + ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                          "-movflags", "+faststart", str(temp)])
    for command in trials:
        temp.unlink(missing_ok=True)
        try:
            p = sh(command, timeout=300)
            if p.returncode or not temp.is_file() or temp.stat().st_size <= 0:
                continue
            check = sh(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                        "-i", str(temp), "-map", "0:v:0", "-frames:v", "1",
                        "-f", "null", "-"], timeout=40)
            if check.returncode:
                continue
            temp.replace(dst)
            return dst
        except (OSError, subprocess.TimeoutExpired):
            continue
        finally:
            temp.unlink(missing_ok=True)
    return None


probe = pinterest.probe_media  # ffprobe: duration, width, height, fps, vcodec, acodec ({} without ffprobe)


def _flag(a, name: str) -> bool:
    return getattr(a, name, False) is True


def intake_audio(path: Path, a, rec: dict, fresh: bool = True) -> dict:
    """--strip-audio: drop the clip's own audio in place (video copied, no re-encode) and say so in the record.

    Fails closed, as the Pinterest path does: when the audio cannot be removed the clip is not handed out
    (file None, an error, exit 1, no .safe.mp4). A file this run downloaded (`fresh`) is deleted, so its music
    cannot leak into the edit; a file an earlier run left in the folder is not used and not deleted."""
    if not _flag(a, "strip_audio") or a.quality == "audio":
        return rec
    if not rec.get("acodec") and shutil.which("ffprobe"):
        rec["audio"] = "none (the file has no audio stream)"
        return rec
    ok, why = pinterest.remove_audio(path)
    if ok:
        rec.update(audio="stripped", acodec=None)
        return rec
    if fresh:
        Path(path).unlink(missing_ok=True)
        kept = "the download was deleted, nothing kept"
    else:
        kept = f"the earlier download {Path(path).name} was left alone but not used"
    rec.update(file=None, audio=f"NOT stripped: {why}",
               error=f"--strip-audio: could not strip the clip's own audio ({why}); {kept}, so its music cannot leak "
                     "into the edit (install ffmpeg, or drop --strip-audio to keep the audio on purpose)")
    return rec


def _pin_extra(a) -> list:
    """The user's own cookies and proxy, passed to yt-dlp for pins as for every other link."""
    extra = []
    if a.cookies:
        extra += ["--cookies", a.cookies]
    if getattr(a, "cookies_from_browser", None):
        extra += ["--cookies-from-browser", a.cookies_from_browser]
    if a.proxy:
        extra += ["--proxy", a.proxy]
    return extra


def classify_pins(urls, a, ytdlp) -> int:
    """--classify: one line per link (kind, pin id, reason); nothing is downloaded or written. Exit 1 on any error."""
    code = 0
    for u in urls:
        if not pinterest.is_pin_link(u):
            print(f"{'skipped':<11} {u}  not a Pinterest pin link (--classify only classifies pins)")
            code = 1
            continue
        rec = pinterest.classify_link(u, ytdlp, _pin_extra(a)) if ytdlp else \
            {"pin_id": pinterest.pin_id(u), "kind": "error", "reason": "yt-dlp not installed: pip install yt-dlp"}
        print(pinterest.summary_line(rec))
        code = 1 if rec.get("kind") == "error" else code
    return code


def _pin_row(url: str, rec: dict) -> dict:
    """The manifest row of a pin: the helper's verdict, credit and measurements; an error when no file came of it."""
    out = {"url": url, "file": rec.get("file"), "via": "pinterest", "pin_id": rec.get("pin_id"), "kind": rec.get("kind"),
           "reason": rec.get("reason"), "retry": rec.get("retry"), "license": pinterest.LICENCE, "credit": rec.get("credit"),
           **{k: rec[k] for k in ("width", "height", "duration", "fps", "vcodec", "acodec", "audio", "label_size",
                                   "size_note", "resolution_verified", "image_url", "embed_url", "sidecar") if k in rec}}
    if not out["file"]:
        out["error"] = rec.get("reason") or "pin not downloaded"
        if rec.get("kind") == "youtube":
            out.update(blocked(rec["reason"], rec.get("embed_url") or "youtube") or {})
    return out


def pin_download(url: str, a, ytdlp) -> dict:
    """A Pinterest pin through the shared helper: classified first, downloaded only when it is a video, never retried.
    Named pinterest-<id> after a pin.it link is followed, so both link forms share one file and one sidecar."""
    rec = pinterest.fetch(url, a.out, prefix="pinterest-", ytdlp=ytdlp, strip_audio=_flag(a, "strip_audio"),
                          extra=_pin_extra(a))
    out = _pin_row(url, rec)
    if not out["file"]:
        return out
    if a.safe:
        s = edit_safe(Path(out["file"]))
        out["safe_file"] = str(s) if s else None
    return out


def pin_audio(url: str, a, ytdlp) -> dict:
    """--quality audio on a pin: classified first like every pin (one yt-dlp -J call); only a video pin's audio is
    fetched, in one yt-dlp attempt with no fallback or impersonation retry. No .pin.json is written for it."""
    v = pinterest.classify_link(url, ytdlp, _pin_extra(a))
    row = _pin_row(url, v)
    if v.get("kind") != "video":
        return row
    got = download(v["url"], a, ytdlp, once=True)
    row.pop("error", None)
    return {**row, **{k: val for k, val in got.items() if k != "url"}, "via": "pinterest"}


def info_for(path: Path) -> dict:
    j = path.with_suffix(".info.json")
    if not j.is_file():
        return {}
    try:
        d = json.loads(j.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {k: d.get(k) for k in ("title", "uploader", "id", "extractor_key", "license", "webpage_url", "upload_date")}


def _is_stock(url: str) -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import stock_fetch as sf  # noqa: PLC0415
    try:
        return sf.stock_file_url(url) is not None
    except (RuntimeError, ValueError):
        return True


def stock_download(url, a) -> dict | None:
    """Pexels / Mixkit / Pixabay pages and direct media-file links, fetched without yt-dlp.

    yt-dlp has no extractor for these stock sites and its generic extractor gets 403 on their pages,
    so they go through stock_fetch.py (Pexels' public download redirect, Mixkit's free 720p file,
    the Pixabay API). Returns None when the link is not one of them, so yt-dlp handles it."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import stock_fetch as sf  # noqa: PLC0415

    try:
        hit = sf.stock_file_url(url)
    except (RuntimeError, ValueError) as e:
        return {"url": url, "file": None, "error": str(e), "hint": "check the clip id / link, or the API key named above"}
    if not hit:
        return None
    source, file_url, cid = hit
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fpath = Path(urllib.parse.urlsplit(file_url).path)
    name = fpath.name or "clip.mp4"
    if cid:
        name = f"{source}-{cid}{Path(name).suffix or '.mp4'}"
    elif fpath.parent.name:  # e.g. cdn.coverr.co/videos/<slug>/1080p.mp4 -> <slug>-1080p.mp4
        name = f"{fpath.parent.name}-{name}"
    dest = out / name
    fresh = not dest.is_file() or not dest.stat().st_size
    try:
        if fresh:
            sf.download(file_url, dest)
    except Exception as e:  # noqa: BLE001 - report any network/HTTP failure as a failed row
        return {"url": url, "file": None, "error": f"{source}: {e}", "source": source, "file_url": file_url}
    rec = intake_audio(dest, a, {"url": url, "file": str(dest), "attempt": 1, "via": "stock_fetch", "source": source,
                                 "file_url": file_url, "id": cid, **probe(dest)}, fresh=fresh)
    if source in sf.LICENCES:
        rec["license"], rec["license_url"] = sf.LICENCES[source][:2]
    if rec.get("file") and a.safe and a.quality != "audio":
        s = edit_safe(dest)
        rec["safe_file"] = str(s) if s else None
    return rec


def download(url, a, ytdlp, once: bool = False) -> dict:
    """yt-dlp with the format fallback chain and one impersonation retry; `once` makes it a single attempt."""
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fmt, extra = selector(a.quality)
    fb = "ba/b/best" if a.quality == "audio" else "bv*+ba/b/best"
    tries = [(fmt, None)] if once else [(fmt, None), (fb, None)]
    imp = None if once else impersonation(ytdlp)
    if imp:
        tries.append((fb, imp))
    before = {p.name for p in out.iterdir()}  # a file already here was not downloaded by this run
    err = ""
    for i, (f, im) in enumerate(tries):
        path, err = attempt(ytdlp, url, out, f, extra, a.cookies, im, a.connections, a.proxy,
                            getattr(a, "cookies_from_browser", None))
        if path:
            p = Path(path)
            rec = intake_audio(p, a, {"url": url, "file": str(p), "attempt": i + 1, "impersonate": im, **probe(p),
                                      **info_for(p)}, fresh=p.name not in before)
            if rec.get("file") and a.safe and a.quality != "audio":
                s = edit_safe(p)
                rec["safe_file"] = str(s) if s else None
            return rec
        if "drm" in (err or "").lower() and (blocked(err, url) or {}).get("drm"):
            break   # DRM: the other format and impersonation tries would only knock on the same lock
    rec = {"url": url, "file": None, "error": err.strip()[-400:] or "download failed",
           "hint": "run --update (site changed), or supply --cookies for private/age-restricted posts"}
    rec.update(blocked(err, url) or {})
    return rec


def doctor(ytdlp) -> int:  # noqa: D103
    print("yt-dlp:", sh(ytdlp + ["--version"]).stdout.strip() if ytdlp else "MISSING (pip install yt-dlp curl_cffi)")
    print("ffmpeg:", "ok" if shutil.which("ffmpeg") else "MISSING")
    print("impersonation:", (impersonation(ytdlp) or "unavailable (pip install curl_cffi)") if ytdlp else "-")
    return 0 if ytdlp else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls", dest="urlfile", help="text file with one URL per line")
    ap.add_argument("-o", "--out", default="downloads")
    ap.add_argument("--quality", default="1080", type=norm_quality, help="best | 2160 | 1080 | 720 | 480 | audio (default 1080)")
    ap.add_argument("--cookies", help="Netscape-format cookies.txt exported from your own browser")
    ap.add_argument("--cookies-from-browser", metavar="BROWSER",
                    help="use your login from a local browser (chrome, firefox, edge, brave, safari…); nothing is copied or stored")
    ap.add_argument("--connections", type=int, default=8)
    ap.add_argument("--proxy")
    ap.add_argument("--cobalt-api", help="explicitly authorized Cobalt API root, no default or public scraping")
    ap.add_argument("--cobalt-key-env", default="KOSIF_COBALT_API_KEY", help="optional provider API key ENV name")
    ap.add_argument("--cobalt-allow-loopback", action="store_true", help="local integration tests only")
    ap.add_argument("--rights", choices=("owned", "direct-permission", "public-domain", "cc0", "cc-by", "cc-by-sa"),
                    help="required with --cobalt-api: documented ownership or permission")
    ap.add_argument("--safe", action="store_true", help="also write an edit-safe H.264/AAC copy (.safe.mp4)")
    ap.add_argument("--strip-audio", action="store_true",
                    help="drop each clip's own audio on intake (video stream copied, needs ffmpeg); use it for Quran and "
                         "other dignified jobs: Pinterest pins usually carry the creator's music")
    ap.add_argument("--classify", action="store_true",
                    help="Pinterest pins only: print what each pin is (video, image, gif, youtube, embedded, deleted, ...) "
                         "with one yt-dlp -J call each, and download nothing")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--update", action="store_true")
    a = ap.parse_args(argv)
    if a.cobalt_api and not a.rights:
        ap.error("--cobalt-api requires --rights")
    if a.cobalt_api and a.quality == "audio":
        ap.error("--cobalt-api currently supports video only")
    if a.strip_audio and a.quality == "audio":
        ap.error("--strip-audio cannot be combined with --quality audio")
    ytdlp = find_ytdlp(install=not bool(a.cobalt_api))
    if a.update:
        return subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "yt-dlp-ejs", "curl_cffi"])
    if a.doctor:
        return doctor(ytdlp)
    if not ytdlp and not a.cobalt_api and not a.urlfile and not all(_is_stock(u) for u in a.urls if is_url(u)):
        print("yt-dlp not found and could not be installed: pip install yt-dlp curl_cffi"
              " (no network? ask the user to upload the video file instead)", file=sys.stderr)
        return 1
    urls = list(a.urls)
    if a.urlfile:
        urls += [l.strip() for l in Path(a.urlfile).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    valid = lambda u: is_url(u) or bool(a.cobalt_api and cobalt.youtube_id(u))
    bad = [u for u in urls if not valid(u)]
    if bad:
        print("skipping entries that are not http(s) URLs: " + ", ".join(repr(u[:60]) for u in bad), file=sys.stderr)
        urls = [u for u in urls if valid(u)]
    if not urls:
        ap.print_usage()
        return 2
    if a.classify:
        return classify_pins(urls, a, ytdlp)
    results = []
    no_ytdlp = {"file": None, "error": "yt-dlp not installed: pip install yt-dlp curl_cffi"}
    for u in urls:
        if a.cobalt_api and cobalt.youtube_id(u):
            try:
                r = cobalt.download(u, a.out, a.cobalt_api, rights=a.rights, quality=a.quality,
                                    key_env=a.cobalt_key_env, allow_loopback=a.cobalt_allow_loopback)
                if a.strip_audio and r.get("file"):
                    r.update(probe(Path(r["file"])))
                    r = intake_audio(Path(r["file"]), a, r)
                if a.safe and r.get("file"):
                    safe = edit_safe(Path(r["file"]))
                    r["safe_file"] = str(safe) if safe else None
            except (cobalt.GatewayError, ValueError) as exc:
                r = {"url": u, "file": None, "provider": "cobalt-opt-in", "error": str(exc)}
            results.append(r)
            print(("OK   " + r["file"]) if r.get("file") else f"FAIL {u}\n     {r.get('error')}")
            continue  # A provider refusal is terminal; do not route around it.
        if pinterest.is_pin_link(u):
            r = (pin_audio if a.quality == "audio" else pin_download)(u, a, ytdlp) if ytdlp else {"url": u, **no_ytdlp}
        else:
            r = stock_download(u, a)
        if r is None:
            r = download(u, a, ytdlp) if ytdlp else {"url": u, **no_ytdlp}
        results.append(r)
        print(("OK   " + r["file"]) if r.get("file") else f"FAIL {u}\n     {r.get('error')}")
        if r.get("file") and r.get("size_note"):
            print("     " + r["size_note"])
        if r.get("blocked"):
            print("BLOCKED " + r["hint"])
    Path(a.out).mkdir(parents=True, exist_ok=True)  # a pin.it link to a board fails before anything is written
    (Path(a.out) / "manifest.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if all(r.get("file") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
