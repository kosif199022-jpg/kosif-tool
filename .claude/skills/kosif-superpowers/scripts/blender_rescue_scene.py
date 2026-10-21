#!/usr/bin/env python3
"""Blender-only, deterministic, original geometric cat-rescue demonstration.

Run using installed Blender, not system Python:
  blender -b --factory-startup --disable-autoexec --python scripts/blender_rescue_scene.py -- C:/temp/cat_rescue.blend

Cycles renderer selection and actual frame quality are verified by blender_cycles_render.py.
Creates original stylized 3D models from geometry; NOT photorealistic cat/human assets.
"""
from __future__ import annotations
import math
import sys
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ImportError:  # plain Python: show help instead of crashing
    if {"-h", "--help"} & set(sys.argv):
        print(__doc__)
        raise SystemExit(0)
    raise SystemExit("Run inside Blender: blender -b --factory-startup --disable-autoexec --python <this file> -- ...")

if "--" not in sys.argv:
    raise SystemExit("Expected -- OUTPUT.blend")
args=sys.argv[sys.argv.index("--")+1:]
if len(args)!=1:
    raise SystemExit("Expected exactly one output .blend")
output=Path(args[0]).resolve()
if output.suffix.lower()!=".blend" or output.exists() or not output.parent.is_dir():
    raise SystemExit("Output must be unused .blend path in existing directory")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

