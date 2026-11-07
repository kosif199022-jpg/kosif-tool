#!/usr/bin/env python3
"""Station «يوريك الشكل قبل ما ينفّذ» (preview for approval): after the director writes edl.json and before
anything is rendered, draw what the edit will look like so the owner can say yes or ask for changes.

Writes into the job folder:
  preview/storyboard.jpg  one frame per cut, cropped to the delivery aspect, with a timeline strip on top
                          (each cut's width = its length, coloured by its role) and a label under each frame
  preview/PLAN_AR.md      the plan in Egyptian Arabic: chosen concept, look, and the movement matrix
                          (مصفوفة التحركات): time, source, role, camera move, transition, words, reason
  preview/plan.json       the same matrix as data (kosif.dm.plan.v1)
  preview/animatic.mp4    only with --animatic: a fast low-resolution draft render of the same EDL

  dm_storyboard.py storyboard --job DIR [--cols 6] [--animatic]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402
import dm_edl  # noqa: E402

STATION = "storyboard"
ROLE_AR = {"hook": "خطّاف", "setup": "تمهيد", "journey": "رحلة", "turn": "تحوّل", "climax": "ذروة",
           "outro": "نهاية", "payoff": "النتيجة", "proof": "دليل", "problem": "المشكلة", "solution": "الحل",
           "cta": "دعوة للفعل", "context": "سياق", "broll": "لقطة مساعدة", "speech": "كلام"}
ROLE_RGB = {"hook": (230, 57, 70), "climax": (244, 162, 97), "turn": (233, 196, 106), "outro": (42, 157, 143),
            "cta": (42, 157, 143), "payoff": (244, 162, 97)}


def frame(src: str, t: float, w: int, h: int, dst: Path) -> bool:
    if not C.have("ffmpeg"):
        return False
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0.0, t):.3f}", "-i", src, "-frames:v", "1",
                        "-vf", vf, "-q:v", "3", str(dst)], capture_output=True, timeout=120)
    return r.returncode == 0 and dst.exists()


def words_in(clip: dict, a: float, b: float) -> str:
    ws = [w for w in clip.get("words") or [] if float(w.get("start", 0)) >= a - 0.05 and float(w.get("end", 0)) <= b + 0.05]
    txt = " ".join(str(w.get("w", "")).strip() for w in ws).strip()
    return (txt[:60] + "…") if len(txt) > 60 else txt


def matrix(job: Path) -> dict:
    edl = dm_edl.reflow(json.loads(json.dumps(C.read(job, "edl"))))
    analysis = C.read(job, "analysis")
    clips = {c["id"]: c for c in analysis.get("clips", [])}
    rows = []
    for ev in edl["events"]:
        secs = dm_edl.event_seconds(ev)
        clip = clips.get(ev.get("clip"), {})
        rows.append({
            "id": ev["id"], "rec_in": round(ev["rec_in"], 2), "rec_out": round(ev["rec_in"] + secs, 2),
            "clip": ev.get("clip"), "src": Path(str(clip.get("path", ""))).name,
            "src_in": ev["src_in"], "src_out": ev["src_out"], "role": ev.get("role") or ev.get("kind") or "",
            "kind": ev.get("kind") or "", "camera": (ev.get("camera") or {}).get("id", "static"),
            "transition": (ev.get("transition_in") or {}).get("id", "cut"), "speed": ev.get("speed", 1.0),
            "grade": (ev.get("grade") or {}).get("id") if isinstance(ev.get("grade"), dict) else ev.get("grade"),
            "mute": bool(ev.get("mute")), "words": words_in(clip, ev["src_in"], ev["src_out"]),
            "reason": str(ev.get("reason", "")),
        })
    return {"schema": "kosif.dm.plan.v1", "width": edl["width"], "height": edl["height"], "fps": edl["fps"],
            "duration": edl["duration"], "grade": (edl.get("grade") or {}).get("id"),
            "captions": edl.get("captions"), "music": ((edl.get("audio") or {}).get("music") or {}).get("path"),
            "rows": rows, "status": "awaiting_owner_approval"}


def sheet(job: Path, plan: dict, cols: int) -> Path | None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    analysis = C.read(job, "analysis")
    paths = {c["id"]: c["path"] for c in analysis.get("clips", [])}
    W, H = plan["width"], plan["height"]
    tw = 200
    th = max(60, round(tw * H / W))
    tmp = job / "preview" / "frames"
    tmp.mkdir(parents=True, exist_ok=True)
    rows = plan["rows"]
    n = len(rows)
    cols = max(1, min(cols, n))
    nrows = (n + cols - 1) // cols
    pad, label_h, strip_h = 10, 44, 46
    img = Image.new("RGB", (pad + cols * (tw + pad), strip_h + pad + nrows * (th + label_h + pad)), (18, 18, 22))
    d = ImageDraw.Draw(img)
    font = None
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "Arial.ttf", "arial.ttf"):
        try:
            font = ImageFont.truetype(name, 12)       # labels are Latin; the Arabic lives in PLAN_AR.md
            break
        except OSError:
            continue
    font = font or ImageFont.load_default()
    total = max(plan["duration"], 0.01)
    x0, x1 = pad, img.width - pad
    for r in rows:                             # timeline strip: width = length, colour = role
        a = x0 + (x1 - x0) * r["rec_in"] / total
        b = x0 + (x1 - x0) * min(r["rec_out"], total) / total
        d.rectangle([a, 8, max(a + 1, b - 1), 30], fill=ROLE_RGB.get(r["role"], (90, 110, 140)))
        d.text((a + 2, 12), r["id"][1:], fill=(255, 255, 255), font=font)
    d.text((x0, 32), f"0s  ->  {plan['duration']:.1f}s   {W}x{H}  grade={plan['grade']}", fill=(170, 170, 180), font=font)
    for i, r in enumerate(rows):
        cx, cy = pad + (i % cols) * (tw + pad), strip_h + pad + (i // cols) * (th + label_h + pad)
        f = tmp / f"{r['id']}.jpg"
        mid = (r["src_in"] + r["src_out"]) / 2
        if r["clip"] in paths and frame(paths[r["clip"]], mid, tw, th, f):
            img.paste(Image.open(f).convert("RGB"), (cx, cy))
        else:
            d.rectangle([cx, cy, cx + tw, cy + th], outline=(90, 90, 90))
        d.rectangle([cx, cy, cx + tw, cy + 4], fill=ROLE_RGB.get(r["role"], (90, 110, 140)))
        d.text((cx, cy + th + 3), f"#{i + 1} {r['rec_in']:.1f}-{r['rec_out']:.1f}s  {r['role']}", fill=(235, 235, 235), font=font)
        d.text((cx, cy + th + 21), f"cam:{r['camera']}  in:{r['transition']}", fill=(160, 200, 255), font=font)
    out = job / "preview" / "storyboard.jpg"
    img.save(out, quality=88)
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def arabic_reason(reason: str) -> str:
    """Reasons are "en | ar; en | ar": keep every Arabic part (the shot's reason and the transition's)."""
    parts = [p.strip() for chunk in reason.split("|") for p in chunk.split(";")]
    ar = [p for p in parts if re.search(r"[\u0600-\u06FF]", p)]
    return ("؛ ".join(ar) or reason).replace("|", "/")[:160]


def plan_md(job: Path, plan: dict, board: Path | None) -> str:
    concepts = C.read(job, "concepts")
    chosen = concepts["decision"]["chosen"]
    con = next((c for c in concepts["concepts"] if c.get("id") == chosen), concepts["concepts"][0])
    look = C.read(job, "look")
    brief = C.read(job, "brief")
    cap = plan.get("captions") or {}
    L = ["# الشكل التقريبي قبل التنفيذ", "",
         "> ده اللي التنين ناوي يعمله. **مفيش رندر نهائي لحد ما توافق.** قول «موافق» أو قول تعديلك "
         "(مثلاً: «ابدأ بلقطة 3»، «شيل الزووم»، «خليه أسرع»، «ستايل تاني»).", "",
         f"- **الطلب:** {brief.get('task', '')}",
         f"- **المقاس والمدة:** {plan['width']}×{plan['height']} · {plan['fps']} fps · {plan['duration']:.1f} ث "
         f"(المطلوب {brief.get('target_seconds', '?')} ث)",
         f"- **الفكرة المختارة ({chosen}):** {con.get('title', '')} — {con.get('logline', '')}",
         f"- **ليه الفكرة دي:** {str(concepts['decision'].get('why', ''))[:300]}",
         f"- **الستايل:** {look.get('style_name', '')} (`{look.get('style_id', '')}`) · اللون: `{plan.get('grade')}`",
         f"- **الكابشن:** {'شغّال، ستايل ' + str(cap.get('style')) if cap.get('enabled') else 'مقفول'} · "
         f"**المزيكا:** {Path(plan['music']).name if plan.get('music') else 'من غير'}", ""]
    alts = [c for c in concepts["concepts"] if c.get("id") != chosen]
    if alts:
        L += ["**أفكار تانية ممكن تختارها بدالها:** " + " · ".join(f"{c['id']}: {c.get('title', '')}" for c in alts), ""]
    if board:
        L += ["![الستوري بورد](storyboard.jpg)", "", "_الشريط اللي فوق: كل مستطيل قطعة، عرضه = طولها، ولونه = دورها._", ""]
    L += ["## مصفوفة التحركات", "",
          "| # | الوقت | من فين | الدور | حركة الكاميرا | الانتقال | الكلام | ليه |",
          "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(plan["rows"], 1):
        why = arabic_reason(r["reason"])
        L.append(f"| {i} | {r['rec_in']:.1f}–{r['rec_out']:.1f} | {r['src']} {r['src_in']:.1f}–{r['src_out']:.1f} "
                 f"| {ROLE_AR.get(r['role'], r['role'])} | {r['camera']} | {r['transition']} "
                 f"| {r['words'].replace('|', '/') or '—'} | {why} |")
    L += ["", "بعد موافقتك: `dragon_montage.py go --job <المجلد>` يرندر ويراجع ويصلّح (لحد 3 جولات)."]
    return "\n".join(L) + "\n"


def cmd_storyboard(a) -> int:
    job = C.job_dir(a.job)
    (job / "preview").mkdir(exist_ok=True)
    plan = matrix(job)
    board = sheet(job, plan, a.cols)
    plan["storyboard"] = "preview/storyboard.jpg" if board else None
    if a.animatic:
        r = subprocess.run([sys.executable, str(HERE / "dm_render.py"), "render", "--job", str(job), "--preview"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        prev = job / "render" / "preview.mp4"
        if r.returncode == 0 and prev.exists():
            shutil.copy2(prev, job / "preview" / "animatic.mp4")
            plan["animatic"] = "preview/animatic.mp4"
    (job / "preview" / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (job / "preview" / "PLAN_AR.md").write_text(plan_md(job, plan, board), encoding="utf-8")
    print(json.dumps({"plan": str(job / "preview" / "PLAN_AR.md"), "storyboard": str(board) if board else None,
                      "animatic": str(job / plan["animatic"]) if plan.get("animatic") else None,
                      "cuts": len(plan["rows"]), "duration": plan["duration"]}, ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    C.utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("storyboard")
    s.add_argument("--job", required=True)
    s.add_argument("--cols", type=int, default=6)
    s.add_argument("--animatic", action="store_true", help="also render a fast low-res draft (preview/animatic.mp4)")
    a = p.parse_args(argv)
    return cmd_storyboard(a)


if __name__ == "__main__":
    raise SystemExit(main())
