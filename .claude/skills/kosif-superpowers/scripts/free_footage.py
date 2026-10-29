#!/usr/bin/env python3
"""Free footage: a database of open-licence video sources, plus search and download with a licence record per clip.

مصادر فيديو مفتوحة الترخيص للمونتاج: قاعدة بيانات بالمواقع وترخيص كل موقع، وبحث وتحميل يحفظ مع كل لقطة ترخيصها وسطر النسب.

Subcommands:
  sources [--find WORD] [--status ok] [--searchable] [--json]
          list or filter data/free_footage_sources.json (offline)
  check   validate the database: required keys, enums, unique ids, template placeholders (offline)
  probe   [--sources a,b] [--out DIR]
          live reachability check of every source's probe URLs; writes <out>/probe-<YYYYMMDD>.json (network)
  search  QUERY [--sources a,b] [--min-height N] [--orientation portrait] [--limit N] [--commercial] [--no-ai]
          key-less APIs (Wikimedia Commons, Internet Archive, NASA), Pexels/Pixabay when PEXELS_API_KEY /
          PIXABAY_API_KEY are in the environment, and the Mixkit and Coverr search pages; saves the results to
          out/free-footage/last_search.json (network)
  download TARGET... --out DIR
          a result id from the last search (wikimedia:81916645) or a page/file URL; saves the file, a sidecar
          <file>.json with licence and attribution, and rebuilds <out>/ATTRIBUTION.md (network)
  credits DIR
          rebuild DIR/ATTRIBUTION.md from the sidecars (offline)

Licences come from what each source declares (Commons extmetadata, the Archive's licenseurl, the Mixkit clip page's
notice, the Coverr and Pexels/Pixabay licences, NASA's media guidelines). The tool records them; it does not grant
them. ND licences are dropped by default (a montage is an adaptation); NC and Mixkit "Restricted" clips are kept but
marked commercial=false, and --commercial drops them. Pinterest is never downloaded: it is not a licence source.

Keys are read from the environment only, never printed or stored. One request per host per --delay seconds
(default 1.0), a timeout on every request, a descriptive User-Agent, and a size cap on pages and files.
Python 3.8+ standard library only (ffprobe is used when present to measure downloads).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html as _html
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
DB_PATH = SK / "data" / "free_footage_sources.json"
SCHEMA_PATH = SK / "schemas" / "free_footage_sources.schema.json"
DB_SCHEMA = "kosif.free-footage-sources.v1"
RESULTS_SCHEMA = "kosif.free_footage.results.v1"
ASSET_SCHEMA = "kosif.free_footage.asset.v1"
PROBE_SCHEMA = "kosif.free_footage.probe.v1"
DEFAULT_RESULTS = Path("out") / "free-footage" / "last_search.json"
DEFAULT_PROBE_DIR = Path("out") / "free-footage"
UA = "KOSIF-free-footage/1.0 (+https://github.com/kosif199022-jpg/kosif-tool; open-licence footage for montage)"
PAGE_CAP_MB = 40          # the Coverr search page alone is about 11 MB
MAX_RETRY_AFTER = 30.0    # seconds we are willing to wait after a 429/503
VIDEO_EXT = (".mp4", ".m4v", ".mov", ".webm", ".mkv", ".ogv", ".ogg", ".mpeg", ".mpg", ".avi")
KEY_ENV = {"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY"}

REQUIRED_TOP = ("schema", "checked_on", "about", "notice", "template_fields", "sources")
REQUIRED_SOURCE = ("id", "name", "url", "category", "licence_source", "licence", "attribution", "commercial_use",
                   "commercial_note", "modification", "video_kinds", "strengths", "search_url", "search_url_checked",
                   "api", "download", "max_resolution", "formats", "tool", "probes", "reachability", "notes")
REQUIRED_NESTED = {
    "licence": ("name", "url", "per_item", "summary"),
    "attribution": ("required", "per_item", "template"),
    "api": ("endpoint", "key_required", "key_env", "docs", "notes"),
    "tool": ("search", "download"),
    "reachability": ("checked_on", "status", "http", "detail"),
}
ENUMS = {
    "category": ("free-stock", "freemium-stock", "open-collection", "public-agency", "media-api", "discovery-only",
                 "paid-stock"),
    "commercial_use": ("yes", "no", "per-item", "n/a"),
    "modification": ("yes", "no", "per-item", "n/a"),
    "tool.search": ("api", "api-key", "scrape", "none"),
    "tool.download": ("api", "direct", "none"),
    "reachability.status": ("ok", "partial", "blocked", "timeout", "needs-key", "paid", "not-checked"),
}
TEMPLATE_FIELDS = ("title", "author", "source", "licence", "licence_url", "page_url")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ENV_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _sibling(name: str):
    """Import a script that lives next to this one (stock_fetch, _secrets) only when a command needs it."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    return importlib.import_module(name)


class FootageError(Exception):
    """A failure the user can act on (exit 1 with the message)."""


class HttpError(FootageError):
    def __init__(self, url: str, status, detail: str = ""):
        self.url, self.status = url, status
        super().__init__(f"HTTP {status} from {redact(url)}" + (f": {detail}" if detail else ""))


# ------------------------------------------------------------------------------------------------- database

