#!/usr/bin/env python3
"""Executed ONLY by locally installed Blender. Original bpy geometry from bounded JSON."""
import argparse
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser(
    prog="blender_worker.py", formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Blender-side KOSIF scene builder: re-validates a kosif.blender.v1 scene JSON and writes\n"
                "a .png still, a .blend or an animated .glb. It runs only inside Blender;\n"
                "blender_bridge.py render is the usual way to launch it.",
    epilog="example:\n  blender --background --factory-startup --disable-autoexec --python-exit-code 3 \\\n"
           "    --python scripts/blender_worker.py -- templates/blender-demo.json ./out/scene.glb")
parser.add_argument("scene", help="kosif.blender.v1 scene JSON")
parser.add_argument("output", help="new output path ending in .png, .blend or .glb")
# Inside Blender the worker's arguments follow "--"; plain python passes them directly.
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
try:
    import bpy
except ImportError:
    parser.error("bpy is not available: run this inside Blender "
                 "(blender --background --python blender_worker.py -- scene.json out.glb) "
                 "or use blender_bridge.py render")
source, output = Path(args.scene).resolve(), Path(args.output).resolve()

scene = json.loads(source.read_text(encoding="utf-8-sig"))
# Called from blender_bridge.py after schema validation; validate again to avoid bypass.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from blender_bridge import validate
validate(scene)
bpy.ops.wm.read_factory_settings(use_empty=True)
stage = bpy.context.scene
stage.render.resolution_x, stage.render.resolution_y = scene.get("size", [512, 512])
stage.render.resolution_percentage = 100
stage.render.image_settings.file_format = "PNG"
stage.render.film_transparent = False
stage.frame_start = 1
stage.frame_end = scene.get("frames", 1)
stage.render.fps = scene.get("fps", 24)
operators = {"cube": bpy.ops.mesh.primitive_cube_add,
             "sphere": bpy.ops.mesh.primitive_uv_sphere_add,
             "cylinder": bpy.ops.mesh.primitive_cylinder_add,
             "cone": bpy.ops.mesh.primitive_cone_add,
             "torus": bpy.ops.mesh.primitive_torus_add}
for index, item in enumerate(scene["objects"]):
    operators[item["shape"]]()
    obj = bpy.context.object
    obj.name = "KOSIF_Object_%02d" % index
    obj.location = item.get("location", [0, 0, 0])
    obj.scale = item.get("scale", [1, 1, 1])
    rgba = item.get("color", [0.2, 0.5, 0.35, 1.0])
    material = bpy.data.materials.new("KOSIF_Material_%02d" % index)
    material.diffuse_color = rgba
    material.use_nodes = True
    material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = rgba
    obj.data.materials.append(material)
    for key in item.get("keyframes", []):
        obj.location = key["location"]
        obj.keyframe_insert(data_path="location", frame=key["frame"])

bpy.ops.object.camera_add(location=(8, -12, 9))
camera = bpy.context.object
direction = (0, 0, 0)
from mathutils import Vector
camera.rotation_euler = (Vector(direction) - camera.location).to_track_quat("-Z", "Y").to_euler()
stage.camera = camera
bpy.ops.object.light_add(type="AREA", location=(3, -4, 8))
bpy.context.object.data.energy = 1000
bpy.context.object.data.shape = "DISK"
bpy.context.object.data.size = 6
stage.world = bpy.data.worlds.new("KOSIF_World")
stage.world.color = (0.15, 0.15, 0.15)
if output.suffix.lower() == ".frames":
    output.mkdir(parents=True, exist_ok=False)
    stage.render.engine = "BLENDER_WORKBENCH"
    stage.display.shading.light = "STUDIO"
    stage.display.shading.color_type = "MATERIAL"
    stage.render.image_settings.file_format = "PNG"
    stage.render.filepath = str(output / "frame_")
    bpy.ops.render.render(animation=True)
    expected = scene.get("frames", 1)
    found = len(list(output.glob("frame_*.png")))
    if found != expected:
        raise RuntimeError("Blender animation frame count mismatch: %s != %s" % (found, expected))
    print("KOSIF_BLENDER_FRAMES", found)
    sys.exit(0)
if output.suffix.lower() == ".png":
    stage.render.filepath = str(output)
    bpy.ops.render.render(write_still=True)
elif output.suffix.lower() == ".blend":
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
elif output.suffix.lower() == ".glb":
    bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", export_animations=True)
else:
    raise ValueError("unsupported output suffix")
if not output.is_file() or output.stat().st_size < 24:
    raise RuntimeError("Blender did not create output")
print("KOSIF_BLENDER_OUTPUT", output.stat().st_size)
