#!/usr/bin/env python3
"""Keyless stock-footage fetcher for montage jobs (Pexels by id, Mixkit by id) with a licence manifest.

Field-tested in a cloud session on 2026-10-21, when Pexels had paused new API keys and
pexels.com search pages returned 403 to scripts:

  * Pexels: the public download endpoint https://www.pexels.com/download/video/<id>/ answers
    with a 302 to the file on videos.pexels.com, so a clip downloads by id with no API key.
    Ids come from a web search restricted to pexels.com (each result URL ends in -<id>/).
  * Mixkit: https://assets.mixkit.co/videos/<id>/<id>-720.mp4 is free; 1080/2160 return 403.

Subcommands:
  probe                  report which stock sources answer from this machine
  pexels <id|url> ...    resolve each clip (302), optionally download, write manifest.json
  mixkit <id|url> ...    download the free 720p file of each clip, write manifest.json

Nothing here searches a site or bypasses a login: you pass ids you found yourself.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148")
PEXELS_DL = "https://www.pexels.com/download/video/{id}/"
PEXELS_PAGE = "https://www.pexels.com/video/{id}/"
MIXKIT_FILE = "https://assets.mixkit.co/videos/{id}/{id}-720.mp4"
LICENCES = {
    "pexels": ("Pexels License", "https://www.pexels.com/license/",
               "Free to use and modify, attribution optional; do not sell unaltered copies or imply endorsement."),
    "mixkit": ("Mixkit Free License", "https://mixkit.co/license/",
               "Free for commercial and personal projects; no redistribution as stock."),
}
PROBES = {
    "mixkit-page": "https://mixkit.co/free-stock-video/mosque/",
    "mixkit-720": "https://assets.mixkit.co/videos/4312/4312-720.mp4",
    "mixkit-1080": "https://assets.mixkit.co/videos/9998/9998-1080.mp4",
    "pexels-search-page": "https://www.pexels.com/search/videos/kaaba/",
    "pexels-download-302": "https://www.pexels.com/download/video/9112700/",
    "pexels-api": "https://api.pexels.com/videos/search?query=kaaba",
    "pixabay-api": "https://pixabay.com/api/videos/",
    "wikimedia-api": "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch=kaaba",
    "coverr": "https://coverr.co/s?q=mecca",
}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # keep the 302 so we can read Location
        return None


def parse_id(token: str) -> str:
    """Accept a bare id or a page URL such as .../video/name-of-clip-35155732/ and return the id."""
    token = token.strip()
    if token.isdigit():
        return token
    m = re.search(r"(\d{3,})/?(?:[?#].*)?$", token)
    if not m:
        raise ValueError(f"no clip id in {token!r}")
    return m.group(1)


def _request(url: str, method: str = "GET", follow: bool = True):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(_NoRedirect)
    return opener.open(req, timeout=30)


def status(url: str) -> str:
    try:
        with _request(url, "HEAD" if url.endswith(".mp4") else "GET", follow=False) as r:
            return str(r.status)
    except urllib.error.HTTPError as e:
        return str(e.code)
    except Exception as e:  # network refused, DNS, TLS
        return type(e).__name__


def resolve_pexels(clip_id: str) -> str:
    """Return the videos.pexels.com file URL behind the public download endpoint."""
    try:
        with _request(PEXELS_DL.format(id=clip_id), follow=False) as r:
            raise RuntimeError(f"expected a 302, got {r.status}")
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
            return e.headers["Location"]
        raise RuntimeError(f"pexels {clip_id}: HTTP {e.code}") from None


def remote_size(url: str) -> int | None:
    try:
        with _request(url, "HEAD") as r:
            n = r.headers.get("Content-Length")
            return int(n) if n else None
    except Exception:
        return None


def download(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    with _request(url) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    tmp.replace(dest)


def probe_media(path: Path) -> dict:
    if not shutil.which("ffprobe"):
        return {}
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        s = d["streams"][0]
        return {"width": s["width"], "height": s["height"], "fps": s["r_frame_rate"],
                "duration": round(float(d["format"]["duration"]), 3)}
    except Exception:
        return {}


def run_source(source: str, tokens: list[str], out: Path, max_mb: float, dry: bool) -> int:
    out.mkdir(parents=True, exist_ok=True)
    name, url, terms = LICENCES[source]
    rows, failed = [], 0
    for tok in tokens:
        try:
            cid = parse_id(tok)
            file_url = resolve_pexels(cid) if source == "pexels" else MIXKIT_FILE.format(id=cid)
            size = remote_size(file_url)
            row = {"id": cid, "source": source, "file_url": file_url,
                   "page": PEXELS_PAGE.format(id=cid) if source == "pexels" else f"https://mixkit.co/free-stock-video/{cid}/",
                   "licence": name, "licence_url": url, "licence_terms": terms,
                   "bytes": size, "file": None}
            if size and max_mb and size > max_mb * 1048576:
                row["skipped"] = f"larger than --max-mb {max_mb:g}"
            elif not dry:
                dest = out / f"{cid}.mp4"
                if not dest.exists():
                    download(file_url, dest)
                row.update(file=dest.name, **probe_media(dest))
            rows.append(row)
            print(f"{cid}\t{(size or 0) / 1048576:.1f} MB\t{row.get('skipped') or row['file'] or 'resolved'}")
        except Exception as e:
            failed += 1
            rows.append({"token": tok, "source": source, "error": str(e)})
            print(f"{tok}\tFAILED\t{e}", file=sys.stderr)
    manifest = out / "manifest.json"
    old = json.loads(manifest.read_text()) if manifest.exists() else []
    keep = [r for r in old if (r.get("source"), r.get("id")) not in {(r2.get("source"), r2.get("id")) for r2 in rows}]
    manifest.write_text(json.dumps(keep + rows, ensure_ascii=False, indent=1) + "\n")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe", help="report which stock sources answer from this machine")
    for src in ("pexels", "mixkit"):
        p = sub.add_parser(src, help=f"fetch {src} clips by id or page URL")
        p.add_argument("clips", nargs="+", help="ids or page URLs")
        p.add_argument("-o", "--out", default="./stock", help="output folder (default ./stock)")
        p.add_argument("--max-mb", type=float, default=120, help="skip files larger than this (0 = no limit)")
        p.add_argument("--dry-run", action="store_true", help="resolve and size only, download nothing")
    a = ap.parse_args(argv)
    if a.cmd == "probe":
        for k, u in PROBES.items():
            print(f"{status(u):>14}  {k:22} {u}")
        return 0
    return run_source(a.cmd, a.clips, Path(a.out), a.max_mb, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
