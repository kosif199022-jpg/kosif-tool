# مهارات خارجية أرسلها المالك / Owner-supplied skills (motion)

> **What this gives you:** the craft numbers, QA tools and working methods from the motion skills and packages the owner sent (two Higgsfield motion skills, an editorial-edit skill, an Arabic song film, KOSIF SEE media-motion and Suno core, a 500-methods web tool) plus the ECC motion skills, rewritten in our own words, with a log of what was actually run here.
> **Open it when:** you plan a launch/UI film, a cut that must feel continuous, a song or lyric film, an edit of real footage, an imitation of a reference video, or you need frame-level QA. Each idea has a power ID (`python3 scripts/powers.py show EASE-X01`); badges follow the usual ladder.

ملخص بكلماتنا لملفين `.skill` أرسلهما المالك (higgsfield-motion-saas و higgsfield-motion-claude). الملفات نفسها لم تُنسخ إلى المستودع؛ لاستخدامها كاملة ثبّتها كمهارات منفصلة.

## الفهرس / contents
1. higgsfield-motion-saas — حركة إطلاق التطبيقات (summary)
2. higgsfield-motion-claude — إطارات وأفلام بأي هوية (summary)
3. نموذج شكل السرعة — Speed-shape model
4. مفردات الانتقال بأرقامها — Transition vocabulary with numbers
5. محرك الكود وخط الرندر — Code engine and render pipeline
6. أدوات فحص مقيسة — Measured QA tools
7. دروس الإنتاج — Production lessons
8. طريقة المونتاج التحريري — The editorial-edit method
9. خط فيلم الأغنية — The song-film pipeline
10. أدوات منقولة إلى بايثون — Ported tools (code)
11. حكم «500 طريقة» — The 500-methods verdict
12. نواة كتابة الأغاني لـSuno — Suno songwriting core
13. توجيه محاكاة الفيديو — Video-imitation routing
14. مهارات ECC للحركة — ECC motion skills
15. سجل التحقق — Verification log (2026-10-16)
16. المصادر والرخص — Sources and licences

## higgsfield-motion-saas — حركة إطلاق التطبيقات
- **القانون الأساسي:** عند أي حدث لا تكون السرعة صفرًا، وعند القطع تكون في أقصاها. القطع يختبئ في أسرع لحظة: «إبرة» زوم متماثلة، أو «قمة» تحوّل غير متماثلة، أو تسارع يُسلَّم لخاصية أخرى بعد القطع.
- **الاتجاه يعبر القطع:** إن طارت الكاميرا داخل شيء، تبدأ اللقطة التالية أبعد (scale < 1) وتتباطأ للداخل. افحص إشارة d(ln scale)/dt على جانبي كل قطع.
- **التداخل:** ابدأ الحركة التالية عند ≈0.45 من الحالية على «null» أب، لتُجمع السرعات بدل أن تصطف.
- لا شيء مهم يظهر أو يختفي بالشفافية وحدها: يُحمل أو ينمو أو يُدفع أو يُمسح أو يتحوّل.
- منحنيات قوية (in(3)/out(3)) للانتقالات فقط؛ داخل المشهد دخول 0.45–0.7 ث وتجاوز ≤2٪.
- مكتبة انتقالات: needle zoom، fly-through (×6–12 ثم يبدأ التالي من ×0.26–0.4)، UI morph بالحجم ±18٪، mockup hand-off، object carry، grow-from-point، smear، خلفية متدفقة.
- خط الإنتاج: مفهوم ← لوحة قصة بتقدير وقت ← محرك `__seek(t)` ← ضبابية حركة من إطارات فرعية (12–16) ← مرور عدسة ← صوت مولّد ← فحص الإطارات حول كل قطع.

