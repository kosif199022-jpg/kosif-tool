# Visual catalog (styles · lighting · cameras · lenses · angles · motion)

## Styles → descriptor strings
| Style | Descriptor |
|---|---|
| Cinematic Masterpiece | cinematic photography, ARRI ALEXA 65, anamorphic lens flare, film grain, ACES colour science, 16-bit RAW |
| Photorealistic | photorealistic, ultra-detailed, RAW photo, sharp focus, subsurface scattering, medium-format Hasselblad quality |
| Anime | Studio-Ghibli-like watercolour, hand-painted backgrounds, cel-shaded, whimsical atmosphere |
| 3D Render | Pixar-style 3D animation, subsurface scattering, ambient occlusion, global illumination |
| Dark Fantasy | gothic architecture, volumetric fog, dramatic chiaroscuro, ethereal glow |
| Product Commercial | hyper-real 3D commercial product shot, studio lighting, premium feel |
| Cyberpunk Neon | neon-drenched streets, holographic ads, rain reflections, teal and magenta |
| Film Noir | high-contrast B&W, Venetian-blind shadows, smoke, 1940s |
| Vintage Film | Kodak-Portra-400-style film, soft grain, warm tones, light leak |
| Watercolour | wet-on-wet technique, bleeding edges, paper texture |
| Surrealism | impossible physics, melting objects, dreamlike |
| Documentary | raw, photojournalistic, available light |
| Baroque Oil | Rembrandt-style chiaroscuro, visible brushstrokes, impasto |
| Gothic Horror | candlelight, long shadows, stone architecture, perpetual fog |
| Wes Anderson | perfect symmetry, pastel palette, centred composition |
| Solarpunk | living architecture, bioluminescent plants, sustainable tech |
| Claymation | stop-motion, visible fingerprints, handmade texture |
| Comic Book | bold outlines, halftone dots, dynamic angles |
| Vaporwave / Synthwave | pink-purple-cyan, glitch art, 80s nostalgia |
| Ukiyo-e | woodblock print, flat colour planes, flowing lines |
Also from the Omni master: Anime, Steampunk, Pixel Art, Low/High-poly 3D, Minimalist, Abstract, Pop Art, Fantasy, Sci-Fi, Romantic, Experimental.

## Lighting setups (with numbers)
| Setup | Recipe |
|---|---|
| Rembrandt | key ~45°, triangle of light on the shadow cheek, ~3:1 ratio, warm ~3200K |
| Butterfly / Paramount | key above the lens axis, symmetrical nose shadow, clamshell fill |
| Split | key at 90°, half face lit, maximum drama |
| Chiaroscuro | one hard source, no fill, deep shadows (Caravaggio) |
| Three-point | key + fill + rim/back; set ratio with `kosif_light_calc ratio` |
| High-key / Low-key | bright even, minimal shadow / dramatic single-source noir |
| Golden hour | sun ~15° above horizon, 3200–3500K, rim from behind |
| Blue hour | ~20 min after sunset, 7500–9000K sky, warm practicals |
| Volumetric / god rays | shafts through fog, dust or windows |
| Neon practical | cyan + magenta on wet surfaces |
| Candle / fire | 1800–2200K, flicker, intimate shadows |
| Moonlight | cool silver ~4100–6500K, soft through cloud |
| Silhouette / backlit | rim only, strong shape |
| Joel-Grimes-style edgy | two large softboxes behind + beauty dish above camera |
Colour-temperature shifts and gel choice: `kosif_light_calc op=mired`. Background falloff: `op=falloff`.

## Camera bodies
ARRI Alexa 65 / Alexa Mini LF (natural skin, wide DR) · RED V-Raptor 8K / Komodo 6K (global shutter, resolution) · Sony Venice 2 (dual-base ISO, highlight roll-off) · IMAX 70mm (huge gate) · Hasselblad X2D (medium-format detail) · Blackmagic URSA 12K · DJI Ronin 4D (stabilised, LiDAR focus) · iPhone Pro / Pixel Pro (computational, documentary feel) · GoPro/FPV (action) · VHS camcorder (lo-fi).

## Lenses
14mm ultra-wide · 24mm f/1.4 · 35mm f/1.4 · 50mm f/1.2 · 85mm portrait f/1.4 · 100mm macro · 135mm f/2 · 200mm f/2.8 · anamorphic 40mm (oval bokeh, horizontal flare). Wider = more environment & distortion; longer = compression & isolation.

## Shot sizes
ECU · CU · MCU · MS · full · wide · extreme wide · POV · over-the-shoulder · two-shot · insert.

## Angles
Eye level · low (hero) · high (vulnerability) · drone top-down · Dutch · worm's-eye · bird's-eye · POV first person.

## Camera motion
Static · pan · tilt · dolly in/out · truck · pedestal · zoom · orbit · handheld · Steadicam · natural-language motion (for video models describe the move in plain prose, e.g. "slow push-in as steam rises").

## Platforms in the user's apps
Veo 3.1 · Runway Gen-4.5 · Midjourney V7 · Kling 2.0 · Sora · Flux Pro · Grok · NanoBanana · ChatGPT image · SDXL · Ideogram. `kosif_prompt_forge` covers: chatgpt, midjourney, flux, sdxl, ideogram (image) and sora, veo, runway, kling (video).
