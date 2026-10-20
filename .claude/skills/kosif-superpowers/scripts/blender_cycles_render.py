#!/usr/bin/env python3
"""Render authorized 3D scenes using Blender Cycles, FFmpeg and read-back QA."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BLENDER_SCRIPT = r"""
import argparse, bpy, sys
from mathutils import Vector
p=argparse.ArgumentParser()
for flag in ('scene','folder','device'): p.add_argument('--'+flag,required=True)
for flag in ('fps','frames','width','height','samples'): p.add_argument('--'+flag,type=int,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
if a.scene.lower().endswith('.blend'):
    bpy.ops.wm.open_mainfile(filepath=a.scene,load_ui=False)
else:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=a.scene)
s=bpy.context.scene
if s.camera is None:
    vertices=[obj.matrix_world@Vector(c) for obj in s.objects if obj.type=='MESH' for c in obj.bound_box]
    if not vertices: raise RuntimeError('No camera or mesh in scene')
    lo=Vector([min(v[i] for v in vertices) for i in range(3)])
    hi=Vector([max(v[i] for v in vertices) for i in range(3)])
    c=(lo+hi)*0.5
    distance=max((hi-lo).length,1.0)
    bpy.ops.object.camera_add(location=c+Vector((distance,-distance*1.4,distance*.8)))
    camera=bpy.context.object
    camera.rotation_euler=(c-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.lens=45
    s.camera=camera
if not any(o.type=='LIGHT' for o in s.objects):
    bpy.ops.object.light_add(type='AREA',location=(3,-4,7))
    light=bpy.context.object
    light.data.energy=800;light.data.shape='DISK';light.data.size=5
s.render.engine='CYCLES';s.cycles.samples=a.samples;s.cycles.device=a.device
if hasattr(s.cycles,'use_denoising'):s.cycles.use_denoising=True
s.render.resolution_x=a.width;s.render.resolution_y=a.height
s.render.resolution_percentage=100
s.render.fps=a.fps;s.frame_start=1;s.frame_end=a.frames
s.render.image_settings.file_format='PNG'
s.render.filepath=a.folder+'/frame_'
try:s.view_settings.view_transform='AgX'
except Exception:pass
bpy.ops.render.render(animation=True)
print('KOSIF_RENDERED',a.frames)
"""
def executable(given,name):
    if given:
        p=Path(given).expanduser()
        return str(p.resolve()) if p.is_file() else shutil.which(given)
    cmd=shutil.which(name)
    if cmd:return cmd
    if name=='blender':
        roots=[Path(r'C:\Users\Public\KOSIF-Tools\Blender5.2.2\blender-5.2.2-windows-x64\blender.exe'),
               Path.home()/'scoop/apps/blender/current/blender.exe',
               Path.home()/'scoop/apps/blender/5.2.2/blender.exe',
               Path(r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe')]
        return next((str(x) for x in roots if x.is_file()),None)
    return None
def digest(f):
    h=hashlib.sha256()
    with open(f,'rb') as inp:
        for b in iter(lambda:inp.read(1048576),b''):h.update(b)
    return h.hexdigest()
def checked(cmd):
    done=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace')
    if done.returncode:raise RuntimeError('Command failed '+str(done.returncode)+' '+done.stdout[-1200:])
    return done.stdout[-500:]
def main():
    p=argparse.ArgumentParser()
    p.add_argument('action',choices=['doctor','plan','render'])
    for arg in ('scene','out','blender','ffmpeg','ffprobe'):p.add_argument('--'+arg)
    for arg,default in (('fps',30),('frames',150),('width',640),('height',360),('samples',24)):
        p.add_argument('--'+arg,type=int,default=default)
    p.add_argument('--device',choices=['CPU','GPU'],default='CPU')
    a=p.parse_args()
    engines={n:executable(getattr(a,n),n) for n in ('blender','ffmpeg','ffprobe')}
    if a.action=='doctor':
        print(json.dumps({'engines':engines,'ready':all(engines.values()),'renderer':'Cycles',
                          'limitation':'Realism also requires high-quality meshes, realistic materials, rigging and lighting'},indent=2));return
    if not a.scene or not a.out: p.error('--scene and --out required')
    src=Path(a.scene).resolve();out=Path(a.out).resolve()
    if not src.is_file() or src.suffix.lower() not in ('.blend','.glb','.gltf'):
        raise ValueError('Input must be existing .blend/.glb/.gltf scene')
    if out.suffix.lower() not in ('.mp4','.mkv') or out.exists():raise ValueError('Output must be a new .mp4/.mkv path')
    if not (1<=a.frames<=3600 and 1<=a.fps<=120 and 4<=a.samples<=512
            and 64<=a.width<=4096 and 64<=a.height<=4096 and a.width%2==0 and a.height%2==0):
        raise ValueError('Invalid size, sample count, duration or fps')
    report={'source':str(src),'sha256':digest(src),'output':str(out),
            'resolution':[a.width,a.height],'fps':a.fps,'frames':a.frames,
            'duration_seconds':a.frames/a.fps,'samples':a.samples,
            'device':a.device,'engine':'Cycles','tools':engines,'status':'PLAN_ONLY'}
    if a.action=='plan':
        print(json.dumps(report,ensure_ascii=False,indent=2));return
    if not all(engines.values()):raise RuntimeError('Blender, FFmpeg and FFprobe are required; use doctor')
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='kosif_cycles_') as temp:
        root=Path(temp);frames=root/'frames';frames.mkdir()
        job=root/'cycles_scene.py';job.write_text(BLENDER_SCRIPT,encoding='utf-8')
        checked([engines['blender'],'--background','--factory-startup','--disable-autoexec',
                 '--python-exit-code','7','--python',str(job),'--','--scene',str(src),
                 '--folder',str(frames),'--fps',str(a.fps),'--frames',str(a.frames),
                 '--width',str(a.width),'--height',str(a.height),
                 '--samples',str(a.samples),'--device',a.device])
        if len(list(frames.glob('frame_*.png')))!=a.frames:
            raise RuntimeError('Actual PNG frame count does not match requested frames')
        checked([engines['ffmpeg'],'-hide_banner','-loglevel','error','-nostdin',
                 '-framerate',str(a.fps),'-start_number','1','-i',str(frames/'frame_%04d.png'),
                 '-c:v','libx264','-crf','18','-pix_fmt','yuv420p',
                 '-movflags','+faststart','-an',str(out)])
    info=subprocess.run([engines['ffprobe'],'-v','error','-select_streams','v:0',
           '-show_entries','stream=width,height,nb_frames,codec_name','-of','json',str(out)],
           capture_output=True,text=True,check=True)
    details=json.loads(info.stdout)['streams'][0]
    if details['width']!=a.width or details['height']!=a.height or int(details.get('nb_frames',a.frames))!=a.frames:
        raise RuntimeError('Video QA failure')
    report.update(status='VERIFIED_VIDEO',video_sha256=digest(out),probe=details)
    rpt=out.with_name(out.stem+'.render-report.json')
    rpt.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'video':str(out),'report':str(rpt),'status':'VERIFIED_VIDEO'}))
if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError,subprocess.SubprocessError) as exc:
        print(json.dumps({'error':str(exc),'status':'FAILED'},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)