## higgsfield-motion-claude — إطارات وأفلام بأي هوية
- نظام رموز HFT: 12 نمطًا (swiss-editorial, luxury-serif, playful-pop, cinematic-noir, soft-pastel-ui, tech-terminal, brutalist-raw, organic-editorial, y2k-chrome-modern, kinetic-type, dot-matrix, higgsfield)، و11 نوعًا (productDemo, explainer, brandFilm, kineticType, logoIdent, dataStory, editorialTitles, characterMotion, spatial3d, broadcastPackage, musicVisual)، و`derive()` لهوية جديدة من لون بذرة ومزاج (calm, luxury, energetic, playful, technical, editorial).
- **أسلوب العمل مع المالك:** شيء مرئي خلال 10–15 دقيقة؛ السيناريو أولًا قبل البناء؛ معايرة بـ~5 إطارات قبل التوسع؛ «ستوب» يوقف كل شيء فورًا؛ جولة مراجعة واحدة بين جولات العميل.
- كثافة حسب النوع: إطلاق مقيد؛ عرض منتج = تطبيق واحد مستمر تسافر فيه الكاميرا؛ مونتاج توليدات = ~40–50 قطعًا في 30 ث ولا صورة تبقى >1 ث.
- فحوص: حجم النص الفعلي وتباين WCAG/APCA في أسوأ بكسل، قفزات الفرق بين الإطارات، الهواء الميت، المدة والإطارات بعد الترميز.

## 3. نموذج شكل السرعة — Speed-shape model
The SaaS skill's core idea is to think in **speed shapes**, not keyframes. Write every move as r = speed ÷ mean speed so a recipe works at any size and frame rate. An After Effects temporal ease is a cubic Bézier in (time, value); with zero key speeds and influence a on both keys the peak is 1/(1−a). That single formula explains why Easy Ease (33.33, peak 1.5×) feels dead on an event (speed 0 at the key) and why a 95/95 "needle" (peak 20×) hides a cut. Four shapes cover most needs: Easy Ease (settles), needle (peak on the cut), cusp (a UI-morph joint that keeps moving through a pose), relay (the next move starts ≈0.45 into the current one so the sum never stops). Across a cut between differently sized layers match *relative* speed rho = (dH/dt)/H; across a zoom cut match the log velocity d(ln s)/dt (same sign, ratio within ~2×). Curves with equal end slopes (expoIn/expoOut, both 6.25) keep speed continuous through a mirrored whip. Read speeds as per-frame number lists: a zero mid-move is a pause, a peak one frame off means move the keys. → EASE-X01…X06, QA-X04.

## 4. مفردات الانتقال بأرقامها — Transition vocabulary with numbers
Six client films gave measured recipes. The rule above all: every transition needs a nameable cause (click, key press, object at the lens, colour flooding from a button), and nothing important appears or disappears by opacity alone. Hard cuts with the speed peak on the cut feel energetic; object transitions without a cut feel premium; cut on the beat grid and shorten shots toward the climax.
- Persistent object + needle: the object zooms ×1 → 1.12 across ±0.2 s while backgrounds hard-cut 3×/s beneath it; move the pivot first; parallax scale^0.6 behind, ^1.35 in front (TRANS-X02).
- Fly-through: the next shot starts *smaller* and decelerates in; starting large and shrinking was rejected (TRANS-X03).
- Carry, grow-from-point, size-not-scale UI morphs, mockup hand-off with polarity flip (TRANS-X04, X06, UI-X02).
- Smear and layered whip with per-layer travel factors (dots 0.5 … cursors 1.2), swing pairs, mirrored whips (TRANS-X05).
- Background changes: colour flood from the action point, column pour, exposure ramp, plate cuts, infinite band with +360 px overscan (TRANS-X07, X08).
- Iris into a wordmark, band glitch on 3–4 cuts only, geometric morph through intermediate shapes, one continuous shot from shared elements (TRANS-X09, X10, SHAPE-X01, X02).
- Camera only inside scenes and neutral in transition windows; motivated moves; single-camera brand film rules (CAM-X01…X03).
- The failures already paid for are listed in TRANS-X12.

