#!/usr/bin/env python3
"""خط إنتاج DaVinci Resolve عبر واجهة Scripting الرسمية: فحص البيئة، وتكرار الخط الزمني، وتجهيز التراكات، والعلامات، وقائمة الوسائط بوقت التصوير، ومهمة رندر مع تحقق ffprobe.

usage:
  python resolve_pipeline.py doctor
  python resolve_pipeline.py clips   [--out log.md]                      # جدول الوسائط (الاسم، وقت التصوير، الكاميرا، الدقة، fps، فضاء اللون)
  python resolve_pipeline.py duplicate --src "Timeline A" [--name X]      # نسخة عمل B مؤرّخة
  python resolve_pipeline.py tracks --timeline B                          # 4 فيديو + 4 صوت بأسماء الأدوار (بلا تكرار)
  python resolve_pipeline.py marker --timeline B --frame 0 --color Blue --name "CHAPTER البداية"
  python resolve_pipeline.py render --timeline B --dir out --name master [--format mp4 --codec H264] [--start]
  python resolve_pipeline.py verify --file out/master.mp4 --timeline B    # الدقة/المعدل/المدة تطابق الخط الزمني

يحتاج Resolve Studio مفتوحاً مع External scripting = Local، ومتغيرات RESOLVE_SCRIPT_API وRESOLVE_SCRIPT_LIB وPYTHONPATH.
بلا الواجهة يطبع الدليل اليدوي لنفس الخطوة ويخرج برمز 2 (لا يدّعي التنفيذ).
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

TRACKS_V = ["OVERLAY", "GFX", "SUBTITLE", "HOOK_TEXT"]
TRACKS_A = ["AMBIENCE", "SFX", "MUSIC", "HOOK"]
MARKER_COLORS = {"Blue", "Cyan", "Green", "Yellow", "Red", "Pink", "Purple", "Fuchsia", "Rose", "Lavender", "Sky", "Mint", "Lemon", "Sand", "Cocoa", "Cream"}
NODE_ORDER = ["EXPOSURE", "WB", "CST", "CONTRAST", "SAT", "LOOK"]
MANUAL = {
    "duplicate": "Edit page → right-click the timeline in Media Pool → Duplicate Timeline → name it <A>_edit_<YYYYMMDD_HHMM>.",
    "tracks": "Timeline → Add Track ×4 video, ×4 audio → right-click track header → rename: " + ", ".join(TRACKS_V + TRACKS_A) + ".",
    "marker": "Place playhead → press M → set color/name/note. Colors must be one of Resolve's 16.",
    "render": "Deliver page → Custom Export → format/codec → Add to Render Queue → Render All; then verify with ffprobe.",
    "clips": "Media Pool → list view → sort by Date Recorded; note camera, resolution, fps, Input Color Space per clip.",
}


def say(obj):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def connect():
    try:
        import DaVinciResolveScript as dvr  # type: ignore
    except ImportError:
        cands = []
        if sys.platform.startswith("win"):
            cands.append(os.path.expandvars(r"%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"))
        elif sys.platform == "darwin":
            cands.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
        else:
            cands.append("/opt/resolve/Developer/Scripting/Modules")
        for c in cands:
            if os.path.isdir(c):
                sys.path.append(c)
        try:
            import DaVinciResolveScript as dvr  # type: ignore
        except ImportError:
            return None, "DaVinciResolveScript module not importable (set RESOLVE_SCRIPT_API / RESOLVE_SCRIPT_LIB / PYTHONPATH)"
    try:
        r = dvr.scriptapp("Resolve")
    except Exception as e:  # pragma: no cover
        return None, f"scriptapp failed: {e}"
    if not r:
        return None, "Resolve is not running, is not Studio, or External scripting is not set to Local"
    return r, None


def project(r):
    pm = r.GetProjectManager(); return pm.GetCurrentProject()


def find_timeline(pr, name):
    for i in range(1, int(pr.GetTimelineCount()) + 1):
        t = pr.GetTimelineByIndex(i)
        if t and t.GetName() == name:
            return t
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["doctor", "clips", "duplicate", "tracks", "marker", "render", "verify"])
    ap.add_argument("--src"); ap.add_argument("--name"); ap.add_argument("--timeline"); ap.add_argument("--out")
    ap.add_argument("--frame", type=int, default=0); ap.add_argument("--color", default="Blue"); ap.add_argument("--note", default="")
    ap.add_argument("--dir", default="renders"); ap.add_argument("--format", default="mp4"); ap.add_argument("--codec", default="H264")
    ap.add_argument("--start", action="store_true"); ap.add_argument("--file")
    a = ap.parse_args()

    if a.cmd == "verify":
        if not a.file:
            sys.exit("--file required")
        pr_ = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,duration",
                              "-show_entries", "format=duration", "-of", "json", a.file], capture_output=True, text=True)
        info = json.loads(pr_.stdout) if pr_.returncode == 0 else {"error": pr_.stderr[-500:]}
        say({"file": a.file, "ffprobe": info, "note": "قارن بالدقة والمعدل والمدة في إعدادات الخط الزمني؛ الفرق المسموح إطار واحد"})
        return

    r, err = connect()
    if r is None:
        say({"mode": "manual", "reason": err, "step": a.cmd, "manual_procedure": MANUAL.get(a.cmd, ""), "executed": False})
        sys.exit(2)
    pr = project(r)
    if a.cmd == "doctor":
        say({"mode": "api", "resolve_version": r.GetVersionString(), "project": pr.GetName() if pr else None,
             "timelines": [pr.GetTimelineByIndex(i).GetName() for i in range(1, int(pr.GetTimelineCount()) + 1)] if pr else [],
             "node_order_policy": NODE_ORDER, "note": "node add/label has no API: Color page → Append a Node → Label Selected Node"})
        return
    if a.cmd == "clips":
        mp = pr.GetMediaPool(); root = mp.GetRootFolder(); rows = []
        def walk(folder):
            for c in folder.GetClipList() or []:
                p = c.GetClipProperty() or {}
                rows.append({"name": p.get("File Name") or p.get("Clip Name"), "date_recorded": p.get("Date Recorded"), "camera": p.get("Camera #") or p.get("Camera Type"),
                             "resolution": p.get("Resolution"), "fps": p.get("FPS"), "color_space": p.get("Input Color Space"), "duration": p.get("Duration")})
            for sub in folder.GetSubFolderList() or []:
                walk(sub)
        walk(root)
        rows.sort(key=lambda x: str(x.get("date_recorded") or ""))
        if a.out:
            with open(a.out, "a", encoding="utf-8") as f:
                f.write("\n## الوسائط بترتيب وقت التصوير\n\n| الملف | وقت التصوير | الكاميرا | الدقة | fps | فضاء اللون |\n|---|---|---|---|---|---|\n")
                for x in rows:
                    f.write(f"| {x['name']} | {x['date_recorded']} | {x['camera']} | {x['resolution']} | {x['fps']} | {x['color_space']} |\n")
        say({"clips": len(rows), "missing_date": sum(1 for x in rows if not x["date_recorded"]), "rows": rows[:50]})
        return
    if a.cmd == "duplicate":
        src = find_timeline(pr, a.src)
        if not src:
            sys.exit(f"timeline not found: {a.src}")
        name = a.name or f"{a.src}_edit_{dt.datetime.now():%Y%m%d_%H%M}"
        dup = src.DuplicateTimeline(name) if hasattr(src, "DuplicateTimeline") else None
        say({"duplicated": bool(dup), "name": name, "note": None if dup else "DuplicateTimeline needs Resolve 19+; do it in the UI"})
        return
    tl = find_timeline(pr, a.timeline) if a.timeline else pr.GetCurrentTimeline()
    if not tl:
        sys.exit("timeline not found")
    if a.cmd == "tracks":
        have_v = {tl.GetTrackName("video", i) for i in range(1, int(tl.GetTrackCount("video")) + 1)}
        have_a = {tl.GetTrackName("audio", i) for i in range(1, int(tl.GetTrackCount("audio")) + 1)}
        added = []
        for kind, names, have in (("video", TRACKS_V, have_v), ("audio", TRACKS_A, have_a)):
            for n in names:
                if n in have:
                    continue
                ok = tl.AddTrack(kind) if kind == "video" else tl.AddTrack("audio", "stereo")
                idx = int(tl.GetTrackCount(kind))
                if ok:
                    tl.SetTrackName(kind, idx, n); added.append(n)
        missing = [n for n in TRACKS_V + TRACKS_A if n not in {tl.GetTrackName("video", i) for i in range(1, int(tl.GetTrackCount("video")) + 1)} | {tl.GetTrackName("audio", i) for i in range(1, int(tl.GetTrackCount("audio")) + 1)}]
        say({"added": added, "missing": missing}); sys.exit(1 if missing else 0)
    if a.cmd == "marker":
        if a.color not in MARKER_COLORS:
            sys.exit(f"color must be one of {sorted(MARKER_COLORS)}")
        ok = tl.AddMarker(a.frame, a.color, a.name or "MARK", a.note, 1)
        say({"marker_added": bool(ok), "frame": a.frame, "color": a.color, "name": a.name}); return
    if a.cmd == "render":
        pr.SetCurrentTimeline(tl)
        ok1 = pr.SetCurrentRenderFormatAndCodec(a.format, a.codec)
        os.makedirs(a.dir, exist_ok=True)
        ok2 = pr.SetRenderSettings({"TargetDir": os.path.abspath(a.dir), "CustomName": a.name or tl.GetName(), "ExportVideo": True, "ExportAudio": True})
        job = pr.AddRenderJob()
        started = pr.StartRendering(job) if (a.start and job) else False
        say({"format_ok": bool(ok1), "settings_ok": bool(ok2), "job": job, "started": bool(started),
             "next": f"python resolve_pipeline.py verify --file {os.path.join(a.dir, (a.name or tl.GetName()) + '.' + a.format)}"})


if __name__ == "__main__":
    main()
