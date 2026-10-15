import concurrent.futures, json, re, time, html, hashlib
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent
HOST="https://www.promptsmotion.com"
HEADERS={"User-Agent":"KOSIF TOOL public-reference catalog/1.0"}
CATEGORIES={
 "Product UI":"Recreate responsive interface states as independent layers; animate meaningful cursor, click, modal, scroll and focus interactions using consistent depth and realistic timings.",
 "Phone":"Use 3D phone layers with realistic screen perspective, shadow, touch interaction, rotating camera and device-safe crops.",
 "Charts":"Use truthful data, animated counters, bars, lines and chart morphs whose labels remain accurate; show axes and readable legends.",
 "Diagrams":"Reveal diagram nodes by causal order; animate SVG edges with dash offsets and show relationships with intentional camera moves.",
 "Kinetic type":"Animate readable words in timed beats; synchronize word-level emphasis to spoken voice, preserve shaping and RTL for Arabic.",
 "Shapes":"Draw SVG geometry and morph compatible paths; animate scale, squash/stretch, rotation and easing with controlled geometry.",
 "Particles":"Use deterministic seeded particles with controlled emitters, fields, attraction and decay that support story meaning.",
 "Characters":"Use consistent character model sheets and rigs, key poses, expressive face animation, walk cycles, anticipation and follow-through.",
 "Photos":"Use original or licensed photos in layered camera rigs with planar parallax, dynamic masking and depth-aware transitions.",
 "Music":"Sync scene shifts and motion accents to measured musical beats without overpowering narration.",
 "Code":"Build genuine time-varying vector/HTML/Canvas/React motion, not a slideshow of generated stills."
}
BASIC="""plotter|قلم البلوتر|الرسم اليدوي
doodle|قصص الدودل|الرسم اليدوي
whiteboard|سبورة بيضاء|الرسم اليدوي
chalkboard|سبورة طباشير|الرسم اليدوي
stickman|شخصيات عصوية|الشخصيات
isometric|عالم أيزومتريك|3D
fake3d|عمق 2.5D|3D
infographic|إنفوجرافيك|بيانات
map-journey|رحلة على الخريطة|بيانات
product|إعلان إطلاق منتج|إعلانات
kinetic-arabic|تايبوغرافي عربي|خطوط
subtitle-punch|كلمات متحركة|خطوط
typewriter|آلة كتابة|خطوط
editorial|مونتاج تحريري|خطوط
viral-mixed-media|مونتاج مختلط|إعلانات
glass-ui|واجهة زجاجية|واجهات
ui-micro|واجهات دقيقة|واجهات
saas-demo|استعراض SaaS|واجهات
scroll-world|عالم تمرير|3D
higgsfield-journey|جولة سينمائية|3D
claymation|صلصال متحرك|الشخصيات
cutout-paper|قصاصات ورقية|الرسم اليدوي
stop-motion|ستوب موشن|الشخصيات
frame-by-frame|إطار بإطار|الرسم اليدوي
character-rig|تحريك هيكلي|الشخصيات
anime-action|أنمي أكشن|الشخصيات
pixel-art|بيكسل آرت|الشخصيات
lowpoly-3d|مجسمات Low Poly|3D
cinematic-3d|مشاهد 3D سينمائية|3D
parallax-2d|بارالاكس|3D
neon-tech|نيون تقني|إعلانات
retrowave|ريترو|إعلانات
minimal|مينيمال|خطوط
brutalist|بروتالي|خطوط
liquid-morph|أشكال سائلة|3D
morph-charts|تحولات بيانات|بيانات
chart-race|سباق رسوم|بيانات
audio-wave|موجة صوت|بيانات
documentary-map|خريطة وثائقية|بيانات
logo-reveal|كشف شعار|إعلانات
ecommerce-ad|إعلان متجر|إعلانات
handwriting-reveal|كتابة يدوية|الرسم اليدوي
whiteboard-cinematic|وايتبورد سينمائي|الرسم اليدوي
comics-panels|لوحات كوميكس|الشخصيات
tech-blueprint|رسومات تقنية|بيانات"""
SOURCES=[
"https://github.com/motalim-ai/motion-starter-kit",
"https://github.com/latent-spaces/brag",
"https://github.com/oso95/scroll-world",
"https://github.com/elayadesign/ai-design-skills",
"https://github.com/midudev/mcp-higgsfield-landing",
"https://github.com/heygen-com/hyperframes",
"https://github.com/kosif199022-jpg/kosif-one",
"https://github.com/kosif199022-jpg/fastify-motion-bro",
"https://github.com/kosif199022-jpg/kosif-studio",
"https://github.com/kosif199022-jpg/kosif-render-lab",
"https://github.com/kosif199022-jpg/kosif-omni",
"https://github.com/kosif199022-jpg/100-superskills"]
TENS=set("plotter doodle whiteboard chalkboard stickman isometric fake3d infographic map-journey product".split())
def load(url):
 r=requests.get(url,headers=HEADERS,timeout=25)
 r.raise_for_status()
 return BeautifulSoup(r.text,"html.parser")

