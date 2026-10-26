# Book lessons → KOSIF Motion (v3.3)

What the owner's reference library (`Desktop/11_مراجع_وكتب_PDF`) teaches that a code-rendered film can use, each turned
into a rule and, where possible, a function. All text is paraphrased; read the books for the full argument.
Scanned books were read with the Windows OCR engine (offline). Unrelated files in that folder (accounting, business
documents, novels, game guides) were not opened.

## 1. James Gurney — *Color and Light* (2010)
| Lesson | Rule for a 3D film | In the kit |
|---|---|---|
| Atmospheric perspective: with distance the **darks are affected first** (lighter, bluer); lit sides lose chroma and warmth; contrast drops until forms match the horizon sky | Fog colour = the horizon sky's colour; extinction per channel (blue scatters most); several depth layers make it visible | `aerialPerspective({ scatter })` — three-channel fog for every built-in material; examples/blue_hour (ridges at 0.7/1.4/2.6/4.5 km of the *same* rock) |
| Reverse atmospheric perspective: looking toward a low sun through moist or dusty air the haze turns warm; rare, so it reads as strange and exciting | Warm the haze only when the camera faces the sun | `fogTowardSun(scene, camera, sunDir, cool, warm)` |
| Reflected light: in shadow, **upfacing planes are cool** (they see the sky), **downfacing planes warm** (they see the lit ground) | Fill = sky colour above + bounce colour below | `skyBounce(scene, { sky, ground })` (a hemisphere light) |
| Night conditions: moonlight reads blue-grey, flame and sodium orange, mercury vapour blue-green; the eye sees less black than a camera | Name the sources; keep shadows readable; complementary blue/orange | `LIGHT_SOURCES`, `lightColor("sodium")`; `makeLookPass({ night })` lifts the darks into rod vision |
| Colour corona: a very bright source (lamp, sun, headlight, glint on water) wears a halo **in its own colour** that lifts the nearby values | Bloom radius generous, threshold below the lamps, never grey bloom | `makePost` bloom radius 0.7 in blue_hour |
| Three rules of specularity: reflective surfaces need the widest value range; convex chrome shows a small view of the whole surroundings; specular is a layer on top of normal modelling | Chrome = a real cube-camera reflection of the scene, not an env gradient | examples/sound_ground orb |
| Gamut masks and limited palettes: choose a wedge of the colour wheel and keep everything inside it; one accent outside | Restrict hues in post, then add one accent | `makeLookPass({ gamut: [centre, width, strength] })`, `harmony()` / `MOTION.palette()` |
| Colour scripting: plan the colour of each sequence like a score | One palette per section; change palette on story beats, not randomly | review lens "colour" |
| Warm and cool: the light and the shadow should differ in temperature | Split toning warm highlights / cool shadows | `makeLookPass({ split })` |

## 2. Joel Grimes — *The Photographer's Guide to Lighting*
- Two setups carry a career: **Rembrandt / cross light** (low-sun or window light from the side, the triangle on the shadow
  cheek) and **top-down / clamshell** (over the camera like an open sky, a bounce below). Then add **edge lights** from
  behind for drama ("edgy three light"), or make every source huge for an **ultra-soft** high-key look.
- Softness is the size of the source **relative to the subject**: a 2 ft source at 2 ft, a 5 ft at 5 ft and a 7 ft at 7 ft
  give the same light on the face; backing a light away also lightens the background (inverse square).
- In code: `lightPreset(scene, "rembrandt" | "clamshell" | "edgy" | "ultrasoft" | "short" | "broad" | "sun")`,
  `softnessDeg(size, distance)` → shadow radius, `falloffStops(d1, d2)`, ratios in stops through `lightRig`.

## 3. *Night Photography: From Snapshots to Great Shots*
- Long exposures turn moving lights into **trails**, water and clouds silky after ~8 s, and stars into arcs; exposure is a
  trade between ISO, aperture and time in stops (reciprocity).
- Star-trail photographers stack frames by keeping each pixel's **brightest** value.
- Tungsten white balance at blue hour makes the sky deep blue while the lamps stay warm.
- In code: `motion.py render --blur 16 --shutter 30 --stack lighten` (a 1 s exposure per frame at 30 fps, lighten stack;
  GPU path in `makeFrameLoop`, CPU path in `film.py`); `--stack average` with a long shutter for silky water and soft
  crowds; montage grades `blue_hour`, `sodium_night`.
- Measured lesson: a light that moves farther than its own size between two sub-samples leaves a **dotted** trail, and a
  stretched light hidden inside a car body shows half-moons — stretch it by `trailLength(speed)` and keep it in front of
  the body (examples/blue_hour).

## 4. *Mastering Google Veo 3* (prompt guide) and the cinematic Midjourney guide
- A prompt that works names **subject · action · setting · style/mood · technical directives** (shot, angle, movement,
  lens, light). The guide's most-used camera words: wide shot, close-up, low angle, tracking shot, medium shot, handheld,
  slow motion, establishing shot, crane shot, high angle, pan, dutch angle, bird's-eye, dolly zoom, rack focus.
- Aspect ratio is part of the look (2.35:1 reads as cinema).
- In code the same words drive a deterministic camera: `shot(kind, o)`, `shotFromWords("low angle tracking shot")`,
  `sequence([{ at, shot }])` with hard cuts, `applyShot(camera, sample, post)`; `dolly_zoom` keeps the subject's frame
  height exactly constant (fov = 2·atan(h / 2d)); `handheld` is seeded three-octave sway, not random jitter.

## 5. *360-Degree Character Sheet* (Arabic PDF)
- Consistency comes from one reference image plus the same subject seen front, left, right and back.
- In 3D this is a camera, not four prompts: `shot("turntable")` holds front → side → back → side; render it as the
  continuity sheet before animating a character.

## 6. Colour-theory cheat sheet (Dan Scott)
- Colour = hue + value + saturation; high-key vs low-key is a value plan; harmonies: complementary, analogous, triadic,
  split-complementary, tetradic.
- In code: `harmony(scheme, hue)` (three-kit) and `MOTION.palette(scheme, hue)` (2D); `motion.py inspect` reports the
  value extremes (blown whites, crushed blacks).

## 7. From the web (October 2026)
- Tone curves in three.js: ACES Filmic is punchy and high-contrast; **AgX** avoids hue shifts in bright highlights (fire,
  neon, sunsets stay their colour) but is less saturated; Khronos **PBR Neutral** keeps albedo faithful for products.
  → `makeRenderer(canvas, W, H, { tone: "aces" | "agx" | "neutral" })`.
- Aerial perspective in engines is per-channel in-scattering + transmittance (Hoffman–Preetham; Hillaire's LUT method);
  monochrome fog is not enough — hence the three-channel fog chunk.
- Night vision (Purkinje shift): rods dominate in the dark, blues and greens read brighter, reds sink, colour drains —
  darktable's low-light module blends a scotopic lightness with a blue tint in the darks; the look pass does the same.
- Dolly zoom: keep the subject's frustum height constant while dollying — the formula above.

Sources: three.js forum on AgX and the Bevy tonemapping docs; Hoffman & Preetham and Hillaire on aerial perspective;
darktable's low-light vision docs and PremiumBeat on moonlight grading; Wikipedia and Unity docs on the dolly zoom.
