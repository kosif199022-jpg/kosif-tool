#!/usr/bin/env python3
"""Original KOSIF workflow adapters: word-boundary paper edits and frame review markers.

These commands generate deterministic, non-destructive JSON. They NEVER decode,
run, edit or upload the source audio, applications, or video.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def _positive_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: expected a finite number")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name}: must be finite and positive")
    return float(value)


def read_words(path):
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(value, dict):
        value = value.get("words")
    if not isinstance(value, list) or not value:
        raise ValueError("words.json must contain a nonempty word list")
    previous_end = 0.0
    result = []
    for n, item in enumerate(value, start=1):
        if isinstance(item, dict) and "word" not in item and isinstance(item.get("text"), str):
            item = {**item, "word": item["text"]}  # WhisperX/ASR files call it "text"
        if not isinstance(item, dict) or not isinstance(item.get("word"), str) or not item["word"].strip():
            raise ValueError(f"word #{n}: missing word")
        start = item.get("start")
        end = item.get("end")
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (start, end)):
            raise ValueError(f"word #{n}: invalid timestamp")
        if start < previous_end - 0.000001 or end <= start or start < 0:
            raise ValueError(f"word #{n}: overlapping or reversed timestamps")
        result.append({"index": n, "word": item["word"], "start": float(start), "end": float(end)})
        previous_end = end
    return result


def parse_keep(expr, size):
    selected = set()
    if not expr.strip():
        raise ValueError("--keep requires one or more word indices")
    for part in expr.split(","):
        p = part.strip()
        if not p:
            raise ValueError("empty --keep range")
        tokens = p.split("-")
        if not (1 <= len(tokens) <= 2) or any(not x.strip().isdigit() for x in tokens):
            raise ValueError(f"invalid --keep range: {p}")
        start = int(tokens[0])
        end = int(tokens[-1])
        if start < 1 or end > size or start > end:
            raise ValueError(f"out-of-bounds --keep range: {p}")
        selected.update(range(start, end + 1))
    return sorted(selected)


def paper_edit(words, keep, fps=30):
    """Produce a video-only cut manifest. Source sound is NEVER edited here."""
    fps = int(_positive_number(fps, "fps"))
    if not keep:
        raise ValueError("empty selection")
    selected = [words[i - 1] for i in keep]
    runs = []
    for word in selected:
        first = math.floor(word["start"] * fps + 0.00000001)
        last = math.ceil(word["end"] * fps - 0.00000001)
        if last <= first:
            last = first + 1
        if runs and word["index"] == runs[-1]["word_indices"][-1] + 1:
            runs[-1]["source_end_frame"] = max(runs[-1]["source_end_frame"], last)
            runs[-1]["word_indices"].append(word["index"])
            runs[-1]["text"] += " " + word["word"]
        else:
            runs.append({"source_start_frame": first, "source_end_frame": last,
                         "word_indices": [word["index"]], "text": word["word"]})
    cursor = 0
    for run in runs:
        n = run["source_end_frame"] - run["source_start_frame"]
        run["output_start_frame"], run["output_end_frame"] = cursor, cursor + n
        cursor += n
    return {"schema": "kosif.video-paper-edit.v1", "fps": fps,
            "audio_policy": "not_processed; never apply these cuts to an audio-master narration",
            "kind": "non_destructive_video_only_cut_plan",
            "output_frames": cursor, "segments": runs}


def frame_reviews(notes, *, duration, fps=30, width=1080, height=1920):
    """Normalize review comments to exact video frames; no network or source media access."""
    duration = _positive_number(duration, "duration")
    fps = int(_positive_number(fps, "fps"))
    width, height = int(_positive_number(width, "width")), int(_positive_number(height, "height"))
    if not isinstance(notes, list):
        raise ValueError("notes must be a list")
    total = math.ceil(duration * fps)
    result = []
    for n, note in enumerate(notes, start=1):
        if not isinstance(note, dict):
            raise ValueError(f"note #{n}: expected an object")
        timestamp = note.get("time")
        if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)) or not math.isfinite(timestamp) or not (0 <= timestamp < duration):
            raise ValueError(f"note #{n}: time outside video")
        comment = note.get("comment")
        if not isinstance(comment, str) or not comment.strip() or len(comment) > 1000:
            raise ValueError(f"note #{n}: invalid comment")
        x, y = note.get("x"), note.get("y")
        if (x is None) != (y is None):
            raise ValueError(f"note #{n}: both x and y required for anchored comment")
        if x is not None and (any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in (x, y))):
            raise ValueError(f"note #{n}: normalized position outside frame")
        frame = min(total - 1, int(math.floor(timestamp * fps + 0.5)))
        payload = {"frame": frame, "comment": comment.strip(), "x": x, "y": y}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
        result.append({"id": digest, "frame": frame, "timecode": f"{frame//(fps*3600):02d}:{frame//(fps*60)%60:02d}:{frame//fps%60:02d}:{frame%fps:02d}",
                       "comment": comment.strip(), "point_px": {"x": round(x * width), "y": round(y * height)} if x is not None else None})
    return {"schema": "kosif.frame-review.v1", "fps": fps, "width": width, "height": height,
            "duration": duration, "frame_count": total, "markers": sorted(result, key=lambda z: (z["frame"], z["id"]))}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    edit = subs.add_parser("paper-edit", help="Non-destructive text-selected VIDEO edit manifest")
    edit.add_argument("words", help="words.json with word/start/end entries")
    edit.add_argument("--keep", required=True, help="1-based word ranges, e.g. 1-3,7-9")
    edit.add_argument("--fps", type=int, default=30)
    edit.add_argument("--out", required=True)
    edit.add_argument("--force", action="store_true", help="overwrite an existing --out")
    review = subs.add_parser("review", help="Frame-accurate, anchored review note markers")
    review.add_argument("notes", help="list of {time,comment,x?,y?}")
    review.add_argument("--duration", type=float, required=True)
    review.add_argument("--fps", type=int, default=30)
    review.add_argument("--width", type=int, default=1080)
    review.add_argument("--height", type=int, default=1920)
    review.add_argument("--out", required=True)
    review.add_argument("--force", action="store_true", help="overwrite an existing --out")
    args = parser.parse_args(argv)
    try:
        if Path(args.out).exists() and not args.force:
            raise ValueError(f"{args.out} already exists; choose a new --out or pass --force")
        if args.command == "paper-edit":
            words = read_words(args.words)
            payload = paper_edit(words, parse_keep(args.keep, len(words)), args.fps)
        else:
            notes = json.loads(Path(args.notes).read_text(encoding="utf-8-sig"))
            payload = frame_reviews(notes, duration=args.duration, fps=args.fps, width=args.width, height=args.height)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "created", "output": str(args.out), "schema": payload["schema"]}, ensure_ascii=False))
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
