# Per shot: trim, retime (speed), pre-crop a 9:16 band with margin, motion-interpolate to 60 fps.
import json,subprocess,sys
c=json.load(open("build/shots.json"))
def probe(p):
    o=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height,r_frame_rate","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip().split(",")
    n,d=o[2].split("/"); return int(o[0]),int(o[1]),float(n)/float(d)
for s in c["shots"]:
    if len(sys.argv)>1 and s["id"] not in sys.argv[1:]: continue
    W,H,fps=probe(s["src"]); cam=s["cam"]
    zmin=min(cam["z0"],cam["z1"])
    cw=H/zmin*9/16
    xs=[cam["c0"][0]*W,cam["c1"][0]*W]
    x0=max(0,int(min(xs)-cw/2*1.12)); x1=min(W,int(max(xs)+cw/2*1.12)); bw=(x1-x0)//2*2
    s["band"]=[x0,0,bw,H]
    dur=(s["end"]-s["start"]+0.8)
    scale="scale=-2:2160," if H>2160 else ""
    vf=f"crop={bw}:{H}:{x0}:0,{scale}setpts=PTS/{s['speed']}"
    if abs(fps-60)>0.5 or s["speed"]!=1.0: vf+=",minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
    else: vf+=",fps=60"
    out=f"build/shot_{s['id']}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s["in"]),"-t",str(dur*s["speed"]+0.3),"-i",s["src"],"-vf",vf,"-t",str(dur),"-an","-c:v","libx264","-crf","10","-preset","fast","-pix_fmt","yuv420p",out],check=True)
    print(s["id"],W,H,round(fps,2),"band",s["band"],flush=True)
json.dump(c,open("build/shots.json","w"),indent=1,ensure_ascii=False)
