#!/usr/bin/env python3
"""Free footage: a database of open-licence video sources, plus search and download with a licence record per clip.

مصادر فيديو مفتوحة الترخيص للمونتاج: قاعدة بيانات بالمواقع وترخيص كل موقع، وبحث وتحميل يحفظ مع كل لقطة ترخيصها وسطر النسب.

Subcommands:
  sources [--find WORD] [--status ok] [--searchable] [--commercial] [--no-attribution] [--include-paid] [--json]
          list or filter data/free_footage_sources.json (offline; paid stock only with --include-paid)
  check   validate the database: required keys, enums, unique ids, template placeholders (offline)
  probe   [--sources a,b] [--out DIR]
          live reachability check of every source's probe URLs, with the URL each one lands on after redirects
          (a site now served from another domain is "moved"); writes <out>/probe-<YYYYMMDD>.json (network)
  search  QUERY [--sources a,b] [--min-height N] [--orientation portrait] [--limit N] [--commercial] [--no-ai]
          [--resolve] [--match any|all] [--no-people] [--wait-429 S] [--retry-failed] [--replace]
          key-less APIs (Wikimedia Commons, Internet Archive, NASA), Pexels/Pixabay when PEXELS_API_KEY /
          PIXABAY_API_KEY are in the environment, and the Mixkit and Coverr search pages; merges the results by id
          into out/free-footage/last_search.json, so ids from earlier searches still download (network)
  download TARGET... --out DIR [--quality 1080] [--max-height N] [--max-mb MB] [--dry-run]
          a result id from the results file (wikimedia:81916645) or a page/file URL; saves the file, a sidecar
          <file>.json with licence and attribution, and rebuilds <out>/ATTRIBUTION.md; --dry-run prints the size,
          resolution and file size it would fetch (network)
  preview RESULTS.json|DIR [--out DIR] [--frames N]
          a contact sheet (HTML, plus a JPG when ffmpeg is installed) from each result's thumbnail or small preview
          file, or from the clips already in DIR, to screen for people and text before downloading full files (network)
  credits DIR
          rebuild DIR/ATTRIBUTION.md from the sidecars (offline)

Licences come from what each source declares (Commons extmetadata, the Archive's licenseurl, the Mixkit clip page's
notice, the Coverr and Pexels/Pixabay licences, NASA's media guidelines). The tool records them; it does not grant
them. ND licences are dropped by default (a montage is an adaptation); NC and Mixkit "Restricted" clips are kept but
marked commercial=false, and --commercial drops them, as it drops the retired CC Sampling, Sampling+ and Developing
Nations licences (recorded unverified, credit required). An Archive licence is the uploader's own claim; one on what
looks like a music video, a film or TV rip or a YouTube re-upload is flagged suspicious-licence (unverified,
commercial unknown). Mixkit Free clips download at their largest listed size (2160p, else 1080p), Restricted clips
at 720p only; newer Mixkit clips have no <id>-<q>.mp4 file and are fetched through the clip page's own download
options. Pinterest is never downloaded: it is not a licence source.

Keys are read from the environment only, never printed or stored. One request per host per --delay seconds
(default 1.0), a timeout on every request, a descriptive User-Agent, and a size cap on pages and files. A Cloudflare
"Just a moment..." browser check is reported, never worked around: the host is left alone for the rest of the run.
Python 3.8+ standard library only (ffprobe/ffmpeg are used when present to measure downloads and draw contact sheets).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import email.utils
import hashlib
import html as _html
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.client import HTTPException  # InvalidURL, IncompleteRead, RemoteDisconnected …: not URLError/ValueError
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
# How to run this script again from where people run it: the repository root, when the skill sits at
# <root>/.claude/skills/<name>/ (ATTRIBUTION.md once said `scripts/free_footage.py`, which fails from the root).
if SK.parent.name == "skills" and SK.parent.parent.name == ".claude":
    SCRIPT_FROM_ROOT, SCRIPT_FROM_WHERE = f".claude/skills/{SK.name}/scripts/free_footage.py", " from the repository root"
else:
    SCRIPT_FROM_ROOT, SCRIPT_FROM_WHERE = "scripts/free_footage.py", " from the skill folder"
DEFAULT_PROBE_DIR = Path("out") / "free-footage"
UA = "KOSIF-free-footage/1.0 (+https://github.com/kosif199022-jpg/kosif-tool; open-licence footage for montage)"
PAGE_CAP_MB = 40          # the Coverr search page alone is about 11 MB
MAX_RETRY_AFTER = 30.0    # seconds we wait after a 429/503 by default (--wait-429 raises it)
MAX_WAIT_429 = 900.0      # the most --wait-429 accepts (upload.wikimedia.org asked for 600 s on 2026-10-29)
MAX_CHALLENGE_WAIT = 600.0  # the most --retry-challenge accepts
RETRY_5XX_SITES = ("archive.org",)  # its data nodes answer a transient 500 that clears on one retry
THUMB_CAP_MB = 5
PREVIEW_CAP_MB = 25       # a 360p preview file, never the full clip
RESULTS_HISTORY = 100     # searches remembered in the results file
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
    "reachability.status": ("ok", "partial", "blocked", "timeout", "needs-key", "paid", "moved", "not-checked"),
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
    def __init__(self, url: str, status, detail: str = "", final_url: str | None = None, retry_after=None):
        self.url, self.status, self.retry_after = url, status, retry_after
        self.final_url = final_url or url  # where urllib ended up after following redirects
        moved = f" (redirected to {redact(self.final_url)})" if self.final_url != url else ""
        super().__init__(f"HTTP {status} from {redact(url)}{moved}" + (f": {detail}" if detail else ""))


class ChallengeError(HttpError):
    """A Cloudflare "Just a moment..." browser check came back instead of the page. The tool never solves it or works
    around it: it says so, leaves that host alone for the rest of the run, and the user retries later."""

    def __init__(self, url: str, status=None, final_url: str | None = None, earlier: bool = False):
        host = (urllib.parse.urlsplit(url).hostname or "the site").lower()
        if earlier:
            detail = (f"skipped: {host} answered with a Cloudflare browser check earlier in this run; "
                      "run the command again in a few minutes")
        else:
            detail = (f"{host} answered with a Cloudflare \"Just a moment...\" browser check instead of the page "
                      "(a bot challenge). The tool does not try to get past it: run the same command again in a few "
                      "minutes (on 2026-10-29 it cleared after about 3 minutes), add --retry-challenge 180 to wait "
                      "once, or open the page in a browser")
        super().__init__(url, status if status is not None else "challenge", detail, final_url)


CHALLENGE_RE = re.compile(rb"<title>\s*Just a moment\.*\s*</title>|window\._cf_chl_opt|/cdn-cgi/challenge-platform/",
                          re.I)


def is_challenge_page(body: bytes) -> bool:
    """True for a Cloudflare interstitial ("Just a moment...", served with 200, 403 or 503)."""
    return bool(body) and bool(CHALLENGE_RE.search(body[:65536]))


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
    """Polite HTTP: one request per host per `delay` seconds, timeouts, a User-Agent, size caps, one retry on 429/503
    (when Retry-After is at most `max_retry_after` seconds) and on a 500/502/504 from an Archive data node.

    A Cloudflare browser check (the "Just a moment..." page, or a 403/503 with cf-mitigated: challenge) raises
    ChallengeError and marks the host, so no further request goes to it in this run; with `challenge_wait` > 0 the
    tool waits that long once per host and asks again, as a person would. `transport(request, timeout)` returns a
    urlopen-like response; tests pass a fake. `sleep` and `clock` are injectable so the rate limit is testable
    without waiting."""

    def __init__(self, delay: float = 1.0, timeout: float = 20.0, transport=None, sleep=time.sleep,
                 clock=time.monotonic, retries: int = 1, max_retry_after: float = MAX_RETRY_AFTER,
                 challenge_wait: float = 0.0):
        self.delay, self.timeout, self.retries = max(0.0, float(delay)), float(timeout), int(retries)
        self.max_retry_after = min(max(0.0, float(max_retry_after)), MAX_WAIT_429)
        self.challenge_wait = min(max(0.0, float(challenge_wait or 0)), MAX_CHALLENGE_WAIT)
        self.transport = transport or (lambda req, timeout: urllib.request.urlopen(req, timeout=timeout))
        self.sleep, self.clock = sleep, clock
        self._last = {}
        self.calls = 0
        self.challenged = set()        # hosts that answered with a browser check in this run
        self._challenge_retried = set()

    def _wait(self, host: str) -> None:
        last = self._last.get(host)
        if last is not None:
            gap = self.delay - (self.clock() - last)
            if gap > 0:
                self.sleep(gap)
        self._last[host] = self.clock()

    def _challenge(self, host: str, url: str, status, final: str) -> None:
        """Wait once (challenge_wait) and return so the caller asks again, or raise ChallengeError."""
        if self.challenge_wait > 0 and host not in self._challenge_retried:
            self._challenge_retried.add(host)
            self.sleep(self.challenge_wait)
            return
        self.challenged.add(host)
        raise ChallengeError(url, status, final_url=final)

    def open(self, url: str, headers: dict | None = None, method: str = "GET"):
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
        if host in self.challenged:
            raise ChallengeError(url, earlier=True)
        hdrs = {"User-Agent": UA, "Accept": "*/*"}
        hdrs.update(headers or {})
        attempt = 0
        while True:
            self._wait(host)
            self.calls += 1
            final = url
            try:
                req = urllib.request.Request(url, headers=hdrs, method=method)
                resp = self.transport(req, self.timeout)
            except urllib.error.HTTPError as e:
                status, rh = e.code, e.headers
                final = _final_url(e, url)  # the URL of the answer, after any redirect
                _close(e)
            except (urllib.error.URLError, OSError, ValueError, HTTPException) as e:  # DNS, refused, TLS, timeout, bad URL
                reason = getattr(e, "reason", e)
                raise HttpError(url, type(reason).__name__ if not isinstance(reason, str) else "error", str(reason)[:160]) from None
            else:
                status = getattr(resp, "status", None) or getattr(resp, "code", 200)
                rh = getattr(resp, "headers", None)
                if status < 400:
                    return resp
                final = _final_url(resp, url)
                _close(resp)
            retry_after = rh.get("Retry-After") if rh else None
            if status in (403, 429, 503) and str((rh.get("cf-mitigated") if rh else "") or "").lower() == "challenge":
                self._challenge(host, url, status, final)  # raises, or waited once
                continue
            final_host = (urllib.parse.urlsplit(final).hostname or "").lower()
            server_error = status in (500, 502, 504) and any(
                h == s or h.endswith("." + s) for s in RETRY_5XX_SITES for h in (host, final_host))
            ra = _seconds(retry_after)
            if (status in (429, 503) or server_error) and attempt < self.retries:
                attempt += 1
                wait = ra if ra is not None else (self.delay * 4 or 2.0)
                if status in (429, 503) and ra is not None and wait > self.max_retry_after:
                    how = (f"rerun with --wait-429 {math.ceil(wait)}, or try later" if wait <= MAX_WAIT_429 else
                           f"longer than --wait-429 can wait ({MAX_WAIT_429:g} s): try later")
                    raise HttpError(url, status, f"rate limited; Retry-After {retry_after}s is too long for "
                                    f"--wait-429 {self.max_retry_after:g} ({how})", final_url=final, retry_after=wait)
                self.sleep(max(wait, 0.5))
                continue
            detail = ""
            if status in (429, 503):
                detail = "rate limited" + (f"; Retry-After {retry_after}s" if retry_after else "") + \
                    (" (again after one wait)" if attempt else "")
            elif server_error:
                detail = "server error, again after one retry"
            raise HttpError(url, status, detail, final_url=final, retry_after=ra)

    def get_bytes(self, url: str, headers: dict | None = None, cap_mb: float = PAGE_CAP_MB) -> bytes:
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
        while True:
            resp = self.open(url, headers)
            try:
                cap = int(cap_mb * 1048576)
                n = resp.headers.get("Content-Length") if getattr(resp, "headers", None) else None
                if n and n.isdigit() and int(n) > cap:
                    raise FootageError(f"{redact(url)} is {int(n) / 1048576:.1f} MB, over the {cap_mb:g} MB page cap")
                body = read_or_fail(resp, cap + 1, url)
                if len(body) > cap:
                    raise FootageError(f"{redact(url)} is larger than the {cap_mb:g} MB page cap")
                status, final = getattr(resp, "status", None) or 200, _final_url(resp, url)
            finally:
                _close(resp)
            if is_challenge_page(body):
                self._challenge(host, url, status, final)  # raises, or waited once
                continue
            return body

    def head(self, url: str) -> dict:
        """{bytes, content_type} from a HEAD request (bytes None when the server does not say)."""
        resp = self.open(url, method="HEAD")
        try:
            h = getattr(resp, "headers", None)
            n = h.get("Content-Length") if h else None
            return {"bytes": int(n) if n and str(n).isdigit() else None,
                    "content_type": (h.get("Content-Type") if h else None) or None}
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


def _seconds(value):
    """Retry-After as seconds (a number or an HTTP date), else None."""
    if value in (None, ""):
        return None
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        pass
    try:  # Python 3.8/3.9 return None for an unreadable date, later versions raise
        when = email.utils.parsedate_to_datetime(str(value))
        return max(0.0, (when - _dt.datetime.now(when.tzinfo or _dt.timezone.utc)).total_seconds())
    except (TypeError, ValueError, IndexError, AttributeError):
        return None


def _final_url(resp, url: str) -> str:
    """The URL a response really came from (urllib follows redirects silently), else the one requested."""
    try:
        return (resp.geturl() if hasattr(resp, "geturl") else None) or url
    except Exception:
        return url


def read_or_fail(resp, n: int, url: str) -> bytes:
    """resp.read(n), with a timeout, a reset or a cut-off body after the headers turned into a FootageError."""
    try:
        return resp.read(n)
    except (OSError, HTTPException) as e:  # TimeoutError, ConnectionResetError, IncompleteRead …
        raise FootageError(f"{redact(url)}: transfer failed ({type(e).__name__})") from None


# ------------------------------------------------------------------------------------------------- licences

CC_URL_RE = re.compile(r"creativecommons\.org/(licenses|publicdomain)/([a-z+-]+)(?:/(\d(?:\.\d)?))?(/igo)?", re.I)
CC_ELEMENTS = {"by", "nc", "nd", "sa"}
# retired or non-standard licences that live under creativecommons.org/licenses/ but are not BY-[NC-ND-SA] combinations
CC_OTHER_NAMES = {"sampling": "Sampling", "sampling+": "Sampling+", "nc-sampling+": "NonCommercial Sampling+",
                  "devnations": "Developing Nations", "gpl": "GNU GPL", "lgpl": "GNU LGPL"}
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
        elements = parts.split("-")
        if "by" not in elements or not set(elements) <= CC_ELEMENTS:
            # Sampling 1.0 allows no copying of the whole work, Sampling+ no commercial copying of it, Developing
            # Nations applies only in developing countries, and all of them need credit: never read them as BY flags
            name = "CC " + CC_OTHER_NAMES.get(parts, parts) + (f" {ver}" if ver else "")
            return licence_record(name, url, attribution=True, commercial=None, derivatives=None, share_alike=None,
                                  verified=False, note="retired or non-standard CC licence: read the deed before use")
        return _cc_flags(elements, ver, bool(igo), url)
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
                extra=None, thumb_url=None, preview_url=None) -> dict:
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
        "thumb_url": https(thumb_url) or None,      # a still (JPEG/PNG) for screening before any download
        "preview_url": https(preview_url) or None,  # a small preview video (360p or so), never the full file
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
COMMONS_THUMB_W = "480"  # imageinfo then also returns thumburl, a still of the video


def commons_search_url(query: str, limit: int) -> str:
    q = {"action": "query", "format": "json", "formatversion": "2", "generator": "search",
         "gsrsearch": f"{query} filetype:video", "gsrnamespace": "6", "gsrlimit": str(max(1, min(limit, 50))),
         "prop": "imageinfo", "iiprop": COMMONS_IIPROP, "iiextmetadatafilter": COMMONS_META,
         "iiurlwidth": COMMONS_THUMB_W}
    return COMMONS_API + "?" + urllib.parse.urlencode(q)


def commons_lookup_url(*, titles=None, pageids=None) -> str:
    q = {"action": "query", "format": "json", "formatversion": "2", "prop": "imageinfo", "iiprop": COMMONS_IIPROP,
         "iiextmetadatafilter": COMMONS_META, "iiurlwidth": COMMONS_THUMB_W}
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
                               thumb_url=strip_tracking(info["thumburl"]) if info.get("thumburl") else None,
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


def size_fits(width, height, quality=None, max_quality=None, max_height=None) -> bool | None:
    """Whether a file is within --quality (its short side, so 1080 means 1080p in either orientation) and
    --max-height (its frame height). None when the size needed for the check is unknown."""
    short = quality or (min(width, height) if width and height else None)
    if max_quality:
        if short is None:
            return None
        if short > max_quality:
            return False
    if max_height:
        if height:
            return height <= max_height
        if short and short > max_height:
            return False  # the short side is a lower bound for the height
        return None
    return True


def pick_archive_file(files: list, max_bytes: int | None = None, max_quality: int | None = None,
                      max_height: int | None = None) -> dict | None:
    """The best video file of an item: highest resolution that fits under max_bytes (else the smallest one), and
    within --quality / --max-height when given (else the smallest file of known size)."""
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
    if max_quality or max_height:
        fit = [v for v in vids if size_fits(v[0][1], v[0][0], None, max_quality, max_height)]
        known = [v for v in vids if v[0][0]]
        vids = fit or ([min(known, key=lambda v: v[0][0])] if known else vids)
    vids.sort(key=lambda v: v[0], reverse=True)
    if max_bytes:
        for _key, size, f in vids:
            if size is None or size <= max_bytes:
                return f
        return min(vids, key=lambda v: v[1] or 0)[2]
    return vids[0][2]


# An Archive licence is whatever the uploader typed. These identifiers and titles mark copyrighted works re-uploaded
# under a licence their uploader cannot grant (seen live on 2026-10-29: "youtube-zILabWVdIMs Prince - Musicology
# (Official Music Video)" as CC BY 4.0, a y2mate rip as CC0, a "Free Willy ... music video ... VHS rip" as PDM).
SUSPICIOUS_ARCHIVE = (
    ("YouTube re-upload", re.compile(r"^youtube |\byoutube (?:video )?[a-z0-9_]{11}\b")),
    ("downloader rip", re.compile(r"\by ?2 ?mate\b|\bytmp[34]\b|\bsavefrom\b|\bsnaptube\b|\bclipconverter\b")),
    ("music video", re.compile(r"\bofficial (?:music )?video\b|\bmusic video\b|\blyrics? video\b|\bofficial audio\b")),
    ("film or TV rip", re.compile(r"\b(?:vhs|dvd|bd|br|web|hd|tv) ?rip\b|\bblu ?ray\b|\bfull episode\b|"
                                  r"\bepisode \d+\b|\bs\d{1,2} ?e\d{1,2}\b|\bfull movie\b|\bmovie\b|\btrailer\b")),
)


def archive_licence_suspicion(ident, title) -> str | None:
    """Why an Archive item's licence looks like an uploader's claim on someone else's work, else None."""
    text = re.sub(r"[\W_]+", " ", f"{ident or ''} {title or ''}".lower()).strip()
    for why, rx in SUSPICIOUS_ARCHIVE:
        if rx.search(text):
            return why
    return None


