#!/usr/bin/env python3
"""Original KOSIF Blender cat fur/detail upgrade for an authorized .blend.

Executed INSIDE Blender 5.2 via --background --factory-startup --disable-autoexec.
Fur: deterministic geometry curve splines parented to existing animated sphere
parts, with physically based strand geometry and subtle color gradients.
Neither copies Blender proprietary code nor asserts photorealistic quality.
"""
from __future__ import annotations
import argparse
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

parser=argparse.ArgumentParser()
parser.add_argument("--source",required=True)
parser.add_argument("--output",required=True)
parser.add_argument("--fur-count",type=int,default=2600)
parser.add_argument("--seed",type=int,default=2307)
p=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
source=Path(p.source).resolve()
output=Path(p.output).resolve()
if source.suffix.lower()!=".blend" or not source.is_file():
    raise SystemExit("Existing .blend source required")
if output.suffix.lower()!=".blend" or output.exists() or not output.parent.is_dir() or output==source:
    raise SystemExit("Output must be new .blend within existing directory")
if not 200<=p.fur_count<=7000 or not 0<=p.seed<=10000000:
    raise SystemExit("Fur count 200..7000 and deterministic seed 0..10000000 required")
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False)
scene=bpy.context.scene
required=("CAT_ANIMATED_GROUP","cat torso","cat head","cat nose","cat curved tail")
if not all(name in bpy.data.objects for name in required):
    raise SystemExit("Source is not the verified original KOSIF cat scene")
if bpy.data.objects.get("KOSIF_CAT_FUR_TORSO") or bpy.data.objects.get("KOSIF_CAT_FUR_HEAD"):
    raise SystemExit("Source already contains this upgrade; refuse duplicate")
random.seed(p.seed)
# Add subtle physically-based multilayer fur to the existing orange material.
fur=bpy.data.materials.get("cat orange-gold fur")
fur.use_nodes=True
nodes=fur.node_tree.nodes
links=fur.node_tree.links
shader=nodes.get("Principled BSDF")
tex=nodes.new("ShaderNodeTexNoise")
tex.label="Procedural gentle tabby roughness"
tex.inputs["Scale"].default_value=6.5
tex.inputs["Detail"].default_value=3
tex.inputs["Roughness"].default_value=.65
ramp=nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position=.20
ramp.color_ramp.elements[0].color=(.29,.107,.033,1)
ramp.color_ramp.elements[1].position=.81
ramp.color_ramp.elements[1].color=(.83,.43,.14,1)
links.new(tex.outputs["Fac"],ramp.inputs["Fac"])
links.new(ramp.outputs["Color"],shader.inputs["Base Color"])
shader.inputs["Roughness"].default_value=.75
# Skin-like microdetail for human face: slight varying roughness only.
skin=bpy.data.materials.get("warm human skin")
skin_shader=skin.node_tree.nodes.get("Principled BSDF")
skin_shader.inputs["Roughness"].default_value=.58
head=bpy.data.objects["cat head"]
torso=bpy.data.objects["cat torso"]

fur_material=bpy.data.materials.new("KOSIF-fur-strands-golden-amber")
fur_material.diffuse_color=(.56,.27,.095,1)
fur_material.use_nodes=True
pbs=fur_material.node_tree.nodes.get("Principled BSDF")
pbs.inputs["Base Color"].default_value=(.56,.265,.09,1)
pbs.inputs["Roughness"].default_value=.8

def make_fur(name, parent, strands, length, radius):
    curves=bpy.data.curves.new(name,"CURVE")
    curves.dimensions="3D"
    curves.resolution_u=1
    curves.bevel_resolution=1
    curves.bevel_depth=radius
    curves.use_fill_caps=False
    mat=fur_material
    curves.materials.append(mat)
    for j in range(strands):
        z=random.uniform(-.97,.97)
        phi=random.uniform(-math.pi,math.pi)
        xy=math.sqrt(max(.005,1-z*z))
        normal=Vector((xy*math.cos(phi),xy*math.sin(phi),z))
        # Lower torso is not exposed fur: put strand density on top/side.
        if name.endswith("TORSO") and normal.z < -.50:
            normal.z=-normal.z*.75
            normal.normalize()
        # The curve uses unit-sphere local coordinates and inherits the
        # sphere's animated object scale/location and CAT root parenting.
        jitter=random.uniform(.82,1.14)
        tangent=Vector((-normal.y,normal.x,.12))
        tangent.normalize()
        start=normal*.988
        root=start + normal*(.015*length)
        middle=start + normal*(length*.62*jitter) + tangent*(.024*length)
        tip=start + normal*(length*jitter) + tangent*(.06*length)
        spline=curves.splines.new("POLY")
        spline.points.add(2)
        for coord,point in zip((root,middle,tip),spline.points):
            point.co=(coord.x,coord.y,coord.z,1)
    obj=bpy.data.objects.new(name,curves)
    bpy.context.collection.objects.link(obj)
    # Curve coordinate system is local to the sphere; inherits its complete
    # animated world transformation, including the parent CAT root.
    obj.parent=parent
    obj.location=(0,0,0)
    obj.rotation_euler=(0,0,0)
    obj.scale=(1,1,1)
    return obj

