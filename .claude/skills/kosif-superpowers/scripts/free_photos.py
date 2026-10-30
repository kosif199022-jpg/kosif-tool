#!/usr/bin/env python3
"""Free photos: search open-licence and free stock photos for montage, download them with a licence record each.

صور مجانية للمونتاج: بحث في مواقع الصور المجانية ومفتوحة الترخيص، وتحميل كل صورة ومعاها ترخيصها وسطر النسب.
الفيديو المجاني له أداة أخته: scripts/free_footage.py (نفس الفكرة للقطات الفيديو).

Subcommands:
  sources [--json]
          the photo sources, their licence, credit rule, commercial use and key variable (offline)
  search  QUERY [--sources a,b] [--limit N] [--orientation landscape|portrait|square] [--min-width PX]
          [--commercial] [--allow-nd] [--replace] [--results FILE]
          key-less: Openverse (CC and public-domain images from many sites), Wikimedia Commons, NASA Images,
          The Met Open Access (CC0 only); with keys in the environment: Pexels (PEXELS_API_KEY), Pixabay
          (PIXABAY_API_KEY), Unsplash (UNSPLASH_ACCESS_KEY). Results merge by id into
          out/free-photos/last_search.json (network)
  sheet   [RESULTS.json] [--out DIR]
          contact_sheet.html: every result's small preview with its id, size, licence and credit, to choose
          before downloading (offline; the browser loads the previews)
  download ID... --out DIR [--size full|large] [--max-mb MB] [--dry-run]
          saves <source>-<id>.<ext>, a <file>.json sidecar (licence, credit line, bytes, sha256) and rebuilds
          <out>/ATTRIBUTION.md; an Unsplash download is reported to Unsplash first, as its API terms require (network)
  credits DIR
          rebuild DIR/ATTRIBUTION.md from the sidecars (offline)

Licences are what each source declares (Openverse's licence_url per image, Commons extmetadata, the Met's
isPublicDomain flag, NASA's media guidelines, the Pexels, Pixabay and Unsplash licences). The tool records them; it
does not grant them. ND licences are dropped by default (a montage is an adaptation), --commercial also drops NC and
unknown licences. Openverse indexes other sites, so its licence is the one the original site shows: open page_url
before using a photo in paid work.

HTTP goes through free_footage.Http: one request per host per --delay seconds, timeouts, a User-Agent, size caps,
one bounded retry on 429/503, and a Cloudflare browser check reported, never worked around. Keys are read from the
environment only, never printed or stored. Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html as _html
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import free_footage as FF  # noqa: E402  (shared HTTP client, licence reader, text helpers)

RESULTS_SCHEMA = "kosif.free_photos.results.v1"
ASSET_SCHEMA = "kosif.free_photos.asset.v1"
DEFAULT_RESULTS = Path("out") / "free-photos" / "last_search.json"
FILE_CAP_MB = 60.0
RESULTS_HISTORY = 50
KEY_ENV = {"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY", "unsplash": "UNSPLASH_ACCESS_KEY"}
SCRIPT_FROM_ROOT = (f".claude/skills/{HERE.parent.name}/scripts/free_photos.py"  # how to run it from the repo root
                    if HERE.parent.parent.name == "skills" else "scripts/free_photos.py")

PD = dict(attribution=False, commercial=True, derivatives=True, share_alike=False)

# One record per source. "commercial": yes / per-item (read each result's licence) / no.
SOURCES = {
    "openverse": {
        "name": "Openverse", "url": "https://openverse.org/", "key": None, "commercial": "per-item",
        "licence": ("Per image: CC BY, CC BY-SA, CC0 or Public Domain Mark", "https://openverse.org/about"),
        "credit": '"{title}" by {author}, {licence} ({licence_url}), via Openverse: {page_url}',
        "about": "Search engine over 800M+ openly licensed images (Flickr, museums, Wikimedia, StockSnap...). "
                 "Credit required for CC BY/BY-SA; the licence is the one the original site shows.",
    },
    "wikimedia": {
        "name": "Wikimedia Commons", "url": "https://commons.wikimedia.org/", "key": None, "commercial": "per-item",
        "licence": ("Per file: CC0, Public domain, CC BY, CC BY-SA", "https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia"),
        "credit": '"{title}" by {author}, {licence} ({licence_url}), from Wikimedia Commons: {page_url}',
        "about": "Huge free media library: places, history, nature, maps. Credit usually required (per file).",
    },
    "nasa": {
        "name": "NASA Image and Video Library", "url": "https://images.nasa.gov/", "key": None, "commercial": "yes",
        "licence": ("NASA Media Usage Guidelines", "https://www.nasa.gov/nasa-brand-center/images-and-media/"),
        "credit": '"{title}", {author} (NASA): {page_url}',
        "about": "Space, Earth from orbit, rockets, astronauts. Generally not copyrighted; acknowledge NASA, no "
                 "implied endorsement, NASA logos and third-party marked images need permission.",
    },
    "met": {
        "name": "The Met Open Access", "url": "https://www.metmuseum.org/about-the-met/policies-and-documents/open-access",
        "key": None, "commercial": "yes",
        "licence": ("CC0 1.0 (Met Open Access)", "https://creativecommons.org/publicdomain/zero/1.0/"),
        "credit": '"{title}" ({author}), The Metropolitan Museum of Art, CC0: {page_url}',
        "about": "Public-domain artworks: Islamic art, calligraphy, manuscripts, antiquities, paintings. Only objects "
                 "the Met marks isPublicDomain are kept.",
    },
    "pexels": {
        "name": "Pexels", "url": "https://www.pexels.com/", "key": "PEXELS_API_KEY", "commercial": "yes",
        "licence": ("Pexels License", "https://www.pexels.com/license/"),
        "credit": "Photo by {author} on Pexels: {page_url}",
        "about": "Modern lifestyle, city, nature, many vertical photos. Credit not required. Not allowed: selling "
                 "unaltered copies, implying endorsement by people shown.",
    },
    "pixabay": {
        "name": "Pixabay", "url": "https://pixabay.com/", "key": "PIXABAY_API_KEY", "commercial": "yes",
        "licence": ("Pixabay Content License", "https://pixabay.com/service/license-summary/"),
        "credit": "Image by {author} from Pixabay: {page_url}",
        "about": "Photos, illustrations and vectors. Credit not required. The API serves up to 1280 px "
                 "(largeImageURL); full size needs approved API access. Download, do not hotlink.",
    },
    "unsplash": {
        "name": "Unsplash", "url": "https://unsplash.com/", "key": "UNSPLASH_ACCESS_KEY", "commercial": "yes",
        "licence": ("Unsplash License", "https://unsplash.com/license"),
        "credit": "Photo by {author} on Unsplash: {page_url}",
        "about": "High-end photography. The licence needs no credit, but its API terms ask apps to credit the "
                 "photographer and Unsplash and to report each download (the tool does). Not allowed: selling "
                 "unaltered copies, building a competing photo service. Unsplash+ photos are paid and skipped.",
    },
}


class PhotoError(FF.FootageError):
    pass


def api_key(source: str, environ=None) -> str | None:
    env = os.environ if environ is None else environ
    name = KEY_ENV.get(source)
    v = (env.get(name) or "").strip() if name else ""
    return v or None


def redact(text) -> str:
    s = FF.redact(text)
    s = re.sub(r"(?i)(client_id=)[^&#\s]+", r"\1***", s)
    for name in KEY_ENV.values():
        k = os.environ.get(name) or ""
        if len(k) >= 6:
            s = s.replace(k, "***")
    return s


def fill_credit(template: str, **fields) -> str:
    return FF.format_attribution(template, **fields)


def result(source: str, native_id, *, title, page_url, file_url, licence: dict, author=None, author_url=None,
           width=None, height=None, preview_url=None, extra=None) -> dict:
    src = SOURCES[source]
    title = FF.clean_text(title) or None
    author = FF.clean_text(author) or None
    rec = {
        "id": f"{source}:{native_id}", "source": source, "source_name": src["name"], "kind": "photo",
        "title": title, "page_url": page_url, "file_url": FF.https(file_url) or None,
        "preview_url": FF.https(preview_url) or None,
        "width": FF._int(width), "height": FF._int(height), "author": author, "author_url": author_url,
        "licence": licence,
        "attribution": fill_credit(src["credit"], title=title, author=author, source=src["name"],
                                   licence=licence.get("name"), licence_url=licence.get("url"), page_url=page_url),
    }
    if extra:
        rec.update(extra)
    return rec


def source_licence(source: str, **over) -> dict:
    name, url = SOURCES[source]["licence"]
    flags = dict(PD)
    flags.update(over)
    return FF.licence_record(name, url, **flags)


# ------------------------------------------------------------------------------------------------- adapters
# Each adapter is a URL builder plus a parser of the answer, so the parsers are tested offline.

OPENVERSE_API = "https://api.openverse.org/v1/images/"


def openverse_url(query: str, limit: int, opts: dict) -> str:
    q = {"q": query, "page_size": str(max(1, min(limit, 20))), "mature": "false",
         "license_type": "commercial,modification" if opts.get("commercial") else
         ("all" if opts.get("allow_nd") else "modification")}
    ori = {"landscape": "wide", "portrait": "tall", "square": "square"}.get(opts.get("orientation") or "")
    if ori:
        q["aspect_ratio"] = ori
    return OPENVERSE_API + "?" + urllib.parse.urlencode(q)


def parse_openverse(data: dict) -> list:
    out = []
    for r in (data or {}).get("results") or []:
        lic = FF.classify_licence(f"CC {r.get('license', '')} {r.get('license_version') or ''}".strip()
                                  if r.get("license") not in ("cc0", "pdm") else r.get("license"),
                                  r.get("license_url"))
        if r.get("license") == "pdm":
            lic = FF.licence_record("Public Domain Mark 1.0", r.get("license_url"), **PD)
        lic["note"] = ((lic.get("note") or "") + "; as declared by " + str(r.get("source") or r.get("provider") or
                       "the original site") + " (Openverse indexes it)").strip("; ")
        out.append(result("openverse", r.get("id"), title=r.get("title"),
                          page_url=r.get("foreign_landing_url") or f"https://openverse.org/image/{r.get('id')}",
                          file_url=r.get("url"), preview_url=r.get("thumbnail"), licence=lic,
                          author=r.get("creator"), author_url=r.get("creator_url"),
                          width=r.get("width"), height=r.get("height"),
                          extra={"native": {"provider": r.get("provider"), "source": r.get("source")}}))
    return out


COMMONS_API = FF.COMMONS_API


def commons_url(query: str, limit: int, opts: dict) -> str:
    q = {"action": "query", "format": "json", "formatversion": "2", "generator": "search",
         "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": "6", "gsrlimit": str(max(1, min(limit, 50))),
         "prop": "imageinfo", "iiprop": FF.COMMONS_IIPROP, "iiextmetadatafilter": FF.COMMONS_META,
         "iiurlwidth": "640"}
    return COMMONS_API + "?" + urllib.parse.urlencode(q)


def parse_commons(data: dict) -> list:
    pages = ((data or {}).get("query") or {}).get("pages") or []
    if isinstance(pages, dict):
        pages = list(pages.values())
    out = []
    for p in sorted(pages, key=lambda p: p.get("index", 0)):
        info = (p.get("imageinfo") or [None])[0]
        if not info or p.get("missing"):
            continue
        mime = info.get("mime") or ""
        if not mime.startswith("image/") or mime in ("image/svg+xml", "image/vnd.djvu", "image/tiff"):
            continue
        meta = info.get("extmetadata") or {}
        mv = lambda k: (meta.get(k) or {}).get("value")  # noqa: E731
        lic = FF.classify_licence(FF.clean_text(mv("LicenseShortName")), FF.clean_text(mv("LicenseUrl")) or None)
        req = str(mv("AttributionRequired") or "").strip().lower()
        if req in ("true", "false"):
            lic["attribution_required"] = req == "true"
        title = FF.clean_text(mv("ObjectName")) or re.sub(r"^File:|\.[A-Za-z0-9]+$", "", p.get("title", ""))
        out.append(result("wikimedia", p.get("pageid"), title=title, page_url=info.get("descriptionurl"),
                          file_url=FF.strip_tracking(info.get("url", "")), licence=lic, author=mv("Artist"),
                          width=info.get("width"), height=info.get("height"),
                          preview_url=FF.strip_tracking(info["thumburl"]) if info.get("thumburl") else None))
    return out


NASA_SEARCH = "https://images-api.nasa.gov/search"


def nasa_url(query: str, limit: int, opts: dict) -> str:
    return NASA_SEARCH + "?" + urllib.parse.urlencode({"q": query, "media_type": "image",
                                                      "page_size": str(max(1, min(limit, 100)))})


def parse_nasa(data: dict) -> list:
    out = []
    for item in ((data or {}).get("collection") or {}).get("items") or []:
        d = (item.get("data") or [{}])[0]
        links = [x for x in item.get("links") or [] if x.get("render") == "image" and x.get("href")]
        if not d.get("nasa_id") or not links:
            continue
        best = max(links, key=lambda x: (x.get("width") or 0, "~orig" in x["href"]))
        small = next((x for x in links if "~medium" in x["href"] or x.get("rel") == "preview"), links[0])
        author = d.get("secondary_creator") or d.get("photographer") or (f"NASA {d['center']}" if d.get("center") else "NASA")
        out.append(result("nasa", d["nasa_id"], title=d.get("title"),
                          page_url="https://images.nasa.gov/details/" + urllib.parse.quote(str(d["nasa_id"]), safe=""),
                          file_url=FF.quote_path(FF.https(best["href"])), preview_url=FF.quote_path(FF.https(small["href"])),
                          licence=source_licence("nasa", attribution=True,
                                                 note="acknowledge NASA; no implied endorsement; NASA logos and "
                                                      "third-party marked material need permission"),
                          author=author, width=best.get("width"), height=best.get("height")))
    return out


MET_SEARCH = "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
MET_OBJECT = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}"


def met_url(query: str, limit: int, opts: dict) -> str:
    # v1 search was retired on 2026-10-01 (HTTP 410 names v1.1, paginated by offset and limit)
    return MET_SEARCH + "?" + urllib.parse.urlencode({"q": query, "hasImages": "true",
                                                     "limit": str(max(1, min(limit * 2, 40))), "offset": "0"})


def parse_met_object(d: dict) -> dict | None:
    if not d or not d.get("isPublicDomain") or not d.get("primaryImage"):
        return None
    title = d.get("title") or "Untitled"
    if d.get("objectDate"):
        title = f"{title}, {d['objectDate']}"
    return result("met", d.get("objectID"), title=title, page_url=d.get("objectURL"),
                  file_url=d.get("primaryImage"), preview_url=d.get("primaryImageSmall"),
                  licence=source_licence("met"), author=d.get("artistDisplayName") or d.get("culture") or None,
                  extra={"native": {"credit_line": d.get("creditLine")}})


def search_met(http, query: str, limit: int, opts: dict) -> list:
    ids = (http.get_json(met_url(query, limit, opts)) or {}).get("objectIDs") or []
    out = []
    for oid in ids[: limit * 2]:
        try:
            rec = parse_met_object(http.get_json(MET_OBJECT.format(id=int(oid))))
        except (FF.FootageError, ValueError, TypeError):
            continue
        if rec:
            out.append(rec)
        if len(out) >= limit:
            break
    return out


PEXELS_API = "https://api.pexels.com/v1/search"


def pexels_url(query: str, limit: int, opts: dict) -> str:
    q = {"query": query, "per_page": str(max(1, min(limit, 80)))}
    if opts.get("orientation"):
        q["orientation"] = opts["orientation"]
    return PEXELS_API + "?" + urllib.parse.urlencode(q)


def parse_pexels(data: dict) -> list:
    out = []
    for p in (data or {}).get("photos") or []:
        src = p.get("src") or {}
        out.append(result("pexels", p.get("id"), title=p.get("alt") or f"Pexels photo {p.get('id')}",
                          page_url=p.get("url"), file_url=src.get("original"), preview_url=src.get("medium"),
                          licence=source_licence("pexels"), author=p.get("photographer"),
                          author_url=p.get("photographer_url"), width=p.get("width"), height=p.get("height"),
                          extra={"sizes": {"full": src.get("original"), "large": src.get("large2x")}}))
    return out


PIXABAY_API = "https://pixabay.com/api/"


def pixabay_url(key: str, query: str, limit: int, opts: dict) -> str:
    q = {"key": key, "q": query[:100], "image_type": "photo", "safesearch": "true",
         "per_page": str(max(3, min(limit, 200)))}
    ori = {"landscape": "horizontal", "portrait": "vertical"}.get(opts.get("orientation") or "")
    if ori:
        q["orientation"] = ori
    return PIXABAY_API + "?" + urllib.parse.urlencode(q)


def parse_pixabay(data: dict) -> list:
    out = []
    for h in (data or {}).get("hits") or []:
        w, hgt = FF._int(h.get("imageWidth")), FF._int(h.get("imageHeight"))
        if w and hgt and max(w, hgt) > 1280:  # largeImageURL is scaled to 1280 on the long side
            k = 1280 / max(w, hgt)
            w, hgt = round(w * k), round(hgt * k)
        out.append(result("pixabay", h.get("id"), title=h.get("tags") or f"Pixabay image {h.get('id')}",
                          page_url=h.get("pageURL"), file_url=h.get("largeImageURL"),
                          preview_url=h.get("webformatURL"), licence=source_licence("pixabay"),
                          author=h.get("user"), width=w, height=hgt))
    return out


UNSPLASH_API = "https://api.unsplash.com/search/photos"


def unsplash_url(query: str, limit: int, opts: dict) -> str:
    q = {"query": query, "per_page": str(max(1, min(limit, 30))), "content_filter": "high"}
    ori = {"landscape": "landscape", "portrait": "portrait", "square": "squarish"}.get(opts.get("orientation") or "")
    if ori:
        q["orientation"] = ori
    return UNSPLASH_API + "?" + urllib.parse.urlencode(q)


def parse_unsplash(data: dict) -> list:
    out = []
    for p in (data or {}).get("results") or []:
        if p.get("premium") or p.get("plus"):
            continue  # Unsplash+ is a paid licence
        urls, links, user = p.get("urls") or {}, p.get("links") or {}, p.get("user") or {}
        page = links.get("html")
        if page:
            page += ("&" if "?" in page else "?") + "utm_source=kosif&utm_medium=referral"
        out.append(result("unsplash", p.get("id"), title=p.get("description") or p.get("alt_description")
                          or f"Unsplash photo {p.get('id')}", page_url=page, file_url=urls.get("full"),
                          preview_url=urls.get("small"), licence=source_licence("unsplash"), author=user.get("name"),
                          author_url=(user.get("links") or {}).get("html"), width=p.get("width"), height=p.get("height"),
                          extra={"sizes": {"full": urls.get("full"),
                                           "large": (urls.get("raw") + "&w=2400&q=85&fm=jpg") if urls.get("raw") else None},
                                 "download_location": links.get("download_location")}))
    return out


def search_source(http, source: str, query: str, limit: int, opts: dict, environ=None) -> list:
    key = api_key(source, environ)
    if SOURCES[source]["key"] and not key:
        raise PhotoError(f"skipped: set {SOURCES[source]['key']} in the environment to search {SOURCES[source]['name']}")
    if source == "openverse":
        return parse_openverse(http.get_json(openverse_url(query, limit, opts)))
    if source == "wikimedia":
        return parse_commons(http.get_json(commons_url(query, limit * 2, opts)))
    if source == "nasa":
        return parse_nasa(http.get_json(nasa_url(query, limit, opts)))
    if source == "met":
        return search_met(http, query, limit, opts)
    if source == "pexels":
        return parse_pexels(http.get_json(pexels_url(query, limit, opts), {"Authorization": key}))
    if source == "pixabay":
        return parse_pixabay(http.get_json(pixabay_url(key, query, limit, opts)))
    if source == "unsplash":
        return parse_unsplash(http.get_json(unsplash_url(query, limit, opts),
                                            {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"}))
    raise PhotoError(f"unknown source {source}")


# ------------------------------------------------------------------------------------------------- filters

def orientation_of(r: dict) -> str | None:
    w, h = r.get("width"), r.get("height")
    if not w or not h:
        return None
    if abs(w - h) <= 0.05 * max(w, h):
        return "square"
    return "landscape" if w > h else "portrait"


def drop_reason(r: dict, opts: dict) -> str | None:
    lic = r.get("licence") or {}
    if lic.get("derivatives") is False and not opts.get("allow_nd"):
        return "nd-licence"
    if opts.get("commercial") and lic.get("commercial") is not True:
        return "not-commercial" if lic.get("commercial") is False else "licence-unconfirmed"
    if not r.get("file_url"):
        return "no-file"
    ori = opts.get("orientation")
    if ori and orientation_of(r) not in (None, ori):
        return "orientation"
    mw = opts.get("min_width")
    if mw and r.get("width") and max(r["width"], r.get("height") or 0) < mw:
        return "too-small"
    return None


def default_sources(environ=None) -> list:
    return [s for s, v in SOURCES.items() if not v["key"] or api_key(s, environ)]


def run_search(http, query: str, sources: list, limit: int, opts: dict, environ=None) -> dict:
    report = {"schema": RESULTS_SCHEMA, "query": query, "searched_at": _dt.datetime.now(_dt.timezone.utc)
              .isoformat(timespec="seconds"), "sources": {}, "dropped": {}, "results": []}
    for s in sources:
        try:
            found = search_source(http, s, query, limit, opts, environ)
        except FF.FootageError as e:
            msg = redact(e)
            report["sources"][s] = {"status": "skipped" if msg.startswith("skipped") else "error", "detail": msg}
            continue
        kept = 0
        for r in found:
            why = drop_reason(r, opts)
            if why:
                report["dropped"][why] = report["dropped"].get(why, 0) + 1
                continue
            if kept < limit:
                report["results"].append(r)
                kept += 1
        report["sources"][s] = {"status": "ok", "found": len(found), "kept": kept}
    return report


def load_results(path: Path) -> dict | None:
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        return d if d.get("schema") == RESULTS_SCHEMA else None
    except (OSError, ValueError):
        return None


def merge_results(prev: dict | None, report: dict) -> dict:
    """New results first, then earlier ones not seen again, so ids from earlier searches still download."""
    seen, merged = set(), []
    for r in report["results"] + ((prev or {}).get("results") or []):
        if r["id"] not in seen:
            seen.add(r["id"])
            merged.append(r)
    hist = ((prev or {}).get("searches") or [])
    hist = [{"query": report["query"], "at": report["searched_at"], "sources": report["sources"],
             "ids": [r["id"] for r in report["results"]]}] + hist
    return {**report, "results": merged, "searches": hist[:RESULTS_HISTORY]}


def licence_text(lic: dict) -> str:
    credit = {True: "credit required", False: "credit optional", None: "credit: check"}[lic.get("attribution_required")]
    com = {True: "commercial ok", False: "NON-commercial", None: "commercial: check"}[lic.get("commercial")]
    return f"{lic.get('name')} · {credit} · {com}"


def print_report(report: dict) -> None:
    for s, st in report["sources"].items():
        extra = f"{st.get('kept')}/{st.get('found')} kept" if st["status"] == "ok" else st.get("detail", "")
        print(f"# {s}: {st['status']} {extra}")
    if report["dropped"]:
        print("# dropped: " + ", ".join(f"{k} {v}" for k, v in sorted(report["dropped"].items())))
    for r in report["results"]:
        size = f"{r['width']}x{r['height']}" if r.get("width") else "size ?"
        print(f"{r['id']:<40} {size:<11} {licence_text(r['licence'])}\n    {r.get('title') or ''}\n    {r.get('page_url')}")


# ------------------------------------------------------------------------------------------------- contact sheet

def sheet_html(data: dict) -> str:
    e = lambda s: _html.escape(str(s if s is not None else ""), quote=True)  # noqa: E731
    cells = []
    for r in data.get("results") or []:
        size = f"{r['width']}×{r['height']}" if r.get("width") else ""
        cells.append(
            f'<figure><a href="{e(r.get("page_url"))}" target="_blank" rel="noopener">'
            f'<img src="{e(r.get("preview_url") or r.get("file_url"))}" alt="{e(r.get("title"))}" loading="lazy"></a>'
            f'<figcaption><code>{e(r["id"])}</code> {e(size)}<br>{e(licence_text(r.get("licence") or {}))}'
            f'<br><small>{e(r.get("attribution"))}</small></figcaption></figure>')
    return ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Free photos: {e(data.get('query'))}</title><style>body{{font:14px system-ui;margin:16px;"
            "background:#111;color:#eee}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));"
            "gap:12px}figure{margin:0;background:#1d1d1d;border-radius:8px;overflow:hidden}img{width:100%;height:180px;"
            "object-fit:cover;display:block}figcaption{padding:8px;line-height:1.4}code{color:#9cf}small{color:#aaa}"
            "a{color:inherit}</style>"
            f"<h1>{e(data.get('query'))}</h1><p>Download with: <code>python3 {e(SCRIPT_FROM_ROOT)} download ID --out DIR"
            f"</code></p><main>{''.join(cells)}</main>")


# ------------------------------------------------------------------------------------------------- download

def sidecar_for(media: Path) -> Path:
    return media.with_name(media.name + ".json")


def safe_stem(rid: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", rid.replace(":", "-")).strip("-")[:120]


def pick_url(rec: dict, size: str) -> str | None:
    return ((rec.get("sizes") or {}).get(size) or rec.get("file_url")) if size == "large" else rec.get("file_url")


def download_one(http, rec: dict, out: Path, size: str = "full", max_mb: float = FILE_CAP_MB,
                 dry_run: bool = False, environ=None) -> Path | None:
    lic = rec.get("licence") or {}
    if lic.get("derivatives") is False:
        raise PhotoError(f"{rec['id']}: {lic.get('name')} forbids edits (ND); not downloaded for a montage")
    url = pick_url(rec, size)
    if not url:
        raise PhotoError(f"{rec['id']}: the result has no file link")
    if dry_run:
        print(f"{rec['id']}: would fetch {redact(url)} ({rec.get('width')}x{rec.get('height')})")
        return None
    if rec["source"] == "unsplash" and rec.get("download_location"):
        key = api_key("unsplash", environ)
        if not key:
            raise PhotoError("unsplash: set UNSPLASH_ACCESS_KEY (its API terms require reporting each download)")
        http.get_json(rec["download_location"], {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"})
    body = http.get_bytes(url, {"Accept": "image/*"}, cap_mb=max_mb)
    ext = FF.image_ext(body[:16])
    if not ext:
        raise PhotoError(f"{rec['id']}: {redact(url)} did not answer with an image (a web page or an error)")
    out.mkdir(parents=True, exist_ok=True)
    path = out / (safe_stem(rec["id"]) + ext)
    path.write_bytes(body)
    side = {"schema": ASSET_SCHEMA, "id": rec["id"], "file": path.name, "source": rec["source"],
            "source_name": rec.get("source_name"), "title": rec.get("title"), "author": rec.get("author"),
            "author_url": rec.get("author_url"), "page_url": rec.get("page_url"), "file_url": redact(url),
            "width": rec.get("width"), "height": rec.get("height"), "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(), "licence": lic, "attribution": rec.get("attribution"),
            "downloaded_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")}
    sidecar_for(path).write_text(json.dumps(side, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def credits_markdown(folder: Path) -> str:
    rows = []
    for p in sorted(Path(folder).glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if d.get("schema") == ASSET_SCHEMA:
            rows.append(d)
    lines = ["# Photo credits", "", f"Rebuild: `python3 {SCRIPT_FROM_ROOT} credits {folder}`", "",
             "| file | source | licence | credit | commercial |", "|---|---|---|---|---|"]
    for d in rows:
        lic = d.get("licence") or {}
        lines.append(f"| {d['file']} | {d.get('source_name')} | [{lic.get('name')}]({lic.get('url')}) | "
                     f"{ {True: 'required', False: 'optional', None: 'check'}[lic.get('attribution_required')] } | "
                     f"{ {True: 'yes', False: 'NO', None: 'check'}[lic.get('commercial')] } |")
    lines += ["", "## Credit lines", ""]
    for d in rows:
        opt = " *(optional)*" if (d.get("licence") or {}).get("attribution_required") is False else ""
        lines.append(f"- {d.get('attribution')}{opt}")
    if not rows:
        lines.append("- (no photos yet)")
    return "\n".join(lines) + "\n"


def write_credits(folder: Path) -> Path:
    path = Path(folder) / "ATTRIBUTION.md"
    path.write_text(credits_markdown(folder), encoding="utf-8")
    return path


# ------------------------------------------------------------------------------------------------- CLI

def cmd_sources(args) -> int:
    if args.json:
        print(json.dumps(SOURCES, ensure_ascii=False, indent=2))
        return 0
    for sid, s in SOURCES.items():
        key = s["key"] or "no key"
        have = "" if not s["key"] else (" (set)" if api_key(sid) else " (not set)")
        print(f"{sid:<10} {s['name']:<30} key: {key}{have} · commercial: {s['commercial']}\n"
              f"           {s['licence'][0]} {s['licence'][1]}\n           {s['about']}")
    return 0


def cmd_search(args) -> int:
    sources = [s.strip() for s in args.sources.split(",")] if args.sources else default_sources()
    bad = [s for s in sources if s not in SOURCES]
    if bad:
        print(f"unknown source(s): {', '.join(bad)}; known: {', '.join(SOURCES)}", file=sys.stderr)
        return 2
    opts = {"orientation": args.orientation, "min_width": args.min_width, "commercial": args.commercial,
            "allow_nd": args.allow_nd}
    http = FF.Http(delay=args.delay, max_retry_after=args.wait_429)
    report = run_search(http, args.query, sources, args.limit, opts)
    path = Path(args.results)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = merge_results(None if args.replace else load_results(path), report)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print_report(report)
    print(f"# results: {path} ({len(data['results'])} kept across searches)")
    return 3 if report["sources"] and all(v["status"] != "ok" for v in report["sources"].values()) else 0


def cmd_sheet(args) -> int:
    data = load_results(Path(args.results))
    if not data:
        print(f"no results file at {args.results}: run search first", file=sys.stderr)
        return 1
    out = Path(args.out or Path(args.results).parent)
    out.mkdir(parents=True, exist_ok=True)
    p = out / "contact_sheet.html"
    p.write_text(sheet_html(data), encoding="utf-8")
    print(p)
    return 0


def cmd_download(args) -> int:
    data = load_results(Path(args.results)) or {"results": []}
    by_id = {r["id"]: r for r in data["results"]}
    http = FF.Http(delay=args.delay, max_retry_after=args.wait_429)
    out, failed = Path(args.out), 0
    for rid in args.ids:
        rec = by_id.get(rid)
        if not rec:
            print(f"{rid}: not in {args.results}; run search first (ids look like openverse:..., met:12345)",
                  file=sys.stderr)
            failed += 1
            continue
        try:
            path = download_one(http, rec, out, args.size, args.max_mb, args.dry_run)
        except FF.FootageError as e:
            print(redact(e), file=sys.stderr)
            failed += 1
            continue
        if path:
            print(f"{rid} -> {path} ({path.stat().st_size / 1048576:.1f} MB) · {licence_text(rec['licence'])}")
    if not args.dry_run and out.is_dir():
        print(f"# credits: {write_credits(out)}")
    return 1 if failed else 0


def cmd_credits(args) -> int:
    p = write_credits(Path(args.dir))
    print(p.read_text(encoding="utf-8"))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sources", help="list the photo sources and their licences (offline)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_sources)

    def net(p):
        p.add_argument("--results", default=str(DEFAULT_RESULTS), help="results file (default %(default)s)")
        p.add_argument("--delay", type=float, default=1.0, help="seconds between requests to one host")
        p.add_argument("--wait-429", type=float, default=FF.MAX_RETRY_AFTER, help="longest Retry-After to wait")

    p = sub.add_parser("search", help="search the photo sources (network)")
    p.add_argument("query")
    p.add_argument("--sources", help=f"comma list from: {', '.join(SOURCES)} (default: every one usable here)")
    p.add_argument("--limit", type=int, default=8, help="results kept per source")
    p.add_argument("--orientation", choices=("landscape", "portrait", "square"))
    p.add_argument("--min-width", type=int, help="long side at least this many pixels")
    p.add_argument("--commercial", action="store_true", help="keep only licences that allow commercial use")
    p.add_argument("--allow-nd", action="store_true", help="keep no-derivatives licences (reference only)")
    p.add_argument("--replace", action="store_true", help="overwrite the results file instead of merging")
    net(p)
    p.set_defaults(fn=cmd_search)
    p = sub.add_parser("sheet", help="contact_sheet.html from the results (offline)")
    p.add_argument("results", nargs="?", default=str(DEFAULT_RESULTS))
    p.add_argument("--out")
    p.set_defaults(fn=cmd_sheet)
    p = sub.add_parser("download", help="download result ids with a licence sidecar and ATTRIBUTION.md (network)")
    p.add_argument("ids", nargs="+")
    p.add_argument("--out", required=True)
    p.add_argument("--size", choices=("full", "large"), default="full",
                   help="full = original file; large = ~2400 px where the source offers it (Pexels, Unsplash)")
    p.add_argument("--max-mb", type=float, default=FILE_CAP_MB)
    p.add_argument("--dry-run", action="store_true")
    net(p)
    p.set_defaults(fn=cmd_download)
    p = sub.add_parser("credits", help="rebuild DIR/ATTRIBUTION.md from the sidecars (offline)")
    p.add_argument("dir")
    p.set_defaults(fn=cmd_credits)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
