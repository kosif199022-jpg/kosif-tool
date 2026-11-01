#!/usr/bin/env python3
"""Song preview: find a song's official 30-second store preview and save it with a rights record.

معاينة الأغنية الرسمية: لما الأغنية المطلوبة مقفولة بـDRM (مثلًا yt-dlp يقول «This video is DRM protected» على
SoundCloud)، نقف عند المصدر ده ومنتحايلش عليه أبدًا (A19 الدرس 16). البديل المشروع: معاينة الـ30 ثانية الرسمية اللي
بيوفّرها الناشر للمتاجر، من واجهة بحث iTunes العامة (Apple) ومن Deezer كمصدر تاني. الأداة بتبحث، وبتنزّل المعاينة،
وبتكتب جنبها سجل حقوق (المصدر، أرقام الأغنية والفنان، رابط المتجر، رابط المعاينة، وقت التنزيل، ملاحظة الترخيص).

When the requested song is DRM-locked, stop at that source (never bypass). The legitimate fallback is the official
30-second preview the label supplies to stores: Apple's public iTunes Search API, with Deezer's public API as a second
source. This tool searches both, downloads a preview and writes a rights sidecar next to it.

Subcommands:
  search  "<artist and title words>" [--country eg] [--limit 10] [--sources itunes,deezer] [--out DIR] [--json]
          one table: row number, source, track, artist, album, release date, duration and whether a preview URL
          exists. The rows are saved to <out>/last_search.json (default out/song-preview/) for `download N` (network)
  download N|PREVIEW_URL [--out DIR]
          N = a row number from the last search in DIR. Saves <artist>-<track>-<source>.<m4a|mp3>, a
          <file>.rights.json sidecar, and prints the duration measured by ffprobe when it is installed (network).
          A raw URL is accepted only from the store preview hosts (*.itunes.apple.com, *.mzstatic.com, *.dzcdn.net).

Licence note written into every sidecar: official 30 s store preview; for private drafts; for public posting use the
platform's licensed sound (e.g. TikTok library); credit the artist. To fill a longer reel, extend only by
phrase-aligned repetition of the preview, never by fetching the full track from anywhere else.

It never touches DRM streams, uses no cookies, no logins and no yt-dlp, and reads no API key. HTTP goes through
urllib, so HTTPS_PROXY from the environment is honoured; every request has a timeout and at most --retries extra
attempts. Python 3.8+ standard library only.

  python3 song_preview.py search "تامر عاشور انا بحبك يا بلادي" --country eg
  python3 song_preview.py download 1 --out out/song-preview
"""
from __future__ import annotations

import argparse
import datetime as _dt
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

RESULTS_SCHEMA = "kosif.song_preview.results.v1"
RIGHTS_SCHEMA = "kosif.song_preview.rights.v1"
DEFAULT_OUT = Path("out") / "song-preview"
CACHE_NAME = "last_search.json"
USER_AGENT = "kosif-song-preview/1.0 (official store previews only)"
MAX_PREVIEW_BYTES = 20 * 1024 * 1024        # a 30 s preview is well under 2 MB
SOURCES = ("itunes", "deezer")
PREVIEW_HOSTS = (".itunes.apple.com", ".mzstatic.com", ".dzcdn.net")
LICENCE_NOTE = ("official 30 s store preview; for private drafts; for public posting use the platform's licensed "
                "sound (e.g. TikTok library); credit artist")
LICENCE_NOTE_AR = ("معاينة متجر رسمية 30 ثانية؛ للمسودات الخاصة فقط؛ للنشر العام استخدم الصوت المرخّص من مكتبة المنصة "
                   "(مثل مكتبة تيك توك)؛ واذكر اسم الفنان")


class FetchError(RuntimeError):
    pass


# ---------------------------------------------------------------- HTTP

def fetch(url: str, *, timeout: float = 15.0, retries: int = 2, max_bytes: int = MAX_PREVIEW_BYTES) -> bytes:
    """GET url with a timeout and at most `retries` extra attempts on network errors, 429 and 5xx."""
    last = ""
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - https only, checked by callers
                data = resp.read(max_bytes + 1)
            if len(data) > max_bytes:
                raise FetchError(f"response larger than {max_bytes} bytes: {url}")
            return data
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code != 429 and exc.code < 500:
                break
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = str(getattr(exc, "reason", exc))
        if attempt < retries:
            time.sleep(min(1.0 * (2 ** attempt), 4.0))
    raise FetchError(f"{last or 'request failed'}: {url}")


def fetch_json(url: str, **kw) -> dict:
    try:
        return json.loads(fetch(url, **kw).decode("utf-8"))
    except ValueError as exc:
        raise FetchError(f"not JSON: {url}") from exc


# ---------------------------------------------------------------- sources

def itunes_url(query: str, country: str, limit: int) -> str:
    q = urllib.parse.urlencode({"term": query, "entity": "song", "limit": limit, "country": country})
    return f"https://itunes.apple.com/search?{q}"


def deezer_url(query: str, limit: int) -> str:
    return "https://api.deezer.com/search?" + urllib.parse.urlencode({"q": query, "limit": limit})


