#!/usr/bin/env python3
"""KOSIF original Telegram typography knowledge index, privacy-first.

Reads exported Telegram HTML, images (header metadata only) and local font tables.
NO font files, image files, raw chat message text, sender data or Telegram URLs
are copied into the PUBLIC atlas. Private source paths remain in a separate
LOCAL-ONLY index that must never be committed. No archives or fonts executed.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

TAGS={
 "kufi":("كوفي","كوفى","kufi","kufic","kufiic"),
 "naskh":("نسخ","naskh","nask"),
 "ruqah":("رقعة","الرقعة","ruqaa","ruqah","rukah"),
 "diwani":("ديواني","ديوانى","diwani"),
 "thuluth":("ثلث","thuluth","thulth","tholoth"),
 "maghrebi":("مغربي","مغربى","maghrebi"),
 "geometric":("هندسي","هندسى","geometric","geometry"),
 "calligraphy":("خط عربي","خطوط عربية","خط عربيه","calligraphy","calligraffiti","كاليجرافي"),
 "brush":("فرشاة","فرشه","brush","pen","قلم"),
 "handwritten":("يدوي","يدوى","handwritten","handwriting"),
 "display":("عناوين","بوستر","poster","display","title","typography","تايبو"),
 "logo":("شعار","لوجو","logo","brand","هوية"),
 "bold":("عريض","bold","black","heavy","extrabold"),
 "light":("خفيف","light","thin","hairline"),
 "rounded":("دائري","دائرى","rounded","round"),
 "decorative":("زخرف","ornament","decorative","pattern"),
 "modern":("حديث","مودرن","modern","contemporary"),
 "vintage":("قديم","تراث","vintage","retro","classic"),
 "arabic":("عربي","عربى","arabic","arab","خط"),
 "latin":("latin","english","انجليزي","إنجليزي"),
 "motion":("موشن","motion","animation","تحريك","animated"),
 "3d":("3d","ثري دي","ثلاثي الأبعاد","مجسم"),
 "font_creation":("fontforge","glyphs","fontlab","fonttools","تصميم خط","صناعة الخطوط"),
 "licensing":("license","ترخيص","حقوق استخدام","ofl","copyright","مسموح"),
}
FONT_EXT={".ttf",".otf"}
IMAGE_EXT={".jpg",".jpeg",".png",".webp",".gif"}
ARCHIVE_EXT={".zip",".rar",".7z"}
OMIT_EXT={".js",".css",".html",".pdf"}
ARABIC_SAMPLE="ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
LATIN_SAMPLE="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def sha(path):
    digest=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk=f.read(1<<20)
            if not chunk:break
            digest.update(chunk)
    return digest.hexdigest()

def norm(value):
    return re.sub(r"\s+"," ",value.lower())

def tag_text(s):
    lowered=norm(s)
    return [key for key,needles in TAGS.items() if any(w in lowered for w in needles)]

def clean_name(s):
    if not s:return ""
    s=re.sub(r"[\x00-\x1f]"," ",str(s))
    s=re.sub(r"\b\S+@\S+\.\S+\b","",s)
    s=re.sub(r"(?:\+?\d[\d\-() ]{8,}\d)","",s)
    return re.sub(r"\s+"," ",s).strip()[:95]

def utf_name(font,ids):
    from fontTools.ttLib import TTFont
    names=font["name"] if "name" in font else None
    if not names:return ""
    for ident in ids:
        for rec in names.names:
            if rec.nameID==ident:
                try:
                    s=clean_name(rec.toUnicode())
                    if s:return s
                except Exception:pass
    return ""

def license_hint(font):
    # License string must be explicitly embedded. OS/2 fsType allows embedding
    # but NEVER means the font may legally be redistributed.
    txt=" ".join((utf_name(font,[13]),utf_name(font,[14]))).lower()
    if "open font license" in txt or "scripts.sil.org/ofl" in txt or "openfontlicense" in txt:
        return "OFL-claimed-unverified"
    if "apache" in txt and "license" in txt:
        return "Apache-claimed-unverified"
    if "public domain" in txt:
        return "public-domain-claimed-unverified"
    if "gnu" in txt and ("license" in txt or "gpl" in txt):
        return "GPL-claimed-unverified"
    if txt and ("all rights reserved" in txt or "non-commercial" in txt or "commercial" in txt):
        return "restricted-or-custom-review"
    return "unknown-no-license-proof"

def font_record(path):
    from fontTools.ttLib import TTFont,TTCollection
    item={"bytes":path.stat().st_size,"sha256":sha(path),"extension":path.suffix.lower()}
    try:
        with path.open('rb') as font_input:
            font=TTFont(font_input,lazy=False,recalcBBoxes=False,recalcTimestamp=False)
            try:
                best=font.getBestCmap() or {}
                item["family"]=utf_name(font,[16,1]) or clean_name(path.stem)
                item["style"]=utf_name(font,[17,2]) or "Unknown"
                item["postscript_name"]=utf_name(font,[6])
                item["license_status"]=license_hint(font)
                os2=font["OS/2"] if "OS/2" in font else None
                item["weight_class"]=int(os2.usWeightClass) if os2 else None
                item["embedding_flags"]=int(os2.fsType) if os2 else None
                item["glyphs"]=len(best)
                item["arabic_codepoints"]=sum(0x600<=x<=0x6ff for x in best)
                item["arabic_base_letters_supported"]=sum(ord(x) in best for x in ARABIC_SAMPLE)
                item["latin_basic_letters_supported"]=sum(ord(x) in best for x in LATIN_SAMPLE)
                item["has_arabic"]=item["arabic_codepoints"]>=12
                item["has_latin"]=item["latin_basic_letters_supported"]>=35
                item["variable"]=("fvar" in font)
                item["color_glyphs"]=any(k in font for k in ("COLR","SVG ","CBDT","sbix"))
                item["tags"]=sorted(set(tag_text(item["family"]+" "+item["style"])))
                item["parsed"]=True
            finally:
                font.close()
    except Exception as e:
        item.update(family="",style="",parsed=False,parse_error=type(e).__name__,
                    license_status="uninspected",tags=[])
    # Never automatically permit redistribution based solely on metadata.
    item["redistribution_approved"]=False
    return item

def read_chat(html):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(html.read_text(encoding="utf-8-sig",errors="replace"),"lxml")
    count=0
    themes=Counter()
    links=Counter()
    notes=[]
    for m in soup.select(".message"):
        if "service" in m.get("class",[]):continue
        count+=1
        txt=m.select_one(".text")
        text=txt.get_text(" ",strip=True) if txt else ""
        found=tag_text(text)
        themes.update(found)
        # Resolve only attachment relative paths; NO Telegram profile URLs.
        attached=[]
        for a in m.select("a[href]"):
            link=unquote(a.get("href","")).replace("\\","/")
            if (link.startswith("files/") or link.startswith("photos/")) and ".." not in Path(link).parts:
                attached.append(link)
                links[Path(link).suffix.lower()]+=1
        notes.append({"message_seq":count,"tags":found,"attachments":sorted(set(attached))})
    return {"messages":count,"themes":themes,"linked_extensions":links},notes

def scan(root, public_out, private_out, *, max_fonts=5000):
    from PIL import Image
    root=Path(root).expanduser().resolve()
    public_out=Path(public_out).expanduser().resolve()
    private_out=Path(private_out).expanduser().resolve()
    if public_out==private_out or any(str(p).startswith(str(root)+str(Path("/"))) for p in (public_out,private_out)):
        raise ValueError("outputs must be outside Telegram exports")
    if not root.is_dir():raise ValueError("missing export directory")
    if any(p.exists() or not p.parent.is_dir() for p in (public_out,private_out)):
        raise ValueError("output paths must be new files under existing directories")
    folders=sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("ChatExport"))
    if not folders:raise ValueError("no ChatExport folders")
    aggregate=Counter()
    themes=Counter()
    fonts=[]
    private_fonts=[]
    private_images=[]
    group_stats=[]
    unparsed=[]
    seen=set()
    total_messages=0
    total_attached=Counter()
    for index,folder in enumerate(folders,1):
        files=sorted((p for p in folder.rglob("*") if p.is_file() and not p.is_symlink()),key=lambda p:p.as_posix().lower())
        messages=0
        group_themes=Counter()
        attached=Counter()
        for html in files:
            if html.suffix.lower()!=".html" or not html.name.lower().startswith("messages"):
                continue
            info,records=read_chat(html)
            messages+=info["messages"]
            group_themes.update(info["themes"])
            attached.update(info["linked_extensions"])
            # local only: attachment linkage for follow-up review, no verbatim text
        exts=Counter()
        for p in files:
            kind=p.suffix.lower()
            exts[kind]+=1
            aggregate[kind]+=1
            if kind in FONT_EXT:
                if len(fonts)>=max_fonts:raise ValueError("font safety limit reached")
                record=font_record(p)
                digest=record["sha256"]
                record["catalog_id"]="type-"+digest[:16]
                record["duplicates_another_source"]=digest in seen
                # Don't release proprietary filename or local source path.
                private_fonts.append({"catalog_id":record["catalog_id"],"relative_source":str(p.relative_to(root)),
                                      "sha256":digest,"family":record.get("family")})
                if digest not in seen:
                    fonts.append(record)
                    seen.add(digest)
                if not record.get("parsed"):unparsed.append(record["catalog_id"])
            elif kind in IMAGE_EXT:
                width=height=None
                try:
                    with Image.open(p) as img:
                        width,height=img.size
                except Exception:pass
                # Only private manifest preserves individual image paths.
                private_images.append({"relative_source":str(p.relative_to(root)),
                                       "bytes":p.stat().st_size,"width":width,"height":height})
        total_messages+=messages
        themes.update(group_themes)
        total_attached.update(attached)
        group_stats.append({"export_no":index,"files":len(files),"messages_parsed":messages,
                            "extensions":dict(exts),"themes":dict(group_themes),
                            "attached_filetypes":dict(attached)})
    family=Counter(x.get("family") or "(unparsed)" for x in fonts)
    licenses=Counter(x["license_status"] for x in fonts)
    with_ar=sum(bool(x.get("has_arabic")) for x in fonts)
    with_latin=sum(bool(x.get("has_latin")) for x in fonts)
    ideas=[]
    patterns=[
      ("kufi-grid","شبكة كوفية هندسية","kufi","Square modular strokes, alternate positive/negative space, square Arabic proportions"),
      ("naskh-editorial","نسخ للتحرير","naskh","Balance readability, joining consistency, diacritics and headline-to-body pairing"),
      ("ruqah-personal","رقعة شخصية","ruqah","Casual energetic handwritten joins for invitations and informal visual identity"),
      ("diwani-ceremony","ديواني فاخر","diwani","Ornamental high-contrast lettering for certificates, packaging and luxury"),
      ("thuluth-poster","ثلث للبوسترات","thuluth","Tall sweeping ascenders and decorative hierarchy in heritage compositions"),
      ("arabic-latin-pair","تزاوج عربي لاتيني","latin","Match x-height perception, baseline rhythm and stroke contrast across scripts"),
      ("geometric-logo","شعار هندسي","geometric","Custom minimal letter construction, carefully kerning Arabic and Latin"),
      ("bold-sale","خط دعائي عريض","bold","High-legibility price numerals and weight contrast for promotional posters"),
      ("calligraphy-motion","كالخط المتحرك","motion","Reveal letter shapes by stroke order, preserve connection and RTL timing"),
      ("decorative-ornament","زخرفة حروف","decorative","Build repeatable ornaments from legal original outlines, not third-party font tracing"),
      ("brush-doodle","قلم حر وفرشاة","brush","Ink textures and monoline sketch overlay with original strokes"),
      ("3d-glyph","حروف مجسمة","3d","Extrusion, bevel and physically based shadows using independently authorized glyphs"),
      ("display-editorial","عناوين تحريرية","display","Pair strong display Arabic headlines with accessible readable body type"),
      ("light-product","خط رفيع للمنتجات","light","Delicate labels with adequate small-size readability and WCAG contrast"),
      ("identity-system","نظام هوية طباعية","logo","Construct a restrained type system with reusable spacing and size scale")
    ]
    for key,label,tag,brief in patterns:
        related=[f["catalog_id"] for f in fonts if tag in f.get("tags",[])][:8]
        ideas.append({"id":key,"title_ar":label,"design_brief_en":brief,
                      "source_theme_message_hits":int(themes.get(tag,0)),
                      "related_font_ids":related,
                      "usage":"Design inspiration only; check font license before actual use"})
    public={
      "schema":"kosif.telegram-typography-index.v1",
      "source":"Telegram Desktop exports, local authorized folder",
      "privacy":"No verbatim chats, usernames, URLs, contact data, images, source paths or font bytes in public file",
      "license_policy":"All source fonts withheld; names and name-table license hints DO NOT grant redistribution or usage rights",
      "scan_scope":{"export_folders":len(folders),"files":sum(x["files"] for x in group_stats),
           "messages_parsed":total_messages,"unique_font_binaries":len(fonts),
           "font_files_seen":len(private_fonts),"images_seen":len(private_images),
           "unparsed_font_binaries":len(unparsed),
           "images_semantically_reviewed":0,
           "executable_attachment_files_executed":0,
           "archives_unpacked":0,
           "font_read_only_parsing":True},
      "file_types":dict(aggregate),
      "topic_hits_from_message_text":dict(themes),
      "message_attachment_types":dict(total_attached),
      "script_coverage":{"fonts_with_arabic":with_ar,"fonts_with_latin":with_latin,
                         "unique_font_families":len(family)},
      "font_license_status_counts":dict(licenses),
      "groups":group_stats,
      "fonts":fonts,
      "typography_design_ideas":ideas,
      "limitations":["Photo files were header-scanned for dimensions only; no full image semantic analysis",
                     "ZIP/RAR members and encrypted archives were not recursively inspected",
                     "HTML message text categorized via deterministic tags; no raw excerpts published",
                     "Font name/OS2 embedding permissions are not copyright licenses",
                     "License and original creator permissions must be verified before using or redistributing fonts",
                     "Font matching based on metadata does not replace rendering a glyph proof sheet"]
    }
    private={"schema":"kosif.telegram-typography-private.v1",
             "purpose":"Local-only authorized asset locator, NEVER upload to GitHub",
             "root_path":str(root),"fonts":private_fonts,
             "images":private_images,"groups":group_stats}
    public_out.write_text(json.dumps(public,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    private_out.write_text(json.dumps(private,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return public

def find(catalog, query, limit=15, has_arabic=None):
    q=norm(query).strip()
    if not q:raise ValueError("query required")
    tags=tag_text(q)
    matches=[]
    for font in catalog["fonts"]:
        if has_arabic is not None and bool(font.get("has_arabic"))!=has_arabic:continue
        hay=norm(font.get("family","")+" "+font.get("style",""))
        score=sum(5 for tag in tags if tag in font.get("tags",[]))
        score+=12 if q in hay else sum(2 for word in q.split() if word in hay)
        if score:
            matches.append((score,font))
    matches.sort(key=lambda pair:(-pair[0],-int(pair[1].get("arabic_codepoints",0)),
                                  pair[1].get("family","")))
    return [{"font_id":x["catalog_id"],"family":x.get("family"),
             "style":x.get("style"),"arabic_glyphs":x.get("arabic_codepoints",0),
             "tags":x.get("tags",[]),"license_status":x["license_status"],
             "score":score} for score,x in matches[:limit]]

def font_from_bytes(data, suffix):
    """Parse bounded ZIP font bytes without extracting to filesystem."""
    import io
    from fontTools.ttLib import TTFont
    record={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
            "extension":suffix.lower()}
    try:
        with io.BytesIO(data) as stream:
            font=TTFont(stream,lazy=False,recalcBBoxes=False,recalcTimestamp=False)
            try:
                best=font.getBestCmap() or {}
                record["family"]=utf_name(font,[16,1]) or "Unnamed font"
                record["style"]=utf_name(font,[17,2]) or "Unknown"
                record["postscript_name"]=utf_name(font,[6])
                record["license_status"]=license_hint(font)
                os2=font["OS/2"] if "OS/2" in font else None
                record["weight_class"]=int(os2.usWeightClass) if os2 else None
                record["embedding_flags"]=int(os2.fsType) if os2 else None
                record["glyphs"]=len(best)
                record["arabic_codepoints"]=sum(0x600<=x<=0x6ff for x in best)
                record["arabic_base_letters_supported"]=sum(ord(x) in best for x in ARABIC_SAMPLE)
                record["latin_basic_letters_supported"]=sum(ord(x) in best for x in LATIN_SAMPLE)
                record["has_arabic"]=record["arabic_codepoints"]>=12
                record["has_latin"]=record["latin_basic_letters_supported"]>=35
                record["variable"]="fvar" in font
                record["color_glyphs"]=any(k in font for k in ("COLR","SVG ","CBDT","sbix"))
                record["tags"]=sorted(set(tag_text(record["family"]+" "+record["style"])))
                record["parsed"]=True
            finally:
                font.close()
    except Exception as exc:
        record.update(family="",style="",parsed=False,parse_error=type(exc).__name__,
                      license_status="uninspected",tags=[])
    record["redistribution_approved"]=False
    record["catalog_id"]="type-"+record["sha256"][:16]
    return record

def enrich_zip_archives(root, old_public, old_private, new_public, new_private):
    """Bounded index of ZIP members. No archive contents copied to GitHub."""
    import zipfile
    root=Path(root).expanduser().resolve()
    old_public=Path(old_public).resolve()
    old_private=Path(old_private).resolve()
    new_public=Path(new_public).resolve()
    new_private=Path(new_private).resolve()
    if not all(x.is_file() for x in (old_public,old_private)):
        raise ValueError("base public and private catalogs required")
    if any(x.exists() or not x.parent.is_dir() for x in (new_public,new_private)):
        raise ValueError("new output filenames required")
    public=json.loads(old_public.read_text(encoding="utf8"))
    private=json.loads(old_private.read_text(encoding="utf8"))
    if public.get("schema")!="kosif.telegram-typography-index.v1":
        raise ValueError("incompatible prior catalog")
    if Path(private["root_path"]).resolve()!=root:
        raise ValueError("private locator belongs to another source")
    existing={f["sha256"] for f in public["fonts"]}
    members=Counter();archives=0;bad_archives=0
    excluded=Counter();duplicates=0;new_fonts=0;unparsed=0
    archive_reports=[]
    for z in sorted(root.rglob("*.zip")):
        if not z.is_file() or z.is_symlink():continue
        archives+=1
        archive_entry_count=0;f_count=0;skip_count=0
        try:
            with zipfile.ZipFile(z) as source:
                infos=source.infolist()
                if len(infos)>2500:
                    excluded["oversize_archive_entry_count"]+=1
                    continue
                archive_entry_count=len(infos)
                for m in infos:
                    if m.is_dir():continue
                    ext=Path(m.filename).suffix.lower()
                    members[ext]+=1
                    if ext not in {".ttf",".otf",".woff",".woff2"}:
                        continue
                    f_count+=1
                    # Avoid malicious ZIP bombs, and do not process absolute or
                    # path-traversal members even though nothing is extracted.
                    parts=m.filename.replace("\\","/").split("/")
                    if (m.file_size>15_000_000 or m.file_size<16 or
                        m.compress_size>15_000_000 or
                        m.file_size/max(1,m.compress_size)>120 or
                        any(part in ("..",".") for part in parts) or
                        m.filename.startswith(("/","\\")) or
                        m.flag_bits&1):
                        excluded["unsafe_or_encrypted_member"]+=1;skip_count+=1
                        continue
                    try:
                        data=source.read(m,pwd=None)
                        if len(data)!=m.file_size:
                            raise ValueError("archive member size mismatch")
                        record=font_from_bytes(data,ext)
                        del data
                    except Exception:
                        excluded["read_failure"]+=1;skip_count+=1
                        continue
                    private["fonts"].append({
                      "catalog_id":record["catalog_id"],
                      "archive_relative":str(z.relative_to(root)),
                      "zip_member":m.filename,
                      "sha256":record["sha256"],
                      "family":record.get("family")})
                    if record["sha256"] in existing:
                        duplicates+=1
                    else:
                        existing.add(record["sha256"])
                        public["fonts"].append(record)
                        new_fonts+=1
                        if not record.get("parsed"):unparsed+=1
        except (zipfile.BadZipFile,PermissionError,OSError):
            bad_archives+=1
            excluded["unreadable_zip"]+=1
        archive_reports.append({"archive_id":"zip-"+sha(z)[:12],
                                "entries":archive_entry_count,"font_entries":f_count,
                                "skipped_font_entries":skip_count})
    counts=public["scan_scope"]
    counts.update({"zip_archives_scanned":archives,"zip_archives_unreadable":bad_archives,
      "zip_font_entries_seen":sum(members.get(x,0) for x in (".ttf",".otf",".woff",".woff2")),
      "zip_font_entries_new_unique":new_fonts,"zip_fonts_duplicate_existing":duplicates,
      "zip_font_entries_not_parsed":sum(excluded.values())-bad_archives+unparsed,
      "font_binary_unique_including_zips":len(public["fonts"]),
      "raw_archives_extracted":0})
    public["font_license_status_counts"]=dict(Counter(f["license_status"] for f in public["fonts"]))
    public["script_coverage"]={"fonts_with_arabic":sum(bool(f.get("has_arabic")) for f in public["fonts"]),
                                "fonts_with_latin":sum(bool(f.get("has_latin")) for f in public["fonts"]),
                                "unique_font_families":len(set(f["family"] for f in public["fonts"]))}
    public["archive_inventory"]={"zip_members_by_extension":dict(members),
                                 "unreadable_zip_count":bad_archives,
                                 "safety_exclusions":dict(excluded),
                                 "archive_identifiers":archive_reports,
                                 "does_not_include_rar_fonts":True}
    public["limitations"].append("ZIP font members inspected from bounded memory; archives with errors/unsafe entries excluded; RAR archives were not indexed or extracted")
    public["schema"]="kosif.telegram-typography-index.v2"
    public["fonts"].sort(key=lambda x:(x.get("family") or "",x["sha256"]))
    new_public.write_text(json.dumps(public,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    new_private.write_text(json.dumps(private,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"zip_archives_scanned":archives,"unreadable_zip":bad_archives,
            "font_entries_in_zips":counts["zip_font_entries_seen"],
            "font_added_unique":new_fonts,"duplicates":duplicates,
            "unique_font_binaries":len(public["fonts"]),
            "failed_to_parse_nested_fonts":unparsed,"excluded":dict(excluded)}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    subs=ap.add_subparsers(dest="action",required=True)
    subs.add_parser("doctor")
    s=subs.add_parser("scan")
    s.add_argument("--root",required=True);s.add_argument("--public-out",required=True)
    s.add_argument("--private-out",required=True)
    z=subs.add_parser("enrich-zips")
    for option in ("root","public","private","new-public","new-private"):
        z.add_argument("--"+option,required=True)
    f=subs.add_parser("find")
    f.add_argument("--index",required=True);f.add_argument("query");f.add_argument("--limit",type=int,default=15)
    f.add_argument("--arabic-only",action="store_true")
    args=ap.parse_args()
    try:
        if args.action=="doctor":
            from bs4 import BeautifulSoup
            from fontTools.ttLib import TTFont
            from PIL import Image
            print(json.dumps({"ready":True,"requires":["beautifulsoup4","fonttools","Pillow"],
                 "reads":["export HTML","TTF","OTF","image headers"],"raw_uploads":False}))
        elif args.action=="scan":
            r=scan(args.root,args.public_out,args.private_out)
            print(json.dumps({"scan_scope":r["scan_scope"],"licenses":r["font_license_status_counts"],
                              "design_briefs":len(r["typography_design_ideas"])},ensure_ascii=False))
        elif args.action=="enrich-zips":
            r=enrich_zip_archives(args.root,args.public,args.private,args.new_public,args.new_private)
            print(json.dumps(r,ensure_ascii=False))
        else:
            catalog=json.loads(Path(args.index).read_text(encoding="utf-8"))
            print(json.dumps(find(catalog,args.query,max(1,min(50,args.limit)),
                                  True if args.arabic_only else None),ensure_ascii=False,indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"success":False,"error":str(e)},ensure_ascii=False),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
