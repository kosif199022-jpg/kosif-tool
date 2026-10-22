#!/usr/bin/env python3
"""دعاء الجمعة — ورك فلو قابل للتكرار (KOSIF).

  python3 jumuah.py setup  --work W                       # يجلب الخطوط والإيموجي إلى W/cache
  python3 jumuah.py text   --work W [--date D] [--handle H] # يبني طبقات النص (PNG شفافة)
  python3 jumuah.py render --work W --audio REF.mp4 --clips DIR [--out F]
  python3 jumuah.py verify --work W --audio REF.mp4 [--out F]
  python3 jumuah.py all    --work W --audio REF.mp4 --clips DIR --date D
  python3 jumuah.py extract --ref REF.mp4                 # (اختياري) يعيد استخراج العنوانين إلى assets/

المقاطع في DIR بأسماء <pexels_id>.mp4 كما في config.json.
"""
import argparse, json, math, os, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(BASE, 'config.json'), encoding='utf-8'))
W, H = CFG['size']
LY = CFG['layout']
SERIF_CANDS = ['/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf', 'C:/Windows/Fonts/times.ttf']
SANS_CANDS = ['/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 'C:/Windows/Fonts/arial.ttf']


def first(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    sys.exit('font not found: ' + ' | '.join(paths))


def run(cmd, **kw):
    print('$', ' '.join(cmd)); return subprocess.run(cmd, check=True, **kw)


# ---------------------------------------------------------------- setup
def cmd_setup(a):
    c = os.path.join(a.work, 'cache'); os.makedirs(c, exist_ok=True)
    if not os.path.exists(os.path.join(c, 'gfonts', 'ofl', 'amiri', 'Amiri-Bold.ttf')):
        run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse', 'https://github.com/google/fonts', os.path.join(c, 'gfonts')])
        run(['git', '-C', os.path.join(c, 'gfonts'), 'sparse-checkout', 'set', 'ofl/amiri'])
    em = CFG['emoji_last_line']
    if not os.path.exists(os.path.join(c, 'emoji', '2D', 'png', '512', f'emoji_u{em}.png')):
        run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse', 'https://github.com/googlefonts/noto-emoji', os.path.join(c, 'emoji')])
        run(['git', '-C', os.path.join(c, 'emoji'), 'sparse-checkout', 'set', '--no-cone', f'/2D/png/512/emoji_u{em}.png'])
    first(SERIF_CANDS); first(SANS_CANDS)
    print('setup ok')


# ---------------------------------------------------------------- text layers
def save_rgba(path, im):
    im.save(path) if isinstance(im, Image.Image) else cv2.imwrite(path, im)


def tracked(txt, font, size, right, baseline, width):
    ft = ImageFont.truetype(font, size)
    d = ImageDraw.Draw(Image.new('L', (1, 1)))
    ws = [d.textlength(ch, font=ft) for ch in txt]
    tr = (width - sum(ws)) / (len(txt) - 1)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    x = right - (sum(ws) + tr * (len(txt) - 1)); x0 = x; xs = []
    for ch, w in zip(txt, ws):
        dr.text((x, baseline), ch, font=ft, fill=(255, 255, 255, 255), anchor='ls'); xs.append(x); x += w + tr
    return im, x0, xs, ws, tr


def cmd_text(a):
    date = a.date or CFG['date']; handle = a.handle or CFG['handle']
    ov = os.path.join(a.work, 'ov'); os.makedirs(ov, exist_ok=True)
    cache = os.path.join(a.work, 'cache')
    for n in ('header', 'gold'):
        Image.open(os.path.join(BASE, 'assets', n + '.png')).save(os.path.join(ov, n + '.png'))
    # date split into day (flies in) + rest
    full, x0, xs, ws, tr = tracked(date, first(SERIF_CANDS), LY['date_size'], LY['date_right'], LY['date_baseline'], LY['date_width'])
    dot = date.index('.'); split = int(xs[dot] - tr / 2)
    arr = np.array(full); day = arr.copy(); day[:, split:] = 0; rest = arr.copy(); rest[:, :split] = 0
    Image.fromarray(day).save(os.path.join(ov, 'day.png')); Image.fromarray(rest).save(os.path.join(ov, 'daterest.png'))
    json.dump({'day_center': [(x0 + split) / 2, LY['date_baseline'] - LY['date_size'] * 0.33]}, open(os.path.join(ov, 'day.json'), 'w'))
    # watermark
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((LY['wm_center_x'], LY['wm_baseline']), handle, font=ImageFont.truetype(first(SANS_CANDS), LY['wm_size']), fill=(255, 255, 255, 235), anchor='ms')
    im.save(os.path.join(ov, 'wm.png'))
    # dua lines
    amiri = os.path.join(cache, 'gfonts', 'ofl', 'amiri', 'Amiri-Bold.ttf')
    ft = ImageFont.truetype(amiri, LY['dua_size'], layout_engine=ImageFont.Layout.RAQM)
    cx, cy = LY['dua_center']
    for k, lines in enumerate(CFG['dua']):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        ys = [cy] if len(lines) == 1 else LY['dua_two_lines_y']
        for t, y in zip(lines, ys):
            dr.text((cx, y), t, font=ft, fill=(255, 255, 255, 255), anchor='mm', direction='rtl', stroke_width=1, stroke_fill=(255, 255, 255, 255))
        if k == len(CFG['dua']) - 1 and CFG.get('emoji_last_line'):
            e = Image.open(os.path.join(cache, 'emoji', '2D', 'png', '512', f"emoji_u{CFG['emoji_last_line']}.png")).convert('RGBA')
            e = e.crop(e.getbbox()); es = int(LY['dua_size'] * 0.8); e = e.resize((int(es * e.width / e.height), es), Image.LANCZOS)
            shift = int(es / 2 + 5); im2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); im2.paste(im, (shift, 0)); im = im2
            bb = im.getbbox(); im.paste(e, (bb[0] - e.width - 14, int(cy - es / 2 + 4)), e)
        im.save(os.path.join(ov, f'dua{k}.png'))
    print('text layers ->', ov, '| date', date, '| handle', handle)


# ---------------------------------------------------------------- render
def easeIn(u): return u * u * u
def easeOut(u): return 1 - (1 - u) ** 3


def fit(g):
    h, w = g.shape[:2]; s = max(W / w, H / h)
    g = cv2.resize(g, (math.ceil(w * s), math.ceil(h * s)), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    y = (g.shape[0] - H) // 2; x = (g.shape[1] - W) // 2; return g[y:y + H, x:x + W]


def cmd_render(a):
    SEG = CFG['segments']; N = CFG['frames']; OUT = CFG['transitions_out']; IN = CFG['transitions_in']
    out_path = a.out or os.path.join(a.work, f"dua_jumuah_{(a.date or CFG['date']).replace('.', '-')}.mp4")
    # reference luma per segment (grade match) — from the reference video if it has a video stream
    refY = []
    cap = cv2.VideoCapture(a.audio)
    while True:
        r, f = cap.read()
        if not r: break
        refY.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).mean())
    clips = []
    for sg in SEG:
        p = os.path.join(a.clips, f"{sg['pexels_id']}.mp4")
        c = cv2.VideoCapture(p); fps = c.get(cv2.CAP_PROP_FPS); fr = []
        while True:
            r, f = c.read()
            if not r: break
            fr.append(f)
        if not fr: sys.exit('missing clip ' + p)
        need = [fit(fr[min(max(int(round((sg['in'] + (n - sg['start']) / 30.0) * fps)), 0), len(fr) - 1)]) for n in range(sg['start'] - 2, sg['end'] + 2)]
        if len(refY) >= sg['end']:
            cy = np.mean([cv2.cvtColor(x, cv2.COLOR_BGR2GRAY).mean() for x in need[2:-2]])
            gain = float(np.clip(np.mean(refY[max(sg['start'], 13):sg['end']]) / cy, 0.72, 1.12))
            lut = np.clip(np.arange(256) * gain, 0, 255).astype(np.uint8); need = [cv2.LUT(x, lut) for x in need]
        clips.append(need)

    def params(k, f):
        a0, b0 = SEG[k]['start'], SEG[k]['end']; s, dx, dy, ang = 1.0, 0.0, 0.0, 0.0
        o = OUT.get(str(k + 1) if k + 1 < len(SEG) else 'end')
        if o and f > b0 - o['W']:
            u = easeIn(min((f - (b0 - o['W'])) / o['W'], 1)); s *= 1 + (o.get('s', 1) - 1) * u
            dx += o.get('dx', 0) * u; dy += o.get('dy', 0) * u; ang += o.get('ang', 0) * u
        i = IN.get(str(k))
        if i and f < a0 + i['W']:
            u = 1 - easeOut(max((f - a0) / i['W'], 0)); s *= 1 + (i.get('s', 1) - 1) * u
            dx += i.get('dx', 0) * u; dy += i.get('dy', 0) * u
        return s, dx, dy, ang

    def warp(img, p):
        s, dx, dy, ang = p
        if abs(s - 1) < 1e-4 and abs(dx) < .01 and abs(dy) < .01 and abs(ang) < .01: return img.astype(np.float32)
        M = cv2.getRotationMatrix2D((W / 2, H / 2), ang, s); M[0, 2] += dx; M[1, 2] += dy
        return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101).astype(np.float32)

    def seg_of(n): return [i for i, sg in enumerate(SEG) if sg['start'] <= n < sg['end']][0]

    def video_frame(n):  # motion blur = average of sub-frame transforms (shutter 1 frame)
        k = seg_of(n); a0 = SEG[k]['start']; img = clips[k][n - a0 + 2]
        p0, p1 = params(k, n - 1.0), params(k, n)
        diff = max(abs(p1[0] - p0[0]) * 400, abs(p1[1] - p0[1]), abs(p1[2] - p0[2]), abs(p1[3] - p0[3]) * 10)
        if diff < 1.5: return warp(img, p1)
        ns = int(min(16, max(4, diff / 6))); acc = np.zeros((H, W, 3), np.float32)
        for j in range(ns):
            f = n - 1 + (j + 1) / ns if n > a0 else n + (j / ns) * 0.999
            acc += warp(img, params(k, f))
        return acc / ns

    ov = os.path.join(a.work, 'ov')
    names = ['header', 'gold', 'daterest', 'day', 'wm'] + [f'dua{k}' for k in range(len(CFG['dua']))]
    L = {n: cv2.imread(os.path.join(ov, n + '.png'), cv2.IMREAD_UNCHANGED).astype(np.float32) for n in names}

    def shadow(rgba, blur, op, off):
        sh = cv2.GaussianBlur(rgba[..., 3] / 255., (0, 0), blur)
        return cv2.warpAffine(sh, np.float32([[1, 0, off[0]], [0, 1, off[1]]]), (W, H)) * op
    SH = {n: np.clip(shadow(L[n], 3.5 if n == 'gold' else 3.0, .95 if n == 'gold' else .8, (1, 2)) + shadow(L[n], 8, .5, (0, 2)), 0, 1) for n in L}

    def put(base, n, op, dx=0, dy=0):
        if op <= .003: return base
        rgba, s = L[n], SH[n]
        if dx or dy:
            M = np.float32([[1, 0, dx], [0, 1, dy]]); rgba = cv2.warpAffine(rgba, M, (W, H)); s = cv2.warpAffine(s, M, (W, H))
        base = base * (1 - s[..., None] * op); al = rgba[..., 3:4] / 255. * op
        return base * (1 - al) + rgba[..., :3] * al

    dayc = json.load(open(os.path.join(ov, 'day.json')))['day_center']; start = LY['day_fly_from']
    last = len(SEG) - 1

    def textlayer(base, n):
        endf = 1 - np.clip((n - LY['end_fade_start']) / 10, 0, 1)
        for nm in ['header', 'gold', 'daterest', 'wm']: base = put(base, nm, endf)
        u = easeOut(min(n / LY['day_fly_frames'], 1)); ddx = (start[0] - dayc[0]) * (1 - u); ddy = (start[1] - dayc[1]) * (1 - u)
        if n >= SEG[last]['start']: ddx += LY['day_end_shift'] * easeOut(min((n - SEG[last]['start']) / 10, 1))
        base = put(base, 'day', endf, ddx, ddy)
        k = seg_of(n); a0, b0 = SEG[k]['start'], SEG[k]['end']
        fin = min((n - a0 + 1) / LY['dua_fade_in'], 1) if k > 0 else min(max(n - 2, 0) / 8, 1)
        fout = min((b0 - n) / LY['dua_fade_out'], 1) if k < last else endf
        return put(base, f'dua{k}', max(0, min(fin, fout)))

    frames = list(range(N))
    if a.preview: frames = [int(x) for x in a.preview.split(',')]
    p = None
    if not a.preview:
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(CFG['fps']), '-i', '-',
                              '-i', a.audio, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                              '-profile:v', 'high', '-c:a', 'copy', '-movflags', '+faststart', out_path], stdin=subprocess.PIPE)
    os.makedirs(os.path.join(a.work, 'preview'), exist_ok=True)
    for n in frames:
        o = textlayer(video_frame(n), n)
        if n <= LY['fade_in_black_frames']: o *= (n / LY['fade_in_black_frames']) ** 1.5
        o = np.clip(o, 0, 255).astype(np.uint8)
        if p: p.stdin.write(o.tobytes())
        else: cv2.imwrite(os.path.join(a.work, 'preview', f'f{n:03d}.jpg'), o)
    if p: p.stdin.close(); p.wait(); print('rendered ->', out_path)
    return out_path