def gather():
 soup=load(HOST)
 hrefs=[]
 for a in soup.select("a[href]"):
  path=a.get("href","")
  if re.fullmatch(r"/[A-Za-z0-9_-]+-[a-f0-9]{6}",path) and path not in hrefs: hrefs.append(path)
 print("Catalog URLs",len(hrefs),flush=True)
 def detail(href):
  url=HOST+href
  try:
   s=load(url); h=s.select_one("h1"); v=s.select_one("video")
   if not h:return None
   following=h.find_next_sibling()
   tags=[x.get_text(" ",strip=True) for x in following.select("span")] if following else []
   tags=[t for t in tags if t in CATEGORIES]
   x=next((a.get("href") for a in h.parent.select("a[href]") if "x.com/" in a.get("href","")),None)
   creator="@"+x.split("/")[3] if x and x.count("/")>=3 else "unknown"
   return {"id":"pm-"+href[1:],"name":h.get_text(" ",strip=True),"category":tags,"creator":creator,"creator_url":x,"page":url,"video":urljoin(HOST,v.get("src")) if v and v.get("src") else None,"poster":urljoin(HOST,v.get("poster")) if v and v.get("poster") else None,"origin":"PromptsMotion"}
  except Exception as e:
   return {"id":"pm-"+href[1:],"name":href[1:],"category":[],"creator":"unverified","page":url,"video":None,"poster":None,"origin":"PromptsMotion","fetch_error":str(e)}
 records=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(detail,x) for x in hrefs]
  for i,f in enumerate(futures):
   rec=f.result()
   if rec:records.append(rec)
   if (i+1)%50==0:print("Inspected",i+1,"/",len(futures),flush=True)
 return records

def make_skill(r):
 name=r["name"];tags=r.get("category",[])
 tactics="\n".join("* "+CATEGORIES[t] for t in tags if t in CATEGORIES)
 if not tactics:tactics="* Develop original choreography using the linked reference; verify actual imagery before claiming a match."
 return f"""---
name: {r['id']}
description: Create a new video using the motion design language referenced at this catalog entry.
---

# KOSIF TOOL — {name}

## Primary motion reference
Page: {r.get('page')}
Video URL: {r.get('video') or 'See source page'}
Credit: {r.get('creator','unknown')}.

Observe this exact reference before implementing when browser/video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, character acting, palette and typography. If you cannot watch it, disclose that; this production guide alone does not prove exact visual similarity.

## Original creative direction
Produce a NEW video featuring the user's own concept, voice or video footage, inspired by this example. Categories: {', '.join(tags) or 'creative motion'}.
{tactics}
* Start with a consistent geometry system and original design tokens (document measured or estimated colors, type, line weights, easing and camera).
* Give every scene an audio interval and visual action. Plan creation order, camera movement, transition and sound cue at sentence or phrase granularity.
* All visuals must animate: draw paths in sequence, move rigged characters when appropriate, and reveal information causally. Static slideshow transitions are not acceptable.
* Build editable and deterministic animation using Remotion/React and SVG/Canvas, or choose Three.js for true spatial scenes, then export via available render tools. Do not imply integrations that are not installed.
* Default 9:16, 1080x1920, 30 fps, H.264 MP4. Respect user's aspect ratio, duration, branding and timeline.
* Treat existing AUDIO as master time: preserve voice; transcribe, align words and animate to verified timestamps. Target <= 100 ms on key words only when measured and checked.
* For source VIDEO, preserve its authorized material and align the motion treatment to real cuts, actions and phrases. For TEXT, create short narration and a timestamped scene plan.
* Arabic requires RTL shaping and typography safe for small screens. Never split joined letters to animate them.
* Animate entrances 0.25–0.6 seconds, accents 0.12–0.3 seconds and transitions 0.3–0.8 seconds as initial estimates only; refine after inspecting the reference.
* Preserve legibility, deliberate visual hierarchy, emotional pacing and performance.

## Claude production runbook
1. Read repository CLAUDE.md, AGENTS.md, STYLE_INDEX.md and the present skill.
2. Open source page and watch/inspect video where possible; do not copy it into this repository.
3. Gather user's already supplied assets; ask at most one batch of necessary questions.
4. Write STYLE.md with reference observations versus unverified assumptions, and PLAN.md with scene-by-scene timing, acting, camera and audio cues.
5. Create original assets and editable code. Use music/SFX only if requested or provided/licensed.
6. Preview at multiple timestamps and compare against reference; correct deviations in motion mechanics and timing.
7. Show preview before final render unless the user explicitly preauthorized rendering.
8. Render and verify MP4 size, fps, audio stream and duration; include editable source files.

## Attribution
Reference and creator are linked above. Original third-party videos, text prompts, assets and music are not redistributed or claimed as KOSIF-owned.
"""
def write(path,content):
 p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding="utf-8")