def archive_result(db: dict, doc: dict, meta: dict, max_bytes: int | None = None, caps: dict | None = None) -> dict | None:
    ident = doc.get("identifier") or (meta.get("metadata") or {}).get("identifier")
    md = meta.get("metadata") or {}
    f = pick_archive_file(meta.get("files") or [], max_bytes, **(caps or {}))
    if not ident or not f:
        return None
    licurl = doc.get("licenseurl") or md.get("licenseurl")
    lic = classify_licence(None, licurl) if licurl else licence_record(
        "unknown (no licenseurl)", None, verified=False, note="the uploader set no licence: rights unknown")
    title = doc.get("title") or md.get("title") or ident
    flags = ["uploader-licence"]
    why = archive_licence_suspicion(ident, title)
    if why and licurl:
        flags.append("suspicious-licence")
        lic.update(commercial=None, verified=False,
                   note=f"looks like a {why}: the uploader's licence claim on what is probably someone else's "
                        "copyrighted work; do not rely on it (trace the rights holder)")
    elif licurl:
        lic["note"] = ((lic.get("note") + "; ") if lic.get("note") else "") + \
            "set by the uploader, not checked by the Archive: trust the uploader? read the item page"
    creator = doc.get("creator") or md.get("creator")
    if isinstance(creator, list):
        creator = ", ".join(map(str, creator))
    fname = f["name"]
    q = urllib.parse.quote(ident)
    return make_result(db, "archive", ident, title=title,
                       page_url=f"https://archive.org/details/{ident}",
                       file_url=f"https://archive.org/download/{q}/{urllib.parse.quote(fname)}",
                       licence=lic, author=creator, width=f.get("width"), height=f.get("height"),
                       duration=f.get("length"), size=f.get("size"), flags=flags,
                       thumb_url=f"https://archive.org/services/img/{q}",
                       extra={"native": {"file": fname, "format": f.get("format"),
                                         **({"suspicious": why} if why and licurl else {})}})


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
            img = next((ln.get("href") for ln in it.get("links") or [] if isinstance(ln, dict)
                        and ln.get("rel") == "preview" and isinstance(ln.get("href"), str)), None)
            out.append({**d, **({"_preview_image": quote_path(https(img))} if img else {})})
    return out


NASA_VARIANTS = ("~orig.mp4", "~large.mp4", "~medium.mp4", "~mobile.mp4", "~small.mp4")


def quote_path(url: str) -> str:
    """url with its path percent-encoded exactly once. The NASA asset API returns links with raw spaces
    (".../video/Causeway Main Launch dust removal/...~orig.mp4"), which http.client refuses (InvalidURL)."""
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(p._replace(path=urllib.parse.quote(urllib.parse.unquote(p.path), safe="/~")))


def nasa_page_url(nasa_id: str) -> str:
    return "https://images.nasa.gov/details/" + urllib.parse.quote(str(nasa_id), safe="")


def nasa_variants(asset: dict) -> tuple:
    """([video URLs, largest first], metadata.json URL) from https://images-api.nasa.gov/asset/<nasa_id>."""
    hrefs = [quote_path(https(i.get("href"))) for i in ((asset or {}).get("collection") or {}).get("items") or []
             if isinstance(i.get("href"), str) and i.get("href")]
    meta = next((h for h in hrefs if h.endswith("/metadata.json")), None)
    vids = [h for tag in NASA_VARIANTS for h in hrefs if h.endswith(tag)]
    if not vids:
        vids = [h for h in hrefs if h.lower().endswith(VIDEO_EXT) and "~preview" not in h][:1]
    return vids, meta


def nasa_preview(asset: dict) -> str | None:
    """The small ~preview.mp4 (else ~mobile/~small) of a NASA asset, for contact sheets."""
    hrefs = [quote_path(https(i.get("href"))) for i in ((asset or {}).get("collection") or {}).get("items") or []
             if isinstance(i.get("href"), str) and i.get("href")]
    return next((h for tag in ("~preview.mp4", "~mobile.mp4", "~small.mp4") for h in hrefs if h.endswith(tag)), None)


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


