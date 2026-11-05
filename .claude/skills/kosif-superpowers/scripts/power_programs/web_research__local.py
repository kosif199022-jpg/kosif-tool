"""WEB-08 Hugging Face hub files through the proxy (env_scope=local: network)."""
from __future__ import annotations
import hashlib
import json
import urllib.request
from pathlib import Path
from ._mind_common import save, eq, truth


def web08(work):
    work = Path(work)
    url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json"
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read()
        final = r.geturl()
    (work / "config.json").write_bytes(data)
    cfg = json.loads(data)
    save(work, "fetch.json", {"url": url, "final_url": final, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return [eq("voice config sample rate", cfg["audio"]["sample_rate"], 22050),
            eq("language family", cfg["language"]["family"], "ar"),
            truth("downloaded through resolve/main", len(data) > 1000, len(data))]


PROGRAMS = {"WEB-08": web08}
