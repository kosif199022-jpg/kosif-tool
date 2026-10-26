"""KOSIF Motion Web — the local studio site: the hands of the montage; Claude is the brain.

    python scripts/web/server.py [--port 8766] [--host 127.0.0.1] [--open] [--workers 2]
    python scripts/kmotion.py web --port 8766

What it serves (all on this PC, nothing leaves it):
  /                      the studio UI (Arabic, RTL): media · recipes · projects · timeline · jobs · Workbench · Claude
  /api/health /api/templates /api/plan /api/validate /api/compile      the KOSIF Motion Workbench v3 contract, unchanged
  /api/render/status /api/render/jobs[/ID[/video]]                    the render-service contract (X-Job-Token), rendered here
  /api/env /api/recipes /api/jobs… /api/media… /api/projects… /api/timeline… /api/claude…   the local studio
  /mcp                   JSON-RPC MCP: the 4 Workbench tools + the studio tools (run recipes, read/write projects, jobs…)
Files are read/written only under the package home (projects, out, workbench) and the media library.
"""
from __future__ import annotations

import argparse
import hmac
import json
import mimetypes
import os
import queue
import re
import secrets
import shutil
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
HOME = Path(os.environ.get("KOSIF_MOTION_HOME") or SCRIPTS.parent).resolve()
sys.path.insert(0, str(SCRIPTS)); sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

from starlette.applications import Starlette  # noqa: E402
from starlette.requests import Request  # noqa: E402
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse, Response, StreamingResponse  # noqa: E402
from starlette.routing import Mount, Route  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402

import claude_bridge  # noqa: E402
import jobs as jobs_mod  # noqa: E402
import recipes  # noqa: E402
import wbcompat  # noqa: E402

VERSION = "6.2"
WB = HOME / "workbench"
MEDIA, JOBS, RENDERS, OUT, TIMELINES = WB / "media", WB / "jobs", WB / "renders", HOME / "out", WB / "timelines"
for d in (MEDIA, JOBS, RENDERS, OUT, TIMELINES):
    d.mkdir(parents=True, exist_ok=True)
STATIC = HERE / "static"
MAX_JSON = 4 * 1024 * 1024
MAX_UPLOAD = 4 * 1024 ** 3
TEXT_EXT = {".html", ".htm", ".js", ".json", ".css", ".txt", ".md", ".svg", ".srt", ".ass", ".vtt", ".csv"}
MEDIA_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".json", ".txt", ".srt"}


def _projects_dir() -> Path:
    import motion
    return motion.PROJECTS


ALLOWED_ROOTS = [HOME, WB]


def _inside(p: Path, roots: list[Path]) -> bool:
    try:
        rp = p.resolve()
    except OSError:
        return False
    return any(rp == r.resolve() or r.resolve() in rp.parents for r in roots)


def _unmojibake(name: str) -> str:
    """Restore an Arabic file name that arrived as the wrong bytes: UTF-8 read as Latin-1/cp1252 (some uploaders), or
    the Windows ANSI code page cp1256 read as Latin-1 (curl on Arabic Windows). A readable name passes unchanged; a
    guess is accepted only when it yields Arabic letters."""
    if any("؀" <= ch <= "ۿ" for ch in name) or all(ord(ch) < 128 for ch in name):
        return name
    arabic = lambda s: sum("؀" <= ch <= "ۿ" for ch in s) >= 2  # noqa: E731
    for raw_enc, real_enc in (("latin-1", "utf-8"), ("cp1252", "utf-8"), ("latin-1", "cp1256")):
        try:
            fixed = name.encode(raw_enc).decode(real_enc)
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if arabic(fixed):
            return fixed
    return name


def _safe_name(name: str) -> str:
    name = _unmojibake(str(name))
    base = Path(str(name).replace("\\", "/")).name
    base = re.sub(r"[^\w\-. ؀-ۿ()]+", "_", base, flags=re.UNICODE).strip(" .")
    if not base or base in (".", "..") or base.startswith("."):
        raise ValueError("invalid name")
    return base[:150]


def _err(msg: str, status: int = 400) -> JSONResponse:
    return JSONResponse({"error": msg}, status_code=status)


async def _json(request: Request) -> dict:
    if "application/json" not in (request.headers.get("content-type") or ""):
        raise ValueError("JSON required")
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > MAX_JSON:
            raise ValueError("request too large")
    x = json.loads(bytes(body) or b"null")
    if not isinstance(x, dict):
        raise ValueError("JSON object required")
    return x


# ───────────────────────── the Workbench contract ─────────────────────────
async def health(request: Request):
    return JSONResponse({"status": "ok", "version": "5.3", "local_version": VERSION, "execution": "planning_with_local_engine", "storage": "local",
                         "engine": {"home": str(HOME), "route": _env_cached().get("route")}})


async def templates(request: Request):
    import mtemplates
    return JSONResponse({"templates": wbcompat.TEMPLATES, "motion_templates": [{"id": k, "ar": v["ar"], "seconds": v["seconds"], "params": {p: d[0] for p, d in v["params"].items()}}
                                                                                for k, v in mtemplates.TEMPLATES.items()]})


async def compat_post(request: Request):
    action = request.url.path.rsplit("/", 1)[-1]
    try:
        x = await _json(request)
        if action == "plan":
            return JSONResponse(wbcompat.make_plan(x))
        if action == "validate":
            return JSONResponse(wbcompat.validate_plan(x.get("plan")))
        if action == "compile":
            return JSONResponse(wbcompat.compile_plan(x.get("plan")))
        return _err("not_found", 404)
    except ValueError as e:
        return _err(str(e) or "Invalid request", 415 if str(e) == "JSON required" else 400)
    except Exception as e:  # noqa: BLE001
        return _err(str(e)[:300], 400)


