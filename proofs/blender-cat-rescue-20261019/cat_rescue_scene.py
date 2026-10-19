import bpy,math,sys
from mathutils import Vector
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1]);out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.world=bpy.data.worlds.new('Sky');s.world.color=(.50,.66,.83)
s.render.engine='BLENDER_WORKBENCH'
s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL'
s.display.shading.show_shadows=True;s.display.shading.background_type='WORLD'
s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.fps=15;s.frame_start=1;s.frame_end=75
def mat(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);return m
G=mat('park',(0.26,.46,.28));Y=mat('rescue jacket',(1,.69,.20));S=mat('skin',(.94,.69,.52))
B=mat('pants',(.16,.32,.56));K=mat('eyes',(.08,.09,.11));O=mat('ginger cat',(.95,.45,.15))
W=mat('white',(.96,.90,.74));R=mat('rescue',(.88,.24,.22));D=mat('wood',(.47,.28,.18))
def mesh(kind,name,pos,scale,m,parent=None):
 if kind=='cube':bpy.ops.mesh.primitive_cube_add(size=1,location=pos)
 elif kind=='cone':bpy.ops.mesh.primitive_cone_add(vertices=8,location=pos)
 else:bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=pos)
 v=bpy.context.object;v.name=name;v.scale=scale;v.data.materials.append(m)
 if parent:v.parent=parent;v.location=pos
 return v
def empty(name):
 o=bpy.data.objects.new(name,None);s.collection.objects.link(o);return o
mesh('cube','lawn',(0,0,-.15),(12,6,.24),G)
mesh('cube','footpath',(0,-.5,.002),(12,1.65,.06),W)
mesh('cube','cat stuck in a box',(1.6,.1,.27),(.98,.83,.52),D)
mesh('cube','blue stream',(2.25,1.0,.02),(1.5,1.4,.02),B)
for x in (-4.2,-3.4,3.1,4.3):mesh('sphere','bush',(x,1.5,.38),(.5,.48,.42),G)
p=empty('Hero movement')
mesh('cube','yellow coat',(0,0,1.35),(.60,.39,.89),Y,p)
mesh('sphere','head',(0,-.03,2.13),(.30,.28,.33),S,p)
mesh('sphere','dark hair',(0,.035,2.35),(.32,.29,.15),K,p)
for x in (-.13,.13):
 mesh('sphere','hero eye',(x,-.29,2.17),(.038,.023,.046),K,p)
 mesh('cube','blue leg',(x*1.5,0,.64),(.23,.30,.77),B,p)
 mesh('cube','shoe',(x*1.5,-.07,.22),(.34,.45,.16),K,p)
mesh('cube','left arm',(-.39,0,1.35),(.17,.22,.73),Y,p)
arm=mesh('cube','right arm reach',(.41,-.1,1.35),(.19,.23,.76),Y,p)
mesh('sphere','left hand',(-.39,-.1,1.0),(.115,.12,.11),S,p)
hand=mesh('sphere','right hand',(.48,-.12,1.0),(.115,.12,.11),S,p)
cat=empty('Ginger kitten')
mesh('sphere','kitten body',(0,0,.15),(.32,.20,.18),O,cat)
mesh('sphere','kitten head',(.20,-.09,.35),(.20,.17,.20),O,cat)
mesh('sphere','white chest',(.20,-.20,.18),(.11,.07,.15),W,cat)
for x in (.07,.32):
 mesh('cone','triangle ear',(x,-.03,.58),(.10,.10,.13),O,cat)
 mesh('sphere','kitten eye',(x,-.245,.38),(.035,.022,.047),K,cat)
mesh('sphere','pink nose',(.24,-.268,.31),(.04,.025,.03),R,cat)
mesh('sphere','long raised tail',(-.32,.08,.42),(.09,.075,.27),O,cat)
for x in (-.18,.19):mesh('sphere','little paw',(x,-.07,.025),(.09,.11,.06),W,cat)
bpy.ops.object.camera_add(location=(2.5,-10,5.0))
c=bpy.context.object;c.rotation_euler=(Vector((0,0,1.2))-c.location).to_track_quat('-Z','Y').to_euler()
c.data.type='ORTHO';c.data.ortho_scale=7.5;s.camera=c
def ease(a,b,n):
 t=max(0,min(1,(n-a)/(b-a)));return t*t*(3-2*t)
def lerp(a,b,t):return a+(b-a)*t
# Final narration is expressed in visuals: approach, reach, lift, carry to safety.
for f in range(1,76):
 approach=ease(1,30,f);reach=ease(28,43,f);lift=ease(42,58,f);returning=ease(58,75,f)
 hx=lerp(-2.75,.50,approach)-.75*returning
 p.location=(hx,-.55,.035*math.sin(f*.7)*((1-approach)*approach+returning*(1-returning)))
 p.rotation_euler=(0,-.20*(reach-lift),0)
 arm.rotation_euler=(0,-.98*reach+.34*lift,0)
 hand.location=(lerp(.46,.92,reach)-.14*lift,-.13,lerp(1.0,1.14,reach)+.23*lift)
 cx=lerp(1.60,hx+.69,lift)
 cz=lerp(.53,1.30,lift)
 cat.location=(cx,-.22,cz)
 cat.rotation_euler=(0,.10*math.sin(f*.2),0)
 p.keyframe_insert('location',frame=f);p.keyframe_insert('rotation_euler',frame=f)
 cat.keyframe_insert('location',frame=f);cat.keyframe_insert('rotation_euler',frame=f)
 arm.keyframe_insert('rotation_euler',frame=f)
 hand.keyframe_insert('location',frame=f)
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out.parent/'Cat_Rescue_5s_Editable.blend'))
for f in range(1,76):
 s.frame_set(f)
 s.render.filepath=str(out/('frame_%04d.png'%f))
 bpy.ops.render.render(write_still=True)
 if f in (1,15,30,45,60,75):print('KOSIF_RENDER_PROGRESS',f,'/75',flush=True)
print('KOSIF_RESCUE_COMPLETE',flush=True)
