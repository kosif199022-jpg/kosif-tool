export function seekMedia(record,target){if(record.element.seeking){record.pendingSeek=target;return false;}record.pendingSeek=null;record.element.currentTime=target;return true;}
export function flushPendingSeek(record){if(record.pendingSeek==null)return false;const target=record.pendingSeek;record.pendingSeek=null;if(Math.abs(record.element.currentTime-target)<.025)return false;return seekMedia(record,target);}
export function releaseMedia(record){record.element.pause?.();record.source?.disconnect();record.gain?.disconnect();URL.revokeObjectURL(record.url);record.element.removeAttribute?.('src');record.element.load?.();}
export function withinByteBudget(records,nextSize,limit=500*1024*1024){return [...records].reduce((sum,r)=>sum+(r.size||0),0)+nextSize<=limit;}
export function matchesAsset(record,asset){return !!record && !!asset && record.type===asset.type && record.fileKey===`${asset.name}:${asset.size}:${asset.lastModified}`;}
export function connectAudio(record,context,destination){if(record.type==='image'||record.source)return;record.element.volume=1;record.element.muted=false;record.source=context.createMediaElementSource(record.element);record.gain=context.createGain();record.gain.gain.value=0;record.source.connect(record.gain);record.gain.connect(context.destination);record.gain.connect(destination);}
export function stableSeek(record,isActive=()=>true,timeout=8000){
 return new Promise((resolve,reject)=>{
  const element=record.element;
  const timer=setTimeout(()=>finish(new Error('انتهت مهلة تجهيز موضع الفيديو. أعد المحاولة.')),timeout);
  function finish(error){clearTimeout(timer);element.removeEventListener('seeked',check);element.removeEventListener('error',failed);error?reject(error):resolve(isActive());}
  function failed(){finish(new Error('تعذرت قراءة الفيديو أثناء تجهيز التصدير.'));}
  function check(){if(!isActive()){finish();return;}if(record.pendingSeek!=null&&flushPendingSeek(record))return;if(!element.seeking&&record.pendingSeek==null)finish();}
  element.addEventListener('seeked',check);element.addEventListener('error',failed);check();
 });
}
