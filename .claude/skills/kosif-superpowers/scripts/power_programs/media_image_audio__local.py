"""Local programs for media-image-audio cards that need an installed model (env_scope=local)."""
from __future__ import annotations
from pathlib import Path
from ._mind_common import save, eq, truth
from . import _local_models as L


def media25(work):
    """Local Arabic STT with word timestamps on CPU (int8): planted Piper line round trip."""
    wav = Path(work) / "speech.wav"
    secs, _, _ = L.piper_say(L.LINE_AR, wav)
    words, info = L.transcribe_words(L.whisper("small"), wav, "ar")
    save(work, "words.json", words)
    return [eq("language", info.language, "ar"),
            truth("planted words heard >= 80%", L.word_match(L.LINE_AR.split(), [w["w"] for w in words]) >= 0.8,
                  [w["w"] for w in words]),
            truth("word timestamps present", all("start" in w and "end" in w for w in words))]


def media27(work):
    """Background removal with rembg (U2Net, local): a planted subject on a busy background.
    Known answer: the alpha mask covers the planted disc and drops the background."""
    import os
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    os.environ.setdefault("U2NET_HOME", str(L.CACHE / "u2net"))
    from rembg import remove, new_session
    work = Path(work)
    rng = np.random.default_rng(7)
    bg = (rng.integers(90, 140, (512, 512, 3))).astype("uint8")
    img = Image.fromarray(bg).filter(ImageFilter.GaussianBlur(1.5))
    d = ImageDraw.Draw(img)
    d.ellipse([156, 136, 356, 376], fill=(200, 30, 40))  # the subject
    d.ellipse([216, 196, 296, 276], fill=(250, 220, 60))
    img.save(work / "in.png")
    out = remove(img, session=new_session("u2net"))
    out.save(work / "cutout.png")
    a = np.array(out)[:, :, 3] > 128
    truth_mask = np.zeros((512, 512), bool)
    yy, xx = np.ogrid[:512, :512]
    truth_mask[((xx - 256) / 100) ** 2 + ((yy - 256) / 120) ** 2 <= 1] = True
    inter, union = (a & truth_mask).sum(), (a | truth_mask).sum()
    iou = inter / max(1, union)
    save(work, "mask_check.json", {"iou": round(float(iou), 3), "kept_px": int(a.sum()), "subject_px": int(truth_mask.sum())})
    return [truth("mask matches the planted subject (IoU >= 0.8)", iou >= 0.8, round(float(iou), 3)),
            truth("corners are transparent", not a[:20, :20].any() and not a[-20:, -20:].any()),
            eq("output has alpha", out.mode, "RGBA")]


PROGRAMS = {"MEDIA-25": media25, "MEDIA-27": media27}