def nasa_result(db: dict, d: dict, video_url: str, dims: dict | None = None, alternates=(), preview=None) -> dict:
    nid = d["nasa_id"]
    author = d.get("secondary_creator") or d.get("photographer") or (f"NASA {d['center']}" if d.get("center") else "NASA")
    flags = ["check-third-party-credit"] if re.search(r"©|copyright", str(d.get("description", "")), re.I) else []
    dims = dims or {}
    return make_result(db, "nasa", nid, title=d.get("title") or nid, page_url=nasa_page_url(nid),
                       file_url=video_url, licence=source_licence("nasa", sources_by_id(db).get("nasa")),
                       author=author, width=dims.get("width"), height=dims.get("height"),
                       duration=dims.get("duration"), mime="video/mp4", flags=flags,
                       thumb_url=d.get("_preview_image"), preview_url=preview,
                       extra={"native": {"center": d.get("center"), "date_created": d.get("date_created"),
                                         **({"keywords": d["keywords"]} if isinstance(d.get("keywords"), list) else {})},
                              **({"alternates": [a for a in alternates if a != video_url]} if alternates else {})})


def search_nasa(http: Http, db: dict, query: str, limit: int, opts: dict) -> list:
    out = []
    for d in parse_nasa_search(http.get_json(nasa_search_url(query, limit * 2)))[: limit * 2]:
        try:
            asset = http.get_json(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(d['nasa_id'])}")
            vids, meta_url = nasa_variants(asset)
            video = vids[0] if vids else None
            dims = {}
            if video and meta_url and (opts.get("min_height") or opts.get("orientation") or opts.get("details")
                                       or opts.get("resolve")):
                dims = parse_nasa_metadata(http.get_json(meta_url))
        except FootageError as e:
            opts.setdefault("warnings", []).append(f"nasa {d['nasa_id']}: {e}")
            continue
        if video:
            out.append(nasa_result(db, d, video, dims, vids, nasa_preview(asset)))
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
    area = lambda f: (_int(f.get("height")) or 0) * (_int(f.get("width")) or 0)  # noqa: E731
    best, small = max(files, key=area), min(files, key=area)
    user = v.get("user") or {}
    return make_result(db, "pexels", v.get("id"), title=pexels_title(v.get("url", "")), page_url=v.get("url"),
                       file_url=best["link"], licence=source_licence("pexels", sources_by_id(db).get("pexels")),
                       author=user.get("name"), width=best.get("width"), height=best.get("height"),
                       duration=v.get("duration"), mime=best.get("file_type"),
                       thumb_url=v.get("image") if isinstance(v.get("image"), str) else None,
                       preview_url=small["link"] if small is not best else None,
                       extra={"native": {"author_url": user.get("url")},
                              "variants": file_variants((f["link"], f.get("width"), f.get("height"), None)
                                                        for f in files)})


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
    have = [vids[s] for s in ("large", "medium", "small", "tiny") if (vids.get(s) or {}).get("url")]
    if not have:
        return None
    best = have[0]
    thumb = next((x["thumbnail"] for x in have if isinstance(x.get("thumbnail"), str) and x["thumbnail"]), None)
    tags = str(h.get("tags") or "").strip()
    return make_result(db, "pixabay", h.get("id"), title=tags.capitalize() if tags else "Pixabay clip",
                       page_url=h.get("pageURL"), file_url=best["url"],
                       licence=source_licence("pixabay", sources_by_id(db).get("pixabay")), author=h.get("user"),
                       width=best.get("width"), height=best.get("height"), duration=h.get("duration"),
                       size=best.get("size"), mime="video/mp4", thumb_url=thumb,
                       preview_url=have[-1]["url"] if len(have) > 1 else None,
                       extra={"variants": file_variants((x["url"], x.get("width"), x.get("height"), x.get("size"))
                                                        for x in have)})


def file_variants(items) -> list:
    """[{quality, width, height, bytes, url}] largest first, from (url, width, height, bytes) tuples; quality is
    the short side (1080 for a 1080x1920 file)."""
    out = []
    for url, w, h, size in items:
        w, h = _int(w) or None, _int(h) or None
        out.append({"quality": min(w, h) if w and h else None, "width": w, "height": h,
                    "bytes": _int(size) or None, "url": url})
    out.sort(key=lambda v: (v["width"] or 0) * (v["height"] or 0), reverse=True)
    return out


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
        tsrc = re.search(r'\ssrc="(https://assets\.mixkit\.co/[^"]+)"', thumb.group(0)) if thumb else None
        video = re.search(r'<video[^>]*\ssrc="(https://assets\.mixkit\.co/[^"]+)"', chunk)
        if cid not in cards:
            order.append(cid)
            cards[cid] = {"title": title, "page": "https://mixkit.co" + link.group(1) if link else None,
                          "dims": _scale_to_short_side(int(tw.group(1)), int(th.group(1)), 720) if tw and th else (None, None),
                          "thumb": _html.unescape(tsrc.group(1)) if tsrc else None,
                          "preview": _html.unescape(video.group(1)) if video else None}
    for cid in ld:
        if cid not in cards:
            order.append(cid)
            cards[cid] = {"title": None, "page": None, "dims": (None, None), "thumb": None, "preview": None}
    out = []
    for cid in order:
        o, c = ld.get(cid) or {}, cards[cid]
        page_url = c["page"] or str(o.get("@id") or "").split("#")[0] or f"https://mixkit.co/free-stock-video/{cid}/"
        lic = mixkit_licence(o.get("copyrightNotice"))
        w, h = c["dims"]
        flags = ([] if lic["verified"] else ["licence-checked-at-download"]) + (["size-from-thumbnail"] if w else [])
        thumb = c["thumb"] or _ld_url(o.get("thumbnailUrl"))
        preview = c["preview"] or _ld_url(o.get("embedUrl"))
        kind, base = mixkit_pattern(cid, _ld_url(o.get("contentUrl")), preview, thumb)
        out.append(mixkit_apply_files(make_result(
            db, "mixkit", cid, title=c["title"] or o.get("name") or f"Mixkit clip {cid}", page_url=page_url,
            file_url=mixkit_file(cid, 720), licence=lic, quality=720, width=w, height=h, duration=o.get("duration"),
            mime="video/mp4", flags=flags, thumb_url=thumb, preview_url=preview,
            extra={"native": {"files": kind, **({"files_base": base} if base else {})}} if kind else None)))
    return out


def _ld_url(v) -> str | None:
    if isinstance(v, list):
        v = next((x for x in v if isinstance(x, str)), None)
    if isinstance(v, dict):
        v = v.get("url") or v.get("contentUrl")
    return v if isinstance(v, str) and v.startswith(("https://", "http://")) else None


MIXKIT_FREE_SIZES = (2160, 1080, 720)  # tried in this order; a size the clip lacks answers 403
MIXKIT_ROUTE_RE = re.compile(r"^https://mixkit\.co/free-stock-video/download/\d+/")


def mixkit_pattern(cid, *urls) -> tuple:
    """How a Mixkit clip's files are named, from any of its asset links (content, preview, thumbnail):
    ("legacy", None) for assets.mixkit.co/videos/<id>/<id>-<q>.mp4; ("active_storage", base) for
    .../active_storage/video_items/<id>/<ts>/<id>-video-<q>.mp4; ("hashed", None) for opaque assets.mixkit.co/<hash>
    links, whose per-size files are only named by the clip page's download route; (None, None) when unknown."""
    cid = str(cid)
    hashed = False
    for u in urls:
        if not isinstance(u, str):
            continue
        if re.search(rf"assets\.mixkit\.co/videos/{cid}/{cid}-", u):
            return "legacy", None
        m = re.match(rf"(https?://assets\.mixkit\.co/active_storage/video_items/{cid}/\d+/{cid}-video)-", u)
        if m:
            return "active_storage", https(m.group(1))
        if re.match(r"https?://assets\.mixkit\.co/[a-z0-9]{16,}/?$", u):
            hashed = True
    return ("hashed", None) if hashed else (None, None)


def mixkit_file(cid, short_side: int, kind: str | None = None, base: str | None = None) -> str | None:
    """The direct file of one size: the <id>-<q>.mp4 template, the active_storage name, or None for hashed links."""
    if kind == "active_storage" and base:
        return f"{base}-{short_side}.mp4"
    if kind == "hashed":
        return None
    return f"https://assets.mixkit.co/videos/{cid}/{cid}-{short_side}.mp4"


def mixkit_quality(url: str) -> int | None:
    m = re.search(r"-(\d{3,4})\.mp4$", urllib.parse.urlsplit(url or "").path)
    return int(m.group(1)) if m else None


def _attr(tag: str, name: str) -> str | None:
    m = re.search(r'\s' + re.escape(name) + r'="([^"]*)"', tag)
    return _html.unescape(m.group(1)) if m else None


def mixkit_page_variants(page: str, cid) -> list:
    """The sizes a Mixkit clip page offers, largest first: [{quality, label, mb, bytes, width, height, route}].

    Free clips list radio inputs (data-label="Full HD", data-size="44.59" MB, value="/free-stock-video/download/<id>/
    ?context=sidebar&type=1080p") followed by the resolution; a Restricted clip has one "Download low resolution for
    free" button whose route has no type (its free file is 720p). The route answers a small page naming the file
    (data-download--modal-url-value="https://assets.mixkit.co/<hash>"); see mixkit_follow_route."""
    cid = str(cid)
    out = []
    for m in re.finditer(r'\svalue="(/free-stock-video/download/' + re.escape(cid) + r'/[^"]*)"', page):
        start = page.rfind("<", 0, m.start())
        end = page.find(">", m.end())
        tag = page[start:end + 1]
        if not tag.startswith("<input"):
            continue
        route = "https://mixkit.co" + _html.unescape(m.group(1))
        q = re.search(r"[?&]type=(\d{3,4})p\b", route)
        after = page[end + 1:end + 600]
        after = after.split("<input", 1)[0]
        res = re.search(r'download-resolution">\s*(\d{3,5})\s*[x×]\s*(\d{3,5})', after)
        mb = _float(_attr(tag, "data-size"))
        out.append({"quality": int(q.group(1)) if q else None, "label": _attr(tag, "data-label"), "mb": mb,
                    "bytes": int(round(mb * 1048576)) if mb else None,
                    "listed": f"{res.group(1)}x{res.group(2)}" if res else None,
                    "width": None, "height": None, "route": route})
    if not out:
        m = re.search(r'data-download--button-modal-url-value="(/free-stock-video/download/' + re.escape(cid) + r'/[^"]*)"',
                      page)
        if m:
            route = "https://mixkit.co" + _html.unescape(m.group(1))
            q = re.search(r"[?&]type=(\d{3,4})p\b", route)
            out.append({"quality": int(q.group(1)) if q else 720, "label": "free low resolution", "mb": None,
                        "bytes": None, "listed": None, "width": None, "height": None, "route": route})
    out = [v for v in out if v["quality"]]
    out.sort(key=lambda v: v["quality"], reverse=True)
    # Width and height from the listed resolution when its short side is the size and its aspect is within 10% of
    # the next larger size's (4096x2160 then 1920x1080 is fine); the site lists the 720p file of a 16:9 clip as
    # "1080x720", so such a size is scaled from the next larger one instead (1280x720).
    ref = None
    for v in out:
        dims = tuple(map(int, v["listed"].split("x"))) if v["listed"] else None
        ok = bool(dims) and min(dims) == v["quality"]
        if ok and ref and abs(dims[0] / dims[1] - ref[0] / ref[1]) > 0.10 * ref[0] / ref[1]:
            ok = False
        if ok:
            v["width"], v["height"] = dims
        elif ref:
            v["width"], v["height"] = _scale_to_short_side(ref[0], ref[1], v["quality"])
        if v["width"] and v["height"]:
            ref = (v["width"], v["height"])
    return out


def mixkit_follow_route(http: Http, route: str) -> str:
    """The file a Mixkit download route names (the link the site's own download button follows)."""
    page = http.get_text(route)  # a Cloudflare check raises ChallengeError here
    m = re.search(r'data-download--modal-url-value="(https://assets\.mixkit\.co/[^"]+)"', page)
    if not m:
        raise FootageError(f"{route}: the download page names no file (the site changed or sent another page)")
    return _html.unescape(m.group(1))


def is_mixkit_route(url) -> bool:
    return bool(MIXKIT_ROUTE_RE.match(str(url or "")))


