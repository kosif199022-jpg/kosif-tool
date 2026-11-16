#!/usr/bin/env python3
"""Black Dragon launcher: one command on claude.ai (cloud) and on the owner's PC.

    python3 scripts/dragon.py where              # which place am I in, which engine copy, which tools exist
    python3 scripts/dragon.py setup [--full]     # install what is missing for this place (pip; PC: also winget plan)
    python3 scripts/dragon.py <dragon command>   # find / show / verify / cut / beats / words / mix / film / engines / run ...
    python3 scripts/dragon.py tool <name> ...    # bundled tools: arena, 3d, motion, cartoon, stickman, stock

Place detection (no flags needed):
  * PC     : a local black-dragon repo exists (DRAGON_HOME, Desktop\\التنين الأسود, ~/kosif-own/black-dragon).
             It is used directly, so local skills, old repos, Blender, yt-dlp and GPU models are all in reach.
  * cloud  : no local repo (claude.ai sandbox, /mnt/user-data present). The engine bundled in app/ is copied
             to a writable folder (/tmp/dragon) and used there. Outputs go to /mnt/user-data/outputs.
Override with DRAGON_MODE=pc|cloud or DRAGON_HOME=<folder>.
"""
import json, os, platform, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
APP = SKILL / "app"
HOME = Path.home()
PC_CANDIDATES = [
    HOME / "OneDrive" / "Desktop" / "التنين الأسود",
    HOME / "Desktop" / "التنين الأسود",
    HOME / "kosif-own" / "black-dragon",
]
OLD_REPOS = {"kosif-tool": HOME / "kosif-own" / "kosif-tool", "kosif-atlas": HOME / "kosif-own" / "kosif-atlas",
             "100-superskills": HOME / "kosif-own" / "100-superskills", "fastify-motion-bro": HOME / "kosif-own" / "fastify-motion-bro"}
PROGRAMS = ["ffmpeg", "ffprobe", "node", "blender", "yt-dlp", "magick", "tesseract", "auto-editor", "nvidia-smi", "git"]
TOOLS = {  # name -> script inside the skill
    "arena": "tools/arena/bracket.py",
    "3d": "tools/studio/build_studio.py",
    "motion": "tools/studio/motion_styles.py",
    "stickman": "tools/stickman/stickman_kit.py",
    "stock": "tools/stock/free_photos.py",
}
PIP_CORE = ["librosa", "soundfile", "pyloudnorm", "opencv-python-headless", "arabic_reshaper", "python-bidi",
            "scenedetect", "auto-editor", "yt-dlp", "pytest"]
PIP_FULL = ["faster-whisper"]          # word timings
PIP_GPU = ["whisperx", "demucs"]       # only where a GPU (or patience) exists
WINGET = {"ffmpeg": "Gyan.FFmpeg", "node": "OpenJS.NodeJS.LTS", "blender": "BlenderFoundation.Blender",
          "yt-dlp": "yt-dlp.yt-dlp", "magick": "ImageMagick.ImageMagick", "tesseract": "UB-Mannheim.TesseractOCR"}


def is_cloud_box():
    return Path("/mnt/user-data").exists() or os.environ.get("CLAUDE_CODE_REMOTE") == "true"


def detect():
    forced = os.environ.get("DRAGON_MODE")
    home = os.environ.get("DRAGON_HOME")
    if home and (Path(home) / "dragon" / "cli.py").exists():
        return (forced or ("cloud" if is_cloud_box() else "pc")), Path(home)
    if forced != "cloud":
        for c in PC_CANDIDATES:
            if (c / "dragon" / "cli.py").exists():
                return "pc", c
    if forced == "pc" or (not is_cloud_box() and platform.system() in ("Windows", "Darwin")):
        return "pc", HOME / ".black-dragon" / "app"      # PC without the repo: use the bundled copy
    return "cloud", Path("/tmp/dragon")


def ensure_home(mode, home):
    if (home / "dragon" / "cli.py").exists():
        return home
    home.mkdir(parents=True, exist_ok=True)
    shutil.copytree(APP, home, dirs_exist_ok=True)
    return home


def where():
    mode, home = detect()
    info = {
        "mode": mode, "os": platform.system(), "dragon_home": str(home),
        "uses_bundled_engine": not any(home == c for c in PC_CANDIDATES),
        "programs": {p: bool(shutil.which(p)) for p in PROGRAMS},
        "old_repos": {k: v.exists() for k, v in OLD_REPOS.items()},
        "outputs": "/mnt/user-data/outputs" if Path("/mnt/user-data").exists() else str(Path.cwd()),
    }
    info["gpu"] = info["programs"]["nvidia-smi"]
    info["route"] = (
        "PC: full power. Use local repos (kosif-tool video_protocol, dragon-montage stations), Blender, yt-dlp, GPU models when present."
        if mode == "pc" else
        "Cloud: bundled engine only. No Blender/GPU; YouTube/TikTok downloads are often blocked, ask the user to upload the file."
    )
    return info


def run(args, home=None):
    env = dict(os.environ)
    if home:
        env["PYTHONPATH"] = str(home) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.call([sys.executable] + args, env=env)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd = argv[0]
    if cmd == "where":
        print(json.dumps(where(), ensure_ascii=False, indent=1)); return 0
    if cmd == "setup":
        mode, home = detect(); home = ensure_home(mode, home)
        pkgs = PIP_CORE + (PIP_FULL if "--full" in argv else []) + (PIP_GPU if "--gpu" in argv else [])
        subprocess.call([sys.executable, "-m", "pip", "install", "-q", "--disable-pip-version-check"] + pkgs)
        info = where()
        if mode == "pc" and platform.system() == "Windows":
            miss = [p for p, ok in info["programs"].items() if not ok and p in WINGET]
            if miss:
                print("missing programs on this PC (install with your OK):")
                for p in miss:
                    print(f"  winget install -e --id {WINGET[p]}")
        run(["-m", "dragon", "doctor"], home=home)
        print(f"mode={mode}  DRAGON_HOME={home}")
        return 0
    if cmd == "tool":
        if len(argv) < 2 or argv[1] not in TOOLS and argv[1] != "cartoon":
            print("tools:", ", ".join(list(TOOLS) + ["cartoon"])); return 2
        if argv[1] == "cartoon":
            print(f"cartoon kit: {SKILL / 'tools' / 'cartoon'}  ->  bash tools/setup.sh <project dir>  (see references/skills/cartoon-short.md)")
            return 0
        return run([str(SKILL / TOOLS[argv[1]])] + argv[2:])
    mode, home = detect(); home = ensure_home(mode, home)
    return run(["-m", "dragon"] + argv, home=home)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
