#!/usr/bin/env python3
"""Daily dua story video: one config (date, dua lines with times, watermark, audio) -> 1080x1920 MP4.

  python3 workflows/dua-daily/scripts/dua_daily.py build  <config.json> --job <dir>
  python3 workflows/dua-daily/scripts/dua_daily.py stills --job <dir>          # one PNG per line + a grid
  python3 workflows/dua-daily/scripts/dua_daily.py render --job <dir> [--out film.mp4] [--preview]

The weekday and the Umm al-Qura Hijri date are computed in the page from `date`
(override with `dayLabel`, `hijriDay`, `hijriMonth`). The page is drawn at 720x1280 CSS
pixels and rendered at device scale 1.5, so the film is 1080x1920, 30 fps, through
tools/render_html.cjs (export standard; the audio is stream-copied when its codec allows).
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
RENDER = REPO / "tools" / "render_html.cjs"


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    segs = cfg.get("segments") or []
    if not segs:
        raise SystemExit("config has no segments")
    last = 0.0
    for i, s in enumerate(segs):
        if not str(s.get("text", "")).strip():
            raise SystemExit(f"segment {i + 1} has no text")
        if not (float(s["start"]) >= last - 1e-6 and float(s["end"]) > float(s["start"])):
            raise SystemExit(f"segment {i + 1}: times must rise ({s['start']} -> {s['end']})")
        last = float(s["end"])
    if not str(cfg.get("date", "")).count("-") == 2:
        raise SystemExit("date must be YYYY-MM-DD")
    return cfg


def build(cfg_path: Path, job: Path) -> Path:
    cfg = load_config(cfg_path)
    job.mkdir(parents=True, exist_ok=True)
    if cfg.get("audio"):
        audio = Path(cfg["audio"]).expanduser()
        if not audio.is_absolute():
            audio = (cfg_path.parent / audio).resolve()
        if not audio.exists():
            raise SystemExit(f"audio not found: {audio}")
        cfg["audio"] = str(audio)
    shutil.copytree(HERE / "fonts", job / "fonts", dirs_exist_ok=True)
    page = (HERE / "template.html").read_text(encoding="utf-8")
    inject = "<script>window.__DUA_CFG=" + json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n"
    page = page.replace("<script>\nconst W=", inject + "<script>\nconst W=", 1)
    if "__DUA_CFG=" not in page:
        raise SystemExit("template changed: could not inject the config")
    (job / "index.html").write_text(page, encoding="utf-8")
    (job / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"built {job / 'index.html'} ({len(cfg['segments'])} lines, {cfg['segments'][-1]['end']} s)")
    return job / "index.html"


def node(args: list) -> int:
    cmd = ["node", str(RENDER), *args]
    print("+ " + " ".join(cmd), file=sys.stderr)
    return subprocess.call(cmd)


def render(job: Path, out: Path, preview: bool) -> int:
    cfg = json.loads((job / "config.json").read_text(encoding="utf-8"))
    args = ["--in", str(job / "index.html"), "--out", str(out), "--width", "720", "--height", "1280",
            "--scale", "1.5", "--fps", str(cfg.get("fps", 30)), "--mode", "seek",
            "--report", str(job / "render_report.json")]
    if cfg.get("audio"):
        args += ["--audio", cfg["audio"]]
    if preview:
        args.append("--preview")
    return node(args)


def stills(job: Path) -> int:
    cfg = json.loads((job / "config.json").read_text(encoding="utf-8"))
    times = ",".join(f"{(s['start'] + s['end']) / 2:.2f}" for s in cfg["segments"])
    return node(["--in", str(job / "index.html"), "--out", str(job / "stills.mp4"), "--width", "720",
                 "--height", "1280", "--scale", "1.5", "--mode", "seek", "--stills", times,
                 "--stills-dir", str(job / "stills")])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("config", type=Path); b.add_argument("--job", type=Path, required=True)
    s = sub.add_parser("stills"); s.add_argument("--job", type=Path, required=True)
    r = sub.add_parser("render"); r.add_argument("--job", type=Path, required=True)
    r.add_argument("--out", type=Path); r.add_argument("--preview", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        build(a.config, a.job); return 0
    if a.cmd == "stills":
        return stills(a.job)
    return render(a.job, a.out or a.job / "film.mp4", a.preview)


if __name__ == "__main__":
    sys.exit(main())
