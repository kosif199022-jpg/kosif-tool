"""Font matching: which available Arabic font reproduces the reference text best?

For each text event and line: the reference ink mask (from the analysis crop) is compared with the same
text rendered in every library face — aspect ratio, tolerant overlap (IoU) and stroke thickness.
Writes the ranking into spec.texts[i].font and a comparison sheet (reference vs top candidates).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import mm_fonts_lib
import mm_img
import mm_render_text as RT
import mm_sheets
from mm_common import has_arabic, log, rnd, save_json, strip_harakat, work_paths

NORM_H = 64


def _tight(mask: np.ndarray):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def _stroke(mask: np.ndarray) -> float:
    if mask.sum() < 10:
        return 0.0
    try:
        if mm_img.HAVE_CV2:
            dt = mm_img.cv2.distanceTransform(mask.astype(np.uint8), mm_img.cv2.DIST_L2, 3)
        else:
            from scipy.ndimage import distance_transform_edt
            dt = distance_transform_edt(mask)
        # ridge values ≈ half stroke width
        ridge = dt[(dt >= mm_img.dilate(dt.astype(np.float32), 1) - 1e-3) & mask]
        return float(np.median(ridge) * 2) if ridge.size else 0.0
    except Exception:
        return 0.0


def signature(mask: np.ndarray) -> dict | None:
    t = _tight(mask.astype(bool))
    if t is None or t.shape[0] < 4:
        return None
    h, w = t.shape
    nw = max(8, int(round(w * NORM_H / h)))
    norm = mm_img.resize(t.astype(np.uint8) * 255, (nw, NORM_H), "area") > 100
    return {"aspect": w / h, "norm": norm, "stroke": _stroke(t) / h, "h": h, "w": w,
            "rows": t.mean(1), "cols": t.mean(0)}


def similarity(ref: dict, cand: dict) -> tuple[float, dict]:
    a = float(np.exp(-abs(np.log(ref["aspect"] / max(1e-6, cand["aspect"]))) * 5.0))
    # force the candidate into the reference box (non-uniform) → tolerant IoU
    R = ref["norm"]
    C = mm_img.resize(cand["norm"].astype(np.uint8) * 255, (R.shape[1], R.shape[0]), "area") > 100
    Rd, Cd = mm_img.dilate(R, 1), mm_img.dilate(C, 1)
    inter = (R & Cd).sum() + (C & Rd).sum()
    tot = R.sum() + C.sum()
    iou = float(inter / max(1, tot))
    # vertical ink profile (where dots, ascenders and descenders sit)
    rp = np.interp(np.linspace(0, 1, 32), np.linspace(0, 1, len(ref["rows"])), ref["rows"])
    cp = np.interp(np.linspace(0, 1, 32), np.linspace(0, 1, len(cand["rows"])), cand["rows"])
    prof = float(max(0.0, np.corrcoef(rp, cp)[0, 1])) if rp.std() > 0 and cp.std() > 0 else 0.5
    s = float(np.exp(-abs(np.log(max(1e-3, ref["stroke"]) / max(1e-3, cand["stroke"]))) * 2.5))
    score = iou ** 1.6 * a ** 0.7 * s ** 0.6 * (0.6 + 0.4 * prof)
    return score, {"iou": rnd(iou, 3), "aspect": rnd(a, 3), "stroke": rnd(s, 3), "profile": rnd(prof, 3)}


def line_mask(work: Path, ev: dict, li: int) -> np.ndarray | None:
    try:
        p = work / ev["crops"]["lines"][li]
    except (KeyError, IndexError):
        return None
    im = np.asarray(Image.open(p).convert("L"))
    return im < 128


def match(work: str, families: list[str] | None = None, top: int = 6, engine: str = "auto",
          extra_dirs: list[str] | None = None, include_system: bool = True) -> dict:
    P = work_paths(work)
    from mm_common import load_json
    spec = load_json(P["spec"])
    lib = mm_fonts_lib.library([P["root"] / "fonts"] + [Path(d) for d in (extra_dirs or [])], include_system)
    if families:
        fam_l = [f.lower() for f in families]
        lib = [e for e in lib if any(f in e["family"].lower() for f in fam_l)]
    log(f"font library: {len(lib)} faces")
    sheets = []
    for ev in spec["texts"]:
        lines = ev.get("lines") or []
        scores: dict[str, list] = {}
        details: dict[str, dict] = {}
        used = 0
        for li, ln in enumerate(lines):
            text = (ln.get("text") or "").strip() or (ln.get("ocr") or "").strip()
            if not text or not has_arabic(text) and not any(c.isalpha() for c in text):
                continue
            m = line_mask(P["root"], ev, li)
            if m is None:
                continue
            ref = signature(m)
            if ref is None:
                continue
            used += 1
            for e in lib:
                try:
                    L = RT.render_line(text, e["path"], 96, engine)
                except Exception:
                    continue
                cand = signature(L.alpha > 0.5)
                if cand is None:
                    continue
                s, d = similarity(ref, cand)
                key = e["path"]
                scores.setdefault(key, []).append(s)
                details.setdefault(key, {"entry": e, "parts": []})["parts"].append(d)
        if not scores:
            ev["font"]["note"] = "no line text yet: fill spec.texts[].lines[].text (or keep OCR) and rerun"
            continue
        ranked = sorted(scores.items(), key=lambda kv: -float(np.mean(kv[1])))
        cands = []
        for path, ss in ranked[:top]:
            e = details[path]["entry"]
            cands.append({"family": e["family"], "weight": e["weight"], "style": e["style"], "file": Path(path).name,
                          "path": path, "source": e["source"], "score": rnd(float(np.mean(ss)), 4),
                          "parts": details[path]["parts"]})
        ev["font"]["candidates"] = cands
        if not ev["font"].get("locked"):
            ev["font"]["chosen"] = cands[0]["path"]
        best = cands[0]["score"]
        ev["font"]["confidence"] = "high" if best > 0.55 else ("medium" if best > 0.4 else "low")
        sheets.append(font_sheet(P, ev, cands))
    # events without their own match borrow the most common choice
    chosen = [e["font"].get("chosen") for e in spec["texts"] if e["font"].get("chosen")]
    if chosen:
        common = max(set(chosen), key=chosen.count)
        for e in spec["texts"]:
            if not e["font"].get("chosen"):
                e["font"]["chosen"] = common
                e["font"]["note"] = "borrowed from the other events (no readable line text)"
    save_json(P["spec"], spec)
    return {"sheets": [str(s) for s in sheets], "events": len(spec["texts"])}


def font_sheet(P: dict, ev: dict, cands: list[dict]) -> Path:
    W = 760
    rows = []
    ref_path = P["root"] / ev["crops"]["zone"]
    ref = Image.open(ref_path).convert("RGB")
    rows.append(("REFERENCE", ref))
    for c in cands:
        imgs = []
        for ln in ev["lines"]:
            text = (ln.get("text") or "").strip() or (ln.get("ocr") or "").strip()
            if not text:
                continue
            target = max(10, ln["ink_h"])
            try:
                size, L = RT.fit_size(text, c["path"], target)
            except Exception:
                continue
            a = (L.alpha * 255).astype(np.uint8)
            img = Image.new("RGB", (a.shape[1], a.shape[0]), (24, 24, 30))
            img.paste((250, 250, 250), (0, 0), Image.fromarray(a))
            imgs.append(img)
        if not imgs:
            continue
        hh = sum(i.height for i in imgs) + 6 * (len(imgs) - 1)
        ww = max(i.width for i in imgs)
        block = Image.new("RGB", (ww, hh), (24, 24, 30))
        y = 0
        for i in imgs:
            block.paste(i, ((ww - i.width) // 2, y))
            y += i.height + 6
        rows.append((f"{c['family']} {c['weight']}  score {c['score']}", block))
    total_h = 0
    fitted = []
    for lab, im in rows:
        s = min(1.0, (W - 20) / im.width)
        im2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        fitted.append((lab, im2))
        total_h += im2.height + 30
    sheet = Image.new("RGB", (W, total_h + 10), (18, 18, 22))
    d = ImageDraw.Draw(sheet)
    y = 6
    for lab, im in fitted:
        mm_sheets.draw_text(d, (10, y), lab, 15, (255, 220, 140) if lab == "REFERENCE" else (230, 230, 235))
        sheet.paste(im, ((W - im.width) // 2, y + 22))
        y += im.height + 30
    out = P["sheets"] / f"fonts_ev{ev['id']:02d}.png"
    sheet.save(out)
    return out
