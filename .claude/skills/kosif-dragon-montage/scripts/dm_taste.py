#!/usr/bin/env python3
"""Station 4 «يختار الذوق» — pick the look for a Dragon Montage job.

  pick  --job DIR [--style ID] [--invent] [--seed N]
        reads brief.json (+ concepts.json chosen concept style_hint/rhythm, + look_override.json from dm_mimic if
        present) → writes look.json (kosif.dm.look.v1). Ranks all styles in data/taste_index.json by fit and says
        why in Egyptian Arabic. --style forces one style; --invent fuses a new look from kmx.py ideate parents
        (kosif-infinite-matrices) and records style_source "kmx".
  query --feeling tense [--platform reel] [--content talking-head] [--energy 0.7] [--top 5]
        prints the top styles for those tags.
  filter grade|transition|camera ID [--W 1080 --H 1920 --fps 30 --seconds 2]
        prints the executable ffmpeg filter (what dm_render applies).

Library helpers for other stations: grade_filter(id), transition_filter(id, offset, seconds=None),
camera_filter(id, W, H, fps, seconds, **params), resolve(kind, id_or_alias), vocab(kind).
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zlib
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

DATA = C.SKILL / "data"
KMX = C.MATRICES / "scripts" / "kmx.py"
STATION = "taste"

FEEL_AR = {"tense": "متوتر", "warm": "دافي", "epic": "ملحمي", "playful": "مرح", "calm": "هادي",
           "inspiring": "ملهم", "sad": "حزين", "funny": "كوميدي"}
FEEL_NEAR = {"tense": ["epic", "sad"], "warm": ["calm", "inspiring"], "epic": ["inspiring", "tense"],
             "playful": ["funny", "inspiring"], "calm": ["warm", "sad"], "inspiring": ["epic", "warm"],
             "sad": ["calm", "warm"], "funny": ["playful"]}
FEEL_ENERGY = {"tense": 0.7, "warm": 0.45, "epic": 0.7, "playful": 0.7, "calm": 0.25, "inspiring": 0.6,
               "sad": 0.3, "funny": 0.75}
PLATFORM_ASPECT = {"reel": "9:16", "story": "9:16", "youtube": "16:9", "landscape": "16:9", "square": "1:1"}
SRC_AR = {"catalog": "كتالوج الستايلات (311)", "library500": "مكتبة الـ500 ستايل", "atlas86": "أطلس الـ86",
          "kmx": "المصفوفات اللانهائية (kmx)", "mimic": "محاكاة فيديو مرجعي"}
TOKEN = re.compile(r"[\w\-]+", re.UNICODE)


# ---------------------------------------------------------------- vocabularies + filters

@lru_cache(maxsize=None)
def _load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def vocab(kind: str) -> dict[str, dict]:
    file, key = {"grade": ("grades.json", "grades"), "transition": ("transitions.json", "transitions"),
                 "camera": ("camera.json", "cameras"), "caption": ("caption_styles.json", "styles")}[kind]
    return {x["id"]: x for x in _load(file)[key]}


def resolve(kind: str, ident: str | None) -> str | None:
    """id, alias, original underscore name or (for transitions) bare xfade name → canonical id, else None."""
    if not ident:
        return None
    v = vocab(kind)
    s = str(ident).strip()
    if s in v:
        return s
    low = s.lower().replace("_", "-")
    for i, x in v.items():
        names = [i] + list(x.get("aliases") or []) + ([x["xfade"]] if x.get("xfade") else [])
        if s in names or low in [str(n).lower().replace("_", "-") for n in names]:
            return i
    if kind == "transition" and f"xfade-{low}" in v:
        return f"xfade-{low}"
    return None


def grade_filter(gid: str) -> str:
    g = vocab("grade")[resolve("grade", gid) or gid]
    return g["ffmpeg"]


def transition_filter(tid: str, offset: float, seconds: float | None = None) -> str | None:
    """xfade filter for [a][b], or None when the transition renders as a cut."""
    t = vocab("transition")[resolve("transition", tid) or tid]
    if not t.get("xfade"):
        return None
    sec = float(seconds if seconds is not None else t["seconds"])
    return f"xfade=transition={t['xfade']}:duration={sec:.3f}:offset={max(0.0, offset):.3f}"


def camera_filter(cid: str, W: int, H: int, fps: float, seconds: float, **params) -> str:
    c = vocab("camera")[resolve("camera", cid) or cid]
    p = {**c.get("defaults", {}), **{k: v for k, v in params.items() if k in c.get("defaults", {})}}
    ctx = {"W": int(W), "H": int(H), "W2": int(W) * 2, "H2": int(H) * 2, "fps": fps,
           "frames": max(1, round(seconds * fps)), **p}
    return c["ffmpeg"].format(**ctx)


# ---------------------------------------------------------------- ranking

def index() -> list[dict]:
    f = DATA / "taste_index.json"
    if not f.exists():
        import build_taste_index
        build_taste_index.main()
    return json.loads(f.read_text(encoding="utf-8"))["styles"]


def words(text: str) -> set[str]:
    return {w.lower() for w in TOKEN.findall(text or "") if len(w) > 2}


def score(row: dict, feeling: str, energy: float, platform: str | None, content: str | None,
          hint: set[str], avoid: set[str]) -> tuple[float, dict]:
    parts = {}
    moods = row["moods"]
    if feeling in moods:
        parts["feeling"] = [3.0, 2.0, 1.2][moods.index(feeling)]
    elif any(n in moods for n in FEEL_NEAR.get(feeling, [])):
        parts["feeling"] = 0.6
    parts["energy"] = round(2.0 * (1 - abs(row["energy"] - energy)), 3)
    if platform:
        parts["platform"] = 1.0 if platform in row["platforms"] else 0.6 if "any" in row["platforms"] else 0.0
    if content and content in row["content_types"]:
        parts["content"] = 2.0 if row["content_types"][0] == content else 1.4
    if feeling in vocab("grade")[row["grade_id"]]["feelings"]:
        parts["grade"] = 0.8                      # the style's own grade already carries the feeling
    bag = set(row.get("keywords") or []) | words(" ".join(map(str, [row.get("name"), row.get("slug"), row.get("family"), row["id"]])))
    hits = sorted(hint & bag)
    if hits:
        parts["hint"] = round(min(3.0, 1.2 * len(hits)), 2)
        parts["hint_words"] = hits[:6]
    bad = sorted(avoid & bag)
    if bad:
        parts["avoid"] = -1.5 * len(bad)
    total = sum(v for k, v in parts.items() if isinstance(v, (int, float)))
    return round(total, 3), parts


def rank(feeling: str, energy: float | None = None, platform: str | None = None, content: str | None = None,
         hint: str = "", avoid: list[str] | None = None, top: int | None = None) -> list[dict]:
    e = FEEL_ENERGY.get(feeling, 0.5) if energy is None else float(energy)
    hw, aw = words(hint), words(" ".join(avoid or []))
    out = []
    for r in index():
        s, parts = score(r, feeling, e, platform, content, hw, aw)
        out.append({**r, "score": s, "parts": parts})
    out.sort(key=lambda r: (-r["score"], r["source"], r["id"]))
    return out[:top] if top else out


# ---------------------------------------------------------------- look assembly

def _transitions(ids: list[str]) -> list[dict]:
    v, out = vocab("transition"), []
    for i in ["cut"] + list(ids):
        i = resolve("transition", i)
        if not i or any(t["id"] == i for t in out):
            continue
        t = {"id": i}
        if v[i].get("xfade"):
            t["seconds"] = v[i]["seconds"]
        out.append(t)
    return out[:4]


def _camera(ids: list[str]) -> list[dict]:
    v, out = vocab("camera"), []
    for i in ids:
        i = resolve("camera", i)
        if i and not any(c["id"] == i for c in out):
            out.append({"id": i, **v[i].get("defaults", {})})
    return out[:3]


def _bpm(energy: float) -> list[int]:
    return [60, 85] if energy < 0.35 else [85, 110] if energy < 0.6 else [105, 128] if energy < 0.8 else [120, 150]


def _captions(style: str, brief: dict) -> dict:
    if brief.get("content_type") in ("talking-head", "interview") and style == "none":
        style = "karaoke"
    cs = vocab("caption")[style]
    font = (cs.get("ass") or {}).get("Fontname") or "Cairo"
    return {"style": style, "font": font, "position": cs.get("position") or "lower",
            "fallback_fonts": _load("caption_styles.json")["font_fallback"]}


def _brief_context(job: Path) -> tuple[dict, dict | None]:
    brief = C.read(job, "brief")
    concept = None
    if (job / "concepts.json").exists():
        try:
            cj = C.read(job, "concepts")
            chosen = (cj.get("decision") or {}).get("chosen")
            concept = next((c for c in cj["concepts"] if c.get("id") == chosen), None) or (cj["concepts"] or [None])[0]
        except (C.ContractError, KeyError, ValueError):
            concept = None
    return brief, concept


def _target_energy(brief: dict, concept: dict | None) -> float:
    e = brief.get("energy")
    e = FEEL_ENERGY.get(brief.get("feeling"), 0.5) if e is None else float(e)
    rhythm = (concept or {}).get("rhythm")
    e += {"on-beat": 0.1, "slow-burn": -0.15, "speech-led": -0.03}.get(rhythm, 0.0)
    return round(max(0.0, min(1.0, e)), 2)


def _why(row: dict, brief: dict, energy: float, concept: dict | None, alts: list[dict], extra: str = "") -> str:
    f = brief.get("feeling")
    g = vocab("grade")[row["grade_id"]]
    bits = [f"اخترت «{row.get('name_ar') or row.get('name')}» ({row['id']}) من {SRC_AR.get(row['source'], row['source'])}"]
    if f in row["moods"]:
        bits.append(f"لأن إحساسه {FEEL_AR.get(f, f)} زي ما البريف عايز بالظبط")
    else:
        bits.append(f"إحساسه ({'، '.join(FEEL_AR.get(m, m) for m in row['moods'])}) قريب من {FEEL_AR.get(f, f)}")
    bits.append(f"وطاقته {row['energy']:.2f} قريبة من المطلوب {energy:.2f}")
    if brief.get("content_type") in row["content_types"]:
        bits.append(f"وبيمشي مع نوع المحتوى ({brief['content_type']})")
    hw = row.get("parts", {}).get("hint_words")
    if hw and concept:
        bits.append(f"وفيه كلمات من فكرة المفهوم {concept.get('id')}: {', '.join(hw)}")
    s = "، ".join(bits) + "."
    s += (f" اللون: «{g['name_ar']}» ({g['id']}) — {row.get('grade_why', '')}. "
          f"الانتقالات: {' / '.join(row['transition_ids'])}. الكاميرا: {' / '.join(row['camera_ids'])}. "
          f"الترجمة: {row['caption_style']}.")
    if alts:
        s += " البدايل اللي كانت قريبة: " + "، ".join(f"{a['id']} ({a['score']:.1f})" for a in alts[:3]) + "."
    return s + (" " + extra if extra else "")


def _apply_override(job: Path, look: dict) -> dict:
    """dm_mimic's look_override.json (a measured reference) wins for grade / transitions / camera."""
    f = job / "look_override.json"
    if not f.exists():
        return look
    try:
        ov = json.loads(f.read_text(encoding="utf-8"))
    except ValueError:
        return look
    applied = []
    gid = resolve("grade", (ov.get("grade") or {}).get("id"))
    if gid:
        look["grade"] = {**look["grade"], **{k: v for k, v in ov["grade"].items() if k != "id"}, "id": gid,
                         "engine": vocab("grade")[gid]["engine"]}
        applied.append("grade")
    trs = []
    for t in ov.get("transitions") or []:
        tid = resolve("transition", t.get("id") if isinstance(t, dict) else t)
        if tid:
            trs.append({**(t if isinstance(t, dict) else {}), "id": tid})
    if trs:
        look["transitions"] = trs
        applied.append("transitions")
    cams = []
    for c in ov.get("camera") or []:
        cid = resolve("camera", c.get("id") if isinstance(c, dict) else c)
        if cid:
            cams.append({**(c if isinstance(c, dict) else {}), "id": cid})
    if cams:
        look["camera"] = cams
        applied.append("camera")
    if applied:
        look["override"] = {"from": "look_override.json", "source": ov.get("style_source", "mimic"), "keys": applied}
        look["why"] += f" وبعدين طبّقت قياسات الفيديو المرجعي (look_override.json) على: {', '.join(applied)}."
    return look


