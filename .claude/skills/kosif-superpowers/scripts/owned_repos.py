#!/usr/bin/env python3
"""Owned-repositories map: what every repository on the owner's GitHub account gives this skill.

One registry (data/owned_repos.json) joins three things Claude needs to know before it reaches for a repo:
what the repo is for (curated), what is measurably inside it (a gitingest-style static digest), and how it
relates to the skill's 15 smart capability groups (have now / learnable / not yet integrated).

    python3 scripts/owned_repos.py digest <clones-dir> --out <digest.json>   # static scan of shallow clones (no code runs)
    python3 scripts/owned_repos.py merge <digest.json>                       # refresh measured fields in data/owned_repos.json
    python3 scripts/owned_repos.py list                                      # one line per repo
    python3 scripts/owned_repos.py show <repo>                               # one repo in full
    python3 scripts/owned_repos.py find "<task>" [--top N] [--json]          # which owned repos help this task
    python3 scripts/owned_repos.py skills [--json]                           # have-now vs learnable, per capability group
    python3 scripts/owned_repos.py render [--check]                          # write references/owned-repos-map.md
    python3 scripts/owned_repos.py verify                                    # registry ↔ groups ↔ privacy consistency
    python3 scripts/owned_repos.py --self-test

Stdlib only. `digest` reads files and never imports, installs or executes repository code; secret-like strings
are counted by pattern name only (their values and, for private repos, their paths are never written).
Private repositories keep only measured counts and the owner's own one-line purpose in the committed
registry: this skill is published from a public repository.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
DATA = SKILL / "data" / "owned_repos.json"
GROUPS = SKILL / "data" / "smart_capability_index.json"
DOC = SKILL / "references" / "owned-repos-map.md"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".next", "dist", "build", ".venv", "venv", "coverage", ".cache"}
EXT_LANG = {".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".jsx": "JavaScript",
            ".ts": "TypeScript", ".tsx": "TypeScript", ".html": "HTML", ".css": "CSS", ".md": "Markdown",
            ".json": "JSON", ".sh": "Shell", ".ps1": "PowerShell", ".bat": "Batch", ".sql": "SQL", ".svg": "SVG",
            ".rs": "Rust", ".go": "Go", ".toml": "TOML", ".yml": "YAML", ".yaml": "YAML"}
MEDIA = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm", ".mp3", ".wav", ".ttf", ".otf", ".woff2", ".glb"}
# Pattern names only. A hit means "rotate or check", never "here is the value".
SECRET_PATTERNS = {
    "anthropic-key": r"sk-ant-[A-Za-z0-9_\-]{20,}",
    "openai-key": r"sk-(?:proj-)?[A-Za-z0-9]{32,}",
    "github-token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "google-api-key": r"AIza[0-9A-Za-z_\-]{35}",
    "aws-access-key": r"AKIA[0-9A-Z]{16}",
    "private-key-block": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "slack-token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
}
SECRET_RE = {k: re.compile(v) for k, v in SECRET_PATTERNS.items()}
AGENT_DOCS = ("CLAUDE.md", "AGENTS.md", "GEMINI.md", "SKILL.md")
MANIFESTS = ("package.json", "pyproject.toml", "requirements.txt", "wrangler.toml", "wrangler.jsonc", "wrangler.json",
             "docker-compose.yml", "plugin.json", "mcp.json")
STATES = ("integrated", "partial", "learnable", "reference", "archive", "empty")
STATE_AR = {"integrated": "مدمج في سوبر باور", "partial": "مدمج جزئيًا", "learnable": "قابل للتعلّم (لم يُدمج بعد)",
            "reference": "مرجع/مصدر", "archive": "أرشيف أو نسخة مكررة", "empty": "فارغ"}
WORD_RE = re.compile(r"[\w؀-ۿ]+")


# ------------------------------------------------------------------ digest (static, read-only)

def _files(root: Path):
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.is_file() and not p.is_symlink():
            yield p


def _readme_summary(root: Path) -> str:
    for name in ("README.md", "readme.md", "README.ar.md", "README.txt"):
        f = root / name
        if f.is_file():
            text = f.read_text(encoding="utf-8", errors="replace")
            lines = [l.strip() for l in text.splitlines()]
            title = next((l.lstrip("# ").strip() for l in lines if l.startswith("#")), "")
            para = next((l for l in lines if l and not l.startswith(("#", "!", "<", "[", "|", ">", "```", "-"))), "")
            return (title + " — " + para)[:300].strip(" —")
    return ""


def digest_repo(root: Path) -> dict:
    langs, media, secrets, secret_files = Counter(), 0, Counter(), set()
    skills, tests, workflows, files, size = 0, 0, 0, 0, 0
    for f in _files(root):
        files += 1
        try:
            size += f.stat().st_size
        except OSError:
            continue
        rel = f.relative_to(root).as_posix()
        ext = f.suffix.lower()
        if ext in EXT_LANG:
            langs[EXT_LANG[ext]] += 1
        elif ext in MEDIA:
            media += 1
        if f.name == "SKILL.md":
            skills += 1
        if re.search(r"(^|/)(tests?|evals?|__tests__)/|(^|/)test_[^/]+\.py$|\.test\.[jt]sx?$|\.spec\.[jt]sx?$", rel):
            tests += 1
        if rel.startswith(".github/workflows/"):
            workflows += 1
        if ext in EXT_LANG and f.stat().st_size < 2_000_000:
            text = f.read_text(encoding="utf-8", errors="replace")
            for name, rx in SECRET_RE.items():
                if rx.search(text):
                    secrets[name] += 1
                    secret_files.add(rel)
    top = sorted(p.name + ("/" if p.is_dir() else "") for p in root.iterdir() if p.name not in SKIP_DIRS)
    manifests = sorted(m for m in MANIFESTS if (root / m).is_file())
    pkg = {}
    if (root / "package.json").is_file():
        try:
            j = json.loads((root / "package.json").read_text(encoding="utf-8"))
            pkg = {"name": j.get("name", ""), "scripts": sorted(j.get("scripts", {}))[:12],
                   "deps": sorted({**j.get("dependencies", {}), **j.get("devDependencies", {})})[:25]}
        except ValueError:
            pkg = {"error": "unparseable package.json"}
    return {"files": files, "size_kb": size // 1024, "languages": dict(langs.most_common(6)), "media_files": media,
            "skill_md": skills, "test_files": tests, "ci_workflows": workflows,
            "agent_docs": sorted(d for d in AGENT_DOCS if (root / d).is_file()), "manifests": manifests,
            "package": pkg, "top_level": top[:30], "readme": _readme_summary(root),
            "secret_like": dict(sorted(secrets.items())), "secret_like_files": sorted(secret_files)[:20]}


def cmd_digest(a) -> int:
    root = Path(a.clones).resolve()
    out = {}
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        name = d.name.replace("_", "/", 1)  # clone dirs are named owner_repo
        out[name] = digest_repo(d)
        print(f"{name:45s} files={out[name]['files']:>6} skills={out[name]['skill_md']:>5} "
              f"tests={out[name]['test_files']:>4} secret_like={sum(out[name]['secret_like'].values())}", file=sys.stderr)
    text = json.dumps({"schema": "kosif.owned-repos.digest.v1", "repos": out}, ensure_ascii=False, indent=1) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


# ------------------------------------------------------------------ registry

def load(path: Path = DATA) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(reg: dict, path: Path = DATA) -> None:
    path.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


PUBLIC_MEASURED = ("files", "size_kb", "languages", "media_files", "skill_md", "test_files", "ci_workflows",
                   "agent_docs", "manifests", "readme")
PRIVATE_MEASURED = ("files", "size_kb", "languages", "skill_md", "test_files")


def cmd_merge(a) -> int:
    reg, dg = load(), json.loads(Path(a.digest).read_text(encoding="utf-8"))["repos"]
    by = {r["repo"]: r for r in reg["repos"]}
    for name, d in sorted(dg.items()):
        r = by.get(name)
        if r is None:
            print(f"! {name} is in the digest but not in the registry: add a curated entry first", file=sys.stderr)
            continue
        keep = PRIVATE_MEASURED if r.get("visibility") == "private" else PUBLIC_MEASURED
        r["measured"] = {k: d[k] for k in keep}
        r["measured"]["secret_like_hits"] = sum(d["secret_like"].values())
    save(reg)
    print(f"merged {len(dg)} digests into {DATA.relative_to(SKILL).as_posix()}")
    return 0


def citations() -> Counter:
    """How many catalog proof paths start with each repository name (the measurable integration signal)."""
    sys.path.insert(0, str(HERE))
    import powers as P  # noqa: E402
    c = Counter()
    for p in P.load_powers():
        for pr in p.get("proof") or []:
            c[pr.split("/")[0]] += 1
    return c


def groups() -> dict:
    return {g["id"]: g for g in json.loads(GROUPS.read_text(encoding="utf-8"))["groups"]}


def _words(text: str) -> set:
    return {w.lower() for w in WORD_RE.findall(text) if len(w) > 2}


def rank(task: str, reg: dict, top: int = 5) -> list:
    q = _words(task)
    gs = groups()
    out = []
    for r in reg["repos"]:
        hay = _words(" ".join([r["repo"], r.get("purpose_en", ""), r.get("purpose_ar", ""), " ".join(r.get("keywords", [])),
                               " ".join(r.get("reusable", []))]))
        gw = set()
        for g in r.get("groups", []):
            gw |= _words(gs.get(g, {}).get("keywords", ""))
        hits = sorted(q & hay)
        ghits = sorted((q & gw) - set(hits))
        score = 3 * len(hits) + len(ghits) + {"integrated": 0.5, "partial": 0.5, "learnable": 0.5, "archive": -2, "empty": -3}.get(r.get("state"), 0)
        if hits or ghits:
            out.append({"repo": r["repo"], "score": score, "state": r["state"], "matched": hits + ghits,
                        "use": r.get("learn", ""), "groups": r.get("groups", [])})
    out.sort(key=lambda x: (-x["score"], x["repo"]))
    return out[:top]


def skill_map(reg: dict) -> list:
    """Per capability group: what Claude has now, what it can learn, and which owned repos feed it."""
    rows = []
    for gid, g in groups().items():
        sc = g.get("status_counts", {})
        feeders = [r["repo"].split("/")[-1] for r in reg["repos"] if gid in r.get("groups", [])]
        learn_repos = [r["repo"].split("/")[-1] for r in reg["repos"]
                       if gid in r.get("groups", []) and r["state"] in ("learnable", "partial")]
        rows.append({"group": gid, "ar": g["ar"], "powers": g["count"],
                     "have_now": sc.get("proven", 0) + sc.get("ready", 0),
                     "methods": sc.get("documented", 0) + sc.get("seen", 0),
                     "learn_by_install": sc.get("install", 0), "learn_by_key": sc.get("key", 0),
                     "ideas": sc.get("idea", 0), "owned_repos": feeders, "learn_from_repos": learn_repos})
    return rows


def problems(reg: dict) -> list:
    errs, gs, seen = [], groups(), set()
    for r in reg.get("repos", []):
        n = r.get("repo", "?")
        if n in seen:
            errs.append(f"{n}: duplicate entry")
        seen.add(n)
        for k in ("repo", "visibility", "state", "purpose_ar", "purpose_en", "groups"):
            if not r.get(k) and not (k == "groups" and r.get("state") == "empty"):
                errs.append(f"{n}: missing {k}")
        if r.get("state") not in STATES:
            errs.append(f"{n}: state {r.get('state')!r} not in {STATES}")
        for g in r.get("groups", []):
            if g not in gs:
                errs.append(f"{n}: unknown capability group {g!r}")
        for rel in r.get("links_in_skill", []):
            if not (SKILL / rel).exists():
                errs.append(f"{n}: links_in_skill path {rel} does not exist")
        if r.get("visibility") == "private":
            m = r.get("measured", {})
            leaked = sorted(set(m) - set(PRIVATE_MEASURED) - {"secret_like_hits"})
            if leaked:
                errs.append(f"{n}: private repo exposes {leaked} in the public registry")
            if r.get("reusable_detail"):
                errs.append(f"{n}: private repo must not carry reusable_detail in the public registry")
    cites = citations()
    for r in reg.get("repos", []):
        short = r.get("repo", "").split("/")[-1]
        if r.get("state") == "integrated" and not cites.get(short) and not r.get("links_in_skill"):
            errs.append(f"{r.get('repo')}: state integrated but no catalog proof cites it and links_in_skill is empty")
    nodes = {r.get("repo") for r in reg.get("repos", [])} | {v.get("id") for v in reg.get("services", [])}
    for v in reg.get("services", []):
        for k in ("id", "kind", "role_ar", "interfaces", "observed"):
            if not v.get(k):
                errs.append(f"service {v.get('id', '?')}: missing {k}")
        if v.get("source") and v["source"] not in nodes:
            errs.append(f"service {v.get('id')}: source {v['source']} is not a listed repo")
    for e in reg.get("relations", []):
        for end in (e.get("from"), e.get("to")):
            if end not in nodes:
                errs.append(f"relation {e.get('from')} -> {e.get('to')}: {end} is neither a listed repo nor a service")
    total = reg.get("account", {}).get("repo_count")
    if total is not None and total != len(reg.get("repos", [])):
        errs.append(f"account.repo_count={total} but the registry lists {len(reg.get('repos', []))} repos")
    return errs


def render(reg: dict) -> str:
    L = ["<!-- generated by scripts/owned_repos.py render; edit data/owned_repos.json instead -->",
         "# خريطة مستودعات المالك ← سوبر باور / Owned repositories map", "",
         f"الحساب: `{reg['account']['owner']}` · عدد المستودعات: **{len(reg['repos'])}** · آخر مسح: {reg['account']['scanned']} "
         f"· الطريقة: {reg['account']['method']}", "",
         "كل مستودع مربوط بمجموعات القدرات الخمس عشرة (`smart_capabilities.py groups`) وبحالته: هل هو مدمج في سوبر باور، "
         "أم مدمج جزئيًا، أم قابل للتعلّم منه، أم مرجع، أم أرشيف. المستودعات الخاصة تظهر بغرضها وأرقامها فقط.", "",
         "اسأل: `python3 scripts/owned_repos.py find \"<المهمة>\"` · خريطة المتاح والقابل للتعلّم: `python3 scripts/owned_repos.py skills`", "",
         "## المستودعات / Repositories", "",
         "«استشهادات» = عدد مسارات الإثبات في كتالوج القدرات التي تبدأ باسم المستودع (مقياس الدمج الفعلي).", "",
         "| المستودع | الحالة | استشهادات | الغرض | المجموعات | ما يُستفاد منه |", "|---|---|---|---|---|---|"]
    cites = citations()
    for r in reg["repos"]:
        vis = " 🔒" if r["visibility"] == "private" else ""
        L.append(f"| `{r['repo']}`{vis} | {STATE_AR[r['state']]} | {cites.get(r['repo'].split('/')[-1], 0)} | {r['purpose_ar']} | {', '.join(r.get('groups', [])) or '—'} "
                 f"| {'؛ '.join(r.get('reusable', [])) or '—'} |")
    L += ["", "## المتاح الآن والقابل للتعلّم / Have now vs can learn", "",
          "«متاح الآن» = قدرات ✅ مثبتة أو 🟢 جاهزة. «طرق» = طرق موثقة يطبقها Claude مباشرة. «بالتثبيت/بالمفتاح» = تصبح متاحة "
          "بعد تثبيت مكتبة أو إضافة مفتاح بإذن المستخدم. «للتعلّم من مستودعاتك» = مستودعات حالتها قابل للتعلّم أو مدمج جزئيًا.", "",
          "| المجموعة | القدرات | متاح الآن | طرق | بالتثبيت | بالمفتاح | مستودعاتك | للتعلّم من مستودعاتك |",
          "|---|---|---|---|---|---|---|---|"]
    for s in skill_map(reg):
        L.append(f"| {s['group']} · {s['ar']} | {s['powers']} | {s['have_now']} | {s['methods']} | {s['learn_by_install']} "
                 f"| {s['learn_by_key']} | {', '.join(s['owned_repos']) or '—'} | {', '.join(s['learn_from_repos']) or '—'} |")
    L += ["", "## الخدمات الحية المرتبطة / Live services", "",
          "خدمات يملكها المالك على Cloudflare تبنيها هذه المستودعات أو تعتمد عليها. الحالة المذكورة مرصودة في تقرير تسليم، "
          "وليست فحصًا حيًا من هذه الجلسة. العناوين الكاملة في متغيرات البيئة داخل kosif-omni وليست هنا.", "",
          "| الخدمة | النوع | المصدر | الدور | الواجهات | آخر رصد |", "|---|---|---|---|---|---|"]
    for v in reg.get("services", []):
        src = f"`{v['source']}`" + (f" `{v['path']}`" if v.get("path") else "") if v.get("source") else "—"
        L.append(f"| `{v['id']}` | {v['kind']} | {src} | {v['role_ar']} | {' · '.join(v['interfaces'])} | {v['observed']} |")
    L += ["", "## قواعد الأمان عند استخدامها / Rules", ""] + [f"- {x}" for x in reg.get("rules", [])]
    L += ["", "## العلاقات بين المستودعات والخدمات / Relationships", ""]
    for e in reg.get("relations", []):
        L.append(f"- `{e['from']}` —{e['kind']}→ `{e['to']}`: {e['note']}")
    L += ["", "## تنبيهات / Findings", ""] + [f"- {x}" for x in reg.get("findings", [])]
    L += ["", "## كيف تحدّث الخريطة / Refresh", "", "```bash",
          "# 1) clone shallow copies outside the repo (private repos need access granted in the session)",
          "# 2) static digest (reads files only):",
          "python3 scripts/owned_repos.py digest <clones-dir> --out <work-dir>/digest.json",
          "python3 scripts/owned_repos.py merge <work-dir>/digest.json",
          "python3 scripts/owned_repos.py render && python3 scripts/owned_repos.py verify", "```", ""]
    heads = [l[3:] for l in L if l.startswith("## ")]
    at = L.index("## المستودعات / Repositories")
    L[at:at] = ["## الفهرس / contents", ""] + [f"- [{h}](#{_slug(h)})" for h in heads] + [""]
    return "\n".join(L)


def _slug(title: str) -> str:
    """GitHub's heading anchor (same rule as check_skill.gh_slug)."""
    t = re.sub(r"`|\*\*|__", "", title.strip()).lower()
    return "".join(c for c in t if c in " -_" or unicodedata.category(c)[0] in "LMN").replace(" ", "-")


