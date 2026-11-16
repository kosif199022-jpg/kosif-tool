# Prompts for the painted version (option B), tested and working

- **Generator:** Higgsfield `generate_image_batch`.
- **Model:** `gpt_image_2_6`.
- **Settings:** `aspect_ratio: "9:16"`, default quality (0.25 credits per image; `quality: "high"` costs 1.5 per image, so don't use it).
- **References:** each image gets `medias: [{role: "image_references", value: <character sheet id>}, {role: "image_references", value: <style reference id>}]`.
- **Output:** 752×1344 images; the build script scales them to 1080×1920.

## 1. Character sheet (one image, 0.25)
Create it once and reuse it by its job_id. If you don't have the old one, upload `refs/charsheet.jpg` with `media_upload` and use its media_id.

> Character sheet in the exact hand-painted meme style of the reference: two cartoon friends, front and side views. CAP: round white bean head, red baseball cap, red t-shirt, dark trousers, red sneakers, cheerful. SPECS: round white bean head, round black glasses, spiky dark hair, blue t-shirt, grey trousers, calm and clever. Plain light background. No text.

## 2. Shots
Every shot prompt starts with:

> Vertical cartoon film frame in the exact hand-painted meme style of the references, same character(s) as the character sheet (Cap in red cap and red shirt, Specs with round glasses and blue shirt).

Then describe:
1. **The place and the light.** For example: heavy rain, grey-blue; or a hot desert, orange; or golden sunset.
2. **The action and the expression, in detail.** For example: laughing hysterically with eyes squeezed shut and tears, or a jealous stare with sweat and tongue out.
3. **The shot size:** wide shot, close-up, or medium close-up.
4. **End every prompt with** `No text, no letters.`

Rules:
- Add one empty background with no characters, to use as a transition (for example, "Next day…").
- **A prop that must stay the same across shots** (an umbrella, for example) gets its colour named in every prompt, e.g. "a BLACK umbrella". Otherwise its colour changes between shots.

## Full example: the upside-down umbrella film (9 images, about 2.25 credits)
Each line goes after the fixed opening:
- s0 wide: Heavy rain on a country road with puddles, grey-blue stormy light. Specs rides a bicycle holding an open black umbrella UPSIDE DOWN, handle pointing up and canopy facing the sky like a bowl, half full of rainwater. Cap rides beside him under a normal umbrella, laughing hard and pointing at him. Full bodies, wide shot.
- s1 close-up: Cap laughing hysterically, mouth wide open, eyes squeezed shut, tears of laughter, pointing right, holding a normal black umbrella, heavy rain.
- s2 insert: an open black umbrella upside down like a bowl, filled to the brim with rainwater, drops splashing, water spilling over the edges; below it Specs's calm face with a small confident smile.
- s3 medium close-up: Specs riding in the rain, drops on his glasses, calm knowing half smile, the full upside-down umbrella above him.
- s4 wide: blazing hot desert road, huge sun, cracked ground, cactus, heat haze; Cap red-faced dripping sweat under a normal umbrella, tongue out; Specs calm with the upside-down umbrella still full of water.
- s5 medium close-up: Specs sips cool water through a long clear tube running down from the upside-down umbrella, eyes closed in bliss, cheeks blushing.
- s6 close-up: Cap in desert heat, sunburned cheeks, cracked lips, tongue out, sweat, eyes wide and jealous staring right.
- s7 wide: desert road at golden sunset, Specs smiling hands the tube to Cap, Cap drinks and laughs, warm backlight, long shadows.
- s8 background with no characters (style reference only): empty desert road at sunrise, huge glowing sun, cacti, heat haze.
