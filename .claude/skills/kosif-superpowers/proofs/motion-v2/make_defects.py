# Build a 4 s 30 fps test clip with known defects, write raw frames to ffmpeg (numpy only).
import subprocess, sys, numpy as np
W, H, FPS, N = 640, 360, 30, 120
out = sys.argv[1]; shift = '--timing' in sys.argv
yy, xx = np.mgrid[0:H, 0:W]
def frame(i, x):
    img = np.full((H, W, 3), 30, np.uint8)
    m = (xx - x) ** 2 + (yy - 180) ** 2 < 40 ** 2; img[m] = (230, 200, 60)
    return img
xs = []; x = 60.0
for i in range(N):
    if i == 50: x += 220                       # JUMP: object teleports and keeps moving
    if 70 <= i <= 81: pass                     # FREEZE: 12 identical frames
    else: x += 4
    xs.append(x)
cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
if shift: cmd += ['-vf', "setpts='(N+0.24*eq(N,60))/30/TB'", '-fps_mode', 'passthrough']
cmd += ['-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(N):
    img = frame(i, xs[i] % (W + 80) - 40)
    if i == 30: img[:] = 255                   # OUTLIER: a one-frame white flash
    p.stdin.write(img.tobytes())
p.stdin.close(); p.wait(); print('wrote', out, 'defects: flash@30, jump@50, freeze 70-81' + (', pts shift @60' if shift else ''))
