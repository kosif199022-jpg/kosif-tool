# Overlapping camera, speed graphs and hook captions — الكاميرا المتداخلة وجرافات السرعة وكابشن الهوك

Technique credit: **Fares Toson** (the "Fares Motion" After Effects panel and its `pro-motion` skill, shared as a gift from a YouTube episode). The method and the measured numbers are restated here in KOSIF's own words; no code, images or projects from that package are in this repo. Code: `starters/remotion/src/easing.ts` (`aeEase`, `GRAPHS`, `overlapRig`, `peakFrame`, `project`) and `tools/overlap_rig.py` (same math in Python plus a checker).

**بالعربية:** الطريقة من فارس توسون (بانل Fares Motion وسكيل pro-motion). الفكرة والأرقام المتقاسة مكتوبة هنا بكلامنا، ومفيش كود أو صور أو بروجكتات منسوخة. الكود الجديد في `easing.ts` و `tools/overlap_rig.py`.

## 1. When to use — إمتى تستخدمه

Any 3D-feeling reel, explainer or vertical video where the camera travels between sections, and any "merge these designs into one video" brief. Pair it with `playbooks/3d.md` (scene building) and `playbooks/kinetic-type.md` (captions).

**بالعربية:** أي ريل أو فيديو طولي فيه كاميرا بتعدّي بين أقسام، وأي طلب "ادمج التصميمات دي في فيديو واحد".

## 2. The overlapping camera rig — ريج الكاميرا المتداخلة

1. **The camera never animates.** It is a one-node camera (AE zoom 1866.7 px at 1080×1920, about 32° horizontal) parented to a chain of 3D nulls. Every camera move is one null with **two keys on one axis**.
2. **Camera position = base + sum of null offsets.** In code: `overlapRig(base, nulls)(frame)`.
3. **Overlap rule.** Start the next null while the previous one is in its slow tail, after it has covered **83–95%** of its distance (13–20 frames of overlap at 30 fps). The combined speed then never reaches zero: in the reference rig the slowest handoff is about 7–11 px/frame and the peaks 105–133 px/frame.
4. **Open and close at full speed.** The first null uses *sharp start (hard)* from frame 0; the last uses *sharp end (hard)* with its last key on the comp's last frame. Moves between sections use *sharp middle*.
5. **Elements in each section** animate directly on their own layers (no nulls), two keys, *sharp start (hard)*: rise 90–235 px with Z rotation returning to 0 (for example +13° → 0°) over 30–58 frames, highlights drawn with Trim Paths End 0 → 100% in 30 frames. **Start them on the peak-speed frame of the camera move entering that section** (`peakFrame(null)`), so camera and elements settle together.
6. **Projection** for code renders: `scale = zoom / (z − camZ)` (`project()`).

Reference rig (4 s, 30 fps, X axis only):

| Null | Move (px) | Frames | Out / In | Graph |
|---|---|---|---|---|
| 1 | −544 | 0 → 40 | 0.01% / 100% | sharp start (hard) |
| 2 | −1290 | 20 → 73 | 74.7% / 79.3% | sharp middle |
| 3 | −1470 | 60 → 109 | 72.7% / 82.2% | sharp middle |
| 4 | −447 | 89 → 119 | 100% / 0.01% | sharp end (hard) |

Check any rig before rendering: `python3 tools/overlap_rig.py check rig.json` (no file = the reference rig). It fails when a move ends before the next begins, when a handoff falls outside the slow tail, or when the camera stalls.

**بالعربية:** الكاميرا نفسها ما بتتحركش. كل حركة نل لوحده بكيين على محور واحد، والنل اللي بعده يبدأ والقبله قطع 83–95% من مسافته. أول حركة "حاد في الأول (قوي)" وآخر حركة "حاد في الآخر (قوي)" على آخر فريم، واللي في النص "حاد في النص". عناصر كل قسم تبدأ مع فريم أقصى سرعة للكاميرا الداخلة عليه.

**Avoid — تجنّب:** moving the camera layer itself; two moves on one null; a move that finishes before the next starts (a visible stop).

## 3. The five speed graphs — الجرافات الخمسة