def parse_itunes(payload: dict) -> list[dict]:
    rows = []
    for it in payload.get("results") or []:
        if it.get("kind") not in (None, "song"):
            continue
        ms = it.get("trackTimeMillis")
        rows.append({
            "source": "itunes",
            "track": it.get("trackName") or "",
            "artist": it.get("artistName") or "",
            "album": it.get("collectionName") or "",
            "release_date": (it.get("releaseDate") or "")[:10] or None,
            "duration_s": round(ms / 1000) if isinstance(ms, (int, float)) else None,
            "preview_url": it.get("previewUrl") or None,
            "store_url": it.get("trackViewUrl") or None,
            "track_id": it.get("trackId"),
            "artist_id": it.get("artistId"),
            "album_id": it.get("collectionId"),
        })
    return rows


def parse_deezer(payload: dict) -> list[dict]:
    rows = []
    for it in payload.get("data") or []:
        if it.get("type") not in (None, "track"):
            continue
        artist = it.get("artist") or {}
        album = it.get("album") or {}
        rows.append({
            "source": "deezer",
            "track": it.get("title") or "",
            "artist": artist.get("name") or "",
            "album": album.get("title") or "",
            "release_date": None,                     # not in Deezer search results
            "duration_s": it.get("duration"),
            "preview_url": it.get("preview") or None,  # sometimes empty
            "store_url": it.get("link") or None,
            "track_id": it.get("id"),
            "artist_id": artist.get("id"),
            "album_id": album.get("id"),
        })
    return rows


def search(query: str, *, country: str = "eg", limit: int = 10, sources=SOURCES,
           timeout: float = 15.0, retries: int = 2) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    errors: dict = {}
    for src in sources:
        try:
            if src == "itunes":
                rows += parse_itunes(fetch_json(itunes_url(query, country, limit), timeout=timeout, retries=retries))
            elif src == "deezer":
                rows += parse_deezer(fetch_json(deezer_url(query, limit), timeout=timeout, retries=retries))
            else:
                errors[src] = "unknown source"
        except FetchError as exc:
            errors[src] = str(exc)
    for i, r in enumerate(rows, 1):
        r["n"] = i
    return rows, errors


# ---------------------------------------------------------------- download

def allowed_preview_url(url: str) -> bool:
    p = urllib.parse.urlparse(url or "")
    host = (p.hostname or "").lower()
    return p.scheme == "https" and any(host.endswith(h) or host == h.lstrip(".") for h in PREVIEW_HOSTS)


def slug(text: str, n: int = 40) -> str:
    s = re.sub(r"[^\w\-]+", "-", text or "", flags=re.UNICODE).strip("-_").lower()
    return s[:n].strip("-")


def ext_for(url: str, data: bytes) -> str:
    path = urllib.parse.urlparse(url).path.lower()
    for e in (".m4a", ".mp3", ".aac", ".mp4"):
        if path.endswith(e):
            return ".m4a" if e == ".mp4" else e
    if data[:3] == b"ID3" or data[:2] in (b"\xff\xfb", b"\xff\xf3"):
        return ".mp3"
    return ".m4a"