def load_db(path: Path = DB_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sources_by_id(db: dict) -> dict:
    return {s["id"]: s for s in db.get("sources", [])}


def template_placeholders(template: str) -> list:
    return re.findall(r"\{(\w+)\}", template or "")


def validate_db(db: dict) -> list:
    """Every structural problem in the database (empty list = valid). Mirrors schemas/free_footage_sources.schema.json."""
    errs = []
    if not isinstance(db, dict):
        return ["the database must be a JSON object"]
    for k in REQUIRED_TOP:
        if k not in db:
            errs.append(f"missing top-level key {k!r}")
    if db.get("schema") != DB_SCHEMA:
        errs.append(f"schema must be {DB_SCHEMA}")
    if not DATE_RE.match(str(db.get("checked_on", ""))):
        errs.append("checked_on must be YYYY-MM-DD")
    fields = db.get("template_fields") or []
    if set(fields) - set(TEMPLATE_FIELDS):
        errs.append(f"template_fields may only name {', '.join(TEMPLATE_FIELDS)}")
    srcs = db.get("sources")
    if not isinstance(srcs, list) or not srcs:
        return errs + ["sources must be a non-empty list"]
    ids, names = set(), set()
    for i, s in enumerate(srcs):
        if not isinstance(s, dict):
            errs.append(f"sources[{i}] must be an object")
            continue
        sid = s.get("id", f"sources[{i}]")
        for k in REQUIRED_SOURCE:
            if k not in s:
                errs.append(f"{sid}: missing {k!r}")
        extra = set(s) - set(REQUIRED_SOURCE)
        if extra:
            errs.append(f"{sid}: unknown keys {sorted(extra)}")
        if not isinstance(sid, str) or not ID_RE.match(sid):
            errs.append(f"{sid}: id must be kebab-case")
        if sid in ids:
            errs.append(f"{sid}: duplicate id")
        ids.add(sid)
        name = str(s.get("name", "")).strip().lower()
        if not name:
            errs.append(f"{sid}: name must be non-empty")
        elif name in names:
            errs.append(f"{sid}: duplicate name {s.get('name')!r}")
        names.add(name)
        if not str(s.get("url", "")).startswith("https://"):
            errs.append(f"{sid}: url must be https")
        for key, keys in REQUIRED_NESTED.items():
            sub = s.get(key)
            if not isinstance(sub, dict):
                errs.append(f"{sid}: {key} must be an object")
                continue
            for k in keys:
                if k not in sub:
                    errs.append(f"{sid}: {key}.{k} missing")
            if set(sub) - set(keys):
                errs.append(f"{sid}: {key} has unknown keys {sorted(set(sub) - set(keys))}")
        for key, allowed in ENUMS.items():
            if "." in key:
                a, b = key.split(".")
                val = (s.get(a) or {}).get(b) if isinstance(s.get(a), dict) else None
            else:
                val = s.get(key)
            if val not in allowed:
                errs.append(f"{sid}: {key} must be one of {allowed} (got {val!r})")
        for key in ("licence_source", "search_url_checked"):
            if not isinstance(s.get(key), bool):
                errs.append(f"{sid}: {key} must be true or false")
        lic = s.get("licence") if isinstance(s.get("licence"), dict) else {}
        if not str(lic.get("url", "")).startswith("https://"):
            errs.append(f"{sid}: licence.url must be https")
        if not isinstance(lic.get("per_item"), bool):
            errs.append(f"{sid}: licence.per_item must be true or false")
        att = s.get("attribution") if isinstance(s.get("attribution"), dict) else {}
        for k in ("required", "per_item"):
            if not isinstance(att.get(k), bool):
                errs.append(f"{sid}: attribution.{k} must be true or false")
        tpl = att.get("template")
        if tpl is not None:
            if not isinstance(tpl, str) or not tpl.strip():
                errs.append(f"{sid}: attribution.template must be a non-empty string or null")
            else:
                bad = set(template_placeholders(tpl)) - set(fields or TEMPLATE_FIELDS)
                if bad:
                    errs.append(f"{sid}: attribution.template uses unknown placeholders {sorted(bad)}")
        surl = s.get("search_url")
        if surl is not None and (not str(surl).startswith("https://") or "{query}" not in str(surl)):
            errs.append(f"{sid}: search_url must be an https URL with a {{query}} placeholder, or null")
        api = s.get("api") if isinstance(s.get("api"), dict) else {}
        if not isinstance(api.get("key_required"), bool):
            errs.append(f"{sid}: api.key_required must be true or false")
        if api.get("key_env") is not None and not ENV_RE.match(str(api.get("key_env"))):
            errs.append(f"{sid}: api.key_env must be an environment variable name")
        tool = s.get("tool") if isinstance(s.get("tool"), dict) else {}
        if tool.get("search") == "api-key" and not (api.get("key_required") and api.get("key_env")):
            errs.append(f"{sid}: tool.search api-key needs api.key_required true and api.key_env")
        if tool.get("search") in ("api", "api-key") and not api.get("endpoint"):
            errs.append(f"{sid}: tool.search {tool.get('search')} needs api.endpoint")
        if s.get("licence_source") is False and (tool.get("download") != "none" or s.get("commercial_use") != "n/a"):
            errs.append(f"{sid}: a source that is not a licence source must have tool.download none and commercial_use n/a")
        for k in ("video_kinds", "formats", "probes"):
            if not isinstance(s.get(k), list):
                errs.append(f"{sid}: {k} must be a list")
        for p in s.get("probes") or []:
            if not (isinstance(p, dict) and p.get("what") and str(p.get("url", "")).startswith("https://")):
                errs.append(f"{sid}: every probe needs what and an https url")
            elif set(p) - {"what", "url", "expect"}:
                errs.append(f"{sid}: probe has unknown keys {sorted(set(p) - {'what', 'url', 'expect'})}")
            elif "expect" in p and not isinstance(p["expect"], int):
                errs.append(f"{sid}: probe expect must be an integer status")
        reach = s.get("reachability") if isinstance(s.get("reachability"), dict) else {}
        if not DATE_RE.match(str(reach.get("checked_on", ""))):
            errs.append(f"{sid}: reachability.checked_on must be YYYY-MM-DD")
        if reach.get("http") is not None and not isinstance(reach.get("http"), int):
            errs.append(f"{sid}: reachability.http must be an integer or null")
    return errs


# ------------------------------------------------------------------------------------------------- secrets

def _keys_in_env() -> list:
    return [os.environ[v] for v in KEY_ENV.values() if os.environ.get(v)]


def redact(text) -> str:
    """Remove API keys from a URL or message: key=... query values and any key value present in the environment."""
    s = str(text)
    s = re.sub(r"(?i)([?&](?:key|api_key|apikey|token|access_token|auth|signature|sig)=)[^&#\s]+", r"\1***", s)
    for k in _keys_in_env():
        if len(k) >= 6:
            s = s.replace(k, "***")
    return s


def api_key(source: str, environ=None) -> str | None:
    env = os.environ if environ is None else environ
    v = (env.get(KEY_ENV[source]) or "").strip() if source in KEY_ENV else ""
    return v or None


# ------------------------------------------------------------------------------------------------- HTTP

class Http:
    """Polite HTTP: one request per host per `delay` seconds, timeouts, a User-Agent, size caps, one retry on 429/503.

    `transport(request, timeout)` returns a urlopen-like response; tests pass a fake. `sleep` and `clock` are
    injectable so the rate limit is testable without waiting."""

    def __init__(self, delay: float = 1.0, timeout: float = 20.0, transport=None, sleep=time.sleep,
                 clock=time.monotonic, retries: int = 1):
        self.delay, self.timeout, self.retries = max(0.0, float(delay)), float(timeout), int(retries)
        self.transport = transport or (lambda req, timeout: urllib.request.urlopen(req, timeout=timeout))
        self.sleep, self.clock = sleep, clock
        self._last = {}
        self.calls = 0

    def _wait(self, host: str) -> None:
        last = self._last.get(host)
        if last is not None:
            gap = self.delay - (self.clock() - last)
            if gap > 0:
                self.sleep(gap)
        self._last[host] = self.clock()

    def open(self, url: str, headers: dict | None = None, method: str = "GET"):
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
        hdrs = {"User-Agent": UA, "Accept": "*/*"}
        hdrs.update(headers or {})
        attempt = 0
        while True:
            self._wait(host)
            self.calls += 1
            req = urllib.request.Request(url, headers=hdrs, method=method)
            try:
                resp = self.transport(req, self.timeout)
            except urllib.error.HTTPError as e:
                status, retry_after = e.code, (e.headers.get("Retry-After") if e.headers else None)
                _close(e)
            except (urllib.error.URLError, OSError, ValueError) as e:  # DNS, refused, TLS, timeout
                reason = getattr(e, "reason", e)
                raise HttpError(url, type(reason).__name__ if not isinstance(reason, str) else "error", str(reason)[:160]) from None
            else:
                status = getattr(resp, "status", None) or getattr(resp, "code", 200)
                retry_after = resp.headers.get("Retry-After") if getattr(resp, "headers", None) else None
                if status < 400:
                    return resp
                _close(resp)
            if status in (429, 503) and attempt < self.retries:
                attempt += 1
                try:
                    wait = float(retry_after) if retry_after else self.delay * 4 or 2.0
                except ValueError:
                    wait = self.delay * 4 or 2.0
                if wait > MAX_RETRY_AFTER:
                    raise HttpError(url, status, f"rate limited; Retry-After {retry_after}s is too long, try later")
                self.sleep(max(wait, 0.5))
                continue
            raise HttpError(url, status)

    def get_bytes(self, url: str, headers: dict | None = None, cap_mb: float = PAGE_CAP_MB) -> bytes:
        resp = self.open(url, headers)
        try:
            cap = int(cap_mb * 1048576)
            n = resp.headers.get("Content-Length") if getattr(resp, "headers", None) else None
            if n and n.isdigit() and int(n) > cap:
                raise FootageError(f"{redact(url)} is {int(n) / 1048576:.1f} MB, over the {cap_mb:g} MB page cap")
            body = resp.read(cap + 1)
            if len(body) > cap:
                raise FootageError(f"{redact(url)} is larger than the {cap_mb:g} MB page cap")
            return body
        finally:
            _close(resp)

    def get_text(self, url: str, headers: dict | None = None) -> str:
        return self.get_bytes(url, headers).decode("utf-8", "replace")

    def get_json(self, url: str, headers: dict | None = None):
        body = self.get_bytes(url, {"Accept": "application/json", **(headers or {})})
        try:
            return json.loads(body.decode("utf-8", "replace"))
        except ValueError:
            raise FootageError(f"{redact(url)} did not return JSON (a block page or a changed API)") from None


def _close(resp) -> None:
    try:
        resp.close()
    except Exception:
        pass


# ------------------------------------------------------------------------------------------------- licences

CC_URL_RE = re.compile(r"creativecommons\.org/(licenses|publicdomain)/([a-z-]+)(?:/(\d(?:\.\d)?))?(/igo)?", re.I)
CC_NAME_RE = re.compile(r"\bCC[- ]?(BY(?:[- ](?:NC|ND|SA))*)(?:[- ](\d\.\d))?(?:[- ](IGO))?\b", re.I)


def licence_record(name, url=None, *, attribution=None, commercial=None, derivatives=None, share_alike=None,
                   verified=True, note="") -> dict:
    return {"name": name, "url": url, "attribution_required": attribution, "commercial": commercial,
            "derivatives": derivatives, "share_alike": share_alike, "verified": verified, "note": note}


def classify_licence(name=None, url=None) -> dict:
    """Read a licence from a Creative Commons URL or a short name (Commons LicenseShortName, an Archive licenseurl).

    Returns licence_record(...) with attribution_required / commercial / derivatives / share_alike as True, False or
    None (unknown). Unknown licences come back with verified=False."""
    url = (url or "").strip() or None
    raw_name = re.sub(r"\s+", " ", str(name or "")).strip()
    if url and url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    m = CC_URL_RE.search(url or "")
    if m:
        kind, parts, ver, igo = m.group(1).lower(), m.group(2).lower(), m.group(3), m.group(4)
        if kind == "publicdomain" or parts == "publicdomain":  # licenses/publicdomain/ is the retired CC PD dedication
            if parts == "zero":
                return licence_record("CC0 " + (ver or "1.0"), url, attribution=False, commercial=True, derivatives=True,
                                      share_alike=False)
            if parts == "mark":
                return licence_record("Public Domain Mark " + (ver or "1.0"), url, attribution=False, commercial=True,
                                      derivatives=True, share_alike=False)
            return licence_record(raw_name or "Public domain", url, attribution=False, commercial=True,
                                  derivatives=True, share_alike=False)
        return _cc_flags(parts.split("-"), ver, bool(igo), url)
    low = raw_name.lower()
    if re.fullmatch(r"cc0(?: 1\.0)?(?: universal)?", low) or "public domain dedication" in low:
        return licence_record("CC0 1.0" if "1.0" in low or low == "cc0" else raw_name, url, attribution=False,
                              commercial=True, derivatives=True, share_alike=False)
    if low in ("public domain", "pd", "pdm") or low.startswith(("public domain", "pd-")):
        return licence_record(raw_name or "Public domain", url, attribution=False, commercial=True, derivatives=True,
                              share_alike=False)
    m = CC_NAME_RE.search(raw_name)
    if m:
        return _cc_flags(re.split(r"[- ]", m.group(1).lower()), m.group(2), bool(m.group(3)), url)
    return licence_record(raw_name or "unknown", url, verified=False,
                          note="licence not recognised: read it on the page before use")


def _cc_flags(parts: list, ver, igo: bool, url) -> dict:
    parts = [p for p in parts if p]
    name = "CC " + "-".join(p.upper() for p in parts) + (f" {ver}" if ver else "") + (" IGO" if igo else "")
    return licence_record(name, url, attribution="by" in parts, commercial="nc" not in parts,
                          derivatives="nd" not in parts, share_alike="sa" in parts)


def source_licence(source: str, db_source: dict | None = None, **over) -> dict:
    """The licence a whole source grants (Pexels, Pixabay, Coverr, NASA), from the database record."""
    lic = (db_source or {}).get("licence") or {}
    fixed = {
        "pexels": dict(attribution=False, commercial=True, derivatives=True, share_alike=False),
        "pixabay": dict(attribution=False, commercial=True, derivatives=True, share_alike=False),
        "coverr": dict(attribution=False, commercial=True, derivatives=True, share_alike=False,
                       note="Coverr License: no AI training or datasets, no competing service, no resale as is"),
        "nasa": dict(attribution=True, commercial=True, derivatives=True, share_alike=False,
                     note="acknowledge NASA; no implied endorsement; NASA logos and third-party marked material need permission"),
    }.get(source, {})
    fixed.update(over)
    return licence_record(lic.get("name") or source, lic.get("url"), **fixed)


MIXKIT_FREE = "Mixkit Stock Video Free License"
MIXKIT_RESTRICTED = "Mixkit Restricted License"


def mixkit_licence(notice) -> dict:
    url = "https://mixkit.co/license/"
    n = (notice or "").strip().lower()
    if "restricted" in n:
        return licence_record(MIXKIT_RESTRICTED, url + "#videoRestricted", attribution=False, commercial=False,
                              derivatives=True, share_alike=False,
                              note="the free 720p file is for personal use only; commercial use needs a paid Envato licence")
    if n in ("free", "mixkit free license") or "free license" in n:
        return licence_record(MIXKIT_FREE, url + "#videoFree", attribution=False, commercial=True, derivatives=True,
                              share_alike=False, note="no redistribution as stock")
    return licence_record("Mixkit licence (Free or Restricted: read the clip page)", url, attribution=False,
                          commercial=None, derivatives=True, share_alike=False, verified=False,
                          note="the search page did not name this clip's licence; download reads it from the clip page")


# ------------------------------------------------------------------------------------------------- attribution

def clean_text(value) -> str:
    """Plain text from an API field that may hold HTML (Commons Artist/Credit)."""
    s = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


def format_attribution(template, *, title=None, author=None, source=None, licence=None, licence_url=None,
                       page_url=None) -> str:
    """Fill a credit template from data/free_footage_sources.json; fragments whose field is missing are dropped."""
    fields = {"title": title, "author": author, "source": source, "licence": licence, "licence_url": licence_url,
              "page_url": page_url}
    fields = {k: clean_text(v) for k, v in fields.items() if v not in (None, "")}
    tpl = template or '"{title}" by {author}, {licence} ({licence_url}), from {source}: {page_url}'
    if "author" not in fields:
        tpl = re.sub(r"\s+by \{author\}", "", tpl)
        tpl = re.sub(r"[;,]?\s*original creator: \{author\}", "; original creator: unknown (trace it)", tpl)
        tpl = re.sub(r"\s*\(\{author\}\)", "", tpl)
        tpl = re.sub(r",?\s*\{author\},?", ",", tpl)
    if "licence_url" not in fields:
        tpl = re.sub(r"\s*\(\{licence_url\}\)", "", tpl)
    if "title" not in fields:
        tpl = tpl.replace('"{title}"', "Untitled clip")
    out = re.sub(r"\{(\w+)\}", lambda m: fields.get(m.group(1), ""), tpl)
    out = re.sub(r"\s+([,;:)])", r"\1", out)
    out = re.sub(r",\s*,", ",", out)
    out = re.sub(r"\(\s*\)", "", out)
    return re.sub(r"\s+", " ", out).strip(" ,;")


def make_result(db: dict, source: str, native_id, *, title, page_url, file_url, licence: dict, author=None,
                width=None, height=None, duration=None, mime=None, size=None, quality=None, flags=(),
                extra=None) -> dict:
    src = sources_by_id(db).get(source) or {}
    tpl = (src.get("attribution") or {}).get("template")
    title = clean_text(title) or None
    author = clean_text(author) or None
    rec = {
        "id": f"{source}:{native_id}",
        "source": source,
        "source_name": src.get("name", source),
        "title": title,
        "page_url": page_url,
        "file_url": file_url,
        "width": _int(width),
        "height": _int(height),
        "duration": _float(duration),
        "quality": _int(quality),
        "mime": mime,
        "bytes": _int(size),
        "author": author,
        "licence": licence,
        "attribution": format_attribution(tpl, title=title, author=author, source=src.get("name", source),
                                          licence=licence.get("name"), licence_url=licence.get("url"),
                                          page_url=page_url),
        "flags": sorted(set(flags)),
    }
    if extra:
        rec.update(extra)
    return rec


def _int(v):
    try:
        return int(float(v)) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _float(v):
    if v in (None, ""):
        return None
    if isinstance(v, str) and ":" in v:  # 0:00:41 or 1:23:45.5
        try:
            secs = 0.0
            for part in v.strip().split(":"):
                secs = secs * 60 + float(part)
            return round(secs, 3)
        except ValueError:
            return None
    if isinstance(v, str) and v.startswith("PT"):  # ISO 8601 PT0M16S
        m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:([\d.]+)S)?", v)
        if m:
            h, mi, s = (float(x) if x else 0.0 for x in m.groups())
            return round(h * 3600 + mi * 60 + s, 3)
        return None
    try:
        return round(float(v), 3)
    except (TypeError, ValueError):
        return None


