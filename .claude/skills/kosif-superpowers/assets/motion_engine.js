/* KOSIF Motion Engine v1 — original deterministic SVG / voice-timed animation.
   Inspired by motion-design concepts; no third-party library source is copied.
   The Python compiler embeds validated JSON in <script type=application/json>.
*/
(() => {
  'use strict';
  const config = JSON.parse(document.getElementById('kosif-data').textContent);
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.getElementById('scene');
  const art = document.getElementById('art');
  const stage = document.getElementById('stage');
  const captions = document.getElementById('captions');
  const bg = document.getElementById('background');
  const state = [];
  const C = x => Math.max(0, Math.min(1, x));
  const lerp = (a,b,t) => a + (b-a) * t;
  const smooth = t => { const v=C(t); return v*v*(3-2*v); };
  const fraction = (t,a,b) => b > a ? smooth((t-a)/(b-a)) : +(t>=a);
  const el = (name, attr={}, parent=art) => {
    const node = document.createElementNS(NS,name);
    for (const [k,v] of Object.entries(attr)) node.setAttribute(k,String(v));
    parent.appendChild(node);
    return node;
  };
  const sceneNodes = config.scenes.map(sc => {
    const layer = el('g',{'data-scene':sc.id},art);
    const entries = (sc.elements || []).map(item => {
      const outer = el('g',{},layer);
      const inner = el('g',{},outer);
      let drawable = [];
      if (item.type === 'path') {
        drawable=[el('path',{d:item.d,stroke:item.stroke || '#172824',
          'stroke-width': item.strokeWidth || 6,fill:'none',
          'stroke-linecap':'round','stroke-linejoin':'round'},inner)];
      } else if (item.type === 'circle') {
        drawable=[el('circle',{cx:item.x,cy:item.y,r:item.r,
          stroke:item.stroke || '#172824','stroke-width':item.strokeWidth || 6,
          fill:item.fill || 'none'},inner)];
      } else if (item.type === 'text') {
        const t = el('text',{x:item.x,y:item.y,fill:item.fill || '#172824',
          'font-size':item.fontSize || 58,'text-anchor':item.anchor || 'middle',
          direction:item.direction || 'rtl'},inner);
        t.textContent=item.text;
        drawable=[t];
      } else if (item.type === 'character') {
        const p=el('g',{transform:'translate('+item.x+' '+item.y+') scale('+(item.scale||1)+')'},inner);
        const paths=[
          'M0 -95 C-27 -95 -34 -65 -28 -42 C-24 -18 24 -18 28 -42 C34 -65 25 -95 0 -95',
          'M0 -18 L0 94','M0 8 L-53 57','M0 8 L53 57',
          'M0 94 L-37 168','M0 94 L37 168',
          'M-12 -63 L-10 -63','M12 -63 L14 -63','M-9 -43 Q0 -34 10 -43'
        ];
        drawable=paths.map((d,i)=>el('path',{d,fill:'none',stroke:item.stroke||'#172824',
          'stroke-width':i<6?7:4,'stroke-linecap':'round'},p));
      }
      const pathLen=drawable.map(d=>{
        try { return typeof d.getTotalLength==='function' ? d.getTotalLength() : 0; }
        catch { return 0; }
      });
      return {item,outer,inner,drawable,pathLen};
    });
    return {sc,layer,entries};
  });
  function tick(t) {
    const sec = C(t / config.duration) * config.duration;
    const current = config.scenes.find(s => sec >= s.start && sec < s.end)
      || config.scenes[config.scenes.length-1];
    bg.setAttribute('fill',current.background || '#f4f0e6');
    sceneNodes.forEach(({sc,layer,entries})=>{
      const shown=sc.id===current.id;
      layer.style.display=shown?'':'none';
      if (!shown) return;
      entries.forEach(({item,outer,inner,drawable,pathLen})=>{
        const start=item.start === undefined ? sc.start : item.start;
        const end=item.end === undefined ? sc.end : item.end;
        const reveal=fraction(sec,start,end);
        const movement=item.move || {};
        const mt=fraction(sec,movement.start===undefined?end:movement.start,
                              movement.end===undefined?sc.end:movement.end);
        const x=lerp(movement.fromX||0,movement.toX||0,mt);
        const y=lerp(movement.fromY||0,movement.toY||0,mt);
        const wobble=item.type==='character' && sec>=end && sec<=sc.end ?
          Math.sin((sec-end)*7)*Math.min(6,Math.max(0,(sec-end)*8)) : 0;
        outer.setAttribute('transform','translate('+x+' '+(y+wobble)+')');
        inner.setAttribute('opacity',String(item.type==='text' ? reveal : 1));
        for (let i=0;i<drawable.length;i++) {
          const node=drawable[i],len=pathLen[i];
          if (len>0) {
            node.style.strokeDasharray=String(len+2);
            node.style.strokeDashoffset=String((len+2)*(1-reveal));
          } else {
            node.style.opacity=String(reveal);
          }
        }
      });
    });
    const camera=current.camera || {};
    const prog=fraction(sec,camera.start===undefined?current.start:camera.start,
                             camera.end===undefined?current.end:camera.end);
    const zoom=lerp(camera.fromZoom||1,camera.toZoom||1,prog);
    const tx=lerp(camera.fromX||0,camera.toX||0,prog);
    const ty=lerp(camera.fromY||0,camera.toY||0,prog);
    const cx=config.width/2,cy=config.height/2;
    stage.setAttribute('transform',
      'translate('+tx+' '+ty+') translate('+cx+' '+cy+') scale('+zoom+') translate('+(-cx)+' '+(-cy)+')');
    // Captions always follow the supplied word timestamps, not a guessed reading speed.
    captions.replaceChildren();
    const group = (current.words || []).filter(w=>w.start<=sec && w.end>sec);
    if (group.length) {
      const w=group[0];
      const backdrop=el('rect',{x:60,y:config.height-260,width:config.width-120,
        height:145,rx:24,fill:'#172824','fill-opacity':'.88'},captions);
      const txt=el('text',{x:config.width/2,y:config.height-166,
        'font-size':Math.min(66,Math.max(30,config.width/(w.text.length*.78+4))),
        'font-weight':'700','text-anchor':'middle',direction:'rtl',fill:'#fff'},captions);
      txt.textContent=w.text;
    }
    return {time:sec,scene:current.id,word:group[0]?.text||null};
  }
  window.__kosif={duration:config.duration,fps:config.fps,seek:tick,source:'KOSIF Motion Engine v1'};
  window.__kosifReady=document.fonts.ready;
  tick(0);
})();