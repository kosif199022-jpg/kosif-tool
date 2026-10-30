#!/bin/zsh
# living_loop.sh <in.mp4> <out.mp4> : forward + reversed, seamless loop, web size (960 wide), no audio.
# Use on a Seedance clip whose start image = end image. The reversed half drops its first frame
# so the turn has no duplicate (a visible stall).
[[ -r "$1" && -n "$2" ]] || { echo "usage: living_loop.sh <in.mp4> <out.mp4>"; exit 1; }
command -v ffmpeg >/dev/null || { echo "missing dependency: ffmpeg"; exit 1; }
ffmpeg -v error -y -i "$1" -filter_complex "[0:v]scale=960:-2,split[a][b];[b]reverse,trim=start_frame=1,setpts=PTS-STARTPTS[r];[a][r]concat=n=2:v=1[v]" -map "[v]" -an -c:v libx264 -crf 25 -preset slow -pix_fmt yuv420p -movflags +faststart "$2" && echo "OK $2"