def strip_tracking(url: str) -> str:
    """Drop utm_* parameters (Commons adds them to imageinfo URLs)."""
    parts = urllib.parse.urlsplit(url)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True) if not k.startswith("utm_")]
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(q)))


def https(url):
    return "https://" + url[7:] if isinstance(url, str) and url.startswith("http://") else url


# ------------------------------------------------------------------------------------------------- Wikimedia Commons

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
COMMONS_IIPROP = "url|size|mime|mediatype|extmetadata"
COMMONS_META = "ObjectName|LicenseShortName|LicenseUrl|Artist|Credit|AttributionRequired|UsageTerms|License"


def commons_search_url(query: str, limit: int) -> str:
    q = {"action": "query", "format": "json", "formatversion": "2", "generator": "search",
         "gsrsearch": f"{query} filetype:video", "gsrnamespace": "6", "gsrlimit": str(max(1, min(limit, 50))),
         "prop": "imageinfo", "iiprop": COMMONS_IIPROP, "iiextmetadatafilter": COMMONS_META}
    return COMMONS_API + "?" + urllib.parse.urlencode(q)


def commons_lookup_url(*, titles=None, pageids=None) -> str:
    q = {"action": "query", "format": "json", "formatversion": "2", "prop": "imageinfo", "iiprop": COMMONS_IIPROP,
         "iiextmetadatafilter": COMMONS_META}
    if titles:
        q["titles"] = titles
    if pageids:
        q["pageids"] = str(pageids)
    return COMMONS_API + "?" + urllib.parse.urlencode(q)


def parse_wikimedia(db: dict, data: dict) -> list:
    pages = ((data or {}).get("query") or {}).get("pages") or []
    if isinstance(pages, dict):  # formatversion=1
        pages = list(pages.values())
    pages = sorted(pages, key=lambda p: p.get("index", 0))
    out = []
    for p in pages:
        info = (p.get("imageinfo") or [None])[0]
        if not info or p.get("missing"):
            continue
        mime = info.get("mime") or ""
        if (info.get("mediatype") or "").upper() != "VIDEO" and not mime.startswith("video/"):
            continue
        meta = info.get("extmetadata") or {}
        mv = lambda k: (meta.get(k) or {}).get("value")  # noqa: E731
        lic = classify_licence(clean_text(mv("LicenseShortName")), clean_text(mv("LicenseUrl")) or None)
        req = str(mv("AttributionRequired") or "").strip().lower()
        if req in ("true", "false"):
            lic["attribution_required"] = req == "true"
        title = clean_text(mv("ObjectName")) or re.sub(r"^File:|\.[A-Za-z0-9]+$", "", p.get("title", ""))
        out.append(make_result(db, "wikimedia", p.get("pageid"), title=title,
                               page_url=info.get("descriptionurl"), file_url=strip_tracking(info.get("url", "")),
                               licence=lic, author=mv("Artist"), width=info.get("width"), height=info.get("height"),
                               duration=info.get("duration"), mime=mime, size=info.get("size"),
                               extra={"native": {"file_title": p.get("title")}}))
    return out


