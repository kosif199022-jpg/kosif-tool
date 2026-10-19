# Blender 5.2.2: KOSIF Cat Rescue — five-second runtime proof

- Authored as original procedural Blender geometry and animation, not third-party binary code.
- cat_rescue_scene.py creates a stylized rescuer, ginger kitten, crate, path, scenery and 75 animated frames.
- Blender Workbench rendered 75 unique frames at 15 fps, 640x360.
- FFmpeg encoded H.264 at 30 fps by frame duplication, 5.000 seconds and 150 encoded frames, silent.
- cat_rescue_5s_editable.blend opens in Blender for modifying meshes, camera and keyframes.
- Technical concept proof, not photorealistic or professional-quality acting.
- Output verified using ffprobe on the Windows host, 2026-10-19.

Reproduction with installed Blender:

    blender --background --factory-startup --disable-autoexec --python cat_rescue_scene.py -- frames

    ffmpeg -framerate 15 -start_number 1 -i frames/frame_%04d.png -vf fps=30,format=yuv420p -t 5 -c:v libx264 -crf 19 -movflags +faststart -an cat_rescue_5s.mp4

Uses Blender Python API, not reverse-engineered binary algorithms.
