#!/usr/bin/env python3
"""يحوّل قائمة قرارات المونتاج (EDL بصيغة JSON) إلى أمر ffmpeg واحد بـ filter_complex وينفّذه: قصّ، وانتقالات xfade/acrossfade، وسرعة، وLUT، وترجمة محروقة، وتطبيع صوت بمرورين، ونسخ بنسب متعددة.

usage:
  python edl_render.py edl.json --out final.mp4 [--dry-run] [--ratios 16:9,9:16] [--copy]
--dry-run يطبع الأمر فقط. --copy يحاول نسخ التدفق بلا إعادة ترميز (يتطلب قطعاً على إطارات مفتاحية وبلا انتقالات/سرعة/LUT).

edl.json:
{
 "fps": 30, "size": [1920, 1080],
 "sources": {"a": "clip1.mp4", "b": "clip2.mp4", "music": "track.mp3"},
 "clips": [
   {"src": "a", "in": 2.0, "out": 8.5, "speed": 1.0, "transition": {"type": "cut"}},
   {"src": "b", "in": 0.0, "out": 6.0, "transition": {"type": "fade", "duration": 0.5}},   # xfade: fade|wipeleft|slideright|circleopen|dissolve|pixelize|…
   {"src": "a", "in": 20, "out": 24, "speed": 2.0, "transition": {"type": "cut"}, "audio_lead": 0.4}  # J-cut: صوت المقطع يبدأ قبل صورته بـ 0.4 ث
 ],
 "music": {"src": "music", "gain_db": -18, "fade_out": 2.0},
 "lut": "looks/teal-orange.cube",
 "captions": "captions.srt",
 "audio": {"loudnorm": {"I": -14, "TP": -1.0, "LRA": 11}}
}
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

XFADE = {"fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown", "circleopen", "circleclose",
         "dissolve", "pixelize", "radial", "smoothleft", "smoothright", "fadeblack", "fadewhite", "distance", "hblur", "zoomin", "squeezeh", "squeezev"}
RATIO_SIZE = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350)}


def run(cmd, dry):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(" ".join(f'"{c}"' if " " in c else c for c in cmd))
    if dry:
        return ""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{r.stderr[-3000:]}")
    return r.stderr


def measure_loudness(path, I, TP, LRA):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    return json.loads(m.group(0)) if m else None


def build(edl, out, size, dry, copy_mode):
    fps = edl.get("fps", 30)
    W, H = size
    src = edl["sources"]
    clips = edl["clips"]
    inputs, fc, order = [], [], {}
    for k, (name, path) in enumerate(src.items()):
        order[name] = k; inputs += ["-i", path]
    vlabels, alabels, durs = [], [], []
    for i, c in enumerate(clips):
        n = order[c["src"]]
        speed = float(c.get("speed", 1.0))
        d = (c["out"] - c["in"]) / speed
        durs.append(d)
        v = f"[{n}:v]trim=start={c['in']}:end={c['out']},setpts=(PTS-STARTPTS)/{speed},fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,format=yuv420p[v{i}]"
        lead = float(c.get("audio_lead", 0))
        a_in = max(0.0, c["in"] - lead)
        a = f"[{n}:a]atrim=start={a_in}:end={c['out']},asetpts=PTS-STARTPTS,atempo={min(max(speed, 0.5), 2.0)},aformat=sample_rates=48000:channel_layouts=stereo[a{i}]"
        fc += [v, a]; vlabels.append(f"[v{i}]"); alabels.append(f"[a{i}]")
    # chain with transitions
    cur_v, cur_a, total = vlabels[0], alabels[0], durs[0]
    for i in range(1, len(clips)):
        tr = clips[i].get("transition", {"type": "cut"})
        t = tr.get("type", "cut"); td = float(tr.get("duration", 0.5))
        if t == "cut" or t not in XFADE:
            fc.append(f"{cur_v}{vlabels[i]}concat=n=2:v=1:a=0[vc{i}]"); fc.append(f"{cur_a}{alabels[i]}concat=n=2:v=0:a=1[ac{i}]")
            total += durs[i]
        else:
            off = max(0.0, total - td)
            fc.append(f"{cur_v}{vlabels[i]}xfade=transition={t}:duration={td}:offset={off:.3f}[vc{i}]")
            fc.append(f"{cur_a}{alabels[i]}acrossfade=d={td}:c1=tri:c2=tri[ac{i}]")
            total += durs[i] - td
        cur_v, cur_a = f"[vc{i}]", f"[ac{i}]"
    # LUT + captions
    vf = []
    if edl.get("lut"):
        vf.append(f"lut3d=file='{edl['lut'].replace(chr(92), '/')}'")
    if edl.get("captions"):
        cap = edl["captions"].replace("\\", "/").replace(":", "\\:")
        vf.append(f"subtitles='{cap}':force_style='FontName=Cairo,FontSize=22,Outline=2,MarginV=60'")
    if vf:
        fc.append(f"{cur_v}{','.join(vf)}[vfinal]"); cur_v = "[vfinal]"
    # music bed
    if edl.get("music"):
        m = edl["music"]; n = order[m["src"]]
        gain = float(m.get("gain_db", -18)); fo = float(m.get("fade_out", 2.0))
        fc.append(f"[{n}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={gain}dB,afade=t=out:st={max(0, total - fo):.3f}:d={fo}[mus]")
        fc.append(f"{cur_a}[mus]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[amix]"); cur_a = "[amix]"
    ln = (edl.get("audio") or {}).get("loudnorm")
    tmp = out + ".pass1.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", cur_v, "-map", cur_a,
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "-shortest", tmp if ln else out]
    run(cmd, dry)
    if ln and not dry:
        meas = measure_loudness(tmp, ln["I"], ln["TP"], ln["LRA"])
        if meas:
            af = (f"loudnorm=I={ln['I']}:TP={ln['TP']}:LRA={ln['LRA']}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
                  f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], dry)
            os.remove(tmp)
        else:
            shutil.move(tmp, out)
    return total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("edl")
    ap.add_argument("--out", default="final.mp4")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ratios", default="", help="نسخ إضافية مثل 9:16,1:1 (قصّ ذكي من المنتصف)")
    ap.add_argument("--copy", action="store_true", help="نسخ تدفق بلا ترميز (قطع على إطارات مفتاحية فقط)")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg غير موجود")
    edl = json.load(open(a.edl, encoding="utf-8"))
    if a.copy:
        # stream-copy path: concat demuxer with -ss/-to per clip into temp files
        parts = []
        for i, c in enumerate(edl["clips"]):
            p = f"{a.out}.part{i}.mp4"
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(c["in"]), "-i", edl["sources"][c["src"]], "-to", str(c["out"] - c["in"]),
                 "-c", "copy", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart", p], a.dry_run)
            parts.append(p)
        lst = a.out + ".txt"
        open(lst, "w", encoding="utf-8").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", a.out], a.dry_run)
        if not a.dry_run:
            for p in parts + [lst]:
                os.remove(p)
        print(json.dumps({"out": a.out, "mode": "stream-copy", "note": "القطع انحاز إلى أقرب إطار مفتاحي؛ للدقة الإطارية أعد الترميز"}, ensure_ascii=False))
        return
    size = edl.get("size") or [1920, 1080]
    total = build(edl, a.out, size, a.dry_run, False)
    extra = {}
    for r in [x for x in a.ratios.split(",") if x.strip()]:
        if r in RATIO_SIZE:
            o = re.sub(r"\.mp4$", f"-{r.replace(':', 'x')}.mp4", a.out)
            build(edl, o, RATIO_SIZE[r], a.dry_run, False); extra[r] = o
    rep = {"out": a.out, "expected_duration_s": round(total, 3), "extra": extra}
    if not a.dry_run:
        pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.out], capture_output=True, text=True)
        got = float(pr.stdout.strip() or 0); rep["actual_duration_s"] = round(got, 3)
        rep["duration_ok"] = abs(got - total) <= 1.5 / edl.get("fps", 30)
    print(json.dumps(rep, ensure_ascii=False))


if __name__ == "__main__":
    main()
