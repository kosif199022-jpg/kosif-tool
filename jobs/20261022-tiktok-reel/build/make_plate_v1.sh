#!/bin/sh
# Builds the 960x1200 (4:5) footage plate for the panel: 7 shots cut on the dua's phrases, 0.4 s transitions.
set -e
C="crop='if(gt(iw/ih,0.8),ih*0.8,iw)':'if(gt(iw/ih,0.8),ih,iw/0.8)',scale=960:1200,setsar=1,fps=30,format=yuv420p"
ffmpeg -nostats -loglevel error -y \
 -ss 2  -t 2.1 -i stock/30148493.mp4 \
 -ss 1  -t 2.68 -i stock/13348531.mp4 \
 -ss 2  -t 3.08 -i stock/11803764.mp4 \
 -ss 10 -t 1.74 -i stock/2960875.mp4 \
 -ss 1  -t 1.94 -i stock/29107904.mp4 \
 -ss 2  -t 3.76 -i stock/10662285.mp4 \
 -ss 4  -t 2.8 -i stock/15357599.mp4 \
 -filter_complex "\
[0:v]$C[v0];[1:v]$C[v1];[2:v]$C[v2];[3:v]$C[v3];[4:v]$C[v4];[5:v]$C[v5];[6:v]$C[v6];\
[v0][v1]xfade=transition=fade:duration=0.4:offset=1.70[x1];\
[x1][v2]xfade=transition=circleopen:duration=0.4:offset=3.98[x2];\
[x2][v3]xfade=transition=wipedown:duration=0.4:offset=6.66[x3];\
[x3][v4]xfade=transition=fadewhite:duration=0.4:offset=8.00[x4];\
[x4][v5]xfade=transition=smoothup:duration=0.4:offset=9.54[x5];\
[x5][v6]xfade=transition=fade:duration=0.4:offset=12.90[x6]" \
 -map "[x6]" -an -q:v 3 build/plate/%04d.jpg