def allowed_variants(rec: dict) -> list:
    """The file sizes a record may be fetched at: every listed size, except that a Mixkit clip that is not Free
    (Restricted, or its licence unread) gets 720p and below only."""
    vs = [v for v in rec.get("variants") or [] if isinstance(v, dict)]
    if rec.get("source") == "mixkit" and (rec.get("licence") or {}).get("name") != MIXKIT_FREE:
        vs = [v for v in vs if (v.get("quality") or 0) <= 720]
    return vs


def mixkit_apply_files(rec: dict) -> dict:
    """Point a Mixkit record at the files its licence lets a script fetch, largest first.

    With the clip page read (rec["variants"], from mixkit_page_variants), the sizes are the ones the page offers:
    each as its direct file when the naming is known (the <id>-<q>.mp4 template or the active_storage name), then its
    download route, which is the only way to a newer clip's hashed file. Without them: Free clips serve
    <id>-1080.mp4 to plain scripts and often <id>-2160.mp4 (measured 2026-10-29: 206 video/mp4); Restricted clips
    answer 403 above 720p, and their free 720p file is for personal use only. A clip whose licence has not been read
    yet gets the 720p file until confirm_licence reads its page. quality is the size a Free clip is known to have
    (the largest listed, else 1080), so --min-height does not count on a 2160p file that may not exist."""
    cid = rec["id"].split(":", 1)[-1]
    if not cid.isdigit():  # a hand-made record for some other mixkit.co link (manual_record): keep its own file
        return rec
    free = (rec.get("licence") or {}).get("name") == MIXKIT_FREE
    nat = rec.get("native") or {}
    kind, base = nat.get("files"), nat.get("files_base")
    vs = allowed_variants(rec)
    if vs:
        for v in vs:
            v["url"] = v.get("url") or mixkit_file(cid, v["quality"], kind, base)
        files = [u for v in vs for u in (v.get("url"), v.get("route")) if u]
        top = vs[0]
        rec.update(file_url=files[0], quality=top["quality"], bytes=top.get("bytes") or rec.get("bytes"))
        if top.get("width") and top.get("height"):
            rec["width"], rec["height"] = top["width"], top["height"]
            rec["flags"] = [f for f in rec.get("flags", []) if f != "size-from-thumbnail"]
    else:
        files = [u for u in (mixkit_file(cid, q, kind, base) for q in (MIXKIT_FREE_SIZES if free else (720,))) if u]
        if not files:  # a hashed clip whose page was not read: the 720p template, which download explains if it fails
            files = [mixkit_file(cid, 720)]
        quality = 1080 if free else 720
        w, h, was = rec.get("width"), rec.get("height"), rec.get("quality")
        if w and h and was and was != quality:
            rec["width"], rec["height"] = _scale_to_short_side(w, h, quality)
        rec.update(file_url=files[0], quality=quality)
    if len(files) > 1:
        rec["alternates"] = files[1:]
    else:
        rec.pop("alternates", None)
    return rec


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
    # the discover page does not name each clip's licence or real size: read them from the pages of the clips that
    # pass the other filters (one request each, at most 2 x limit, and no more once `limit` clips are kept) when
    # --resolve, --commercial or --details asks for it, or when --min-height drops a clip at 720p that would pass at
    # the 1080p a Free clip has
    need, mh = opts.get("commercial") or opts.get("details") or opts.get("resolve"), opts.get("min_height")
    rest = {**opts, "commercial": False, "min_height": None}
    tall = {**rest, "min_height": mh}

    def as_free(r):  # the same clip at the 1080p a Free licence gives
        return mixkit_apply_files({**r, "licence": {"name": MIXKIT_FREE}, "native": {}, "variants": []})

    read = kept = 0
    for rec in found:
        if read >= limit * 2 or kept >= limit:
            break
        if not rec["licence"]["verified"] and keep(rec, rest) is None and \
                (need or (mh and keep(rec, tall) is not None and keep(as_free(rec), tall) is None)):
            confirm_licence(http, db, rec)
            read += 1
            if "mixkit.co" in http.challenged:  # no more requests to it in this run
                opts.setdefault("warnings", []).append(
                    "mixkit: mixkit.co answered with a Cloudflare browser check; the other clips' licences were "
                    "left unread (run the search again in a few minutes)")
                break
        if keep(rec, opts) is None:
            kept += 1
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
        urls = v.get("urls") if isinstance(v.get("urls"), dict) else {}
        preview = urls.get("mp4Preview") or urls.get("mp4_preview")
        if not isinstance(preview, str) and re.search(r"/\d{3,4}p\.mp4$", mp4):
            preview = re.sub(r"/\d{3,4}p\.mp4$", "/360p.mp4", mp4)  # Coverr serves every clip at 360p too
        thumb = next((x for x in (v.get("thumbnail"), v.get("poster"), urls.get("thumbnail"), urls.get("poster"))
                      if isinstance(x, str) and x.startswith("http")), None)
        out.append(make_result(db, "coverr", vid, title=(v.get("title") or "").strip() or slug,
                               page_url=f"https://coverr.co/videos/{slug}", file_url=mp4,
                               licence=source_licence("coverr", sources_by_id(db).get("coverr")), author=author,
                               width=w, height=h, duration=v.get("duration"), mime="video/mp4", flags=flags,
                               thumb_url=thumb, preview_url=preview if isinstance(preview, str) else None,
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


STOP_WORDS = {"a", "an", "the", "of", "in", "on", "at", "and", "or", "with", "for", "to", "from", "by", "into",
              "over", "under", "video", "videos", "footage", "clip", "clips", "stock", "free", "hd", "4k"}
# Title words that name a person or a body part. A title heuristic only: a clip can show people its title does not
# name, so screen the contact sheet (preview) as well.
PEOPLE_WORDS = set("""
woman women man men girl girls boy boys couple couples portrait portraits person persons people child children kid
kids baby babies toddler toddlers family families lady ladies guy guys teen teens teenager teenagers face faces
selfie model models dancer dancers dancing crowd crowds friend friends businessman businessmen businesswoman
businesswomen mother father mom dad daughter son bride groom wedding player players athlete athletes worker workers
tourist tourists student students doctor nurse grandmother grandfather husband wife boyfriend girlfriend lover lovers
someone somebody human humans hiker hikers surfer surfers skater skaters runner runners cyclist cyclists chef farmer
farmers soldier soldiers silhouette silhouettes hand hands finger fingers feet foot legs she he her his
""".split())


def _stem(w: str) -> str:
    for suf in ("ing", "es", "s", "ed"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def query_terms(query: str) -> list:
    words = re.findall(r"[a-z0-9]+", str(query or "").lower())
    kept = [w for w in words if w not in STOP_WORDS] or words
    return list(dict.fromkeys(_stem(w) for w in kept))


def relevance(r: dict, query: str) -> float | None:
    """The share of the query's words (stemmed, stop words left out) found in the result's title or keywords, 0..1;
    None when the query has no words. Sites match loosely (a Mixkit "seedling" search returned "Woman sending
    messages on Whatsapp"), so 0 means the title shares nothing with the query."""
    terms = query_terms(query)
    if not terms:
        return None
    nat = r.get("native") or {}
    hay = " ".join([str(r.get("title") or "")] + [str(k) for k in nat.get("keywords") or []]).lower()
    words = {_stem(w) for w in re.findall(r"[a-z0-9]+", hay)}
    squashed = re.sub(r"[^a-z0-9]+", "", hay)
    hits = 0
    for t in terms:
        if t in words or (len(t) >= 5 and t in squashed) or \
                (len(t) >= 4 and any(len(w) >= 4 and (w.startswith(t) or t.startswith(w)) for w in words)):
            hits += 1
    return round(hits / len(terms), 2)


def people_word(r: dict) -> str | None:
    """The first title word that names a person (woman, man, couple, portrait, hands ...), else None."""
    return next((w for w in re.findall(r"[a-z]+", str(r.get("title") or "").lower()) if w in PEOPLE_WORDS), None)


def commercial_drop_reason(r: dict) -> str:
    """Why --commercial drops a result, one reason per cause so the counts say what to do next."""
    lic, flags = r.get("licence") or {}, r.get("flags") or []
    if lic.get("commercial") is False:
        return "Mixkit Restricted (personal use only)" if lic.get("name") == MIXKIT_RESTRICTED else "non-commercial licence"
    if "suspicious-licence" in flags:
        return "suspicious uploader licence (music video, film or rip)"
    if r.get("source") == "mixkit" and not lic.get("verified"):
        return "Mixkit licence not read (the clip page did not answer)"
    return "commercial use not confirmed"


def keep(r: dict, opts: dict) -> str | None:
    """None when the result passes the filters, else the reason it is dropped."""
    lic = r.get("licence") or {}
    if lic.get("derivatives") is False and not opts.get("allow_nd"):
        return "no-derivatives licence (a montage is an edit)"
    if opts.get("commercial") and lic.get("commercial") is not True:
        return commercial_drop_reason(r)
    if not opts.get("any_licence") and lic.get("name", "").startswith("unknown"):
        return "unknown licence"
    if opts.get("no_ai") and "ai-generated" in r.get("flags", []):
        return "AI-generated"
    if opts.get("no_people") and people_word(r):
        return "people named in the title (--no-people)"
    match = opts.get("match")
    if match in ("any", "all"):
        rel = relevance(r, opts.get("query") or "")
        if rel is not None and (rel == 0 if match == "any" else rel < 1):
            return "title matches no query word (--match any)" if match == "any" else \
                "title misses a query word (--match all)"
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
                                                  "no_ai", "no_people", "match", "resolve") if opts.get(k)},
              "limit_per_source": limit, "sources": {}, "results": [], "warnings": []}
    opts = {**opts, "query": query}
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
            if getattr(e, "retry_after", None) is not None:
                report["sources"][name]["retry_after"] = e.retry_after
            if isinstance(e, ChallengeError):
                report["sources"][name]["challenge"] = True
            report["warnings"].extend(redact(w) for w in local.get("warnings", []))
            continue
        except (KeyError, TypeError, ValueError, AttributeError) as e:  # a changed page or API shape
            report["sources"][name] = {"status": "error", "detail": f"could not read the answer ({type(e).__name__}); "
                                       "the site may have changed"}
            continue
        except (OSError, HTTPException) as e:  # backstop: a network failure Http did not word; the others go on
            report["sources"][name] = {"status": "error", "detail": f"network failure ({type(e).__name__})"}
            continue
        kept, dropped = [], {}
        for r in found:
            why = keep(r, opts)
            if why:
                dropped[why] = dropped.get(why, 0) + 1
            elif len(kept) < limit:
                r["query"] = query
                r["relevance"] = relevance(r, query)
                kept.append(r)
        report["results"].extend(kept)
        report["sources"][name] = {"status": "ok", "count": len(kept), "found": len(found),
                                   **({"dropped": dropped} if dropped else {})}
        if name == "archive" and kept:
            sus = sum("suspicious-licence" in r.get("flags", []) for r in kept)
            report["warnings"].append(
                "archive: every licence is the uploader's own claim, not checked by the Archive (trust the uploader?)"
                + (f"; {sus} look like music videos, films, TV or YouTube rips and are marked suspicious-licence "
                   "(commercial ?)" if sus else ""))
        report["warnings"].extend(redact(w) for w in local.get("warnings", []))
    return report


def _size_text(r: dict) -> str:
    if r.get("width") and r.get("height"):
        est = "~" if "size-from-thumbnail" in (r.get("flags") or []) else ""
        return f"{est}{r['width']}x{r['height']}"
    return f"{r['quality']}p" if r.get("quality") else "?"