def ffprobe_duration(path: Path) -> float | None:
    exe = shutil.which("ffprobe")
    if not exe:
        return None
    try:
        p = subprocess.run([exe, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                           capture_output=True, text=True, timeout=30)
        return round(float(p.stdout.strip()), 3)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def load_cache(out: Path) -> dict:
    f = out / CACHE_NAME
    if not f.is_file():
        raise SystemExit(f"no saved search in {f}: run `search` first (with the same --out) / مفيش بحث محفوظ")
    return json.loads(f.read_text(encoding="utf-8"))


def download(target: str, out: Path, *, timeout: float = 30.0, retries: int = 2) -> dict:
    if target.isdigit():
        cache = load_cache(out)
        rows = {r["n"]: r for r in cache.get("rows", [])}
        row = rows.get(int(target))
        if row is None:
            raise SystemExit(f"row {target} is not in the last search ({len(rows)} rows)")
        row = dict(row, query=cache.get("query"))
    else:
        row = {"source": "url", "track": "", "artist": "", "preview_url": target}
    url = row.get("preview_url")
    if not url:
        raise SystemExit(f"row {target} ({row.get('source')}) has no preview URL; pick another row / الصف ده مفيهوش معاينة")
    if not allowed_preview_url(url):
        raise SystemExit("refused: only official store preview hosts are accepted "
                         f"({', '.join(PREVIEW_HOSTS)}); this tool never fetches full tracks or DRM streams")
    data = fetch(url, timeout=timeout, retries=retries)
    out.mkdir(parents=True, exist_ok=True)
    stem = "-".join(x for x in (slug(row.get("artist", ""), 24), slug(row.get("track", ""), 40)) if x) or "preview"
    path = out / f"{stem}-{row.get('source')}{ext_for(url, data)}"
    path.write_bytes(data)
    duration = ffprobe_duration(path)
    rights = {
        "schema": RIGHTS_SCHEMA,
        "file": path.name,
        "bytes": len(data),
        "source": row.get("source"),
        "track": row.get("track"),
        "artist": row.get("artist"),
        "album": row.get("album"),
        "release_date": row.get("release_date"),
        "track_id": row.get("track_id"),
        "artist_id": row.get("artist_id"),
        "store_url": row.get("store_url"),
        "preview_url": url,
        "query": row.get("query"),
        "fetched_at": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat(),
        "duration_s": duration,
        "licence_note": LICENCE_NOTE,
        "licence_note_ar": LICENCE_NOTE_AR,
        "credit": f"{row.get('artist')} — {row.get('track')}" if row.get("artist") else None,
    }
    side = path.with_name(path.name + ".rights.json")
    side.write_text(json.dumps(rights, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rights["path"] = str(path)
    rights["rights_path"] = str(side)
    return rights


# ---------------------------------------------------------------- CLI

def fmt_dur(s) -> str:
    return f"{int(s) // 60}:{int(s) % 60:02d}" if isinstance(s, (int, float)) else "?"


def print_rows(rows: list[dict]) -> None:
    print(f"{'#':>3}  {'source':7} {'preview':7} {'dur':>5}  {'released':10}  track — artist — album")
    for r in rows:
        print(f"{r['n']:>3}  {r['source']:7} {'yes' if r.get('preview_url') else 'no':7} {fmt_dur(r.get('duration_s')):>5}  "
              f"{(r.get('release_date') or '-'):10}  {r['track']} — {r['artist']} — {r['album']}")


def cmd_search(a) -> int:
    sources = tuple(s.strip() for s in a.sources.split(",") if s.strip())
    rows, errors = search(a.query, country=a.country, limit=a.limit, sources=sources,
                          timeout=a.timeout, retries=a.retries)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    payload = {"schema": RESULTS_SCHEMA, "query": a.query, "country": a.country, "sources": list(sources),
               "searched_at": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat(),
               "errors": errors, "rows": rows}
    (out / CACHE_NAME).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if a.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_rows(rows)
        for src, err in errors.items():
            print(f"warning: {src} failed: {err}", file=sys.stderr)
        print(f"\nsaved {len(rows)} rows to {out / CACHE_NAME}; next: download <n> --out {out}")
    return 0 if rows else 1


def cmd_download(a) -> int:
    try:
        rec = download(a.target, Path(a.out), timeout=a.timeout, retries=a.retries)
    except FetchError as exc:
        print(f"download failed: {exc}", file=sys.stderr)
        return 1
    print(f"saved  {rec['path']} ({rec['bytes']} bytes)")
    print(f"rights {rec['rights_path']}")
    print(f"duration {rec['duration_s']} s" if rec["duration_s"] is not None else "duration: ffprobe not available")
    print(f"note: {LICENCE_NOTE}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="song_preview.py",
        description=__doc__,
        epilog=("No DRM, no cookies, no logins, no yt-dlp. Private drafts only; public posts use the platform's "
                "licensed sound and credit the artist. / مفيش تحايل على DRM ولا كوكيز ولا تسجيل دخول؛ "
                "المعاينة للمسودات الخاصة، والنشر العام بالصوت المرخّص من المنصة مع ذكر الفنان."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--out", default=str(DEFAULT_OUT),
                        help=f"folder for the search cache and downloads (default {DEFAULT_OUT}) / فولدر الحفظ")
        sp.add_argument("--timeout", type=float, default=15.0, help="seconds per request / مهلة كل طلب")
        sp.add_argument("--retries", type=int, choices=range(0, 4), default=2, metavar="0-3",
                        help="extra attempts on network errors, 429 and 5xx (default 2) / محاولات إضافية")

    s = sub.add_parser("search", help="search iTunes and Deezer / ابحث عن الأغنية",
                       description="Search the iTunes Search API and Deezer; save the rows for `download N`. "
                                   "ابحث باسم الفنان والأغنية واحفظ النتائج.")
    s.add_argument("query", help="artist and title words / اسم الفنان والأغنية")
    s.add_argument("--country", default="eg", help="iTunes storefront, two letters (default eg) / بلد المتجر")
    s.add_argument("--limit", type=int, default=10, help="rows per source (default 10) / عدد النتائج لكل مصدر")
    s.add_argument("--sources", default="itunes,deezer", help="comma list: itunes,deezer / المصادر")
    s.add_argument("--json", action="store_true", help="print JSON / اطبع JSON")
    common(s)
    s.set_defaults(func=cmd_search)

    d = sub.add_parser("download", help="save a preview and its rights sidecar / نزّل المعاينة وسجل الحقوق",
                       description="Download row N of the last search (or a store preview URL) plus <file>.rights.json. "
                                   "نزّل الصف رقم N من آخر بحث، ومعاه سجل الحقوق.")
    d.add_argument("target", help="row number from the last search, or an official preview URL / رقم الصف أو رابط المعاينة")
    common(d)
    d.set_defaults(func=cmd_download)
    return p


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    if getattr(a, "limit", 1) < 1 or getattr(a, "limit", 1) > 50:
        print("--limit must be 1..50", file=sys.stderr)
        return 2
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