# ------------------------------------------------------------------ CLI

def cmd_list(a) -> int:
    cites = citations()
    reg = load()
    for v in reg.get("services", []):
        print(f"{'service:' + v['id']:45s} {v['kind']:19s} {v['observed'][:60]}")
    for r in reg["repos"]:
        print(f"{r['repo']:45s} {r['visibility']:8s} {r['state']:11s} cites={cites.get(r['repo'].split('/')[-1], 0):<5} "
              f"{', '.join(r.get('groups', []))}")
    return 0


def cmd_show(a) -> int:
    for r in load()["repos"]:
        if r["repo"] == a.repo or r["repo"].split("/")[-1] == a.repo:
            print(json.dumps(r, ensure_ascii=False, indent=1))
            return 0
    print(f"no repo {a.repo!r}; try: owned_repos.py list", file=sys.stderr)
    return 1


def cmd_find(a) -> int:
    res = rank(a.task, load(), a.top)
    if a.json:
        print(json.dumps({"task": a.task, "results": res}, ensure_ascii=False, indent=1))
    else:
        for x in res or [{"repo": "(no owned repo matches; use hub.py find)", "score": 0, "state": "", "matched": [], "use": ""}]:
            print(f"{x['score']:>5} {x['repo']:42s} {x['state']:11s} {', '.join(x['matched'][:6])}")
            if x["use"]:
                print(f"      → {x['use']}")
    return 0


