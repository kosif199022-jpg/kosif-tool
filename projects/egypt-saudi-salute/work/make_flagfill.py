# Flag layer extended behind the heads (colour by inpaint, extent by interpolating each flag's bottom edge).
import cv2, numpy as np
im = cv2.imread('assets/photo.png'); H, W = im.shape[:2]
fm = (cv2.imread('assets/flagmask.png', 0) > 128).astype(np.uint8)
pa = (cv2.imread('assets/fg.png', cv2.IMREAD_UNCHANGED)[:, :, 3] > 20).astype(np.uint8)
ext = fm.copy()
for x0, x1 in [(46, 490), (506, 941)]:
    cols = np.arange(x0, x1); bot = np.full(len(cols), np.nan); top = np.full(len(cols), np.nan)
    for i, x in enumerate(cols):
        ys = np.where(fm[:, x])[0]
        if len(ys) == 0: continue
        # column is trustworthy if the pixel just below the flag bottom is not a person
        yb = ys.max()
        if yb + 3 < H and pa[yb + 3, x] == 0: bot[i] = yb
        top[i] = ys.min()
    ok = ~np.isnan(bot)
    bi = np.interp(np.arange(len(cols)), np.where(ok)[0], bot[ok])
    for i, x in enumerate(cols):
        if np.isnan(top[i]): continue
        ext[int(top[i]):int(bi[i]) + 1, x] = 1
ext = cv2.morphologyEx(ext, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
hole = ((ext == 1) & (pa == 1)).astype(np.uint8) * 255
hole = cv2.dilate(hole, np.ones((15, 15), np.uint8)) & (ext * 255)
col = cv2.inpaint(im, hole, 7, cv2.INPAINT_TELEA)
P = cv2.resize(cv2.imread('assets/photo@2x.jpg'), (W * 2, H * 2))
c2 = cv2.resize(col, (W * 2, H * 2), interpolation=cv2.INTER_CUBIC)
h2 = cv2.resize(cv2.GaussianBlur(hole, (0, 0), 2), (W * 2, H * 2)).astype(np.float32)[:, :, None] / 255
rgb = (P * (1 - h2) + c2 * h2).astype(np.uint8)
a2 = cv2.resize(cv2.GaussianBlur(ext * 255, (0, 0), 1.2), (W * 2, H * 2), interpolation=cv2.INTER_LINEAR)
cv2.imwrite('assets/flagfill@2x.png', np.dstack([rgb, a2])[: 640 * 2])
v = cv2.resize(np.dstack([rgb, a2])[:1240], (470, 310)); bg = np.zeros_like(v[:, :, :3]); bg[:] = (255, 0, 255)
al = v[:, :, 3:4] / 255; cv2.imwrite('/tmp/claude-0/-home-user-kosif-tool/d758488b-c8f1-57b4-af58-3bc7882c4b5c/scratchpad/ff.jpg', (v[:, :, :3] * al + bg * (1 - al)).astype(np.uint8))
