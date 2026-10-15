import json
from pathlib import Path
base=Path(__file__).resolve().parent
p=base/"build_catalog.py"
t=p.read_text(encoding="utf-8")
t=t.replace('source+"/reference.mp4" if ident in TENS else None','source.replace("/tree/","/blob/")+"/reference.mp4" if ident in TENS else None')
t=t.replace('source+"/preview.jpg" if ident in TENS else None','source.replace("/tree/","/blob/")+"/preview.jpg" if ident in TENS else None')
p.write_text(t,encoding="utf-8")
cat=base/"catalog/styles.json"
data=json.loads(cat.read_text(encoding="utf-8"))
for r in data:
 if r["id"] not in {"plotter","doodle","whiteboard","chalkboard","stickman","isometric","fake3d","infographic","map-journey","product"}: continue
 old=r["video"];new=old.replace("/tree/","/blob/")
 r["video"]=new;r["poster"]=r["poster"].replace("/tree/","/blob/")
 (base/"styles"/r["id"]/"STYLE.json").write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
 sk=base/"styles"/r["id"]/"SKILL.md"
 sk.write_text(sk.read_text(encoding="utf-8").replace(old,new),encoding="utf-8")
cat.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print("fixed",len(data),"and 10 base reference URLs")