def main():
 records=gather()
 for line in BASIC.splitlines():
  ident,name,cat=line.split("|")
  source=("https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/"+ident) if ident in TENS else ("https://github.com/kosif199022-jpg/kosif-one")
  record={"id":ident,"name":name,"category":[cat],"page":source,"video":(source.replace("/tree/","/blob/")+"/reference.mp4" if ident in TENS else None),"poster":(source.replace("/tree/","/blob/")+"/preview.jpg" if ident in TENS else None),"creator":"KOSIF + attributed sources","origin":"KOSIF original style"}
  records.insert(0,record)
 assert len(records)>=250,f"Only {len(records)} records found, aborting"
 for i,r in enumerate(records):
  write(f"styles/{r['id']}/SKILL.md",make_skill(r))
  write(f"styles/{r['id']}/STYLE.json",json.dumps(r,ensure_ascii=False,indent=2))
 write("catalog/styles.json",json.dumps(records,ensure_ascii=False,indent=2))
 write("catalog/prompts_motion.json",json.dumps([r for r in records if r["origin"]=="PromptsMotion"],ensure_ascii=False,indent=2))
 write("STYLE_INDEX.md","# KOSIF TOOL Style Index\n\nUse IDs verbatim when addressing Claude. Open the video reference in the style folder.\n\n"+"".join(f"- [{r['id']}](styles/{r['id']}/SKILL.md) — {r['name']} — [reference]({r['page']})\n" for r in records))
 write("AGENTS.md","""# KOSIF TOOL Agent Guide

1. Identify the user-requested style ID using STYLE_INDEX.md or catalog/styles.json.
2. Read styles/<id>/SKILL.md and STYLE.json in full. Follow the execution runbook.
3. Open the referenced source page and video if tools permit; never claim to have seen video you could not access.
4. Create fresh original assets and animation; no redistribution of external clips or prompts.
5. For user-supplied audio align actions and narration timings. For a user video study cuts, movement and voice first.
6. Output STYLE.md, PLAN.md, source scene files, preview, test report and rendered MP4 after approval.
7. Preserve licenses, content rights, source attribution, secrets and platform terms.
8. If a style appears as an external-only example, use its prompt as a creative brief, not proof of an existing tested implementation.
""")
 write("CLAUDE.md","""# Claude entry point
Read AGENTS.md, STYLE_INDEX.md and the selected styles/<style-id>/SKILL.md + STYLE.json. Inspect the source video when your tools allow. Produce editable real motion graphics (not static slides). Preserve user's audio and synchronize to word timing when provided. Preview before final rendering. Do not copy third-party videos, text prompts, code or media without a compatible license.
""")
 write("README.md",f"""# KOSIF TOOL — Motion Graphics Style Atlas

A Claude-readable library of **{len(records)} motion style entries**: {len(records)-45} externally linked PromptsMotion demonstrations plus 45 KOSIF curated style profiles. These are reference-based instructions, not guaranteed pre-built render engines.

Open [visual catalog](index.html) or [style index](STYLE_INDEX.md).

## Usage with Claude Code
Share this repository and say:
Read CLAUDE.md and AGENTS.md. Apply style ID pm-stephanlivera-df17a2 to my attached audio. Inspect its reference video when possible, then follow its original KOSIF SKILL.md. Show an animated preview and render after I approve.

## Attribution and source policy
- Do not rehost third-party video, thumbnails, paid prompts, voice or music. Links point to owners' websites.
- The detailed SKILL.md files here are original KOSIF instructions, not copied PromptsMotion prompts.
- An externally linked example is not a claim that the exact animation has been coded or validated.
- Verify source terms before redistributing source code. PromptsMotion: https://www.promptsmotion.com/terms
- Catalog references were indexed from public metadata; source entries can change.

## Related repositories
"""+ "\n".join("- "+url for url in SOURCES)+"\n")
 write(".nojekyll","")
 print("WROTE",len(records),"entries and files",flush=True)
if __name__=="__main__": main()
