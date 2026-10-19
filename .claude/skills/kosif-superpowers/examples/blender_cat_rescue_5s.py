"""Original five-second KOSIF cat rescue. Runs with Blender bpy (headless).
Stylized procedural animation; no downloaded models, no proprietary assets.
Render: blender -b --factory-startup --disable-autoexec -t 4 -P THIS_FILE
"""
import bpy, math, os
from mathutils import Vector
from pathlib import Path
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=480
scene.render.resolution_y=854
scene.render.resolution_percentage=100
scene.render.fps=24
scene.frame_start=1
scene.frame_end=120
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(Path.home()/'KOSIF_RESEARCH_PRIVATE_20261019'/'cat_rescue_frames')+os.sep
scene.render.film_transparent=False
scene.view_settings.view_transform='Standard'
scene.display.shading.light='STUDIO'
scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_shadows=True
scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH'
scene.world=bpy.data.worlds.new('Midnight')
scene.world.color=(0.06,0.09,0.14)
def mat(name,rgba):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*rgba,1)
    return m
colors={
 'street':mat('warm concrete',(0.35,.34,.31)),
 'building':mat('midnight-indigo',(.11,.17,.23)),
 'building2':mat('slate-blue',(.17,.25,.29)),
 'window':mat('warm window',(.94,.64,.27)),
 'jacket':mat('olive bomber',(.20,.39,.31)),
 'shirt':mat('white shirt',(.91,.86,.73)),
 'jeans':mat('black jeans',(.13,.20,.27)),
 'skin':mat('warm skin',(.72,.47,.33)),
 'hair':mat('dark hair',(.12,.12,.14)),
 'cat':mat('orange fur',(.84,.37,.17)),
 'white':mat('white fur',(.97,.89,.73)),
 'eye':mat('amber eye',(.27,.45,.25)),
 'pink':mat('nose',(1,.47,.54)),
 'red':mat('heart',(.91,.20,.27)),
 'plaster':mat('gentle bandage',(.94,.84,.66)),
 'stripe':mat('fur stripes',(.56,.22,.11))}
def parent(o,p):
    o.parent=p
    return o
