import * as THREE from "three";
import {DURATION_SECONDS, sceneAtSeconds} from "./storyboard.mjs";
const width=720,height=1280;
const stage=document.getElementById("stage");
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x071016);
scene.fog=new THREE.FogExp2(0x071016,.029);
const camera=new THREE.PerspectiveCamera(31,width/height,.1,100);
camera.position.set(0,0,9.6);camera.lookAt(0,0,0);
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:"low-power"});
renderer.setSize(width,height,false);
renderer.setPixelRatio(1);
renderer.setClearColor(0x071016,1);
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.55;
stage.prepend(renderer.domElement);
const group=new THREE.Group();scene.add(group);
const gold=new THREE.MeshPhysicalMaterial({color:0xb98a42,metalness:.86,roughness:.21,clearcoat:1,clearcoatRoughness:.12,emissive:0x4a2609,emissiveIntensity:.24});
const ivory=new THREE.MeshPhysicalMaterial({color:0xc7c9ba,metalness:.92,roughness:.24,clearcoat:.8});
const blue=new THREE.MeshPhysicalMaterial({color:0x1a4a5d,metalness:.68,roughness:.23,transparent:true,opacity:.85,side:THREE.DoubleSide});
const center=new THREE.Mesh(new THREE.IcosahedronGeometry(.94,3),gold);
group.add(center);
const knot=new THREE.Mesh(new THREE.TorusKnotGeometry(1.24,.17,180,18,2,3),ivory);
knot.rotation.set(.6,.4,.2);group.add(knot);
const ring=new THREE.Mesh(new THREE.TorusGeometry(2.17,.039,16,180),gold);
ring.rotation.x=.61;ring.rotation.y=.19;group.add(ring);
const wideRing=new THREE.Mesh(new THREE.TorusGeometry(2.6,.012,8,144),blue);
wideRing.rotation.x=1.22;wideRing.rotation.y=.4;group.add(wideRing);
const satelliteGroup=new THREE.Group();group.add(satelliteGroup);
for(let i=0;i<11;i++){
  const angle=i*(Math.PI*2/11);
  const s=.055+(i%3)*.025;
  const sphere=new THREE.Mesh(new THREE.SphereGeometry(s,14,10),i%2?gold:ivory);
  sphere.position.set(Math.sin(angle)*2.52,Math.cos(angle)*1.76,(i%2)*.42-.26);
  satelliteGroup.add(sphere);
}
const seed=763;
let k=seed;const random=()=>((k=(1664525*k+1013904223)>>>0)/4294967296);
const positions=new Float32Array(450*3);
for(let i=0;i<450;i++){positions[i*3]=(random()-.5)*14;positions[i*3+1]=(random()-.5)*23;positions[i*3+2]=-3+(random()-.5)*9;}
const starsGeo=new THREE.BufferGeometry();starsGeo.setAttribute("position",new THREE.BufferAttribute(positions,3));
const stars=new THREE.Points(starsGeo,new THREE.PointsMaterial({color:0xe7bd73,size:.035,opacity:.63,transparent:true,sizeAttenuation:true}));
scene.add(stars);
const ambient=new THREE.AmbientLight(0x8190af,2.6);scene.add(ambient);
const warm=new THREE.PointLight(0xf2b56b,90,20,2);warm.position.set(-4,3,3);scene.add(warm);
const cool=new THREE.PointLight(0x72c8ed,80,20,2);cool.position.set(3,-2,5);scene.add(cool);
const rim=new THREE.DirectionalLight(0xffffff,3.4);rim.position.set(0,5,-3);scene.add(rim);
const clip=new THREE.AnimationClip("turntable",DURATION_SECONDS,[new THREE.NumberKeyframeTrack(".rotation[y]",[0,DURATION_SECONDS],[0,Math.PI*2])]);
const mixer=new THREE.AnimationMixer(center);mixer.clipAction(clip).play();
const h=document.getElementById("headline");const kicker=document.getElementById("micro");const caption=document.getElementById("caption");const bar=document.getElementById("progress");const clock=document.getElementById("time");
const clock0=performance.now();
const tracking={renderedFrames:0,initialFrames:[],clickedObjects:0};
function renderAt(ms){
  const s=sceneAtSeconds(ms/1000);
  mixer.setTime(s.time);
  group.rotation.y=s.orbitRadians*.78;
  group.rotation.z=Math.sin(s.time*1.2)*.14;
  ring.rotation.x=.61+Math.sin(s.time*1.5)*.25;
  wideRing.rotation.y=.4+s.time*.44;
  knot.rotation.x=.6+s.time*.31;
  knot.rotation.y=.4+s.time*.18;
  satelliteGroup.rotation.z=-s.orbitRadians*.8;
  stars.rotation.y=s.time*.009;
  camera.position.set(s.cameraX,Math.sin(s.time*.38)*.22,s.cameraZ);
  camera.lookAt(0,.45,0);
  warm.intensity=s.lightIntensity;
  h.textContent=s.headline;kicker.textContent=s.kicker;caption.textContent=s.caption;
  bar.style.width=(s.progress*100).toFixed(2)+"%";
  clock.textContent="00:"+String(Math.floor(s.time)).padStart(2,"0")+" / 00:05";
  renderer.render(scene,camera);
  tracking.renderedFrames++;
  if(tracking.initialFrames.length<8)tracking.initialFrames.push({time:s.time,headline:s.headline});
  return {time:s.time,headline:s.headline,progress:s.progress,sceneObjects:scene.children.length,
     meshes:group.children.filter(x=>x.isMesh).length,drawCalls:renderer.info.render.calls,
     triangles:renderer.info.render.triangles,renderedFrames:tracking.renderedFrames};
}
const raycaster=new THREE.Raycaster();
stage.addEventListener("pointerdown",e=>{
 if(new URLSearchParams(location.search).has("capture"))return;
 const rect=renderer.domElement.getBoundingClientRect();
 const x=((e.clientX-rect.left)/rect.width)*2-1;const y=-((e.clientY-rect.top)/rect.height)*2+1;
 raycaster.setFromCamera(new THREE.Vector2(x,y),camera);
 const selection=raycaster.intersectObjects([center,knot,ring],false);
 if(selection.length){tracking.clickedObjects++;caption.textContent="OBJECT SELECTED · INTERACTIVE 3D";}
});
window.renderAt=renderAt;
window.__KOSIF_3D={ready:true,renderer:"WebGLRenderer",threeRevision:THREE.REVISION,
   duration:DURATION_SECONDS,features:["Scene","PerspectiveCamera","MeshPhysicalMaterial","AnimationMixer","Raycaster","PBR","procedural-particles"],tracking};
renderAt(0);
if(!new URLSearchParams(location.search).has("capture")){
 const tick=()=>{renderAt((performance.now()-clock0)% (DURATION_SECONDS*1000));requestAnimationFrame(tick)};
 requestAnimationFrame(tick);
}else{document.body.dataset.capture="1";}
