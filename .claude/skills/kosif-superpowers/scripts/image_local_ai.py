#!/usr/bin/env python3
"""KOSIF Superpowers: local, offline image AI with user-supplied ONNX models.

Commands
  models                         the three open models Mosamem pins (facts: licence, source, size, SHA-256)
  verify-model FILE --sha256 HEX check a downloaded file against a pinned SHA-256 (or the known pin by file name)
  remove-bg --model M in out     BiRefNet-style subject matte -> RGBA PNG with a soft alpha
  inpaint --model M --mask m in out   MI-GAN-style fill of the white area of the mask

It never downloads anything. When a model is missing it prints the pinned URL and asks the user to
fetch it themselves. The model table restates public facts published by the Mosamem project
(https://github.com/motalim-ai/mosamem, GPL-3.0, file src-tauri/src/ai/models.rs, checked 2026-10-22);
no Mosamem code is included here. This file is an independent MIT implementation.

Optional dependencies (imported only by remove-bg / inpaint): onnxruntime, numpy, Pillow.
Exit codes: 0 ok, 1 checksum mismatch or bad input, 2 dependency or model missing.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

UPSTREAM = "https://github.com/motalim-ai/mosamem"
UPSTREAM_FILE = "src-tauri/src/ai/models.rs"
CHECKED = "2026-10-22"

# Facts restated from the upstream pin table (commit-pinned URLs, sizes in bytes, SHA-256).
MODELS = [
    {
        "id": "subject",
        "model": "BiRefNet lite (ONNX export by onnx-community)",
        "features": ["select subject", "remove background"],
        "license": "MIT",
        "source": "https://huggingface.co/onnx-community/BiRefNet_lite-ONNX",
        "kosif_command": "remove-bg",
        "io": "input float32 [1,3,1024,1024] RGB normalised with ImageNet mean/std; output logits [1,1,1024,1024] -> sigmoid",
        "files": [
            {"name": "birefnet_lite_fp16.onnx",
             "url": "https://huggingface.co/onnx-community/BiRefNet_lite-ONNX/resolve/de15b22ba131738a16dff04aab8bdf8dc32e3ac1/onnx/model_fp16.onnx",
             "sha256": "d39b897ceb16ae654c1731f3dba0cf9b368d9cae74b5a57459b455cc8bfec402",
             "size": 114538221},
        ],
    },
    {
        "id": "select",
        "model": "SAM 2.1 hiera-tiny (ONNX export by onnx-community)",
        "features": ["object selection from clicks or a box"],
        "license": "Apache-2.0",
        "source": "https://huggingface.co/onnx-community/sam2.1-hiera-tiny-ONNX",
        "kosif_command": None,
        "io": "encoder float32 [1,3,1024,1024]; decoder takes input_points/input_labels/image_embeddings.0-2 and returns iou_scores + pred_masks (not wrapped by this script yet)",
        "files": [
            {"name": "vision_encoder_fp16.onnx",
             "url": "https://huggingface.co/onnx-community/sam2.1-hiera-tiny-ONNX/resolve/814a066640debee5a91e70aa401fb8e17e030503/onnx/vision_encoder_fp16.onnx",
             "sha256": "7773e79d589dada8e1e630cc7eb18b17b2c5b4faeb1eaab5ebf9df618ecbd50a", "size": 314925},
            {"name": "vision_encoder_fp16.onnx_data",
             "url": "https://huggingface.co/onnx-community/sam2.1-hiera-tiny-ONNX/resolve/814a066640debee5a91e70aa401fb8e17e030503/onnx/vision_encoder_fp16.onnx_data",
             "sha256": "a4dd3759e9b6a476d991fb3493787992e78777e51462695e1bede71ae258103e", "size": 67005504},
            {"name": "prompt_encoder_mask_decoder.onnx",
             "url": "https://huggingface.co/onnx-community/sam2.1-hiera-tiny-ONNX/resolve/814a066640debee5a91e70aa401fb8e17e030503/onnx/prompt_encoder_mask_decoder.onnx",
             "sha256": "874414704c5d686db7d206a35f6e15d26563d50c8c4468fccc6739bd7e491dcf", "size": 213114},
            {"name": "prompt_encoder_mask_decoder.onnx_data",
             "url": "https://huggingface.co/onnx-community/sam2.1-hiera-tiny-ONNX/resolve/814a066640debee5a91e70aa401fb8e17e030503/onnx/prompt_encoder_mask_decoder.onnx_data",
             "sha256": "e9874d900dd4134ed60eab1e97910327c2419e0b2954485d8fd6e7f1a1470f47", "size": 20958208},
        ],
    },
    {
        "id": "fill",
        "model": "MI-GAN pipeline v2 (Picsart AI Research)",
        "features": ["smart fill / inpainting"],
        "license": "MIT (code and weights)",
        "source": "https://github.com/Picsart-AI-Research/MI-GAN",
        "kosif_command": "inpaint",
        "io": "inputs image uint8 [1,3,H,W] and mask uint8 [1,1,H,W] (255 = keep, 0 = fill); output result uint8 [1,3,H,W]",
        "files": [
            {"name": "migan_pipeline_v2.onnx",
             "url": "https://huggingface.co/andraniksargsyan/migan/resolve/406830d0fa60666da0071c342ad2fbc8f30c5c64/migan_pipeline_v2.onnx",
             "sha256": "6f1f3530a1a2324b19752018ce756088b07973cda8d7d890034ace5c8a48c40b", "size": 28079181},
        ],
    },
]

MEAN = (0.485, 0.456, 0.406)
STD = (0.229, 0.224, 0.225)


def fail(msg, code):
    print(msg, file=sys.stderr)
    return code


def known_pin(name):
    for m in MODELS:
        for f in m["files"]:
            if f["name"] == name or f["url"].rsplit("/", 1)[-1] == name:
                return m, f
    return None, None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_hint(model_id):
    m = next(x for x in MODELS if x["id"] == model_id)
    lines = [f"Model not found. This tool never downloads. Fetch it yourself only if you agree (licence {m['license']}):"]
    for f in m["files"]:
        lines.append(f"  {f['url']}  ({f['size']:,} bytes, sha256 {f['sha256']})")
    lines.append(f"Then run: python3 scripts/image_local_ai.py verify-model <file> --sha256 <hex>")
    return "\n".join(lines)


def load_deps():
    missing = []
    mods = {}
    for name, imp in (("numpy", "numpy"), ("onnxruntime", "onnxruntime"), ("Pillow", "PIL.Image")):
        try:
            mods[name] = __import__(imp, fromlist=["_"])
        except Exception:
            missing.append(name)
    if missing:
        return None, "missing optional dependencies: " + ", ".join(missing) + " (pip install " + " ".join(missing) + ")"
    return mods, None


def open_session(ort, model):
    opts = ort.SessionOptions()
    opts.log_severity_level = 3
    return ort.InferenceSession(str(model), sess_options=opts, providers=["CPUExecutionProvider"])


# ---- commands ----

def cmd_models(a):
    if a.json:
        print(json.dumps({"upstream": UPSTREAM, "upstream_file": UPSTREAM_FILE, "checked": CHECKED,
                          "downloads": False, "models": MODELS}, ensure_ascii=False, indent=1))
        return 0
    print(f"Pinned by {UPSTREAM} ({UPSTREAM_FILE}), checked {CHECKED}. Nothing is downloaded by this tool.")
    for m in MODELS:
        total = sum(f["size"] for f in m["files"])
        cmd = m["kosif_command"] or "(listed only)"
        print(f"\n[{m['id']}] {m['model']}  licence {m['license']}  {total / 1e6:.1f} MB  -> {cmd}")
        print(f"  source {m['source']}")
        for f in m["files"]:
            print(f"  {f['name']}  {f['size']:,} B  sha256 {f['sha256']}")
            print(f"    {f['url']}")
    return 0


def cmd_verify(a):
    p = Path(a.file)
    if not p.is_file():
        return fail(f"model file not found: {p}", 2)
    expected = (a.sha256 or "").lower()
    pin_model, pin_file = known_pin(p.name)
    if not expected:
        if not pin_file:
            return fail("no --sha256 given and the file name matches no known pin", 1)
        expected = pin_file["sha256"]
    got = sha256_file(p)
    ok = got == expected
    print(json.dumps({"file": str(p), "size": p.stat().st_size, "sha256": got, "expected": expected,
                      "match": ok, "known_pin": pin_model["id"] if pin_model else None}, indent=1))
    return 0 if ok else 1


def _model_or_hint(model, model_id):
    if not model or not Path(model).is_file():
        print(fetch_hint(model_id), file=sys.stderr)
        return False
    return True


def cmd_remove_bg(a):
    mods, err = load_deps()
    if err:
        return fail(err, 2)
    if not _model_or_hint(a.model, "subject"):
        return 2
    np, ort, Image = mods["numpy"], mods["onnxruntime"], mods["Pillow"]
    if not Path(a.input).is_file():
        return fail(f"input image not found: {a.input}", 1)
    img = Image.open(a.input).convert("RGBA")
    w, h = img.size
    sess = open_session(ort, a.model)
    inp = sess.get_inputs()[0]
    size = a.size
    shape = inp.shape
    if not size:
        size = shape[-1] if len(shape) == 4 and isinstance(shape[-1], int) else 1024
    # flatten transparency over mid-grey, resize, ImageNet-normalise, NCHW
    flat = Image.new("RGBA", (w, h), (128, 128, 128, 255))
    flat.alpha_composite(img)
    rgb = flat.convert("RGB").resize((size, size), Image.BILINEAR)
    x = np.asarray(rgb, dtype=np.float32) / 255.0
    x = (x - np.array(MEAN, dtype=np.float32)) / np.array(STD, dtype=np.float32)
    x = x.transpose(2, 0, 1)[None, ...]
    if "float16" in inp.type:
        x = x.astype(np.float16)
    out = sess.run(None, {inp.name: x})[0]
    m = np.asarray(out, dtype=np.float32)
    m = m.reshape(m.shape[-2], m.shape[-1])
    if a.activation == "sigmoid":
        m = 1.0 / (1.0 + np.exp(-m))
    m = np.clip(m, 0.0, 1.0)
    matte = Image.fromarray((m * 255.0 + 0.5).astype(np.uint8), "L").resize((w, h), Image.BILINEAR)
    alpha = np.asarray(img.split()[3], dtype=np.uint16) * np.asarray(matte, dtype=np.uint16) // 255
    out_img = img.copy()
    out_img.putalpha(Image.fromarray(alpha.astype(np.uint8), "L"))
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    out_img.save(a.output)
    if a.mask_out:
        matte.save(a.mask_out)
    cover = float(np.asarray(matte, dtype=np.float32).mean() / 255.0)
    print(json.dumps({"output": a.output, "size": [w, h], "model_input": size, "coverage": round(cover, 4),
                      "model": str(a.model), "network": False}, indent=1))
    return 0


def cmd_inpaint(a):
    mods, err = load_deps()
    if err:
        return fail(err, 2)
    if not _model_or_hint(a.model, "fill"):
        return 2
    np, ort, Image = mods["numpy"], mods["onnxruntime"], mods["Pillow"]
    from PIL import ImageFilter
    for f in (a.input, a.mask):
        if not Path(f).is_file():
            return fail(f"file not found: {f}", 1)
    img = Image.open(a.input).convert("RGB")
    w, h = img.size
    hole = Image.open(a.mask).convert("L")
    if hole.size != (w, h):
        return fail(f"mask size {hole.size} differs from image size {(w, h)}", 1)
    hole = hole.point(lambda v: 255 if v > 127 else 0)
    grow = a.grow if a.grow is not None else int(np.ceil(2.0 * max(w, h) / 512.0)) + 1
    model_hole = hole.filter(ImageFilter.MaxFilter(2 * grow + 1)) if grow > 0 else hole
    known = 255 - np.asarray(model_hole, dtype=np.uint8)  # 255 keep, 0 fill
    chw = np.asarray(img, dtype=np.uint8).transpose(2, 0, 1)[None, ...]
    sess = open_session(ort, a.model)
    ins = sess.get_inputs()
    by = {i.name: i for i in ins}
    img_in = by.get("image", ins[0])
    mask_in = by.get("mask", ins[1] if len(ins) > 1 else None)
    if mask_in is None:
        return fail("model has a single input; an MI-GAN-style model takes image and mask", 1)

    def cast(arr, spec):
        return arr.astype(np.float32) / 255.0 if "float" in spec.type else arr.astype(np.uint8)
    feeds = {img_in.name: cast(chw, img_in), mask_in.name: cast(known[None, None, ...], mask_in)}
    outs = sess.get_outputs()
    out_name = next((o.name for o in outs if o.name == "result"), outs[0].name)
    res = np.asarray(sess.run([out_name], feeds)[0])
    if res.dtype != np.uint8:
        res = np.clip(res * (255.0 if res.max() <= 1.0 else 1.0), 0, 255).astype(np.uint8)
    res = res.reshape(3, h, w).transpose(1, 2, 0)
    sel = np.asarray(hole, dtype=np.uint8)[..., None] > 0  # only the user's own hole is replaced
    final = np.where(sel, res, np.asarray(img, dtype=np.uint8))
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(final.astype(np.uint8), "RGB").save(a.output)
    print(json.dumps({"output": a.output, "size": [w, h], "hole_pixels": int(sel.sum()), "grow": grow,
                      "model": str(a.model), "network": False}, indent=1))
    return 0


def build_parser():
    p = argparse.ArgumentParser(description="Offline image AI with user-supplied ONNX models (never downloads).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("models", help="list the three pinned open models (facts only)")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_models)
    s = sub.add_parser("verify-model", help="check a model file's SHA-256")
    s.add_argument("file")
    s.add_argument("--sha256", help="expected hex digest (default: the known pin for this file name)")
    s.set_defaults(fn=cmd_verify)
    s = sub.add_parser("remove-bg", help="subject matte -> RGBA PNG (BiRefNet-style model)")
    s.add_argument("--model", required=True, help="path to a local ONNX file")
    s.add_argument("--size", type=int, default=0, help="model input side (default: from the model, else 1024)")
    s.add_argument("--activation", choices=["sigmoid", "none"], default="sigmoid")
    s.add_argument("--mask-out", help="also save the greyscale matte here")
    s.add_argument("input")
    s.add_argument("output")
    s.set_defaults(fn=cmd_remove_bg)
    s = sub.add_parser("inpaint", help="fill the white area of --mask (MI-GAN-style model)")
    s.add_argument("--model", required=True)
    s.add_argument("--mask", required=True, help="PNG the image's size; white = area to fill")
    s.add_argument("--grow", type=int, default=None, help="px to grow the hole before the model (default ~2 model px)")
    s.add_argument("input")
    s.add_argument("output")
    s.set_defaults(fn=cmd_inpaint)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