def search_wikimedia(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    return parse_wikimedia(db, http.get_json(commons_search_url(query, limit * 2)))


def commons_title_from_url(url: str) -> str | None:
    parts = urllib.parse.urlsplit(url)
    host, path = (parts.hostname or "").lower(), urllib.parse.unquote(parts.path)
    if host == "commons.wikimedia.org":
        m = re.search(r"/wiki/(File:.+)$", path)
        if m:
            return m.group(1).replace(" ", "_")
        q = dict(urllib.parse.parse_qsl(parts.query))
        if q.get("title", "").startswith("File:"):
            return q["title"]
    if host == "upload.wikimedia.org":
        segs = [s for s in path.split("/") if s]
        if "transcoded" in segs:
            i = segs.index("transcoded")
            if len(segs) > i + 3:
                return "File:" + segs[i + 3]
        elif segs:
            return "File:" + segs[-1]
    return None


# ------------------------------------------------------------------------------------------------- Internet Archive

ARCHIVE_SEARCH = "https://archive.org/advancedsearch.php"


def archive_search_url(query: str, limit: int, any_licence: bool = False) -> str:
    q = f"({query}) AND mediatype:(movies)" + ("" if any_licence else " AND licenseurl:*")
    params = [("q", q)] + [("fl[]", f) for f in ("identifier", "title", "creator", "licenseurl", "year")] + \
        [("rows", str(max(1, min(limit, 100)))), ("output", "json")]
    return ARCHIVE_SEARCH + "?" + urllib.parse.urlencode(params)


def parse_archive_search(data: dict) -> list:
    return [d for d in (((data or {}).get("response") or {}).get("docs") or []) if d.get("identifier")]


def pick_archive_file(files: list, max_bytes: int | None = None) -> dict | None:
    """The best video file of an item: highest resolution that fits under max_bytes (else the smallest one)."""
    vids = []
    for f in files or []:
        name = str(f.get("name") or "")
        if not name.lower().endswith(VIDEO_EXT) or ".thumbs/" in name or name.lower().endswith(".ogg") and not f.get("height"):
            continue
        h, w, size = _int(f.get("height")) or 0, _int(f.get("width")) or 0, _int(f.get("size"))
        mp4 = name.lower().endswith((".mp4", ".m4v"))
        vids.append(((h, w, mp4, f.get("source") == "original"), size, f))
    if not vids:
        return None
    vids.sort(key=lambda v: v[0], reverse=True)
    if max_bytes:
        for _key, size, f in vids:
            if size is None or size <= max_bytes:
                return f
        return min(vids, key=lambda v: v[1] or 0)[2]
    return vids[0][2]


def archive_result(db: dict, doc: dict, meta: dict, max_bytes: int | None = None) -> dict | None:
    ident = doc.get("identifier") or (meta.get("metadata") or {}).get("identifier")
    md = meta.get("metadata") or {}
    f = pick_archive_file(meta.get("files") or [], max_bytes)
    if not ident or not f:
        return None
    licurl = doc.get("licenseurl") or md.get("licenseurl")
    lic = classify_licence(None, licurl) if licurl else licence_record(
        "unknown (no licenseurl)", None, verified=False, note="the uploader set no licence: rights unknown")
    creator = doc.get("creator") or md.get("creator")
    if isinstance(creator, list):
        creator = ", ".join(map(str, creator))
    fname = f["name"]
    return make_result(db, "archive", ident, title=doc.get("title") or md.get("title") or ident,
                       page_url=f"https://archive.org/details/{ident}",
                       file_url=f"https://archive.org/download/{urllib.parse.quote(ident)}/{urllib.parse.quote(fname)}",
                       licence=lic, author=creator, width=f.get("width"), height=f.get("height"),
                       duration=f.get("length"), size=f.get("size"),
                       extra={"native": {"file": fname, "format": f.get("format")}})


def search_archive(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    docs = parse_archive_search(http.get_json(archive_search_url(query, limit * 2, opts.get("any_licence"))))
    out = []
    for doc in docs[: limit * 2]:
        try:
            meta = http.get_json(f"https://archive.org/metadata/{urllib.parse.quote(doc['identifier'])}")
        except FootageError as e:
            opts.setdefault("warnings", []).append(f"archive {doc['identifier']}: {e}")
            continue
        r = archive_result(db, doc, meta, opts.get("max_bytes"))
        if r:
            out.append(r)
    return out


# ------------------------------------------------------------------------------------------------- NASA

NASA_SEARCH = "https://images-api.nasa.gov/search"


def nasa_search_url(query: str | None = None, limit: int = 10, nasa_id: str | None = None) -> str:
    q = {"media_type": "video", "page_size": str(max(1, min(limit, 100)))}
    if query:
        q["q"] = query
    if nasa_id:
        q["nasa_id"] = nasa_id
    return NASA_SEARCH + "?" + urllib.parse.urlencode(q)


def parse_nasa_search(data: dict) -> list:
    out = []
    for it in ((data or {}).get("collection") or {}).get("items") or []:
        d = (it.get("data") or [{}])[0]
        if d.get("media_type") == "video" and d.get("nasa_id"):
            out.append(d)
    return out


NASA_VARIANTS = ("~orig.mp4", "~large.mp4", "~medium.mp4", "~mobile.mp4", "~small.mp4")


def nasa_variants(asset: dict) -> tuple:
    """([video URLs, largest first], metadata.json URL) from https://images-api.nasa.gov/asset/<nasa_id>."""
    hrefs = [https(i.get("href")) for i in ((asset or {}).get("collection") or {}).get("items") or [] if i.get("href")]
    meta = next((h for h in hrefs if h.endswith("/metadata.json")), None)
    vids = [h for tag in NASA_VARIANTS for h in hrefs if h.endswith(tag)]
    if not vids:
        vids = [h for h in hrefs if h.lower().endswith(VIDEO_EXT) and "~preview" not in h][:1]
    return vids, meta


def pick_nasa_asset(asset: dict) -> tuple:
    """(video URL, metadata.json URL): ~orig.mp4, else the next largest variant."""
    vids, meta = nasa_variants(asset)
    return (vids[0] if vids else None), meta


def parse_nasa_metadata(meta: dict) -> dict:
    g = lambda *ks: next((meta.get(k) for k in ks if meta.get(k) not in (None, "")), None)  # noqa: E731
    w, h = g("QuickTime:ImageWidth", "QuickTime:SourceImageWidth"), g("QuickTime:ImageHeight", "QuickTime:SourceImageHeight")
    if not (w and h) and isinstance(meta.get("Composite:ImageSize"), str):
        m = re.match(r"(\d+)\s*[x×]\s*(\d+)", meta["Composite:ImageSize"])
        if m:
            w, h = m.groups()
    dur = g("QuickTime:Duration", "QuickTime:MediaDuration", "QuickTime:TrackDuration")
    if isinstance(dur, str) and dur.endswith(" s"):
        dur = dur[:-2]
    return {"width": _int(w), "height": _int(h), "duration": _float(dur)}


def nasa_result(db: dict, d: dict, video_url: str, dims: dict | None = None, alternates=()) -> dict:
    nid = d["nasa_id"]
    author = d.get("secondary_creator") or d.get("photographer") or (f"NASA {d['center']}" if d.get("center") else "NASA")
    flags = ["check-third-party-credit"] if re.search(r"©|copyright", str(d.get("description", "")), re.I) else []
    dims = dims or {}
    return make_result(db, "nasa", nid, title=d.get("title") or nid, page_url=f"https://images.nasa.gov/details/{nid}",
                       file_url=video_url, licence=source_licence("nasa", sources_by_id(db).get("nasa")),
                       author=author, width=dims.get("width"), height=dims.get("height"),
                       duration=dims.get("duration"), mime="video/mp4", flags=flags,
                       extra={"native": {"center": d.get("center"), "date_created": d.get("date_created")},
                              **({"alternates": [a for a in alternates if a != video_url]} if alternates else {})})


def search_nasa(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    out = []
    for d in parse_nasa_search(http.get_json(nasa_search_url(query, limit * 2)))[: limit * 2]:
        try:
            vids, meta_url = nasa_variants(http.get_json(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(d['nasa_id'])}"))
            video = vids[0] if vids else None
            dims = {}
            if video and meta_url and (opts.get("min_height") or opts.get("orientation") or opts.get("details")):
                dims = parse_nasa_metadata(http.get_json(meta_url))
        except FootageError as e:
            opts.setdefault("warnings", []).append(f"nasa {d['nasa_id']}: {e}")
            continue
        if video:
            out.append(nasa_result(db, d, video, dims, vids))
    return out


# ------------------------------------------------------------------------------------------------- Pexels and Pixabay (keys)

def pexels_title(page_url: str) -> str:
    """'Video of forest' from https://www.pexels.com/video/video-of-forest-1448735/ (a bare id gives 'Pexels clip')."""
    seg = urllib.parse.urlsplit(page_url or "").path.rstrip("/").rsplit("/", 1)[-1]
    words = re.sub(r"-?\d+$", "", seg).replace("-", " ").strip()
    return words.capitalize() if re.search(r"[a-z]", words, re.I) else "Pexels clip"


def pexels_video(db: dict, v: dict) -> dict | None:
    files = [f for f in v.get("video_files") or [] if f.get("link") and "mp4" in str(f.get("file_type", "mp4"))]
    if not files:
        return None
    best = max(files, key=lambda f: ((_int(f.get("height")) or 0) * (_int(f.get("width")) or 0)))
    user = v.get("user") or {}
    return make_result(db, "pexels", v.get("id"), title=pexels_title(v.get("url", "")), page_url=v.get("url"),
                       file_url=best["link"], licence=source_licence("pexels", sources_by_id(db).get("pexels")),
                       author=user.get("name"), width=best.get("width"), height=best.get("height"),
                       duration=v.get("duration"), mime=best.get("file_type"),
                       extra={"native": {"author_url": user.get("url")}})


def parse_pexels(db: dict, data: dict) -> list:
    return [r for r in (pexels_video(db, v) for v in (data or {}).get("videos") or []) if r]


def search_pexels(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    key = api_key("pexels")
    q = {"query": query, "per_page": str(max(1, min(limit * 2, 80)))}
    if opts.get("orientation") in ("portrait", "landscape", "square"):
        q["orientation"] = opts["orientation"]
    data = http.get_json("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(q), {"Authorization": key})
    return parse_pexels(db, data)


def pixabay_hit(db: dict, h: dict) -> dict | None:
    vids = h.get("videos") or {}
    best = next((vids[s] for s in ("large", "medium", "small", "tiny") if (vids.get(s) or {}).get("url")), None)
    if not best:
        return None
    tags = str(h.get("tags") or "").strip()
    return make_result(db, "pixabay", h.get("id"), title=tags.capitalize() if tags else "Pixabay clip",
                       page_url=h.get("pageURL"), file_url=best["url"],
                       licence=source_licence("pixabay", sources_by_id(db).get("pixabay")), author=h.get("user"),
                       width=best.get("width"), height=best.get("height"), duration=h.get("duration"),
                       size=best.get("size"), mime="video/mp4")


def parse_pixabay(db: dict, data: dict) -> list:
    return [r for r in (pixabay_hit(db, h) for h in (data or {}).get("hits") or []) if r]


def pixabay_url(key: str, *, query=None, clip_id=None, per_page=20) -> str:
    q = {"key": key, "safesearch": "true", "per_page": str(max(3, min(per_page, 200)))}
    if query:
        q["q"] = query[:100]
    if clip_id:
        q["id"] = str(clip_id)
    return "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(q)


def search_pixabay(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    return parse_pixabay(db, http.get_json(pixabay_url(api_key("pixabay"), query=query, per_page=limit * 2)))


# ------------------------------------------------------------------------------------------------- Mixkit (page scrape)

MIXKIT_CARD = 'data-item-grid--video-player-item-id-value="'


def _ld_objects(page: str) -> list:
    out = []
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S | re.I):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            continue
        stack = [data]
        while stack:
            o = stack.pop()
            if isinstance(o, list):
                stack.extend(o)
            elif isinstance(o, dict):
                out.append(o)
                stack.extend(v for v in o.values() if isinstance(v, (list, dict)))
    return out


def mixkit_ld_videos(page: str) -> dict:
    """{clip id: VideoObject} from a Mixkit page's JSON-LD."""
    found = {}
    for o in _ld_objects(page):
        if o.get("@type") != "VideoObject":
            continue
        m = re.search(r"-(\d+)/(?:#video)?$", str(o.get("@id") or "")) or \
            re.search(r"/videos/(\d+)/", str(o.get("contentUrl") or ""))
        if m:
            found[m.group(1)] = o
    return found


def mixkit_page_notice(page: str) -> str | None:
    """The licence a Mixkit clip page names: the JSON-LD copyrightNotice, else the download box's licence link."""
    for o in _ld_objects(page):
        if o.get("@type") == "VideoObject" and o.get("copyrightNotice"):
            return str(o["copyrightNotice"])
    m = re.search(r'data-license="(videoFree|videoRestricted)"', page)
    if m:
        return "Free" if m.group(1) == "videoFree" else MIXKIT_RESTRICTED
    return None


def parse_mixkit(db: dict, page: str) -> list:
    ld = mixkit_ld_videos(page)
    order, cards = [], {}
    starts = [m.start() for m in re.finditer(re.escape(MIXKIT_CARD), page)]
    for i, pos in enumerate(starts):
        chunk = page[pos: starts[i + 1] if i + 1 < len(starts) else pos + 6000]
        m = re.match(re.escape(MIXKIT_CARD) + r"(\d+)", chunk)
        if not m:
            continue
        cid = m.group(1)
        title = None
        for rx in (r'item-grid-video-player__overlay-video-title">\s*(.*?)\s*</',
                   r'class="item-grid-video-player__overlay-link"[^>]*>\s*(.*?)\s*</a>',
                   r'item-grid-card__title">\s*<a[^>]*>\s*(.*?)\s*</a>', r'<img[^>]*\salt="([^"]+)"'):
            t = re.search(rx, chunk, re.S)
            if t and clean_text(t.group(1)):
                title = clean_text(t.group(1)).rstrip(".")
                break
        link = re.search(r'href="(/free-stock-video/[^"]*?-' + cid + r'/)"', chunk)
        thumb = re.search(r'<img[^>]*class="item-grid-video-player__thumb"[^>]*>', chunk)
        tw = re.search(r'\swidth="(\d+)"', thumb.group(0)) if thumb else None
        th = re.search(r'\sheight="(\d+)"', thumb.group(0)) if thumb else None
        if cid not in cards:
            order.append(cid)
            cards[cid] = {"title": title, "page": "https://mixkit.co" + link.group(1) if link else None,
                          "dims": _scale_to_short_side(int(tw.group(1)), int(th.group(1)), 720) if tw and th else (None, None)}
    for cid in ld:
        if cid not in cards:
            order.append(cid)
            cards[cid] = {"title": None, "page": None, "dims": (None, None)}
    out = []
    for cid in order:
        o, c = ld.get(cid) or {}, cards[cid]
        page_url = c["page"] or str(o.get("@id") or "").split("#")[0] or f"https://mixkit.co/free-stock-video/{cid}/"
        lic = mixkit_licence(o.get("copyrightNotice"))
        w, h = c["dims"]
        flags = ([] if lic["verified"] else ["licence-checked-at-download"]) + (["size-from-thumbnail"] if w else [])
        out.append(make_result(db, "mixkit", cid, title=c["title"] or o.get("name") or f"Mixkit clip {cid}",
                               page_url=page_url, file_url=f"https://assets.mixkit.co/videos/{cid}/{cid}-720.mp4",
                               licence=lic, quality=720, width=w, height=h, duration=o.get("duration"),
                               mime="video/mp4", flags=flags))
    return out


def _scale_to_short_side(w: int, h: int, short: int) -> tuple:
    """The size of a `short`p file with the aspect of a w x h thumbnail (multiples of 8: 460x818 -> 720x1280)."""
    if not (w and h):
        return None, None
    if h >= w:
        return short, int(round(short * h / w / 8) * 8)
    return int(round(short * w / h / 8) * 8), short


def mixkit_search_url(query: str) -> str:
    slug = re.sub(r"\s+", " ", query.strip().lower())
    return "https://mixkit.co/free-stock-video/discover/" + urllib.parse.quote(slug, safe="") + "/"


def search_mixkit(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    found = parse_mixkit(db, http.get_text(mixkit_search_url(query)))
    if opts.get("commercial") or opts.get("details"):
        # the discover page does not name each clip's licence: read it from the pages of the clips that pass the
        # other filters (one request each, at most 2 x limit)
        rest = {**opts, "commercial": False}
        for rec in [r for r in found if not r["licence"]["verified"] and keep(r, rest) is None][: limit * 2]:
            confirm_licence(http, db, rec)
    return found


# ------------------------------------------------------------------------------------------------- Coverr (page state)

NG_ESCAPES = (("&q;", '"'), ("&s;", "'"), ("&l;", "<"), ("&g;", ">"), ("&a;", "&"))


def coverr_state(page: str) -> dict:
    m = re.search(r'<script[^>]*id="ng-state"[^>]*>(.*?)</script>', page, re.S)
    if not m:
        raise FootageError("coverr: the page has no ng-state JSON (the site changed or a block page came back)")
    raw = m.group(1)
    try:
        return json.loads(raw)
    except ValueError:
        for a, b in NG_ESCAPES:  # older Angular escaped the transfer state
            raw = raw.replace(a, b)
        try:
            return json.loads(raw)
        except ValueError:
            raise FootageError("coverr: the ng-state JSON does not parse") from None


def _coverr_videos(state: dict) -> list:
    if isinstance(state, dict) and isinstance(state.get("search_coverr_videos"), dict):
        hits = state["search_coverr_videos"].get("hits")
        return [h for h in hits if isinstance(h, dict)] if isinstance(hits, list) else []  # no hits = no results
    found, stack = [], [state]
    while stack:  # fall back to any object that looks like a Coverr video
        o = stack.pop()
        if isinstance(o, dict):
            if isinstance(o.get("urls"), dict) and o["urls"].get("mp4") and o.get("id"):
                found.append(o)
                continue
            stack.extend(o.values())
        elif isinstance(o, list):
            stack.extend(o)
    return found


def coverr_dims(v: dict) -> tuple:
    """(width, height) of the downloadable file. Coverr's "<q>p.mp4" is 16/9*q pixels wide whatever the orientation
    (measured 2026-10-29: the 1080p file of a 1152x2048 vertical clip is 1920x3412, an upscale), height by aspect."""
    w, h = _int(v.get("maxWidth")), _int(v.get("maxHeight"))
    m = re.search(r"/(\d{3,4})p\.mp4", str((v.get("urls") or {}).get("mp4") or ""))
    if not (w and h):
        return None, None
    if not m:
        return w, h
    fw = int(round(int(m.group(1)) * 16 / 9))
    return fw, int(fw * h / w) // 2 * 2


def parse_coverr(db: dict, page: str) -> tuple:
    """(results, number of premium clips skipped). Only free clips are kept; personal fields are never copied."""
    out, premium, seen = [], 0, set()
    for v in _coverr_videos(coverr_state(page)):
        vid = str(v.get("id"))
        if vid in seen:
            continue
        seen.add(vid)
        if v.get("isPremium"):
            premium += 1
            continue
        mp4 = (v.get("urls") or {}).get("mp4")
        if not mp4:
            continue
        w, h = coverr_dims(v)
        contrib = v.get("contributor") if isinstance(v.get("contributor"), dict) else {}
        author = contrib.get("fullname") or contrib.get("username")  # never the e-mail or other personal fields
        flags = ["ai-generated"] if v.get("isAiGenerated") else []
        if w and _int(v.get("maxWidth")) and w > _int(v.get("maxWidth")):
            flags.append("upscaled-file")
        slug = v.get("slug") or vid
        out.append(make_result(db, "coverr", vid, title=(v.get("title") or "").strip() or slug,
                               page_url=f"https://coverr.co/videos/{slug}", file_url=mp4,
                               licence=source_licence("coverr", sources_by_id(db).get("coverr")), author=author,
                               width=w, height=h, duration=v.get("duration"), mime="video/mp4", flags=flags,
                               extra={"native": {"source_width": _int(v.get("maxWidth")),
                                                 "source_height": _int(v.get("maxHeight")),
                                                 "fps": v.get("fps"), "has_audio": v.get("hasAudio")}}))
    return out, premium


def search_coverr(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    results, premium = parse_coverr(db, http.get_text("https://coverr.co/s?" + urllib.parse.urlencode({"q": query})))
    if premium:
        opts.setdefault("warnings", []).append(f"coverr: skipped {premium} premium (Coverr+) clips")
    return results


SEARCHERS = {
    "wikimedia": search_wikimedia,
    "archive": search_archive,
    "nasa": search_nasa,
    "pexels": search_pexels,
    "pixabay": search_pixabay,
    "mixkit": search_mixkit,
    "coverr": search_coverr,
}


# ------------------------------------------------------------------------------------------------- search

def orientation_of(r: dict) -> str | None:
    w, h = r.get("width"), r.get("height")
    if not (w and h):
        return None
    return "square" if abs(w - h) <= 0.05 * max(w, h) else ("portrait" if h > w else "landscape")


def keep(r: dict, opts: dict) -> str | None:
    """None when the result passes the filters, else the reason it is dropped."""
    lic = r.get("licence") or {}
    if lic.get("derivatives") is False and not opts.get("allow_nd"):
        return "no-derivatives licence (a montage is an edit)"
    if opts.get("commercial") and lic.get("commercial") is not True:
        return "commercial use not allowed or not confirmed"
    if not opts.get("any_licence") and lic.get("name", "").startswith("unknown"):
        return "unknown licence"
    if opts.get("no_ai") and "ai-generated" in r.get("flags", []):
        return "AI-generated"
    mh = opts.get("min_height")
    if mh:
        h = r.get("height")
        src_h = (r.get("native") or {}).get("source_height")
        if h and src_h:
            h = min(h, src_h)  # an upscaled file does not add detail
        if h is None and r.get("quality") and r["quality"] >= mh:
            h = r["quality"]  # the short side is a lower bound for the height
        if h is None:
            return "size unknown"
        if h < mh:
            return f"height {h} < {mh}"
    want = opts.get("orientation")
    if want:
        o = orientation_of(r)
        if o is None:
            return "orientation unknown"
        if o != want:
            return f"{o}, not {want}"
    return None


def default_sources(db: dict, environ=None) -> list:
    names = []
    for s in db["sources"]:
        mode = s["tool"]["search"]
        if s["id"] not in SEARCHERS or mode == "none":
            continue
        if mode == "api-key" and not api_key(s["id"], environ):
            continue
        names.append(s["id"])
    return names


def run_search(http: Http, db: dict, query: str, sources: list, limit: int, opts: dict, environ=None) -> dict:
    report = {"schema": RESULTS_SCHEMA, "query": query,
              "searched_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "filters": {k: opts.get(k) for k in ("min_height", "orientation", "commercial", "allow_nd", "any_licence",
                                                  "no_ai") if opts.get(k)},
              "limit_per_source": limit, "sources": {}, "results": [], "warnings": []}
    by_id = sources_by_id(db)
    for name in sources:
        src = by_id.get(name)
        if name not in SEARCHERS or not src:
            report["sources"][name] = {"status": "unsupported", "detail": "no search adapter; open its search_url"}
            continue
        if src["tool"]["search"] == "api-key" and not api_key(name, environ):
            env = KEY_ENV[name]
            report["sources"][name] = {"status": "skipped", "detail": f"needs {env} in the environment "
                                       "(set it as a secret; never paste a key into chat)"}
            continue
        local = dict(opts)
        try:
            found = SEARCHERS[name](http, db, query, limit, local)
        except FootageError as e:
            report["sources"][name] = {"status": "error", "detail": redact(e)}
            continue
        except (KeyError, TypeError, ValueError, AttributeError) as e:  # a changed page or API shape
            report["sources"][name] = {"status": "error", "detail": f"could not read the answer ({type(e).__name__}); "
                                       "the site may have changed"}
            continue
        kept, dropped = [], {}
        for r in found:
            why = keep(r, opts)
            if why:
                dropped[why] = dropped.get(why, 0) + 1
            elif len(kept) < limit:
                r["query"] = query
                kept.append(r)
        report["results"].extend(kept)
        report["sources"][name] = {"status": "ok", "count": len(kept), "found": len(found),
                                   **({"dropped": dropped} if dropped else {})}
        report["warnings"].extend(redact(w) for w in local.get("warnings", []))
    return report


def print_results(report: dict) -> None:
    for name, st in report["sources"].items():
        extra = f"{st.get('count', 0)} kept of {st.get('found', 0)}" if st["status"] == "ok" else st.get("detail", "")
        if st.get("dropped"):
            extra += " (dropped: " + ", ".join(f"{v} {k}" for k, v in st["dropped"].items()) + ")"
        print(f"# {name:10} {st['status']:11} {extra}")
    for w in report.get("warnings", []):
        print(f"# warning: {w}")
    for r in report["results"]:
        size = f"{r['width']}x{r['height']}" if r.get("width") and r.get("height") else (f"{r['quality']}p" if r.get("quality") else "?")
        dur = f"{r['duration']:.0f}s" if r.get("duration") else "?"
        lic = r["licence"]
        com = {True: "commercial ok", False: "NON-commercial", None: "commercial ?"}[lic.get("commercial")]
        att = "credit required" if lic.get("attribution_required") else ("credit optional" if lic.get("attribution_required") is False else "credit ?")
        print(f"{r['id']}\t{size}\t{dur}\t{lic.get('name')} | {com} | {att}\t{(r.get('title') or '')[:70]}")


# ------------------------------------------------------------------------------------------------- download

def pick_from_results(results_path: Path, rid: str) -> dict | None:
    try:
        data = json.loads(Path(results_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return next((r for r in data.get("results", []) if r.get("id") == rid), None)


def resolve_id(http: Http, db: dict, rid: str, opts: dict) -> dict:
    source, _, native = rid.partition(":")
    if not native:
        raise FootageError(f"{rid!r} is not a result id (source:id) or a URL")
    if source == "wikimedia":
        found = parse_wikimedia(db, http.get_json(commons_lookup_url(pageids=native)))
    elif source == "archive":
        meta = http.get_json(f"https://archive.org/metadata/{urllib.parse.quote(native)}")
        found = [r for r in [archive_result(db, {"identifier": native}, meta, opts.get("max_bytes"))] if r]
    elif source == "nasa":
        docs = [d for d in parse_nasa_search(http.get_json(nasa_search_url(nasa_id=native, limit=1))) if d["nasa_id"] == native]
        found = []
        if docs:
            vids, _meta = nasa_variants(http.get_json(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(native)}"))
            found = [nasa_result(db, docs[0], vids[0], alternates=vids)] if vids else []
    elif source == "mixkit" and native.isdigit():
        found = [make_result(db, "mixkit", native, title=f"Mixkit clip {native}",
                             page_url=f"https://mixkit.co/free-stock-video/{native}/",
                             file_url=f"https://assets.mixkit.co/videos/{native}/{native}-720.mp4",
                             licence=mixkit_licence(None), quality=720, mime="video/mp4")]
    elif source in ("pexels", "pixabay") and native.isdigit():
        return resolve_url(http, db, f"https://www.{source}.com/video/{native}/" if source == "pexels"
                           else f"https://pixabay.com/videos/id-{native}/", opts)
    else:
        raise FootageError(f"{rid}: not in the results file; run search again (or pass the clip's page URL)")
    if not found:
        raise FootageError(f"{rid}: the source returned no such video")
    return found[0]


def resolve_url(http: Http, db: dict, url: str, opts: dict) -> dict | None:
    """A result record for a page or file URL of a supported source, or None for any other link."""
    parts = urllib.parse.urlsplit(url)
    host, path = (parts.hostname or "").lower(), parts.path
    title = commons_title_from_url(url)
    if title:
        found = parse_wikimedia(db, http.get_json(commons_lookup_url(titles=title)))
        if not found:
            raise FootageError(f"commons: {title} is not a video file or does not exist")
        return found[0]
    if host in ("archive.org", "www.archive.org"):
        m = re.match(r"/(?:details|download)/([^/]+)", path)
        if m:
            return resolve_id(http, db, "archive:" + urllib.parse.unquote(m.group(1)), opts)
    if host in ("images.nasa.gov", "images-assets.nasa.gov"):
        m = re.match(r"/(?:details/|video/)([^/]+)", path)
        if m:
            return resolve_id(http, db, "nasa:" + urllib.parse.unquote(m.group(1)), opts)
    if host in ("mixkit.co", "www.mixkit.co", "assets.mixkit.co"):
        m = re.search(r"-(\d+)/?$", path) or re.search(r"/videos/(\d+)/", path) or re.search(r"/(\d+)/?$", path)
        if m:
            rec = resolve_id(http, db, "mixkit:" + m.group(1), opts)
            if "free-stock-video" in path:
                rec["page_url"] = f"https://mixkit.co{path}"
            return rec
    if host.endswith("pexels.com"):
        m = re.search(r"(\d{3,})/?$", path)
        if not m:
            return None
        cid = m.group(1)
        if api_key("pexels"):
            r = pexels_video(db, http.get_json(f"https://api.pexels.com/videos/videos/{cid}",
                                               {"Authorization": api_key("pexels")}))
            if r:
                return r
        stock_fetch = _sibling("stock_fetch")  # the key-less public download endpoint (302 to videos.pexels.com)
        try:
            file_url = stock_fetch.resolve_pexels(cid)
        except RuntimeError as e:
            raise FootageError(f"pexels {cid}: {e}") from None
        page = url if "/video/" in path else f"https://www.pexels.com/video/{cid}/"
        return make_result(db, "pexels", cid, title=pexels_title(page), page_url=page, file_url=file_url,
                           licence=source_licence("pexels", sources_by_id(db).get("pexels")), mime="video/mp4")
    if host.endswith("pixabay.com"):
        m = re.search(r"(\d{3,})/?$", path)
        if not m:
            return None
        key = api_key("pixabay")
        if not key:
            raise FootageError("pixabay needs PIXABAY_API_KEY in the environment (pixabay.com pages answer 403 to scripts)")
        hits = parse_pixabay(db, http.get_json(pixabay_url(key, clip_id=m.group(1), per_page=3)))
        if not hits:
            raise FootageError(f"pixabay {m.group(1)}: no such clip")
        return hits[0]
    if host in ("coverr.co", "www.coverr.co"):
        results, _premium = parse_coverr(db, http.get_text(url))
        slug = path.rstrip("/").rsplit("/", 1)[-1]
        for r in results:
            if r["page_url"].endswith("/" + slug):
                return r
        raise FootageError("coverr: the clip was not found on that page (premium clips are not downloaded)")
    if host.endswith("pinterest.com") or host.endswith("pinimg.com") or host == "pin.it":
        raise FootageError("Pinterest is not a licence source: trace the original creator (scripts/source_finder.py) "
                           "and fetch it from a licensed source, or keep a pin as private reference only")
    return None


def _same_site(host: str, site_url: str) -> bool:
    base = (urllib.parse.urlsplit(site_url).hostname or "").lower()
    base = base[4:] if base.startswith("www.") else base
    return bool(base) and (host == base or host.endswith("." + base))


def manual_record(db: dict, url: str, opts: dict) -> dict:
    """A record for any other direct file link, built from licence evidence the user supplies."""
    if not (opts.get("licence") and opts.get("licence_url")):
        raise FootageError("no licence is known for this link: pass --licence NAME --licence-url URL (and --author, "
                           "--title, --page-url) from the clip's page, or use a supported source")
    lic = classify_licence(opts["licence"], opts["licence_url"])
    if lic["name"].startswith("unknown") or not lic["verified"]:
        lic = licence_record(opts["licence"], opts["licence_url"], attribution=True, commercial=None, derivatives=None,
                             verified=False, note="user-supplied licence evidence, not machine-read")
    else:
        lic["verified"] = False
        lic["note"] = "user-supplied licence evidence, not machine-read"
    host = (urllib.parse.urlsplit(url).hostname or "link").lower()
    native = hashlib.sha256(url.encode()).hexdigest()[:12]
    known = sources_by_id(db)
    sid = next((s["id"] for s in db["sources"] if _same_site(host, s["url"])), None)
    rec = make_result(db, sid or "manual", native, title=opts.get("title") or Path(urllib.parse.urlsplit(url).path).stem,
                      page_url=opts.get("page_url") or url, file_url=url, licence=lic, author=opts.get("author"))
    if not sid:
        rec["source_name"] = host
        rec["attribution"] = format_attribution(None, title=rec["title"], author=rec["author"], source=host,
                                                licence=lic["name"], licence_url=lic["url"], page_url=rec["page_url"])
    elif known.get(sid, {}).get("licence_source") is False:
        raise FootageError(f"{sid} is not a licence source; it cannot be downloaded with a licence record")
    return rec


def confirm_licence(http: Http, db: dict, rec: dict) -> dict:
    """Mixkit: read the clip page's own licence notice before downloading (Free vs Restricted)."""
    if rec.get("source") != "mixkit" or (rec.get("licence") or {}).get("verified"):
        return rec
    try:
        page = http.get_text(rec["page_url"])
    except FootageError as e:
        rec["licence"]["note"] += f"; the clip page could not be read ({e})"
        return rec
    notice = mixkit_page_notice(page)
    if notice:
        lic = mixkit_licence(notice)
        rec["licence"] = lic
        vo = next((o for o in _ld_objects(page) if o.get("@type") == "VideoObject"), {})
        if vo.get("name") and str(rec.get("title") or "").startswith("Mixkit clip"):
            rec["title"] = clean_text(vo["name"])
        if rec.get("duration") is None and vo.get("duration"):
            rec["duration"] = _float(vo["duration"])
        rec["flags"] = [f for f in rec.get("flags", []) if f != "licence-checked-at-download"]
        rec["attribution"] = format_attribution(((sources_by_id(db).get("mixkit") or {}).get("attribution") or {}).get("template"),
                                                title=rec.get("title"), source="Mixkit", licence=lic["name"],
                                                licence_url=lic["url"], page_url=rec["page_url"])
    return rec


MAGIC = ((4, b"ftyp"), (4, b"moov"), (4, b"mdat"), (4, b"free"), (4, b"wide"), (0, b"\x1a\x45\xdf\xa3"),
         (0, b"OggS"), (0, b"\x00\x00\x01\xba"), (0, b"\x00\x00\x01\xb3"), (0, b"RIFF"))
CT_EXT = {"video/mp4": ".mp4", "video/webm": ".webm", "video/ogg": ".ogv", "video/quicktime": ".mov",
          "video/x-matroska": ".mkv", "video/mpeg": ".mpeg", "video/x-msvideo": ".avi"}


def looks_like_video(head: bytes, content_type: str = "") -> bool:
    if any(head[off:off + len(sig)] == sig for off, sig in MAGIC):
        return True
    if len(head) > 188 and head[0] == 0x47 and head[188] == 0x47:  # MPEG-TS
        return True
    if head.lstrip()[:1] in (b"<", b"{"):
        return False
    return content_type.split(";")[0].strip().lower().startswith("video/")


def safe_name(rec: dict, content_type: str = "") -> str:
    native = rec["id"].split(":", 1)[1] if ":" in rec["id"] else rec["id"]
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{rec['source']}-{native}").strip("._")[:90]
    ext = Path(urllib.parse.urlsplit(rec["file_url"]).path).suffix.lower()
    if ext not in VIDEO_EXT:
        ext = CT_EXT.get(content_type.split(";")[0].strip().lower(), ".mp4")
    return stem + ext


def fetch_file(http: Http, url: str, dest: Path, max_mb: float) -> dict:
    """Stream url into dest through a .part file with a size cap and a check that the bytes are a video."""
    resp = http.open(url)
    tmp = dest.with_name(dest.name + ".part")
    cap = int(max_mb * 1048576) if max_mb else None
    sha, n = hashlib.sha256(), 0
    try:
        ctype = (resp.headers.get("Content-Type") if getattr(resp, "headers", None) else "") or ""
        length = resp.headers.get("Content-Length") if getattr(resp, "headers", None) else None
        if cap and length and str(length).isdigit() and int(length) > cap:
            raise FootageError(f"the file is {int(length) / 1048576:.1f} MB, over --max-mb {max_mb:g}")
        first = True
        with open(tmp, "wb") as f:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                if first:
                    if not looks_like_video(chunk[:512], ctype):
                        raise FootageError("the server sent a web page or other data, not a video "
                                           "(a login wall, a block page or a moved file)")
                    first = False
                n += len(chunk)
                if cap and n > cap:
                    raise FootageError(f"the file is larger than --max-mb {max_mb:g}; stopped")
                sha.update(chunk)
                f.write(chunk)
        if n == 0:
            raise FootageError("the server sent an empty file")
        tmp.replace(dest)
        return {"bytes": n, "sha256": sha.hexdigest(), "content_type": ctype}
    except BaseException:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise
    finally:
        _close(resp)


def measure(path: Path) -> dict:
    if not shutil.which("ffprobe"):
        return {}
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height,codec_name,r_frame_rate:format=duration", "-of", "json", str(path)],
                             capture_output=True, text=True, timeout=60)
        d = json.loads(out.stdout or "{}")
        s = (d.get("streams") or [{}])[0]
        return {k: v for k, v in {"width": s.get("width"), "height": s.get("height"), "codec": s.get("codec_name"),
                                  "fps": s.get("r_frame_rate"),
                                  "duration": _float((d.get("format") or {}).get("duration"))}.items() if v}
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}


def _redact_all(obj):
    if isinstance(obj, str):
        return redact(obj)
    if isinstance(obj, dict):
        return {k: _redact_all(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_redact_all(v) for v in obj]
    return obj


def sidecar_for(media: Path) -> Path:
    return media.with_name(media.name + ".json")


def download_one(http: Http, db: dict, target: str, out: Path, opts: dict) -> dict:
    if re.match(r"^https?://", target, re.I):
        rec = resolve_url(http, db, target, opts) or manual_record(db, target, opts)
    else:
        rec = pick_from_results(opts["results"], target) or resolve_id(http, db, target, opts)
    if not rec.get("file_url"):
        raise FootageError(f"{rec.get('id')}: no downloadable file")
    if (sources_by_id(db).get(rec["source"]) or {}).get("licence_source") is False:
        raise FootageError(f"{rec['source']} is not a licence source")
    cap = int(opts["max_mb"] * 1048576) if opts.get("max_mb") else None
    if rec["source"] == "archive" and cap and (rec.get("bytes") or 0) > cap:
        smaller = resolve_id(http, db, rec["id"], {**opts, "max_bytes": cap})  # the item's smaller derivative
        if (smaller.get("bytes") or 0) <= cap:
            smaller["query"] = rec.get("query")
            rec = smaller
    if rec["source"] == "nasa" and "alternates" not in rec and not opts.get("dry_run"):
        try:  # a results file from before alternates were recorded: fetch the variant list once
            rec = {**resolve_id(http, db, rec["id"], opts), "query": rec.get("query")}
        except FootageError:
            pass
    rec = confirm_licence(http, db, rec)
    lic = rec["licence"]
    if lic.get("derivatives") is False and not opts.get("allow_nd"):
        raise FootageError(f"{rec['id']}: {lic.get('name')} forbids edits (ND); a montage is an edit. "
                           "Pass --allow-nd only to keep it unedited as reference")
    if opts.get("commercial") and lic.get("commercial") is not True:
        raise FootageError(f"{rec['id']}: {lic.get('name')} does not allow (or does not confirm) commercial use")
    out.mkdir(parents=True, exist_ok=True)
    dest = out / safe_name(rec)
    if opts.get("dry_run"):
        return {"id": rec["id"], "file": dest.name, "dry_run": True, "file_url": redact(rec["file_url"]),
                "licence": lic.get("name"), "attribution": rec["attribution"]}
    info = {}
    if dest.exists() and not opts.get("force"):
        data = dest.read_bytes()
        info = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "content_type": None, "reused": True}
    else:
        urls = [rec["file_url"]] + list(rec.get("alternates") or [])
        for i, u in enumerate(urls):
            try:
                info = fetch_file(http, u, dest, opts.get("max_mb", 300))
            except FootageError as e:
                if "--max-mb" in str(e) and i + 1 < len(urls):
                    continue  # over the cap: try the next smaller variant (NASA ~large, ~medium, ~mobile)
                raise
            if u != rec["file_url"]:
                rec["flags"] = sorted(set(rec.get("flags", [])) | {"smaller-variant"})
                rec["file_url"], rec["width"], rec["height"] = u, None, None
            break
    sidecar = {
        "schema": ASSET_SCHEMA,
        "file": dest.name,
        "downloaded_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bytes": info["bytes"],
        "sha256": info["sha256"],
        "result": _redact_all(rec),
        "licence": lic,
        "attribution": rec["attribution"],
        "measured": measure(dest),
        "rights_note": "Licence as declared by the source when downloaded; it is not legal advice. Read the clip page "
                       "before publishing, keep this file with the project, and credit as the attribution line says.",
    }
    try:  # never write anything that looks like a credential (signed CDN links are redacted above)
        hits = _sibling("_secrets").scan_object(sidecar)
    except ImportError:
        hits = []
    if hits:
        raise FootageError("refusing to write a sidecar with a credential-like value at " + ", ".join(h[0] for h in hits[:3]))
    sidecar_for(dest).write_text(json.dumps(sidecar, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_credits(out)
    return {"id": rec["id"], "file": dest.name, "bytes": info["bytes"], "licence": lic.get("name"),
            "attribution": rec["attribution"], "reused": bool(info.get("reused"))}


def _cell(s) -> str:
    return str(s if s not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def credits_markdown(folder: Path) -> str:
    rows = []
    for p in sorted(Path(folder).glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if d.get("schema") == ASSET_SCHEMA:
            rows.append(d)
    rows.sort(key=lambda d: d.get("file", ""))
    lines = ["# Attribution — footage credits", "",
             "Generated by `scripts/free_footage.py` from the `*.json` sidecars in this folder "
             "(run `python3 scripts/free_footage.py credits <this folder>` after removing a clip).", "",
             "| file | source | licence | credit required | commercial use |", "|---|---|---|---|---|"]
    yn = {True: "yes", False: "no", None: "check"}
    for d in rows:
        lic = d.get("licence") or {}
        r = d.get("result") or {}
        lines.append(f"| {_cell(d.get('file'))} | {_cell(r.get('source_name') or r.get('source'))} | "
                     f"{_cell(lic.get('name'))} | {yn.get(lic.get('attribution_required'), 'check')} | "
                     f"{yn.get(lic.get('commercial'), 'check')} |")
    lines += ["", "## Credit lines", "", "Copy these into the video description or end credits "
              "(lines marked *optional* are not required by the licence but are good practice).", ""]
    for d in rows:
        opt = " *(optional)*" if (d.get("licence") or {}).get("attribution_required") is False else ""
        lines.append(f"- {d.get('attribution')}{opt}")
    if not rows:
        lines.append("- (no clips yet)")
    return "\n".join(lines) + "\n"


def write_credits(folder: Path) -> Path:
    path = Path(folder) / "ATTRIBUTION.md"
    path.write_text(credits_markdown(folder), encoding="utf-8")
    return path


# ------------------------------------------------------------------------------------------------- probe

def probe_source(http: Http, src: dict) -> dict:
    rows = []
    for p in src.get("probes") or []:
        t0 = time.monotonic()
        row = {"what": p["what"], "url": p["url"]}
        try:
            resp = http.open(p["url"], {"Range": "bytes=0-65535"} if p["url"].lower().endswith(VIDEO_EXT) else None)
            status = getattr(resp, "status", None) or 200
            ctype = resp.headers.get("Content-Type") if getattr(resp, "headers", None) else None
            _close(resp)
            row.update(http=status, content_type=ctype)
        except HttpError as e:
            row.update(http=e.status if isinstance(e.status, int) else None, error=None if isinstance(e.status, int) else str(e))
        row["ms"] = int((time.monotonic() - t0) * 1000)
        code = row.get("http")
        if isinstance(code, int) and code < 400:
            row["verdict"] = "ok"
        elif isinstance(code, int) and code == p.get("expect"):
            row["verdict"] = "expected"
        elif isinstance(code, int):
            row["verdict"] = "blocked"
        else:
            row["verdict"] = "timeout" if re.search(r"time[sd]?\s?out", str(row.get("error", "")), re.I) else "error"
        rows.append(row)
    verdicts = [r["verdict"] for r in rows]
    if verdicts and all(v == "ok" for v in verdicts):
        status = "ok"
    elif "expected" in verdicts:
        status = "needs-key"  # the API answered as designed for a request without a key
    elif "ok" in verdicts:
        status = "partial"  # e.g. the API answers but the file host is rate limited
    elif "timeout" in verdicts:
        status = "timeout"
    elif "blocked" in verdicts:
        status = "blocked"
    else:
        status = "error" if rows else "not-checked"
    if status in ("ok", "partial") and src["reachability"]["status"] == "paid":
        status = "paid"
    was = src["reachability"]["status"]
    return {"id": src["id"], "name": src["name"], "status": status, "recorded": was, "changed": status != was,
            "probes": rows}


def run_probe(http: Http, db: dict, names: list) -> dict:
    by_id = sources_by_id(db)
    today = _dt.date.today().isoformat()
    report = {"schema": PROBE_SCHEMA, "date": today,
              "measured_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "database_checked_on": db.get("checked_on"), "sources": []}
    for n in names:
        report["sources"].append(probe_source(http, by_id[n]))
    return report


# ------------------------------------------------------------------------------------------------- CLI

def _source_list(db: dict, value: str | None) -> list:
    if not value:
        return []
    names = [x.strip().lower() for x in value.split(",") if x.strip()]
    known = sources_by_id(db)
    bad = [n for n in names if n not in known]
    if bad:
        raise FootageError(f"unknown source(s): {', '.join(bad)} (see: free_footage.py sources)")
    return names


def cmd_sources(args, db) -> int:
    rows = db["sources"]
    if args.id:
        rows = [s for s in rows if s["id"] == args.id]
        if not rows:
            raise FootageError(f"no source {args.id!r}")
    if args.status:
        rows = [s for s in rows if s["reachability"]["status"] == args.status]
    if args.searchable:
        rows = [s for s in rows if s["tool"]["search"] != "none"]
    if args.no_attribution:
        rows = [s for s in rows if not s["attribution"]["required"]]
    if args.commercial:
        rows = [s for s in rows if s["commercial_use"] == "yes"]
    if args.find:
        w = args.find.lower()
        rows = [s for s in rows if w in json.dumps(s, ensure_ascii=False).lower()]
    if args.json or args.id:
        print(json.dumps(rows if not args.id else rows[0], ensure_ascii=False, indent=1))
        return 0
    print(f"# {len(rows)} of {len(db['sources'])} sources (checked {db.get('checked_on')}); "
          "a listed source is not a licence for any clip")
    for s in rows:
        att = "credit" if s["attribution"]["required"] else "no-credit"
        key = f" key:{s['api']['key_env']}" if s["api"].get("key_env") and s["tool"]["search"] == "api-key" else ""
        print(f"{s['id']:12} {s['reachability']['status']:10} search:{s['tool']['search']:8}{key:22} "
              f"{s['commercial_use']:9} {att:9} {s['licence']['name'][:60]}")
    return 0


def cmd_check(args, db) -> int:
    errs = validate_db(db)
    for e in errs:
        print(f"error: {e}")
    if not errs:
        print(f"ok: {len(db['sources'])} sources, ids unique, templates valid ({DB_PATH.relative_to(SK).as_posix()})")
    return 1 if errs else 0


def make_http(args) -> Http:
    return Http(delay=args.delay, timeout=args.timeout)


def cmd_probe(args, db) -> int:
    names = _source_list(db, args.sources) or [s["id"] for s in db["sources"]]
    report = run_probe(make_http(args), db, names)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"probe-{report['date'].replace('-', '')}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        for s in report["sources"]:
            codes = " ".join(f"{p['what']}={p.get('http') or p.get('verdict')}" for p in s["probes"])
            flag = f"  (was {s['recorded']})" if s["changed"] else ""
            print(f"{s['id']:12} {s['status']:10} {codes}{flag}")
        print(f"# report: {path}")
    return 0


def cmd_search(args, db) -> int:
    names = _source_list(db, args.sources) or default_sources(db)
    opts = {"min_height": args.min_height, "orientation": args.orientation, "commercial": args.commercial,
            "allow_nd": args.allow_nd, "any_licence": args.any_licence, "no_ai": args.no_ai,
            "max_bytes": int(args.max_mb * 1048576) if args.max_mb else None, "details": args.details}
    report = run_search(make_http(args), db, " ".join(args.query), names, max(1, min(args.limit, 50)), opts)
    if not args.no_save:
        path = Path(args.save)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print_results(report)
        if not args.no_save:
            print(f"# saved {len(report['results'])} results to {args.save}; "
                  "download with: free_footage.py download <id> --out <dir>")
    statuses = [v["status"] for v in report["sources"].values()]
    return 3 if statuses and all(s == "error" for s in statuses) else 0


def cmd_download(args, db) -> int:
    http = make_http(args)
    opts = {"results": Path(args.results), "max_mb": args.max_mb, "licence": args.licence,
            "licence_url": args.licence_url, "author": args.author, "title": args.title, "page_url": args.page_url,
            "allow_nd": args.allow_nd, "commercial": args.commercial, "dry_run": args.dry_run, "force": args.force,
            "max_bytes": int(args.max_mb * 1048576) if args.max_mb else None}
    out, failed, done = Path(args.out), 0, []
    for t in args.targets:
        try:
            r = download_one(http, db, t, out, opts)
            done.append(r)
            note = "dry run" if r.get("dry_run") else (f"{r['bytes'] / 1048576:.1f} MB" + (" (kept)" if r.get("reused") else ""))
            print(f"{r['id']}\t{r['file']}\t{note}\t{r['licence']}")
        except FootageError as e:
            failed += 1
            print(f"{t}\tFAILED\t{redact(e)}", file=sys.stderr)
    if args.json:
        print(json.dumps(done, ensure_ascii=False, indent=1))
    if done and not args.dry_run:
        print(f"# credits: {out / 'ATTRIBUTION.md'}")
    return 1 if failed else 0


def cmd_credits(args, db) -> int:
    folder = Path(args.dir)
    if not folder.is_dir():
        raise FootageError(f"{folder} is not a folder")
    path = write_credits(folder)
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="free_footage.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=str(DB_PATH), help="sources database (default data/free_footage_sources.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def net(p):
        p.add_argument("--delay", type=float, default=1.0, help="seconds between requests to one host (default 1.0)")
        p.add_argument("--timeout", type=float, default=20.0, help="seconds per request (default 20)")

    p = sub.add_parser("sources", help="list or filter the sources database (offline)")
    p.add_argument("--id", help="show one source in full")
    p.add_argument("--find", help="keep sources whose record mentions this word")
    p.add_argument("--status", choices=ENUMS["reachability.status"], help="recorded reachability")
    p.add_argument("--searchable", action="store_true", help="only sources this tool can search")
    p.add_argument("--no-attribution", action="store_true", help="only sources that do not require credit")
    p.add_argument("--commercial", action="store_true", help="only sources whose licence allows commercial use")
    p.add_argument("--json", action="store_true")
    sub.add_parser("check", help="validate the database (offline)")
    p = sub.add_parser("probe", help="live reachability check of every source (network)")
    p.add_argument("--sources", help="comma-separated source ids (default: all)")
    p.add_argument("--out", default=str(DEFAULT_PROBE_DIR), help="folder for probe-<YYYYMMDD>.json")
    p.add_argument("--json", action="store_true")
    net(p)
    p = sub.add_parser("search", help="search the key-less APIs, keyed APIs with keys, Mixkit and Coverr (network)")
    p.add_argument("query", nargs="+")
    p.add_argument("--sources", help="comma-separated ids (default: every searchable source whose key is present)")
    p.add_argument("--limit", type=int, default=6, help="results kept per source (default 6, max 50)")
    p.add_argument("--min-height", type=int, help="keep clips at least this many pixels tall (1920 for vertical 1080p)")
    p.add_argument("--orientation", choices=("portrait", "landscape", "square"))
    p.add_argument("--commercial", action="store_true", help="drop NC, Restricted and unconfirmed licences")
    p.add_argument("--allow-nd", action="store_true", help="keep no-derivatives licences (reference only)")
    p.add_argument("--any-licence", action="store_true", help="keep Archive items with no licence (rights unknown)")
    p.add_argument("--no-ai", action="store_true", help="drop clips flagged as AI-generated")
    p.add_argument("--details", action="store_true", help="NASA: also read each clip's size (one request more)")
    p.add_argument("--max-mb", type=float, default=300, help="Archive: prefer a file under this size (default 300)")
    p.add_argument("--save", default=str(DEFAULT_RESULTS), help="results file (default out/free-footage/last_search.json)")
    p.add_argument("--no-save", action="store_true")
    p.add_argument("--json", action="store_true")
    net(p)
    p = sub.add_parser("download", help="download result ids or URLs with a licence sidecar and ATTRIBUTION.md (network)")
    p.add_argument("targets", nargs="+", help="result ids (wikimedia:81916645) or page/file URLs")
    p.add_argument("--out", required=True, help="folder for the clips, sidecars and ATTRIBUTION.md")
    p.add_argument("--results", default=str(DEFAULT_RESULTS), help="results file from search")
    p.add_argument("--max-mb", type=float, default=300, help="refuse files larger than this (default 300; 0 = no cap)")
    p.add_argument("--licence", help="licence name for a link from an unsupported site (from its page)")
    p.add_argument("--licence-url", help="licence URL for a link from an unsupported site")
    p.add_argument("--author")
    p.add_argument("--title")
    p.add_argument("--page-url")
    p.add_argument("--allow-nd", action="store_true", help="allow a no-derivatives licence (keep the clip unedited)")
    p.add_argument("--commercial", action="store_true", help="refuse clips whose licence does not confirm commercial use")
    p.add_argument("--dry-run", action="store_true", help="resolve and print, write nothing")
    p.add_argument("--force", action="store_true", help="download again even when the file exists")
    p.add_argument("--json", action="store_true")
    net(p)
    p = sub.add_parser("credits", help="rebuild DIR/ATTRIBUTION.md from the sidecars (offline)")
    p.add_argument("dir")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        db = load_db(Path(args.db))
    except (OSError, ValueError) as e:
        print(f"error: cannot read the sources database: {e}", file=sys.stderr)
        return 1
    if args.cmd != "check":
        errs = validate_db(db)
        if errs:
            print("error: the sources database is invalid (run: free_footage.py check): " + errs[0], file=sys.stderr)
            return 1
    try:
        return {"sources": cmd_sources, "check": cmd_check, "probe": cmd_probe, "search": cmd_search,
                "download": cmd_download, "credits": cmd_credits}[args.cmd](args, db)
    except FootageError as e:
        print(f"error: {redact(e)}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    sys.exit(main())
