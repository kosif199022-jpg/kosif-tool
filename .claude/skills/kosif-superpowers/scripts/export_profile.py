#!/usr/bin/env python3
"""KOSIF delivery export standard: one place for the settings every final video uses.

The owner approved these after the "Dari Ya Albi" reel and asked for them on every
future export (same or better, never lower). Full rationale: playbooks/export-standard.md.

    size     1080x1920 (9:16) by default; no 4K unless the user asks for it
    fps      30
    video    H.264 High, CRF 17, preset slow, yuv420p, BT.709 tagged
    audio    the user's track stream-copied byte for byte when MP4 can carry it;
             AAC 320k 48 kHz only when the pipeline must cut or mix, or the codec
             cannot live in MP4 (WAV/FLAC sources)
    file     MP4 with +faststart
    colour   matched to the source by measurement (see the playbook), never a stock LUT

Use from another script in this folder:

    from export_profile import video_args, audio_args, FASTSTART
    cmd = ["ffmpeg", "-i", frames, "-i", voice, *video_args(), *audio_args(voice), *FASTSTART, out]

`python3 export_profile.py` prints the settings as JSON (also the source for tools/render_html.cjs).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CRF = 17            # lower = better; never raise it for a delivery file
PRESET = "slow"     # better compression at the same CRF than "medium"; never faster for delivery
PROFILE = "high"
PIX_FMT = "yuv420p"
# BT.709 is what phones and TikTok/Instagram assume for HD; tagging it stops players guessing.
COLOR_TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
# Filter that converts RGB frames (PNG renders) with the BT.709 matrix instead of ffmpeg's BT.601 default.
RGB_TO_709 = "scale=out_color_matrix=bt709:out_range=tv"
FASTSTART = ["-movflags", "+faststart"]
# Codecs an MP4 carries as-is, so the voice can be copied without re-encoding.
MP4_COPY_AUDIO = ("aac", "mp3", "alac")
AAC_FALLBACK = ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"]


def video_args(crf: int = CRF, preset: str = PRESET, fps: int | None = None) -> list[str]:
    """libx264 arguments for a delivery file. Quality can only go up from the standard."""
    crf = min(int(crf), CRF)
    args = ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-profile:v", PROFILE, "-pix_fmt", PIX_FMT, *COLOR_TAGS]
    if fps:
        args += ["-r", str(fps)]
    return args


def audio_codec(path) -> str | None:
    """First audio stream's codec name, or None when there is none or ffprobe is missing."""
    if not shutil.which("ffprobe"):
        return None
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return (r.stdout or "").strip().splitlines()[0] if r.returncode == 0 and r.stdout.strip() else None


def audio_args(path=None, *, must_reencode: bool = False) -> list[str]:
    """Copy the user's audio byte for byte when MP4 can hold it, else the AAC 320k floor.

    Pass must_reencode=True when a filter (cut at a non-packet point, mix, loudnorm,
    apad, aresample) touches the audio, because a filtered stream cannot be copied.
    """
    if not must_reencode and path is not None and audio_codec(path) in MP4_COPY_AUDIO:
        return ["-c:a", "copy"]
    return list(AAC_FALLBACK)


def profile() -> dict:
    return {"schema": "kosif.export-profile.v1", "width": WIDTH, "height": HEIGHT, "fps": FPS, "crf": CRF,
            "preset": PRESET, "profile": PROFILE, "pix_fmt": PIX_FMT, "color": "bt709", "faststart": True,
            "audio_copy_codecs": list(MP4_COPY_AUDIO), "audio_fallback": "aac 320k 48000",
            "four_k": "only when the user asks", "doc": "playbooks/export-standard.md"}


if __name__ == "__main__":
    json.dump(profile(), sys.stdout, indent=2)
    sys.stdout.write("\n")