All five cover the same distance in the same time; only the position of the peak speed changes. The key next to the peak gets a small influence, the other a large one (long tail). Speed is 0 at both keys. Conversion: `cubic-bezier(Out, 0, 1 − In, 1)`; in code `aeEase(out, in)` or `GRAPHS.<name>`; list them with `python3 tools/overlap_rig.py graphs`.

| Name (code) | Out | In | Peak | Feel |
|---|---|---|---|---|
| sharp end — `sharpEnd` | 100% | 35% | ~78% of time, ~4× average | charges up, lands with force |
| sharp middle — `sharpMid` | 70% | 75% | middle, ~3.7× | soft ends, a whip |
| sharp start (hard) — `sharpStartHard` | ~0.01–1% | 100% | frame 0, ~10× | hit, then a long glide |
| sharp start (soft) — `sharpStartSoft` | 32% | 100% | ~19%, ~4× | fast start without the hit |
| sharp end (hard) — `sharpEndHard` | 100% | ~0.01–1% | last frames, ~12× | slow, then slams in |

In After Effects type the numbers into Keyframe Velocity (Ctrl+Shift+K) with speed 0. Do not read influence off the length of the yellow handle in the speed graph: it looks about half the real value.

## 4. Merging scenes — الدمج بين المشاهد

Join scenes **only with camera moves and overlap**: no morphing one shape into another, no circle wipe, no reveal. Lay every scene side by side in one 3D world (X/Y, or one behind another on Z), pin each background as a plane in its scene's slot, rebuild each design as real layers (text, cards, shapes; cut complex pieces from the source and key out their background), and let the null chain carry the camera from scene to scene.

**بالعربية:** الدمج بالكاميرا والأوفرلابنج بس. ممنوع المورف والـ Circle Wipe والريفيل. كل مشهد في مكانه في عالم 3D واحد، وخلفيته Plane ثابت، والكاميرا هي اللي بتعدّي.

## 5. Hook captions (word by word) — كابشن الهوك كلمة كلمة

- One layer per word. Each word **cuts in already blurred** and slides 127 px with blur 37.5 → 0 over 20 frames, *sharp start (hard)* (0.1% / 100%). No fades in, and a whole block **cuts out together**.
- Do the slide and blur with an effect stack (Transform with the comp shutter angle, then Gaussian Blur), not the layer's Position, so Position/Scale stay free for layout. The offset and blur live in layer space, so they grow with layer scale.
- Block 1 (big lines) slides right; block 2 (small line + key word) rises.
- Visual hierarchy: white regular words scaled ~2×, one word stretched with kashida (ـــ) for emphasis, then the **key word** bold in light green `#C7FFAB` with a soft glow. A key word may type on in 10 frames, or reveal in steps with the speech using masked copies (ال ← المنف ← المنفذين).
- Place lines at chest height, 55–60% of the frame height (y ≈ 1090 at 1920). Font in the source: IBM Plex Sans Arabic (Regular / Medium / Bold).
- In Remotion: drive `translateX/Y` and `filter: blur()` from `progress(frame, start, 20, GRAPHS.sharpStartHard)`; with `words.json` set each `start` to the word's spoken frame (`playbooks/audio-sync.md`).

## 6. Talking-head + 3D graphics rhythm — إيقاع التوك هيد مع الجرافيك

Observed in three of the creator's reels; use as a starting rhythm, not a rule:

- Talking head in a dark room with green or violet neon; a 3–5 s 3D graphics insert every 6–10 s, graphics ≈ 40–50% of the runtime, average shot 2.6–3.2 s.
- Written hook from the first second; CTA at the end.
- Graphics on light grounds (cream `#FAF8EC` or `#F4F4F4`, sometimes pastel holographic gradients): tilted real UI cards with soft shadow and depth of field, a clicking cursor, typed text. The dark-room vs light-graphics contrast is part of the look.
- Transitions 6–10 frames with strong motion blur; no slow transitions or long fades.

## 7. Verify — التحقق

- `python3 tools/overlap_rig.py check <rig.json>` prints OK.
- Scrub the preview frame by frame across each handoff: the background never freezes.
- Element entrances in each section start within ±2 frames of that section's camera peak.
