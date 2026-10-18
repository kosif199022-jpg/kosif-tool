# Builds plate@2x.jpg: the background behind the people, flags removed (sky inpainted) so wind-displaced flags never double.
import cv2, numpy as np, os
src = 'assets/photo@2x.jpg' if os.path.exists('assets/photo@2x.jpg') else None
im1 = cv2.imread('assets/photo.png')
p2 = cv2.imread(src) if src else cv2.resize(im1, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
if not src: cv2.imwrite('assets/photo@2x.jpg', p2, [cv2.IMWRITE_JPEG_QUALITY, 94]); print('placeholder bicubic photo@2x')
H, W = p2.shape[:2]
# one joint hole = people + flags, so the fill only borrows sky, poles and buildings
a = cv2.imread('assets/fg.png', cv2.IMREAD_UNCHANGED)[:, :, 3]
m = cv2.dilate((a > 20).astype(np.uint8) * 255, np.ones((25, 25), np.uint8))
fm = cv2.imread('assets/flagmask.png', 0)
fmd = cv2.dilate((fm > 60).astype(np.uint8) * 255, np.ones((9, 9), np.uint8))
hole = m | fmd
s = 0.3; small = cv2.resize(im1, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
hs = cv2.resize(hole, (small.shape[1], small.shape[0]), interpolation=cv2.INTER_NEAREST)
inp = cv2.inpaint(small, hs, 12, cv2.INPAINT_TELEA)
# sky rows: replace the fill with the row's real sky colour (no pole streaks in the sky)
sm = small.astype(np.int16); skyp = (sm[:, :, 0] - sm[:, :, 2] > 25) & (sm[:, :, 0] > 150) & (hs == 0)
ytop = int(640 * s); last = None
for y in range(ytop):
    row = small[y][skyp[y]]
    col = np.median(row, 0) if len(row) > 8 else last
    if col is None: continue
    last = col
    k = np.clip((ytop - y) / (60 * s), 0, 1)  # fade to Telea near the buildings
    inp[y][hs[y] > 0] = (inp[y][hs[y] > 0] * (1 - k) + col * k).astype(np.uint8)
inp = cv2.GaussianBlur(cv2.resize(inp, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 9)
ff = cv2.resize(cv2.GaussianBlur(hole, (0, 0), 4), (W, H)).astype(np.float32)[:, :, None] / 255
plate = (p2 * (1 - ff) + inp * ff).astype(np.uint8)
cv2.imwrite('assets/plate@2x.jpg', plate, [cv2.IMWRITE_JPEG_QUALITY, 92])
cv2.imwrite('/tmp/claude-0/-home-user-kosif-tool/d758488b-c8f1-57b4-af58-3bc7882c4b5c/scratchpad/plate.jpg', cv2.resize(plate, (470, 836)))
print('plate', plate.shape)