def _kmx_ideas(job: Path, seed: int) -> list[dict]:
    if not KMX.is_file():
        return []
    try:
        res = C.run(job, STATION, "kmx.ideate", C.py(KMX) + ["ideate", "--count", "6", "--seed", str(seed)],
                    owner_media=False, check=False, timeout=120)
        if res.returncode != 0:
            return []
        return json.loads(res.stdout).get("ideas", [])
    except (ValueError, OSError, RuntimeError):
        return []


def invent(job: Path, brief: dict, ranked: list[dict], seed: int) -> tuple[dict, dict]:
    """Fuse a novel look from kmx ideate parents (atlas styles) — returns (pseudo-row, kmx record)."""
    by_slug = {r["source_style_id"]: r for r in ranked if r["source"] == "atlas86" and r.get("source_style_id")}
    best, best_s = None, None
    for idea in _kmx_ideas(job, seed):
        parents = [by_slug[p] for p in idea.get("parents", []) if p in by_slug]
        if len(parents) < 2:
            continue
        s = sum(p["score"] for p in parents) / len(parents) + 0.1 * float(idea.get("weight", 1))
        if best_s is None or s > best_s:
            best, best_s = (idea, parents), s
    if best:
        idea, parents = best
        rec = {"idea": idea, "parents": [p["id"] for p in parents], "fallback": False}
        sid = idea["id"]
    else:   # kmx missing or no idea mapped: fuse the top three styles from different sources ourselves
        parents, seen = [], set()
        for r in ranked:
            if r["source"] not in seen:
                parents.append(r)
                seen.add(r["source"])
            if len(parents) == 3:
                break
        sid = "KMX-local-%08x" % zlib.crc32("|".join(p["id"] for p in parents).encode())
        rec = {"idea": None, "parents": [p["id"] for p in parents], "fallback": True,
               "note": "kmx.py ideate unavailable or no parents matched the atlas; fused the top styles per source"}
    lead = max(parents, key=lambda p: p["score"])
    moods = []
    for p in parents:
        moods += [m for m in p["moods"] if m not in moods]
    pool_t, pool_c = [], []
    for p in sorted(parents, key=lambda p: -p["score"]):
        pool_t += [t for t in p["transition_ids"] if t not in pool_t]
        pool_c += [c for c in p["camera_ids"] if c not in pool_c]
    row = {"id": sid, "source": "kmx", "name": " × ".join(p.get("name") or p["id"] for p in parents),
           "name_ar": "دمج جديد: " + " × ".join(p.get("name") or p["id"] for p in parents),
           "moods": moods[:3], "energy": round(sum(p["energy"] for p in parents) / len(parents), 2),
           "content_types": lead["content_types"], "grade_id": lead["grade_id"],
           "grade_why": f"لون الأب الأقوى {lead['id']} ({lead.get('grade_why', '')})",
           "transition_ids": pool_t[:4], "camera_ids": pool_c[:3], "caption_style": lead["caption_style"],
           "score": round(sum(p["score"] for p in parents) / len(parents), 3), "parts": lead.get("parts", {})}
    return row, rec