def cmd_skills(a) -> int:
    rows = skill_map(load())
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0
    print(f"{'group':10s} {'powers':>6} {'have':>5} {'methods':>7} {'install':>7} {'key':>4}  owned repos (learnable)")
    for s in rows:
        print(f"{s['group']:10s} {s['powers']:>6} {s['have_now']:>5} {s['methods']:>7} {s['learn_by_install']:>7} "
              f"{s['learn_by_key']:>4}  {', '.join(s['owned_repos']) or '-'}"
              + (f"  ({', '.join(s['learn_from_repos'])})" if s["learn_from_repos"] else ""))
    return 0


def cmd_render(a) -> int:
    text = render(load())
    if a.check:
        ok = DOC.is_file() and DOC.read_text(encoding="utf-8") == text
        print("render: up to date" if ok else "render: references/owned-repos-map.md is stale — run owned_repos.py render")
        return 0 if ok else 1
    DOC.write_text(text, encoding="utf-8")
    print(f"wrote {DOC.relative_to(SKILL).as_posix()}")
    return 0


def cmd_verify(a) -> int:
    reg = load()
    errs = problems(reg)
    if DOC.is_file() and DOC.read_text(encoding="utf-8") != render(reg):
        errs.append("references/owned-repos-map.md is stale — run owned_repos.py render")
    for e in errs:
        print("ERROR", e)
    print(f"verify: {len(reg['repos'])} repos · {len(errs)} error(s) → {'OK' if not errs else 'FAIL'}")
    return 1 if errs else 0


