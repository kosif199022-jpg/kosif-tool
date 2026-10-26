"""KOSIF Voice2Motion v2.2 — audio-led semantic motion graphics (v5.2: fonts found on Windows/Linux/macOS, shaped Arabic captions).
Offline Python/Pillow/NumPy/FFmpeg. Transcripts are provided by user or via external ASR;
never claims auto transcription or precise word alignment when only text is supplied.
Output is deterministic for fixed audio, cue sheet, fps and size.
"""
from __future__ import annotations
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to a legacy code page
import argparse, json, math, re, wave, subprocess, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
FF=shutil.which('ffmpeg') or 'ffmpeg'; FP=shutil.which('ffprobe') or 'ffprobe'   # resolved paths (a bare name misses .cmd stand-ins on Windows)
WHITE=(238,247,255); MUTED=(132,160,181); CYAN=(64,222,232); GOLD=(255,196,79); GREEN=(81,236,179); RED=(255,103,112)
import os

def _first(paths):
    for p in paths:
        if p and Path(p).is_file():return str(p)
    return None

_WIN=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
_LOCAL=Path(os.environ.get('LOCALAPPDATA','.'))/'Microsoft'/'Windows'/'Fonts'
# Arabic-capable first (shaped text needs a font with Arabic presentation forms), then Latin fallbacks.
FONT_PATH=_first([os.environ.get('KOSIF_FONT'),_LOCAL/'NotoKufiArabic-Regular.ttf',_WIN/'NotoKufiArabic-Regular.ttf',_LOCAL/'Amiri-Regular.ttf',_WIN/'Amiri-Regular.ttf',
    _WIN/'segoeui.ttf',_WIN/'tahoma.ttf',_WIN/'arial.ttf','/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'])
BOLD_PATH=_first([os.environ.get('KOSIF_FONT_BOLD'),_LOCAL/'NotoKufiArabic-Bold.ttf',_WIN/'NotoKufiArabic-Bold.ttf',_LOCAL/'Amiri-Bold.ttf',_WIN/'Amiri-Bold.ttf',
    _WIN/'segoeuib.ttf',_WIN/'tahomabd.ttf',_WIN/'arialbd.ttf','/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/System/Library/Fonts/Supplemental/Arial Bold.ttf']) or FONT_PATH
_FONTS={}
def font(size,bold=False):
    key=(bool(bold),max(9,round(size)))
    if key not in _FONTS:
        p=BOLD_PATH if bold else FONT_PATH
        _FONTS[key]=ImageFont.truetype(p,key[1]) if p else ImageFont.load_default()
    return _FONTS[key]

_AR=re.compile(r'[\u0600-\u06FF]')
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _RESHAPER=arabic_reshaper.ArabicReshaper({'delete_harakat':False,'support_ligatures':True})
except Exception:                                            # pragma: no cover - shaping is optional
    _RESHAPER=None; get_display=None
def shape(s):
    """Arabic text as Pillow must receive it: joined letterforms, visual (RTL) order. Latin passes through."""
    s=str(s)
    if _RESHAPER is None or not _AR.search(s):return s
    return get_display(_RESHAPER.reshape(s))

CUE={'text':''}
def head(default=''):
    """The scene's big label from the cue's own words: its number, else its longest word — never a fact it did not say."""
    t=CUE['text'];m=re.search(r'\d+(?:[.,:]\d+)?',t)
    if m:return m.group(0)
    ws=[w.strip('.,!?؟،') for w in t.split()]
    return max(ws,key=len) if ws else default

def sub(n=26):
    t=CUE['text'].strip()
    return t if len(t)<=n else t[:n-1].rsplit(' ',1)[0]+'…'

