import {chromium} from "playwright-core";
import {spawn,spawnSync} from "node:child_process";
import {createServer} from "node:http";
import {mkdir,writeFile,readFile,readdir,stat} from "node:fs/promises";
import {existsSync} from "node:fs";
import {join,resolve} from "node:path";
import {makeHandler} from "./server.mjs";
import {DURATION_SECONDS} from "./storyboard.mjs";
const args=process.argv.slice(2);
const value=(name,fallback)=>{const i=args.indexOf(name);return i<0?fallback:args[i+1];};
const out=resolve(value("--out",join(process.cwd(),"threejs-result")));
const fps=Number(value("--fps","12"));
if(!Number.isInteger(fps)||fps<1||fps>30)throw new Error("fps must be 1..30");
const width=720,height=1280;
const chrome=process.env.KOSIF_CHROME||"C:/Program Files/Google/Chrome/Application/chrome.exe";
if(!existsSync(chrome))throw new Error("Chrome missing: set KOSIF_CHROME");
const onlySmoke=args.includes("--smoke");
const frames=onlySmoke?3:Math.round(DURATION_SECONDS*fps);
const server=createServer(makeHandler());
const port=await new Promise((resolve,reject)=>server.listen(0,"127.0.0.1",()=>resolve(server.address().port)).once("error",reject));
let browser;
try{
 browser=await chromium.launch({executablePath:chrome,headless:true,
    args:["--enable-unsafe-swiftshader","--use-gl=angle","--use-angle=swiftshader","--disable-gpu-sandbox"]});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
 const errors=[];page.on("pageerror",e=>errors.push(e.message));
 const response=await page.goto("http://127.0.0.1:"+port+"/?capture=1",{waitUntil:"load"});
 await page.waitForFunction("window.__KOSIF_3D?.ready===true",{timeout:25000});
 const initial=await page.evaluate(()=>window.__KOSIF_3D);
 if(initial.renderer!=="WebGLRenderer")throw new Error("Not actual Three WebGL");
 if(response.status()!==200)throw new Error("HTTP response not 200");
 await mkdir(out,{recursive:true});
 let first,last;
 for(let i=0;i<frames;i++){
    const t=onlySmoke?[0,1.9,4.4][i]:(i/fps);
    const info=await page.evaluate(ms=>window.renderAt(ms),Math.round(t*1000));
    if(info.drawCalls<3||info.triangles<100)throw new Error("WebGL scene empty or incomplete");
    if(!first)first=info;last=info;
    await page.screenshot({path:join(out,"frame_"+String(i).padStart(4,"0")+".png"),type:"png",animations:"disabled"});
 }
 if(errors.length)throw new Error("Browser errors: "+errors.join("; ").slice(0,1000));
 const hashes=[];
 const crypto=await import("node:crypto");
 for(let i of [0,Math.floor(frames/2),frames-1]){
   const buf=await readFile(join(out,"frame_"+String(i).padStart(4,"0")+".png"));
   hashes.push(crypto.createHash("sha256").update(buf).digest("hex"));
 }
 if(new Set(hashes).size<2)throw new Error("Rendered frames identical (motion not verified)");
 const receipt={schema:"kosif.threejs.motion-lab.v1",threeRevision:initial.threeRevision,
    renderer:initial.renderer,verifiedWebGL:true,framesRendered:frames,frameRate:fps,
    durationSeconds:onlySmoke?null:DURATION_SECONDS,frameHashes:hashes,
    firstFrame:first,lastFrame:last,browserErrors:errors,
    ffmpegExport:false,video:null,videoSha256:null,
    videoReference:{id:"CCUSpJkAfgU",title:"Claude + Three.js = Premium 3D Motion Graphics",
       exact_visual_replication_claim:false},
    notes:"Original visuals; tutorial inspiration only. No external media, no user files."};
 if(!onlySmoke){
   const vid=join(out,"kosif-threejs-motion-lab.mp4");
   const ff=spawnSync("ffmpeg",["-hide_banner","-y","-loglevel","error","-framerate",String(fps),
      "-i",join(out,"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","20",
      "-movflags","+faststart","-t",String(DURATION_SECONDS),vid],
      {windowsHide:true,timeout:180000,encoding:"utf8"});
   if(ff.status===0 && existsSync(vid)){
     receipt.ffmpegExport=true;receipt.video="kosif-threejs-motion-lab.mp4";
     receipt.videoSha256=crypto.createHash("sha256").update(await readFile(vid)).digest("hex");
   }else receipt.ffmpegError=(ff.error?.message||ff.stderr||"FFmpeg unavailable").slice(0,500);
 }
 await writeFile(join(out,"receipt.json"),JSON.stringify(receipt,null,2)+"\n");
 console.log(JSON.stringify({out,receipt},null,2));
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