# ───────────────────────── the render-service contract (local) ─────────────────────────
class RenderJob:
    def __init__(self, manifest: dict):
        self.id = secrets.token_urlsafe(18); self.token = secrets.token_urlsafe(32)
        self.manifest = manifest; self.dir = RENDERS / self.id; self.video = self.dir / "video.mp4"
        self.status = "queued"; self.progress = 0.0; self.error = None; self.metadata = None
        self.created = time.time(); self.cancel = threading.Event()

    def public(self) -> dict:
        r = {"status": self.status, "progress": self.progress}
        if self.error:
            r["error"] = self.error
        if self.metadata and self.status == "succeeded":
            r["metadata"] = self.metadata
        return r


class RenderEngine:
    def __init__(self):
        self.jobs: dict[str, RenderJob] = {}
        self.q: queue.Queue[RenderJob] = queue.Queue()
        threading.Thread(target=self._worker, daemon=True, name="kosif-manifest-render").start()

    def _worker(self):
        while True:
            job = self.q.get()
            try:
                if job.cancel.is_set():
                    job.status = "cancelled"; continue
                job.status = "running"
                job.dir.mkdir(parents=True, exist_ok=True)
                def prog(p, j=job):
                    j.progress = p
                job.metadata = wbcompat.render_manifest(job.manifest, job.video, prog, job.cancel.is_set)
                job.status, job.progress = ("cancelled" if job.cancel.is_set() else "succeeded"), 1.0
            except InterruptedError:
                job.status = "cancelled"
            except Exception as e:  # noqa: BLE001
                job.status = "cancelled" if job.cancel.is_set() else "failed"
                job.error = f"Render could not be completed: {str(e)[:160]}"
            finally:
                if job.status != "succeeded":
                    shutil.rmtree(job.dir, ignore_errors=True)
                self.q.task_done()

    def submit(self, manifest: dict) -> RenderJob:
        j = RenderJob(manifest); self.jobs[j.id] = j; self.q.put(j); return j

    def lookup(self, request: Request, job_id: str) -> RenderJob | None:
        job = self.jobs.get(job_id)
        supplied = request.headers.get("x-job-token", "")
        if not hmac.compare_digest(supplied.encode(), (job.token if job else "0" * 43).encode()) or job is None:
            return None
        return job


async def render_status(request: Request):
    env = _env_cached()
    return JSONResponse({"configured": True, "ready": bool(env.get("ffmpeg")), "renderer": "local-pillow-ffmpeg", "limits": wbcompat.LIMITS, "ephemeral": False,
                         "note": "silent 2D manifests render here; projects (HTML, 3D, timelines, footage) render through /api/jobs"})


async def render_submit(request: Request):
    try:
        x = await _json(request)
        if set(x) != {"manifest"}:
            raise ValueError("body must be {manifest}")
        m = wbcompat.validate_manifest(x["manifest"])
    except ValueError as e:
        return _err(f"Invalid or unsupported manifest: {e}", 422)
    j = request.app.state.render.submit(m)
    return JSONResponse({"job_id": j.id, "job_token": j.token, "status": j.status}, status_code=202)


async def render_job(request: Request):
    j = request.app.state.render.lookup(request, request.path_params["job_id"])
    if not j:
        return _err("Job unavailable", 404)
    if request.method == "DELETE":
        j.cancel.set(); j.status = "cancelled"; j.metadata = None
        return JSONResponse(j.public())
    return JSONResponse(j.public())


async def render_video(request: Request):
    j = request.app.state.render.lookup(request, request.path_params["job_id"])
    if not j:
        return _err("Job unavailable", 404)
    if j.status != "succeeded" or not j.video.exists():
        return _err("Video unavailable", 409)
    return FileResponse(j.video, media_type="video/mp4", filename="kosif-motion.mp4")


# ───────────────────────── the studio ─────────────────────────
_ENV: dict = {}


def _env_cached(ttl: float = 120.0) -> dict:
    if not _ENV or time.time() - _ENV.get("_t", 0) > ttl:
        try:
            import env_check
            _ENV.clear(); _ENV.update(env_check.check()); _ENV["_t"] = time.time()
        except Exception as e:  # noqa: BLE001
            _ENV.clear(); _ENV.update({"error": str(e)[:200], "_t": time.time()})
    return {k: v for k, v in _ENV.items() if k != "_t"}


async def env(request: Request):
    e = _env_cached()
    return JSONResponse({"version": VERSION, "home": str(HOME), "projects": str(_projects_dir()), "media": str(MEDIA), "out": str(OUT), "env": e,
                         "claude": claude_bridge.Settings(WB / "settings.json").public(), "python": sys.version.split()[0]})


async def recipes_list(request: Request):
    return JSONResponse({"groups": recipes.catalogue()})


async def jobs_list(request: Request):
    return JSONResponse({"jobs": request.app.state.runner.list()[:80]})


async def jobs_submit(request: Request):
    try:
        x = await _json(request)
        rid = str(x.get("recipe", ""))
        r = recipes.BY_ID.get(rid)
        if not r:
            raise ValueError(f"unknown recipe {rid!r}")
        args = recipes.build_args(r, x.get("args") or {})
    except ValueError as e:
        return _err(str(e), 400)
    job = request.app.state.runner.submit(rid, r["cmd"], args, str(x.get("note", ""))[:200])
    return JSONResponse(job.public(), status_code=202)


async def job_get(request: Request):
    j = request.app.state.runner.get(request.path_params["job_id"])
    return JSONResponse(j.public()) if j else _err("not found", 404)


async def job_cancel(request: Request):
    ok = request.app.state.runner.cancel(request.path_params["job_id"])
    return JSONResponse({"cancelled": ok}) if ok else _err("not found", 404)


async def job_log(request: Request):
    j = request.app.state.runner.get(request.path_params["job_id"])
    if not j:
        return _err("not found", 404)
    if request.url.path.endswith(".txt"):
        return PlainTextResponse("".join(j.lines))
    start = int(request.query_params.get("from", 0) or 0)

    def gen():
        sent = start
        while True:
            with j.lock:
                chunk = j.lines[sent:]
            for ln in chunk:
                yield f"data: {json.dumps(ln, ensure_ascii=False)}\n\n"
            sent += len(chunk)
            if j.status in ("done", "failed", "cancelled") and sent >= len(j.lines):
                yield f"event: end\ndata: {json.dumps(j.public(), ensure_ascii=False)}\n\n"
                return
            time.sleep(0.3)
    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"})


