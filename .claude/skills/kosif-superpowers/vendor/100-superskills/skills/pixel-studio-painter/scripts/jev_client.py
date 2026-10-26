"""Jev, the fast judge: asks the live Jev service to choose between options, twice in parallel with the options in
reverse order, and reports the order-robust choice with its probabilities. Jev judges; it never authorises.
Offline or KOSIF_JEV_URL=off -> None, and the caller falls back to its own deterministic rule."""
from __future__ import annotations

import json
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://kosif-jev.kosif199022.workers.dev/api/public-jev"


def _call(packet: dict, timeout: float) -> dict:
    req = urllib.request.Request(os.environ.get("KOSIF_JEV_URL", URL), method="POST",
                                 data=json.dumps(packet, ensure_ascii=False).encode("utf-8"),
                                 headers={"content-type": "application/json", "user-agent": "kosif-studio/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:            # Cloudflare refuses calls without a UA
        data = json.loads(r.read(1_000_000).decode("utf-8", "replace"))
    return data["result"]["answers"]["decision"]


def choose(question: str, state: dict, options: dict[str, str], timeout: float = 20) -> dict | None:
    """{choice, probabilities (mean of both orders), stable, latency_s} or None when Jev cannot be reached."""
    if os.environ.get("KOSIF_JEV_URL", "").strip().lower() == "off":
        return None
    a = {"type": "choice", "state": state, "instructions": question, "criteria": options}
    b = {**a, "criteria": dict(reversed(list(options.items())))}
    t0 = time.time()
    try:
        with ThreadPoolExecutor(2) as ex:
            ra, rb = ex.map(lambda p: _call(p, timeout), (a, b))
    except Exception:
        return None
    probs = {k: round((ra["probabilities"].get(k, 0) + rb["probabilities"].get(k, 0)) / 2, 4) for k in options}
    best = max(probs, key=probs.get)
    return {"choice": best, "probabilities": probs, "stable": ra.get("choice") == rb.get("choice"),
            "latency_s": round(time.time() - t0, 2), "model": "jev"}