def cube(name,loc,scale,material,par=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=name;o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    if par:parent(o,par)
    bevel=o.modifiers.new('Soft rounded edges','BEVEL');bevel.width=min(scale)*.17;bevel.segments=2
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def sphere(name,loc,scale,material,par=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=1,location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material)
    if par:parent(o,par)
    for poly in o.data.polygons:poly.use_smooth=True
    return o
def cone(name,loc,rad,depth,material,par=None):
    bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=rad,radius2=.015,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;o.data.materials.append(material)
    if par:parent(o,par)
    return o
def empty(name,loc=(0,0,0),par=None):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc
    if par:parent(o,par)
    return o
def key(o,frames,prop='location'):
    for f,value in frames:
        setattr(o,prop,value);o.keyframe_insert(data_path=prop,frame=f)
    # Blender 5.x uses layered Actions; Bezier is the native keyframe default.
cube('wet pavement',(0,0,-.12),(12,9,.20),colors['street'])
for i,(x,y,h) in enumerate([(-3,3.2,4.9),(1,3.9,5.5),(4,3.7,4.3)]):
    cube('old Cairo building %s'%i,(x,y,h/2),(2.6,1.1,h),colors['building' if i%2==0 else 'building2'])
    for j in range(3):
        cube('window', (x-.45,y-.61,1.5+j*.95),(.36,.04,.47),colors['window'])
        cube('window', (x+.45,y-.61,1.5+j*.95),(.36,.04,.47),colors['window'])
cube('sidewalk stripe',(0,-2,-.01),(9,.13,.025),colors['plaster'])
hero=empty('HERO_RIG')
key(hero,[(1,(-2.6,0,0)),(22,(-1.25,0,0)),(37,(-1.1,0,0)),(60,(-1.1,0,-.31)),(82,(-1.1,0,0)),(120,(-.25,0,0))])
torso=empty('HERO_TORSO',(0,0,1.3),hero)
key(torso,[(1,(0,0,1.3)),(39,(0,0,1.3)),(60,(.1,0,1.04)),(80,(0,0,1.3)),(120,(0,0,1.3))])
cube('olive jacket',(0,0,0),(.76,.39,.96),colors['jacket'],torso)
cube('shirt visible',(0,-.216,.03),(.28,.025,.82),colors['shirt'],torso)
sphere('head',(0,-.02,.75),(.30,.27,.34),colors['skin'],torso)
sphere('hair cap',(0,-.03,.98),(.305,.28,.14),colors['hair'],torso)
sphere('nose',(0,-.29,.70),(.055,.07,.055),colors['skin'],torso)
for side in (-1,1):
    sphere('eyes',(side*.113,-.267,.80),(.027,.024,.035),colors['hair'],torso)
    cube('pants leg',(side*.19,0,-1.02),(.28,.32,1.05),colors['jeans'],torso)
    cube('shoe',(side*.19,-.15,-1.55),(.3,.55,.19),colors['hair'],torso)
    shoulder=empty('ARM_%s'%side,(side*.45,-.02,.33),torso)
    cube('sleeve',(0,0,-.32),(.24,.28,.62),colors['jacket'],shoulder)
    sphere('hand',(0,-.01,-.69),(.11,.11,.16),colors['skin'],shoulder)
    rot=lambda a:(0,a,0)
    if side==1:
        key(shoulder,[(1,rot(.07)),(36,rot(.15)),(54,rot(-1.30)),(74,rot(-1.22)),(100,rot(-1.00)),(120,rot(-.94))],'rotation_euler')
    else:
        key(shoulder,[(1,rot(.00)),(37,rot(-.10)),(54,rot(-.93)),(78,rot(-1.03)),(120,rot(-.95))],'rotation_euler')
# cat consists of original primitive geometry parented to one animated rig
cat=empty('RESCUED_CAT')
key(cat,[(1,(.38,-.1,.25)),(47,(.38,-.1,.25)),(58,(-.39,-.48,.46)),
         (79,(-.61,-.41,1.23)),(100,(-.40,-.38,1.25)),(120,(.18,-.38,1.25))])
sphere('orange tabby body',(0,0,.10),(.47,.25,.23),colors['cat'],cat)
sphere('white chest',(-.24,-.175,.16),(.21,.14,.20),colors['white'],cat)
sphere('cat head',(-.33,-.1,.31),(.25,.23,.25),colors['cat'],cat)
sphere('white muzzle',(-.43,-.287,.21),(.17,.065,.10),colors['white'],cat)
for side in (-1,1):
    cone('pointy cat ears',(-.36+side*.16,-.10,.57),.09,.21,colors['cat'],cat)
    sphere('cat eyes',(-.36+side*.098,-.313,.36),(.043,.022,.056),colors['eye'],cat)
    sphere('small pupils',(-.36+side*.098,-.336,.36),(.013,.012,.034),colors['hair'],cat)
    sphere('cat paws',(.22+side*.17,-.16,-.09),(.10,.10,.07),colors['white'],cat)
sphere('pink nose',(-.45,-.34,.245),(.033,.025,.025),colors['pink'],cat)
# curved tail composed of small ellipsoids
for i in range(5):
    sphere('upright fluffy tail %d'%i,(.42+i*.035,.14,.12+i*.15),(.065,.07,.11),colors['cat'],cat)
for i in range(3):
    cube('tabby stripes %d'%i,(.05+i*.13,-.224,.28-i*.018),(.05,.032,.085),colors['stripe'],cat)
cube('gentle bandage',(.20,-.02,-.09),(.14,.24,.09),colors['plaster'],cat)
heart=empty('HEART_REVEAL',(-.26,-.2,2.15))
sphere('heart left',(-.11,0,0),(.13,.10,.13),colors['red'],heart)
sphere('heart right',(.11,0,0),(.13,.10,.13),colors['red'],heart)
cone('heart tip',(0,0,-.15),.17,.28,colors['red'],heart)
key(heart,[(1,(0,0,0)),(76,(0,0,0)),(83,(.55,.55,.55)),(98,(1,1,1)),(120,(.9,.9,.9))],'scale')
camdata=bpy.data.cameras.new('Film camera')
camera=bpy.data.objects.new('Film camera',camdata);bpy.context.collection.objects.link(camera)
camera.location=(5,-10,4.3)
target=Vector((-.3,0,1.55))
camera.rotation_euler=(target-Vector(camera.location)).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO';camdata.ortho_scale=7.75;scene.camera=camera
camdata.keyframe_insert(data_path='ortho_scale',frame=1)
camdata.ortho_scale=6.65;camdata.keyframe_insert(data_path='ortho_scale',frame=120)
# workbench previews are computationally efficient and deterministic
scene.camera.data.lens=36
scene.render.filepath=str(Path.home()/'KOSIF_RESEARCH_PRIVATE_20261019'/'cat_rescue_frames')+os.sep
bpy.ops.wm.save_as_mainfile(filepath=str(Path.home()/'KOSIF_RESEARCH_PRIVATE_20261019'/'KOSIF_CAT_RESCUE_5S.blend'))
print('KOSIF_CAT_RESCUE_SCENE_READY',len(scene.objects),scene.frame_end,flush=True)
bpy.ops.render.render(animation=True)
print('KOSIF_CAT_RESCUE_ALL_FRAMES_FINISHED',flush=True)