def probe_audio(path):
    if not Path(path).is_file(): raise FileNotFoundError(path)
    r=subprocess.run([FP,'-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)],capture_output=True,text=True,check=True)
    d=float(r.stdout.strip());
    if not 0<d<3600:raise ValueError('Audio duration must be >0 and <3600 seconds')
    return d

def validate_cues(cues,duration):
    if not isinstance(cues,list) or not cues:raise ValueError('At least one cue is required')
    out=[];p=-1
    for c in cues:
        if not {'start','end','text','kind'}<=set(c):raise ValueError('Cue missing start/end/text/kind')
        a,b=float(c['start']),float(c['end'])
        if not (0<=a<b<=duration+.08):raise ValueError(f'Invalid cue timing: {c}')
        if a<p-0.015:raise ValueError('Cues must be sorted and nonoverlapping')
        p=b
        if c['kind'] not in {'weather','traffic','support','refund','generic'}:raise ValueError('Unknown visual cue '+c['kind'])
        out.append({'start':a,'end':min(b,duration),'text':str(c['text']),'kind':c['kind']})
    return out

def classify(text):
    t=text.lower()
    if re.search(r'refund|funds back|استرداد|استرجاع|مرتجع',t):return 'refund'
    if re.search(r'charge|support|ticket|billing|frustrat|شكوى|تذكرة|فاتورة|مشكلة',t):return 'support'
    if re.search(r'traffic|bridge|meeting|early|commut|مرور|زحام|اجتماع|بدري',t):return 'traffic'
    if re.search(r'sunny|weather|degree|morning|طقس|صباح|مشمس|درجات',t):return 'weather'
    return 'generic'

def estimate_cues(text,duration):
    """A fallback, not word-level ASR: durations are approximated from the provided transcript."""
    parts=[s.strip() for s in re.split(r'(?<=[.!?؟])\s+|\n+',text) if s.strip()]
    if not parts:raise ValueError('Transcript is empty')
    weights=np.array([max(4,len(s.split())) for s in parts],float);weights/=weights.sum()
    edges=np.r_[0,np.cumsum(weights)*duration];edges[-1]=duration
    return [{'start':round(float(edges[i]),3),'end':round(float(edges[i+1]),3),'text':s,'kind':classify(s)} for i,s in enumerate(parts)]

def audio_envelope(audio,rate=50):
    # Use ffmpeg as WAV/MP3/M4A reader; pipe mono PCM @8000 Hz.
    p=subprocess.run([FF,'-v','error','-i',str(audio),'-ac','1','-ar','8000','-f','s16le','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    samples=np.frombuffer(p.stdout,np.int16).astype(np.float32)/32768
    hop=160;cnt=len(samples)//hop
    if not cnt:return np.ones(1,dtype=np.float32)*.1
    rms=np.sqrt(np.mean(samples[:cnt*hop].reshape(cnt,hop)**2,axis=1))
    norm=float(np.percentile(rms,90))+.0001
    return np.clip(rms/norm,0,1.5).astype(np.float32)

def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)

def clamp(x,a=0,b=1):return min(b,max(a,x))

def rr(d,box,r,fill,outline=None,width=1):
    box=tuple(map(int,box));d.rounded_rectangle(box,radius=int(r),fill=fill,outline=outline,width=width)

def txt(d,x,y,s,size=30,col=WHITE,bold=False,anchor=None):
    d.text((int(x),int(y)),shape(s),font=font(size,bold),fill=col,anchor=anchor)

def centered(d,x,y,s,size,col=WHITE,bold=False):txt(d,x,y,s,size,col,bold,'mm')

def wrap_words(text,maxchars=27,maxlines=3):
    if _AR.search(text):maxchars=int(maxchars*1.15)            # Arabic letters are narrower once joined
    words=text.split();lines=[];curr=''
    for w in words:
        if len((curr+' '+w).strip())>maxchars and curr:
            lines.append(curr);curr=w
        else:curr=(curr+' '+w).strip()
    if curr:lines.append(curr)
    if len(lines)>maxlines:
        lines=lines[:maxlines-1]+[' '.join(lines[maxlines-1:])]
    return lines

def draw_sun(d,x,y,r,t):
    pulse=1+.035*math.sin(t*2.5)
    for j in range(3):
        q=r*(1.5+j*.25);d.ellipse((x-q,y-q,x+q,y+q),outline=(25+j*13,81+j*11,99+j*11),width=2)
    for k in range(12):
        a=k*math.tau/12 + .08*math.sin(t);r0=r*1.12;r1=r*1.35
        d.line((x+math.cos(a)*r0,y+math.sin(a)*r0,x+math.cos(a)*r1,y+math.sin(a)*r1),fill=GOLD,width=5)
    r*=pulse;d.ellipse((x-r,y-r,x+r,y+r),fill=GOLD)
    d.ellipse((x-r*.62,y-r*.62,x+r*.62,y+r*.62),fill=(255,220,125))

def weather(d,t,W,H,level):
    x,y=W//2,round(H*.33);draw_sun(d,x,y-36,W*.115,t)
    # cloud travelling on a curved path
    cx=x+W*.17+15*math.sin(t*.6);cy=y+W*.09
    for a,b,rad in [(-34,0,24),(-8,-13,30),(22,0,25)]:d.ellipse((cx+a-rad,cy+b-rad,cx+a+rad,cy+b+rad),fill=(222,240,249))
    rr(d,(W*.12,H*.54,W*.88,H*.73),22,(17,43,61),outline=(35,95,112),width=2)
    h=head();centered(d,W/2,H*.585,h+('°' if h[:1].isdigit() else ''),58,WHITE,True)
    centered(d,W/2,H*.666,sub(),20,GOLD,True)

def traffic(d,t,W,H,level):
    x=W/2;y=H*.27
    # stylized isometric bridge with central lane and moving colored vehicles
    d.polygon([(W*.12,H*.31),(W*.88,H*.31),(W*.99,H*.65),(W*.01,H*.65)],fill=(36,60,80))
    for u in [-.72,-.35,0,.35,.72]:
        d.line((W*(.5+u*.18),H*.31,W*(.5+u*.55),H*.65),fill=(71,115,126),width=2)
    for i in range(7):
        px=W*(.25+.5*i/7);py=H*(.375+.235*((i*.27+t*.18)%1))
        w=(8+17*(py/H));h=w*1.45
        rr(d,(px-w,py-h,px+w,py+h),5,(209,77+int(15*math.sin(i)),78) if i%3 else (87,216,220))
        d.line((px-w*.65,py+h,px+w*.65,py+h),fill=(255,160,134),width=3)
    rr(d,(W*.1,H*.68,W*.9,H*.79),22,(13,50,69),outline=CYAN,width=2)
    centered(d,W*.5,H*.708,head(),25,CYAN,True)
    centered(d,W*.5,H*.753,sub(),18,WHITE,False)

def support(d,t,W,H,level):
    wave=math.sin(t*2.5)*3
    rr(d,(W*.14,H*.235+wave,W*.86,H*.695+wave),24,(20,43,65),outline=(82,104,126),width=2)
    centered(d,W/2,H*.29+wave,head(),23,WHITE,True)
    centered(d,W/2,H*.355+wave,sub(22),20,RED,True)
    for j in range(2):
        y=H*(.44+j*.083)+wave
        rr(d,(W*.23,y,W*.77,y+W*.09),12,(58,51,70) if j==0 else (96,42,57))
        rr(d,(W*.27,y+W*.03,W*.5,y+W*.05),4,(150,140,160))
        txt(d,W*.71,y+W*.018,'!',24,RED,True,'ma')

def refund(d,t,W,H,level):
    x,y=W/2,H*.345;r=W*.12*(1+.02*math.sin(t*3))
    d.ellipse((x-r*1.35,y-r*1.35,x+r*1.35,y+r*1.35),outline=(32,114,116),width=5)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(22,87,79),outline=GREEN,width=7)
    d.line((x-r*.45,y,x-r*.08,y+r*.32),fill=GREEN,width=10,joint='curve')
    d.line((x-r*.08,y+r*.32,x+r*.58,y-r*.35),fill=GREEN,width=10,joint='curve')
    rr(d,(W*.11,H*.51,W*.89,H*.733),22,(13,49,56),outline=(44,112,104),width=2)
    centered(d,W/2,H*.562,head(),34,WHITE,True)
    centered(d,W/2,H*.623,sub(22),20,GREEN,True)
    for i in range(3):
        x=W*(.37+.13*i);yy=H*.69
        d.ellipse((x-9,yy-9,x+9,yy+9),fill=GREEN if (t*2)%4>i*.35 else (61,124,118))

def generic(d,t,W,H,level):
    x,y=W/2,H*.39
    for i in range(6):
        rad=40+i*24+6*math.sin(t+i)
        d.ellipse((x-rad,y-rad,x+rad,y+rad),outline=(28+i*6,91+i*11,111+i*8),width=2)
    centered(d,x,y,head('•'),40,CYAN,True)

def getcue(cues,t):
    for c in cues:
        if c['start']<=t<c['end']:return c
    if t<cues[0]['start']:return cues[0]
    return min(cues,key=lambda c:min(abs(t-c['start']),abs(t-c['end'])))

def bg(W,H):
    y=np.linspace(0,1,H,dtype=np.float32)[:,None]
    x=np.linspace(0,1,W,dtype=np.float32)[None,:]
    arr=np.empty((H,W,3),dtype=np.uint8)
    arr[:,:,0]=np.clip(9+12*y+3*np.sin(x*7+y*3),0,255)
    arr[:,:,1]=np.clip(18+16*y+11*x,0,255)
    arr[:,:,2]=np.clip(33+18*y+18*x,0,255)
    return Image.fromarray(arr,'RGB')

def visual_frame(t,duration,cues,amp,base):
    W,H=base.size;im=base.copy();d=ImageDraw.Draw(im)
    sc=W/540
    cue=getcue(cues,t);k=cue['kind'];local=t-cue['start'];CUE['text']=cue['text']
    # top identity bar
    txt(d,W*.08,H*.05,'KOSIF',26*sc,WHITE,True)
    txt(d,W*.08,H*.083,'VOICE  /  MOTION',12*sc,CYAN,True)
    rr(d,(W*.71,H*.051,W*.93,H*.09),10,(28,58,73))
    centered(d,W*.82,H*.071,f'{int(t):02d}s / {int(round(duration)):02d}s',11*sc,WHITE,True)
    d.line((W*.08,H*.127,W*.92,H*.127),fill=(58,88,99),width=max(1,int(sc)))
    d.line((W*.08,H*.127,W*(.08+.84*t/duration),H*.127),fill=CYAN,width=max(2,int(3*sc)))
    # scene visual itself
    {'weather':weather,'traffic':traffic,'support':support,'refund':refund,'generic':generic}[k](d,t,W,H,amp)
    # Caption box: show estimated phrase highlighted progressively without faking word times
    cap=cue['text'];a=ease(clamp(local/.37));oy=(1-a)*18*sc
    rr(d,(W*.065,H*.819+oy,W*.935,H*.948+oy),20*sc,(19,42,61),outline=(46,99,112),width=2)
    lines=wrap_words(cap,30,3)
    if lines:
        sz=(23 if len(cap)<36 else 18 if len(cap)<75 else 16)*sc
        ys=H*.855+oy
        for i,line in enumerate(lines):
            centered(d,W/2,ys+i*33*sc,line,sz,WHITE,True)
    # audio reactive bars (genuinely drawn from recorded speech energy)
    mid=W/2
    for i in range(23):
        q=(i-11)/11
        hh=(5+amp*25*(.35+.65*(1-abs(q)))+.8*math.sin(i+t*13))*sc
        x=mid+i*W*.024-11*W*.024
        d.line((x,H*.963-hh,x,H*.963),fill=CYAN if amp>.18 else MUTED,width=max(2,int(3*sc)))
    return im

def normalized_audio(audio,target=-14.0):
    """The voice at the delivery loudness (two-pass, linear; timeline._normalize_audio). Returns (file, measured LUFS)."""
    import tempfile
    tmpd=Path(tempfile.mkdtemp(prefix='kosif_v2m_'));raw=tmpd/'voice.wav';out=tmpd/'voice.m4a'
    subprocess.run([FF,'-y','-v','error','-i',str(audio),'-vn','-ac','2','-ar','48000','-c:a','pcm_f32le',str(raw)],check=True,capture_output=True)
    _sys.path.insert(0,str(HERE));import timeline
    return out,timeline._normalize_audio(raw,out,target)

def render(audio,cues,out,fps=24,size=(540,960),preview=False,loudness=-14.0):
    duration=probe_audio(audio);validate_cues(cues,duration)
    if fps not in [12,15,20,24,25,30,60]:raise ValueError('Unsupported FPS')
    W,H=size
    if W<240 or H<320 or W*H>1920*1080:raise ValueError('Unsafe/unsupported render dimensions')
    env=audio_envelope(audio);background=bg(W,H)
    total=math.ceil(duration*fps)
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    measured=None
    if loudness is not None:
        audio,measured=normalized_audio(audio,loudness)
    cmd=[FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','pipe:0','-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t',str(duration),'-movflags','+faststart','-threads','2',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for frame in range(total):
            t=frame/fps;energy=float(env[min(len(env)-1,int(t*50))]);im=visual_frame(t,duration,cues,energy,background)
            proc.stdin.write(im.tobytes())
            if frame%120==0:print(f'RENDER {frame}/{total}',flush=True)
        proc.stdin.close();err=proc.stderr.read().decode(errors='replace');ret=proc.wait()
        if ret:raise RuntimeError('ffmpeg failed: '+err[-1000:])
    except Exception:
        proc.kill();proc.wait();raise
    return {'path':str(out),'duration':duration,'fps':fps,'frames':total,'size':[W,H],'voice_lufs_before':measured,'loudness_target':loudness}

def main(argv=None):
    p=argparse.ArgumentParser(description='KOSIF Voice2Motion — semantic audio-to-motion, offline')
    p.add_argument('audio');p.add_argument('--transcript',help='Text file with transcript (not automatically transcribed)')
    p.add_argument('--cues',help='JSON cue sheet with estimated or independently aligned times')
    p.add_argument('--out',default='KOSIF-Voice2Motion.mp4');p.add_argument('--fps',type=int,default=24)
    p.add_argument('--size',default='540x960');p.add_argument('--plan-only',action='store_true');p.add_argument('--keep-level',action='store_true',help='keep the voice level (no -14 LUFS normalisation)')
    p.add_argument('--plan-out',default=None)
    a=p.parse_args(argv);dur=probe_audio(a.audio)
    if a.cues:
        obj=json.loads(Path(a.cues).read_text(encoding='utf-8'));cues=obj['cues'] if isinstance(obj,dict) else obj
        label=obj.get('timing_quality','provided_timestamps') if isinstance(obj,dict) else 'provided_timestamps'
    elif a.transcript:
        cues=estimate_cues(Path(a.transcript).read_text(encoding='utf-8'),dur);label='estimated_from_text_length_NOT_ASR'
    else:p.error('Provide --cues or --transcript. Automatic ASR unavailable offline; no invented transcript.')
    cues=validate_cues(cues,dur)
    plan={'schema':'kosif.voice2motion.v1','source':str(a.audio),'duration':dur,'timing_quality':label,'cues':cues}
    planp=Path(a.plan_out) if a.plan_out else Path(a.out).with_suffix('.json');planp.parent.mkdir(parents=True,exist_ok=True)
    planp.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8');print('PLAN',planp)
    if a.plan_only:return
    w,h=map(int,a.size.split('x'));print('RESULT',json.dumps(render(a.audio,cues,a.out,a.fps,(w,h),loudness=None if a.keep_level else -14.0)))

if __name__=='__main__':main()
