#!/usr/bin/env python3
"""KOSIF Full Body v1: original, deterministic, word-cued 2D character animation.
No Adobe/CapCut code. Uses existing KOSIF paint renderer and analytic two-bone IK.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from creative_paint import paint, svg, color, num
from character_ik import solve_ik, words_from_file, probe, packet_hashes

SCHEMA = "kosif.fullbody.v1"
KINDS = {"walk", "run", "wave", "smile", "blink", "nod"}
MAX_FRAMES = 600


def location(v):
    if not isinstance(v, list) or len(v) != 2:
        raise ValueError("origin must be [x,y]")
    return (num(v[0], -1000, 3000), num(v[1], -1000, 3000))


def prepare(scene, words=None):
    if not isinstance(scene, dict) or scene.get("schema") != SCHEMA:
        raise ValueError("invalid full body scene")
    w, h = scene.get("width"), scene.get("height")
    if type(w) is not int or type(h) is not int or not (128 <= w <= 1280 and 128 <= h <= 1280):
        raise ValueError("invalid canvas dimensions")
    duration = num(scene.get("duration"), 0.1, 30)
    bg = color(scene.get("background", "#F4F0E6"))
    ch = scene.get("character", {})
    if not isinstance(ch, dict):
        raise ValueError("character must be an object")
    origin = location(ch.get("origin", [w / 2, h / 2]))
    scale = num(ch.get("scale", 1), 0.35, 1.8)
    skin = color(ch.get("skin", "#E8BD98"))
    clothes = color(ch.get("clothes", "#355B47"))
    pants = color(ch.get("pants", "#344B60"))
    hair = color(ch.get("hair", "#25312D"))
    actions = scene.get("actions", [])
    if not isinstance(actions, list) or len(actions) > 100:
        raise ValueError("actions must be array with <=100 entries")
    cues = []
    last = -1
    channel_ends = {}
    for action in actions:
        if not isinstance(action, dict) or action.get("kind") not in KINDS:
            raise ValueError("unsupported action")
        if ("time" in action) == ("word" in action):
            raise ValueError("action must have exactly one of time or word")
        if "time" in action:
            start = num(action["time"], 0, duration)
        else:
            token = action["word"]
            index = action.get("occurrence", 1)
            if not isinstance(token, str) or not token.strip() or type(index) is not int or index < 1:
                raise ValueError("invalid word cue")
            matches = [entry for entry in (words or []) if entry["word"].strip() == token.strip()]
            if len(matches) < index:
                raise ValueError("word cue not found in verified timings")
            start = num(matches[index-1]["start"], 0, duration)
        length = num(action.get("duration"), 0.05, 30)
        if start < last:
            raise ValueError("actions must be ordered by start")
        if start + length > duration + 1e-7:
            raise ValueError("action extends beyond scene")
        kind = action["kind"]
        channel = "locomotion" if kind in ("walk", "run") else kind
        if start < channel_ends.get(channel, -1) - 1e-7:
            raise ValueError("overlapping actions on same channel")
        channel_ends[channel] = start + length
        last = start
        speed = num(action.get("speed", 30 if kind == "walk" else 65), -300, 300)
        cues.append({"kind": kind, "time": start, "duration": length, "speed": speed,
                     "word": action.get("word")})
    return {"width": w, "height": h, "duration": duration, "background": bg,
            "character": {"origin": origin, "scale": scale, "skin": skin,
                          "clothes": clothes, "pants": pants, "hair": hair},
            "actions": cues}


def motion(p, t):
    t = num(t, 0, p["duration"])
    active = {}
    distance = 0
    for a in p["actions"]:
        elapsed = min(max(t - a["time"], 0), a["duration"])
        if a["kind"] in ("walk", "run"):
            distance += elapsed * a["speed"]
        if a["time"] <= t < a["time"] + a["duration"]:
            active[a["kind"]] = elapsed
            active[a["kind"] + "_duration"] = a["duration"]
    return active, distance


def drawing(p, t):
    active, distance = motion(p, t)
    cfg = p["character"]
    s = cfg["scale"]
    ox, oy = cfg["origin"]
    x = ox + distance
    y = oy
    walk_kind = "run" if "run" in active else "walk" if "walk" in active else None
    freq = 2.7 if walk_kind == "run" else 1.4
    phase = 2 * math.pi * freq * active[walk_kind] if walk_kind else 0
    stride = 48 if walk_kind == "run" else 30
    lift = 37 if walk_kind == "run" else 21
    bob = 6 * abs(math.sin(phase)) if walk_kind else 0
    y -= bob * s

    def P(dx, dy):
        return (x + dx*s, y + dy*s)

    def Q(pt):
        return [round(v, 4) for v in pt]

    def line(a, b, shade, width=5):
        return {"kind": "line", "points": [Q(a), Q(b)],
                "stroke": shade, "stroke_width": width*s}

    def ellipse(pt, rx, ry, shade, outline="#182823", border=2):
        return {"kind": "ellipse", "x": pt[0]-rx*s, "y": pt[1]-ry*s,
                "width": 2*rx*s, "height": 2*ry*s, "fill": shade,
                "stroke": outline, "stroke_width": border*s}

    def polygon(coords, shade):
        return {"kind": "polygon", "points": [Q(z) for z in coords],
                "fill": shade, "stroke": "#182823", "stroke_width": 3*s}

    skin, top, pants, hair = (cfg[k] for k in ("skin", "clothes", "pants", "hair"))
    foot_l, foot_r = P(-26, 231), P(26, 231)
    if walk_kind:
        z = math.sin(phase)
        zz = math.sin(phase + math.pi)
        foot_l = P(-26 + stride*z, 231 - lift*max(0, z))
        foot_r = P(26 + stride*zz, 231 - lift*max(0, zz))
    hip_l, hip_r = P(-24, 72), P(24, 72)
    leg_l = solve_ik(hip_l, foot_l, 91*s, 93*s, 1)
    leg_r = solve_ik(hip_r, foot_r, 91*s, 93*s, -1)
    arms = []
    for side in (-1, 1):
        shoulder = P(46*side, -48)
        hand = P(side*111, 49)
        if walk_kind:
            arm_swing = math.sin(phase + (0 if side == 1 else math.pi))
            hand = P(side*107 + side*18*arm_swing, 46 - 42*arm_swing)
        if side == 1 and "wave" in active:
            u = active["wave"] / active["wave_duration"]
            envelope = min(1, u*5, (1-u)*5)
            hand = P(106 + envelope*20*math.sin(2*math.pi*3*u), -113-envelope*30)
        arms.append(solve_ik(shoulder, hand, 76*s, 75*s, -side))
    back = []
    for leg in (leg_l, leg_r):
        back += [line(leg["shoulder"], leg["elbow"], pants, 22),
                 line(leg["elbow"], leg["wrist"], pants, 17),
                 ellipse(leg["wrist"], 17, 8, hair)]
    for arm in (arms[0],):
        back += [line(arm["shoulder"], arm["elbow"], top, 19),
                 line(arm["elbow"], arm["wrist"], skin, 14),
                 ellipse(arm["wrist"], 10, 10, skin)]
    body = [polygon([P(-51,-52), P(51,-52), P(56,70), P(-56,70)], top),
            ellipse(P(0,-125), 43, 52, skin),
            ellipse(P(0,-166), 43, 15, hair)]
    nod = math.sin(2*math.pi*2*active["nod"])*8 if "nod" in active else 0
    face = []
    face_y = -130 + nod
    blink = "blink" in active and math.sin(math.pi*active["blink"]/active["blink_duration"]) > 0.4
    for sx in (-16, 16):
        if blink:
            face.append(line(P(sx-7, face_y), P(sx+7, face_y), hair, 2))
        else:
            face.append(ellipse(P(sx, face_y), 3.5, 5, hair, hair, 0))
    face.append(ellipse(P(0, face_y+15), 3, 4, "#C98F75", "#C98F75", 0))
    happy = "smile" in active
    mouth_y = face_y+29
    if happy:
        mouth = [P(-17,mouth_y), P(-9,mouth_y+8), P(0,mouth_y+11),
                 P(9,mouth_y+8), P(17,mouth_y)]
    else:
        mouth = [P(-12,mouth_y), P(12,mouth_y)]
    face.append({"kind":"line", "points":[Q(z) for z in mouth],
                 "stroke":hair, "stroke_width":2.5*s})
    front = []
    arm = arms[1]
    front += [line(arm["shoulder"],arm["elbow"],top,20),
              line(arm["elbow"],arm["wrist"],skin,15),
              ellipse(arm["elbow"],8,8,skin),
              ellipse(arm["wrist"],10,10,skin)]
    floor = [{"kind":"rectangle","x":0,"y":p["height"]-32,"width":p["width"],
              "height":32,"fill":"#E7D8BE","stroke_width":0}]
    layers = [
        {"name":"ground","visible":True,"shapes":floor},
        {"name":"back limbs","visible":True,"shapes":back},
        {"name":"torso and head","visible":True,"shapes":body},
        {"name":"facial expression","visible":True,"shapes":face},
        {"name":"front arm","visible":True,"shapes":front}
    ]
    for item in layers:
        item["opacity"] = 1
    return {"schema":"kosif.paint.v1","width":p["width"],"height":p["height"],
            "background":p["background"],"layers":layers}


def export(p, destination, fps=24, at=0, audio=None):
    dest = Path(destination)
    if dest.exists():
        raise ValueError("refusing to overwrite an existing output")
    fps = int(num(fps, 1, 60))
    kind = dest.suffix.lower()
    if kind not in (".png", ".svg", ".gif", ".mp4"):
        raise ValueError("supported formats: PNG SVG GIF MP4")
    if audio and kind != ".mp4":
        raise ValueError("audio permitted only with MP4")
    frames = 1
    with tempfile.TemporaryDirectory(prefix="kosif-fullbody-") as work:
        work = Path(work)
        temp = work / ("final" + kind)
        if kind == ".png":
            paint(drawing(p, at)).save(temp)
        elif kind == ".svg":
            temp.write_text(svg(drawing(p, at)), encoding="utf-8")
        else:
            frames = round(p["duration"]*fps)
            if abs(frames / fps - p["duration"]) > 1e-8 or frames > MAX_FRAMES:
                raise ValueError("duration must be exact frame count within 600")
            if kind == ".mp4" and not shutil.which("ffmpeg"):
                raise ValueError("ffmpeg unavailable")
            if audio:
                streams = probe(audio, "a:0")
                if not streams or streams[0].get("codec_name") != "aac":
                    raise ValueError("AAC audio required for lossless packet copy")
                if abs(float(streams[0].get("duration") or 0)-p["duration"]) > 1/fps+0.02:
                    raise ValueError("audio duration must match video")
            images = []
            for index in range(frames):
                img = paint(drawing(p, index/fps)).convert("RGB")
                if kind == ".gif":
                    images.append(img)
                else:
                    img.save(work / f"{index:05d}.png")
            if kind == ".gif":
                images[0].save(temp, save_all=True, append_images=images[1:],
                               duration=round(1000/fps), loop=0, optimize=False)
            else:
                silent = work/"silent.mp4"
                subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(fps),
                                "-i",str(work/"%05d.png"),"-frames:v",str(frames),
                                "-c:v","libx264","-pix_fmt","yuv420p","-crf","19",str(silent)],
                               check=True, capture_output=True)
                if audio:
                    subprocess.run(["ffmpeg","-v","error","-y","-i",str(silent),"-i",
                                    str(audio),"-map","0:v:0","-map","1:a:0","-c:v","copy",
                                    "-c:a","copy",str(temp)],check=True,capture_output=True)
                    if packet_hashes(audio) != packet_hashes(temp):
                        raise ValueError("original AAC packets changed")
                else:
                    shutil.copyfile(silent, temp)
                if probe(temp,"v:0")[0]["codec_name"] != "h264":
                    raise ValueError("H264 verification failed")
        if dest.exists():
            raise ValueError("output appeared concurrently; not overwriting")
        shutil.copyfile(temp, dest)
    return {"verified":dest.stat().st_size>100,"output":str(dest),"frames":frames,
            "sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
            "audio_packets_preserved":bool(audio),"format":kind[1:]}


def main():
    parser=argparse.ArgumentParser(description="KOSIF original full body character animator")
    sub=parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    r=sub.add_parser("render")
    r.add_argument("--scene",required=True)
    r.add_argument("--words")
    r.add_argument("--output",required=True)
    r.add_argument("--fps",type=int,default=24)
    r.add_argument("--time",type=float,default=0)
    r.add_argument("--audio")
    args=parser.parse_args()
    if args.command == "doctor":
        print(json.dumps({"schema":SCHEMA,"ffmpeg":bool(shutil.which("ffmpeg")),
                          "exports":["png","svg","gif","mp4"],"actions":sorted(KINDS)}))
        return 0
    try:
        scene=json.loads(Path(args.scene).read_text(encoding="utf-8-sig"))
        prepared=prepare(scene, words_from_file(args.words))
        print(json.dumps(export(prepared,args.output,args.fps,args.time,args.audio)))
        return 0
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as exc:
        print(json.dumps({"verified":False,"error":str(exc)}),file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
