# KOSIF independent native Z-buffer rasterizer

This is original CPU rasterization code; it does **not** run Blender.
`native_3d.py` accepts existing `kosif.native3d.v1` JSON with optional
`"render_mode": "zbuffer"` for per-pixel barycentric depth interpolation.
The prior `painter` mode remains the default for backward compatibility.

From the repository root:

```powershell
python .claude/skills/kosif-superpowers/scripts/native_3d.py doctor
python .claude/skills/kosif-superpowers/scripts/native_3d.py render --scene .claude/skills/kosif-superpowers/templates/native-zbuffer-demo.json --output depth-proof.png
```

It draws opaque cube/sphere/cylinder/cone/torus meshes, supports orthographic camera,
translation and yaw keyframes, flat directional shading and PNG/MP4 export.
It uses Pillow and FFmpeg, not bpy and not any other Blender component.
No PBR, textured materials, 3D physics, shadows, bone skinning or ray tracing.
Occlusion with exactly coplanar/intersecting surfaces remains ambiguous.
The renderer is a small subset and must not be labeled Blender-compatible.
Use read-only Blender source/documentation study to prioritize future work.
