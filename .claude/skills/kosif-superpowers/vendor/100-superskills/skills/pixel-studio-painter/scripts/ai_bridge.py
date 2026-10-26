"""The AI behind 🧩 (edit a picture) and 🤖 (a picture from a description).

Backends, tried in this order unless settings.json says otherwise:
  * Claude Code's own CLI (`claude -p`), when it is installed and logged in — no key needed;
  * the Anthropic API, when an API key is in settings.json or ANTHROPIC_API_KEY;
  * none: the studio copies the text for the user to paste into any AI, and colour-only edits are done locally.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SETTINGS = HERE / "settings.json"
DEFAULTS = {"backend": "auto", "anthropic_api_key": "", "model": "claude-sonnet-5-5", "timeout": 240}
_cache: dict = {}


def load_settings() -> dict:
    try:
        return {**DEFAULTS, **json.loads(SETTINGS.read_text(encoding="utf-8"))}
    except (OSError, ValueError):
        return dict(DEFAULTS)


def save_settings(d: dict):
    SETTINGS.write_text(json.dumps({**load_settings(), **d}, ensure_ascii=False, indent=2), encoding="utf-8")
    _cache.clear()


def claude_cli() -> str | None:
    """Where Claude Code's CLI is: on PATH, or where npm / the installer put it."""
    found = shutil.which("claude")
    if found and not found.lower().endswith(".cmd"):
        return found
    home = Path.home()
    for p in (Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe",
              home / ".claude" / "local" / "claude.exe", home / ".claude" / "local" / "claude",
              Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "claude-code" / "claude.exe"):
        if p.is_file():
            return str(p)
    return found


def _env() -> dict:
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _run_cli(cli: str, prompt: str, timeout: float) -> str:
    """One non-interactive answer from the CLI. Long prompts go through stdin (Windows limits the command line)."""
    work = tempfile.mkdtemp(prefix="kosif_ai_")
    try:
        if len(prompt) < 28000:
            args, inp = [cli, "-p", prompt, "--output-format", "text"], ""
        else:
            args, inp = [cli, "-p", "نفّذ التعليمات الموجودة في المدخل التالي كاملة.", "--output-format", "text"], prompt
        r = subprocess.run(args, input=inp, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=_env(), cwd=work, timeout=timeout)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    out = (r.stdout or "").strip()
    if r.returncode != 0 or not out:
        raise RuntimeError((r.stderr or out or f"exit {r.returncode}").strip()[-400:])
    return out


def cli_ready(timeout: float = 25.0) -> tuple[bool, str]:
    """Is the CLI installed and logged in? Checked once per run (a short real call), then remembered."""
    if "cli" in _cache and time.time() - _cache["cli"][2] < 600:
        return _cache["cli"][:2]
    cli = claude_cli()
    if not cli:
        res = (False, "Claude Code غير مثبّت على هذا الجهاز")
    else:
        try:
            _run_cli(cli, "Reply with exactly the word OK and nothing else.", timeout)
            res = (True, f"Claude Code جاهز ({cli})")
        except subprocess.TimeoutExpired:
            res = (False, "Claude Code لم يردّ في الوقت المحدد")
        except Exception as e:
            msg = str(e)
            res = (False, "Claude Code مثبّت لكنه غير مسجّل الدخول: افتح طرفية واكتب  claude  ثم  /login  مرة واحدة"
                   if "login" in msg.lower() else f"Claude Code: {msg[:200]}")
    _cache["cli"] = (*res, time.time())
    return res


def api_key() -> str:
    return (load_settings().get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY", "")).strip()


def backend() -> str | None:
    """'cli' | 'api' | None, honouring settings.json's backend (auto / cli / api / none)."""
    want = load_settings().get("backend", "auto")
    if want == "none":
        return None
    if want in ("auto", "cli") and cli_ready()[0]:
        return "cli"
    if want in ("auto", "api") and api_key():
        return "api"
    return None


def _ask_api(prompt: str, timeout: float, model: str) -> str:
    import urllib.request
    body = json.dumps({"model": model, "max_tokens": 8000, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"x-api-key": api_key(), "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "".join(part.get("text", "") for part in data.get("content", []) if part.get("type") == "text").strip()


def ask(prompt: str, timeout: float | None = None) -> str:
    """The AI's answer as text, through whichever backend is available. RuntimeError when none is."""
    s = load_settings()
    timeout = timeout or float(s.get("timeout", 240))
    b = backend()
    if b == "cli":
        return _run_cli(claude_cli(), prompt, timeout)
    if b == "api":
        return _ask_api(prompt, timeout, s.get("model", DEFAULTS["model"]))
    raise RuntimeError("لا يوجد ذكاء اصطناعي متصل: سجّل الدخول في Claude Code (claude ثم /login) أو ضع مفتاح API في الإعدادات")


def status() -> dict:
    ok, msg = cli_ready()
    return {"backend": backend(), "cli": claude_cli(), "cli_ok": ok, "cli_msg": msg, "api_key": bool(api_key()),
            "settings": load_settings()}


if __name__ == "__main__":
    import sys
    print(json.dumps({k: v for k, v in status().items() if k != "settings"}, ensure_ascii=False, indent=1))
    if len(sys.argv) > 1:
        print(ask(" ".join(sys.argv[1:])))