def mat(name,color,roughness=.48,metallic=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    shader=m.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value=(*color,1)
    shader.inputs["Roughness"].default_value=roughness
    shader.inputs["Metallic"].default_value=metallic
    return m

asphalt=mat("charcoal asphalt",(.12,.15,.17),.88)
pavement=mat("warm concrete",(.46,.44,.38),.9)
strip=mat("warm road paint",(.86,.67,.27),.55)
wall=mat("dusty green buildings",(.24,.39,.32),.75)
tile=mat("pinkish plaster",(.47,.29,.24),.85)
fur=mat("cat orange-gold fur",(.70,.33,.13),.8)
fur_light=mat("cat cream muzzle",(.95,.82,.59),.8)
ear_inner=mat("soft salmon inner ear",(.8,.37,.29),.75)
eye=mat("dark glossy eyes",(.025,.035,.035),.13)
nose=mat("rose cat nose",(.76,.28,.26),.43)
pants=mat("navy slacks",(.09,.16,.25),.78)
shirt=mat("warm jade jacket",(.13,.38,.29),.8)
skin=mat("warm human skin",(.65,.40,.26),.76)
hair=mat("dark hair",(.08,.08,.09),.7)
shoes=mat("brown shoes",(.18,.14,.12),.6)
water=mat("small puddle",(.15,.24,.26),.08,metallic=.28)
glass=mat("windows",(.1,.2,.22),.18,metallic=.23)

def place(obj,name,loc,scale,material):
    obj.name=name
    obj.location=loc
    obj.scale=scale
    if material:obj.data.materials.append(material)
    if obj.type=="MESH":
        for f in obj.data.polygons:f.use_smooth=True
    return obj

def cube(name,loc,scale,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    return place(bpy.context.object,name,loc,scale,material)

def sphere(name,loc,scale,material,parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10,location=loc)
    ob=place(bpy.context.object,name,loc,scale,material)
    if parent:
        ob.parent=parent
        ob.matrix_parent_inverse=parent.matrix_world.inverted()
    return ob

def cylinder(name,loc,radius,depth,material,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=radius,depth=depth,location=loc,rotation=rot)
    ob=bpy.context.object
    return place(ob,name,loc,(1,1,1),material)

def between(name,first,last,radius,material):
    direction=Vector(last)-Vector(first)
    center=(Vector(first)+Vector(last))/2
    ob=cylinder(name,center,radius,direction.length,material)
    ob.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
    return ob

def cone(name,loc,rad,dep,material):
    bpy.ops.mesh.primitive_cone_add(vertices=16,radius1=rad,radius2=0,depth=dep,location=loc)
    ob=bpy.context.object
    return place(ob,name,loc,(1,1,1),material)

def curve(name,points,material,radius=.045):
    cv=bpy.data.curves.new(name,"CURVE")
    cv.dimensions="3D";cv.resolution_u=16;cv.bevel_depth=radius;cv.bevel_resolution=3
    sp=cv.splines.new("BEZIER");sp.bezier_points.add(len(points)-1)
    for node,point in zip(sp.bezier_points,points):
        node.co=point;node.handle_left_type="AUTO";node.handle_right_type="AUTO"
    ob=bpy.data.objects.new(name,cv)
    bpy.context.collection.objects.link(ob);cv.materials.append(material)
    return ob

# Stylized physically shaded city street
cube("road", (0,-1.0,-.10), (9,7,.2),asphalt)
cube("sidewalk", (0,2.13,.015), (9,2.5,.28),pavement)
cube("curb edge", (0,.86,.03), (9,.12,.20),tile)
for x in [-3.7,-2.2,-.7,.8,2.3,3.8]:
    cube("lane-stripe", (x,-2.5,.014),(0.65,.06,.012),strip)
for x in (-2.65,-1.5,1.7,3.35):
    cube("brick wall", (x,4.0,1.9),(1.4,.35,3.8),wall if x<0 else tile)
    for z in (1.1,2.45):
        cube("window", (x,3.79,z),(.7,.06,.65),glass)
cube("parcel box",(-2.1,1.75,.5),(.8,.7,1),tile)
cube("wood fence", (2.5,2.45,.48),(1.9,.14,.96),wall)
sphere("reflective puddle",(.75,-.92,.015),(.63,.29,.012),water)
# Lamp and warm glow
between("lamp pole",(-3.6,.8,0),(-3.6,.8,3.1),.055,shoes)
between("lamp arm",(-3.6,.8,3.1),(-3.0,.55,3.0),.05,shoes)
sphere("lamp fixture",(-3,.55,2.95),(.11,.11,.08),strip)

# Moving cat, independent geometry parent under an empty
cat=bpy.data.objects.new("CAT_ANIMATED_GROUP",None)
bpy.context.collection.objects.link(cat)
cat.location=(-1.20,.05,.25)
def cat_part(name,offset,scale,material):
    ob=sphere(name,(cat.location.x+offset[0],cat.location.y+offset[1],
                   cat.location.z+offset[2]),scale,material)
    ob.parent=cat
    # convert global coords to local transform while retaining visual location
    ob.matrix_parent_inverse=cat.matrix_world.inverted()
    return ob
cat_part("cat torso",(-.18,0,.27),(.39,.22,.24),fur)
cat_part("cat head",(.26,0,.38),(.245,.22,.235),fur)
cat_part("white cat muzzle",(.42,-.02,.30),(.10,.17,.11),fur_light)
for y in (-.15,.15):
    ear=cone("cat ears",(.10 if y>0 else .11,y,.83),.12,.28,fur)
    ear.parent=cat;ear.matrix_parent_inverse=cat.matrix_world.inverted()
    cat_part("cat pupil",(.465,y*.8,.42),(.036,.044,.047),eye)
    cat_part("cat feet",(-.30,y*.85,.055),(.085,.095,.12),fur_light)
    cat_part("front cat feet",(.19,y*.85,.055),(.085,.095,.12),fur_light)
cat_part("cat nose",(.49,-.005,.295),(.028,.042,.03),nose)
tail=curve("cat curved tail",[(-1.53,.16,.54),(-1.71,.2,.87),(-1.53,.12,1.03)],fur,.052)
tail.parent=cat;tail.matrix_parent_inverse=cat.matrix_world.inverted()

# Human by side of street reaching hand to cat
torso=sphere("rescuer torso",(.90,.23,1.34),(.29,.22,.55),shirt)
sphere("rescuer head",(.82,.19,2.03),(.23,.215,.26),skin)
sphere("rescuer hair",(.80,.22,2.21),(.24,.22,.095),hair)
between("left leg",(.73,.23,1.03),(.70,.21,.25),.115,pants)
between("right leg",(1.05,.23,1.03),(1.33,.21,.25),.12,pants)
sphere("left shoe",(.69,.08,.20),(.22,.11,.105),shoes)
sphere("right shoe",(1.33,.08,.20),(.22,.11,.105),shoes)
between("support arm",(1.03,.10,1.60),(1.12,-.20,1.12),.087,shirt)
# Animated reaching arm/hand (single parent pivot)
arm=bpy.data.objects.new("RESCUER_HAND_ANIMATED",None)
bpy.context.collection.objects.link(arm)
arm.location=(.66,.05,1.50)
arm_obj=between("reaching sleeve",(.66,.05,1.5),(.22,-.05,.77),.08,shirt)
arm_obj.parent=arm;arm_obj.matrix_parent_inverse=arm.matrix_world.inverted()
hand=sphere("rescuer hand",(.20,-.05,.71),(.12,.09,.11),skin)
hand.parent=arm;hand.matrix_parent_inverse=arm.matrix_world.inverted()

# Physically based lighting using AREA, world HDR-like ambient (not actual HDRI)
world=bpy.context.scene.world
world.use_nodes=True
world.node_tree.nodes.get("Background").inputs["Color"].default_value=(.50,.60,.67,1)
world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.38
def light(name,loc,energy,size,color):
    bpy.ops.object.light_add(type="AREA",location=loc)
    obj=bpy.context.object;obj.name=name
    obj.data.energy=energy;obj.data.shape="DISK";obj.data.size=size;obj.data.color=color
    obj.rotation_euler=(Vector((0,0,.7))-obj.location).to_track_quat("-Z","Y").to_euler()
light("overcast daylight",(-3,-4,7),1100,5.8,(1,.90,.81))
light("sky softbox",(3,0,5),650,4.0,(.73,.86,1.0))
light("edge warm bounce",(1.5,3,4),400,3.0,(1.0,.76,.55))
# camera
bpy.ops.object.camera_add(location=(4.7,-7.5,3.25))
camera=bpy.context.object;camera.name="cinematic 3D camera"
target=Vector((0,.65,.95))
camera.rotation_euler=(target-camera.location).to_track_quat("-Z","Y").to_euler()
camera.data.lens=38
bpy.context.scene.camera=camera
camera.data.dof.use_dof=True
camera.data.dof.focus_distance=8.8
camera.data.dof.aperture_fstop=7

# Animation 2-second story
for frame, cat_x, arm_angle, cam_dist in [(1,-1.5,0,0),(8,-1.3,-.13,-.14),
  (16,-.97,-.22,-.29),(24,-.78,-.31,-.45)]:
    cat.location.x=cat_x; cat.keyframe_insert(data_path="location",frame=frame)
    arm.rotation_euler[1]=arm_angle;arm.keyframe_insert(data_path="rotation_euler",frame=frame)
    camera.location.y=-7.5+cam_dist;camera.location.x=4.7+cam_dist*.2
    camera.keyframe_insert(data_path="location",frame=frame)
# Timeline and render
s=bpy.context.scene
s.frame_start=1;s.frame_end=24;s.render.fps=12
s.render.engine="CYCLES"
s.cycles.samples=12
if hasattr(s.cycles,"use_denoising"):s.cycles.use_denoising=True
s.render.resolution_x=384;s.render.resolution_y=216;s.render.resolution_percentage=100
s.render.image_settings.file_format="PNG"
s.render.film_transparent=False
try:s.view_settings.view_transform="AgX"
except Exception:pass
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(output),check_existing=False)
print("KOSIF_3D_SCENE_CREATED",str(output),"objects",len(bpy.data.objects),"frames",s.frame_end,
      "engine",s.render.engine,flush=True)
