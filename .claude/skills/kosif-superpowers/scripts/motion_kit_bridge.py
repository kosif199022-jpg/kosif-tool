#!/usr/bin/env python3
"""KOSIF Motion Starter Bridge: original executable integration, not a link catalog.

Reads motalim-ai/motion-starter-kit line/word timing JSON and produces native KOSIF
Motion Director JSON and optional seekable SVG HTML. Does not install upstream code,
transcribe, alter audio, retrieve references, or assert style-clone fidelity.
"""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import motion_director as director
import code_drawing_master as drawing

# Ten documented external styles; four mapped to tested native SVG primitives.
STYLE_MAP = {
    "plotter": ("native_svg", "#f4f0e6", "#b75b2b"),
    "doodle": ("native_svg", "#f4f0e6", "#355b47"),
    "whiteboard": ("native_svg", "#fffdf6", "#193d39"),
    "infographic": ("native_svg", "#141c26", "#76e3cb"),
    "chalkboard": ("upstream_reference", None, None),
    "stickman": ("upstream_reference", None, None),
    "isometric": ("upstream_reference", None, None),
    "fake3d": ("upstream_reference", None, None),
    "map-journey": ("upstream_reference", None, None),
    "product": ("upstream_reference", None, None),
}

def normalize_timing(obj, allow_estimated=False):
    """Validate upstream lines[].words[].w/start/end; do not fabricate alignment."""
    if not isinstance(obj, dict) or not isinstance(obj.get("lines"), list):
        raise ValueError("expected Motion Starter Kit JSON with lines[]")
    duration = director.number(obj.get("duration"), 0.1, 120)
    audio = obj.get("audio")
    if audio is not None and (not isinstance(audio, str) or not audio.strip()):
        raise ValueError("audio must be a non-empty filename or null")
    if not audio and not allow_estimated:
        raise ValueError("no audio: estimated text timings require --allow-estimated")
    source = obj.get("source", "unspecified")
    if not isinstance(source, str):
        raise ValueError("invalid source metadata")
    lines = obj["lines"]
    if not 1 <= len(lines) <= 24:
        raise ValueError("need 1..24 lines for this KOSIF storyboard")
    cleaned = []
    last_end = 0.0
    total_words = 0
    for line in lines:
        if not isinstance(line, dict) or not isinstance(line.get("words"), list):
            raise ValueError("each line needs words[]")
        if not line["words"] or len(line["words"]) > 240:
            raise ValueError("each line needs 1..240 words")
        words = []
        for row in line["words"]:
            if not isinstance(row, dict):
                raise ValueError("word must be an object")
            word = row.get("w", row.get("word", row.get("text")))
            word = director.text(word, 120)
            start = director.number(row.get("start"), 0, duration)
            end = director.number(row.get("end"), 0, duration)
            if start < last_end - 1e-6 or end <= start:
                raise ValueError("overlapping, unordered, or zero-length word")
            words.append({"text": word, "start": start, "end": end})
            last_end = end
        total_words += len(words)
        cleaned.append({"words": words, "start": words[0]["start"], "end": words[-1]["end"]})
    return {
        "duration": duration,
        "lines": cleaned,
        "audio_claimed": bool(audio),
        "timing_provenance": "upstream_audio_alignment_not_independently_verified" if audio else "estimated_no_audio",
        "upstream_source": source[:120],
        "word_count": total_words,
    }

