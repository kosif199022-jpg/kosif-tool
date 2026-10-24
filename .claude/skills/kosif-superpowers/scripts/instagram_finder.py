#!/usr/bin/env python3
"""Find and download Instagram videos for a product — البحث عن فيديوهات إنستجرام لمنتج وتحميلها.

Instagram has no keyword search for other people's posts that a script may use without
logging in, so this tool builds a *local, searchable index* of the owner's saved source
accounts (and optional hashtags or single post links), then ranks the indexed videos
against a product query in Arabic or English. Downloads go through the existing
built-in downloader scripts/fetch_video.py (yt-dlp).

  python3 instagram_finder.py accounts                       # saved source accounts
  python3 instagram_finder.py add-account "https://www.instagram.com/name?igsh=..."
  python3 instagram_finder.py plan "عطر رجالي"               # keywords, hashtags, web searches (offline)
  python3 instagram_finder.py index --session-user ME        # read captions of saved accounts (instaloader)
  python3 instagram_finder.py index --browser chrome         # same, with your local browser login
  python3 instagram_finder.py get "https://www.instagram.com/reel/..."  # download a link you have, one step
  python3 instagram_finder.py add-posts URL [URL ...]        # index single reels you found (yt-dlp)
  python3 instagram_finder.py search "perfume splash" --top 15 --save out/instagram/hits.json
  python3 instagram_finder.py thumbs out/instagram/hits.json # thumbnails to check visually first
  python3 instagram_finder.py download out/instagram/hits.json --pick 1,3 --rights permission

Only the standard library is imported at start; instaloader and yt-dlp are optional and
used only by the commands that need them. Respect Instagram's terms: keep the default
rate limits, use your own session, and download only what you own, have permission for,
or keep as private reference.
"""
from __future__ import annotations

import argparse
import atexit
import datetime as dt
import json
import math
import os
import re
import subprocess
import tempfile
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "instagram_sources.json"
SYNONYMS = ROOT / "data" / "instagram_synonyms.json"
FETCHER = ROOT / "scripts" / "fetch_video.py"
DEFAULT_INDEX = Path("out") / "instagram" / "index.json"
RIGHTS = ("owned", "permission", "licensed", "reference-only")
HANDLE_RE = re.compile(r"^[A-Za-z0-9._]{1,30}$")
RESERVED = {"p", "reel", "reels", "tv", "explore", "stories", "accounts", "direct", "about", "legal"}
POST_RE = re.compile(r"^/(?:[A-Za-z0-9._]+/)?(p|reel|reels|tv)/([A-Za-z0-9_-]{5,})/?")
SESSION_ENV = "INSTAGRAM_SESSIONID"  # optional: the sessionid cookie of the user's own (ideally secondary) account
MAX_PER_ACCOUNT = 200   # hard cap per account per run (rate limits)
MAX_DOWNLOADS = 25      # hard cap per download run unless --max is raised (≤ 100)

# ---------------------------------------------------------------- text helpers
_TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_AR_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"})
_AR_PREFIXES = ("وال", "بال", "فال", "كال", "لل", "ال")


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").casefold()
    return _TASHKEEL.sub("", s).translate(_AR_MAP)


def stem(tok: str) -> str:
    for p in _AR_PREFIXES:
        if tok.startswith(p) and len(tok) - len(p) >= 3:
            return tok[len(p):]
    if tok.isascii() and len(tok) > 4 and tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok


def tokens(s: str) -> list[str]:
    return [stem(t) for t in re.findall(r"\w+", norm_text(s)) if len(t) > 1 or not t.isascii()]


def load_synonyms(path: Path = SYNONYMS) -> dict[str, set[str]]:
    try:
        groups = json.loads(path.read_text(encoding="utf-8"))["groups"]
    except (OSError, ValueError, KeyError):
        return {}
    table: dict[str, set[str]] = {}
    for g in groups:
        normed = {t for w in g for t in tokens(w)}
        for t in normed:
            table.setdefault(t, set()).update(normed)
    return table


