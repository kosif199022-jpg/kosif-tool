#!/usr/bin/env python3
"""Regenerate every derived file of the atlas from catalog/styles.json.

Writes: styles/<id>/SKILL.md (all), STYLE_INDEX.md, catalog/playbooks.json,
catalog/meta.json, sitemap.xml and the statistics block in README.md.
Run after tools/sync_catalog.py or tools/import_briefs.py.

  python3 tools/build.py            # regenerate everything
  python3 tools/build.py --check    # exit 1 if any derived file would change (CI)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://kosif199022-jpg.github.io/kosif-tool"
REPO = "https://github.com/kosif199022-jpg/kosif-tool"

TACTICS = {
    "product-ui": "Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.",
    "phone": "Use 3D or 2.5D phone layers with believable screen perspective, shadow, touch interaction, device rotation and safe crops.",
    "charts": "Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.",
    "diagrams": "Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.",
    "kinetic-type": "Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.",
    "shapes": "Build a geometric system; morph only compatible paths; animate scale, squash and stretch, rotation and easing with controlled geometry.",
    "particles": "Use deterministic seeded particles with explicit emitters, fields, attraction and decay that carry story meaning, not decoration.",
    "characters": "Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.",
    "photos": "Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.",
    "music": "Cut and accent on measured beats; keep narration intelligible; duck music under voice; deliver at -14 LUFS.",
    "code": "Write genuine time-varying vector, Canvas, React or WebGL motion; seed all randomness; never a slideshow of stills.",
    "hand-drawn": "Order stroke draw-on like a human hand would; keep imperfection deliberate; pace reveals to narration.",
    "3d": "Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.",
    "ads": "Hook in the first second; one feature per beat; clear price or call-to-action card; brand-consistent logo reveal.",
}


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def playbook_meta(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    title = m.group(1).strip() if m else path.stem
    if " — " in title:
        en, ar = title.split(" — ", 1)
    else:
        en, ar = title, title
    body = re.sub(r"^#.*$", "", text, count=1, flags=re.M).strip()
    para = next((p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not p.strip().startswith("#")), "")
    excerpt = re.sub(r"\s+", " ", para)[:240]
    words = len(re.findall(r"[A-Za-z]{2,}", text))
    return {"key": path.stem, "title_en": en.strip(), "title_ar": ar.strip(), "path": f"playbooks/{path.name}", "excerpt": excerpt, "words_en": words}


def skill_md(r: dict, cats: dict, briefs: dict) -> str:
    keys = r.get("category") or []
    labels = ", ".join(f"{cats[k]['en']} / {cats[k]['ar']}" for k in keys if k in cats) or "creative motion"
    playbooks = [cats[k]["playbook"] for k in keys if k in cats and (ROOT / cats[k]["playbook"]).exists()]
    tactics = "\n".join(f"* {TACTICS[k]}" for k in keys if k in TACTICS) or "* Develop original choreography from the reference; verify imagery before claiming a match."
    b = briefs.get(r["id"])
    name_ar = r.get("name_ar") or ""
    title = f"{r['name']}" + (f" / {name_ar}" if name_ar and name_ar != r["name"] else "")
    desc = r.get("summary_en") or "Create a new video using the motion design language referenced at this catalog entry."
    ref = [f"- Page: {r.get('page')}",
           f"- Video: {r.get('video') or 'see source page'}",
           f"- Credit: {r.get('creator', 'unknown')}" + (f" ({r['creator_url']})" if r.get("creator_url") else ""),
           f"- Source type: {r.get('type')} · Origin: {r.get('origin')}"]
    if r.get("published"):
        ref.append(f"- Published on source: {r['published']}" + (f" · credited model: {r['model']}" if r.get("model") else "") + (f" · effort: {r['effort']}" if r.get("effort") else ""))
    if r.get("aspect_label"):
        ref.append(f"- Reference aspect: {r['aspect_label']} ({r['aspect']['w']}×{r['aspect']['h']})")
    if r.get("tech"):
        ref.append(f"- Technologies named by the source: {', '.join(r['tech'])}")
    if r.get("source_prompt_words"):
        ref.append(f"- Creator's public prompt length: about {r['source_prompt_words']} words (not reproduced here)")
    if r.get("rank"):
        ref.append(f"- Popularity rank on source library: #{r['rank']}")
    brief_block = ""
    if b:
        brief_block = f"""
