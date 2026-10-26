/* MIDNIGHT / A twelve-second hand-authored 2.5D short. No external assets. */
(function(root){
'use strict';
const DURATION=12,W=1280,H=720,TAU=Math.PI*2;
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const smooth=v=>{v=clamp(v);return v*v*(3-2*v)};
const lerp=(a,b,t)=>a+(b-a)*t;
const n=v=>Number(v).toFixed(2);
const rnd=i=>{const v=Math.sin(i*127.1+311.7)*43758.5453123;return v-Math.floor(v)};
const rect=(x,y,w,h,fill,extra='')=>`<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" fill="${fill}" ${extra}/>`;
const path=(d,fill,extra='')=>`<path d="${d}" fill="${fill}" ${extra}/>`;
const line=(x,y,x2,y2,c,w=1,op=1)=>`<path d="M${n(x)} ${n(y)}L${n(x2)} ${n(y2)}" fill="none" stroke="${c}" stroke-width="${w}" opacity="${op}"/>`;
const neon=(d,c,w=3)=>path(d,'none',`stroke="${c}" stroke-width="${w*7}" opacity=".045" stroke-linecap="round"`)+path(d,'none',`stroke="${c}" stroke-width="${w*3}" opacity=".12" stroke-linecap="round"`)+path(d,'none',`stroke="${c}" stroke-width="${w}" stroke-linecap="round"`)+path(d,'none',`stroke="#f2ffff" stroke-width="${w*.24}" opacity=".85" stroke-linecap="round"`);
const defs=`<defs>
<linearGradient id="sky" x2="0" y2="1"><stop stop-color="#030915"/><stop offset=".6" stop-color="#11293a"/><stop offset="1" stop-color="#3d4561"/></linearGradient>
<radialGradient id="moon"><stop stop-color="#a9d7ce" stop-opacity=".33"/><stop offset=".28" stop-color="#509eac" stop-opacity=".12"/><stop offset="1" stop-color="#173b51" stop-opacity="0"/></radialGradient>
<radialGradient id="cyanHalo"><stop stop-color="#28eee5" stop-opacity=".2"/><stop offset="1" stop-color="#18bfc7" stop-opacity="0"/></radialGradient>
<radialGradient id="roseHalo"><stop stop-color="#ff4566" stop-opacity=".23"/><stop offset="1" stop-color="#ee235a" stop-opacity="0"/></radialGradient>
<radialGradient id="lampHalo"><stop stop-color="#ffe3a4" stop-opacity=".45"/><stop offset=".17" stop-color="#ffd378" stop-opacity=".10"/><stop offset="1" stop-color="#ffd378" stop-opacity="0"/></radialGradient>
<linearGradient id="street" x2="0" y2="1"><stop stop-color="#17343f"/><stop offset=".22" stop-color="#152b36"/><stop offset="1" stop-color="#030b16"/></linearGradient>
<linearGradient id="fur" x1="0" y1="0" x2=".4" y2="1"><stop stop-color="#ffbb66"/><stop offset=".4" stop-color="#e78836"/><stop offset="1" stop-color="#9e442e"/></linearGradient>
<linearGradient id="head" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffc681"/><stop offset=".5" stop-color="#ed963f"/><stop offset="1" stop-color="#b85532"/></linearGradient>
<linearGradient id="leg" x2=".8" y2="1"><stop stop-color="#e79745"/><stop offset="1" stop-color="#b3522b"/></linearGradient>
<linearGradient id="tail" x2="0" y2="1"><stop stop-color="#ffb75e"/><stop offset="1" stop-color="#b76030"/></linearGradient>
<linearGradient id="vignette"><stop stop-color="#020611" stop-opacity=".8"/><stop offset=".17" stop-color="#020611" stop-opacity="0"/><stop offset=".8" stop-color="#020611" stop-opacity="0"/><stop offset="1" stop-color="#020611" stop-opacity=".75"/></linearGradient>
<linearGradient id="reflection" x2="0" y2="1"><stop stop-color="#e18843" stop-opacity=".19"/><stop offset="1" stop-color="#44d9d8" stop-opacity="0"/></linearGradient>
<linearGradient id="beam" x2="0" y2="1"><stop stop-color="#ffe4a3" stop-opacity=".06"/><stop offset="1" stop-color="#ffe4a3" stop-opacity="0"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="screen"><rect width="1280" height="720"/></clipPath>
</defs>`;
function skyline(){let s='';for(let i=0;i<30;i++){const x=i*91-130,h=105+rnd(i+3)*235,w=62+rnd(i+18)*46,y=432-h;s+=rect(x,y,w,h,i%2?'#10222f':'#0b1c2a');s+=line(x+w,y,x+w,433,'#386273',1,.4);if(i%3===0)s+=line(x+w*.7,y,x+w*.7,y-28,'#1d3b4a',2);for(let r=0;r<h/19-1;r++)for(let c=0;c<w/14-1;c++){if(rnd(i*883+r*23+c)>.43)s+=rect(x+8+c*14,y+12+r*19,3.5,6,rnd(i+r+c)>.5?'#4b99a2':'#9c976e',`opacity="${.15+rnd(c+r*9)*.4}"`);}}return s}
const farSky=skyline();
function architecture(){let s='';for(let i=0;i<12;i++){const x=i*214-360,w=200,h=250+rnd(i+991)*230,y=485-h;s+=rect(x,y,w,h,i%2?'#10232d':'#0b1824');s+=rect(x+10,y+14,w-20,h-14,'#142630');s+=rect(x+w-28,y,28,h,'#0a151f');s+=line(x,y,x+w,y,'#486572',2,.6);for(let r=0;r<9;r++){const wy=y+25+r*43;if(wy>431)break;for(let c=0;c<4;c++){const wx=x+23+c*39,lit=rnd(i*30+r*41+c)>.37;s+=rect(wx,wy,23,28,lit?'#255367':'#06121e');if(lit){s+=rect(wx+2,wy+2,19,24,(i+r+c)%3?'#51a7b1':'#cf9563',`opacity="${.13+rnd(r+c)*.28}"`);s+=line(wx+11,wy,wx+11,wy+28,'#0e2836',2);s+=line(wx,wy+14,wx+23,wy+14,'#0e2836',2);}s+=line(wx-2,wy+30,wx+26,wy+30,'#1e3946',3);}}
for(let v=0;v<4;v++)s+=line(x+8,490-v*9,x+w-7,490-v*9,'#1f3b44',1,.6);
if(i%2===0){s+=rect(x+36,y-20,57,20,'#0c1a26');for(let l=0;l<4;l++)s+=line(x+40,y-16+l*4,x+87,y-16+l*4,'#294352',1);}
s+=path(`M${x+12} ${y+15}V450q0 12 10 12h30`,'none','stroke="#263c45" stroke-width="5"');}
// Street level shopfronts, hand-drawn signage and layered awnings.
s+=rect(350,300,223,205,'#112b32');s+=rect(365,340,191,150,'#0a161e');for(let q=0;q<4;q++)s+=rect(370+q*46,347,39,137,'#27494a');s+=rect(374,350,174,129,'#f3a565','opacity=".08"');
s+=rect(347,297,234,34,'#10212b');s+=neon('M365 315h194','#32e9cf',2);s+=`<text x="458" y="318" text-anchor="middle" fill="#b5ffdf" font-family="sans-serif" font-size="13" letter-spacing="6">LATE NIGHT</text>`;
s+=path('M353 340l-20 30h264l-22-30Z','#18373d');for(let i=0;i<8;i++)s+=path(`M${357+i*28} 340l-14 30h12l13-30Z`,'#255256');s+=line(333,371,597,371,'#579a8e',3,.6);
s+=rect(800,340,255,165,'#171e2c');s+=rect(820,363,90,139,'#08131d');s+=rect(925,363,109,105,'#1c3847');for(let j=0;j<5;j++)s+=line(925,380+j*18,1034,380+j*18,'#527981',1,.5);s+=rect(929,368,101,94,'#ff9762','opacity=".08"');
s+=rect(804,295,246,42,'#13202a');s+=neon('M813 302h226v29H813z','#fc5f70',2);s+=`<text x="926" y="322" text-anchor="middle" fill="#ffad9c" font-family="sans-serif" font-weight="700" font-size="15" letter-spacing="5">MOON / CAT</text>`;
s+=rect(760,210,43,168,'#142333','rx="8"');s+=neon('M768 219h27v151h-27z','#fb536f',2);s+=`<text x="782" y="249" text-anchor="middle" fill="#ffb8a3" font-family="sans-serif" font-size="19">M</text><text x="782" y="282" text-anchor="middle" fill="#ffb8a3" font-family="sans-serif" font-size="19">O</text><text x="782" y="315" text-anchor="middle" fill="#ffb8a3" font-family="sans-serif" font-size="19">O</text><text x="782" y="349" text-anchor="middle" fill="#ffb8a3" font-family="sans-serif" font-size="19">N</text>`;
s+=rect(1300,292,186,218,'#091924');s+=rect(1310,325,167,156,'#17313c');for(let a=0;a<8;a++)s+=line(1314,332+a*18,1472,332+a*18,'#2c535e',1);s+=neon('M1320 302h143','#00dacd',3);
// Fire escapes and utility cables.
for(let y=164;y<400;y+=65){s+=line(1080,y,1190,y,'#040e18',5);s+=line(1084,y-20,1084,y,'#122f3d',3);s+=line(1190,y-20,1190,y,'#122f3d',3);s+=path(`M1090 ${y}l85 65`,'none','stroke="#071823" stroke-width="6"');for(let k=0;k<8;k++)s+=line(1094+k*11,y+6+k*7,1115+k*11,y+6+k*7,'#254653',2);}
s+=path('M-300 150Q300 265 815 165T1900 170M-250 169Q310 284 845 183T1950 183','none','stroke="#08131c" stroke-width="3"');
return s}
const midBuildings=architecture();
function streetProps(){let s='';// bike
s+=`<g transform="translate(220 484)" stroke="#29515a" stroke-width="4" fill="none"><circle cx="0" cy="0" r="27"/><circle cx="88" cy="0" r="27"/><path d="M0 0l27-43 25 43H0l42-31 10 31 30-48M88 0 77-49h18M24-44H41"/></g>`;
// Lamps
for(const x of [54,1275,1900]){s+=path(`M${x} 530V219q0-20 20-20h37`,'none','stroke="#04101b" stroke-width="10"');s+=line(x+3,222,x+3,526,'#355461',2,.7);s+=rect(x+39,199,34,7,'#fcebbd','rx="3"');s+=`<ellipse cx="${x+57}" cy="205" rx="122" ry="113" fill="url(#lampHalo)"/>`;s+=path(`M${x+40} 207l-80 325h231l-119-325Z`,'url(#beam)');}
// bollards and planters
for(let i=0;i<4;i++){let x=100+i*474;s+=rect(x,473,11,61,'#0a1923','rx="4"');s+=rect(x,482,11,5,'#61b1b5','opacity=".55"');s+=`<ellipse cx="${x+5}" cy="537" rx="24" ry="4" fill="#040c16" opacity=".7"/>`;}
s+=rect(1132,475,98,61,'#14272f','rx="5"');s+=rect(1141,484,80,39,'#0c1b23');for(let i=0;i<12;i++){let x=1144+i*6;s+=path(`M${x} 477q${-30+rnd(i)*60} -30 ${-20+rnd(i+3)*45} ${-40-rnd(i+1)*50}`,'none','stroke="#1b554b" stroke-width="7" stroke-linecap="round"');}
return s}
const props=streetProps();
function pose(time){const t=clamp(time,0,12);let x=430,walk=0,jump=0,crouch=0,angle=0,phase=0;
if(t<4.1){x=430+59*t;walk=1;phase=t*TAU*1.12;}
else if(t<5.2){x=671.9;phase=4.1*TAU*1.12;crouch=14*smooth((t-4.65)/.55);}
else if(t<6.9){let u=(t-5.2)/1.7;x=lerp(671.9,1050,u);jump=147*4*u*(1-u);angle=lerp(-14,12,u);phase=4.1*TAU*1.12;}
else if(t<7.35){x=1050+24*(t-6.9);crouch=18*Math.sin((t-6.9)/.45*Math.PI);phase=0;}
else if(t<9.7){x=1060.8+48*(t-7.35);walk=1;phase=(t-7.35)*TAU*.98;}
else{x=1173.6;phase=2.35*TAU*.98;}
return {t,x,walk,jump,crouch,angle,phase};}
function limb(hx,phase,far,front,p){let fx=hx,fy=-p.crouch-(p.walk?2*Math.cos(phase*2):Math.sin(p.t*2)*.6);const u=((phase/TAU)%1+1)%1;
if(p.walk){if(u<.6){fx=hx+25-(u/.6)*50;}else{let v=(u-.6)/.4;fx=hx-25+50*smooth(v);fy-=21*Math.sin(v*Math.PI);}}
let hy=-65+p.crouch*.4;
if(p.jump>0){const u=(p.t-5.2)/1.7;fx=hx+(front?1:-1)*(18+26*Math.sin(Math.PI*u));fy=-28-28*Math.sin(Math.PI*u)+(front?-10:9);hy=-61;}
if(p.crouch){fx+=front?12:-14;}
const ky=(hy+fy)*.52, kx=(hx+fx)*.5+(front?-13:20),col=far?'#944b32':'url(#leg)',paw=far?'#c89b69':'#f3cd98';
let s=path(`M${n(hx)} ${n(hy)}Q${n(kx)} ${n(ky)} ${n(fx)} ${n(fy-10)}`,'none',`stroke="${col}" stroke-width="${front?19:23}" stroke-linecap="round"`);
s+=path(`M${n(fx-4)} ${n(fy-7)}q12-2 17 4q3 5-6 6h-14q-6-2-2-10Z`,paw);s+=path(`M${n(fx+7)} ${n(fy-1)}v3m4-4v4`,'none','stroke="#8a5039" stroke-width="1"');
if(!far){s+=path(`M${n(kx-7)} ${n(ky+8)}l13 1m-11 8 10 1`,'none','stroke="#823c28" stroke-width="3.5" stroke-linecap="round" opacity=".7"');s+=path(`M${n(hx-7)} ${n(hy)}Q${n(kx-7)} ${n(ky)} ${n(fx-6)} ${n(fy-12)}`,'none','stroke="#fbc584" stroke-width="1.8" opacity=".4"');}
return s}
function cat(p,reflection=false){let {t,phase:ph}=p;const bob=p.walk?2*Math.cos(ph*2):Math.sin(t*2)*.6,bodyY=p.crouch+bob,tail=12*Math.sin(t*2.2)+3*Math.sin(t*5),look=smooth((t-9.7)/.7),attention=smooth((t-4.1)/.3)*(1-smooth((t-5.0)/.2));
let s=`<g transform="translate(0 ${n(bodyY)}) rotate(${n(p.angle)} 0 -64)">`;
s+=path(`M-67-79C-135 ${n(-95-tail)} -127 ${n(-158-tail)} -183 ${n(-146-tail)}Q-204 ${n(-138-tail)} -199 ${n(-116-tail)}`,'none','stroke="#583430" stroke-width="27" stroke-linecap="round"');
s+=path(`M-67-79C-135 ${n(-95-tail)} -127 ${n(-158-tail)} -183 ${n(-146-tail)}Q-204 ${n(-138-tail)} -199 ${n(-116-tail)}`,'none','stroke="url(#tail)" stroke-width="22" stroke-linecap="round"');
s+=path(`M-168 ${n(-149-tail)}q-15-1-21 6M-139 ${n(-139-tail)}l-11 11M-120 ${n(-119-tail)}l-14 8M-199 ${n(-119-tail)}q-1-7 2-11`,'none','stroke="#77402d" stroke-width="9" opacity=".82"');
s+=path(`M-77-84C-128 ${n(-101-tail)} -132 ${n(-158-tail)} -182 ${n(-153-tail)}`,'none','stroke="#4ad5c9" stroke-width="2" opacity=".5"');
s+=limb(-54,ph+Math.PI,true,false,p)+limb(54,ph,true,true,p);
s+=path('M-81-58Q-104-94-60-117Q-37-131 8-116Q37-112 66-119Q88-111 91-76Q77-47 45-37Q0-27-41-40Q-76-29-81-58Z','url(#fur)','stroke="#663628" stroke-width="2"');
s+=path('M-63-51Q-1-20 50-46Q70-63 83-81Q75-38 46-31Q-1-19-43-36Z','#c7793b','opacity=".55"');
s+=path('M27-53Q50-51 72-70L75-96Q68-117 56-119Q45-93 27-53Z','#f5cb8d','opacity=".74"');
s+=path('M-76-93Q-38-130 5-114Q35-112 55-117','none','stroke="#87ebce" stroke-width="2.4" opacity=".75"');
s+=path('M-46-118q12 16 8 27M-19-119q11 12 7 25M7-113q10 8 8 19M-68-96q9 2 19 13M-72-80q10 1 17 9','none','stroke="#8f4128" stroke-width="8" stroke-linecap="round" opacity=".82"');
s+=limb(-60,ph,false,false,p)+limb(57,ph+Math.PI,false,true,p);
// Collar with small pendant.
s+=path('M65-117Q86-113 92-91','none','stroke="#123e4f" stroke-width="10"');s+=path('M65-118Q86-114 92-91','none','stroke="#63dbd2" stroke-width="2"');s+=`<circle cx="89" cy="-80" r="5" fill="#fed88f"/><circle cx="88" cy="-81" r="1.5" fill="#fff3b6"/>`;
// Head movement: attentive lift and final three-quarter glance.
s+=`<g transform="translate(${n(75-look*4)} ${n(-120-attention*9)}) rotate(${n(-attention*10+look*6)})">`;
s+=path('M-28-24L-33-66Q-31-72-25-66L-1-39L22-43L44-69Q49-72 48-62L45-16Z','#d98740','stroke="#693929" stroke-width="2"');
s+=path('M-23-34L-26-57 -6-38M28-34L41-58 39-26','#a66267');s+=path('M-23-46l-3-12 8 10M36-42l5-16-1 16','none','stroke="#ecc4a2" stroke-width="2"');
s+=path('M-40-17Q-43-48-10-49Q21-55 44-31Q52-22 48-9L64 1Q67 11 56 19L45 22Q39 42 8 43Q-20 42-31 29L-46 27 -37 16 -49 11 -40 4Z','url(#head)','stroke="#6a3a2c" stroke-width="1.8"');
s+=path('M-39-17Q-42-47-11-49Q17-55 37-39','none','stroke="#87e4bf" stroke-width="2.1" opacity=".72"');
s+=path('M15 12Q29-2 42 6Q51 2 59 8Q66 17 48 27Q31 45 8 34Q1 23 15 12Z','#f4d5a6');s+=path('M-22 26Q-10 34 8 33L21 43Q-8 53-26 33Z','#e6b679');
s+=path('M-7-46l5 18m13-20-1 17m15-12-6 13M-34-9l13 5M-35 2l12 3','none','stroke="#944125" stroke-width="5" stroke-linecap="round"');
const blink=(t>2.44&&t<2.56)||(t>9.9&&t<10.06)||(t>11.3&&t<11.45);let eyes='';
if(blink){eyes=path('M17-11q8 6 16-1','none','stroke="#273138" stroke-width="3.5" stroke-linecap="round"');if(look>.1)eyes+=path('M-13-9q5 5 11 0','none','stroke="#273138" stroke-width="3"');}
else{eyes=path('M13-13Q23-22 35-13Q29-1 18-3Z','#eff6be','stroke="#384a36" stroke-width="2"');eyes+=`<ellipse cx="${n(27-look*5)}" cy="-11" rx="3.1" ry="7" fill="#164f47"/><ellipse cx="${n(28-look*5)}" cy="-11" rx="1.5" ry="6" fill="#0b151e"/><circle cx="${n(28-look*5)}" cy="-14" r="1.8" fill="#fff"/>`;if(look>.1)eyes+=`<g opacity="${n(look)}"><path d="M-16-9q7-9 15 0q-5 10-12 4Z" fill="#dbeaaf" stroke="#465039" stroke-width="1.5"/><ellipse cx="-6" cy="-8" rx="2.7" ry="6" fill="#18483e"/><circle cx="-5" cy="-10" r="1.3" fill="#fff"/></g>`;}
s+=eyes;
s+=path('M54 8l10-2q3 5-4 9Z','#684039');s+=path('M59 15q-1 8-13 7','none','stroke="#734b3a" stroke-width="1.6"');s+=path('M48 22l25-1M45 27l27 6M17 20l-28 0M18 26l-27 7','none','stroke="#cfe5d1" stroke-width="1.25" opacity=".8"');
for(let k=0;k<18;k++){const x=-28+rnd(k)*53,y=-30+rnd(k+50)*62;s+=line(x,y,x+2.4,y+2,'#ffd7a0',.8,.28);}
s+='</g></g>';return s;}
function butterfly(t,p){const x=p.x+185-90*smooth((t-9.2)/1.9),y=348-20*Math.sin(t*1.8)-48*smooth((t-4.2)/1.8)+55*smooth((t-7)/2);const wing=Math.abs(Math.sin(t*TAU*4.5))*.85+.13;return `<g transform="translate(${n(x)} ${n(y)})"><circle r="28" fill="url(#cyanHalo)"/><g transform="scale(${n(wing)} 1)"><path d="M0 0C-22-22-33-14-17 1C-28 18-7 13 0 1M0 0C22-22 33-14 17 1C28 18 7 13 0 1" fill="#86fff0" opacity=".87"/></g><path d="M-1-6l2 13" stroke="#f0fff2" stroke-width="2"/></g>`;}
function rain(t,cam,near=false){let s='',count=near?32:152;for(let i=0;i<count;i++){const speed=near?630:340+rnd(i)*260,len=near?37:11+rnd(i+22)*14,base=rnd(i+617)*1800;let x=((base-t*95-cam*(near?.1:.03))%1450+1450)%1450-60,y=(rnd(i+271)*880+t*speed)%850-60;s+=line(x,y,x-6-len*.2,y+len,near?'#95d6df':'#86b7c9',near?1.3:.8,near?.17:.13);}return s;}
function ground(t,cam,p){let s=rect(-300,506,2650,250,'url(#street)');s+=rect(-300,506,2650,9,'#2a4650');s+=line(-300,519,2350,519,'#548086',1,.43);s+=line(-300,531,2350,531,'#07141f',4,.9);
// Perspective paving joints.
for(let i=-5;i<19;i++){const x=i*170;s+=line(x,532,x-180,740,'#55747a',1,.09);}
for(let j=0;j<6;j++){let y=541+j*j*8;s+=line(-300,y,2350,y,'#7da0a3',1,.06);}
// Broad coloured wet light, then broken horizontal reflections.
s+=`<ellipse cx="918" cy="576" rx="188" ry="66" fill="url(#roseHalo)"/><ellipse cx="461" cy="559" rx="201" ry="82" fill="url(#cyanHalo)"/>`;
for(let i=0;i<85;i++){const x=250+rnd(i+6)*1250,y=534+rnd(i+390)*155,w=4+rnd(i+29)*64,rose=x>760&&x<1110;s+=line(x+Math.sin(t*2+i)*3,y,x+w+Math.sin(t*2+i)*3,y,rose?'#f86879':'#62c9c6',1+rnd(i+4)*2,.025+rnd(i+145)*.10);}
// Puddle being jumped over.
s+=path('M714 550Q772 538 834 544T982 559Q997 581 932 586L754 581Q711 575 714 550Z','#0a222d','stroke="#356271" stroke-width=".8" opacity=".9"');s+=path('M734 557Q850 545 967 563M752 576Q862 586 959 572','none','stroke="#68bac5" stroke-width="1" opacity=".36"');
for(let i=0;i<20;i++){const u=(t*.65+rnd(i+603))%1,x=200+rnd(i+761)*1550,y=540+rnd(i+522)*107;s+=`<ellipse cx="${n(x)}" cy="${n(y)}" rx="${n(5+u*24)}" ry="${n(1+u*4)}" fill="none" stroke="${i%3?'#76d7dc':'#f6978e'}" stroke-width=".7" opacity="${n((1-u)*.19)}"/>`;}
// Reflection of hero, distorted into a soft elongated silhouette.
s+=`<ellipse cx="${n(p.x)}" cy="570" rx="128" ry="24" fill="url(#reflection)"/><ellipse cx="${n(p.x)}" cy="543" rx="${n(97-p.jump*.19)}" ry="${n(10-p.jump*.025)}" fill="#020915" opacity="${n(.5-p.jump*.0015)}"/>`;
return s;}
function splash(t,p){let s='';const events=[{at:5.2,x:675},{at:6.9,x:1050},{at:7.53,x:1070},{at:8.02,x:1093},{at:8.55,x:1120},{at:9.1,x:1145}];for(const e of events){const a=t-e.at;if(a<0||a>.63)continue;for(let j=0;j<11;j++){let vx=(rnd(j+30)-.5)*210,vy=-(45+rnd(j+87)*84),x=e.x+vx*a,y=540+vy*a+145*a*a;s+=`<ellipse cx="${n(x)}" cy="${n(y)}" rx="${n(1.8*(1-a/.8))}" ry="${n(2.8*(1-a/.8))}" fill="#91e2df" opacity="${n((1-a/.63)*.7)}"/>`;}s+=`<ellipse cx="${e.x}" cy="542" rx="${n(4+a*75)}" ry="${n(1+a*12)}" fill="none" stroke="#94e3df" stroke-width="1" opacity="${n(.45*(1-a/.63))}"/>`;}
return s;}
function sceneSVG(time){const p=pose(time),t=p.t,cam=lerp(0,630,smooth(t/12)),zoom=1+.10*smooth(t/12);let s=`<svg width="1280" height="720" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="An orange tabby explores a rainy neon city and leaps over a puddle">${defs}<g clip-path="url(#screen)">${rect(0,0,W,H,'url(#sky)')}`;
s+=`<circle cx="${n(941-cam*.035)}" cy="148" r="345" fill="url(#moon)"/><circle cx="${n(941-cam*.035)}" cy="148" r="34" fill="#acd3cf" opacity=".42"/><path d="M760 135q130-33 352 6" fill="none" stroke="#102737" stroke-width="27" opacity=".68"/>`;
s+=`<g transform="translate(${n(-cam*.19)} 0)">${farSky}</g>`;
s+=`<path d="M0 405Q610 345 1280 421V542H0Z" fill="#416978" opacity=".085"/>`;
s+=`<g transform="translate(${n(640*(1-zoom))} ${n(500*(1-zoom))}) scale(${n(zoom)})"><g transform="translate(${n(-cam*.68)} 0)">${midBuildings}`;
// Floating neon glows and a quiet scanning sign.
s+=`<ellipse cx="777" cy="285" rx="183" ry="248" fill="url(#roseHalo)" opacity="${n(.76+.07*Math.sin(t*5))}"/><ellipse cx="469" cy="359" rx="181" ry="138" fill="url(#cyanHalo)"/>`;
s+=`<g opacity="${n(.45+.25*Math.sin(t*1.4))}">${neon('M1334 356h20m8 0h20m8 0h20m8 0h20','#68ebed',1.7)}</g></g>`;
s+=`<g transform="translate(${n(-cam)} 0)">${ground(t,cam,p)}${props}`;
// Hero reflection, visible but dark and rippled.
s+=`<g transform="translate(${n(p.x)} ${n(551+p.jump*.13)}) scale(1 -.25)" opacity=".085">${cat(p,true)}</g>`;
s+=`<g transform="translate(${n(p.x)} ${n(538-p.jump)})">${cat(p)}</g>${splash(t,p)}${butterfly(t,p)}</g></g>`;
s+=rain(t,cam,false);
// Foreground alley edges move faster than the background, creating depth.
let fgx=-cam*1.38;s+=`<g transform="translate(${n(fgx)} 0)"><path d="M-160 0H35V720h-195Z" fill="#020712"/><path d="M42 0V720" stroke="#153041" stroke-width="6"/><path d="M49 30V695" stroke="#32707a" stroke-width="1.8" opacity=".35"/><path d="M2020 0h270v720h-270z" fill="#020812" opacity=".8"/><path d="M2040 0v720" stroke="#1f3e48" stroke-width="7"/></g>`;
s+=rain(t,cam,true);s+=rect(0,0,W,H,'url(#vignette)');
// Film frame, an understated title, and tiny cinematic wayfinding.
s+=rect(0,0,1280,36,'#020711');s+=rect(0,684,1280,36,'#020711');s+=`<text x="55" y="63" fill="#bdd8d9" opacity=".63" font-family="sans-serif" font-size="9" letter-spacing="3">KOSIF MOTION / ORIGINAL SHORT</text><text x="1225" y="63" text-anchor="end" fill="#82aab5" opacity=".65" font-family="monospace" font-size="10">12 SEC • 24 FPS</text>`;
let title=1-smooth((t-2.2)/1.0);s+=`<g opacity="${n(title)}"><text x="88" y="139" fill="#dcebe5" font-family="sans-serif" font-size="43" font-weight="300" letter-spacing="10">MIDNIGHT</text><text x="91" y="165" fill="#84afb5" font-family="sans-serif" font-size="10" letter-spacing="4">A LITTLE COURAGE. A VERY BIG CITY.</text><path d="M92 183h49" stroke="#ed9f64" stroke-width="2"/></g>`;
let end=smooth((t-10.4)/.7);s+=`<g opacity="${n(end)}"><text x="95" y="175" fill="#dcebe5" font-family="sans-serif" font-size="29" font-weight="300" letter-spacing="6">FOLLOW THE LIGHT.</text><text x="97" y="201" fill="#87aeb5" font-family="sans-serif" font-size="10" letter-spacing="3">EVERY ADVENTURE STARTS WITH ONE STEP.</text></g>`;
s+='</g></svg>';return s;}
const api={DURATION,sceneSVG,pose};if(typeof module!=='undefined')module.exports=api;root.CinematicCat=api;
})(typeof window!=='undefined'?window:globalThis);