def expand_query(query: str, syn: dict[str, set[str]] | None = None) -> list[dict]:
    """One group per query word: the word plus its synonyms (normalised)."""
    syn = load_synonyms() if syn is None else syn
    out, seen = [], set()
    for t in tokens(query):
        if t in seen:
            continue
        seen.add(t)
        out.append({"word": t, "terms": sorted({t} | syn.get(t, set()))})
    return out


def hashtag_ideas(query: str, syn=None) -> list[str]:
    groups = expand_query(query, syn)
    words = [g["word"] for g in groups]
    tags = []
    if len(words) > 1:
        tags.append("".join(words))
    for g in groups:
        tags += g["terms"]
    base = [w for w in words if w.isascii()]
    for w in base:
        tags += [w + suffix for suffix in ("photography", "video", "reels", "commercial")]
    seen, ordered = set(), []
    for t in tags:
        t = re.sub(r"\W", "", t)
        if t and t not in seen:
            seen.add(t)
            ordered.append(t)
    return ordered[:25]


# ---------------------------------------------------------------- accounts
def normalize_account(raw: str) -> dict:
    """Return {handle, url} from a profile URL or @handle; drops every query string and fragment."""
    raw = (raw or "").strip()
    if raw.startswith("@") or HANDLE_RE.match(raw):
        handle = raw.lstrip("@")
    else:
        parts = urllib.parse.urlsplit(raw if "://" in raw else "https://" + raw)
        host = (parts.hostname or "").lower()
        if host not in ("instagram.com", "www.instagram.com", "m.instagram.com"):
            raise ValueError(f"not an instagram.com profile link: {raw!r}")
        segs = [s for s in parts.path.split("/") if s]
        if not segs:
            raise ValueError(f"no account name in link: {raw!r}")
        handle = segs[0]
    if not HANDLE_RE.match(handle) or handle.lower() in RESERVED:
        raise ValueError(f"not a valid Instagram account name: {handle!r}")
    handle = handle.lower()
    return {"handle": handle, "url": f"https://www.instagram.com/{handle}/"}


def clean_post_url(raw: str) -> str | None:
    parts = urllib.parse.urlsplit((raw or "").strip())
    if (parts.hostname or "").lower() not in ("instagram.com", "www.instagram.com", "m.instagram.com"):
        return None
    m = POST_RE.match(parts.path)
    if not m:
        return None
    kind = "reel" if m.group(1) in ("reel", "reels") else m.group(1)
    return f"https://www.instagram.com/{kind}/{m.group(2)}/"


def load_sources(path: Path = SOURCES) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_sources(obj: dict, path: Path = SOURCES) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- index
def load_index(path: Path) -> dict:
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            pass
    return {"schema": "kosif.instagram_index.v1", "posts": {}}