## 5. محرك الكود وخط الرندر — Code engine and render pipeline
The SaaS skill builds films as browser pages with a pure `seek(t)` engine, captures frames, blends sub-frames, runs a photographic lens pass, synthesizes sound from the cut list and encodes. Transferable pieces:
- **Lens pass** (owner's `lens.py`, numpy + Pillow): barrel, radial fringes, three-scale highlight bloom, vignette, mid-tone grain seeded per frame. Ran here (V7) → GLOW-X01.
- **Adaptive motion blur**: 180° shutter centred on the frame; sample count from the measured luma change, clamp(3 + 1.6·diff, 5, 14); never straddle a hard cut → ENG-X01.
- **Interleaved workers + continuity gate**: round-robin frames per worker (3:09 vs 5:18 contiguous) and refuse to encode with gaps → ENG-X02.
- **Sound kit** (owner's `sound_kit.py`, numpy only): the cuts are the rhythm; risers end on cuts; UI sounds on contact frames; onset check ±5 ms. Ran here (V6) → BEAT-X05.
- **Alive characters** (SDF pets): motion signatures per personality, idle ×2 → CHAR-X01. **Inside the system** glyph kit → PART-X01. LED lattice bulge → RETRO-X01.
- **Bugs already paid for** (fonts.ready, DevTools ports, negative clip insets, ProcessPool guard…) → ENG-X03.
- Host-specific parts (macOS Swift encoders, AppleScript/After Effects automation) are not carried over; ffmpeg does the same here.

## 6. أدوات فحص مقيسة — Measured QA tools
The second Higgsfield skill's strongest leftover is measurement instead of opinion:
- **fdiff** scans the *encoded* file: OUTLIER, JUMP, FREEZE, DEAD AIR and TIMING (a one-frame 8 ms glitch once produced 24.023 fps). Whole-frame luma said "clean" while 18 local defects existed, hence the 12×12 block maximum. Python port in §10, ran here (V2) → QA-X01.
- **activity** measures dead air with the block maximum (8/255 for ≥ 0.2 s; strict pass 20/0.4 s) and reads stills against a list of allowed reads → QA-X02, EASE-X08.
- **textcheck** computes effective text size through every transform and the worst-pixel contrast by rendering twice (with and without text). Pillow port in §10, ran here (V3) → QA-X03.
- **music_window / cut_audio** pick the best music window, snap scenario times to hits, verify hits on the final mix and cut the music cleanly. Ran here (V4, V5) → BEAT-X01…X04.

## 7. دروس الإنتاج — Production lessons
From an 89 KB production diary, the rules worth keeping:
- **Working rhythm:** a visible result in 10–15 min; scenario first (shot table on the beat grid + trigger map + ≤ 2 questions); calibrate ~5 key frames before building in parallel; number versions, never overwrite; never ship silent or without frame-level QA; ≤ 1 review round between client rounds; "stop" halts everything including credit spend → STORY-X01, STORY-X03.
- **Status answers** give clock time, what changed, the stage, an image, a clock-time ETA and an offer to stop. **Estimates** were 3–4× too high; real numbers in STORY-X04.
- **Client taste** turned into rules (STORY-X02); the critic must read the client's own words (QA-X05).
- **Micro-choreography** of the main hit and **cursor as protagonist** → EASE-X11, UI-X01. Named-intent eases → EASE-X06.
- **Orchestration** for parallel builds (disjoint files, frozen kit signatures, digests not whole documents, never message a sub-agent inside a running workflow) → MISC-X02.
- **Generated footage** on the Higgsfield connector: production parameters and a performance-first prompt skeleton (🔑, spend only with approval) → GEN-X01.

## 8. طريقة المونتاج التحريري — The editorial-edit method
An owner-supplied "editorial film edit" skill (origin and licence not stated; reference only) is mostly an **edit discipline** for real footage: the source governs duration, order, speech, pauses, aspect and sound; build a transcript and a source-to-programme time map; never show stray frames of an adjacent take; keep absolute word timing when moving a boundary; run a capability preflight before promising an MP4; test short pieces before an expensive export; deliver the editable project and a music-free version; contact sheets and numbers do not replace watching and listening → FOOT-X01, FOOT-X02. Its browser engine adds a one-overshoot spring and arriving-key tracks (EASE-X09), per-layer posterize (EASE-X10), type that keeps moving through cuts and a three-family font source of truth (TYPE-X01, X02), caption chunks locked to one position (SYNC-X02), and a WebGL archival chain with a careful **film-grain post-mortem**: grain that looked like a sliding sticker because one noise field was translated each frame, lived in screen coordinates while the picture weaved, and repeated every 997 frames (TEX-X01, X02).

## 9. خط فيلم الأغنية — The song-film pipeline
The owner's Arabic lyric film (1080×1920, 30 fps, 56.92 s, 8 scenes) shows that a whole song film can be **one deterministic canvas file plus three small Python tools**: `analyze.py` writes per-frame band envelopes, kicks, tempo and estimated word times with an honest `timing_quality` note (SYNC-X01); `render.py` seeks each frame in Playwright, pipes JPEGs into ffmpeg and muxes the song untouched (ENG-X04); `sheet.py` makes contact sheets. Signature devices: the focal-point infinite zoom (TRANS-X11), the RTL whole-word reveal with a key-word pop (ARAB-X01), a quill that follows the ink frontier (DRAW-X01), Rubin-vase profiles, a constellation face and a portrait made of the lyric's words (STORY-X05). The song is a commercial third-party track: it is not in this repo, and any proof re-render must use an original or licensed track.

## 10. أدوات منقولة إلى بايثون — Ported tools (code)
Two of the owner's measuring tools run on macOS Swift or a Chrome DevTools bridge. These ports reproduce their method with numpy, Pillow and ffmpeg (all usually present). Both ran here (V2, V3). Copy a block into a `.py` file to use it.

**frame_qa.py** — OUTLIER · JUMP · FREEZE · DEAD AIR · TIMING on an encoded file (QA-X01, QA-X02):
```python
"""frame_qa.py - frame-level QA of an encoded video (numpy + ffmpeg/ffprobe).
usage: python3 frame_qa.py film.mp4 [--fps 30]   (exit 1 when anything is found)"""
import json, subprocess, sys
import numpy as np

def frames(path, w=384):
    p = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height,r_frame_rate', '-of', 'json', path], capture_output=True, text=True, check=True).stdout)['streams'][0]
    h = int(round(p['height'] * w / p['width'] / 2)) * 2
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={w}:{h}:flags=area,format=gray',
        '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    num, den = map(int, p['r_frame_rate'].split('/'))
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32), num / den

def runs(mask):
    out, s = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and s is None: s = i
        if not m and s is not None: out.append((s, i - 1)); s = None
    return out

def scan(path, fps=None, B=12):
    f, rate = frames(path); fps = fps or rate; n = len(f)
    diff = np.abs(np.diff(f, axis=0))                                  # diff[i-1] = |f[i] - f[i-1]|
    mad = np.r_[0, diff.mean((1, 2))]
    hh, ww = (f.shape[1] // B) * B, (f.shape[2] // B) * B
    blk = diff[:, :hh, :ww].reshape(n - 1, hh // B, B, ww // B, B).mean((2, 4)).max((1, 2))
    blockmax = np.r_[255, blk]
    out = []
    for i in range(1, n - 1):                                          # OUTLIER: one odd frame between two similar ones
        dac = np.abs(f[i + 1] - f[i - 1]).mean(); m = min(mad[i], mad[i + 1])
        if m > 3 and m >= 2 * dac: out.append(('OUTLIER', i, f'dAB {mad[i]:.1f} dBC {mad[i+1]:.1f} dAC {dac:.1f}'))
    for i in range(1, n):                                              # JUMP: change >= 3x the local median (+-6 frames)
        loc = np.r_[mad[max(1, i - 6):i], mad[i + 1:i + 7]]
        if len(loc) and mad[i] > 3 and mad[i] >= 3 * max(np.median(loc), 0.05) and not any(o[1] in (i, i - 1) for o in out if o[0] == 'OUTLIER'):
            out.append(('JUMP', i, f'mad {mad[i]:.1f} vs median {np.median(loc):.2f}'))
    for s, e in runs(mad[1:] < 0.15):                                  # FREEZE: >= 6 still frames with motion on both sides
        s, e = s + 1, e + 1
        if e - s + 1 >= 6 and s > 1 and e < n - 1: out.append(('FREEZE', s, f'{e - s + 1} frames ({s}-{e})'))
    for s, e in runs(blockmax < 8):                                    # DEAD AIR: no 12x12 block changes by >= 8/255 for >= 0.2 s
        if (e - s + 1) / fps >= 0.2: out.append(('DEAD AIR', s, f'{(e - s + 1) / fps:.2f} s ({s}-{e})'))
    pts = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'packet=pts_time',
        '-of', 'json', path], capture_output=True, text=True, check=True).stdout)['packets']
    t = np.sort([float(p['pts_time']) for p in pts])
    for i, d in enumerate(np.diff(t)):                                 # TIMING: frame duration off nominal by > 1 ms
        if abs(d - 1 / fps) > 0.001: out.append(('TIMING', i + 1, f'{d * 1000:.1f} ms'))
    return sorted(out, key=lambda o: o[1]), mad, blockmax, fps

if __name__ == '__main__':
    path = sys.argv[1]; fps = float(sys.argv[sys.argv.index('--fps') + 1]) if '--fps' in sys.argv else None
    found, mad, bm, fps = scan(path, fps)
    for kind, i, note in found: print(f'{kind:9s} frame {i:4d}  t={i / fps:6.3f}s  {note}')
    print(f'{len(mad)} frames @ {fps:g} fps; findings: {len(found)}')
    sys.exit(1 if found else 0)
```
Port choices: JUMP also needs mad > 3 (a noise floor) and skips frames already flagged as OUTLIER; for a stricter dead-air pass change `8` to `20` and `0.2` to `0.4`.

**textcheck (Pillow)** — effective size and worst-pixel contrast by double render (QA-X03). `bg` is the frame without text, `draw_text(draw)` draws the text, `scales` lists every ancestor scale including the camera:
```python
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def lin(c):
    c = np.asarray(c, np.float64) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def wcag_L(rgb): r, g, b = np.moveaxis(lin(rgb), -1, 0); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def apca_Y(rgb):
    r, g, b = np.moveaxis((np.asarray(rgb, np.float64) / 255) ** 2.4, -1, 0)
    return 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
def apca_lc(txt, bg):                                   # APCA 0.0.98G constants; returns |Lc|
    clamp = lambda y: np.where(y > 0.022, y, y + np.clip(0.022 - y, 0, None) ** 1.414)
    t, b = clamp(apca_Y(txt)), clamp(apca_Y(bg))
    normal = (b ** 0.56 - t ** 0.57) * 1.14; rev = (b ** 0.65 - t ** 0.62) * 1.14
    lc = np.where(b > t, np.where(normal < 0.1, 0, normal - 0.027), np.where(rev > -0.1, 0, rev + 0.027))
    return np.abs(lc) * 100

def check(bg, draw_text, text_rgb, font_px, scales=(1.0,), caps=False, role='read'):
    with_t = bg.copy(); draw_text(ImageDraw.Draw(with_t))
    diff = np.abs(np.asarray(with_t, np.int16) - np.asarray(bg, np.int16)).max(2) > 0
    mask = np.asarray(Image.fromarray((diff * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0  # dilate 2 px
    under = np.asarray(bg)[mask]
    Lt, Lb = wcag_L(text_rgb), wcag_L(under)
    ratio = (np.maximum(Lt, Lb) + 0.05) / (np.minimum(Lt, Lb) + 0.05)
    lc = apca_lc(np.broadcast_to(text_rgb, under.shape), under)
    eff = font_px * float(np.prod(scales))                                   # every ancestor scale counts
    need = {'read': 48 if caps else 64, 'label': 28}.get(role, 20)
    ok = eff >= need and ratio.min() >= 4.5 and lc.min() >= 60
    return dict(effective_px=round(eff, 1), need_px=need, worst_wcag=round(float(ratio.min()), 2),
                worst_apca=round(float(lc.min()), 1), verdict='PASS' if ok else 'FAIL')
```
For DOM films, take `bg` and the text frame from two browser screenshots of the same `seek(t)` (the second with text set transparent). Text that is only seen through glass or blur should be listed, not judged.

## 11. حكم «500 طريقة» — The 500-methods verdict
The owner's web tool advertises 500 methods; counting its JSON shows 150 text decorations (30 base styles × 5 variants), 120 CSS cards (10 recipes × 12 colour themes), 115 text tools (23 transforms × 5 output wrappers) and 115 prompts (5 frameworks × 23 personas), all with the same demo output. It is combinatorial padding, so it was **not** imported as 500 powers. What survives: the 10 CSS surface recipes as a card palette, the reminder that text encoders are one-liners, the 5 prompt frameworks, and a warning that ornament/kashida "decoration" breaks Arabic shaping in rendered video (MISC-X01, ARAB-X03). The tool's single-page web export embeds a third-party web config key: never republish that file.

## 12. نواة كتابة الأغاني لـSuno — Suno songwriting core
KOSIF SEE's media-motion pack carries a full songwriting method (the catalog already had Suno prompt powers BEAT-166…178). New here: compress the brief and ask only high-impact gaps; write **hook first** (title phrase, chorus promise, hook device, bridge turn); write for breath; keep one dialect register with Gulf, Hijazi and Egyptian consistency gates and no typographic elongation; order the Style field (genre → tempo → vocal → instruments → texture → atmosphere → lift); keep Exclude for true negatives; fix surgically (weak line → lyric edit, weak chorus → Replace Section…); hand back four separate copy blocks and check an 11-point rubric → BEAT-X06…X10. The pack says its platform facts were checked against the official docs on 2026-10-07; model tiers, slider names and length limits drift, so re-check them live. Writing the package is not generating the song; generation needs the user's account.

## 13. توجيه محاكاة الفيديو — Video-imitation routing
When the user sends a reference video and asks for "the same edit", follow an 8-step contract: inspect (originals read-only, deterministic samples) → analyse (separate cuts from camera motion, measure transition ranges, keep uncertainty) → Arabic overlay (geometry, spans, font *candidates*, proper shaping) → audio (original when authorised) → assets (licensed only; Pinterest as mood) → render only with an available executor, otherwise return the plan marked EXECUTOR_NOT_EXPOSED → QA gates (a failed gate blocks any "exact match" claim) → deliver MP4 + editable shot plan + storyboard + font-candidate report + discrepancy summary → FOOT-X05, ARAB-X02. Negative routes: a still image, Suno lyrics, motion from audio without a reference, or only downloading a link. Underneath sits a ladder worth applying everywhere: method packaged ≠ tool exposed ≠ authorised ≠ executed ≠ verified (QA-X07). The original routing points to a plugin of another host; only the method is kept.

## 14. مهارات ECC للحركة — ECC motion skills
From the ECC skill collection (MIT, https://github.com/affaan-m/ECC), the motion-relevant methods in our words:
- motion-foundations + make-interfaces-feel-better → motion tokens, five spring presets, transform/opacity only, reduced motion, press 0.96, exits shorter than entrances (UI-X04).
- ui-demo → Playwright recordings of real web apps; ran here, and found that headless recordings draw no pointer (UI-X03, UI-X01).
- manim-video → thesis sentence, 3–6 scenes, `manim -ql` smoke render first (EXPL-X01).
- remotion-video-creation → a 29-rule checklist (ENG-X05). video-editing → tool layers and state hygiene (FOOT-X04).
- taste-distillation / taste-application → grade by measurement in CIELAB zones with median/MAD and background share; one continuous generation then cut; re-encode for frame-accurate cuts (COLOR-X01, GEN-X02, FOOT-X03).
- frontend-slides → show three previews instead of asking questions (STORY-X06).

## 15. سجل التحقق — Verification log (2026-10-16)
All runs used copies in a session scratch folder, `python3 -I`, and original synthetic inputs (no third-party media). Environment facts change per machine; re-run before relying on them.

| # | What ran | Result |
|---|---|---|
| V1 | own numeric script (numpy): AE Bézier speeds, needle frame list, curve slopes, rho match, log-velocity examples, spring, relay geometry, shutter offsets | peaks 1.500 / 10.00 / 20.00 = 1/(1−a); needle 100→135 in 0.4 s @60 → … 161 581 581 161 …; expoIn end and expoOut start slopes 6.250 / 6.250; r2 6.254, influence 84; Strata 2.222 → 1.523 /s, LO 27.17 → 15.81 /s; spring max 1.0736 at k 0.315, 1.0000 at k 1; 90° relay: sequential 0 %/0 %, start 0.5 → 22.1 %/60 %, start 0.45 → 26.2 %/57 %; N = 4 shutter offsets ±0.0625/±0.1875 frame |
| V2 | `frame_qa.py` (§10) on a 4 s 640×360 clip with a planted flash, jump and freeze; a second clip with one frame 8 ms late | OUTLIER @30 (dAB 221.5, dAC 0.9), JUMP @50 (7.1 vs median 0.45), FREEZE 70–81 (12 frames), DEAD AIR 0.40 s; TIMING: one 42.0 ms frame |
| V3 | textcheck (§10) with Tajawal Bold 72 px over a dark→light gradient | dark third PASS (worst 7.46:1, Lc 90.8); across the gradient FAIL (mean 6.66:1 but worst 2.71:1, Lc 57.8); inside a 0.6× push-out FAIL (43.2 px effective); sanity black/white 21.0:1, Lc 106.0 |
| V4 | owner's `music_window.py` on an original 90 s 120 BPM synthetic track | tempo 119.7 BPM; with a 1.2 s breath: DROP +13.5 dB at 48.10 s, window 46.9–76.9 s; with an 8 s breakdown: only a LIFT at 46.12 s; `--snap` moved 4/9/17/24 s by +0.10…+0.15 s; `--hits` five true hits +6 ms, a wrong hit flagged EARLY −244 ms; `--sections` −39.5 / −42.5 / −33.0 dB |
| V5 | owner's `cut_audio.py` | WAV 30.000 s, 48 kHz, 2 ch, 12 ms fade-in, shaped fade-out to 0; `.m4a` refused without afconvert (use ffmpeg AAC) |
| V6 | owner's `sound_kit.py` (6 s score) | 4/4 onsets +0 ms; −13.4 LUFS, −1.0 dBFS; 0.6 s |
| V7 | owner's `lens.py` on 960×540 frames | corner 65.3 → 47.8, halo +6.1, grain std 0 → 4.1 re-seeded per frame, ±1 px R/B fringe; 1.2 s for 3 frames |
| V8 | ffmpeg trims of a 10 s 30 fps clip (GOP 60) for 1.3–3.3 s | output-seek copy 41 frames from frame 60; input-seek copy 62 frames / 2.167 s; re-encode 60 frames from frame 39 |
| V9 | Node Playwright `recordVideo` of a one-button page, then `frame_qa.py` | VP8 1280×720 25 fps 2.2 s; dead air 1.28 s at the start because no pointer is drawn |
| D1 | session distillation `motion-leftovers` §3.2 | the editorial engine's spring and track sampler ran in node (max 1.0736; sample → 9.6875) |
| D2 | session distillation `motion-leftovers` §4.1 | the song film's `analyze.py` re-ran on a copy: 56.92 s, bpm ~69.2, 25 kicks |
| D3 | session distillation `motion-leftovers` §5 | the 500-methods JSON counted: 150 / 120 / 115 / 115 by category |

Not run: the owner's Swift tools (macOS only), `activity.mjs` and `textcheck.mjs` (need the owner's DevTools bridge; ported instead), the song film's renderer (it needs the commercial song), the ECC skills' own scripts, Suno and Higgsfield generation (account and spend).

## 16. المصادر والرخص — Sources and licences
- **Owner packages** (higgsfield-motion-saas, higgsfield-motion-claude, film_project, KOSIF SEE, kosif-tool-ultra): owner material without a LICENSE file. Summarised and paraphrased here, not vendored; `owner-upload:` paths in power records point into those archives. The Higgsfield skills were written for a client; brand colours, client names and quotes were left out.
- **Editorial film edit skill**: origin and licence not stated; used as a reference only. It cites third-party reels as style references; do not copy their media.
- **film_project song**: a commercial third-party track and its lyrics; neither is in this repo.
- **ECC** (https://github.com/affaan-m/ECC): MIT, © 2026 Affaan Mustafa; ideas rewritten in our words.
- Tools named: Playwright (Apache-2.0), Manim Community (MIT), motion (MIT), Remotion (its own licence; some companies need a paid licence).
