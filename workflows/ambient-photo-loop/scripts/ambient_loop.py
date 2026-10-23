#!/usr/bin/env python3
"""Ambient photo loop: turn one still photo into a long, silent video where only
the sky, water, flags and light move. The person (found by a human-segmentation
model) is copied from the source photo into every frame unchanged.

  python3 ambient_loop.py masks  --image PHOTO --config config.json --out DIR
  python3 ambient_loop.py test   --config config.json --out DIR      # 4 stills + diff
  python3 ambient_loop.py render --config config.json --out DIR      # loop.mp4 -> final.mp4
  python3 ambient_loop.py verify --config config.json --out DIR      # person/loop checks
  python3 ambient_loop.py all    --image PHOTO --config config.json --out DIR

Needs: ffmpeg, numpy, opencv-python-headless, rembg (+ onnxruntime). rembg
downloads its model (~176 MB) on first use.
"""
import argparse, json, os, subprocess, sys
import numpy as np, cv2

TAU = 2 * np.pi


def load_cfg(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def cmd_masks(a, cfg):
    from rembg import remove, new_session
    from PIL import Image
    W, H = cfg['size']
    src = cv2.imread(a.image)
    if src is None:
        sys.exit(f'cannot read {a.image}')
    sh, sw = src.shape[:2]
    sx, sy = W / sw, H / sh
    img = cv2.resize(src, (W, H), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(os.path.join(a.out, 'base.png'), img)

    pm = remove(Image.open(a.image), session=new_session(cfg['person_model']), only_mask=True)
    pm = cv2.resize(np.array(pm), (W, H)).astype(np.float32) / 255
    pm = (pm > cfg['person_threshold']).astype(np.float32)
    d = cfg['person_dilate_px']
    pm = cv2.dilate(pm, np.ones((d, d), np.uint8))
    protect = np.clip(cv2.GaussianBlur(pm, (0, 0), 3), 0, 1)

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    pts = np.array(cfg['sky_skyline'], np.float32)
    lim = np.interp(np.arange(W), pts[:, 0] * sx, pts[:, 1] * sy)
    sky = (yy < lim[None, :] - 6).astype(np.float32)
    for x0, y0, x1, y1 in cfg['sky_exclude_boxes']:
        sky[int(y0 * sy):int(y1 * sy), int(x0 * sx):int(x1 * sx)] = 0
    sky = cv2.GaussianBlur(sky, (0, 0), 5) * (1 - protect)

    v = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 2].astype(np.float32)
    geo = np.zeros((H, W), np.float32)
    poly = np.array(cfg['water_polygon'], np.float32) * [sx, sy]
    cv2.fillPoly(geo, [poly.astype(np.int32)], 1)
    water = geo * np.clip((v - cfg['water_min_brightness']) / 50, 0, 1)
    water = cv2.GaussianBlur(water, (0, 0), 3) * (1 - protect)

    np.savez(os.path.join(a.out, 'masks.npz'), protect=protect, sky=sky, water=water)
    ov = img.astype(np.float32)
    ov[..., 2] += 120 * sky
    ov[..., 0] += 150 * water
    ov[..., 1] += 120 * protect
    cv2.imwrite(os.path.join(a.out, 'mask_overlay.jpg'),
                cv2.resize(np.clip(ov, 0, 255).astype(np.uint8), (W // 2, H // 2)))
    print('masks ->', a.out, '(red sky, blue water, green protected person)')


class Animator:
    def __init__(self, cfg, out, src_size):
        W, H = cfg['size']
        self.W, self.H, self.fps, self.T = W, H, cfg['fps'], float(cfg['loop_seconds'])
        self.img = cv2.imread(os.path.join(out, 'base.png')).astype(np.float32)
        m = np.load(os.path.join(out, 'masks.npz'))
        self.protect, sky, self.water = m['protect'], m['sky'], m['water']
        sw, sh = src_size
        sx, sy = W / sw, H / sh
        self.sx = sx
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        self.xx, self.yy = xx, yy

        flagw = np.zeros((H, W), np.float32)
        ramp = np.zeros((H, W), np.float32)
        for f in cfg['flags']:
            x0, y0, x1, y1 = f['box']
            b = np.zeros((H, W), np.float32)
            b[int(y0 * sy):int(y1 * sy), int(x0 * sx):int(x1 * sx)] = 1
            b = cv2.GaussianBlur(b, (0, 0), 14)
            flagw = np.maximum(flagw, b)
            # wave grows from 0 at the pole to full at the free end
            r = np.clip((xx - f['pole_x'] * sx) / ((x1 - f['pole_x']) * sx), 0, 1)
            ramp = np.where(b > 0.01, r, ramp)
        self.flagw = flagw * (1 - self.protect)
        self.ramp = ramp
        self.flag_amp = cfg['flag_wave_px']
        self.sky = sky * (1 - self.flagw)
        # higher clouds drift faster (cheap parallax)
        self.v = cfg['cloud_speed_px_s'] * (1.0 - 0.5 * np.clip(yy / (cfg['sky_skyline'][-1][1] * sy), 0, 1))

        def smooth_noise(seed, scale):
            r = np.random.default_rng(seed).random((H // scale + 2, W // scale + 2)).astype(np.float32)
            return cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC)
        self.n1 = smooth_noise(1, 24) * TAU
        self.n2 = smooth_noise(2, 40) * TAU
        self.hi = np.clip((self.img.mean(2) - 170) / 60, 0, 1) * self.water

        sun = (cfg['sun'][0] * sx, cfg['sun'][1] * sy)
        dsun = np.sqrt((xx - sun[0]) ** 2 + (yy - sun[1]) ** 2)
        self.sunglow = np.exp(-(dsun / (140 * sx)) ** 2) * (1 - self.protect)
        self.bg = 1 - self.protect
        self.warm = np.array([0.55, 0.8, 1.0], np.float32)  # BGR
        self.diag = xx * 0.55 + yy * 0.35
        self.sweep = cfg['light_sweep_strength']
        self.sunk = cfg['sun_glow_strength']

    def remap(self, dx, dy):
        return cv2.remap(self.img, self.xx + dx, self.yy + dy, cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT)

    def frame(self, i):
        img, xx, yy = self.img, self.xx, self.yy
        t = i / self.fps
        a = t / self.T          # 0..1 over one loop, every motion is periodic in T
        ph = TAU * a
        # clouds: crossfade two drifts so frame T equals frame 0 (seamless loop)
        A = self.remap(-self.v * t, 0)
        B = self.remap(-self.v * (t - self.T), 0)
        cl = A * (1 - a) + B * a
        out = img * (1 - self.sky[..., None]) + cl * self.sky[..., None]

        k = TAU / (110 * self.sx)
        dyf = self.flag_amp * self.ramp * np.sin(k * xx - 3 * ph)
        dxf = 0.375 * self.flag_amp * self.ramp * np.sin(k * xx * 0.7 - 3 * ph + 1.0)
        F = self.remap(dxf, dyf) * (1 + 0.06 * self.ramp * np.cos(k * xx - 3 * ph))[..., None]
        out = out * (1 - self.flagw[..., None]) + F * self.flagw[..., None]

        dyw = 1.1 * np.sin(yy * 0.21 + self.n1 - 6 * ph) + 0.6 * np.sin(xx * 0.05 + self.n2 + 4 * ph)
        dxw = 1.6 * np.sin(yy * 0.13 + self.n2 - 5 * ph)
        Wt = self.remap(dxw, dyw) * (1 + 0.10 * self.hi * np.sin(self.n1 * 3 + xx * 0.3 - 8 * ph))[..., None]
        out = out * (1 - self.water[..., None]) + Wt * self.water[..., None]

        dmin, dmax = self.diag.min(), self.diag.max()
        c = dmin + (dmax - dmin) * (-0.2 + 1.4 * a)
        band = np.exp(-((self.diag - c) / 260) ** 2) * np.sin(np.pi * a) ** 2
        glow = self.sweep * band * self.bg + self.sunk * self.sunglow * (0.5 + 0.5 * np.sin(ph))
        out = out + 255 * glow[..., None] * self.warm * (1 - out / 255)

        # the person is always the source pixels
        out = out * (1 - self.protect[..., None]) + img * self.protect[..., None]
        return np.clip(out + 0.5, 0, 255).astype(np.uint8)


def animator(a, cfg):
    with open(os.path.join(a.out, 'source_size.json')) as f:
        return Animator(cfg, a.out, tuple(json.load(f)))


def cmd_test(a, cfg):
    an = animator(a, cfg)
    n = int(an.T * an.fps)
    base = an.img
    for i in [0, n // 4, n // 2, 3 * n // 4]:
        f = an.frame(i)
        cv2.imwrite(os.path.join(a.out, f'test_{i:04d}.jpg'), f)
    d = np.clip(np.abs(f.astype(np.float32) - base).sum(2) * 3, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(a.out, 'test_diff.jpg'), d)
    print('test stills ->', a.out)


def cmd_render(a, cfg):
    an = animator(a, cfg)
    n = int(an.T * an.fps)
    loop = os.path.join(a.out, 'loop.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
                          '-s', f'{an.W}x{an.H}', '-r', str(an.fps), '-i', '-', '-c:v', 'libx264',
                          '-preset', 'slow', '-crf', str(cfg['crf']), '-pix_fmt', 'yuv420p', loop],
                         stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(an.frame(i).tobytes())
        if i % 120 == 0:
            print(f'frame {i}/{n}', flush=True)
    p.stdin.close()
    if p.wait():
        sys.exit('ffmpeg failed')
    reps = int(round(cfg['duration_seconds'] / an.T))
    lst = os.path.join(a.out, 'list.txt')
    with open(lst, 'w') as f:
        f.write("file 'loop.mp4'\n" * reps)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-c', 'copy', '-movflags', '+faststart', '-an', os.path.join(a.out, 'final.mp4')], check=True)
    print('final ->', os.path.join(a.out, 'final.mp4'))


def cmd_verify(a, cfg):
    path = os.path.join(a.out, 'final.mp4')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                            'format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames',
                            '-of', 'json', path], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    base = cv2.imread(os.path.join(a.out, 'base.png')).astype(np.float32)
    core = np.load(os.path.join(a.out, 'masks.npz'))['protect'] > 0.99
    cap = cv2.VideoCapture(path)
    dur = float(info['format']['duration'])
    loop = cfg['loop_seconds']
    rows = []
    for t in [0, loop - 1 / cfg['fps'], loop, dur / 2, dur - 0.1]:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        d = np.abs(f.astype(np.float32) - base).mean(2)
        rows.append({'t': round(t, 3), 'person_mean_abs_diff': round(float(d[core].mean()), 2),
                     'background_mean_abs_diff': round(float(d[~core].mean()), 2)})
    rep = {'probe': info, 'samples': rows,
           'note': 'person diff should be small and the same at every t (H.264/yuv420 only)'}
    with open(os.path.join(a.out, 'verify.json'), 'w') as f:
        json.dump(rep, f, indent=2)
    print(json.dumps(rep, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['masks', 'test', 'render', 'verify', 'all'])
    ap.add_argument('--image')
    ap.add_argument('--config', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    os.makedirs(a.out, exist_ok=True)
    if a.cmd in ('masks', 'all'):
        if not a.image:
            sys.exit('--image is required for masks/all')
        h, w = cv2.imread(a.image).shape[:2]
        with open(os.path.join(a.out, 'source_size.json'), 'w') as f:
            json.dump([w, h], f)
        cmd_masks(a, cfg)
    if a.cmd in ('test', 'all'):
        cmd_test(a, cfg)
    if a.cmd in ('render', 'all'):
        cmd_render(a, cfg)
    if a.cmd in ('verify', 'all'):
        cmd_verify(a, cfg)


if __name__ == '__main__':
    main()
