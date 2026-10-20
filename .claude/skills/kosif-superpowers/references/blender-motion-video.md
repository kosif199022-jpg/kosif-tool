# KOSIF headless Blender motion to MP4

The original KOSIF Blender adapter now has a dedicated H.264 motion exporter.
Run Blender in the background; there is no need to open the graphical interface.
The installed Blender engine and FFmpeg are still required. In contrast, the
limited KOSIF native_3d.py rasterizer needs no Blender.

From a full kosif-tool checkout root, run the local adapter doctor, then:

    python .claude/skills/kosif-superpowers/scripts/blender_motion_video.py render --scene .claude/skills/kosif-superpowers/templates/blender-demo.json --output video.mp4 --blender C:/path/to/blender.exe

Only bounded, validated kosif.blender.v1 JSON is admitted, with 1-12 primitives,
1-240 frames, at 1-60 fps, resolution 128-1920 pixels. Blender starts with
--background --factory-startup --disable-autoexec and renders a temporary
image sequence in Workbench. FFmpeg encodes H.264. ffprobe verifies codec, dimensions
and exact frame count. Existing outputs are not overwritten.

A one-second 24-frame 128x128 real render passed on the owner's Windows laptop
using Blender 5.2.2. This is not equivalent to a professional photorealistic
human or cat video; the existing separate five-second cat-rescue Blender demo
contains simplified procedural geometry. The renderer does not add narration.

Provenance: independent KOSIF integration using publicly documented Blender
APIs, not Blender engine copied into KOSIF. For zero-Blender rendering, see
scripts/native_3d.py and its separate limitations and tests.
