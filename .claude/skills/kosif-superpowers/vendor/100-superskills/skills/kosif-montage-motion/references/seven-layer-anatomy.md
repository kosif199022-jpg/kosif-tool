# The 7-layer prompt anatomy ("Dragon Anatomy")

Every generation prompt carries seven layers. Write each as a concrete, physical description.

| # | Layer | Must say | Typical specifics |
|---|-------|----------|-------------------|
| 1 | **Location** | indoor/outdoor, place, time of day, weather | HDRI-style environment, era, geography, depth layers (foreground / mid / background) |
| 2 | **Subject** | who/what, pose, expression, action | exact physical description, contrapposto/weight shift, emotion in the eyes, hands doing something specific |
| 3 | **Wardrobe** | garments, materials, condition | fabric (velvet, linen, leather, oak), colour, wear/dirt, accessories, fit to character |
| 4 | **Lighting** | key / fill / rim, direction, quality, Kelvin | e.g. "soft window key from camera left, warm 3800K, fill −2 stops, cool rim from behind" |
| 5 | **Camera** | body, lens, aperture, angle, shot size, motion | "ARRI Alexa Mini LF, 50mm f/1.4, eye level, medium close-up, slow push-in" |
| 6 | **Atmosphere** | air, particles, mood | haze, dust motes, rain, snow, volumetric rays, humidity, colour mood |
| 7 | **Technical** | resolution, frame rate, aspect, parameters | 8K / 24 fps / 16:9; platform parameters (`--ar`, style/stylize flags — verify per version) |

## Golden formula (single line)
`[STYLE], [COMPOSITION RULE], [CAMERA + LENS + f-stop], [LIGHTING + Kelvin + direction], [SUBJECT with texture/detail], [WARDROBE with fabric], [ENVIRONMENT with layers], [ATMOSPHERE with physics], mood: [EMOTION] --ar X:Y`

## Composition rules to choose from
Rule of thirds · golden ratio / spiral · centred symmetry (Wes-Anderson style) · leading lines · negative space · frame-within-frame · low-angle hero / high-angle vulnerability · depth stacking.

## Negative-prompt baseline
`blurry, deformed hands, extra fingers, watermark, text overlay, low quality, bad anatomy, floating objects, duplicate limbs, disfigured, cropped, jpeg artifacts` — add scene-specific negatives (anachronisms, wrong gear, wrong culture details).

## Weak vs strong words
Weak: "4k", "HQ", "best quality", "masterpiece", "beautiful" (add little). Strong: physical cues — *volumetric, subsurface scattering, chiaroscuro, Rembrandt triangle, anamorphic flare, film grain, atmospheric perspective, tungsten 3200K, f/1.4 shallow depth of field*. The user's Black Camel scorer rewards the strong list and penalises the weak list — a useful heuristic, not a measure of image quality.

## Self-check before delivering
- All 7 layers present? · Lock text verbatim? · One light direction? · Time of day consistent with Kelvin? · Wardrobe matches era/culture? · Aspect ratio matches platform? · Negatives present? · No contradictory instructions?