def _media_index() -> dict:
    p = MEDIA / ".index.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _media_index_save(d: dict):
    (MEDIA / ".index.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _probe(p: Path) -> dict | None:
    try:
        import tools
        info = tools.probe(p)
        return {"duration": round(info["duration"], 3), "video": info["video"], "audio": info["audio"]}
    except Exception:  # noqa: BLE001
        return None


async def media_list(request: Request):
    idx = _media_index()
    items = []
    for f in sorted(MEDIA.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if f.name.startswith(".") or not f.is_file():
            continue
        st = f.stat()
        meta = idx.get(f.name) or {}
        items.append({"name": f.name, "path": str(f), "url": f"/media/{f.name}", "bytes": st.st_size, "mtime": st.st_mtime, "ext": f.suffix.lower(),
                      "kind": "video" if f.suffix.lower() in (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v") else "audio" if f.suffix.lower() in (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")
                      else "image" if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif") else "data", **({"probe": meta.get("probe")} if meta.get("probe") else {})})
    return JSONResponse({"media": items, "dir": str(MEDIA)})


async def media_upload(request: Request):
    form = await request.form()
    saved = []
    idx = _media_index()
    for key, up in form.multi_items():
        if not hasattr(up, "filename"):
            continue
        try:
            name = _safe_name(up.filename or "file")
        except ValueError:
            continue
        if Path(name).suffix.lower() not in MEDIA_EXT:
            saved.append({"name": name, "error": "نوع ملف غير مدعوم"}); continue
        dst = MEDIA / name
        if dst.exists():
            stem, suf = Path(name).stem, Path(name).suffix
            dst = MEDIA / f"{stem}_{int(time.time())}{suf}"
        size = 0
        with dst.open("wb") as f:
            while True:
                chunk = await up.read(1 << 20)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_UPLOAD:
                    f.close(); dst.unlink(missing_ok=True)
                    saved.append({"name": name, "error": "الملف أكبر من الحد"}); break
                f.write(chunk)
        if dst.exists():
            pr = _probe(dst) if dst.suffix.lower() not in (".json", ".txt", ".srt") else None
            idx[dst.name] = {"probe": pr, "uploaded": time.time()}
            saved.append({"name": dst.name, "path": str(dst), "bytes": size, "probe": pr})
    _media_index_save(idx)
    return JSONResponse({"saved": saved})


async def media_delete(request: Request):
    try:
        name = _safe_name(request.path_params["name"])
    except ValueError:
        return _err("invalid name")
    p = MEDIA / name
    if not p.exists() or not _inside(p, [MEDIA]):
        return _err("not found", 404)
    p.unlink()
    idx = _media_index(); idx.pop(name, None); _media_index_save(idx)
    return JSONResponse({"deleted": name})


def _project_info(d: Path) -> dict:
    import motion
    idx = d / "index.html"
    info = {"name": d.name, "path": str(d), "has_index": idx.exists(), "mtime": d.stat().st_mtime, "preview": f"/projects/{d.name}/index.html" if idx.exists() else None}
    if idx.exists():
        try:
            html = idx.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'data-width="(\d+)"[^>]*data-height="(\d+)"', html)
            info["size"] = f"{m.group(1)}x{m.group(2)}" if m else None
            info["seconds"] = motion.duration_of(idx)
            info["kind"] = "3d" if re.search(r"three-kit|window\.K3", html) else "canvas" if "window.seek" in html else "manifest" if "kosif-site" in html else "2d"
        except OSError:
            pass
    for extra in ("template.json", "edit.json", "verse.json", "cues.json"):
        if (d / extra).exists():
            info.setdefault("files", []).append(extra)
    dirs = [OUT, Path(getattr(motion, "OUT_DIR", OUT)), d / "out"]               # the site's out/, the engine's out/, the project's own
    outs = sorted({p for od in dirs if od.exists() for p in od.glob(f"{d.name}*.mp4")} | {p for p in (d / "out").glob("*.mp4")} if (d / "out").exists() else
                  {p for od in dirs[:2] if od.exists() for p in od.glob(f"{d.name}*.mp4")}, key=lambda p: p.stat().st_mtime, reverse=True)
    info["outputs"] = [str(p) for p in outs[:6]]
    frames = sorted((d / "frames").glob("*.png")) if (d / "frames").exists() else []
    info["frames"] = [f"/projects/{d.name}/frames/{f.name}" for f in frames[:12]]
    return info


async def projects_list(request: Request):
    root = _projects_dir()
    items = [_project_info(d) for d in sorted(root.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True) if d.is_dir() and not d.name.startswith(".")] if root.exists() else []
    return JSONResponse({"projects": items, "dir": str(root)})


def _project_path(name: str, rel: str | None = None) -> Path:
    import motion
    d = _projects_dir() / motion.safe_name(name)
    if rel is None:
        return d
    p = (d / rel.replace("\\", "/")).resolve()
    if not _inside(p, [d]) or p.suffix.lower() not in TEXT_EXT:
        raise ValueError("path must be a text file inside the project")
    return p


async def project_create(request: Request):
    try:
        x = await _json(request)
        import motion
        kind = x.get("kind", "new"); name = motion.safe_name(str(x.get("name", "")))
        if kind == "template":
            import mtemplates
            d = mtemplates.create(name, str(x.get("template", "title-card")), dict(x.get("params") or {}), x.get("seconds"), int(x.get("fps", 30)), str(x.get("size", "1080x1920")))
        elif kind == "manifest":
            m = wbcompat.validate_manifest(x.get("manifest"))
            d = _projects_dir() / name; d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(wbcompat.project_html({k: v for k, v in m.items() if k != "frames"}), encoding="utf-8")
            (d / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        else:
            d = motion.new(name, float(x.get("seconds", 8)), int(x.get("fps", 30)), str(x.get("size", "1080x1920")), str(x.get("title", "")),
                           bool(x.get("three_d")), bool(x.get("canvas")), bool(x.get("lab")))
        return JSONResponse(_project_info(Path(d)), status_code=201)
    except SystemExit as e:
        return _err(str(e), 400)
    except (ValueError, OSError) as e:
        return _err(str(e), 400)


async def project_files(request: Request):
    try:
        d = _project_path(request.path_params["name"])
    except SystemExit as e:
        return _err(str(e))
    if not d.exists():
        return _err("not found", 404)
    files = [{"path": p.relative_to(d).as_posix(), "bytes": p.stat().st_size} for p in sorted(d.rglob("*"))
             if p.is_file() and p.suffix.lower() in TEXT_EXT and "assets" not in p.relative_to(d).parts and "node_modules" not in p.parts and p.stat().st_size < 2_000_000]
    return JSONResponse({"name": d.name, "files": files, "info": _project_info(d)})


async def project_file(request: Request):
    try:
        if request.method == "GET":
            p = _project_path(request.path_params["name"], request.query_params.get("path", "index.html"))
            if not p.exists():
                return _err("not found", 404)
            return JSONResponse({"path": request.query_params.get("path", "index.html"), "content": p.read_text(encoding="utf-8", errors="replace")})
        x = await _json(request)
        p = _project_path(request.path_params["name"], str(x.get("path", "index.html")))
        content = x.get("content")
        if not isinstance(content, str) or len(content) > 4_000_000:
            raise ValueError("content: a string up to 4 MB")
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            bak = p.with_suffix(p.suffix + ".bak"); shutil.copy2(p, bak)
        p.write_text(content, encoding="utf-8")
        return JSONResponse({"written": str(p), "bytes": len(content.encode("utf-8"))})
    except (ValueError, SystemExit) as e:
        return _err(str(e))


async def file_download(request: Request):
    raw = request.query_params.get("path", "")
    p = Path(raw)
    runner = request.app.state.runner
    known = {o for j in runner.jobs.values() for o in j.outputs}
    if not p.is_file() or not (_inside(p, ALLOWED_ROOTS + [_projects_dir()]) or str(p) in known):
        return _err("not found", 404)
    mt = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return FileResponse(p, media_type=mt, filename=p.name if request.query_params.get("download") else None)


async def timeline_validate(request: Request):
    try:
        x = await _json(request)
        import timeline
        spec = x.get("spec")
        if isinstance(spec, str):
            sp = Path(spec)
            if not sp.is_file() or not _inside(sp, ALLOWED_ROOTS):
                raise ValueError("spec path not found")
            res = timeline.summary(sp)
        else:
            res = timeline.summary(spec)
        return JSONResponse({"ok": True, **res})
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"ok": False, "error": str(e)[:400]}, status_code=400)


async def studio_import(request: Request):
    """A KOSIF Studio 6.0 project JSON → a timeline spec (saved under workbench/timelines) + the mapping report."""
    try:
        x = await _json(request)
        import studio_import as si
        project = x.get("project")
        if isinstance(project, str):
            project = json.loads(project)
        media = x.get("media_dir")
        mdir = Path(media) if media else MEDIA
        if not _inside(mdir, ALLOWED_ROOTS):
            raise ValueError("media_dir must be inside the studio home")
        spec, report = si.convert(project, mdir, x.get("size"))
        name = _safe_name(str(x.get("name") or report.get("name") or "studio"))
        p = TIMELINES / (Path(name).stem + ".json")
        p.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        return JSONResponse({"saved": str(p), "spec": spec, "report": report})
    except (ValueError, TypeError) as e:
        return _err(str(e)[:300])


async def timeline_list(request: Request):
    items = [{"name": p.stem, "path": str(p), "mtime": p.stat().st_mtime} for p in sorted(TIMELINES.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)]
    return JSONResponse({"timelines": items, "dir": str(TIMELINES)})


async def timeline_save(request: Request):
    try:
        x = await _json(request)
        name = _safe_name(str(x.get("name", "timeline")))
        spec = x.get("spec")
        if not isinstance(spec, dict):
            raise ValueError("spec must be an object")
        p = TIMELINES / (Path(name).stem + ".json")
        p.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        return JSONResponse({"saved": str(p)})
    except ValueError as e:
        return _err(str(e))


async def timeline_get(request: Request):
    try:
        p = TIMELINES / (Path(_safe_name(request.path_params["name"])).stem + ".json")
    except ValueError:
        return _err("invalid name")
    if not p.exists():
        return _err("not found", 404)
    return JSONResponse({"name": p.stem, "path": str(p), "spec": json.loads(p.read_text(encoding="utf-8"))})


async def timeline_example(request: Request):
    import timeline
    return JSONResponse({"spec": timeline.EXAMPLE, "transitions": timeline.transitions()})


async def transitions(request: Request):
    import timeline
    return JSONResponse({"transitions": [{"id": t, "ar": timeline.transition_ar(t)} for t in timeline.transitions()]})


# ───────────────────────── Claude ─────────────────────────
def _settings() -> claude_bridge.Settings:
    return claude_bridge.Settings(WB / "settings.json")


def _context(x: dict, request: Request) -> dict:
    ctx: dict = {"recipes": [{"id": r["id"], "ar": r["ar"], "fields": [f[0] for f in r["fields"]]} for _, _, rs in recipes.GROUPS for r in rs],
                 "paths": {"home": str(HOME), "media": str(MEDIA), "projects": str(_projects_dir()), "out": str(OUT)}}
    if x.get("media", True):
        idx = _media_index()
        ctx["media"] = [{"name": f.name, "path": str(f), "probe": (idx.get(f.name) or {}).get("probe")} for f in sorted(MEDIA.iterdir()) if f.is_file() and not f.name.startswith(".")][:60]
    if x.get("projects", True):
        root = _projects_dir()
        ctx["projects"] = [{"name": d.name, "seconds": _project_info(d).get("seconds")} for d in sorted(root.iterdir()) if d.is_dir()][:60] if root.exists() else []
    if x.get("project"):
        try:
            p = _project_path(str(x["project"]), str(x.get("project_file", "index.html")))
            if p.exists():
                ctx["project_file"] = {"project": x["project"], "path": x.get("project_file", "index.html"), "content": p.read_text(encoding="utf-8", errors="replace")[:40000]}
        except (ValueError, SystemExit):
            pass
    if x.get("timeline"):
        ctx["timeline"] = x["timeline"]
    if x.get("timeline_schema", True):
        import timeline
        ctx["timeline_schema"] = timeline.__doc__.split("Spec (")[1][:3000] if "Spec (" in (timeline.__doc__ or "") else ""
        ctx["transitions"] = timeline.transitions()
    return ctx


async def claude_status(request: Request):
    s = _settings()
    be = claude_bridge.backend(s)
    ok, msg = claude_bridge.cli_ready() if s.load().get("backend") in ("auto", "cli") else (False, "CLI غير مفعّل في الإعدادات")
    return JSONResponse({"backend": be, "cli": {"ready": ok, "message": msg}, "settings": s.public(), "mcp": f"{request.url.scheme}://{request.url.netloc}/mcp"})


async def claude_settings(request: Request):
    try:
        x = await _json(request)
        if x.get("backend") not in (None, "auto", "cli", "api", "mcp", "none"):
            raise ValueError("backend")
        _settings().save({k: v for k, v in x.items() if k in claude_bridge.DEFAULTS})
        return JSONResponse(_settings().public())
    except ValueError as e:
        return _err(str(e))


async def claude_ask(request: Request):
    try:
        x = await _json(request)
        task = str(x.get("task", "")).strip()
        if not task:
            raise ValueError("task required")
        ctx = _context(x.get("context") or {}, request)
        if request.url.path.endswith("/package"):
            return JSONResponse({"package": claude_bridge.package(task, ctx)})
        res = claude_bridge.ask(_settings(), task, ctx)
        return JSONResponse(res)
    except ValueError as e:
        return _err(str(e))
    except Exception as e:  # noqa: BLE001
        return _err(f"Claude: {str(e)[:300]}", 502)


async def claude_apply(request: Request):
    """Apply a plan (from Claude's reply or pasted): write project files, save a timeline, queue the actions."""
    try:
        x = await _json(request)
        plan = x.get("plan")
        if isinstance(plan, str):
            plan = claude_bridge.extract(plan)
        if not isinstance(plan, dict):
            raise ValueError("no JSON plan found in the reply")
        done: dict = {"files": [], "timeline": None, "jobs": [], "notes": plan.get("notes")}
        import motion
        for f in plan.get("files") or []:
            p = _project_path(str(f.get("project", "")), str(f.get("path", "index.html")))
            content = f.get("content")
            if not isinstance(content, str):
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists():
                shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
            p.write_text(content, encoding="utf-8")
            if p.name == "index.html":
                motion.sync_assets(p.parent)
            done["files"].append(str(p))
        if isinstance(plan.get("timeline"), dict):
            name = _safe_name(str(plan.get("timeline_name") or f"claude-{time.strftime('%Y%m%d-%H%M%S')}"))
            tp = TIMELINES / (Path(name).stem + ".json")
            tp.write_text(json.dumps(plan["timeline"], ensure_ascii=False, indent=1), encoding="utf-8")
            done["timeline"] = str(tp)
        for a in plan.get("actions") or []:
            r = recipes.BY_ID.get(str(a.get("recipe", "")))
            if not r:
                done["jobs"].append({"error": f"unknown recipe {a.get('recipe')}"}); continue
            try:
                args = recipes.build_args(r, a.get("args") or {})
            except ValueError as e:
                done["jobs"].append({"error": str(e)}); continue
            job = request.app.state.runner.submit(r["id"], r["cmd"], args, "claude")
            done["jobs"].append(job.public())
        return JSONResponse(done)
    except (ValueError, SystemExit) as e:
        return _err(str(e))


# ───────────────────────── MCP ─────────────────────────
MCP_TOOLS = [
    {"name": "motion_plan", "description": "Create a deterministic motion shot plan (kosif.proplan.v1); no media render.",
     "inputSchema": {"type": "object", "properties": {"task": {"type": "string", "maxLength": 5000}, "seconds": {"type": "number", "minimum": 2, "maximum": 600},
                                                      "fps": {"type": "number", "enum": wbcompat.FPS}, "aspect": {"type": "string", "enum": list(wbcompat.ASPECTS)}}, "required": ["task"]}},
    {"name": "motion_validate", "description": "Validate a kosif.proplan.v1 timeline.", "inputSchema": {"type": "object", "properties": {"plan": {"type": "object"}}, "required": ["plan"]}},
    {"name": "motion_compile", "description": "Compile a plan to a manifest and safe 2D HTML where supported. Does not execute.", "inputSchema": {"type": "object", "properties": {"plan": {"type": "object"}}, "required": ["plan"]}},
    {"name": "motion_templates", "description": "List template descriptions.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_env", "description": "What this studio PC can do (route A/B/C, ffmpeg, browser, whisper, fonts, face detector).", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_recipes", "description": "The recipe catalogue (every kmotion command the studio runs) with typed fields.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_run", "description": "Run a recipe as a background job (reel, direct, verse, audio2motion, montage, timeline, scenes, privacy, template, new, render, export, inspect…). Returns the job id; poll kosif_job.",
     "inputSchema": {"type": "object", "properties": {"recipe": {"type": "string"}, "args": {"type": "object"}, "note": {"type": "string"}}, "required": ["recipe"]}},
    {"name": "kosif_job", "description": "A job's status, outputs and the tail of its log.", "inputSchema": {"type": "object", "properties": {"job_id": {"type": "string"}, "tail": {"type": "integer"}}, "required": ["job_id"]}},
    {"name": "kosif_jobs", "description": "Recent jobs.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_media", "description": "The media library (files the user put in the studio, with probe data).", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_projects", "description": "The projects (compositions) with sizes, durations and renders.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_project_read", "description": "Read a text file of a project (index.html, edit.json, verse.json…).",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "path": {"type": "string"}}, "required": ["name"]}},
    {"name": "kosif_project_write", "description": "Write a text file into a project (a .bak of the old file is kept; index.html re-syncs the kit).",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "path": {"type": "string"}, "content": {"type": "string"}}, "required": ["name", "path", "content"]}},
    {"name": "kosif_project_create", "description": "Create a project: kind new (2D/3D/canvas/lab), template (motion template + params) or manifest (a compiled 2D manifest).",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "kind": {"type": "string", "enum": ["new", "template", "manifest"]}, "template": {"type": "string"},
                                                      "params": {"type": "object"}, "seconds": {"type": "number"}, "fps": {"type": "integer"}, "size": {"type": "string"}, "title": {"type": "string"},
                                                      "three_d": {"type": "boolean"}, "lab": {"type": "boolean"}, "canvas": {"type": "boolean"}, "manifest": {"type": "object"}}, "required": ["name"]}},
    {"name": "kosif_timeline_check", "description": "Validate a timeline spec and return its summary (clip durations, transitions, total).",
     "inputSchema": {"type": "object", "properties": {"spec": {"type": "object"}}, "required": ["spec"]}},
    {"name": "kosif_timeline_save", "description": "Save a timeline spec in the studio (then kosif_run timeline with spec=path).",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "spec": {"type": "object"}}, "required": ["name", "spec"]}},
    {"name": "kosif_transitions", "description": "The xfade transitions of this FFmpeg build.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_render_manifest", "description": "Render a kosif.motion.manifest.v1 locally (silent 2D MP4); returns job id + token; poll /api/render/jobs/ID.",
     "inputSchema": {"type": "object", "properties": {"manifest": {"type": "object"}}, "required": ["manifest"]}},
    {"name": "kosif_reviews", "description": "Films open for review on the review page (/review/NAME/): version, scenes, how many feedback rounds.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "kosif_review_init", "description": "Open a film for scene-by-scene review: a project folder (index.html), a timeline spec (.json) or a video; writes reel.json (next version) and returns the page URL.",
     "inputSchema": {"type": "object", "properties": {"target": {"type": "string"}, "video": {"type": "string"}, "title": {"type": "string"}, "name": {"type": "string"}}, "required": ["target"]}},
    {"name": "kosif_review_feedback", "description": "The last feedback the user sent from the review page: the prompt text, the edits (path → value), pinned notes, scene status.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "kosif_review_apply", "description": "Apply the bound edits of the last feedback to the source (timeline spec / kosif-props / :root colours); returns what is left for you (notes, motion, unbound edits) and the approved scenes not to touch.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
]


