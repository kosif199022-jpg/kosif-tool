# Blender cat fur, facial detail and cinematic Cycles upgrade

KOSIF adds **real renderable procedural fur geometry**, NOT just an image effect. The shader and detailed .blend file use Blender 5.2 LTS through its supported Python API.

## What actually changed

- Original source: `blender_rescue_scene.py` outputs a fully editable animated 3D scene (cat, rescuer, road, camera). This source remains unchanged.
- New `scripts/blender_cat_fur_upgrade.py` opens the original, adds **2,600 deterministic geometry fur strands** (1,716 torso, 884 head for the example), six whiskers, two eye catchlights, human face landmarks, fur base-color noise and road material micro-bump.
- Adds approximate paw/ground contact correction by changing the cat's animated root Z while preserving the X animation.
- Sets a closer 3D camera, physical area lights retained and optional depth of field; saves a NEW editable `.blend`, never overwriting the original.
- `blender_cinematic_bridge.py pipeline --fur-count 2600` now automatically performs this upgrade in a private temporary `.blend`, renders using **genuine Cycles CPU**, checks the render report against actual SHA-256 scene/video hashes, then adds KOSIF 2D animated overlays and the source PCM-WAV soundtrack re-encoded as AAC into an H.264 MP4.
- Existing `pipeline` without `--fur-count` is backward-compatible. The standalone upgrader is available when editable upgraded .blend is needed.

## Standalone scene and a visual inspection

Run from `.claude/skills/kosif-superpowers/`, replacing the paths with unused paths on the authorized computer:

```powershell
& "C:\Users\Public\KOSIF-Tools\Blender5.2.2\blender-5.2.2-windows-x64\blender.exe" --background --factory-startup --disable-autoexec --python-exit-code 7 --python scripts/blender_cat_fur_upgrade.py -- --source ./rescue_scene.blend --output ./upgraded_cat.blend --fur-count 2600 --seed 2307
```

For an all-in-one end-to-end render, given real 16-bit PCM WAV and source scene:

```sh
python scripts/blender_cinematic_bridge.py pipeline --blend ./rescue_scene.blend --scene templates/blender-rescue-overlay-512.json --audio ./master.wav --output ./fur_scene_new.mp4 --fur-count 2600 --fur-seed 2307 --width 512 --height 288 --samples 12 --fps 12 --fade-frames 2 --pulse-element 2
```

**Three rendering levels** can be used with the same fully integrated pipeline: 384×216 at 4 samples (quick smoke), 512×288 at 12 samples (tested preview), and larger sizes/samples for further evaluations. Higher sample count alone cannot make simplified geometry photorealistic.

## Grounded acceptance

- The actual Blender 5.2.2 upgrade generated **2,600 curve strands and 6 whiskers, a 64-object editable scene**; 7/7 Blender regression tests passed, including Blender-native checking of curve count, animated parenting, physically shaded materials, face landmarks, source preservation, output collision refusal and bounds.
- The new 512×288 movie was rendered with **Cycles CPU, 12 samples, 24 frames, 12 fps**; the end-to-end KOSIF pipeline produced H.264 video with AAC audio and 4 attempted/onset candidate-driven pulses. Data and SHA-256 file receipts are recorded in `proofs/blender-cat-fur-upgrade-20261020.json`. An additional one-command auto-upgrade pipeline has been tested separately.
- Local media files and editable `.blend` originals: `C:\Users\Public\KOSIF-BLENDER-FUR-UPGRADE-20261020`.

## Boundaries

This improves perceived material realism, fine fur geometry and shot staging; it **does not** generate a live-action-looking animal or human automatically. Better results need physically correct fur grooming/dynamics, species-correct topology, optical eye models, realistic character rigs and facial anatomy, high-quality textures, acting, art direction, appropriate scene light and render budget.

Only original procedural assets or user-authorized scene inputs are used. Source .blend is opened with Blender's autoexec disabled. WAV source remains immutable; exported audio is re-encoded AAC. CPU video rendering may take significantly longer for fur strands and larger sizes. REA and Ghidra were not used here: documented Blender Python API is the suitable mechanism for actual Cycles rendering.