def save_index(idx: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    idx["updated_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    path.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")


def post_record(**kw) -> dict:
    rec = {"shortcode": kw["shortcode"], "url": kw.get("url") or f"https://www.instagram.com/p/{kw['shortcode']}/",
           "account": (kw.get("account") or "").lower(), "is_video": bool(kw.get("is_video")),
           "caption": kw.get("caption") or "", "hashtags": [h.lower() for h in (kw.get("hashtags") or [])],
           "alt": kw.get("alt") or "", "date": kw.get("date"), "views": kw.get("views"), "likes": kw.get("likes"),
           "duration": kw.get("duration"), "thumbnail": kw.get("thumbnail"), "source": kw.get("source")}
    if not rec["hashtags"]:
        rec["hashtags"] = [h.lower() for h in re.findall(r"#(\w+)", rec["caption"])]
    return rec


def instaloader_posts(handle: str, limit: int, session_user: str | None, hashtag: bool = False,
                      browser: str | None = None):
    """Yield post records newest first. Imported lazily (pip install instaloader)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from _deps import ensure  # noqa: PLC0415
        ensure(["instaloader"])
    except Exception:  # noqa: BLE001 — best effort; the ImportError below explains the rest
        pass
    import instaloader  # noqa: PLC0415
    L = instaloader.Instaloader(download_pictures=False, download_videos=False, download_video_thumbnails=False,
                                download_comments=False, save_metadata=False, quiet=True, max_connection_attempts=2)
    if session_user:
        L.load_session_from_file(session_user)
    elif os.environ.get(SESSION_ENV) and not browser:
        L.context.update_cookies({"sessionid": os.environ[SESSION_ENV].strip()})
        user = L.test_login()
        if not user:
            raise RuntimeError(f"{SESSION_ENV} is set but Instagram does not accept it (expired or logged out)")
        L.context.username = user  # cookies alone leave instaloader in anonymous mode, which cloud IPs get redirected from
    elif browser:  # the user's own browser login, read locally; never written to disk by this tool
        from instaloader.__main__ import get_cookies_from_instagram  # noqa: PLC0415
        cookies = get_cookies_from_instagram("instagram", browser, None)
        if cookies:
            L.context.update_cookies(cookies)
            user = L.test_login()
            if not user:
                raise RuntimeError(f"not logged in to Instagram in {browser}")
            L.context.username = user
    if hashtag:
        it = instaloader.Hashtag.from_name(L.context, handle).get_posts_resumable()
    else:
        it = instaloader.Profile.from_username(L.context, handle).get_posts()
    for n, p in enumerate(it):
        if n >= limit:
            break
        yield post_record(shortcode=p.shortcode, account=p.owner_username, is_video=p.is_video,
                          url=f"https://www.instagram.com/{'reel' if p.is_video else 'p'}/{p.shortcode}/",
                          caption=p.caption, hashtags=list(p.caption_hashtags), alt=p.accessibility_caption,
                          date=p.date_utc.date().isoformat() if p.date_utc else None,
                          views=p.video_view_count if p.is_video else None, likes=p.likes,
                          duration=p.video_duration if p.is_video else None, thumbnail=p.url,
                          source=("#" if hashtag else "@") + handle)


def env_cookiefile() -> str | None:
    """Write INSTAGRAM_SESSIONID to a private temporary Netscape cookies file for yt-dlp; deleted at exit."""
    value = os.environ.get(SESSION_ENV, "").strip()
    if not value or any(c in value for c in "\t\r\n"):
        return None
    fd, path = tempfile.mkstemp(prefix="ig-cookies-", suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:  # mkstemp creates the file with mode 0600
        f.write("# Netscape HTTP Cookie File\n")
        f.write(f".instagram.com\tTRUE\t/\tTRUE\t2147483647\tsessionid\t{value}\n")
    atexit.register(lambda: os.path.exists(path) and os.remove(path))
    return path


def ytdlp_post(url: str, cookies: str | None, browser: str | None = None) -> dict:
    sys.path.insert(0, str(FETCHER.parent))
    from fetch_video import find_ytdlp  # noqa: PLC0415
    ytdlp = find_ytdlp()
    if not ytdlp:
        raise RuntimeError("yt-dlp not found: pip install yt-dlp")
    cmd = ytdlp + ["--skip-download", "--dump-json", "--no-playlist", "--no-warnings"]
    if cookies:
        cmd += ["--cookies", cookies]
    if browser:
        cmd += ["--cookies-from-browser", browser]
    p = subprocess.run(cmd + ["--", url], text=True, capture_output=True, timeout=120)
    if p.returncode or not p.stdout.strip():
        err = (p.stderr or "no metadata").strip()
        lines = [l for l in err.splitlines() if l.startswith("ERROR")]
        raise RuntimeError((lines[-1] if lines else err)[:300])
    d = json.loads(p.stdout.strip().splitlines()[0])
    up = d.get("upload_date") or ""
    return post_record(shortcode=d.get("id") or url.rstrip("/").rsplit("/", 1)[-1], url=url,
                       account=d.get("channel") or d.get("uploader_id") or d.get("uploader"),
                       is_video=bool(d.get("duration") or d.get("vcodec") not in (None, "none")),
                       caption=d.get("description") or d.get("title"), hashtags=d.get("tags") or [],
                       date=f"{up[:4]}-{up[4:6]}-{up[6:]}" if len(up) == 8 else None,
                       views=d.get("view_count"), likes=d.get("like_count"), duration=d.get("duration"),
                       thumbnail=d.get("thumbnail"), source="link")


# ---------------------------------------------------------------- ranking
def score_post(post: dict, groups: list[dict], phrase: str) -> tuple[float, list[str]]:
    tags = {stem(norm_text(h)) for h in post.get("hashtags", [])}
    cap = set(tokens(post.get("caption", "")))
    alt = set(tokens(post.get("alt", "")))
    blob = " ".join([norm_text(post.get("caption", "")), " ".join(tags)])
    total, hit_groups, why = 0.0, 0, []
    for g in groups:
        best, reason = 0.0, ""
        for t in g["terms"]:
            exact = t == g["word"]
            w = 1.0 if exact else 0.7
            if t in tags:
                s, r = 3.0 * w, f"#{t}"
            elif any(len(t) >= 4 and t in h for h in tags):
                s, r = 2.0 * w, f"#…{t}…"
            elif t in cap:
                s, r = 2.0 * w, f"caption:{t}"
            elif t in alt:
                s, r = 1.5 * w, f"image:{t}"
            elif len(t) >= 4 and t in blob:
                s, r = 1.0 * w, f"~{t}"
            else:
                continue
            if s > best:
                best, reason = s, r
        if best:
            hit_groups += 1
            total += best
            why.append(reason)
    if not hit_groups:
        return 0.0, []
    coverage = hit_groups / len(groups)
    total *= 0.4 + 0.6 * coverage
    if len(groups) > 1 and phrase and phrase in blob:
        total += 2.0
        why.append("phrase")
    if post.get("views"):
        total += min(1.0, math.log10(1 + post["views"]) / 7)
    return round(total, 3), why


def search(idx: dict, query: str, top: int = 20, account: str | None = None, include_photos: bool = False,
           min_dur: float | None = None, max_dur: float | None = None, since: str | None = None,
           syn=None) -> list[dict]:
    groups = expand_query(query, syn)
    if not groups:
        return []
    phrase = " ".join(tokens(query))
    hits = []
    for p in idx.get("posts", {}).values():
        if not include_photos and not p.get("is_video"):
            continue
        if account and p.get("account") != account.lower().lstrip("@"):
            continue
        d = p.get("duration")
        if min_dur is not None and (d is None or d < min_dur):
            continue
        if max_dur is not None and (d is None or d > max_dur):
            continue
        if since and (p.get("date") or "") < since:
            continue
        s, why = score_post(p, groups, phrase)
        if s > 0:
            hits.append({**p, "score": s, "why": why})
    hits.sort(key=lambda h: (-h["score"], h.get("date") or "", h["shortcode"]))
    for i, h in enumerate(hits[:top], 1):
        h["rank"] = i
    return hits[:top]


# ---------------------------------------------------------------- commands
def cmd_accounts(a) -> int:
    src = load_sources(a.sources)
    if a.json:
        print(json.dumps(src["accounts"], ensure_ascii=False, indent=1))
    else:
        for acc in src["accounts"]:
            print(f"@{acc['handle']:<24} {acc['url']}")
        print(f"{len(src['accounts'])} saved account(s)")
    return 0


def cmd_add_account(a) -> int:
    src = load_sources(a.sources)
    have = {x["handle"] for x in src["accounts"]}
    rc = 0
    for raw in a.links:
        try:
            acc = normalize_account(raw)
        except ValueError as e:
            print("SKIP " + str(e), file=sys.stderr)
            rc = 2
            continue
        if acc["handle"] in have:
            print(f"already saved: @{acc['handle']}")
            continue
        src["accounts"].append({**acc, "added": dt.date.today().isoformat(), "tags": list(a.tag or [])})
        have.add(acc["handle"])
        print(f"saved @{acc['handle']} → {acc['url']}")
    save_sources(src, a.sources)
    return rc


def cmd_remove_account(a) -> int:
    src = load_sources(a.sources)
    h = a.handle.lower().lstrip("@")
    before = len(src["accounts"])
    src["accounts"] = [x for x in src["accounts"] if x["handle"] != h]
    save_sources(src, a.sources)
    print(("removed @" + h) if len(src["accounts"]) < before else ("not saved: @" + h))
    return 0


def cmd_plan(a) -> int:
    groups = expand_query(a.query)
    tags = hashtag_ideas(a.query)
    words = " ".join(g["word"] for g in groups)
    q = urllib.parse.quote_plus
    plan = {"query": a.query, "keyword_groups": groups, "hashtags": tags,
            "saved_accounts": [x["url"] for x in load_sources(a.sources)["accounts"]],
            "web_searches": [f"https://www.google.com/search?q={q(f'site:instagram.com/reel {words}')}",
                             f"https://www.google.com/search?q={q('site:instagram.com/reel ' + ' OR '.join('#' + t for t in tags[:5]))}",
                             f"https://duckduckgo.com/?q={q(f'site:instagram.com/reel {words}')}"],
            "next": ["index the saved accounts: instagram_finder.py index --session-user <you>",
                     "paste reel links you found: instagram_finder.py add-posts <links>",
                     f'rank them: instagram_finder.py search "{a.query}" --save out/instagram/hits.json']}
    print(json.dumps(plan, ensure_ascii=False, indent=1))
    return 0


LOGIN_HINT = ("Instagram wants a login from this network (common on cloud and datacenter IPs). "
              "Run on your own computer with --browser chrome (index) or --cookies-from-browser chrome (add-posts). "
              "INSTAGRAM_SESSIONID does not lift this: tested 2026-10-24, the session is accepted but profile pages "
              "and post timelines still redirect from cloud IPs. "
              "| إنستجرام طالب تسجيل دخول من الشبكة دي، وحتى INSTAGRAM_SESSIONID مش بيحل ده من سيرفر الكلاود؛ شغّل الأداة على جهازك مع --browser chrome.")


def is_login_wall(e) -> bool:
    t = str(e).lower()
    return any(k in t for k in ("302 found", "accounts/login", "require_login", "login required",
                                "empty media response", "cookies", "401"))


def cmd_index(a) -> int:
    path = Path(a.index)
    idx = load_index(path)
    saved = [x["handle"] for x in load_sources(a.sources)["accounts"]]
    handles = saved if a.accounts in (None, "all") else [normalize_account(h)["handle"] for h in a.accounts.split(",")]
    targets = [(h, False) for h in handles] + [(t.lstrip("#").lower(), True) for t in (a.hashtag or [])]
    limit = max(1, min(a.limit, MAX_PER_ACCOUNT))
    known = set(idx["posts"])
    report, rc = [], 0
    for i, (name, is_tag) in enumerate(targets):
        if i:
            time.sleep(a.sleep)
        new = 0
        try:
            for rec in instaloader_posts(name, limit, a.session_user, hashtag=is_tag, browser=a.browser):
                if rec["shortcode"] in known and not a.full and not is_tag:
                    break  # profiles are newest first: the rest is already indexed
                idx["posts"][rec["shortcode"]] = rec
                known.add(rec["shortcode"])
                new += 1
        except ImportError:
            print("instaloader is not installed: pip install instaloader (or use add-posts with yt-dlp)", file=sys.stderr)
            return 1
        except Exception as e:  # network, login, rate limit, private account
            rc = 1
            report.append({"source": ("#" if is_tag else "@") + name, "error": str(e)[:300]})
            print(f"FAIL {'#' if is_tag else '@'}{name}: {str(e)[:200]}", file=sys.stderr)
            if "429" in str(e) or "wait a few minutes" in str(e).lower():
                print("Instagram asked us to slow down; stopping this run.", file=sys.stderr)
                break
            if is_login_wall(e):
                print(LOGIN_HINT, file=sys.stderr)
                break  # every other account will hit the same wall
            continue
        finally:
            save_index(idx, path)
        report.append({"source": ("#" if is_tag else "@") + name, "new_posts": new})
        print(f"OK   {'#' if is_tag else '@'}{name}: {new} new post(s)")
    print(f"index: {path} ({len(idx['posts'])} posts)")
    return rc


def cmd_add_posts(a) -> int:
    path = Path(a.index)
    idx = load_index(path)
    raw = list(a.urls)
    if a.urlfile:
        raw += [l.strip() for l in Path(a.urlfile).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    rc = 0
    for i, u in enumerate(raw):
        url = clean_post_url(u)
        if not url:
            print(f"SKIP not an Instagram post/reel link: {u[:80]}", file=sys.stderr)
            rc = 2
            continue
        if i:
            time.sleep(a.sleep)
        try:
            rec = ytdlp_post(url, a.cookies, a.cookies_from_browser)
        except Exception as e:
            print(f"FAIL {url}: {str(e)[:200]}", file=sys.stderr)
            rc = 1
            if is_login_wall(e):
                print(LOGIN_HINT, file=sys.stderr)
                break  # the rest of the links will hit the same wall
            continue
        idx["posts"][rec["shortcode"]] = rec
        print(f"OK   {url} @{rec['account']}")
    save_index(idx, path)
    print(f"index: {path} ({len(idx['posts'])} posts)")
    return rc


def cmd_search(a) -> int:
    idx = load_index(Path(a.index))
    if not idx["posts"]:
        print("the index is empty: run `index` or `add-posts` first", file=sys.stderr)
        return 1
    hits = search(idx, a.query, a.top, a.account, a.include_photos, a.min_dur, a.max_dur, a.since)
    if a.save:
        Path(a.save).parent.mkdir(parents=True, exist_ok=True)
        Path(a.save).write_text(json.dumps({"query": a.query, "hits": hits}, ensure_ascii=False, indent=1), encoding="utf-8")
    if a.json:
        print(json.dumps(hits, ensure_ascii=False, indent=1))
    else:
        for h in hits:
            cap = re.sub(r"\s+", " ", h["caption"])[:70]
            print(f"{h['rank']:>2}. {h['score']:>5}  @{h['account']:<18} {h['url']}\n      {', '.join(h['why'])} · {cap}")
        print(f"{len(hits)} match(es) for {a.query!r} in {len(idx['posts'])} indexed posts")
    return 0 if hits else 1


def _load_hits(p: str) -> list[dict]:
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return d["hits"] if isinstance(d, dict) else d


def _pick(hits: list[dict], pick: str | None, top: int | None) -> list[dict]:
    if pick:
        want = [int(x) for x in pick.split(",") if x.strip()]
        by_rank = {h.get("rank", i + 1): h for i, h in enumerate(hits)}
        missing = [w for w in want if w not in by_rank]
        if missing:
            raise SystemExit(f"--pick ranks not in results: {missing}")
        return [by_rank[w] for w in want]
    return hits[: (top or 5)]


def cmd_thumbs(a) -> int:
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rc = 0
    for h in _pick(_load_hits(a.results), a.pick, a.top):
        t = h.get("thumbnail")
        if not t or urllib.parse.urlsplit(t).scheme != "https":
            print(f"no thumbnail for #{h.get('rank')} {h['url']}")
            continue
        dst = out / f"{h.get('rank', 0):02d}_{h['shortcode']}.jpg"
        try:
            with urllib.request.urlopen(urllib.request.Request(t, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                dst.write_bytes(r.read(5_000_000))
            print(f"OK   {dst}")
        except Exception as e:  # thumbnail links from Instagram expire after a while
            rc = 1
            print(f"FAIL #{h.get('rank')} {e} (re-run index/add-posts for a fresh link)", file=sys.stderr)
        time.sleep(a.sleep)
    return rc


def cmd_download(a) -> int:
    if a.rights != "owned" and a.rights != "reference-only" and not a.evidence:
        print("RIGHTS CHECK: --rights permission/licensed needs --evidence (a link or note proving it)", file=sys.stderr)
        return 2
    return _download(_pick(_load_hits(a.results), a.pick, a.top), a)


def cmd_get(a) -> int:
    """One step for a link you already have: clean it, download it, log the rights. No index needed."""
    if a.rights != "owned" and a.rights != "reference-only" and not a.evidence:
        print("RIGHTS CHECK: --rights permission/licensed needs --evidence (a link or note proving it)", file=sys.stderr)
        return 2
    raw = list(a.urls)
    if a.urlfile:  # e.g. the .txt the Chrome extension "Instagram link collector" exports
        raw += [l.strip() for l in Path(a.urlfile).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    chosen, rc, seen = [], 0, set()
    for u in raw:
        url = clean_post_url(u)
        if not url:
            print(f"SKIP not an Instagram post/reel link: {u[:80]}", file=sys.stderr)
            rc = 2
            continue
        if url not in seen:
            seen.add(url)
            chosen.append({"url": url, "account": None})
    if not chosen:
        return rc or 2
    return _download(chosen, a) or rc


def _download(chosen: list, a) -> int:
    cap = min(a.max, 100)
    if len(chosen) > cap:
        print(f"refusing {len(chosen)} downloads in one run (cap {cap}); pick fewer or raise --max", file=sys.stderr)
        return 2
    out = Path(a.out)
    base = [sys.executable, str(FETCHER), "-o", str(out), "--quality", a.quality]
    if a.safe:
        base.append("--safe")
    if a.cookies:
        base += ["--cookies", a.cookies]
    if a.cookies_from_browser:
        base += ["--cookies-from-browser", a.cookies_from_browser]
    if a.dry_run:
        print(json.dumps({"action": "dry_run_no_download", "rights": a.rights,
                          "commands": [base + [h["url"]] for h in chosen]}, ensure_ascii=False, indent=1))
        return 0
    out.mkdir(parents=True, exist_ok=True)
    log = out / "instagram_rights.jsonl"
    rc = 0
    for i, h in enumerate(chosen):
        if i:
            time.sleep(a.sleep)
        p = subprocess.run(base + [h["url"]], text=True, capture_output=True)
        rec = None
        try:
            rec = next((r for r in json.loads((out / "manifest.json").read_text(encoding="utf-8"))
                        if r.get("url") == h["url"] and r.get("file")), None)
        except (OSError, ValueError):
            pass
        if p.returncode or not rec:
            rc = 1
            print(f"FAIL {h['url']}\n     {(p.stderr or p.stdout).strip()[-300:]}", file=sys.stderr)
            continue
        entry = {"downloaded_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                 "url": h["url"], "account": h.get("account"), "file": rec["file"], "safe_file": rec.get("safe_file"),
                 "rights": a.rights, "evidence": a.evidence,
                 "credit": f"@{h['account']}" if h.get("account") else rec.get("uploader") or "see the post",
                 "note": "operator rights assertion, not a legal audit"}
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"OK   {rec['file']}")
    print(f"rights log: {log}")
    return rc


def cmd_doctor(a) -> int:
    sys.path.insert(0, str(FETCHER.parent))
    from fetch_video import find_ytdlp  # noqa: PLC0415
    try:
        import instaloader  # noqa: F401,PLC0415
        il = getattr(instaloader, "__version__", "ok")
    except ImportError:
        il = "MISSING (pip install instaloader) — needed for `index`"
    yt = find_ytdlp()
    print("instaloader:", il)
    print("yt-dlp:", " ".join(yt) if yt else "MISSING (pip install yt-dlp) — needed for add-posts and download")
    print(f"{SESSION_ENV}:", "set (value hidden)" if os.environ.get(SESSION_ENV) else "not set (optional)")
    print("saved accounts:", len(load_sources(a.sources)["accounts"]))
    idx = load_index(Path(a.index))
    print("index:", a.index, f"({len(idx['posts'])} posts)")
    return 0 if yt else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", type=Path, default=SOURCES, help=argparse.SUPPRESS)
    ap.add_argument("--index", default=str(DEFAULT_INDEX), help="local index file (default out/instagram/index.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("accounts", help="list saved source accounts")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("add-account", help="save profile links (tracking parameters are removed)")
    s.add_argument("links", nargs="+")
    s.add_argument("--tag", action="append", help="a label such as 'product' or 'food'")
    s = sub.add_parser("remove-account")
    s.add_argument("handle")
    s = sub.add_parser("plan", help="offline: keywords, synonyms, hashtags and web searches for a product")
    s.add_argument("query")
    s = sub.add_parser("index", help="read recent posts of saved accounts into the local index (instaloader)")
    s.add_argument("--accounts", help="comma-separated handles (default: all saved)")
    s.add_argument("--hashtag", action="append", help="also index a hashtag (needs --session-user)")
    s.add_argument("--limit", type=int, default=40, help=f"posts per account (max {MAX_PER_ACCOUNT})")
    s.add_argument("--session-user", help="your Instagram username with a saved instaloader session (instaloader -l USER)")
    s.add_argument("--browser", help="use your Instagram login from a local browser (chrome, firefox, edge, brave, safari…)")
    s.add_argument("--sleep", type=float, default=8.0, help="seconds between accounts (default 8)")
    s.add_argument("--full", action="store_true", help="re-read posts already indexed")
    s = sub.add_parser("add-posts", help="index single post/reel links with yt-dlp")
    s.add_argument("urls", nargs="*")
    s.add_argument("--urls", dest="urlfile")
    s.add_argument("--cookies")
    s.add_argument("--cookies-from-browser", metavar="BROWSER", help="your login from a local browser")
    s.add_argument("--sleep", type=float, default=4.0)
    s = sub.add_parser("search", help="rank indexed videos for a product query (Arabic or English)")
    s.add_argument("query")
    s.add_argument("--top", type=int, default=20)
    s.add_argument("--account")
    s.add_argument("--include-photos", action="store_true")
    s.add_argument("--min-dur", type=float)
    s.add_argument("--max-dur", type=float)
    s.add_argument("--since", help="YYYY-MM-DD")
    s.add_argument("--save", help="write results JSON for thumbs/download")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("get", help="download reel/post links you already have, in one step (no index needed)")
    s.add_argument("urls", nargs="*", help="Instagram reel or post links (tracking parameters are removed)")
    s.add_argument("--urls", dest="urlfile", help="a text file with one link per line (for example from the Chrome extension)")
    s.add_argument("--rights", choices=RIGHTS, default="reference-only",
                   help="owned | permission | licensed | reference-only (default: private study, not for publishing)")
    s.add_argument("--evidence", help="link or note proving permission/licence")
    s.add_argument("-o", "--out", default=str(Path("out") / "instagram" / "videos"))
    s.add_argument("--quality", default="1080")
    s.add_argument("--cookies", help="your own Netscape cookies.txt (never commit it)")
    s.add_argument("--cookies-from-browser", metavar="BROWSER", help="your login from a local browser")
    s.add_argument("--safe", action=argparse.BooleanOptionalAction, default=True)
    s.add_argument("--sleep", type=float, default=5.0)
    s.add_argument("--max", type=int, default=MAX_DOWNLOADS)
    s.add_argument("--dry-run", action="store_true")
    for name in ("thumbs", "download"):
        s = sub.add_parser(name, help="thumbnails of chosen results" if name == "thumbs" else
                           "download chosen results through fetch_video.py")
        s.add_argument("results", help="JSON written by search --save")
        s.add_argument("--pick", help="ranks, e.g. 1,3,5")
        s.add_argument("--top", type=int, help="first N results (default 5)")
        s.add_argument("--sleep", type=float, default=5.0 if name == "download" else 1.0)
        s.add_argument("-o", "--out", default=str(Path("out") / "instagram" / ("thumbs" if name == "thumbs" else "videos")))
        if name == "download":
            s.add_argument("--rights", choices=RIGHTS, required=True,
                           help="owned | permission | licensed | reference-only (private study, not for publishing)")
            s.add_argument("--evidence", help="link or note proving permission/licence")
            s.add_argument("--quality", default="1080")
            s.add_argument("--cookies", help="your own Netscape cookies.txt (never commit it)")
            s.add_argument("--cookies-from-browser", metavar="BROWSER", help="your login from a local browser")
            s.add_argument("--safe", action=argparse.BooleanOptionalAction, default=True)
            s.add_argument("--max", type=int, default=MAX_DOWNLOADS)
            s.add_argument("--dry-run", action="store_true")
    sub.add_parser("doctor")
    a = ap.parse_args(argv)
    if hasattr(a, "cookies") and not a.cookies and not getattr(a, "cookies_from_browser", None):
        a.cookies = env_cookiefile()  # None unless INSTAGRAM_SESSIONID is set
    fn = {"accounts": cmd_accounts, "add-account": cmd_add_account, "remove-account": cmd_remove_account,
          "plan": cmd_plan, "index": cmd_index, "add-posts": cmd_add_posts, "search": cmd_search,
          "thumbs": cmd_thumbs, "download": cmd_download, "get": cmd_get, "doctor": cmd_doctor}[a.cmd]
    return fn(a)


if __name__ == "__main__":
    sys.exit(main())
