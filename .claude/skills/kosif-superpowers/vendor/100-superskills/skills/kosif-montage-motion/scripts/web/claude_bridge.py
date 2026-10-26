"""The brain link: how the site asks Claude for a plan, a timeline or a composition.

Ways in, tried in this order (settings.json `backend`: auto / cli / api / mcp / none):
  cli   Claude Code's CLI (`claude -p`) when it is installed and logged in — no key, nothing stored.
  api   the Anthropic API with a key kept in workbench/settings.json (never sent to the browser in full).
  mcp   no call at all: Claude Code (or any MCP client) drives this site through /mcp — the site is the hands,
        Claude is the brain in its own window. `package()` also gives the same prompt to paste into any Claude chat
        and `apply()` reads the reply back. This is the mode that always works.

Replies are expected in one fenced ```json block:
{"actions": [{"recipe": "reel", "args": {"clip": "…", "--out": "…"}}],
 "files": [{"project": "NAME", "path": "index.html", "content": "…"}],
 "timeline": {…a timeline spec…}, "notes": "…"}
Nothing is executed on arrival: the site shows the plan and the user presses تطبيق.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

DEFAULTS = {"backend": "auto", "anthropic_api_key": "", "model": "claude-sonnet-5-5", "timeout": 240}
_cache: dict = {}


class Settings:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict:
        try:
            return {**DEFAULTS, **json.loads(self.path.read_text(encoding="utf-8"))}
        except (OSError, ValueError):
            return dict(DEFAULTS)

    def save(self, d: dict):
        cur = self.load()
        cur.update({k: v for k, v in d.items() if k in DEFAULTS})
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")
        _cache.clear()

    def public(self) -> dict:
        d = self.load()
        key = d.get("anthropic_api_key") or ""
        return {"backend": d["backend"], "model": d["model"], "timeout": d["timeout"], "api_key_set": bool(key), "api_key_hint": (key[:7] + "…") if key else ""}


def claude_cli() -> str | None:
    found = shutil.which("claude")
    if found and not found.lower().endswith(".cmd"):
        return found
    home = Path.home()
    for p in (Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe",
              Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd", home / ".claude" / "local" / "claude.exe", home / ".claude" / "local" / "claude",
              Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "claude-code" / "claude.exe"):
        if p.is_file():
            return str(p)
    return found


def _env() -> dict:
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _run_cli(cli: str, prompt: str, timeout: float) -> str:
    work = tempfile.mkdtemp(prefix="kosif_ai_")
    try:
        if len(prompt) < 28000:
            args, inp = [cli, "-p", prompt, "--output-format", "text"], ""
        else:
            args, inp = [cli, "-p", "نفّذ التعليمات الموجودة في المدخل التالي كاملة.", "--output-format", "text"], prompt
        r = subprocess.run(args, input=inp, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env(), cwd=work, timeout=timeout, shell=cli.lower().endswith(".cmd"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    out = (r.stdout or "").strip()
    if r.returncode != 0 or not out:
        raise RuntimeError((r.stderr or out or f"exit {r.returncode}").strip()[-400:])
    return out


def cli_ready(timeout: float = 25.0) -> tuple[bool, str]:
    if "cli" in _cache and time.time() - _cache["cli"][2] < 600:
        return _cache["cli"][:2]
    cli = claude_cli()
    if not cli:
        res = (False, "Claude Code CLI غير موجود على هذا الجهاز (claude غير مثبّت في PATH)")
    else:
        try:
            _run_cli(cli, "Reply with exactly the word OK and nothing else.", timeout)
            res = (True, f"Claude Code جاهز ({cli})")
        except subprocess.TimeoutExpired:
            res = (False, "Claude Code لم يردّ في الوقت المحدد")
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            res = (False, "Claude Code مثبّت لكنه غير مسجّل الدخول: افتح طرفية واكتب claude ثم /login" if "login" in msg.lower() else f"Claude Code: {msg[:200]}")
    _cache["cli"] = (*res, time.time())
    return res


def backend(settings: Settings) -> str:
    want = settings.load().get("backend", "auto")
    if want == "none":
        return "mcp"
    if want in ("auto", "cli") and cli_ready()[0]:
        return "cli"
    if want in ("auto", "api") and (settings.load().get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY")):
        return "api"
    return "mcp"


def _ask_api(prompt: str, key: str, timeout: float, model: str) -> str:
    import urllib.request
    body = json.dumps({"model": model, "max_tokens": 8000, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST",
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "".join(part.get("text", "") for part in data.get("content", []) if part.get("type") == "text").strip()


SYSTEM = """أنت عقل استوديو KOSIF Motion المحلي. الموقع ينفّذ؛ أنت تخطّط وتكتب. لديك وصفات (recipes) بحقولها، ومشاريع
(تركيبات HTML حتمية على motion-kit: window.__timelines["root"] = tl، لا Math.random، لا Date، لا setTimeout)، وتايملاين JSON
(clips/overlays/audio كما في schema التايملاين). اكتب خطة تنفيذ فقط في كتلة ```json واحدة بهذا الشكل:
{"notes": "سطر أو سطران بالعربية", "actions": [{"recipe": "ID", "args": {"الحقل": "القيمة"}}],
 "files": [{"project": "NAME", "path": "index.html", "content": "…"}], "timeline": {...} }
قواعد: لا تخترع ملفات غير موجودة في قائمة الوسائط؛ المدد بالثواني؛ النصوص عربية سليمة؛ ≤ 8 كلمات على الشاشة؛ حركة لها معنى
(مدخل → تطوير → ذروة قرب النهاية)؛ لا تدّعِ أن شيئاً صُيّر — الموقع هو من يصيّر ويفحص."""


def package(task: str, context: dict) -> str:
    """The full prompt: the system rules, the live context (recipes, media, projects, current spec) and the task."""
    ctx = json.dumps(context, ensure_ascii=False, indent=1)
    if len(ctx) > 60000:
        ctx = ctx[:60000] + "\n…(مقتطع)"
    return f"{SYSTEM}\n\n## السياق الحي\n```json\n{ctx}\n```\n\n## الطلب\n{task.strip()}\n"


def extract(reply: str) -> dict | None:
    """The ```json block of a reply (or a bare JSON object), parsed; None when there is none."""
    m = re.search(r"```json\s*(\{.*?\})\s*```", reply, re.S) or re.search(r"```\s*(\{.*?\})\s*```", reply, re.S)
    text = m.group(1) if m else reply.strip()
    try:
        obj = json.loads(text)
    except ValueError:
        return None
    return obj if isinstance(obj, dict) else None


def ask(settings: Settings, task: str, context: dict) -> dict:
    prompt = package(task, context)
    d = settings.load()
    be = backend(settings)
    if be == "cli":
        reply = _run_cli(claude_cli(), prompt, float(d.get("timeout", 240)))
    elif be == "api":
        reply = _ask_api(prompt, d.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY", ""), float(d.get("timeout", 240)), d.get("model", DEFAULTS["model"]))
    else:
        return {"backend": "mcp", "reply": None, "plan": None, "package": prompt,
                "message": "لا يوجد اتصال مباشر (CLI أو مفتاح): انسخ الحزمة إلى Claude ثم ألصق الرد هنا، أو دع Claude Code يتحكم عبر /mcp."}
    return {"backend": be, "reply": reply, "plan": extract(reply), "package": None, "message": "تم"}
