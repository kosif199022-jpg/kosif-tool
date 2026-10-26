"""Consent-gated public client for external Python rendering. Python 3.10+ stdlib.

No API key, browser renderer, media uploads, redirects, or command execution.
Job capabilities live only in memory. Never print raw remote responses.
"""
from __future__ import annotations
import argparse
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from site_bridge import read_plan, parse_json, BridgeError

ORIGIN = 'https://kosif-motion-workbench.smartsphere152.chatgpt.site'
MAX_JSON_BYTES = 1_048_576
MAX_VIDEO_BYTES = 100 * 1024 * 1024
DEADLINE_SECONDS = 300
PATH = re.compile(r'/api/(?:validate|compile|render/(?:status|jobs(?:/[A-Za-z0-9_-]{20,128}(?:/video)?)?))\Z')
CAPABILITY = re.compile(r'[A-Za-z0-9_-]{20,128}\Z')

class RenderError(Exception):
    """Only fixed, non-secret error messages may be surfaced."""

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RenderError('Redirect refused; only the fixed HTTPS Site is allowed.')

def emit(event, **safe_fields):
    print(json.dumps({'event':event, **safe_fields}, ensure_ascii=False), flush=True)

def remaining(deadline):
    seconds=deadline-time.monotonic()
    if seconds<=0:raise RenderError('Render deadline exceeded; no automatic resubmission.')
    return min(20,seconds)

def make_request(method,path,payload=None,token=None):
    if not PATH.fullmatch(path):raise RenderError('Unapproved endpoint refused.')
    allowed = ('GET',) if path.endswith('/status') or path.endswith('/video') else ('POST',) if path in ('/api/validate','/api/compile','/api/render/jobs') else ('GET','DELETE')
    if method not in allowed:raise RenderError('Unapproved method refused.')
    headers={'Accept':'application/json' if not path.endswith('/video') else 'video/mp4'}
    if token is not None:
        if not isinstance(token,str) or not CAPABILITY.fullmatch(token) or not path.startswith('/api/render/jobs/'):
            raise RenderError('Invalid job capability or target.')
        headers['X-Job-Token']=token
    body=None
    if payload is not None:
        if method!='POST':raise RenderError('Unexpected request body.')
        try:body=json.dumps(payload,ensure_ascii=False,allow_nan=False).encode('utf-8')
        except (ValueError,TypeError,RecursionError):raise RenderError('Invalid finite JSON payload.') from None
        if len(body)>MAX_JSON_BYTES:raise RenderError('Request exceeds 1 MiB.')
        headers['Content-Type']='application/json'
    return urllib.request.Request(ORIGIN+path,method=method,headers=headers,data=body)

def open_response(req,deadline):
    try:
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
        response=opener.open(req,timeout=remaining(deadline))
        if response.geturl()!=req.full_url:
            response.close();raise RenderError('Unexpected response location refused.')
        return response
    except urllib.error.HTTPError as exc:
        code=exc.code;exc.close()
        if code in (502,503):raise RenderError('Python render backend is unconfigured or unavailable; hosting resources must be provided separately.') from None
        if code==429:raise RenderError('Shared demo quota or active-job limit reached; no automatic paid upgrade or retry.') from None
        raise RenderError('Site request failed (HTTP %d); no automatic retry.'%code) from None
    except (urllib.error.URLError,OSError,ValueError):raise RenderError('Site connection failed; no automatic provisioning or charges.') from None

def api(method,path,payload=None,*,token=None,deadline=None):
    if deadline is None:deadline=time.monotonic()+20
    req=make_request(method,path,payload,token)
    with open_response(req,deadline) as response:
        if response.headers.get('Content-Type','').split(';')[0].strip().lower()!='application/json':
            raise RenderError('Expected JSON from the Site.')
        raw=response.read(MAX_JSON_BYTES+1)
    remaining(deadline)
    try:return parse_json(raw)
    except BridgeError:raise RenderError('Invalid or oversized JSON response.') from None