def print_results(report: dict) -> None:
    for name, st in report["sources"].items():
        extra = f"{st.get('count', 0)} kept of {st.get('found', 0)}" if st["status"] == "ok" else st.get("detail", "")
        if st.get("dropped"):
            extra += " (dropped: " + ", ".join(f"{v} {k}" for k, v in st["dropped"].items()) + ")"
        ra = st.get("retry_after")
        if st["status"] == "error" and ra is not None and "--wait-429" not in extra:
            extra += (f" [Retry-After {ra:g}s: --wait-429 {math.ceil(ra)} waits for it (at most {MAX_WAIT_429:g})"
                      if ra <= MAX_WAIT_429 else f" [Retry-After {ra:g}s: longer than --wait-429 can wait") + \
                ", or search again later with --retry-failed]"
        print(f"# {name:10} {st['status']:11} {extra}")
    for w in report.get("warnings", []):
        print(f"# warning: {w}")
    unread = loose = 0
    for r in report["results"]:
        dur = f"{r['duration']:.0f}s" if r.get("duration") else "?"
        lic = r["licence"]
        flags = r.get("flags") or []
        com = {True: "commercial ok", False: "NON-commercial", None: "commercial ?"}[lic.get("commercial")]
        att = "credit required" if lic.get("attribution_required") else ("credit optional" if lic.get("attribution_required") is False else "credit ?")
        name = lic.get("name")
        if "suspicious-licence" in flags:
            name = f"{name} SUSPICIOUS (uploader's claim)"
        elif "uploader-licence" in flags:
            name = f"{name} (uploader's claim)"
        if r.get("source") == "mixkit" and not lic.get("verified"):
            unread += 1
        if r.get("relevance") == 0:
            loose += 1
        print(f"{r['id']}\t{_size_text(r)}\t{dur}\t{name} | {com} | {att}\t{(r.get('title') or '')[:70]}")
    if unread:
        print(f"# note: {unread} Mixkit licence(s) and real sizes are not read yet (~ sizes are thumbnail guesses): "
              "--resolve reads each clip page (one request per clip); --commercial does too")
    if loose:
        print(f"# note: {loose} result(s) share no word with the query in their title (the site matched loosely); "
              "--match any drops them")


# ------------------------------------------------------------------------------------------------- download