def self_test() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        root = Path(t) / "me_demo"
        (root / "tests").mkdir(parents=True)
        (root / "README.md").write_text("# Demo\n\nDraws characters.\n", encoding="utf-8")
        (root / "SKILL.md").write_text("---\nname: d\n---\n", encoding="utf-8")
        (root / "tests" / "test_a.py").write_text("x = 1\n", encoding="utf-8")
        (root / "leak.js").write_text("const k = 'AKIA" + "ABCDEFGHIJKLMNOP';\n", encoding="utf-8")
        d = digest_repo(root)
        assert d["skill_md"] == 1 and d["test_files"] == 1, d
        assert d["secret_like"] == {"aws-access-key": 1} and "AKIA" not in json.dumps(d["secret_like"]), d
        assert d["readme"].startswith("Demo"), d
    reg = load()
    assert not problems(reg), problems(reg)
    bad = {"account": {}, "repos": [{"repo": "o/p", "visibility": "private", "state": "learnable", "purpose_ar": "x",
                                     "purpose_en": "x", "groups": ["nope"], "measured": {"readme": "secret plan"}}]}
    errs = problems(bad)
    assert any("unknown capability group" in e for e in errs) and any("exposes" in e for e in errs), errs
    assert rank("رسم شخصيات", reg), "drawing task should match an owned repo"
    assert len(skill_map(reg)) == len(groups())
    print("self-test: OK")
    return 0


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("digest"); p.add_argument("clones"); p.add_argument("--out")
    p = sub.add_parser("merge"); p.add_argument("digest")
    sub.add_parser("list")
    p = sub.add_parser("show"); p.add_argument("repo")
    p = sub.add_parser("find"); p.add_argument("task"); p.add_argument("--top", type=int, default=5); p.add_argument("--json", action="store_true")
    p = sub.add_parser("skills"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("render"); p.add_argument("--check", action="store_true")
    sub.add_parser("verify")
    a = ap.parse_args(argv)
    return {"digest": cmd_digest, "merge": cmd_merge, "list": cmd_list, "show": cmd_show, "find": cmd_find,
            "skills": cmd_skills, "render": cmd_render, "verify": cmd_verify}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