## Creative brief (الملف الإبداعي)
{b['summary_ar']}

{b['summary_en']}

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack ({', '.join(b.get('stack') or []) or '—'}), suggested duration ({b.get('duration_s') if b.get('duration_s') is not None else 'per material'} s), aspect {b['aspect']}, difficulty {b['difficulty']}/5.
"""
    pb_block = "\n".join(f"- [{p}](../../{p})" for p in playbooks) or "- (no category playbook yet)"
    return f"""---
name: {r['id']}
description: {desc}
---

# KOSIF TOOL — {title}

## Primary motion reference (المرجع)
{chr(10).join(ref)}

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.
{brief_block}
## Categories and playbooks (التصنيفات والدلائل)
Categories: {labels}.
{pb_block}

Category tactics:
{tactics}

## Original creative direction (التوجيه الإبداعي)
Produce a NEW video from the user's own concept, voice or footage, inspired by this reference.
* Start from a consistent geometry system and original design tokens; document measured versus estimated colors, type, line weights, easing and camera in STYLE.md.
* Give every scene an audio interval and a visual action. Plan creation order, camera movement, transition and sound cue at sentence or phrase granularity in PLAN.md.
* Everything animates: paths draw in sequence, rigs move, information is revealed causally. Static slideshow transitions are not acceptable.
* Build editable, deterministic animation with Remotion/React, SVG/Canvas (see starters/html-canvas) or Three.js for true spatial scenes; render with tools/render_html.cjs or Remotion. Never imply integrations that are not installed.
* Default 9:16, 1080×1920, 30 fps, H.264 MP4 with AAC audio. Respect the user's aspect ratio, duration, branding and timeline.
* Existing AUDIO is master time: keep the voice untouched, transcribe, align words and animate to verified timestamps; aim for ≤ 100 ms on key words and check it.
* For source VIDEO, preserve the authorized material and align the treatment to real cuts, actions and phrases. For TEXT, write short narration and a timestamped scene plan.
* Arabic needs RTL shaping and phone-safe typography; never split joined letters to animate them (see playbooks/arabic-typography.md).
* Entrances 250–600 ms, accents 120–300 ms, transitions 300–800 ms as first estimates; refine after inspecting the reference.
* Preserve legibility, hierarchy, emotional pacing and performance.