def pick_from_results(results_path: Path, rid: str) -> dict | None:
    try:
        data = json.loads(Path(results_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return next((r for r in data.get("results", []) if isinstance(r, dict) and r.get("id") == rid), None)


def load_results(path: Path) -> dict | None:
    """An earlier results file (kosif.free_footage.results.v1), else None."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("schema") == RESULTS_SCHEMA else None


def _norm_query(q) -> str:
    return re.sub(r"\s+", " ", str(q or "").strip().lower())


def search_entry(report: dict) -> dict:
    return {"query": report.get("query"), "searched_at": report.get("searched_at"), "filters": report.get("filters", {}),
            "sources": report.get("sources", {}), "ids": [r.get("id") for r in report.get("results", [])]}


def merge_results(prev: dict | None, report: dict) -> dict:
    """The new search on top of the earlier results file: this search's results first, then every earlier result
    whose id it did not return (each keeps the query that found it), and a `searches` history. A Mixkit result whose
    licence an earlier search read is not replaced by the same clip unread. The top-level query, sources and filters
    describe the newest search, as before."""
    merged = dict(report)
    old = [r for r in (prev or {}).get("results", []) if isinstance(r, dict) and r.get("id")]
    by_old = {r["id"]: r for r in old}
    new = []
    for r in report.get("results", []):
        o = by_old.get(r.get("id"))
        if o and r.get("source") == "mixkit" and not (r.get("licence") or {}).get("verified") \
                and (o.get("licence") or {}).get("verified"):
            r = {**o, "query": r.get("query"), "relevance": r.get("relevance")}
        new.append(r)
    seen = {r.get("id") for r in new}
    merged["results"] = new + [r for r in old if r["id"] not in seen]
    history = list((prev or {}).get("searches") or ([search_entry(prev)] if prev else []))
    merged["searches"] = (history + [search_entry(report)])[-RESULTS_HISTORY:]
    return merged


def save_results(path: Path, report: dict, replace: bool = False) -> dict:
    """Write the results file, merged with the earlier one unless replace (the old overwrite)."""
    path = Path(path)
    data = {**report, "searches": [search_entry(report)]} if replace else merge_results(load_results(path), report)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(path)
    return data


def answered_sources(prev: dict | None, query: str) -> dict:
    """{source: (status record, searched_at)} for the sources that answered the last time this query was saved."""
    out = {}
    for entry in (prev or {}).get("searches") or ([search_entry(prev)] if prev else []):
        if _norm_query(entry.get("query")) != _norm_query(query):
            continue
        for name, st in (entry.get("sources") or {}).items():
            if isinstance(st, dict) and st.get("status") in ("ok", "cached"):
                out[name] = (st, entry.get("searched_at"))
            elif name in out:
                out.pop(name)  # it failed in a later search of the same query
    return out


def resolve_id(http: Http, db: dict, rid: str, opts: dict) -> dict:
    source, _, native = rid.partition(":")
    if not native:
        raise FootageError(f"{rid!r} is not a result id (source:id) or a URL")
    if source == "wikimedia":
        found = parse_wikimedia(db, http.get_json(commons_lookup_url(pageids=native)))
    elif source == "archive":
        meta = http.get_json(f"https://archive.org/metadata/{urllib.parse.quote(native)}")
        caps = {k: opts.get(k) for k in ("max_quality", "max_height") if opts.get(k)}
        found = [r for r in [archive_result(db, {"identifier": native}, meta, opts.get("max_bytes"), caps)] if r]
    elif source == "nasa":
        docs = [d for d in parse_nasa_search(http.get_json(nasa_search_url(nasa_id=native, limit=1))) if d["nasa_id"] == native]
        found = []
        if docs:
            asset = http.get_json(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(native)}")
            vids, _meta = nasa_variants(asset)
            found = [nasa_result(db, docs[0], vids[0], alternates=vids, preview=nasa_preview(asset))] if vids else []
    elif source == "mixkit" and native.isdigit():
        # /free-stock-video/<id>/ redirects to a search page, but any "<slug>-<id>/" redirects to the clip's own page,
        # whose licence notice confirm_licence reads (and whose canonical link replaces this page_url)
        found = [make_result(db, "mixkit", native, title=f"Mixkit clip {native}",
                             page_url=f"https://mixkit.co/free-stock-video/clip-{native}/", file_url=mixkit_file(native, 720),
                             licence=mixkit_licence(None), quality=720, mime="video/mp4")]  # sizes follow the licence
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
        except (OSError, HTTPException) as e:  # URLError (DNS, refused, timeout) is an OSError
            raise FootageError(f"pexels {cid}: the download endpoint did not answer "
                               f"({type(getattr(e, 'reason', e)).__name__})") from None
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


def confirm_licence(http: Http, db: dict, rec: dict, files: bool = False) -> dict:
    """Mixkit: read the clip page's own licence notice before downloading (Free vs Restricted), and with it the sizes
    the page offers (rec["variants"]), the thumbnail and the preview. files=True reads the page even when the licence
    is already known, for a record that has no sizes yet (results written before sizes were recorded)."""
    if rec.get("source") != "mixkit" or not rec["id"].split(":", 1)[-1].isdigit():
        return rec
    if (rec.get("licence") or {}).get("verified") and not (files and "variants" not in rec):
        return rec
    try:
        page = http.get_text(rec["page_url"])
    except ChallengeError:
        if files and not (rec.get("licence") or {}).get("verified"):
            raise  # download without a known licence: stop this target and say so, rather than guess
        rec["licence"]["note"] = (rec["licence"].get("note") or "") + \
            "; the clip page answered with a Cloudflare browser check (not read)"
        rec.setdefault("native", {})["page_error"] = "Cloudflare browser check"
        return rec
    except FootageError as e:
        rec["licence"]["note"] = (rec["licence"].get("note") or "") + f"; the clip page could not be read ({e})"
        rec.setdefault("native", {})["page_error"] = str(redact(e))[:300]
        return rec
    notice = mixkit_page_notice(page)
    cid = rec["id"].split(":", 1)[1]
    canon = re.search(r'<link[^>]*rel="canonical"[^>]*href="(https://mixkit\.co/free-stock-video/[^"]*-' + re.escape(cid)
                      + r'/)"', page)
    if canon:
        rec["page_url"] = canon.group(1)  # the clip's real page, not the redirecting clip-<id>/ form
    vo = next((o for o in _ld_objects(page) if o.get("@type") == "VideoObject"), {})
    nat = rec.setdefault("native", {})
    nat.pop("page_error", None)
    content, embed, thumb = _ld_url(vo.get("contentUrl")), _ld_url(vo.get("embedUrl")), _ld_url(vo.get("thumbnailUrl"))
    kind, base = mixkit_pattern(cid, content, embed, thumb)
    if kind:
        nat["files"] = kind
        if base:
            nat["files_base"] = base
        else:
            nat.pop("files_base", None)
    rec["thumb_url"] = https(thumb) or rec.get("thumb_url")
    rec["preview_url"] = https(embed) or rec.get("preview_url")
    rec["variants"] = mixkit_page_variants(page, cid)  # [] when the page lists none (the template sizes apply)
    if vo.get("name") and str(rec.get("title") or "").startswith("Mixkit clip"):
        rec["title"] = clean_text(vo["name"])
    if rec.get("duration") is None and vo.get("duration"):
        rec["duration"] = _float(vo["duration"])
    if notice:
        lic = mixkit_licence(notice)
        rec["licence"] = lic
        rec["flags"] = [f for f in rec.get("flags", []) if f != "licence-checked-at-download"]
        rec["attribution"] = format_attribution(((sources_by_id(db).get("mixkit") or {}).get("attribution") or {}).get("template"),
                                                title=rec.get("title"), source="Mixkit", licence=lic["name"],
                                                licence_url=lic["url"], page_url=rec["page_url"])
    mixkit_apply_files(rec)  # a Free clip at its largest listed size (else 2160p/1080p), a Restricted one at 720p
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
                chunk = read_or_fail(resp, 1 << 20, url)  # a reset or a stalled read mid-file is a FootageError
                if not chunk:
                    break
                if first:
                    if not looks_like_video(chunk[:512], ctype):
                        if is_challenge_page(chunk):
                            host = (urllib.parse.urlsplit(url).hostname or "").lower()
                            http.challenged.add(host)
                            raise ChallengeError(url, getattr(resp, "status", None) or 200, final_url=_final_url(resp, url))
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
                              "stream=width,height,codec_name,r_frame_rate,pix_fmt,color_range,color_space,"
                              "color_transfer,color_primaries:format=duration,format_name", "-of", "json", str(path)],
                             capture_output=True, text=True, timeout=60)
        d = json.loads(out.stdout or "{}")
        s = (d.get("streams") or [{}])[0]
        f = d.get("format") or {}
        return {k: v for k, v in {"width": s.get("width"), "height": s.get("height"), "codec": s.get("codec_name"),
                                  "fps": s.get("r_frame_rate"), "duration": _float(f.get("duration")),
                                  "pix_fmt": s.get("pix_fmt"), "color_range": s.get("color_range"),
                                  "color_space": s.get("color_space"), "color_transfer": s.get("color_transfer"),
                                  "color_primaries": s.get("color_primaries"),
                                  "container": f.get("format_name")}.items() if v and v != "unknown"}
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}


def range_warnings(measured: dict, file_name: str) -> list:
    """A note when a download is full-range (yuvj420p, or color_range pc), as QuickTime .mov files from the Archive
    often are: converting it as if it were limited range crushes the blacks and clips the whites."""
    pix, rng = str(measured.get("pix_fmt") or ""), str(measured.get("color_range") or "").lower()
    if not (pix.startswith("yuvj") or rng in ("pc", "jpeg", "full")):
        return []
    kind = "QuickTime " if "mov" in str(measured.get("container") or "") or file_name.lower().endswith(".mov") else ""
    matrix = measured.get("color_space") or "not tagged"
    return [f"full-range {kind}video ({pix or 'pix_fmt ?'}, color_range {rng or '?'}): convert it range-aware, e.g. "
            f"ffmpeg -i {file_name} -vf \"scale=in_range=pc:out_range=tv,format=yuv420p\" -color_range tv ... "
            f"(colour matrix: {matrix}; set in_color_matrix/out_color_matrix when it is not the one you deliver)"]


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


def _caps(opts: dict) -> dict:
    return {k: opts.get(k) for k in ("max_quality", "max_height") if opts.get(k)}


def _caps_text(opts: dict) -> str:
    return " and ".join(t for t in (f"--quality {opts['max_quality']}" if opts.get("max_quality") else "",
                                    f"--max-height {opts['max_height']}" if opts.get("max_height") else "") if t)


def download_candidates(rec: dict, opts: dict) -> list:
    """The files download tries, in order: [{url, route, quality, width, height, bytes}].

    A record with sizes (rec["variants"]: a Mixkit clip page's download options, Pexels and Pixabay files) gives
    each allowed size within --quality / --max-height, largest first, as its direct file and then (Mixkit) its
    download route; sizes known to be over --max-mb are left out. Any other record gives file_url, then its
    alternates (NASA ~large/~medium, the Mixkit size templates). A size that is unknown is not ruled out."""
    caps = _caps(opts)
    cap_bytes = int(opts["max_mb"] * 1048576) if opts.get("max_mb") else None
    fits = lambda c: size_fits(c.get("width"), c.get("height"), c.get("quality"), caps.get("max_quality"),  # noqa: E731
                               caps.get("max_height")) is not False
    vs = allowed_variants(rec)
    if vs:
        fit = [v for v in vs if fits(v)]
        if not fit:
            offered = ", ".join(f"{v.get('quality')}p" + (f" {v['width']}x{v['height']}" if v.get("width") else "")
                                for v in vs)
            raise FootageError(f"{rec['id']}: no file within {_caps_text(opts)}; it comes at {offered}")
        small = [v for v in fit if not (cap_bytes and v.get("bytes") and v["bytes"] > cap_bytes)]
        if not small:
            least = min(v["bytes"] for v in fit)
            raise FootageError(f"{rec['id']}: every size is over --max-mb {opts['max_mb']:g} "
                               f"(the smallest is {least / 1048576:.1f} MB)")
        out = []
        for v in small:
            base = {k: v.get(k) for k in ("quality", "width", "height", "bytes", "label")}
            if v.get("url"):
                out.append({**base, "url": v["url"], "route": False})
            if v.get("route"):
                out.append({**base, "url": v["route"], "route": True})
        return out
    mixkit = rec.get("source") == "mixkit"
    out = []
    for i, u in enumerate([rec["file_url"]] + list(rec.get("alternates") or [])):
        c = {"url": u, "route": is_mixkit_route(u), "quality": None, "width": None, "height": None, "bytes": None}
        if mixkit:
            c["quality"] = mixkit_quality(u)
            if c["quality"] and rec.get("width") and rec.get("height"):
                c["width"], c["height"] = _scale_to_short_side(rec["width"], rec["height"], c["quality"])
        elif i == 0:
            c.update(width=rec.get("width"), height=rec.get("height"), quality=rec.get("quality"),
                     bytes=rec.get("bytes"))
        out.append(c)
    if caps:
        fit = [c for c in out if fits(c)]
        if not fit:
            first = out[0]
            size = f"{first['width']}x{first['height']}" if first.get("width") else f"{first.get('quality')}p"
            raise FootageError(f"{rec['id']}: its file is {size}, over {_caps_text(opts)} "
                               f"({rec.get('source_name') or rec.get('source')} offers no smaller size here)")
        out = fit
    return out


def dry_run_pick(http: Http, cands: list, cap: int | None) -> dict | None:
    """The candidate download would end up with, without fetching it: a size the source lists is taken as is; any
    other is asked with HEAD (a missing size, 403/404/410, moves on to the next; so does one over --max-mb)."""
    for i, c in enumerate(cands):
        last = i + 1 == len(cands)
        if c.get("bytes"):
            if cap and c["bytes"] > cap and not last:
                continue
            return {**c, "size_from": "listed by the source"}
        u = c["url"]
        try:
            if c.get("route"):
                u = mixkit_follow_route(http, u)
            h = http.head(u)
        except ChallengeError:
            raise
        except HttpError as e:
            if e.status in (403, 404, 410) and not last:
                continue
            if e.status in (405, 501):  # HEAD not allowed: the size stays unknown
                return {**c, "url": u, "size_from": None}
            raise
        if cap and h["bytes"] and h["bytes"] > cap and not last:
            continue
        return {**c, "url": u, "bytes": h["bytes"], "size_from": "HEAD" if h["bytes"] else None}
    return None


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
    caps = _caps(opts)
    over_caps = caps and size_fits(rec.get("width"), rec.get("height"), rec.get("quality"), **caps) is False
    if rec["source"] == "archive" and ((cap and (rec.get("bytes") or 0) > cap) or over_caps):
        smaller = resolve_id(http, db, rec["id"], {**opts, "max_bytes": cap})  # the item's smaller derivative
        if (not cap or (smaller.get("bytes") or 0) <= cap) and \
                (not caps or size_fits(smaller.get("width"), smaller.get("height"), None, **caps) is not False):
            smaller["query"] = rec.get("query")
            rec = smaller
    if rec["source"] == "nasa" and "alternates" not in rec and not opts.get("dry_run"):
        try:  # a results file from before alternates were recorded: fetch the variant list once
            rec = {**resolve_id(http, db, rec["id"], opts), "query": rec.get("query")}
        except FootageError:
            pass
    rec = confirm_licence(http, db, rec, files=True)  # Mixkit: licence, sizes and the download route from the page
    if rec["source"] == "mixkit":
        mixkit_apply_files(rec)  # also for a results file written before Free clips were fetched above 720p
    lic = rec["licence"]
    if lic.get("derivatives") is False and not opts.get("allow_nd"):
        raise FootageError(f"{rec['id']}: {lic.get('name')} forbids edits (ND); a montage is an edit. "
                           "Pass --allow-nd only to keep it unedited as reference")
    if opts.get("commercial") and lic.get("commercial") is not True:
        why = "suspicious uploader licence on what looks like someone else's work" \
            if "suspicious-licence" in rec.get("flags", []) else "does not allow (or does not confirm) commercial use"
        raise FootageError(f"{rec['id']}: {lic.get('name')} {why}")
    out.mkdir(parents=True, exist_ok=True)
    dest = out / safe_name(rec)
    cands = download_candidates(rec, opts)
    # the size this clip is expected at: the largest listed one within --quality/--max-height (not --max-mb, so a
    # budget fallback is flagged smaller-variant), else the first candidate's; a Mixkit Free clip without listed
    # sizes is expected at 1080p (its 2160p file may not exist)
    within = [v["quality"] for v in allowed_variants(rec) if v.get("quality") and
              size_fits(v.get("width"), v.get("height"), v.get("quality"), **caps) is not False]
    qs = [c["quality"] for c in cands if c.get("quality")]
    top = within[0] if within else (qs[0] if qs else None)
    expected = min([q for q in (rec.get("quality"), top) if q] or [0]) or None
    note = "" if not caps or any(c.get("quality") or c.get("height") for c in cands) else \
        f"{_caps_text(opts)} not checked: {rec.get('source_name') or rec['source']} does not list this file's size"
    if opts.get("dry_run"):
        pick = dry_run_pick(http, cands, cap) or {**cands[0], "size_from": None}
        q = pick.get("quality") or (mixkit_quality(pick["url"]) if rec["source"] == "mixkit" else None) or \
            (min(pick["width"], pick["height"]) if pick.get("width") and pick.get("height") else None)
        return {"id": rec["id"], "file": dest.name, "dry_run": True, "file_url": redact(pick["url"]),
                "licence": lic.get("name"), "attribution": rec["attribution"],
                "quality": q, "width": pick.get("width"), "height": pick.get("height"), "bytes": pick.get("bytes"),
                "size_from": pick.get("size_from"), "over_max_mb": bool(cap and pick.get("bytes") and pick["bytes"] > cap),
                "candidates": len(cands), **({"note": note} if note else {})}
    info = {}
    if dest.exists() and not opts.get("force"):
        data = dest.read_bytes()
        info = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "content_type": None, "reused": True}
    else:
        for i, c in enumerate(cands):
            u = c["url"]
            try:
                if c.get("route"):
                    u = mixkit_follow_route(http, u)  # the hashed file a newer clip's download option names
                info = fetch_file(http, u, dest, opts.get("max_mb", 300))
            except ChallengeError:
                raise  # never worked around; the message says to retry later
            except FootageError as e:
                missing = isinstance(e, HttpError) and e.status in (403, 404, 410)
                if i + 1 < len(cands) and ("--max-mb" in str(e) or missing or
                                           (c.get("route") and "names no file" in str(e))):
                    # over the cap, or this size does not exist: try the next file (this size's download route,
                    # or the next smaller size: NASA ~large, ~medium; a Mixkit Free clip without -2160 has -1080)
                    continue
                if rec["source"] == "mixkit" and missing and not rec.get("variants"):
                    err = (rec.get("native") or {}).get("page_error")
                    raise FootageError(
                        f"{e}; newer Mixkit clips have no <id>-<size>.mp4 file and are fetched through the clip "
                        "page's download options, " + (f"but the clip page could not be read ({err})" if err else
                                                      "which this clip page did not list")) from None
                raise
            q = c.get("quality") or (mixkit_quality(u) if rec["source"] == "mixkit" else None)
            if rec["source"] == "mixkit" or rec.get("variants"):
                if q and expected and q < expected:
                    rec["flags"] = sorted(set(rec.get("flags", [])) | {"smaller-variant"})
                if c.get("width") and c.get("height"):
                    rec["width"], rec["height"] = c["width"], c["height"]
                elif q and rec.get("width") and rec.get("height") and rec.get("quality") and q != rec["quality"]:
                    rec["width"], rec["height"] = _scale_to_short_side(rec["width"], rec["height"], q)
                rec["file_url"], rec["quality"] = u, q or rec.get("quality")
                if c.get("route"):
                    rec.setdefault("native", {})["download_route"] = c["url"]
            elif u != rec["file_url"]:
                rec["flags"] = sorted(set(rec.get("flags", [])) | {"smaller-variant"})
                rec["file_url"], rec["width"], rec["height"] = u, None, None
            break
    measured = measure(dest)
    warnings = range_warnings(measured, dest.name)
    if warnings:
        rec["flags"] = sorted(set(rec.get("flags", [])) | {"full-range"})
    sidecar = {
        "schema": ASSET_SCHEMA,
        "file": dest.name,
        "downloaded_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bytes": info["bytes"],
        "sha256": info["sha256"],
        "result": _redact_all(rec),
        "licence": lic,
        "attribution": rec["attribution"],
        "measured": measured,
        **({"warnings": warnings} if warnings else {}),
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
            "attribution": rec["attribution"], "reused": bool(info.get("reused")),
            "quality": rec.get("quality"), "width": measured.get("width") or rec.get("width"),
            "height": measured.get("height") or rec.get("height"),
            **({"warnings": warnings} if warnings else {}), **({"note": note} if note else {})}


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
             f"Generated by `{SCRIPT_FROM_ROOT}` from the `*.json` sidecars in this folder "
             f"(after removing a clip, run `python3 {SCRIPT_FROM_ROOT} credits <this folder>`{SCRIPT_FROM_WHERE}).", "",
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


# ------------------------------------------------------------------------------------------------- preview

CELL_W, CELL_H = 320, 180


def image_ext(head: bytes) -> str | None:
    """.jpg/.png/.gif/.webp from an image's first bytes, else None (a web page, an error, anything else)."""
    if head[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if head[:4] == b"GIF8":
        return ".gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return ".webp"
    return None


def preview_items(src: Path, ids=None, query=None, limit: int = 40) -> list:
    """[(record, local media file or None)] from a results file, or from a folder of downloads and their sidecars."""
    items = []
    if src.is_dir():
        for p in sorted(src.glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(d, dict) or d.get("schema") != ASSET_SCHEMA:
                continue
            media = p.with_name(p.name[: -len(".json")])
            rec = dict(d.get("result") or {})
            rec.setdefault("id", d.get("file"))
            rec.setdefault("licence", d.get("licence") or {})
            items.append((rec, media if media.is_file() else None))
    else:
        data = load_results(src)
        if data is None:
            raise FootageError(f"{src} is neither a free_footage results file nor a folder of downloads")
        items = [(r, None) for r in data.get("results", []) if isinstance(r, dict)]
    if ids:
        wanted = set(ids)
        items = [it for it in items if it[0].get("id") in wanted]
    if query:
        items = [it for it in items if _norm_query(it[0].get("query")) == _norm_query(query)]
    return items[: max(1, limit)]


def _ffmpeg(args: list, timeout: int = 120) -> bool:
    try:
        return subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], capture_output=True,
                              timeout=timeout).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _fit(w: int, h: int) -> str:
    return f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black"


ONE_IMAGE = ["-frames:v", "1", "-update", "1"]  # write a single image, not an image sequence


def video_frames(video: Path, dest: Path, frames: int = 1) -> bool:
    """A still a third of the way in (frames=1), or a strip of `frames` evenly spaced stills, as a JPEG."""
    dur = measure(video).get("duration") or 0
    if frames <= 1:
        return _ffmpeg(["-ss", f"{dur / 3:.2f}", "-i", str(video), *ONE_IMAGE, "-vf", _fit(CELL_W, CELL_H), str(dest)])
    rate = frames / dur if dur else 1.0
    return _ffmpeg(["-i", str(video), "-vf", f"fps={rate:.6f},{_fit(CELL_W, CELL_H)},format=yuvj420p,"
                    f"tile={frames}x1", *ONE_IMAGE, str(dest)])


def fetch_image(http: Http, url: str, stem: Path) -> Path:
    body = http.get_bytes(url, {"Accept": "image/*"}, cap_mb=THUMB_CAP_MB)
    ext = image_ext(body[:16])
    if not ext:
        raise FootageError(f"{redact(url)} did not answer with an image")
    path = stem.with_name(stem.name + ext)
    path.write_bytes(body)
    return path


def contact_sheet_jpg(rows: list, out: Path, frames: int, cols: int) -> Path | None:
    """One JPEG of every cell (numbered like the HTML page), drawn by ffmpeg; None when ffmpeg failed."""
    w, h = CELL_W * max(1, frames), CELL_H
    cells = out / "cells"
    cells.mkdir(exist_ok=True)
    try:
        for i, row in enumerate(rows, 1):
            dest = cells / f"{i:04d}.jpg"
            src = ["-i", str(out / row["image"])] if row.get("image") else ["-f", "lavfi", "-i", f"color=c=black:s={w}x{h}"]
            label = f",drawtext=text='{row['n']}':x=8:y=8:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.6"
            # one pixel format for every cell: thumbnails come as yuvj420p and yuvj422p, and a format change in
            # the middle of the sequence makes ffmpeg rebuild the filter graph, so tile would start over
            # (seen live: a 6-cell sheet showed only cells 5 and 6)
            same = ",format=yuvj420p"
            if not (_ffmpeg([*src, *ONE_IMAGE, "-vf", _fit(w, h) + label + same, str(dest)]) or
                    _ffmpeg([*src, *ONE_IMAGE, "-vf", _fit(w, h) + same, str(dest)])):  # no fonts: no numbers
                return None
        c = max(1, cols if frames <= 1 else 1)
        sheet = out / "contact_sheet.jpg"
        ok = _ffmpeg(["-framerate", "1", "-i", str(cells / "%04d.jpg"), "-vf",
                      f"format=yuvj420p,tile={c}x{math.ceil(len(rows) / c)}:padding=4:margin=4", *ONE_IMAGE, str(sheet)])
        return sheet if ok else None
    finally:
        shutil.rmtree(cells, ignore_errors=True)


def build_preview(http: Http, items: list, out: Path, frames: int = 1, cols: int = 4) -> dict:
    """A contact sheet of the items: each one's thumbnail, else a still (or a strip of `frames` stills) from its
    small preview video or from the local clip. Writes contact_sheet.html (always), contact_sheet.jpg (with ffmpeg)
    and contact_sheet.json. Never fetches a full clip: previews are capped at PREVIEW_CAP_MB and deleted after use."""
    out.mkdir(parents=True, exist_ok=True)
    thumbs = out / "thumbs"
    thumbs.mkdir(exist_ok=True)
    have_ff = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
    rows = []
    for n, (rec, media) in enumerate(items, 1):
        stem = thumbs / f"{n:03d}-{re.sub(r'[^A-Za-z0-9._-]+', '_', str(rec.get('id') or n))[:60]}"
        lic = rec.get("licence") or {}
        row = {"n": n, "id": rec.get("id"), "title": rec.get("title"), "page_url": rec.get("page_url"),
               "size": _size_text(rec), "duration": rec.get("duration"), "licence": lic.get("name"),
               "commercial": lic.get("commercial"), "flags": rec.get("flags") or [], "relevance": rec.get("relevance"),
               "image": None, "from": None, "errors": []}
        order = []
        if media is not None and have_ff:
            order.append("local")
        tries = ["preview", "thumb"] if frames > 1 else ["thumb", "preview"]
        order += [t for t in tries if (t == "thumb" and rec.get("thumb_url")) or
                  (t == "preview" and rec.get("preview_url") and have_ff)]
        for how in order:
            try:
                if how == "local":
                    img = stem.with_name(stem.name + ".jpg")
                    if not video_frames(media, img, frames):
                        raise FootageError("ffmpeg could not read the local clip")
                elif how == "thumb":
                    img = fetch_image(http, rec["thumb_url"], stem)
                else:
                    tmp = stem.with_name(stem.name + ".preview.mp4")
                    try:
                        fetch_file(http, rec["preview_url"], tmp, PREVIEW_CAP_MB)
                        img = stem.with_name(stem.name + ".jpg")
                        if not video_frames(tmp, img, frames):
                            raise FootageError("ffmpeg could not read the preview file")
                    finally:
                        if tmp.exists():
                            tmp.unlink()
            except FootageError as e:
                row["errors"].append(f"{how}: {redact(e)}"[:240])
                continue
            row.update(image=img.relative_to(out).as_posix(), **{"from": {"local": "the downloaded clip",
                                                                         "thumb": "thumbnail",
                                                                         "preview": "preview video"}[how]})
            break
        if not order:
            row["errors"].append("no thumbnail or preview link" + ("" if have_ff else " usable without ffmpeg"))
        rows.append(row)
    html_path = out / "contact_sheet.html"
    html_path.write_text(contact_sheet_html(rows, frames), encoding="utf-8")
    jpg = contact_sheet_jpg(rows, out, frames, cols) if have_ff and rows else None
    summary = {"schema": "kosif.free_footage.preview.v1",
               "made_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "frames": frames, "html": html_path.name, "jpg": jpg.name if jpg else None, "items": rows}
    (out / "contact_sheet.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return summary


def contact_sheet_html(rows: list, frames: int) -> str:
    e = lambda s: _html.escape(str(s if s is not None else ""), quote=True)  # noqa: E731
    com = {True: "commercial ok", False: "NON-commercial", None: "commercial ?"}
    cards = []
    for r in rows:
        img = f'<img src="{e(r["image"])}" alt="{e(r["title"])}" loading="lazy">' if r.get("image") else \
            '<div class="none">no picture</div>'
        flags = " ".join(f'<span class="flag">{e(f)}</span>' for f in r.get("flags") or [])
        dur = f"{r['duration']:.0f}s" if isinstance(r.get("duration"), (int, float)) else "?"
        link = f'<a href="{e(r["page_url"])}">page</a>' if str(r.get("page_url") or "").startswith("https://") else ""
        cards.append(f'<figure class="card"><div class="n">{r["n"]}</div>{img}<figcaption><b>{e(r["id"])}</b> '
                     f'{link}<br>{e(r["title"])}<br>{e(r["size"])} · {e(dur)} · {e(r["licence"])} · '
                     f'{e(com.get(r.get("commercial"), "commercial ?"))}<br>{flags}'
                     + (f'<br><small>{e("; ".join(r["errors"]))}</small>' if r.get("errors") and not r.get("image") else "")
                     + "</figcaption></figure>")
    width = CELL_W * max(1, frames)
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Footage contact sheet</title>"
            "<style>body{font:14px/1.4 system-ui,sans-serif;margin:16px;background:#111;color:#eee}"
            f".grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax({min(width, 960)}px,1fr));gap:12px}}"
            ".card{margin:0;background:#1d1d1d;border-radius:6px;overflow:hidden;position:relative}"
            ".card img{width:100%;display:block}.none{aspect-ratio:16/9;display:grid;place-items:center;color:#888}"
            ".n{position:absolute;left:6px;top:6px;background:#000a;padding:0 6px;border-radius:4px}"
            "figcaption{padding:8px}a{color:#8cf}.flag{background:#333;border-radius:3px;padding:0 4px;margin-right:4px;"
            "font-size:12px}small{color:#f99}</style></head><body>"
            "<h1>Footage contact sheet</h1><p>Screen each clip for people, faces and text before downloading it. "
            "Licences are what each source declares; read the clip page before publishing.</p>"
            f"<div class=\"grid\">{''.join(cards)}</div></body></html>\n")


# ------------------------------------------------------------------------------------------------- probe

def site_of(url: str) -> str:
    """The registrable part of a URL's host, roughly: the last two labels (www.videvo.net -> videvo.net)."""
    host = (urllib.parse.urlsplit(url or "").hostname or "").lower()
    return ".".join(host.split(".")[-2:])


def probe_source(http: Http, src: dict) -> dict:
    rows = []
    for p in src.get("probes") or []:
        t0 = time.monotonic()
        row = {"what": p["what"], "url": p["url"]}
        final = p["url"]
        try:
            resp = http.open(p["url"], {"Range": "bytes=0-65535"} if p["url"].lower().endswith(VIDEO_EXT) else None)
            status = getattr(resp, "status", None) or 200
            ctype = resp.headers.get("Content-Type") if getattr(resp, "headers", None) else None
            final = _final_url(resp, p["url"])
            _close(resp)
            row.update(http=status, content_type=ctype)
        except HttpError as e:
            final = e.final_url
            row.update(http=e.status if isinstance(e.status, int) else None, error=None if isinstance(e.status, int) else str(e))
            if isinstance(e, ChallengeError):
                row.update(challenge=True, error=str(e))
        if final != p["url"]:
            row["final_url"] = redact(final)  # urllib follows redirects silently; keep where it landed
        row["ms"] = int((time.monotonic() - t0) * 1000)
        code = row.get("http")
        if row.get("challenge"):
            row["verdict"] = "blocked"  # a Cloudflare browser check: reachable by a person, not by this script now
        elif site_of(final) != site_of(p["url"]):
            row["verdict"] = "moved"  # the site now answers from another domain (videvo.net -> freepik.com)
        elif isinstance(code, int) and code < 400:
            row["verdict"] = "ok"
        elif isinstance(code, int) and code == p.get("expect"):
            row["verdict"] = "expected"
        elif isinstance(code, int):
            row["verdict"] = "blocked"
        else:
            row["verdict"] = "timeout" if re.search(r"time[sd]?\s?out", str(row.get("error", "")), re.I) else "error"
        rows.append(row)
    verdicts = [r["verdict"] for r in rows]
    if "moved" in verdicts:
        status = "moved"  # whatever the new domain answers, this record describes a site that is gone
    elif verdicts and all(v == "ok" for v in verdicts):
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


def is_paid(src: dict) -> bool:
    return src.get("category") == "paid-stock" or (src.get("reachability") or {}).get("status") == "paid"


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
    if (args.no_attribution or args.commercial) and not args.include_paid:
        rows = [s for s in rows if not is_paid(s)]  # a paid plan's licence is not free footage
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
    return Http(delay=args.delay, timeout=args.timeout,
                max_retry_after=getattr(args, "wait_429", None) if getattr(args, "wait_429", None) is not None
                else MAX_RETRY_AFTER, challenge_wait=getattr(args, "retry_challenge", 0) or 0)


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
    query = " ".join(args.query)
    opts = {"min_height": args.min_height, "orientation": args.orientation, "commercial": args.commercial,
            "allow_nd": args.allow_nd, "any_licence": args.any_licence, "no_ai": args.no_ai,
            "max_bytes": int(args.max_mb * 1048576) if args.max_mb else None, "details": args.details,
            "resolve": args.resolve, "match": args.match, "no_people": args.no_people}
    path = Path(args.save)
    cached = {}
    if args.retry_failed:
        done = answered_sources(load_results(path), query)
        cached = {n: done[n] for n in names if n in done}
        names = [n for n in names if n not in cached]
    report = run_search(make_http(args), db, query, names, max(1, min(args.limit, 50)), opts)
    for n, (st, when) in cached.items():
        report["sources"][n] = {"status": "cached", "count": st.get("count", 0), "found": st.get("found", 0),
                                "detail": f"answered at {when}; its results stay in the file (--retry-failed)"}
    data = None
    if not args.no_save:
        data = save_results(path, report, replace=args.replace)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        if args.retry_failed and cached and not names:
            print("# --retry-failed: every source answered the last time this query was saved; nothing was asked again")
        print_results(report)
        if data is not None:
            older = len(data["results"]) - len(report["results"])
            print(f"# saved {len(report['results'])} results to {args.save}"
                  + (f" (with {older} from earlier searches: {len(data.get('searches') or [])} searches in the file)"
                     if older > 0 else "")
                  + "; download with: free_footage.py download <id> --out <dir>; screen first with: "
                  f"free_footage.py preview {args.save}")
    statuses = [v["status"] for v in report["sources"].values()]
    return 3 if statuses and all(s == "error" for s in statuses) else 0


def _dry_text(r: dict) -> str:
    q = f"{r['quality']}p" if r.get("quality") else "?p"
    dims = f" {r['width']}x{r['height']}" if r.get("width") and r.get("height") else ""
    mb = f"{r['bytes'] / 1048576:.1f} MB" if r.get("bytes") else "size unknown"
    src = f" ({r['size_from']})" if r.get("size_from") else ""
    return f"dry run: {q}{dims}, {mb}{src}" + (" OVER --max-mb" if r.get("over_max_mb") else "")


def cmd_download(args, db) -> int:
    http = make_http(args)
    opts = {"results": Path(args.results), "max_mb": args.max_mb, "licence": args.licence,
            "licence_url": args.licence_url, "author": args.author, "title": args.title, "page_url": args.page_url,
            "allow_nd": args.allow_nd, "commercial": args.commercial, "dry_run": args.dry_run, "force": args.force,
            "max_bytes": int(args.max_mb * 1048576) if args.max_mb else None,
            "max_quality": args.quality, "max_height": args.max_height}
    out, failed, done, challenged = Path(args.out), 0, [], 0
    for t in args.targets:
        try:
            r = download_one(http, db, t, out, opts)
            done.append(r)
            note = _dry_text(r) if r.get("dry_run") else (
                f"{r['bytes'] / 1048576:.1f} MB" + (f" {r['quality']}p" if r.get("quality") else "")
                + (" (kept)" if r.get("reused") else ""))
            print(f"{r['id']}\t{r['file']}\t{note}\t{r['licence']}")
            for w in r.get("warnings") or []:
                print(f"# warning: {r['file']}: {w}")
            if r.get("note"):
                print(f"# note: {r['id']}: {r['note']}")
        except ChallengeError as e:
            failed += 1
            challenged += 1
            print(f"{t}\tFAILED\t{redact(e)}", file=sys.stderr)
        except FootageError as e:
            failed += 1
            print(f"{t}\tFAILED\t{redact(e)}", file=sys.stderr)
        except (OSError, HTTPException) as e:  # backstop: one target's network or disk failure; the batch goes on
            failed += 1
            print(f"{t}\tFAILED\t{type(e).__name__}: {redact(str(e))[:200]}", file=sys.stderr)
    if args.json:
        print(json.dumps(done, ensure_ascii=False, indent=1))
    if done and not args.dry_run:
        print(f"# credits: {out / 'ATTRIBUTION.md'}")
    if challenged:
        print(f"# {challenged} target(s) not fetched: {', '.join(sorted(http.challenged))} answered with a Cloudflare "
              "browser check. Run the same command again in a few minutes (files already saved are kept), or add "
              "--retry-challenge 180 to wait once.", file=sys.stderr)
    return 1 if failed else 0


def cmd_preview(args, db) -> int:
    src = Path(args.source)
    ids = [x.strip() for x in (args.ids or "").split(",") if x.strip()]
    items = preview_items(src, ids or None, args.query, args.limit)
    if not items:
        raise FootageError(f"nothing to preview in {src}" + (" for those ids" if ids else ""))
    out = Path(args.out) if args.out else (src if src.is_dir() else src.parent) / "preview"
    summary = build_preview(make_http(args), items, out, max(1, min(args.frames, 12)), max(1, min(args.cols, 8)))
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return 0
    for r in summary["items"]:
        how = r["from"] or ("FAILED: " + "; ".join(r["errors"]))[:160]
        print(f"{r['n']:3}  {r['id']}\t{r['size']}\t{how}\t{(r.get('title') or '')[:60]}")
    print(f"# contact sheet: {out / summary['html']}" + (f" and {out / summary['jpg']}" if summary["jpg"] else
                                                         " (install ffmpeg for a JPG sheet and video stills)"))
    return 0 if any(r["image"] for r in summary["items"]) else 1


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

    def bounded(maximum):
        def conv(text):
            try:
                v = float(text)
            except ValueError:
                raise argparse.ArgumentTypeError(f"{text!r} is not a number of seconds") from None
            if not 0 <= v <= maximum:
                raise argparse.ArgumentTypeError(f"must be between 0 and {maximum:g} seconds")
            return v
        return conv

    def net(p):
        p.add_argument("--delay", type=float, default=1.0, help="seconds between requests to one host (default 1.0)")
        p.add_argument("--timeout", type=float, default=20.0, help="seconds per request (default 20)")
        p.add_argument("--wait-429", type=bounded(MAX_WAIT_429), default=None, metavar="SECONDS",
                       help=f"wait once for a 429/503 whose Retry-After is up to this long (default "
                            f"{MAX_RETRY_AFTER:g}, at most {MAX_WAIT_429:g}); longer waits fail with the Retry-After")
        p.add_argument("--retry-challenge", type=bounded(MAX_CHALLENGE_WAIT), default=0, metavar="SECONDS",
                       help="when a site answers with a Cloudflare 'Just a moment...' check, wait this long once and "
                            f"ask again (default 0: report it and stop asking that site; at most {MAX_CHALLENGE_WAIT:g})")

    p = sub.add_parser("sources", help="list or filter the sources database (offline)")
    p.add_argument("--id", help="show one source in full")
    p.add_argument("--find", help="keep sources whose record mentions this word")
    p.add_argument("--status", choices=ENUMS["reachability.status"], help="recorded reachability")
    p.add_argument("--searchable", action="store_true", help="only sources this tool can search")
    p.add_argument("--no-attribution", action="store_true", help="only sources that do not require credit")
    p.add_argument("--commercial", action="store_true", help="only sources whose licence allows commercial use")
    p.add_argument("--include-paid", action="store_true",
                   help="keep paid-stock sources (Storyblocks) in --commercial and --no-attribution lists")
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
    p.add_argument("--commercial", action="store_true",
                   help="drop NC, Mixkit Restricted, suspicious and unconfirmed licences; reads each Mixkit clip page "
                        "to tell Free from Restricted (one request per clip, as --resolve)")
    p.add_argument("--resolve", action="store_true",
                   help="read each Mixkit clip page (licence, real sizes and file sizes, thumbnail) and NASA "
                        "metadata.json for the results kept; one request per clip")
    p.add_argument("--match", choices=("any", "all"),
                   help="drop results whose title shares no query word (any) or misses one (all); sites match loosely")
    p.add_argument("--no-people", action="store_true",
                   help="drop results whose title names people (woman, man, couple, portrait, hands ...): a title "
                        "heuristic, so screen the contact sheet too (preview)")
    p.add_argument("--allow-nd", action="store_true", help="keep no-derivatives licences (reference only)")
    p.add_argument("--any-licence", action="store_true", help="keep Archive items with no licence (rights unknown)")
    p.add_argument("--no-ai", action="store_true", help="drop clips flagged as AI-generated")
    p.add_argument("--details", action="store_true", help="NASA: also read each clip's size (one request more)")
    p.add_argument("--max-mb", type=float, default=300, help="Archive: prefer a file under this size (default 300)")
    p.add_argument("--save", default=str(DEFAULT_RESULTS),
                   help="results file; new results are merged into it by id, so earlier ids keep working "
                        "(default out/free-footage/last_search.json)")
    p.add_argument("--replace", action="store_true", help="overwrite the results file instead of merging")
    p.add_argument("--retry-failed", action="store_true",
                   help="ask only the sources that did not answer the last time this query was saved (a 429, a "
                        "timeout); the others' saved results are kept")
    p.add_argument("--no-save", action="store_true")
    p.add_argument("--json", action="store_true")
    net(p)
    p = sub.add_parser("download", help="download result ids or URLs with a licence sidecar and ATTRIBUTION.md (network)")
    p.add_argument("targets", nargs="+", help="result ids (wikimedia:81916645) or page/file URLs")
    p.add_argument("--out", required=True, help="folder for the clips, sidecars and ATTRIBUTION.md")
    p.add_argument("--results", default=str(DEFAULT_RESULTS), help="results file from search")
    p.add_argument("--max-mb", type=float, default=300,
                   help="refuse files larger than this (default 300; 0 = no cap); takes the next smaller size instead "
                        "where the source has one (Mixkit, Archive, NASA, Pexels, Pixabay)")
    p.add_argument("--quality", type=int, metavar="P",
                   help="largest size to fetch, as the short side (1080 = 1080p, also for a vertical clip), where "
                        "the source lists sizes (Mixkit, Archive, Pexels, Pixabay)")
    p.add_argument("--max-height", type=int, metavar="PX", help="largest frame height to fetch, where sizes are known")
    p.add_argument("--licence", help="licence name for a link from an unsupported site (from its page)")
    p.add_argument("--licence-url", help="licence URL for a link from an unsupported site")
    p.add_argument("--author")
    p.add_argument("--title")
    p.add_argument("--page-url")
    p.add_argument("--allow-nd", action="store_true", help="allow a no-derivatives licence (keep the clip unedited)")
    p.add_argument("--commercial", action="store_true", help="refuse clips whose licence does not confirm commercial use")
    p.add_argument("--dry-run", action="store_true",
                   help="resolve and print the size, resolution and file size it would fetch (a HEAD request when "
                        "the source does not list the size); write nothing")
    p.add_argument("--force", action="store_true", help="download again even when the file exists")
    p.add_argument("--json", action="store_true")
    net(p)
    p = sub.add_parser("preview", help="contact sheet from thumbnails or small previews, before downloading (network)")
    p.add_argument("source", help="a results file from search, or a folder of downloads (their sidecars)")
    p.add_argument("--out", help="folder for contact_sheet.html/.jpg/.json (default: <results folder>/preview)")
    p.add_argument("--frames", type=int, default=1,
                   help="stills per clip: 1 = the thumbnail; 2-12 = a strip from the small preview file (needs ffmpeg)")
    p.add_argument("--cols", type=int, default=4, help="columns in the JPG sheet (default 4)")
    p.add_argument("--limit", type=int, default=40, help="at most this many clips (default 40)")
    p.add_argument("--ids", help="comma-separated result ids to show (default: all)")
    p.add_argument("--query", help="only the results found by this query (in a merged results file)")
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
                "download": cmd_download, "preview": cmd_preview, "credits": cmd_credits}[args.cmd](args, db)
    except FootageError as e:
        print(f"error: {redact(e)}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    sys.exit(main())
