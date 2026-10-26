"""A photograph from a prompt: the studio cannot paint one from code, so it asks an image model, then draws the
result pixel by pixel and writes the Python program that reproduces it (to_python).

Backends:
  online  Pollinations (https://image.pollinations.ai): free, no account, FLUX-class models. The prompt is sent to
          their server; nothing else is. Used only when the user has agreed to that.
  local   Stable Diffusion (sd-turbo) through diffusers on the CPU, if the user chose to install it (~2 GB).

    python generate.py "prompt…" --out out/photo.png [--backend online|local] [--size 1344x768] [--seed 7]
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ONLINE = "https://image.pollinations.ai/prompt/"


def online(prompt: str, out: Path, width: int, height: int, seed: int | None, model: str = "flux",
           negative: str = "", timeout: float = 180) -> dict:
    q = {"width": width, "height": height, "model": model, "nologo": "true", "enhance": "false"}
    if seed is not None:
        q["seed"] = seed
    text = prompt + (f". Avoid: {negative}" if negative else "")
    url = ONLINE + urllib.parse.quote(text, safe="") + "?" + urllib.parse.urlencode(q)
    t = time.perf_counter()
    req = urllib.request.Request(url, headers={"User-Agent": "kosif-studio/1.0", "Accept": "image/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    if not data or "image" not in ctype:
        raise RuntimeError(f"the generator returned {ctype or 'nothing'} ({len(data)} bytes)")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    from PIL import Image
    with Image.open(out) as im:
        im.load()
        size = im.size
        fmt = im.format
    if fmt != "PNG":                         # keep a lossless copy: it is the reference the studio matches exactly
        png = out.with_suffix(".png")
        Image.open(out).convert("RGB").save(png)
        out = png
    return {"backend": "online", "model": model, "file": str(out), "size": size, "seconds": round(time.perf_counter() - t, 1),
            "seed": seed}


def local(prompt: str, out: Path, width: int, height: int, seed: int | None, steps: int = 4) -> dict:
    try:
        import torch
        from diffusers import AutoPipelineForText2Image
    except ImportError as e:
        raise RuntimeError("the local backend needs: pip install torch diffusers transformers accelerate safetensors "
                           "(about 2 GB with the sd-turbo weights)") from e
    t = time.perf_counter()
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32)
    pipe.to("cpu")
    g = torch.Generator("cpu").manual_seed(seed if seed is not None else 0)
    im = pipe(prompt, num_inference_steps=steps, guidance_scale=0.0, width=width, height=height, generator=g).images[0]
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    return {"backend": "local", "model": "stabilityai/sd-turbo", "file": str(out), "size": im.size,
            "seconds": round(time.perf_counter() - t, 1), "seed": seed}


def generate(prompt: str, out: Path, backend: str = "online", width: int = 1344, height: int = 768,
             seed: int | None = None, negative: str = "") -> dict:
    if backend == "local":
        return local(prompt, out, width - width % 8, height - height % 8, seed)
    return online(prompt, out, width, height, seed, negative=negative)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--out", default=str(HERE / "out" / "generated.png"))
    ap.add_argument("--backend", default="online", choices=["online", "local"])
    ap.add_argument("--size", default="1344x768")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--negative", default="")
    ap.add_argument("--code", action="store_true", help="also write the Python program that reproduces the image")
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.lower().split("x"))
    info = generate(a.prompt, Path(a.out), a.backend, w, h, a.seed, a.negative)
    if a.code:
        import to_python
        p = Path(info["file"])
        code = p.with_suffix(".py")
        code.write_text(to_python.image_to_python(p, p.stem), encoding="utf-8")
        info["code"] = str(code)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()