## Claude production runbook (خطوات الإنتاج)
1. Read CLAUDE.md, AGENTS.md, this skill, STYLE.json, BRIEF.md (if present) and the playbooks above.
2. Open the source page and inspect the video where possible; never copy it into this repository.
3. Gather the user's assets; ask at most one batch of necessary questions.
4. `python3 tools/kosif.py scaffold {r['id']} <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    records = load_json(ROOT / "catalog" / "styles.json")
    cats = {c["key"]: c for c in load_json(ROOT / "catalog" / "categories.json")}
    briefs_p = ROOT / "catalog" / "briefs.json"
    briefs = load_json(briefs_p) if briefs_p.exists() else {}
    outputs: dict[Path, str] = {}

    for r in records:
        outputs[ROOT / "styles" / r["id"] / "SKILL.md"] = skill_md(r, cats, briefs)
        r["skill"] = f"styles/{r['id']}/SKILL.md"
        r["playbooks"] = [cats[k]["playbook"] for k in (r.get("category") or []) if k in cats and (ROOT / cats[k]["playbook"]).exists()]
        if r.get("brief") and not (ROOT / r["brief"]).exists():
            r["brief"] = None

    # STYLE_INDEX.md grouped by category
    lines = ["# KOSIF TOOL Style Index", "", "Use IDs verbatim when addressing Claude. Each entry links its SKILL.md, the original reference and, when present, the KOSIF creative brief.", "",
             f"Total: {len(records)} styles · {sum(1 for r in records if r['origin']=='PromptsMotion')} PromptsMotion references · {sum(1 for r in records if r['origin']!='PromptsMotion')} KOSIF base styles · {sum(1 for r in records if r.get('brief'))} with briefs.", ""]
    lines += ["## Playbooks", ""]
    for p in sorted(x for x in (ROOT / "playbooks").glob("*.md") if x.name.lower() != "readme.md"):
        m = playbook_meta(p)
        if m:
            lines.append(f"- [{m['title_en']} — {m['title_ar']}]({m['path']})")
    lines.append("")
    by_cat: dict[str, list] = {k: [] for k in cats}
    by_cat["uncategorized"] = []
    for r in records:
        keys = r.get("category") or ["uncategorized"]
        for k in keys:
            by_cat.setdefault(k, []).append(r)
    for k, rs in by_cat.items():
        if not rs:
            continue
        label = f"{cats[k]['en']} / {cats[k]['ar']}" if k in cats else "Uncategorized / بدون تصنيف"
        lines += [f"## {label} ({len(rs)})", ""]
        for r in sorted(rs, key=lambda x: (x["origin"] != "KOSIF original style", x.get("rank") or 10_000, x["id"])):
            name = r["name"] + (f" · {r['name_ar']}" if r.get("name_ar") and r["name_ar"] != r["name"] else "")
            extra = f" — [brief]({r['brief']})" if r.get("brief") else ""
            lines.append(f"- [{r['id']}]({r['skill']}) — {name} — [reference]({r['page']}){extra}")
        lines.append("")
    outputs[ROOT / "STYLE_INDEX.md"] = "\n".join(lines).rstrip() + "\n"

    pbs = [m for m in (playbook_meta(p) for p in sorted(x for x in (ROOT / "playbooks").glob("*.md") if x.name.lower() != "readme.md")) if m]
    outputs[ROOT / "catalog" / "playbooks.json"] = json.dumps(pbs, ensure_ascii=False, indent=1) + "\n"

    meta = {
        "total": len(records),
        "promptsmotion": sum(1 for r in records if r["origin"] == "PromptsMotion"),
        "base": sum(1 for r in records if r["origin"] != "PromptsMotion"),
        "with_briefs": sum(1 for r in records if r.get("brief")),
        "playbooks": len(pbs),
        "categories": dict(Counter(c for r in records for c in (r.get("category") or []))),
        "types": dict(Counter(r.get("type") for r in records)),
        "aspects": dict(Counter(r.get("aspect_label") or "unknown" for r in records)),
        "creators": len({r["creator"] for r in records if r["origin"] == "PromptsMotion"}),
        "latest_published": max((r.get("published") or "" for r in records), default=None) or None,
    }
    outputs[ROOT / "catalog" / "meta.json"] = json.dumps(meta, ensure_ascii=False, indent=1) + "\n"

    urls = [f"{SITE}/", f"{SITE}/#/generator", f"{SITE}/#/playbooks", f"{SITE}/#/guide"] + [f"{SITE}/#/style/{r['id']}" for r in records]
    outputs[ROOT / "sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"

    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        block = (f"<!-- stats:start -->\n**{meta['total']}** styles · **{meta['promptsmotion']}** PromptsMotion references · **{meta['base']}** KOSIF base styles · "
                 f"**{meta['with_briefs']}** original briefs · **{meta['playbooks']}** playbooks · **{meta['creators']}** credited creators\n<!-- stats:end -->")
        if "<!-- stats:start -->" in text:
            text = re.sub(r"<!-- stats:start -->.*?<!-- stats:end -->", block, text, flags=re.S)
            outputs[readme] = text

    outputs[ROOT / "catalog" / "styles.json"] = json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    outputs[ROOT / "catalog" / "prompts_motion.json"] = json.dumps([r for r in records if r["origin"] == "PromptsMotion"], ensure_ascii=False, indent=2) + "\n"
    for r in records:
        outputs[ROOT / "styles" / r["id"] / "STYLE.json"] = json.dumps(r, ensure_ascii=False, indent=2) + "\n"

    changed = []
    for path, content in outputs.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != content:
            changed.append(path)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    if args.check:
        if changed:
            print("derived files out of date:", *[str(p.relative_to(ROOT)) for p in changed[:20]], sep="\n  ")
            return 1
        print("derived files up to date")
        return 0
    print(f"regenerated {len(changed)} files ({len(records)} styles, {len(pbs)} playbooks, {meta['with_briefs']} briefs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
