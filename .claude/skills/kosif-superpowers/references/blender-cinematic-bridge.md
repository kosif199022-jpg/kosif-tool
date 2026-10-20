# KOSIF Blender + Unified Cinematic integration

KOSIF now connects an installed **Blender Cycles renderer** to the existing **KOSIF Unified Draw + audio-clocked 2D compositor**.

## Working architecture

```text
Original .blend / .gltf / .glb
       │
       ▼
blender_cycles_render.py (installed Blender 5.2.2, Cycles CPU)
       │ PNG frames → H.264 MP4 with readback frame QA
       ▼
blender_cinematic_bridge.py
       ├── audio_cue_mapper.py: PCM WAV duration and amplitude-onset candidates
       ├── unified_draw.py: authored shape/stroke layers and keyframes
       ├── unified_media.compose / creative_paint.py: alpha overlays per decoded Blender frame
       ├── unified_cinematic.fade_frame: visual fade in/out
       └── FFmpeg: H.264 video with source WAV re-encoded as AAC audio
                │
                ▼
    tested output: MP4 with matching video frames and audio
```

**The original 3D geometry is rendered by genuine Blender Cycles, not simulated by Three.js or a KOSIF renderer.** KOSIF controls generation of a deterministic demonstration scene and composes the independently rendered silent 3D footage with graphics and audio.

## Local working commands

Run from `.claude/skills/kosif-superpowers/`. Use new output paths.

```powershell
python scripts/blender_cinematic_bridge.py doctor

# Scene generation via installed Blender (outputs an editable .blend):
& "C:\Users\Public\KOSIF-Tools\Blender5.2.2\blender-5.2.2-windows-x64\blender.exe" --background --factory-startup --disable-autoexec --python-exit-code 7 --python scripts/blender_rescue_scene.py -- "C:\Users\Public\KOSIF-BLENDER-CINEMATIC-20261020\rescue_scene.blend"

# Fully integrated pipeline, 3D render + compositing + original WAV:
python scripts/blender_cinematic_bridge.py pipeline --blend "C:\Users\Public\KOSIF-BLENDER-CINEMATIC-20261020\rescue_scene.blend" --scene templates/blender-rescue-overlay.json --audio "C:\Users\Public\KOSIF-UNIFIED-CINEMATIC-ACCEPTANCE-20261020\master.wav" --output "C:\Users\Public\KOSIF-BLENDER-CINEMATIC-20261020\final_new.mp4" --fps 12 --width 384 --height 216 --samples 4 --fade-frames 2 --pulse-element 2

# Or compose pre-rendered Blender video without re-rendering the scene:
python scripts/blender_cinematic_bridge.py compose --blender-video ./cycles_raw.mp4 --scene templates/blender-rescue-overlay.json --audio ./source.wav --output ./composite.mp4 --fps 12 --pulse-element 2
python scripts/test_blender_cinematic_bridge.py
```

Each command is a fresh new file; **never overwrite** originals. `pipeline` uses the existing Blender Cycles renderer, scene validation, real PNG frames, video encoding and FFprobe readback. `compose` accepts only verified compatible silent MP4/MKV input. Note that other independently generated MP4 files should have separate provenance; do not call non-Blender footage "Cycles".

The example scene is built from original geometry under `scripts/blender_rescue_scene.py`: modeled street, stylized orange cat moving toward a person, animated reaching arm, road puddle, area lighting, physically based materials, Cycles denoising, depth of field and animated 3D camera. **This is a stylized demo, NOT photorealistic live-action cat footage.** No commercial assets or models are copied or packaged. Genuine photorealism would additionally require production-grade fur/skin grooming, rigging, textures, lighting, acting, shading, and longer production renders.

## Scope, checks and limitations

- 3D input: user-authorized `.blend`, `.gltf`, `.glb` only; embedded .blend auto-execution disabled when launched by the Cycles renderer. The sample generator refuses to overwrite an existing .blend.
- 2D overlay: `kosif.unified-draw.v1`, same dimensions and fps as the actual Blender render, optional keyframe motion and measured transient-driven pulses. Pulse refuses to overwrite manually authored keyframes.
- Sound master: uncompressed 16-bit PCM WAV (0.1–30 seconds). Video duration is frame-quantized to the WAV. WAV source is unchanged; exported AAC is re-encoded and **not sample-identical**. Music beats/BPM and phonemes are *not verified*.
- Resource bounds: max 300 frames, 1–60 fps, 4–64 Cycles samples for integrated pipeline, render width/height even and 64–2048, bounded frame-pixel budget, fresh output paths. MP4 H.264/AAC output verified via FFprobe.
- No source Blender model, test audio or video are published from a user's personal libraries; acceptance artifacts remain on the authorized computer. Code and sanitized SHA-256 evidence only go to GitHub.

## Verification

The bridge's **eight integration tests** generate independent synthetic FFmpeg video/audio samples, check real output codecs and frame counts, validate failure modes, and confirm source input integrity. Full Cycles production acceptance is separately recorded at `proofs/blender-cinematic-acceptance-20261020.json`, including scene SHA256, render report and source/output codecs and sample preview.

The integration has no need to reverse-engineer Blender binaries with REA/Ghidra; Blender's supported Python API and genuine Cycles executable are used. Reverse engineering of separate authorized binaries remains a distinct research task.