def pick(job: Path, style: str | None = None, do_invent: bool = False, seed: int | None = None) -> dict:
    job = Path(job)
    brief, concept = _brief_context(job)
    feeling = brief.get("feeling") or "inspiring"
    energy = _target_energy(brief, concept)
    hint = " ".join(filter(None, [(concept or {}).get("style_hint"), (concept or {}).get("title"), brief.get("one_truth")]))
    ranked = rank(feeling, energy, brief.get("platform"), brief.get("content_type"), hint, brief.get("avoid"))
    extra = ""
    kmx_rec = None
    if style:
        row = next((r for r in ranked if r["id"] == style or r.get("slug") == style or r.get("source_style_id") == style), None)
        if row is None:
            raise SystemExit(f"dm_taste: style {style!r} not in taste_index (catalog/library500/atlas86 ids or slugs)")
        extra = "(الستايل ده انت اللي حددته بـ --style.)"
    elif do_invent:
        s = seed if seed is not None else zlib.crc32((brief.get("task") or "").encode()) % 100000
        row, kmx_rec = invent(job, brief, ranked, s)
        extra = ("ده ستايل مخترع: دمجت آباء من أفكار kmx ideate (حالتها PROPOSED، متجربتش قبل كده)."
                 if not kmx_rec["fallback"] else "kmx مش متاح فدمجت أحسن ستايل من كل مصدر.")
    else:
        row = ranked[0]
    alts = [r for r in ranked if r["id"] != row["id"]][:5]
    g = vocab("grade")[row["grade_id"]]
    look = C.new("look",
                 style_id=row["id"], style_source=row["source"],
                 style_name=row.get("name"), style_ref=row.get("ref"),
                 grade={"id": g["id"], "engine": g["engine"], "lut": None},
                 transitions=_transitions(row["transition_ids"]),
                 camera=_camera(row["camera_ids"]),
                 captions=_captions(row["caption_style"], brief),
                 music={"mood": feeling, "bpm_range": _bpm(energy)},
                 why=_why(row, brief, energy, concept, alts, extra),
                 fit={"score": row.get("score"), "parts": row.get("parts"), "target_energy": energy,
                      "feeling": feeling, "concept": (concept or {}).get("id")},
                 alternatives=[{"id": a["id"], "source": a["source"], "name": a.get("name"), "score": a["score"]} for a in alts],
                 matrix_atoms=sorted({a for t in row["transition_ids"] for a in vocab("transition")[t].get("matrix_atoms", [])}
                                     | {a for c in row["camera_ids"] for a in vocab("camera")[c].get("matrix_atoms", [])}))
    if kmx_rec:
        look["kmx"] = kmx_rec
    look = _apply_override(job, look)
    C.write(job, "look", look)
    return look


