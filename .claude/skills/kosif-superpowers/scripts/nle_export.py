#!/usr/bin/env python3
"""NLE Export: hand a KOSIF timeline to DaVinci Resolve, Final Cut Pro, Premiere Pro, Blender or CapCut.

Reads a `kosif.timeline.v1` project (kosif_timeline.py) or a `kosif.edl.v1`
cut plan (cinematic_cut_planner.py) and writes editable timelines that point
at the ORIGINAL media files (nothing is copied or re-encoded):

  fcpxml   FCPXML 1.9   -> Final Cut Pro, DaVinci Resolve
  xmeml    FCP7 XML v5  -> Premiere Pro, DaVinci Resolve
  edl      CMX3600 EDL  -> DaVinci Resolve, Premiere Pro, Avid (one file per track)
  blender  bpy script   -> Blender Video Sequencer (fades and layout included)
  srt      captions     -> every editor, CapCut included (needs --words)
  capcut   CapCut pack  -> SRT + a numbered cut list (CapCut has no public timeline import)

Every time is snapped to whole frames; the receipt reports the largest drift,
what each format could not carry (fades, layout) and a SHA-256 per file.
Standard library only; ffprobe is used when present to read source lengths.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

TIMELINE_SCHEMA = "kosif.timeline.v1"
EDL_SCHEMA = "kosif.edl.v1"
RECEIPT_SCHEMA = "kosif.nle-export.v1"
FORMATS = ("fcpxml", "xmeml", "edl", "blender", "srt", "capcut")
DEFAULT_FORMATS = ("fcpxml", "xmeml", "edl", "blender")
KINDS = {"video": {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".mxf", ".avi"},
         "image": {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"},
         "audio": {".wav", ".mp3", ".m4a", ".aac", ".flac", ".aif", ".aiff"}}
MAX_SECONDS = 4 * 3600
MAX_CLIPS = 2000
SAFE_NAME = re.compile(r"[^0-9A-Za-z؀-ۿ._-]+")


# --------------------------------------------------------------------------- model
def _num(value, name, lo, hi):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if not lo <= float(value) <= hi:
        raise ValueError(f"{name} must be within {lo}..{hi}")
    return float(value)


def _int(value, name, lo, hi):
    if type(value) is not int or not lo <= value <= hi:
        raise ValueError(f"{name} must be an integer within {lo}..{hi}")
    return value


def probe(path):
    """Return {'duration', 'width', 'height', 'audio', 'video', 'rate'} or {} without ffprobe."""
    if not shutil.which("ffprobe"):
        return {}
    try:
        res = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                             check=True, capture_output=True, text=True, timeout=30)
        md = json.loads(res.stdout)
    except (subprocess.SubprocessError, OSError, ValueError):
        return {}
    streams = md.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    try:
        dur = float(md.get("format", {}).get("duration") or 0) or None
    except (TypeError, ValueError):
        dur = None
    out = {"duration": dur, "video": v is not None, "audio": a is not None}
    if v:
        out["width"], out["height"] = v.get("width"), v.get("height")
    if a:
        out["rate"] = int(a.get("sample_rate") or 48000)
        out["channels"] = int(a.get("channels") or 2)
    return out


class Timeline:
    def __init__(self, name, fps, width, height, duration):
        self.name, self.fps, self.width, self.height = name, fps, width, height
        self.frames = round(duration * fps)
        self.tracks = []          # [{"id","kind","layer","clips":[...]}]
        self.media = {}           # resolved path -> probe info
        self.drift = 0.0          # largest |seconds - frames/fps| seen while snapping
        self.warnings = []

    def f(self, seconds):
        frames = round(seconds * self.fps)
        self.drift = max(self.drift, abs(seconds - frames / self.fps))
        return frames

    def info(self, path):
        if path not in self.media:
            self.media[path] = probe(path)
        return self.media[path]

    def clips(self, kind=None):
        for t in self.tracks:
            for c in t["clips"]:
                if kind is None or t["kind"] == kind:
                    yield t, c


def _resolve(raw, base, kind, allow_missing):
    if not isinstance(raw, str) or not raw or "://" in raw:
        raise ValueError("clip paths must be local files")
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = base / p
    p = p.resolve()
    if p.suffix.lower() not in KINDS[kind]:
        raise ValueError(f"{p.name}: not a {kind} file type")
    if not p.is_file() and not allow_missing:
        raise ValueError(f"missing source file: {p} (use --allow-missing to relink later in the editor)")
    return p


def from_timeline(doc, base, name, allow_missing):
    fps = _int(doc.get("fps"), "fps", 1, 120)
    tl = Timeline(name, fps, _int(doc.get("width"), "width", 16, 8192), _int(doc.get("height"), "height", 16, 8192),
                  _num(doc.get("duration"), "duration", 0.04, MAX_SECONDS))
    tracks = doc.get("tracks")
    if not isinstance(tracks, list) or not tracks:
        raise ValueError("tracks must be a nonempty list")
    seen, count = set(), 0
    for ti, tr in enumerate(tracks):
        if not isinstance(tr, dict) or tr.get("kind") not in KINDS:
            raise ValueError(f"track {ti}: kind must be video, image or audio")
        tid = str(tr.get("id") or f"track{ti + 1}")
        track = {"id": tid, "kind": tr["kind"], "layer": _int(tr.get("layer", 0), f"{tid}.layer", 0, 99),
                 "order": ti, "clips": []}
        for ci, cl in enumerate(tr.get("clips") or []):
            count += 1
            if count > MAX_CLIPS:
                raise ValueError("too many clips")
            cid = str(cl.get("id") or f"{tid}-{ci + 1}")
            if cid in seen:
                raise ValueError(f"duplicate clip id {cid}")
            seen.add(cid)
            path = _resolve(cl.get("path"), base, tr["kind"], allow_missing)
            start = _num(cl.get("start", 0), f"{cid}.start", 0, MAX_SECONDS)
            dur = _num(cl.get("duration"), f"{cid}.duration", 1 / fps, MAX_SECONDS)
            src_in = _num(cl.get("in", 0), f"{cid}.in", 0, MAX_SECONDS)
            clip = {"id": cid, "path": path, "start": tl.f(start), "dur": max(1, tl.f(dur)), "in": tl.f(src_in),
                    "volume": _num(cl.get("volume", 1.0), f"{cid}.volume", 0, 4),
                    "fade_in": tl.f(_num(cl.get("fade_in", 0), f"{cid}.fade_in", 0, dur)),
                    "fade_out": tl.f(_num(cl.get("fade_out", 0), f"{cid}.fade_out", 0, dur)),
                    "audio": tr["kind"] == "audio" or (tr["kind"] == "video" and cl.get("include_audio") is True)}
            if tr["kind"] != "audio" and any(k in cl for k in ("x", "y", "width", "height")):
                clip["layout"] = {"x": int(cl.get("x", 0)), "y": int(cl.get("y", 0)),
                                  "w": int(cl.get("width", tl.width)), "h": int(cl.get("height", tl.height))}
            if clip["start"] + clip["dur"] > tl.frames:
                tl.frames = clip["start"] + clip["dur"]
                tl.warnings.append(f"{cid} ends after the declared duration; the sequence was lengthened")
            track["clips"].append(clip)
        track["clips"].sort(key=lambda c: (c["start"], c["id"]))
        tl.tracks.append(track)
    if not any(t["clips"] for t in tl.tracks):
        raise ValueError("no clips")
    return tl


def from_cut_plan(doc, base, name, allow_missing, audio=None):
    video = doc.get("video") or {}
    fps = _int(video.get("fps", 30), "video.fps", 1, 120)
    frames = _int(video.get("frame_count"), "video.frame_count", 1, MAX_SECONDS * 120)
    tl = Timeline(name, fps, _int(video.get("width", 1080), "width", 16, 8192),
                  _int(video.get("height", 1920), "height", 16, 8192), frames / fps)
    track = {"id": "V1", "kind": "video", "layer": 0, "order": 0, "clips": []}
    for sc in doc.get("scenes") or []:
        if not sc.get("footage_path"):
            tl.warnings.append(f"{sc.get('id')}: no footage chosen; left as a gap")
            continue
        f0, f1 = _int(sc["start_frame"], "start_frame", 0, frames), _int(sc["end_frame_exclusive"], "end", 1, frames)
        trim = sc.get("video_trim") or {}
        track["clips"].append({"id": str(sc.get("id")), "path": _resolve(sc["footage_path"], base, "video", allow_missing),
                               "start": f0, "dur": max(1, f1 - f0), "in": tl.f(float(trim.get("in", 0))),
                               "volume": 1.0, "fade_in": 0, "fade_out": 0, "audio": False})
    tl.tracks.append(track)
    if audio:
        ap = _resolve(str(audio), Path.cwd(), "audio", allow_missing)
        tl.tracks.append({"id": "VO", "kind": "audio", "layer": 0, "order": 1, "clips": [
            {"id": "voice", "path": ap, "start": 0, "dur": frames, "in": 0, "volume": 1.0,
             "fade_in": 0, "fade_out": 0, "audio": True}]})
    if not any(t["clips"] for t in tl.tracks):
        raise ValueError("the cut plan has no scene with footage")
    return tl


def load(path, allow_missing=False, audio=None):
    path = Path(path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    name = str(doc.get("name") or path.stem)
    if doc.get("schema") == TIMELINE_SCHEMA:
        return from_timeline(doc, path.parent, name, allow_missing)
    if doc.get("schema") == EDL_SCHEMA:
        return from_cut_plan(doc, path.parent, name, allow_missing, audio)
    raise ValueError(f"unknown schema {doc.get('schema')!r}; expected {TIMELINE_SCHEMA} or {EDL_SCHEMA}")


def source_frames(tl, clip, kind):
    """Length of the source media in frames (probe when possible, else what the timeline uses)."""
    used = clip["in"] + clip["dur"]
    if kind == "image":
        return used
    dur = tl.info(clip["path"]).get("duration")
    if dur:
        avail = int(math.floor(dur * tl.fps + 1e-6))
        if avail < used:
            tl.warnings.append(f"{clip['id']}: uses {used} frames but the source has {avail}")
        return max(avail, used)
    return used


# --------------------------------------------------------------------------- formats
def _t(frames, fps):
    if frames == 0:
        return "0s"
    g = math.gcd(frames, fps)
    return f"{frames // g}s" if fps // g == 1 else f"{frames // g}/{fps // g}s"


def _db(volume):
    return "-96dB" if volume <= 0 else f"{20 * math.log10(volume):.2f}dB"


def _video_order(tl):
    return sorted((t for t in tl.tracks if t["kind"] != "audio"), key=lambda t: (t["layer"], t["order"]))


def _audio_order(tl):
    return [t for t in tl.tracks if t["kind"] == "audio"]


def write_fcpxml(tl):
    fps = tl.fps
    out = ['<?xml version="1.0" encoding="UTF-8"?>', "<!DOCTYPE fcpxml>", '<fcpxml version="1.9">', "  <resources>",
           f'    <format id="r1" frameDuration="{_t(1, fps)}" width="{tl.width}" height="{tl.height}" '
           f'colorSpace="1-1-1 (Rec. 709)"/>']
    ids, n = {}, 2
    for t, c in tl.clips():
        key = (c["path"], t["kind"])
        if key in ids:
            continue
        ids[key] = f"r{n}"
        n += 1
        info = tl.info(c["path"])
        has_audio = t["kind"] == "audio" or (t["kind"] == "video" and info.get("audio", c["audio"]))
        attrs = [f'id="{ids[key]}"', f"name={quoteattr(c['path'].stem)}", 'start="0s"',
                 f'duration="{_t(0 if t["kind"] == "image" else source_frames(tl, c, t["kind"]), fps)}"',
                 f'hasVideo="{0 if t["kind"] == "audio" else 1}"', f'hasAudio="{1 if has_audio else 0}"']
        if t["kind"] != "audio":
            attrs.append('format="r1"')
        if has_audio:
            attrs += ['audioSources="1"', f'audioChannels="{info.get("channels", 2)}"',
                      f'audioRate="{info.get("rate", 48000)}"']
        out.append(f"    <asset {' '.join(attrs)}>")
        out.append(f'      <media-rep kind="original-media" src={quoteattr(c["path"].as_uri())}/>')
        out.append("    </asset>")
    out += ["  </resources>", "  <library>", f"    <event name={quoteattr('KOSIF ' + tl.name)}>",
            f"      <project name={quoteattr(tl.name)}>",
            f'        <sequence format="r1" duration="{_t(tl.frames, fps)}" tcStart="0s" tcFormat="NDF" '
            f'audioLayout="stereo" audioRate="48k">', "          <spine>",
            f'            <gap name="KOSIF base" offset="0s" start="0s" duration="{_t(tl.frames, fps)}">']
    lanes = [(t, i + 1) for i, t in enumerate(_video_order(tl))] + [(t, -(i + 1)) for i, t in enumerate(_audio_order(tl))]
    for t, lane in lanes:
        for c in t["clips"]:
            ref = ids[(c["path"], t["kind"])]
            if t["kind"] == "image":   # a still lives in a <clip> wrapper, as Final Cut Pro writes it
                out.append(f'              <clip lane="{lane}" offset="{_t(c["start"], fps)}" name={quoteattr(c["id"])} '
                           f'start="0s" duration="{_t(c["dur"], fps)}" format="r1">'
                           f'<video ref="{ref}" offset="0s" start="0s" duration="{_t(c["dur"], fps)}"/></clip>')
                continue
            tag = "asset-clip"
            attrs = [f'ref="{ref}"', f'lane="{lane}"', f'offset="{_t(c["start"], fps)}"',
                     f"name={quoteattr(c['id'])}", f'start="{_t(c["in"], fps)}"', f'duration="{_t(c["dur"], fps)}"']
            if t["kind"] == "video":
                attrs.append(f'srcEnable="{"all" if c["audio"] else "video"}"')
            if t["kind"] == "audio":
                attrs.append('audioRole="dialogue"' if t["id"].lower() in ("vo", "voice", "narration") else 'audioRole="music"')
            body = f'<adjust-volume amount="{_db(c["volume"])}"/>' if c["audio"] and c["volume"] != 1.0 else ""
            out.append(f"              <{tag} {' '.join(attrs)}" + (f">{body}</{tag}>" if body else "/>"))
    out += ["            </gap>", "          </spine>", "        </sequence>", "      </project>", "    </event>",
            "  </library>", "</fcpxml>", ""]
    return "\n".join(out)


def _rate(fps, pad):
    return f"{pad}<rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>"


def write_xmeml(tl):
    fps = tl.fps
    files, fid = {}, 0
    clip_no = 0

    def file_el(t, c, pad):
        nonlocal fid
        key = c["path"]
        if key in files:
            return f'{pad}<file id="{files[key]}"/>'
        fid += 1
        files[key] = f"file-{fid}"
        info = tl.info(c["path"])
        media = []
        if t["kind"] != "audio":
            media.append(f"{pad}    <video><samplecharacteristics><width>{info.get('width') or tl.width}</width>"
                         f"<height>{info.get('height') or tl.height}</height></samplecharacteristics></video>")
        if t["kind"] == "audio" or info.get("audio", c["audio"]):
            media.append(f"{pad}    <audio><samplecharacteristics><samplerate>{info.get('rate', 48000)}</samplerate>"
                         f"<depth>16</depth></samplecharacteristics><channelcount>{info.get('channels', 2)}</channelcount></audio>")
        return "\n".join([f'{pad}<file id="{files[key]}">', f"{pad}  <name>{escape(c['path'].name)}</name>",
                          f"{pad}  <pathurl>{escape(c['path'].as_uri())}</pathurl>", _rate(fps, pad + "  "),
                          f"{pad}  <duration>{source_frames(tl, c, t['kind'])}</duration>",
                          f"{pad}  <media>", *media, f"{pad}  </media>", f"{pad}</file>"])

    def clipitem(t, c, pad, audio_side=False):
        nonlocal clip_no
        clip_no += 1
        lines = [f'{pad}<clipitem id="clipitem-{clip_no}">', f"{pad}  <name>{escape(c['id'])}</name>",
                 f"{pad}  <enabled>TRUE</enabled>", f"{pad}  <duration>{source_frames(tl, c, t['kind'])}</duration>",
                 _rate(fps, pad + "  "), f"{pad}  <start>{c['start']}</start>",
                 f"{pad}  <end>{c['start'] + c['dur']}</end>", f"{pad}  <in>{c['in']}</in>",
                 f"{pad}  <out>{c['in'] + c['dur']}</out>", file_el(t, c, pad + "  ")]
        if audio_side:
            lines.append(f"{pad}  <sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>")
            if c["volume"] != 1.0:
                lines.append(f"{pad}  <filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid>"
                             f"<effectcategory>audiolevels</effectcategory><effecttype>audiolevels</effecttype>"
                             f"<mediatype>audio</mediatype><parameter><parameterid>level</parameterid><name>Level</name>"
                             f"<valuemin>0</valuemin><valuemax>3.98109</valuemax><value>{c['volume']:.5f}</value>"
                             f"</parameter></effect></filter>")
        lines.append(f"{pad}</clipitem>")
        return "\n".join(lines)

    v = ["      <video>", "        <format><samplecharacteristics>", _rate(fps, "          "),
         f"          <width>{tl.width}</width><height>{tl.height}</height>"
         f"<pixelaspectratio>square</pixelaspectratio>", "        </samplecharacteristics></format>"]
    for t in _video_order(tl):
        v.append("        <track>")
        v += [clipitem(t, c, "          ") for c in t["clips"]]
        v.append("        </track>")
    v.append("      </video>")
    a = ["      <audio>"]
    for t in _video_order(tl):
        with_audio = [c for c in t["clips"] if c["audio"]]
        if with_audio:
            a.append("        <track>")
            a += [clipitem(t, c, "          ", True) for c in with_audio]
            a.append("        </track>")
    for t in _audio_order(tl):
        a.append("        <track>")
        a += [clipitem(t, c, "          ", True) for c in t["clips"]]
        a.append("        </track>")
    a.append("      </audio>")
    return "\n".join(['<?xml version="1.0" encoding="UTF-8"?>', "<!DOCTYPE xmeml>", '<xmeml version="5">',
                      '  <sequence id="sequence-1">', f"    <name>{escape(tl.name)}</name>",
                      f"    <duration>{tl.frames}</duration>", _rate(fps, "    "),
                      f"    <timecode>{_rate(fps, '')}<string>00:00:00:00</string><frame>0</frame>"
                      f"<displayformat>NDF</displayformat></timecode>", "    <media>", *v, *a,
                      "    </media>", "  </sequence>", "</xmeml>", ""])


def _tc(frames, fps):
    s, ff = divmod(frames, fps)
    m, ss = divmod(s, 60)
    h, mm = divmod(m, 60)
    return f"{h:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def write_edls(tl):
    """One CMX3600 EDL per track (EDL has one picture track per file)."""
    files = {}
    for t in tl.tracks:
        if not t["clips"]:
            continue
        chan = "AA" if t["kind"] == "audio" else "V"
        lines = [f"TITLE: {tl.name} {t['id']}"[:70], "FCM: NON-DROP FRAME", ""]
        last_end = -1
        for i, c in enumerate(t["clips"], 1):
            if c["start"] < last_end:
                tl.warnings.append(f"edl {t['id']}: {c['id']} overlaps the previous clip; EDL events cannot overlap")
            last_end = max(last_end, c["start"] + c["dur"])
            lines.append(f"{i:03d}  AX       {chan:<5} C        {_tc(c['in'], tl.fps)} {_tc(c['in'] + c['dur'], tl.fps)} "
                         f"{_tc(c['start'], tl.fps)} {_tc(c['start'] + c['dur'], tl.fps)}")
            lines.append(f"* FROM CLIP NAME: {c['path'].name}")
            lines.append(f"* SOURCE FILE: {c['path']}")
            lines.append("")
        files[f"{SAFE_NAME.sub('_', t['id'])}.edl"] = "\n".join(lines)
    return files


BLENDER_TEMPLATE = r'''# Generated by KOSIF nle_export.py: builds the timeline in Blender's Video Sequencer.
# Run:  blender --background --python THIS_FILE -- --save out.blend
#   or open Blender > Scripting > Open this file > Run Script.
import json
import sys

import bpy

DATA = json.loads(r"""__DATA__""")


def strips(ed):
    coll = getattr(ed, "strips", None)          # Blender 5.0+
    return coll if coll is not None else ed.sequences


def trim(st, src_in, dur):
    if hasattr(st, "left_handle_offset"):      # Blender 5.0+ handle API
        st.left_handle_offset = src_in
        st.duration = dur
    else:                                       # Blender 4.x
        st.frame_offset_start = src_in
        st.frame_final_duration = dur


def span(st):
    if hasattr(st, "left_handle"):
        return st.left_handle, st.right_handle
    return st.frame_final_start, st.frame_final_end


def key(strip, prop, frame, value):
    setattr(strip, prop, value)
    strip.keyframe_insert(data_path=prop, frame=frame)


def build(scene):
    r = scene.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = DATA["width"], DATA["height"], 100
    r.fps, r.fps_base = DATA["fps"], 1.0
    scene.frame_start, scene.frame_end = 1, DATA["frames"]
    ed = scene.sequence_editor or scene.sequence_editor_create()
    coll = strips(ed)
    made = []
    for s in DATA["strips"]:
        start = 1 + s["start"]
        head = start - s["in"]
        fit = {"fit_method": "ORIGINAL"} if s.get("layout") and s.get("src_w") else {}
        if s["kind"] == "video":
            st = coll.new_movie(s["name"], s["path"], s["channel"], head, **fit)
        elif s["kind"] == "image":
            st = coll.new_image(s["name"], s["path"], s["channel"], start, **fit)
        else:
            st = coll.new_sound(s["name"], s["path"], s["channel"], head)
        trim(st, s["in"], s["dur"])
        if s["kind"] == "audio":
            st.volume = s["volume"]
            if s["fade_in"]:
                key(st, "volume", start, 0.0); key(st, "volume", start + s["fade_in"], s["volume"])
            if s["fade_out"]:
                end = start + s["dur"]
                key(st, "volume", end - s["fade_out"], s["volume"]); key(st, "volume", end, 0.0)
        else:
            if s.get("layout") and s.get("src_w") and s.get("src_h"):
                lay = s["layout"]
                st.transform.scale_x = lay["w"] / s["src_w"]
                st.transform.scale_y = lay["h"] / s["src_h"]
                st.transform.offset_x = lay["x"] + lay["w"] / 2 - DATA["width"] / 2
                st.transform.offset_y = DATA["height"] / 2 - (lay["y"] + lay["h"] / 2)
            if s["channel"] > 1 or s["kind"] == "image":
                st.blend_type = "ALPHA_OVER"
            if s["fade_in"]:
                key(st, "blend_alpha", start, 0.0); key(st, "blend_alpha", start + s["fade_in"], 1.0)
            if s["fade_out"]:
                end = start + s["dur"]
                key(st, "blend_alpha", end - s["fade_out"], 1.0); key(st, "blend_alpha", end, 0.0)
        a, b = span(st)
        made.append({"name": st.name, "channel": st.channel, "start": int(a), "end": int(b)})
    return made


made = build(bpy.context.scene)
print("KOSIF_VSE " + json.dumps({"strips": made}))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if "--save" in argv:
    bpy.ops.wm.save_as_mainfile(filepath=argv[argv.index("--save") + 1])
'''


def write_blender(tl):
    data = {"name": tl.name, "fps": tl.fps, "width": tl.width, "height": tl.height, "frames": tl.frames, "strips": []}
    channel = 1
    for t in _video_order(tl):
        for c in t["clips"]:
            info = tl.info(c["path"])
            s = {"name": c["id"], "kind": t["kind"], "path": str(c["path"]), "channel": channel, "start": c["start"],
                 "dur": c["dur"], "in": 0 if t["kind"] == "image" else c["in"], "volume": c["volume"],
                 "fade_in": c["fade_in"], "fade_out": c["fade_out"]}
            if c.get("layout"):
                s["layout"] = c["layout"]
                s["src_w"], s["src_h"] = info.get("width"), info.get("height")
                if not info.get("width"):
                    tl.warnings.append(f"blender: {c['id']} layout skipped (source size unknown without ffprobe)")
            data["strips"].append(s)
        channel += 1
    for t in _video_order(tl):
        for c in (c for c in t["clips"] if c["audio"]):
            data["strips"].append({"name": c["id"] + "-audio", "kind": "audio", "path": str(c["path"]), "channel": channel,
                                   "start": c["start"], "dur": c["dur"], "in": c["in"], "volume": c["volume"],
                                   "fade_in": c["fade_in"], "fade_out": c["fade_out"]})
        if any(c["audio"] for c in t["clips"]):
            channel += 1
    for t in _audio_order(tl):
        for c in t["clips"]:
            data["strips"].append({"name": c["id"], "kind": "audio", "path": str(c["path"]), "channel": channel,
                                   "start": c["start"], "dur": c["dur"], "in": c["in"], "volume": c["volume"],
                                   "fade_in": c["fade_in"], "fade_out": c["fade_out"]})
        channel += 1
    if channel > 128:
        raise ValueError("Blender's sequencer has 128 channels")
    payload = json.dumps(data, ensure_ascii=False, indent=1)
    if '"""' in payload:
        raise ValueError('a path contains """, which the Blender script cannot embed')
    return BLENDER_TEMPLATE.replace("__DATA__", payload)


