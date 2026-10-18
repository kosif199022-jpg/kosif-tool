# Does a stream-copy trim land on the requested frame? (numpy + ffmpeg). Frame i is encoded as grey level 0.8*i.
import subprocess, sys, json, numpy as np
d = sys.argv[1]; W, H, N = 320, 180, 300
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
    '-c:v', 'libx264', '-g', '60', '-keyint_min', '60', '-sc_threshold', '0', '-crf', '10', '-pix_fmt', 'yuv420p', f'{d}/src.mp4'], stdin=subprocess.PIPE)
for i in range(N): p.stdin.write(np.full((H, W), int(round(0.8 * i)), np.uint8).tobytes())
p.stdin.close(); p.wait()
def first_frames(f, k=3):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-frames:v', str(k), '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return [round(float(np.frombuffer(raw[j*W*H:(j+1)*W*H], np.uint8).mean()) / 0.8, 1) for j in range(k)]
def info(f):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames:format=duration', '-of', 'json', f], capture_output=True, text=True).stdout)
    return int(j['streams'][0]['nb_read_frames']), float(j['format']['duration'])
A, B = '1.3', '3.3'                                     # want source frames 39..98 (60 frames)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', A, '-to', B, '-i', f'{d}/src.mp4', '-c', 'copy', f'{d}/copy_in.mp4'])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{d}/src.mp4', '-ss', A, '-to', B, '-c', 'copy', f'{d}/copy_out.mp4'])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', A, '-to', B, '-i', f'{d}/src.mp4', '-c:v', 'libx264', '-crf', '10', f'{d}/reenc.mp4'])
for name in ('copy_in', 'copy_out', 'reenc'):
    n, dur = info(f'{d}/{name}.mp4'); print(f'{name:9s} decoded frames {n:3d}  duration {dur:.3f}s  first frames (source index) {first_frames(f"{d}/{name}.mp4")}')
print('requested: 60 frames, first = source frame 39 (1.3 s); keyframes every 60 frames (0, 2.0 s, 4.0 s ...)')