# ---------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--job", required=True)
    p.add_argument("--style")
    p.add_argument("--invent", action="store_true")
    p.add_argument("--seed", type=int)
    q = sub.add_parser("query")
    q.add_argument("--feeling", required=True, choices=list(FEEL_AR))
    q.add_argument("--platform")
    q.add_argument("--content")
    q.add_argument("--energy", type=float)
    q.add_argument("--hint", default="")
    q.add_argument("--top", type=int, default=5)
    q.add_argument("--json", action="store_true")
    f = sub.add_parser("filter")
    f.add_argument("kind", choices=["grade", "transition", "camera"])
    f.add_argument("id")
    f.add_argument("--W", type=int, default=1080)
    f.add_argument("--H", type=int, default=1920)
    f.add_argument("--fps", type=float, default=30)
    f.add_argument("--seconds", type=float, default=2.0)
    a = ap.parse_args(argv)
    if a.cmd == "pick":
        look = pick(Path(a.job), a.style, a.invent, a.seed)
        print(json.dumps({k: look[k] for k in ("style_id", "style_source", "grade", "transitions", "camera", "captions")},
                         ensure_ascii=False))
        print(look["why"])
        return 0
    if a.cmd == "query":
        rows = rank(a.feeling, a.energy, a.platform, a.content, a.hint, top=a.top)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
            return 0
        for r in rows:
            print(f"{r['score']:5.2f}  {r['id']:28} {r['source']:10} {str(r.get('name'))[:34]:34} "
                  f"moods={','.join(r['moods'])} e={r['energy']} grade={r['grade_id']} "
                  f"tr={','.join(r['transition_ids'])} cam={','.join(r['camera_ids'])} cap={r['caption_style']}")
        return 0
    if a.kind == "grade":
        print(grade_filter(a.id))
    elif a.kind == "transition":
        print(transition_filter(a.id, max(0.0, a.seconds - 0.5)) or "cut")
    else:
        print(camera_filter(a.id, a.W, a.H, a.fps, a.seconds))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