def check_status(deadline=None):
    status=api('GET','/api/render/status',deadline=deadline)
    if status.get('configured') is not True:raise RenderError('External Python renderer is not configured; hosting resources and provisioning are pending.')
    if status.get('ready') is not True:raise RenderError('External Python renderer is unavailable; no automatic provisioning or charges.')
    return {'configured':True,'ready':True,'engine':'python-pillow-ffmpeg'}

def prepare_manifest(source):
    keys={'schema','title','width','height','fps','duration','scenes'}
    if not isinstance(source,dict) or set(source)!=keys or source['schema']!='kosif.motion.manifest.v1':raise RenderError('Unsupported manifest.')
    m=dict(source)
    for key in ('width','height','fps','duration'):
        if isinstance(m[key],bool) or not isinstance(m[key],(int,float)) or not math.isfinite(m[key]):raise RenderError('Invalid manifest dimensions or timing.')
    if m['fps'] not in (24,25,30) or not 1<=m['duration']<=30 or min(m['width'],m['height'])<128:raise RenderError('Only 24/25/30 fps, 1–30 seconds and dimensions at least 128 are supported.')
    scale=min(1,1280/max(m['width'],m['height']))
    m['width']=int(m['width']*scale//2)*2;m['height']=int(m['height']*scale//2)*2
    if min(m['width'],m['height'])<128:raise RenderError('Scaled dimensions are below 128 pixels.')
    if not isinstance(m['title'],str) or not 1<=len(m['title'])<=5000:raise RenderError('Invalid manifest title.')
    frames=round(m['fps']*m['duration'])
    if abs(frames-m['fps']*m['duration'])>.001:raise RenderError('Duration must contain whole frames.')
    if not isinstance(m['scenes'],list) or not 1<=len(m['scenes'])<=50:raise RenderError('Expected 1–50 scenes.')
    end=0;ids=set()
    cameras={'fast_reveal','slow_push','match_cut','focus_lift','still_hold','locked','dolly_in','orbit','side_track','push_in'}
    for s in m['scenes']:
        if not isinstance(s,dict) or set(s)!={'id','start_frame','end_frame_exclusive','title','subtitle','camera','accent'}:raise RenderError('Unsupported scene fields; media and commands are forbidden.')
        if not isinstance(s['id'],str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',s['id']) or s['id'] in ids:raise RenderError('Invalid scene identifier.')
        ids.add(s['id'])
        if type(s['start_frame']) is not int or type(s['end_frame_exclusive']) is not int or s['start_frame']!=end or not end<s['end_frame_exclusive']<=frames:raise RenderError('Scenes must cover the timeline without gaps or overlaps.')
        end=s['end_frame_exclusive']
        if not isinstance(s['camera'],str) or s['camera'] not in cameras or not isinstance(s['accent'],str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',s['accent']):raise RenderError('Unsupported scene appearance.')
        if any(not isinstance(s[k],str) or len(s[k])>limit for k,limit in [('title',120),('subtitle',300)]):raise RenderError('Scene text exceeds supported limits.')
    if end!=frames:raise RenderError('Scenes do not cover the duration.')
    return m

def compile_plan(plan,deadline=None):
    if plan.get('intent')!='2d_motion':raise RenderError('Only 2D motion plans are supported; 3D, footage and prompt jobs are refused.')
    if api('POST','/api/validate',{'plan':plan},deadline=deadline).get('valid') is not True:raise RenderError('Plan validation failed.')
    compiled=api('POST','/api/compile',{'plan':plan},deadline=deadline)
    return prepare_manifest(compiled.get('manifest'))

def checked_output(path):
    path=Path(path)
    if '..' in path.parts or path.suffix.lower()!='.mp4':raise RenderError('Use a new .mp4 output without parent traversal.')
    path=path.absolute()
    if any(p.is_symlink() for p in (path,*path.parents)) or path.exists() or not path.parent.is_dir():raise RenderError('Output must be new with an existing non-symlink parent; no overwrites.')
    return path

def download(job_id,token,out,deadline):
    out=checked_output(out);partial=None
    req=make_request('GET','/api/render/jobs/'+job_id+'/video',token=token)
    try:
        with open_response(req,deadline) as response:
            if response.headers.get('Content-Type','').split(';')[0].strip().lower()!='video/mp4':raise RenderError('Download is not video/mp4.')
            length=response.headers.get('Content-Length')
            if length is not None and (not length.isdigit() or not 12<=int(length)<=MAX_VIDEO_BYTES):raise RenderError('Invalid or excessive download size.')
            fd,name=tempfile.mkstemp(prefix='.'+out.name+'-',suffix='.partial',dir=out.parent);partial=Path(name)
            total=0;prefix=b''
            with os.fdopen(fd,'wb') as stream:
                while True:
                    remaining(deadline);chunk=response.read(65536)
                    if not chunk:break
                    total+=len(chunk)
                    if total>MAX_VIDEO_BYTES:raise RenderError('Download exceeds 100 MiB.')
                    prefix=(prefix+chunk)[:12];stream.write(chunk)
                stream.flush();os.fsync(stream.fileno())
            if total<12 or prefix[4:8]!=b'ftyp' or (length is not None and total!=int(length)):raise RenderError('Invalid or incomplete MP4 bytes.')
        remaining(deadline)
        # Atomic no-clobber publication: unlike os.rename on POSIX, link cannot overwrite.
        os.link(partial,out)
        return total
    except OSError:raise RenderError('Download or exclusive output creation failed; existing files preserved.') from None
    finally:
        if partial is not None:partial.unlink(missing_ok=True)

def render(plan,out,*,allow_remote=False):
    if not allow_remote:raise RenderError('Approved transmission of plan contents requires --allow-remote.')
    out=checked_output(out);deadline=time.monotonic()+DEADLINE_SECONDS
    job_id=token=None
    try:
        check_status(deadline)
        manifest=compile_plan(plan,deadline)
        emit('submitting',width=manifest['width'],height=manifest['height'],fps=manifest['fps'],seconds=manifest['duration'])
        job=api('POST','/api/render/jobs',{'manifest':manifest},deadline=deadline)
        job_id=job.get('job_id');token=job.get('job_token')
        if not all(isinstance(v,str) and CAPABILITY.fullmatch(v) for v in (job_id,token)):
            job_id=token=None;raise RenderError('Invalid job capability response; no resubmission.')
        path='/api/render/jobs/'+job_id
        while True:
            result=api('GET',path,token=token,deadline=deadline)
            state=result.get('status')
            if state not in ('queued','running','succeeded','failed','cancelled'):raise RenderError('Unsupported render state.')
            progress=result.get('progress');safe={}
            if type(progress) in (int,float) and math.isfinite(progress) and 0<=progress<=1:safe['progress']=progress
            emit(state,**safe)
            if state=='succeeded':
                size=download(job_id,token,out,deadline);emit('downloaded',bytes=size,audio=False);return out
            if state in ('failed','cancelled'):raise RenderError('Remote render did not complete; no automatic resubmission or charges.')
            time.sleep(min(2,remaining(deadline)))
    except (KeyboardInterrupt,RenderError):
        if job_id and token:
            try:api('DELETE','/api/render/jobs/'+job_id,token=token,deadline=time.monotonic()+10)
            except (RenderError,OSError):emit('cancellation_unconfirmed')
        raise

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('status');p=sub.add_parser('render');p.add_argument('--plan',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--allow-remote',action='store_true')
    args=parser.parse_args(argv)
    try:
        if args.command=='status':emit('status',**check_status())
        else:render(read_plan(args.plan),args.out,allow_remote=args.allow_remote)
        return 0
    except KeyboardInterrupt:emit('interrupted');return 130
    except (RenderError,BridgeError) as exc:emit('error',message=str(exc));return 2
    except (OSError,ValueError,TypeError,RecursionError):emit('error',message='Client failed safely; no automatic retry.');return 2
if __name__=='__main__':raise SystemExit(main())