def _srt_time(sec):
    ms = max(0, round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def phrases_from_words(doc, pause=0.4, max_words=7, max_chars=42):
    if isinstance(doc, dict) and isinstance(doc.get("phrases"), list) and doc["phrases"] and \
            all(isinstance(p, dict) and "text" in p and "start" in p and "end" in p for p in doc["phrases"]):
        return [(float(p["start"]), float(p["end"]), str(p["text"]).strip()) for p in doc["phrases"]]
    words = doc.get("words") if isinstance(doc, dict) else doc
    if not isinstance(words, list) or not words:
        raise ValueError("words.json must be a list of {word,start,end} or {'words': [...]}")
    out, cur = [], []
    for w in words:
        text = str(w.get("word") or w.get("text") or "").strip()
        if not text:
            continue
        start, end = float(w["start"]), float(w["end"])
        if cur and (start - cur[-1][1] > pause or len(cur) >= max_words
                    or len(" ".join(x[2] for x in cur)) + 1 + len(text) > max_chars):
            out.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
            cur = []
        cur.append((start, end, text))
    if cur:
        out.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
    return out


def write_srt(phrases):
    return "\n".join(f"{i}\n{_srt_time(a)} --> {_srt_time(b)}\n{text}\n" for i, (a, b, text) in enumerate(phrases, 1))


def write_cutlist(tl):
    rows = ["# CapCut cut list / قائمة القطع لكاب كات", "",
            "CapCut has no public timeline import, so rebuild the cut from this list: drop the files in this order, "
            "trim each to its source in/out and place it at the timeline time. Import the .srt with the captions panel "
            "where your CapCut version offers it.", "",
            "كاب كات مفيهوش استيراد تايملاين رسمي: حط الملفات بالترتيب ده، قصّ كل واحد من (بداية/نهاية المصدر) "
            "وحطه عند وقت التايملاين. ملف الترجمة .srt بيتستورد من لوحة الكابشن لو نسختك بتدعمه.", "",
            f"Project: {tl.name} · {tl.width}x{tl.height} · {tl.fps} fps · {_tc(tl.frames, tl.fps)}", "",
            "| # | track | clip | file | timeline in → out | source in → out |", "|---|---|---|---|---|---|"]
    n = 0
    for t in _video_order(tl) + _audio_order(tl):
        for c in t["clips"]:
            n += 1
            rows.append(f"| {n} | {t['id']} | {c['id']} | `{c['path'].name}` | {_tc(c['start'], tl.fps)} → "
                        f"{_tc(c['start'] + c['dur'], tl.fps)} | {_tc(c['in'], tl.fps)} → {_tc(c['in'] + c['dur'], tl.fps)} |")
    return "\n".join(rows) + "\n"


HANDOFF = """# Open this timeline in your editor / افتح التايملاين في برنامجك

All files point at the original media; nothing was copied or re-encoded. Keep the media where it is, or relink.
كل الملفات بتشاور على الميديا الأصلية من غير نسخ ولا إعادة ترميز. سيب الميديا مكانها أو اعمل Relink.

| editor | file | how to open |
|---|---|---|
| DaVinci Resolve | `{base}.fcpxml` (or `{base}.premiere.xml`, `*.edl`) | File → Import → Timeline… (uncheck "automatically import source clips" only if they are already in the media pool) |
| Final Cut Pro | `{base}.fcpxml` | File → Import → XML… |
| Premiere Pro | `{base}.premiere.xml` | File → Import… (FCP7 XML), or `*.edl` via File → Import |
| Avid / any EDL tool | `<track>.edl` | one EDL per track, CMX3600 non-drop |
| Blender | `{base}.blender_vse.py` | `blender --background --python {base}.blender_vse.py -- --save {base}.blend`, or Scripting → Run Script |
| CapCut | `{base}.capcut.md` (+ `.srt`) | no timeline import: follow the cut list |

Not carried by every format (do it in the editor) / حاجات مش كل الصيغ بتنقلها:
{gaps}
"""


def export(tl, out_dir, formats, words=None, force=False):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = SAFE_NAME.sub("_", tl.name).strip("_") or "timeline"
    files = {}
    if "fcpxml" in formats:
        files[f"{base}.fcpxml"] = write_fcpxml(tl)
    if "xmeml" in formats:
        files[f"{base}.premiere.xml"] = write_xmeml(tl)
    if "edl" in formats:
        files.update({f"{base}.{k}": v for k, v in write_edls(tl).items()})
    if "blender" in formats:
        files[f"{base}.blender_vse.py"] = write_blender(tl)
    phrases = None
    if words is not None:
        phrases = phrases_from_words(json.loads(Path(words).read_text(encoding="utf-8")))
    if ("srt" in formats or "capcut" in formats) and phrases:
        files[f"{base}.srt"] = write_srt(phrases)
    elif "srt" in formats:
        raise ValueError("srt needs --words words.json")
    if "capcut" in formats:
        files[f"{base}.capcut.md"] = write_cutlist(tl)
    gaps = []
    fades = [c["id"] for _, c in tl.clips() if c["fade_in"] or c["fade_out"]]
    layout = [c["id"] for _, c in tl.clips() if c.get("layout")]
    if fades:
        gaps.append(f"- fades on {', '.join(fades)}: Blender script only; add dissolves/opacity in Resolve/FCP/Premiere")
    if layout:
        gaps.append(f"- position/size on {', '.join(layout)}: Blender script only; set Transform in the other editors")
    files["HANDOFF.md"] = HANDOFF.format(base=base, gaps="\n".join(gaps) or "- nothing: every clip is carried as-is")
    clash = [n for n in files if (out_dir / n).exists()]
    if clash and not force:
        raise FileExistsError(f"refusing to overwrite {', '.join(clash)} (use --force)")
    receipt_files = []
    for name, text in files.items():
        data = text.encode("utf-8")
        (out_dir / name).write_bytes(data)
        receipt_files.append({"file": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    receipt = {"schema": RECEIPT_SCHEMA, "name": tl.name, "fps": tl.fps, "width": tl.width, "height": tl.height,
               "frames": tl.frames, "seconds": round(tl.frames / tl.fps, 3),
               "tracks": [{"id": t["id"], "kind": t["kind"], "clips": len(t["clips"])} for t in tl.tracks],
               "clips": sum(len(t["clips"]) for t in tl.tracks), "formats": sorted(formats),
               "max_snap_drift_ms": round(tl.drift * 1000, 3), "probed": bool(shutil.which("ffprobe")),
               "not_carried": gaps, "warnings": tl.warnings, "files": receipt_files,
               "captions": len(phrases) if phrases else 0,
               "notice": "Timelines reference the original media; open them in the editor to verify before delivery."}
    (out_dir / "receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


# --------------------------------------------------------------------------- cli
def main(argv=None):
    ap = argparse.ArgumentParser(prog="nle_export.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("export", help="write editable timelines for the editors")
    ex.add_argument("--project", required=True, help="kosif.timeline.v1 project or kosif.edl.v1 cut plan (JSON)")
    ex.add_argument("--out", required=True, help="output folder")
    ex.add_argument("--formats", default=",".join(DEFAULT_FORMATS),
                    help=f"comma list from {','.join(FORMATS)} or 'all' (default {','.join(DEFAULT_FORMATS)})")
    ex.add_argument("--words", help="words.json for captions (srt, capcut)")
    ex.add_argument("--audio", help="voice-over file to add as an audio track (cut plans only)")
    ex.add_argument("--name", help="sequence name (default: the project's name or file stem)")
    ex.add_argument("--allow-missing", action="store_true", help="export even when a source file is missing (relink later)")
    ex.add_argument("--force", action="store_true", help="overwrite earlier export files in --out")
    sub.add_parser("formats", help="list the formats and which editor opens each")
    args = ap.parse_args(argv)
    if args.cmd == "formats":
        for line in __doc__.splitlines()[6:12]:
            print(line.strip())
        return 0
    formats = set(FORMATS if args.formats == "all" else (f.strip() for f in args.formats.split(",") if f.strip()))
    bad = formats - set(FORMATS)
    if bad:
        ap.error(f"unknown format(s): {', '.join(sorted(bad))}")
    if args.words and args.formats != "all" and not formats & {"srt", "capcut"}:
        formats.add("srt")
    try:
        tl = load(args.project, args.allow_missing, args.audio)
        if args.name:
            tl.name = args.name
        receipt = export(tl, args.out, formats, args.words, args.force)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "written", "out": str(Path(args.out)), "files": [f["file"] for f in receipt["files"]],
                      "clips": receipt["clips"], "seconds": receipt["seconds"],
                      "max_snap_drift_ms": receipt["max_snap_drift_ms"], "warnings": receipt["warnings"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