def _mcp_call(app, name: str, a: dict) -> dict:
    if name == "motion_templates":
        return {"templates": wbcompat.TEMPLATES}
    if name == "motion_plan":
        return wbcompat.make_plan(a)
    if name == "motion_validate":
        return wbcompat.validate_plan(a.get("plan"))
    if name == "motion_compile":
        return wbcompat.compile_plan(a.get("plan"))
    if name == "kosif_env":
        return _env_cached()
    if name == "kosif_reviews":
        return {"reviews": _review_mod().list_reels()}
    if name == "kosif_review_init":
        rv = _review_mod()
        return rv.init(Path(str(a["target"])), Path(str(a["video"])) if a.get("video") else None, a.get("title"), a.get("name"))
    if name == "kosif_review_feedback":
        return _review_mod().latest_feedback(str(a["name"]))
    if name == "kosif_review_apply":
        return _review_mod().apply(str(a["name"]))
    if name == "kosif_recipes":
        return {"groups": recipes.catalogue()}
    if name == "kosif_run":
        r = recipes.BY_ID.get(str(a.get("recipe", "")))
        if not r:
            raise ValueError(f"unknown recipe {a.get('recipe')!r}")
        job = app.state.runner.submit(r["id"], r["cmd"], recipes.build_args(r, a.get("args") or {}), str(a.get("note", "mcp"))[:200])
        return job.public()
    if name == "kosif_job":
        j = app.state.runner.get(str(a.get("job_id", "")))
        if not j:
            raise ValueError("job not found")
        tail = int(a.get("tail", 40) or 40)
        return {**j.public(), "log_tail": "".join(j.lines[-tail:])}
    if name == "kosif_jobs":
        return {"jobs": app.state.runner.list()[:30]}
    if name == "kosif_media":
        idx = _media_index()
        return {"media": [{"name": f.name, "path": str(f), "bytes": f.stat().st_size, "probe": (idx.get(f.name) or {}).get("probe")} for f in sorted(MEDIA.iterdir()) if f.is_file() and not f.name.startswith(".")]}
    if name == "kosif_projects":
        root = _projects_dir()
        return {"projects": [_project_info(d) for d in sorted(root.iterdir()) if d.is_dir() and not d.name.startswith(".")] if root.exists() else []}
    if name == "kosif_project_read":
        p = _project_path(str(a.get("name", "")), str(a.get("path", "index.html")))
        if not p.exists():
            raise ValueError("file not found")
        return {"path": str(p), "content": p.read_text(encoding="utf-8", errors="replace")}
    if name == "kosif_project_write":
        import motion
        p = _project_path(str(a.get("name", "")), str(a.get("path", "index.html")))
        content = a.get("content")
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
        p.write_text(content, encoding="utf-8")
        if p.name == "index.html":
            motion.sync_assets(p.parent)
        return {"written": str(p)}
    if name == "kosif_project_create":
        import motion
        name_ = motion.safe_name(str(a.get("name", "")))
        kind = a.get("kind", "new")
        if kind == "template":
            import mtemplates
            d = mtemplates.create(name_, str(a.get("template", "title-card")), dict(a.get("params") or {}), a.get("seconds"), int(a.get("fps", 30)), str(a.get("size", "1080x1920")))
        elif kind == "manifest":
            m = wbcompat.validate_manifest(a.get("manifest"))
            d = _projects_dir() / name_; d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(wbcompat.project_html({k: v for k, v in m.items() if k != "frames"}), encoding="utf-8")
        else:
            d = motion.new(name_, float(a.get("seconds", 8)), int(a.get("fps", 30)), str(a.get("size", "1080x1920")), str(a.get("title", "")), bool(a.get("three_d")), bool(a.get("canvas")), bool(a.get("lab")))
        return _project_info(Path(d))
    if name == "kosif_timeline_check":
        import timeline
        return timeline.summary(a.get("spec"))
    if name == "kosif_timeline_save":
        p = TIMELINES / (Path(_safe_name(str(a.get("name", "timeline")))).stem + ".json")
        if not isinstance(a.get("spec"), dict):
            raise ValueError("spec must be an object")
        p.write_text(json.dumps(a["spec"], ensure_ascii=False, indent=1), encoding="utf-8")
        return {"saved": str(p)}
    if name == "kosif_transitions":
        import timeline
        return {"transitions": timeline.transitions()}
    if name == "kosif_render_manifest":
        m = wbcompat.validate_manifest(a.get("manifest"))
        j = app.state.render.submit(m)
        return {"job_id": j.id, "job_token": j.token, "status": j.status, "poll": f"/api/render/jobs/{j.id}"}
    raise ValueError("Unknown tool")


