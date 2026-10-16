# Numeric checks of the speed-shape model (own code, numpy only).
import math, numpy as np
u = np.linspace(0, 1, 200001)
def bez(p0, p1, p2, p3): return (1-u)**3*p0 + 3*(1-u)**2*u*p1 + 3*(1-u)*u**2*p2 + u**3*p3
def ae_speed_ratio(a):                 # AE temporal ease: zero speed at both keys, influence a on both sides
    x = bez(0, a, 1-a, 1); y = bez(0, 0, 1, 1)
    v = np.gradient(y, u) / np.gradient(x, u)
    return v.max()                     # mean speed = 1 (unit value over unit time)
print('1) peak/mean speed: Easy Ease 33.33 -> %.3f | influence 90 -> %.2f | needle 95 -> %.2f  (model: 1/(1-a))' % (ae_speed_ratio(1/3), ae_speed_ratio(.9), ae_speed_ratio(.95)))
def css_slope(x1, y1, x2, y2, end):
    x = bez(0, x1, x2, 1); y = bez(0, y1, y2, 1); s = np.gradient(y, u) / np.gradient(x, u)
    return s[-2] if end else s[1]
print('2) expoIn (.7,0,.84,0) end slope %.3f | expoOut (.16,1,.3,1) start slope %.3f  (equal -> no speed jump at the cut)' % (css_slope(.7,0,.84,0,True), css_slope(.16,1,.3,1,False)))
r1, p, q, D = 9, .18, .18, 1
r2 = r1 * p/(1+p) * (1-q)/q * D
print('3) rho matching: r2 = %.3f, SL2 end influence = min(86, 100(1-1/r2)) = %.1f' % (r2, min(86, 100*(1-1/r2))))
strata_a = 3 * .35/.35 / 1.35; strata_b = 3 * .185/.27 / 1.35
lo_a = 5 * math.log(12/1.04) / .45; lo_b = 5 * .74/.9 / .26
print('4) d(ln s)/dt across cuts: Strata %.3f -> %.3f /s (ratio %.2f) | LO %.2f -> %.2f /s (ratio %.2f); same sign, ratio <= 2 -> reads as one move' % (strata_a, strata_b, strata_a/strata_b, lo_a, lo_b, lo_a/lo_b))
k = np.linspace(0, 1, 100001); sp = 1 - np.exp(-6*k)*np.cos(7.5*k)*(1-k)
print('5) spring(k)=1-e^(-6k)cos(7.5k)(1-k): max %.4f at k=%.3f, value at k=1 = %.4f' % (sp.max(), k[sp.argmax()], sp[-1]))
ss = lambda t: np.where(t <= 0, 0, np.where(t >= 1, 1, t*t*(3-2*t)))
t = np.linspace(-.2, 2.2, 240001)
for start in (1.0, .5, .45):
    P = np.stack([ss(t), ss((t-start))], 1)      # A=(0,0) -> B=(1,0) -> C=(1,1): a 90 degree turn, equal legs, Easy Ease both
    pos = np.stack([P[:, 0], P[:, 1]], 1)
    dist = np.hypot(pos[:, 0]-1, pos[:, 1]).min()
    v = np.hypot(*np.gradient(pos, t, axis=0).T); mid = (t > .2) & (t < start + .8)
    print('6) 90-degree A->B->C, next move starts at %.2f D: closest approach to B = %.1f%% of |AB|, min speed = %.0f%% of peak' % (start, 100*dist, 100*v[mid].min()/v.max()))
N = 4; print('7) 180-degree shutter, N=4 sub-frame offsets (frames):', [round(.5*((kk+.5)/N-.5), 4) for kk in range(N)])
f = lambda d: 1 if d < .5 else min(14, max(5, 3 + 1.6*d))
print('8) adaptive blur samples n(diff) for diff 0.3/1/3/6/10:', [round(f(d), 1) for d in (.3, 1, 3, 6, 10)])
def ae_value(T, a, v0, v1, fps):         # value at each frame of a zero-speed / influence-a AE ease (bisection on x(u))
    out = []
    for fr in range(int(round(T * fps)) + 1):
        x = fr / fps / T; lo, hi = 0.0, 1.0
        for _ in range(60):
            m = (lo + hi) / 2; xm = 3*(1-m)**2*m*a + 3*(1-m)*m*m*(1-a) + m**3
            lo, hi = (m, hi) if xm < x else (lo, m)
        m = (lo + hi) / 2; out.append(v0 + (v1 - v0) * (3*(1-m)*m*m + m**3))
    return out
vals = ae_value(.4, .95, 100, 135, 60)
print('9) needle 95/95, 100 -> 135 in 0.4 s @60: per-frame speed (units/s):', [round((b - a) * 60) for a, b in zip(vals, vals[1:])])
