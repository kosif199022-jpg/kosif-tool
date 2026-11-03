#!/usr/bin/env python3
"""Suno bridge (appendix A46): the local half of the Suno MCP connector.

The Suno MCP server (https://api.suno.com/mcp) is reached by Claude through a
connector signed in with the user's Suno account (OAuth, no API key). This
script never holds a token and never generates music. It does the parts that
can be checked locally:

  doctor   offline facts: endpoint, OAuth scopes from the committed probe
           evidence, the consent rule, where the connector is added.
  probe    unauthenticated, read-only HTTP check of the server and its OAuth
           metadata (no credits; a 401 is the expected healthy answer).
  plan     turn a request into a Suno song brief (style tags, structure,
           lyric scaffold, duration) plus an approval_digest. Generating
           spends Suno credits (credits:spend), so the brief is shown to the
           user and only their explicit yes lets Claude call the generation tool.
  receipt  after the approved generation, check the tool's returned JSON
           (song id, duration, link) against the approved digest and write a
           SHA-256 receipt. A mismatched digest is refused.

Stdlib only. Exit codes: 0 ok, 1 refused/invalid, 2 usage, 3 network blocked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.suno.com/mcp"
RESOURCE_METADATA = "https://api.suno.com/.well-known/oauth-protected-resource/mcp"
SKILL = Path(__file__).resolve().parents[1]
EVIDENCE = SKILL / "references" / "protocol" / "evidence" / "A46-suno-mcp-probe.txt"
SCHEMA_PLAN = "kosif.suno.plan.v1"
SCHEMA_RECEIPT = "kosif.suno.receipt.v1"
STYLE_LIMIT = 200  # Suno style field is short; keep the tags compact

# keyword -> (genre tags, mood) ; Arabic and English, checked in order
GENRES = [
    (("دعاء", "ابتهال", "نشيد", "اناشيد", "أناشيد", "dua", "nasheed", "islamic", "ramadan", "رمضان", "جمعة"),
     ["nasheed", "a cappella", "spiritual"], "spiritual"),
    (("مهرجان", "mahraganat", "شعبي", "shaabi"), ["mahraganat", "egyptian shaabi", "electro"], "energetic"),
    (("خليجي", "khaleeji", "سعودي", "saudi"), ["khaleeji", "arabic pop"], "celebratory"),
    (("طرب", "tarab", "عود", "oud", "كلاسيك عربي"), ["arabic tarab", "oud", "qanun", "strings"], "nostalgic"),
    (("إعلان", "اعلان", "ad ", "advert", "promo", "commercial", "jingle"), ["upbeat pop", "jingle", "catchy hook"], "upbeat"),
    (("سينمائي", "cinematic", "epic", "ملحمي", "trailer", "تريلر"), ["cinematic orchestral", "epic", "hybrid trailer"], "epic"),
    (("lofi", "lo-fi", "لوفاي", "هادي", "هادئ", "calm", "relax"), ["lo-fi", "chill", "soft piano"], "calm"),
    (("راب", "rap", "hip hop", "هيب هوب", "trap", "تراب"), ["arabic rap", "trap beat"], "confident"),
    (("حزين", "sad", "ballad", "رومانسي", "romantic", "حب", "love"), ["arabic ballad", "piano", "strings"], "emotional"),
    (("أطفال", "اطفال", "kids", "children"), ["children's song", "playful", "bright"], "playful"),
    (("رياضة", "sport", "workout", "gym", "حماس"), ["edm", "anthem", "driving drums"], "energetic"),
]
DEFAULT_GENRE = (["arabic pop", "modern production"], "warm")
NO_INSTRUMENT_WORDS = ("بدون موسيقى", "بلا موسيقى", "بدون آلات", "بلا آلات", "no instruments",
                       "no music", "a cappella", "acapella", "صوت فقط", "vocals only")
INSTRUMENTAL_WORDS = ("بدون كلام", "بلا كلام", "موسيقى فقط", "instrumental", "no vocals", "بدون غناء")
DIALECTS = [
    (("مصري", "مصرية", "egyptian"), "Egyptian Arabic"),
    (("خليجي", "سعودي", "khaleeji", "saudi"), "Gulf Arabic"),
    (("شامي", "لبناني", "سوري", "levantine"), "Levantine Arabic"),
    (("فصحى", "msa", "classical arabic"), "Modern Standard Arabic"),
]


def _has(text: str, words) -> bool:
    return any(w in text for w in words)


def _arabic(text: str) -> bool:
    return bool(re.search(r"[؀-ۿ]", text))


def _duration(text: str, given: int | None) -> int:
    if given:
        return given
    m = re.search(r"(\d{1,3})\s*(ث|ثانية|ثواني|s\b|sec|seconds)", text)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{1,2})\s*(د|دقيقة|دقايق|دقائق|min|minutes)", text)
    if m:
        return int(m.group(1)) * 60
    return 30 if _has(text, ("إعلان", "اعلان", "ad ", "promo", "reel", "ريلز", "تيك توك", "tiktok")) else 120


def _structure(seconds: int, instrumental: bool) -> list[str]:
    if instrumental:
        return ["Intro", "Theme", "Build", "Drop", "Outro"] if seconds > 45 else ["Intro", "Theme", "Outro"]
    if seconds <= 35:
        return ["Hook", "Chorus", "Tag"]
    if seconds <= 90:
        return ["Intro", "Verse", "Chorus", "Outro"]
    return ["Intro", "Verse 1", "Pre-Chorus", "Chorus", "Verse 2", "Chorus", "Bridge", "Final Chorus", "Outro"]


def build_plan(task: str, duration: int | None = None, lang: str | None = None,
               instrumental: bool | None = None, vocal: str | None = None) -> dict:
    low = " " + task.lower() + " "
    tags, mood = DEFAULT_GENRE
    for words, gtags, gmood in GENRES:
        if _has(low, words):
            tags, mood = gtags, gmood
            break
    tags = list(tags)
    no_instruments = _has(low, NO_INSTRUMENT_WORDS) or "a cappella" in tags
    if no_instruments and "a cappella" not in tags:
        tags.insert(0, "a cappella")
    if instrumental is None:
        instrumental = _has(low, INSTRUMENTAL_WORDS)
    if instrumental and no_instruments:
        instrumental = False  # vocals-only beats "instrumental": an a cappella piece has no instruments
    language = lang or ("Arabic" if _arabic(task) else "English")
    dialect = next((d for words, d in DIALECTS if _has(low, words)), None)
    if language.lower().startswith("ar") and dialect:
        tags.append(dialect.lower())
    if not instrumental:
        tags.append(vocal or ("male vocals" if _has(low, ("رجالي", "male", "شاب")) else
                              "female vocals" if _has(low, ("نسائي", "female", "بنت")) else "clear vocals"))
    tags.append(mood)
    style = ", ".join(dict.fromkeys(t for t in tags if t))[:STYLE_LIMIT]
    seconds = _duration(low, duration)
    sections = _structure(seconds, instrumental)
    lyrics = None if instrumental else "\n\n".join(
        f"[{s}]\n<{'اكتب هنا' if language.lower().startswith('ar') else 'write here'}: {s.lower()} — "
        f"{task.strip()[:60]}>" for s in sections)
    prompt = {"style": style, "instrumental": bool(instrumental), "duration_seconds": seconds,
              "language": language, "dialect": dialect, "structure": sections, "lyrics_scaffold": lyrics,
              "title_hint": task.strip()[:60]}
    digest = hashlib.sha256(json.dumps(prompt, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    notes = []
    if no_instruments:
        notes.append("vocals only, no instruments (a cappella / nasheed), as many users want for religious content")
    if lyrics:
        notes.append("lyrics_scaffold is a structure with placeholders: Claude writes the real lyrics with the user, "
                     "and any change to them changes the digest")
    return {
        "schema": SCHEMA_PLAN, "task": task, "prompt": prompt, "approval_digest": digest,
        "endpoint": ENDPOINT, "credits_spend": True, "approval_required": True, "generated": False,
        "consent": ("Generating spends Suno credits. Show style, lyrics and duration to the user and get an "
                    "explicit yes; a digest is not consent. Changed prompt = new digest = ask again."),
        "next": ["Show this brief to the user and wait for yes",
                 "Call the Suno MCP generation tool with exactly prompt.style / lyrics / instrumental",
                 "Save the tool's JSON answer, then: suno_bridge.py receipt --plan PLAN --result RESULT "
                 "--approved-digest " + digest],
        "fallback": ["Higgsfield generate_audio (same credit consent)",
                     "licensed free music with source and licence (free_footage/free_photos style sidecar)",
                     "leave the music slot empty and write 'waiting for Suno' in the delivery"],
        "notes": notes,
    }


def _first(obj, keys):
    """Find the first value for any of keys anywhere in a nested JSON answer."""
    if isinstance(obj, dict):
        for k in keys:
            if obj.get(k) not in (None, ""):
                return obj[k]
        for v in obj.values():
            found = _first(v, keys)
            if found not in (None, ""):
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = _first(v, keys)
            if found not in (None, ""):
                return found
    return None


def build_receipt(plan: dict, result: dict, approved: str, audio: Path | None = None) -> tuple[dict, list[str]]:
    errors = []
    if plan.get("schema") != SCHEMA_PLAN:
        errors.append("plan is not a kosif.suno.plan.v1 file")
    recomputed = hashlib.sha256(json.dumps(plan.get("prompt", {}), ensure_ascii=False,
                                           sort_keys=True).encode()).hexdigest()
    if recomputed != plan.get("approval_digest"):
        errors.append("plan was edited after its digest was computed: re-run plan and ask the user again")
    if approved != plan.get("approval_digest"):
        errors.append("approved digest does not match this plan: the user approved a different prompt")
    song_id = _first(result, ("id", "song_id", "clip_id", "uuid"))
    url = _first(result, ("audio_url", "url", "stream_url", "song_url", "link"))
    dur = _first(result, ("duration", "duration_seconds", "length"))
    if not song_id:
        errors.append("result has no song id: 'made' is only claimed when the tool returned one")
    if not url and audio is None:
        errors.append("result has no audio link and no downloaded --audio file")
    audio_meta = None
    if audio is not None:
        if not audio.is_file() or audio.stat().st_size == 0:
            errors.append("--audio file is missing or empty")
        else:
            audio_meta = {"path": str(audio), "bytes": audio.stat().st_size,
                          "sha256": hashlib.sha256(audio.read_bytes()).hexdigest()}
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True).encode()
    receipt = {"schema": SCHEMA_RECEIPT, "status": "VERIFIED" if not errors else "REFUSED",
               "approval_digest": plan.get("approval_digest"), "song_id": song_id, "audio_url": url,
               "duration_seconds": dur, "result_sha256": hashlib.sha256(raw).hexdigest(),
               "audio_file": audio_meta, "style": plan.get("prompt", {}).get("style"),
               "licence_note": "ownership and commercial use follow the user's Suno plan; not checked here",
               "errors": errors}
    return receipt, errors


def doctor() -> dict:
    scopes = []
    if EVIDENCE.is_file():
        m = re.search(r'"scopes_supported":\[([^\]]*)\]', EVIDENCE.read_text(encoding="utf-8"))
        if m:
            scopes = [s.strip().strip('"') for s in m.group(1).split(",") if s.strip()]
    return {"schema": "kosif.suno.doctor.v1", "endpoint": ENDPOINT, "auth": "OAuth 2.1 with the Suno account, no API key",
            "evidence_file": str(EVIDENCE.relative_to(SKILL)) if EVIDENCE.is_file() else None,
            "resource_scopes": scopes, "spends_credits": "credits:spend" in scopes,
            "connect": {"claude.ai": "Settings > Connectors > Add custom connector > https://api.suno.com/mcp",
                        "claude-code": "claude mcp add --transport http suno https://api.suno.com/mcp ; then /mcp"},
            "in_claude_ai_directory": False,
            "rule": "read-only calls free; any generation needs the user's explicit yes on the shown brief",
            "network_requests": 0}


def probe(timeout: float = 15.0) -> tuple[dict, int]:
    out = {"schema": "kosif.suno.probe.v1", "endpoint": ENDPOINT, "credentials_sent": False}
    req = urllib.request.Request(ENDPOINT, headers={"User-Agent": "kosif-suno-bridge/1", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out.update(http_status=r.status, verdict="unexpected: answered without sign-in")
    except urllib.error.HTTPError as e:
        out.update(http_status=e.code, www_authenticate=e.headers.get("www-authenticate"),
                   verdict="healthy: server up, needs Suno sign-in" if e.code == 401 else "unexpected status")
    except (urllib.error.URLError, OSError) as e:
        out.update(http_status=None, verdict="network-blocked from this machine", error=str(e)[:200])
        return out, 3
    try:
        with urllib.request.urlopen(RESOURCE_METADATA, timeout=timeout) as r:
            meta = json.loads(r.read(65536).decode("utf-8"))  # metadata is ~300 bytes; bound the read
            out["scopes_supported"] = meta.get("scopes_supported")
            out["authorization_servers"] = meta.get("authorization_servers")
    except (urllib.error.URLError, OSError, ValueError) as e:
        out["metadata_error"] = str(e)[:200]
    return out, 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="offline facts about the connector and the consent rule")
    p = sub.add_parser("probe", help="unauthenticated read-only HTTP check (no credits)")
    p.add_argument("--timeout", type=float, default=15.0)
    p = sub.add_parser("plan", help="request -> Suno brief + approval_digest (never generates)")
    p.add_argument("task")
    p.add_argument("--duration", type=int, help="seconds")
    p.add_argument("--lang")
    p.add_argument("--instrumental", action="store_true", default=None)
    p.add_argument("--vocal", help="e.g. 'male vocals'")
    p.add_argument("--out", type=Path)
    p = sub.add_parser("receipt", help="check an approved generation result and write a receipt")
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--result", type=Path, required=True, help="the Suno tool's JSON answer, saved to a file")
    p.add_argument("--approved-digest", required=True)
    p.add_argument("--audio", type=Path, help="the downloaded audio file, if any")
    p.add_argument("--out", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "doctor":
        print(json.dumps(doctor(), ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "probe":
        out, code = probe(a.timeout)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return code
    if a.cmd == "plan":
        if not a.task.strip():
            print("task is empty", file=sys.stderr)
            return 2
        plan = build_plan(a.task, a.duration, a.lang, a.instrumental, a.vocal)
        text = json.dumps(plan, ensure_ascii=False, indent=2)
        if a.out:
            a.out.parent.mkdir(parents=True, exist_ok=True)
            a.out.write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0
    try:
        plan = json.loads(a.plan.read_text(encoding="utf-8"))
        result = json.loads(a.result.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"cannot read plan/result: {e}", file=sys.stderr)
        return 1
    receipt, errors = build_receipt(plan, result, a.approved_digest, a.audio)
    text = json.dumps(receipt, ensure_ascii=False, indent=2)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
