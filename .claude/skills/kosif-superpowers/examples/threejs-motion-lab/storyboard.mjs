export const DURATION_SECONDS = 5;
export const FPS_DEFAULT = 12;
export const CUES = Object.freeze([
  Object.freeze({start:0,end:1.65,kicker:"IDEAS INTO REALITY",headline:"DEPTH",caption:"From a single thought to an immersive scene."}),
  Object.freeze({start:1.65,end:3.4,kicker:"DESIGNED IN MOTION",headline:"MOTION",caption:"Camera, light and geometry move as one."}),
  Object.freeze({start:3.4,end:5,kicker:"THE NEXT CREATIVE TOOLKIT",headline:"KOSIF",caption:"THREE.JS  /  CINEMATIC ENGINE"}),
]);
export function sceneAtSeconds(seconds) {
  if (!Number.isFinite(seconds)) throw new TypeError("seconds must be finite");
  const t = Math.max(0, Math.min(DURATION_SECONDS,seconds));
  const cueIndex = Math.min(CUES.length-1,CUES.findIndex((x)=>t<x.end)<0?CUES.length-1:CUES.findIndex((x)=>t<x.end));
  const cue=CUES[cueIndex];
  const progress=t/DURATION_SECONDS;
  return {time:t,progress,cueIndex,kicker:cue.kicker,headline:cue.headline,caption:cue.caption,
    orbitRadians:Math.PI*2*progress,
    cameraZ:9.6-1.45*Math.sin(Math.PI*progress),
    cameraX:.45*Math.sin(Math.PI*2*progress),
    lightIntensity:110+35*Math.sin(Math.PI*progress),
    accentHue:(.105+.018*Math.sin(Math.PI*2*progress)),
  };
}