torso_n=round(p.fur_count*.66)
head_n=p.fur_count-torso_n
torso_fur=make_fur("KOSIF_CAT_FUR_TORSO",torso,torso_n,.15,.0025)
head_fur=make_fur("KOSIF_CAT_FUR_HEAD",head,head_n,.092,.0022)
# Eyelids and highlight geometry are anchored in head-local coordinates.
def head_sphere(name,loc,scale,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(0,0,0))
    obj=bpy.context.object
    obj.name=name
    obj.parent=head
    obj.location=loc
    obj.scale=scale
    obj.data.materials.append(material)
    for pol in obj.data.polygons:pol.use_smooth=True
    return obj

gloss=bpy.data.materials.new("KOSIF-eye-catchlight")
gloss.diffuse_color=(1,1,.91,1)
gloss.use_nodes=True
gloss.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value=(1,1,.87,1)
for side in (-1,1):
    # Existing head geometry is a unit sphere scaled to .245,.22,.235.
    head_sphere("KOSIF-eye-shine",(.88,side*.45,.21),(.08,.055,.07),gloss)

# Whiskers in head coordinates, inherited directly from the animated head.
whisker=bpy.data.materials.new("KOSIF-cream-whiskers")
whisker.diffuse_color=(.96,.91,.77,1)
curve=bpy.data.curves.new("KOSIF-cat-whisker-curves","CURVE")
curve.dimensions="3D";curve.bevel_depth=.002;curve.bevel_resolution=2
curve.materials.append(whisker)
for side in (-1,1):
    for row in range(3):
        base=Vector((.81,side*.54,-.29+row*.06))
        extension=Vector((.93+row*.06,side*(1.45+row*.10),-.42+row*.15))
        spline=curve.splines.new("BEZIER");spline.bezier_points.add(1)
        for pt,v in zip(spline.bezier_points,(base,extension)):
            pt.co=v;pt.handle_left_type="AUTO";pt.handle_right_type="AUTO"
whiskers=bpy.data.objects.new("KOSIF_CAT_WHISKERS",curve)
bpy.context.collection.objects.link(whiskers)
whiskers.parent=head

# Fix original floating paws. Cat's white foot pads have their lowest points
# at world z ~= 0.18 at the original animated root height 0.25, so lower
# the CAT root until paws approach road contact. Preserve XY animation.
cat=bpy.data.objects["CAT_ANIMATED_GROUP"]
for f in (1,8,16,24):
    scene.frame_set(f)
    cat.location.z=.066
    cat.keyframe_insert(data_path="location",frame=f)

# Add simple facial landmarks to the previously faceless rescuer. These remain
# procedural/stylized; no claims of scanned human geometry.
human=bpy.data.objects.get("rescuer head")
if human:
    eye_mat=bpy.data.materials.get("dark glossy eyes")
    skin_mat=bpy.data.materials.get("warm human skin")
    for side in (-1,1):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(0,0,0))
        obj=bpy.context.object
        obj.name="KOSIF_RESCUER_EYE"
        obj.parent=human
        obj.location=(side*.36,-.86,.12)
        obj.scale=(.09,.063,.065)
        obj.data.materials.append(eye_mat)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(0,0,0))
    obj=bpy.context.object
    obj.name="KOSIF_RESCUER_NOSE"
    obj.parent=human
    obj.location=(0,-.96,-.12)
    obj.scale=(.15,.14,.20)
    obj.data.materials.append(skin_mat)

# Material work on the street as well, without proprietary HDR texture.
road=bpy.data.materials["charcoal asphalt"]
rough=road.node_tree.nodes.get("Principled BSDF")
noise=road.node_tree.nodes.new("ShaderNodeTexNoise")
noise.label="Procedural microvariation, no image license needed"
noise.inputs["Scale"].default_value=100
bump=road.node_tree.nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value=.13
bump.inputs["Distance"].default_value=.02
road.node_tree.links.new(noise.outputs["Fac"],bump.inputs["Height"])
road.node_tree.links.new(bump.outputs["Normal"],rough.inputs["Normal"])
# Focus on rescue rather than street wide, with moderately shallow DOF.
cam=scene.camera
cam.location=(3.1,-5.25,2.32)
cam.data.lens=43
target=Vector((-.18,.30,.65))
cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
cam.data.dof.use_dof=True
cam.data.dof.focus_distance=(target-cam.location).length
cam.data.dof.aperture_fstop=6.3
# Existing animation is keyframed: keyframe revised camera composition with subtle push.
for f,off in ((1,0.0),(8,-.10),(16,-.20),(24,-.31)):
    cam.location=(3.1+off*.25,-5.25+off,2.32)
    cam.keyframe_insert(data_path="location",frame=f)
scene.render.engine="CYCLES"
scene.cycles.samples=16
scene.render.resolution_x=512;scene.render.resolution_y=288
scene.render.resolution_percentage=100
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(output),check_existing=False)
print("KOSIF_FUR_UPGRADE_VERIFIED", "fur_strands",p.fur_count,
      "torso_splines",len(torso_fur.data.splines),
      "head_splines",len(head_fur.data.splines),
      "whiskers",len(whiskers.data.splines),
      "object_count",len(bpy.data.objects),"engine",scene.render.engine,
      "output",str(output),flush=True)