def build_story(timing, style, fps=30):
    if style not in STYLE_MAP:
        raise ValueError("unknown style")
    state, background, accent = STYLE_MAP[style]
    if state != "native_svg":
        raise ValueError("style needs its own adapter; no executable native KOSIF renderer yet")
    scenes = []
    lines = timing["lines"]
    duration = timing["duration"]
    for idx, line in enumerate(lines):
        start = 0.0 if idx == 0 else lines[idx]["start"]
        end = lines[idx + 1]["start"] if idx + 1 < len(lines) else duration
        if end <= start or line["end"] > end + 1e-6:
            raise ValueError("invalid line span")
        caption = " ".join(w["text"] for w in line["words"])
        if len(caption) > 150:
            caption = caption[:147].rstrip() + "…"
        k = max(0.001, end - start)
        main_text = {
            "type": "text", "text": caption, "x": 540, "y": 370,
            "start": start, "end": min(end, start + max(0.1, k * 0.45)),
            "fontSize": 52 if len(caption) > 60 else 68,
            "fill": accent,
        }
        motion_line = {
            "type": "path", "d": "M140 920 C340 670 710 1170 940 860",
            "stroke": accent, "strokeWidth": 9, "start": start, "end": end,
        }
        elements = [main_text, motion_line]
        if style == "doodle":
            elements.append({
                "type": "actor", "x": 540, "y": 1320, "scale": 1.35,
                "parts": drawing.human_parts("determined"), "action": "walk",
                "start": start, "end": min(end, start + k * 0.6),
                "move": {"fromX": -45, "toX": 65, "start": start, "end": end},
            })
        elif style == "infographic":
            elements.append({
                "type": "circle", "x": 540, "y": 1280, "r": 160, "fill": accent,
                "stroke": accent, "start": start, "end": end,
            })
        scenes.append({
            "id": f"line_{idx + 1:02d}", "start": start, "end": end,
            "background": background, "words": line["words"],
            "camera": {"fromZoom": 1.0, "toZoom": 1.05, "start": start, "end": end},
            "elements": elements,
        })
    spec = {"version": 1, "width": 1080, "height": 1920,
            "fps": fps, "duration": duration, "scenes": scenes}
    director.validate(spec)
    return spec

def demo_timings():
    # Explicitly synthetic: useful for testing shape/camera rendering, not audio sync.
    return normalize_timing({
        "duration": 6.0, "audio": None, "source": "KOSIF synthetic demonstration",
        "lines": [
            {"words": [
                {"w": "الرسم", "start": 0.2, "end": 1.2},
                {"w": "يتحرك", "start": 1.2, "end": 2.4},
            ]},
            {"words": [
                {"w": "مع", "start": 3.2, "end": 4.0},
                {"w": "الفكرة", "start": 4.0, "end": 5.6},
            ]},
        ],
    }, allow_estimated=True)

def write_outputs(spec, out, html=None):
    out_path = Path(out).expanduser()
    html_path = Path(html).expanduser() if html else None
    targets = [out_path] + ([html_path] if html_path else [])
    if len({str(p.resolve()) for p in targets}) != len(targets):
        raise ValueError("output filenames must be distinct")
    if any(p.exists() or p.is_symlink() or not p.parent.is_dir() for p in targets):
        raise ValueError("outputs must be new files in existing directories")
    if html_path:
        # Compile into memory via a scratch destination to avoid partial final artifacts.
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "preview.html"
            director.compile_spec(spec, scratch)
            html_content = scratch.read_text(encoding="utf-8")
            out_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            html_path.write_text(html_content, encoding="utf-8")
    else:
        out_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"storyboard": str(out_path.resolve()),
            "html": str(html_path.resolve()) if html_path else None}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("styles")
    for verb in ("demo", "build"):
        p = sub.add_parser(verb)
        p.add_argument("--style", choices=sorted(STYLE_MAP), default="doodle")
        p.add_argument("--out", required=True)
        p.add_argument("--html", help="optional seekable HTML preview")
        p.add_argument("--fps", type=int, choices=(24, 25, 30, 60), default=30)
        if verb == "build":
            p.add_argument("--timings", required=True, help="Motion Starter Kit words.json")
            p.add_argument("--allow-estimated", action="store_true",
                           help="accept reading-speed estimates if no audio was aligned")
    args = ap.parse_args(argv)
    try:
        if args.command == "styles":
            payload = {"origin": "motalim-ai/motion-starter-kit",
                       "license": "MIT (check dependencies, reference media and Remotion separately)",
                       "styles": {k: {"state": v[0]} for k, v in STYLE_MAP.items()}}
        else:
            timing = demo_timings() if args.command == "demo" else normalize_timing(
                json.loads(Path(args.timings).read_text(encoding="utf-8")),
                allow_estimated=args.allow_estimated,
            )
            spec = build_story(timing, args.style, args.fps)
            paths = write_outputs(spec, args.out, args.html)
            payload = {
                "status": "editable_native_svg_storyboard_created_not_mp4",
                "style": args.style, "scenes": len(spec["scenes"]),
                "words": timing["word_count"],
                "timing_provenance": timing["timing_provenance"],
                "input_audio_processed": False, "video_rendered": False,
                **paths,
            }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