async def mcp(request: Request):
    if request.method == "GET":
        return JSONResponse({"name": "kosif-motion-web", "version": VERSION, "transport": "json-rpc over POST", "tools": [t["name"] for t in MCP_TOOLS]})
    rid = None
    try:
        q = await _json(request)
        rid = q.get("id")
        def reply(result):
            return JSONResponse({"jsonrpc": "2.0", "id": rid, "result": result})
        if q.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC")
        method = q.get("method")
        if method == "notifications/initialized":
            return Response(status_code=202)
        if method == "initialize":
            return reply({"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "serverInfo": {"name": "kosif-motion-web", "version": VERSION}})
        if method == "tools/list":
            return reply({"tools": MCP_TOOLS})
        if method == "ping":
            return reply({})
        if method == "tools/call":
            params = q.get("params") or {}
            result = _mcp_call(request.app, str(params.get("name")), params.get("arguments") or {})
            return reply({"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}], "structuredContent": result})
        return JSONResponse({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}})
    except (ValueError, SystemExit) as e:
        return JSONResponse({"jsonrpc": "2.0", "id": rid, "error": {"code": -32602, "message": str(e) or "Invalid request"}})
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"jsonrpc": "2.0", "id": rid, "error": {"code": -32603, "message": str(e)[:300]}})



# ───────────────────────── review (the Motion OS page, MIT, on the KOSIF engine) ─────────────────────────
def _review_mod():
    import review
    return review


def _review_folder(name: str) -> Path:
    try:
        return _review_mod().folder_of(name)
    except SystemExit as e:
        raise FileNotFoundError(str(e))


async def reviews_list(request: Request):
    return JSONResponse({"reviews": _review_mod().list_reels()})


async def review_create(request: Request):
    x = await request.json()
    target = Path(str(x.get("target") or ""))
    if not str(target) or not target.exists():
        return JSONResponse({"error": f"not found: {target}"}, status_code=400)
    try:
        r = _review_mod().init(target, Path(x["video"]) if x.get("video") else None, x.get("title"), x.get("name"))
    except (ValueError, SystemExit) as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    return JSONResponse(r)


async def review_page(request: Request):
    name = request.path_params["name"]
    try:
        _review_folder(name)
    except FileNotFoundError as e:
        return PlainTextResponse(str(e), status_code=404)
    if not request.url.path.endswith("/"):
        from starlette.responses import RedirectResponse
        return RedirectResponse(f"/review/{name}/")
    return FileResponse(STATIC / "review" / "index.html", media_type="text/html", headers={"cache-control": "no-store"})


async def review_file(request: Request):
    name, rel = request.path_params["name"], request.path_params["path"]
    try:
        folder = _review_folder(name)
    except FileNotFoundError as e:
        return PlainTextResponse(str(e), status_code=404)
    f = (folder / rel).resolve()
    if folder not in f.parents or not f.is_file():
        return PlainTextResponse("not found", status_code=404)
    return FileResponse(f, headers={"cache-control": "no-store"})


async def review_feedback(request: Request):
    name = request.path_params["name"]
    try:
        _review_folder(name)
        if request.method == "GET":
            return JSONResponse(_review_mod().latest_feedback(name))
        fb = await request.json()
        if not isinstance(fb, dict) or len(json.dumps(fb)) > 2_000_000:
            return JSONResponse({"error": "feedback must be a JSON object under 2 MB"}, status_code=400)
        return JSONResponse(_review_mod().save_feedback(name, fb))
    except FileNotFoundError as e:
        return JSONResponse({"error": str(e)}, status_code=404)


async def review_export(request: Request):
    """The page's Export button: GET → {state, pct, line, out}; POST {over, boxes} → a `kmotion review export` job."""
    name = request.path_params["name"]
    try:
        folder = _review_folder(name)
    except FileNotFoundError as e:
        return JSONResponse({"state": "error", "line": str(e)}, status_code=404)
    runner = request.app.state.runner
    jid = request.app.state.review_jobs.get(name)
    j = runner.get(jid) if jid else None
    if request.method == "POST" and not (j and j.status in ("queued", "running")):
        body = await request.json()
        props = folder / "review" / "export-props.json"; props.parent.mkdir(exist_ok=True)
        props.write_text(json.dumps({"over": (body or {}).get("over") or {}}, ensure_ascii=False), encoding="utf-8")
        j = runner.submit("review-export", "review", ["export", name, "--props", str(props)], "review page")
        request.app.state.review_jobs[name] = j.id
    if not j:
        return JSONResponse({"state": "idle"})
    tail = "".join(j.lines[-3:]).strip().splitlines()
    m = [x for x in re.findall(r"(\d+)/(\d+)", "".join(j.lines[-6:])) if int(x[1]) > 0]
    pct = min(99, round(int(m[-1][0]) / int(m[-1][1]) * 100)) if m else 0
    state = {"queued": "running", "running": "running", "done": "done"}.get(j.status, "error")
    out = ""
    if state == "done":
        out = json.loads((folder / "reel.json").read_text(encoding="utf-8")).get("src", "")
        pct = 100
    return JSONResponse({"state": state, "pct": pct, "line": (tail[-1] if tail else "")[:200], "out": out, "job": j.id})


# ───────────────────────── app ─────────────────────────
async def index(request: Request):
    return FileResponse(STATIC / "index.html", media_type="text/html")


def create_app(workers: int = 2) -> Starlette:
    routes = [
        Route("/", index),
        Route("/api/health", health), Route("/api/templates", templates),
        Route("/api/plan", compat_post, methods=["POST"]), Route("/api/validate", compat_post, methods=["POST"]), Route("/api/compile", compat_post, methods=["POST"]),
        Route("/api/render/status", render_status),
        Route("/api/render/jobs", render_submit, methods=["POST"]),
        Route("/api/render/jobs/{job_id}", render_job, methods=["GET", "DELETE"]),
        Route("/api/render/jobs/{job_id}/video", render_video),
        Route("/api/env", env), Route("/api/recipes", recipes_list), Route("/api/transitions", transitions),
        Route("/api/jobs", jobs_list), Route("/api/jobs", jobs_submit, methods=["POST"]),
        Route("/api/jobs/{job_id}", job_get), Route("/api/jobs/{job_id}/cancel", job_cancel, methods=["POST"]),
        Route("/api/jobs/{job_id}/log", job_log), Route("/api/jobs/{job_id}/log.txt", job_log),
        Route("/api/media", media_list), Route("/api/media", media_upload, methods=["POST"]), Route("/api/media/{name}", media_delete, methods=["DELETE"]),
        Route("/api/projects", projects_list), Route("/api/projects", project_create, methods=["POST"]),
        Route("/api/projects/{name}/files", project_files), Route("/api/projects/{name}/file", project_file, methods=["GET", "POST", "PUT"]),
        Route("/api/file", file_download),
        Route("/api/timeline/validate", timeline_validate, methods=["POST"]), Route("/api/timeline/list", timeline_list),
        Route("/api/studio/import", studio_import, methods=["POST"]),
        Route("/api/timeline/save", timeline_save, methods=["POST"]), Route("/api/timeline/example", timeline_example), Route("/api/timeline/{name}", timeline_get),
        Route("/api/claude/status", claude_status), Route("/api/claude/settings", claude_settings, methods=["POST"]),
        Route("/api/claude/ask", claude_ask, methods=["POST"]), Route("/api/claude/package", claude_ask, methods=["POST"]), Route("/api/claude/apply", claude_apply, methods=["POST"]),
        Route("/mcp", mcp, methods=["GET", "POST"]),
        Route("/api/reviews", reviews_list), Route("/api/reviews", review_create, methods=["POST"]),
        Route("/review/{name}", review_page), Route("/review/{name}/", review_page),
        Route("/review/{name}/feedback", review_feedback, methods=["GET", "POST"]),
        Route("/review/{name}/export", review_export, methods=["GET", "POST"]),
        Route("/review/{name}/{path:path}", review_file),
        Mount("/static", StaticFiles(directory=str(STATIC)), name="static"),
        Mount("/media", StaticFiles(directory=str(MEDIA)), name="media"),
    ]
    if (STATIC / "studio" / "index.html").exists():                               # KOSIF Studio 6.0 (the v4 browser editor) + its examples
        routes.append(Mount("/studio", StaticFiles(directory=str(STATIC / "studio"), html=True), name="studio"))
    if (STATIC / "examples").exists():
        routes.append(Mount("/examples", StaticFiles(directory=str(STATIC / "examples"), html=True), name="examples"))
    pdir = _projects_dir()
    pdir.mkdir(parents=True, exist_ok=True)
    routes.append(Mount("/projects", StaticFiles(directory=str(pdir)), name="projects"))
    from starlette.middleware import Middleware
    app = Starlette(routes=routes, middleware=[Middleware(_Headers)])
    app.state.runner = jobs_mod.Runner(JOBS, HOME, workers)
    app.state.render = RenderEngine()
    app.state.review_jobs = {}
    return app


LOCAL_HOSTS = {"127.0.0.1", "localhost", "[::1]"}


def _foreign_origin(scope) -> bool:
    """A state-changing request from another website's page (its browser sends Origin / Sec-Fetch-Site) is refused:
    the server listens on loopback, but any page open in the user's browser could otherwise post to it. Tools like
    curl and the site's own pages (same origin, or no Origin at all) pass."""
    if scope.get("method", "GET") in ("GET", "HEAD", "OPTIONS"):
        return False
    headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
    sfs = headers.get("sec-fetch-site")
    if sfs in ("cross-site", "same-site"):
        return True
    origin = headers.get("origin")
    if origin and origin != "null":
        host = origin.split("://", 1)[-1].split("/", 1)[0].rsplit(":", 1)[0]
        return host not in LOCAL_HOSTS
    return False


class _Headers:
    """no-store on the API, nosniff everywhere, and the foreign-origin guard (pure ASGI; Starlette ≥ 1 has no @app.middleware)."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        path = scope.get("path", "")
        if (path.startswith("/api/") or path.startswith("/review/") or path == "/mcp") and _foreign_origin(scope):
            body = b'{"error":"cross-origin request refused: the studio API answers only its own pages"}'
            await send({"type": "http.response.start", "status": 403, "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())]})
            await send({"type": "http.response.body", "body": body})
            return

        async def send_wrapped(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-content-type-options", b"nosniff"))
                if path.startswith("/api/") or path == "/mcp":
                    headers.append((b"cache-control", b"no-store"))
                message = {**message, "headers": headers}
            await send(message)
        await self.app(scope, receive, send_wrapped)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1"); ap.add_argument("--port", type=int, default=8766)
    ap.add_argument("--workers", type=int, default=2, help="recipe jobs run at once"); ap.add_argument("--open", action="store_true", help="open the browser")
    a = ap.parse_args()
    import uvicorn
    app = create_app(a.workers)
    url = f"http://{a.host}:{a.port}/"
    print(f"KOSIF Motion Web v{VERSION} — {url}   (home: {HOME})")
    if a.open:
        import webbrowser
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")


if __name__ == "__main__":
    main()