# ---------------------------------------------------------------- verify
def cmd_verify(a):
    out = a.out or os.path.join(a.work, f"dua_jumuah_{(a.date or CFG['date']).replace('.', '-')}.mp4")
    pr = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,nb_frames,r_frame_rate,duration', '-of', 'json', out], capture_output=True, text=True)
    st = json.loads(pr.stdout)['streams']; v = [s for s in st if s['codec_type'] == 'video'][0]
    md5 = lambda f: subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-map', '0:a', '-c', 'copy', '-f', 'md5', '-'], capture_output=True, text=True).stdout.strip()
    m_ref, m_out = md5(a.audio), md5(out)
    checks = [('size', f"{v['width']}x{v['height']}", f'{W}x{H}'), ('fps', v['r_frame_rate'], f"{CFG['fps']}/1"),
              ('frames', v.get('nb_frames'), str(CFG['frames'])), ('audio md5', m_out, m_ref)]
    sheet = os.path.splitext(out)[0] + '_sheet.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', 'fps=2,scale=180:-1,tile=8x4', '-frames:v', '1', sheet])
    rep = ['# TEST_REPORT — دعاء الجمعة', '', f'الملف: `{os.path.basename(out)}`', '', '| المعيار | المقيس | المطلوب | النتيجة |', '|---|---|---|---|']
    ok = True
    for n, got, want in checks:
        good = str(got) == str(want); ok &= good; rep.append(f'| {n} | {got} | {want} | {"✅" if good else "❌"} |')
    rep += ['', f'لوحة لقطات: `{os.path.basename(sheet)}` (مراجعة بصرية بلقطات ثابتة).']
    open(os.path.join(a.work, 'TEST_REPORT.md'), 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
    print('\n'.join(rep)); sys.exit(0 if ok else 1)


# ---------------------------------------------------------------- extract (optional)
def cmd_extract(a):
    """يعيد استخراج «الجُمُعَة» و«ليلة جمعة مباركة» من فيديو مرجعي (الطبقة ثابتة والخلفية تتغير)."""
    cap = cv2.VideoCapture(a.ref); fr = []; i = 0
    while True:
        r, f = cap.read()
        if not r: break
        if i % 3 == 0 and 45 <= i <= 455: fr.append(f[:720])
        i += 1
    p8 = np.percentile(np.stack(fr), 8, axis=0).astype(np.uint8); p8 = np.vstack([p8, np.zeros((1024 - p8.shape[0], 576, 3), np.uint8)])
    ss = lambda x, lo, hi: np.clip((x - lo) / (hi - lo), 0, 1)
    def box(al, x0, y0, x1, y1): m = np.zeros_like(al); m[y0:y1, x0:x1] = al[y0:y1, x0:x1]; return m
    def to_rgba(al, col):
        al = cv2.resize(al, (W, H), interpolation=cv2.INTER_CUBIC).clip(0, 1); c = np.zeros((H, W, 3), np.float32); c[:] = col
        return np.dstack([c, al * 255]).clip(0, 255).astype(np.uint8)
    hdr = box(ss(p8.min(2).astype(np.float32), 95, 215), 300, 135, 535, 258)
    gold = box(ss(p8.max(2).astype(np.float32), 105, 215), 120, 350, 470, 420)
    gcol = np.median(p8[gold > .9].reshape(-1, 3), axis=0)
    cv2.imwrite(os.path.join(BASE, 'assets', 'header.png'), to_rgba(hdr, (250, 250, 250)))
    cv2.imwrite(os.path.join(BASE, 'assets', 'gold.png'), to_rgba(gold, tuple(float(v) for v in gcol)))
    print('assets re-extracted, gold BGR', gcol)


def main():
    ap = argparse.ArgumentParser(description='دعاء الجمعة workflow')
    sp = ap.add_subparsers(dest='cmd', required=True)
    for name in ('setup', 'text', 'render', 'verify', 'all'):
        s = sp.add_parser(name); s.add_argument('--work', default='work')
        s.add_argument('--date'); s.add_argument('--handle'); s.add_argument('--audio'); s.add_argument('--clips'); s.add_argument('--out'); s.add_argument('--preview')
    e = sp.add_parser('extract'); e.add_argument('--ref', required=True)
    a = ap.parse_args()
    if a.cmd == 'extract': return cmd_extract(a)
    os.makedirs(a.work, exist_ok=True)
    if a.cmd == 'setup': cmd_setup(a)
    elif a.cmd == 'text': cmd_text(a)
    elif a.cmd == 'render': cmd_render(a)
    elif a.cmd == 'verify': cmd_verify(a)
    elif a.cmd == 'all':
        cmd_setup(a); cmd_text(a); a.out = cmd_render(a); cmd_verify(a)


if __name__ == '__main__':
    main()
