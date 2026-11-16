# -*- coding: utf-8 -*-
"""
Media Hunter - بحث فائق السرعة في 615 موقع ميديا للمونتاج.

الأوامر:
  build                         يبني الفهرس (catalog.db) من الكتالوج وقوالب البحث
  sites  "q" [--type] [--free]  أنسب المواقع للطلب + رابط بحث جاهز لكل موقع (أجزاء من الثانية)
  search "q" [--type] [...]     بحث حي متوازي في كل مصادر الـ API مرة واحدة ويرجع ملفات حقيقية
  links  "q" [--type]           صفحة HTML فيها روابط البحث في كل المواقع المناسبة
  hunt   "q" [--type]           search + sites في JSON واحد (الأمر الأساسي لـ Claude)
  get    1 3 5 [-o DIR]         تحميل نتايج من آخر search بالرقم + تسجيل المصدر في sources.txt
  keys                          حالة مفاتيح الـ API الاختيارية
  sources                       قائمة مصادر البحث الحي
"""
import argparse, asyncio, csv, glob, html, json, os, re, sqlite3, subprocess, sys, time
from urllib.parse import quote, quote_plus, urlparse

import httpx

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
# Mutable state (index, 24h cache, last results, keys.json) lives outside the repository.
CACHE = os.environ.get("MH_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "kosif-media-hunter")
os.makedirs(CACHE, exist_ok=True)
OUT_ROOT = os.environ.get("MH_OUT") or os.path.join(os.getcwd(), "out", "media-hunter")
DB = os.path.join(CACHE, "catalog.db")
LAST = os.path.join(CACHE, "last_results.json")
CATALOG_CSV = os.path.join(HERE, "data", "media_sites_615.csv")
UA = "MediaHunter/1.0 (local montage research tool; +https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia) httpx/0.28"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

# ---------------------------------------------------------------- keys
def load_keys():
    keys = {}
    for p in (os.path.join(HERE, "keys.json"), os.path.join(CACHE, "keys.json")):
        if os.path.exists(p):
            keys.update(json.load(open(p, encoding="utf-8")))
    for k in ["PEXELS_API_KEY", "PIXABAY_API_KEY", "UNSPLASH_ACCESS_KEY", "GIPHY_API_KEY",
              "EUROPEANA_API_KEY", "SI_API_KEY"]:
        if os.environ.get(k):
            keys[k] = os.environ[k]
    return keys
KEYS = load_keys()

# ---------------------------------------------------------------- arabic helpers
AR_RE = re.compile(r"[؀-ۿ]")
def norm_ar(s):
    s = re.sub(r"[ً-ْـ]", "", s or "")
    return s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")

AR2EN = {
 "بحر":"sea","محيط":"ocean","موج":"waves","امواج":"waves","شاطئ":"beach","صحراء":"desert","رمل":"sand",
 "جبل":"mountain","جبال":"mountains","غابه":"forest","شجر":"trees","نهر":"river","شلال":"waterfall",
 "مطر":"rain","عاصفه":"storm","برق":"lightning","سحاب":"clouds","غيوم":"clouds","سماء":"sky","ثلج":"snow",
 "غروب":"sunset","شروق":"sunrise","ليل":"night","نجوم":"stars","قمر":"moon","شمس":"sun","فضاء":"space",
 "مجره":"galaxy","كوكب":"planet","ارض":"earth","مدينه":"city","شارع":"street","زحمه":"traffic","مرور":"traffic",
 "مباني":"buildings","برج":"tower","ناطحات":"skyscrapers","طريق":"road","عربيه":"car","سياره":"car",
 "طياره":"airplane","طائره":"airplane","قطار":"train","سفينه":"ship","مركب":"boat","درون":"drone",
 "جوي":"aerial","تصوير جوي":"aerial","بطيء":"slow motion","سلو موشن":"slow motion","تايم لابس":"timelapse",
 "ناس":"people","شخص":"person","راجل":"man","رجل":"man","ست":"woman","امراه":"woman","طفل":"child",
 "اطفال":"children","عيله":"family","اسره":"family","زحام":"crowd","جمهور":"crowd","شباب":"young people",
 "رياضه":"sport","كوره":"football","كره القدم":"football","ملعب":"stadium","جري":"running","ملاكمه":"boxing",
 "سباحه":"swimming","جيم":"gym","خيل":"horse","حصان":"horse","جمل":"camel","اسد":"lion","نسر":"eagle",
 "صقر":"falcon","طيور":"birds","طير":"bird","قطه":"cat","كلب":"dog","سمك":"fish","حيوانات":"animals",
 "ورد":"flowers","زهور":"flowers","نار":"fire","دخان":"smoke","انفجار":"explosion","ماء":"water","مياه":"water",
 "مسجد":"mosque","جامع":"mosque","كعبه":"kaaba","مكه":"mecca","قران":"quran","صلاه":"prayer","رمضان":"ramadan",
 "فانوس":"lantern","اهرامات":"pyramids","هرم":"pyramid","مصر":"egypt","القاهره":"cairo","النيل":"nile",
 "فرعوني":"ancient egypt","فراعنه":"pharaoh","اثار":"ancient ruins","تاريخ":"history","تاريخي":"historical",
 "قديم":"vintage","ارشيف":"archive","حرب":"war","جيش":"army","جندي":"soldier","علم":"flag","احتفال":"celebration",
 "فرح":"wedding","زفاف":"wedding","عيد":"festival","العاب ناريه":"fireworks","موسيقي":"music","حفله":"concert",
 "اكل":"food","طعام":"food","قهوه":"coffee","مطبخ":"kitchen","سوق":"market","فلوس":"money","شغل":"work",
 "مكتب":"office","بيزنس":"business","تكنولوجيا":"technology","كمبيوتر":"computer","موبايل":"smartphone",
 "ذكاء اصطناعي":"artificial intelligence","روبوت":"robot","مستشفي":"hospital","دكتور":"doctor","طب":"medical",
 "مدرسه":"school","جامعه":"university","كتاب":"book","مكتبه":"library","فن":"art","لوحه":"painting",
 "خلفيه":"background","خامه":"texture","نسيج":"fabric","خشب":"wood","معدن":"metal","حجر":"stone","رخام":"marble",
 "ذهب":"gold","ذهبي":"golden","اسود":"black","ابيض":"white","احمر":"red","ازرق":"blue","اخضر":"green",
 "ضوء":"light","اضاءه":"lighting","تسريب ضوء":"light leak","جزيئات":"particles","غبار":"dust","ضباب":"fog",
 "سينمائي":"cinematic","حزين":"sad","سعيد":"happy","حب":"love","وحده":"alone","امل":"hope","نصر":"victory",
 "بطل":"hero","قوه":"power","سرعه":"speed","حركه":"motion","رقص":"dance","مشي":"walking","يد":"hands","ايد":"hands",
 "عين":"eye","وجه":"face","بورتريه":"portrait","طبيعه":"nature","ريف":"countryside","زراعه":"farm","حقل":"field",
 "بركان":"volcano","زلزال":"earthquake","فيضان":"flood","جليد":"ice","قطب":"arctic","تحت الماء":"underwater",
 "شعاب":"coral reef","ايقونه":"icon","ايقونات":"icons","خط":"font","شعار":"logo",
}
def translate_query(q):
    """ترجمة تقريبية للكلمات العربية الشائعة. Claude المفروض يبعت الطلب بالإنجليزي أصلا."""
    if not AR_RE.search(q):
        return q, False
    t = norm_ar(q)
    out = []
    for phrase in sorted(AR2EN, key=len, reverse=True):
        if " " in phrase and phrase in t:
            out.append(AR2EN[phrase]); t = t.replace(phrase, " ")
    for w in t.split():
        w2 = w[2:] if w.startswith("ال") and len(w) > 4 else w
        if w in AR2EN: out.append(AR2EN[w])
        elif w2 in AR2EN: out.append(AR2EN[w2])
        elif not AR_RE.search(w): out.append(w)
    en = " ".join(dict.fromkeys(out)).strip()
    return (en or q), True

# ---------------------------------------------------------------- catalog
CAT_TAGS = {
 "فيديو ستوك مجاني": "video footage stock free b-roll clips 4k فيديو فوتيج مجاني",
 "صور ستوك مجانية": "photo photos images stock free صور مجاني",
 "ستوك مدفوع واحترافي": "premium paid stock video photo cinematic footage licensing مدفوع احترافي",
 "أرشيف ومتاحف ومصادر حكومية": "archive museum historical public domain government vintage art history ارشيف متحف تاريخي",
 "مؤثرات VFX وأوفرليز وقوالب": "vfx overlay overlays green screen transitions light leaks grain particles smoke fire explosion lut luts templates after effects premiere مؤثرات",
 "خامات وHDRI و3D وخلفيات": "texture textures hdri 3d models pbr materials background wallpaper blender خامات خلفيات",
 "فيكتور وPNG وأيقونات وخطوط": "vector svg png transparent cutout icons illustration mockup fonts stickers فيكتور ايقونات خطوط",
 "محركات بحث ومتخصص": "search engine aggregator niche stock محرك بحث",
 "عربي وشرق أوسط": "arab arabic middle east gulf egypt islamic عربي شرق اوسط",
 "توليد بالذكاء الاصطناعي": "ai generator generate text to video text to image ذكاء اصطناعي توليد",
 "مراجع بصرية وفريمات": "reference frames film stills moodboard cinematography shots مراجع",
 "فوتيج تجريبي من الكاميرات": "sample footage camera test raw r3d 8k 4k log footage فوتيج تجريبي",
 "مجتمعات مصورين": "photographers community photography portfolio مصورين",
 "أخبار ورياضة (ترخيص)": "news sports editorial press licensing اخبار رياضه",
 "طبيعة وفضاء وطقس": "nature wildlife space weather ocean earth satellite astronomy طبيعه فضاء طقس",
 "خلفيات وسينماجراف": "wallpaper background cinemagraph gif loop خلفيات",
}

def domain(u):
    return urlparse(u).netloc.lower().removeprefix("www.")

def cmd_build(a):
    rows = list(csv.reader(open(CATALOG_CSV, encoding="utf-8-sig")))[1:]
    tmpl = {}
    for f in sorted(glob.glob(os.path.join(HERE, "templates", "out*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line: continue
            try: o = json.loads(line)
            except Exception: continue
            tmpl[o.get("url", "").strip()] = o
    if os.path.exists(DB): os.remove(DB)
    c = sqlite3.connect(DB)
    c.executescript("""
      create table sites(id integer primary key, name, url, domain, category, media_type, price, quality,
                         license, notes, status, search_tpl, tpl_verified, api_no_key, api_needs_key, filters);
      create virtual table fts using fts5(name, domain, category, media_type, tags, notes,
                         content='', tokenize='unicode61 remove_diacritics 2');
      create table cache(k primary key, ts real, data);
    """)
    have = 0
    for i, r in enumerate(rows, 1):
        name, url, cat, mt, price, q, lic, notes, st = (r + [""] * 9)[:9]
        t = tmpl.get(url.strip(), {})
        tpl = (t.get("search_template") or "").strip()
        if tpl and "{q}" in tpl and "google.com/search" not in tpl: have += 1
        elif not tpl or "{q}" not in tpl: tpl = f"https://www.google.com/search?q=site:{domain(url)}+{{q}}"; t = dict(t, verified="site-search")
        c.execute("insert into sites values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (i, name, url, domain(url), cat, mt, price, q, lic, notes, st, tpl, t.get("verified", ""),
                   t.get("api_no_key", ""), t.get("api_needs_key", ""), t.get("filters_hint", "")))
        tags = CAT_TAGS.get(cat, "") + " " + mt + " " + q
        c.execute("insert into fts(rowid,name,domain,category,media_type,tags,notes) values(?,?,?,?,?,?,?)",
                  (i, norm_ar(name), domain(url).replace(".", " "), norm_ar(cat), norm_ar(mt), norm_ar(tags), norm_ar(notes)))
    c.commit()
    print(f"catalog.db: {len(rows)} موقع، منهم {have} بقالب بحث خاص، والباقي بحث جوجل داخل الموقع.")

TYPE_WORDS = {"video": "فيديو video footage", "image": "صور photo image", "hdri": "hdri", "texture": "texture خامات",
              "3d": "3d", "icon": "ايقونات icons", "font": "خطوط fonts", "vfx": "vfx overlay", "art": "museum art متحف",
              "gif": "gif", "ai": "ai generator"}

TOP = ["pexels.com", "pixabay.com", "mixkit.co", "coverr.co", "unsplash.com", "videvo.net", "artgrid.io", "storyblocks.com",
       "stock.adobe.com", "shutterstock.com", "pond5.com", "gettyimages.com", "elements.envato.com", "motionarray.com",
       "commons.wikimedia.org", "openverse.org", "archive.org", "images.nasa.gov", "filmsupply.com", "freepik.com",
       "vecteezy.com", "videezy.com", "dareful.com", "mazwai.com", "life-of-pix.com", "kaboompics.com", "stocksnap.io"]

def find_sites(q, typ=None, free=False, limit=25, _fallback=False, _q=None):
    c = sqlite3.connect(DB)
    en, _ = translate_query(q)
    link_q = _q or en
    words = set(re.findall(r"\w+", norm_ar(q) + " " + en + " " + TYPE_WORDS.get(typ or "", "")))
    words = [w for w in words if len(w) > 1]
    if not words: return []
    match = " OR ".join(f'"{w}"*' for w in words)
    sql = """select s.*, bm25(fts, 4.0, 3.0, 2.0, 2.0, 1.5, 1.0) as score from fts join sites s on s.id=fts.rowid
             where fts match ? order by score limit 400"""
    res = []
    for row in c.execute(sql, (match,)):
        d = dict(zip([x[0] for x in c.execute("select * from sites limit 0").description] + ["score"], row))
        if free and "مدفوع" in d["price"] and "جزئ" not in d["price"]: continue
        if typ == "video" and "فيديو" not in d["media_type"] and "فوتيج" not in d["category"]: d["score"] += 3
        if typ == "image" and "صور" not in d["media_type"]: d["score"] += 3
        if d["tpl_verified"] == "yes": d["score"] -= 0.5
        if d["domain"] in TOP: d["score"] -= (3.0 if _fallback else 1.0) * (1 - TOP.index(d["domain"]) / len(TOP))
        if d["api_no_key"]: d["score"] -= 0.5
        tpl = d["search_tpl"]
        in_path = tpl.find("{q}") < (tpl.find("?") if "?" in tpl else len(tpl))
        enc = (link_q.strip().replace(" ", "-") if "mixkit.co" in tpl else quote(link_q)) if in_path else quote_plus(link_q)
        d["search_url"] = tpl.replace("{q}", enc)
        res.append(d)
    res.sort(key=lambda d: d["score"])
    if len(res) < 5 and not _fallback:   # الكلمات مش في الكتالوج: رجّع أقوى المواقع للنوع المطلوب
        extra = find_sites("stock " + TYPE_WORDS.get(typ or "", "video photo"), typ, free, limit, _fallback=True, _q=en)
        ids = {d["id"] for d in res}; res += [d for d in extra if d["id"] not in ids]
    return res[:limit]

def cmd_sites(a):
    t0 = time.perf_counter()
    res = find_sites(a.query, a.type, a.free, a.limit)
    if a.json:
        print(json.dumps([{k: r[k] for k in ("name", "url", "category", "media_type", "price", "quality", "license", "search_url", "tpl_verified")} for r in res], ensure_ascii=False, indent=1)); return
    for i, r in enumerate(res, 1):
        print(f"{i:>2}. {r['name']} | {r['category']} | {r['price']} | {r['quality']}\n    {r['search_url']}")
    print(f"\n{len(res)} موقع في {1000*(time.perf_counter()-t0):.0f}ms")

def cmd_links(a):
    res = find_sites(a.query, a.type, a.free, a.limit or 200)
    en, _ = translate_query(a.query)
    os.makedirs(OUT_ROOT, exist_ok=True)
    out = os.path.join(OUT_ROOT, f"links_{re.sub(r'[^\w]+', '_', a.query)[:40]}.html")
    groups = {}
    for r in res: groups.setdefault(r["category"], []).append(r)
    h = [f"<!doctype html><meta charset=utf-8><title>{html.escape(a.query)}</title><body dir=rtl style='font-family:Segoe UI,Tahoma;background:#0b0b0b;color:#eee;max-width:1100px;margin:auto'>",
         f"<h1>بحث: {html.escape(a.query)} <small style='color:#999'>({html.escape(en)})</small></h1><p>{len(res)} موقع</p>"]
    for cat, l in groups.items():
        h.append(f"<h2 style='color:#d4af37'>{html.escape(cat)} ({len(l)})</h2><ol>")
        for r in l:
            h.append(f"<li><a style='color:#8cf' target=_blank href='{html.escape(r['search_url'])}'>{html.escape(r['name'])}</a> "
                     f"<small style='color:#999'>{html.escape(r['price'])} · {html.escape(r['quality'])}</small></li>")
        h.append("</ol>")
    open(out, "w", encoding="utf-8").write("\n".join(h))
    print(out)

# ---------------------------------------------------------------- live sources
def R(source, kind, title, page, media, preview, w=None, h=None, dur=None, lic="", author=""):
    return {"source": source, "kind": kind, "title": (title or "").strip()[:140], "page_url": page, "media_url": media,
            "preview_url": preview, "width": int(w) if str(w or "").isdigit() else None,
            "height": int(h) if str(h or "").isdigit() else None, "duration": dur, "license": lic, "author": author}

async def j(cl, url, **kw):
    r = await cl.get(url, **kw); r.raise_for_status(); return r.json()

async def s_openverse(cl, q, kind, n):
    d = await j(cl, "https://api.openverse.org/v1/images/", params={"q": q, "page_size": min(n, 20)})
    return [R("Openverse/" + (x.get("source") or ""), "image", x.get("title"), x.get("foreign_landing_url"), x.get("url"),
              x.get("thumbnail"), x.get("width"), x.get("height"), lic=f"{x.get('license','')} {x.get('license_version','')}".strip(),
              author=x.get("creator") or "") for x in d.get("results", [])]

async def s_wikimedia(cl, q, kind, n):
    ft = "filetype:video" if kind == "video" else "filetype:bitmap"
    d = await j(cl, "https://commons.wikimedia.org/w/api.php", params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} {ft}", "gsrnamespace": 6,
        "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 640,
        "iiextmetadatafilter": "LicenseShortName|Artist"})
    out = []
    for p in sorted((d.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 0)):
        ii = (p.get("imageinfo") or [{}])[0]; md = ii.get("extmetadata", {})
        out.append(R("Wikimedia Commons", kind, p.get("title", "").removeprefix("File:"), ii.get("descriptionurl"), ii.get("url"),
                     ii.get("thumburl"), ii.get("width"), ii.get("height"), ii.get("duration"),
                     md.get("LicenseShortName", {}).get("value", ""), re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:60]))
    return out

async def s_nasa(cl, q, kind, n):
    d = await j(cl, "https://images-api.nasa.gov/search", params={"q": q, "media_type": kind, "page_size": n})
    items = d.get("collection", {}).get("items", [])[:n]
    async def one(it):
        dd = (it.get("data") or [{}])[0]; nid = dd.get("nasa_id")
        media = None
        try:
            files = await j(cl, it["href"])
            pref = ["~orig.mp4", "~large.mp4", "~orig.mov"] if kind == "video" else ["~orig.jpg", "~orig.tif", "~large.jpg", "~orig.png"]
            for p in pref:
                m = [f for f in files if f.endswith(p)]
                if m: media = m[0].replace("http://", "https://"); break
        except Exception: pass
        return R("NASA", kind, dd.get("title"), f"https://images.nasa.gov/details/{quote(nid or '')}", media,
                 (it.get("links") or [{}])[0].get("href"), lic="Public Domain (NASA)", author=dd.get("center", ""))
    return await asyncio.gather(*[one(it) for it in items])

async def s_archive(cl, q, kind, n):
    mt = "movies" if kind == "video" else "image"
    d = await j(cl, "https://archive.org/advancedsearch.php", params={
        "q": f"title:({q}) AND mediatype:({mt})", "fl[]": ["identifier", "title", "licenseurl", "year"], "rows": n,
        "output": "json"})
    return [R("Internet Archive", kind, f"{x.get('title','')} {x.get('year','')}".strip(), f"https://archive.org/details/{x['identifier']}",
              None, f"https://archive.org/services/img/{x['identifier']}", lic=x.get("licenseurl") or "راجع الصفحة")
            for x in d.get("response", {}).get("docs", [])]

async def s_europeana(cl, q, kind, n):
    d = await j(cl, "https://api.europeana.eu/record/v2/search.json", params={
        "wskey": KEYS.get("EUROPEANA_API_KEY", "api2demo"), "query": q, "media": "true", "reusability": "open",
        "rows": n, "qf": "TYPE:" + ("VIDEO" if kind == "video" else "IMAGE")})
    return [R("Europeana/" + ((x.get("dataProvider") or [""])[0])[:30], kind, (x.get("title") or [""])[0], x.get("guid"),
              (x.get("edmIsShownBy") or [None])[0], (x.get("edmPreview") or [None])[0], lic=(x.get("rights") or [""])[0])
            for x in d.get("items", [])]

async def s_met(cl, q, kind, n):
    d = await j(cl, "https://collectionapi.metmuseum.org/public/collection/v1/search", params={"q": q, "hasImages": "true"})
    ids = (d.get("objectIDs") or [])[:min(n, 12)]
    async def one(i):
        try: o = await j(cl, f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}")
        except Exception: return None
        if not o.get("primaryImage"): return None
        return R("The Met", "image", o.get("title"), o.get("objectURL"), o.get("primaryImage"), o.get("primaryImageSmall"),
                 lic="CC0" if o.get("isPublicDomain") else "حقوق محفوظة", author=o.get("artistDisplayName", ""))
    return [x for x in await asyncio.gather(*[one(i) for i in ids]) if x]

async def s_aic(cl, q, kind, n):
    d = await j(cl, "https://api.artic.edu/api/v1/artworks/search", params={
        "q": q, "limit": n, "fields": "id,title,image_id,is_public_domain,thumbnail,artist_title",
        "query[term][is_public_domain]": "true"})
    out = []
    for x in d.get("data", []):
        if not x.get("image_id"): continue
        b = f"https://www.artic.edu/iiif/2/{x['image_id']}"
        t = x.get("thumbnail") or {}
        out.append(R("Art Institute Chicago", "image", x.get("title"), f"https://www.artic.edu/artworks/{x['id']}",
                     f"{b}/full/1686,/0/default.jpg", f"{b}/full/400,/0/default.jpg", t.get("width"), t.get("height"),
                     lic="CC0", author=x.get("artist_title") or ""))
    return out

async def s_cleveland(cl, q, kind, n):
    d = await j(cl, "https://openaccess-api.clevelandart.org/api/artworks/", params={"q": q, "has_image": 1, "cc0": 1, "limit": n})
    out = []
    for x in d.get("data", []):
        im = x.get("images") or {}; big = im.get("print") or im.get("full") or im.get("web") or {}
        out.append(R("Cleveland Museum", "image", x.get("title"), x.get("url"), big.get("url"), (im.get("web") or {}).get("url"),
                     big.get("width"), big.get("height"), lic="CC0"))
    return out

async def s_wellcome(cl, q, kind, n):
    d = await j(cl, "https://api.wellcomecollection.org/catalogue/v2/images", params={"query": q, "pageSize": n})
    out = []
    for x in d.get("results", []):
        loc = (x.get("locations") or [{}])[0]; base = (loc.get("url") or "").removesuffix("/info.json")
        src = x.get("source") or {}
        out.append(R("Wellcome Collection", "image", src.get("title"), f"https://wellcomecollection.org/works/{src.get('id','')}",
                     f"{base}/full/max/0/default.jpg" if base else None, f"{base}/full/400,/0/default.jpg" if base else None,
                     lic=((loc.get("license") or {}).get("id") or "").upper()))
    return out

async def s_loc(cl, q, kind, n):
    d = await j(cl, "https://www.loc.gov/photos/", params={"q": q, "fo": "json", "c": n},
                headers={"User-Agent": BROWSER_UA})
    out = []
    for x in d.get("results", []):
        imgs = x.get("image_url") or []
        if not imgs: continue
        big = imgs[-1].split("#")[0]
        out.append(R("Library of Congress", "image", x.get("title"), x.get("id") or x.get("url"), big, imgs[0].split("#")[0],
                     lic="راجع الصفحة (أغلبها ملكية عامة)"))
    return out

async def s_smithsonian(cl, q, kind, n):
    d = await j(cl, "https://api.si.edu/openaccess/api/v1.0/search", params={
        "q": f"{q} AND online_media_type:Images", "rows": n, "api_key": KEYS.get("SI_API_KEY", "DEMO_KEY")})
    out = []
    for x in d.get("response", {}).get("rows", []):
        dn = x.get("content", {}).get("descriptiveNonRepeating", {})
        m = ((dn.get("online_media") or {}).get("media") or [{}])[0]
        if not m.get("content"): continue
        out.append(R("Smithsonian", "image", x.get("title"), dn.get("record_link") or dn.get("guid"), m.get("content"),
                     m.get("thumbnail"), lic=(m.get("usage") or {}).get("access", "")))
    return out

_PH = {}
async def s_polyhaven(cl, q, kind, n):
    t = {"hdri": "hdris", "texture": "textures", "3d": "models"}.get(kind, "all")
    k = "ph_" + t
    data = cache_get(k, 7 * 86400)
    if data is None:
        data = await j(cl, "https://api.polyhaven.com/assets", params={"t": t}); cache_put(k, data)
    words = [w.lower() for w in q.split()]
    scored = []
    for aid, a in data.items():
        hay = " ".join([aid, a.get("name", "")] + a.get("tags", []) + a.get("categories", [])).lower()
        s = sum(w in hay for w in words)
        if s: scored.append((s, a.get("download_count", 0), aid, a))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    kk = {0: "hdri", 1: "texture", 2: "3d"}
    return [R("Poly Haven", kk.get(a.get("type"), kind), a.get("name"), f"https://polyhaven.com/a/{aid}",
              f"polyhaven:{aid}", f"https://cdn.polyhaven.com/asset_img/thumbs/{aid}.png?height=256",
              lic="CC0", author=", ".join((a.get("authors") or {}).keys())) for _, _, aid, a in scored[:n]]

async def s_ambientcg(cl, q, kind, n):
    d = await j(cl, "https://ambientcg.com/api/v2/full_json", params={"q": q, "limit": n, "include": "previewData,downloadData",
                                                                       "type": "HDRI" if kind == "hdri" else "Material"})
    out = []
    for x in d.get("foundAssets", []):
        prev = x.get("previewImage") or {}
        pv = prev.get("512-PNG") or prev.get("256-PNG") or next(iter(prev.values()), None)
        dl = None
        try:
            fl = x["downloadFolders"]["default"]["downloadFiletypeCategories"]["zip"]["downloads"]
            fl = sorted(fl, key=lambda f: f.get("size", 0)); dl = fl[-1]["fullDownloadPath"] if fl else None
        except Exception: pass
        out.append(R("ambientCG", kind, x.get("displayName") or x.get("assetId"), x.get("shortLink") or f"https://ambientcg.com/a/{x.get('assetId')}",
                     dl, pv, lic="CC0"))
    return out

async def s_iconify(cl, q, kind, n):
    d = await j(cl, "https://api.iconify.design/search", params={"query": q, "limit": max(32, n)})
    out = []
    for ic in d.get("icons", [])[:n]:
        p, nm = ic.split(":", 1)
        u = f"https://api.iconify.design/{p}/{nm}.svg"
        out.append(R("Iconify/" + p, "icon", ic, f"https://icon-sets.iconify.design/{p}/{nm}/", u, u,
                     lic=((d.get("collections") or {}).get(p) or {}).get("license", {}).get("spdx", "")))
    return out

async def s_wallhaven(cl, q, kind, n):
    d = await j(cl, "https://wallhaven.cc/api/v1/search", params={"q": q, "purity": "100", "sorting": "relevance", "atleast": "1920x1080"})
    return [R("Wallhaven", "wallpaper", " ".join([x.get("category", ""), x.get("resolution", "")]), x.get("url"), x.get("path"),
              (x.get("thumbs") or {}).get("large"), x.get("dimension_x"), x.get("dimension_y"),
              lic="حقوق أصحابها - راجع المصدر", author=x.get("source", "")) for x in d.get("data", [])[:n]]

async def s_vam(cl, q, kind, n):
    d = await j(cl, "https://api.vam.ac.uk/v2/objects/search", params={"q": q, "images_exist": 1, "page_size": n})
    out = []
    for x in d.get("records", []):
        b = (x.get("_images") or {}).get("_iiif_image_base_url")
        if not b: continue
        out.append(R("V&A Museum", "image", x.get("_primaryTitle") or x.get("objectType"), f"https://collections.vam.ac.uk/item/{x.get('systemNumber')}/",
                     f"{b}full/full/0/default.jpg", f"{b}full/400,/0/default.jpg", lic="V&A terms (غير تجاري غالبا)",
                     author=(x.get("_primaryMaker") or {}).get("name", "")))
    return out

async def s_smk(cl, q, kind, n):
    d = await j(cl, "https://api.smk.dk/api/v1/art/search/", params={"keys": q, "rows": n, "filters": "[has_image:true],[public_domain:true]", "lang": "en"})
    return [R("SMK Denmark", "image", ((x.get("titles") or [{}])[0]).get("title"), x.get("frontend_url"),
              x.get("image_native") or x.get("image_thumbnail"), x.get("image_thumbnail"), x.get("image_width"), x.get("image_height"),
              lic="CC0" if x.get("public_domain") else "", author=((x.get("production") or [{}])[0]).get("creator", ""))
            for x in d.get("items", [])]

async def s_sketchfab(cl, q, kind, n):
    d = await j(cl, "https://api.sketchfab.com/v3/search", params={"type": "models", "q": q, "downloadable": "true", "count": n})
    out = []
    for x in d.get("results", []):
        th = sorted((x.get("thumbnails") or {}).get("images", []), key=lambda i: i.get("width", 0))
        out.append(R("Sketchfab", "3d", x.get("name"), x.get("viewerUrl"), None, th[-1]["url"] if th else None,
                     lic=(x.get("license") or {}).get("label", "") if isinstance(x.get("license"), dict) else "راجع الصفحة (تحميل بحساب)",
                     author=(x.get("user") or {}).get("displayName", "")))
    return out

# ---- keyed (optional)
async def s_pexels(cl, q, kind, n):
    h = {"Authorization": KEYS["PEXELS_API_KEY"]}
    if kind == "video":
        d = await j(cl, "https://api.pexels.com/videos/search", params={"query": q, "per_page": min(n, 40)}, headers=h)
        out = []
        for v in d.get("videos", []):
            f = max(v.get("video_files", []), key=lambda f: (f.get("width") or 0), default={})
            out.append(R("Pexels", "video", v.get("url", "").rstrip("/").split("/")[-1].replace("-", " "), v.get("url"), f.get("link"),
                         v.get("image"), f.get("width"), f.get("height"), v.get("duration"), "Pexels License", (v.get("user") or {}).get("name", "")))
        return out
    d = await j(cl, "https://api.pexels.com/v1/search", params={"query": q, "per_page": min(n, 40)}, headers=h)
    return [R("Pexels", "image", p.get("alt"), p.get("url"), p["src"]["original"], p["src"]["medium"], p.get("width"), p.get("height"),
              lic="Pexels License", author=p.get("photographer", "")) for p in d.get("photos", [])]

async def s_pixabay(cl, q, kind, n):
    k = KEYS["PIXABAY_API_KEY"]
    if kind == "video":
        d = await j(cl, "https://pixabay.com/api/videos/", params={"key": k, "q": q, "per_page": max(3, min(n, 50))})
        out = []
        for v in d.get("hits", []):
            vs = v.get("videos", {}); b = vs.get("large") if (vs.get("large") or {}).get("url") else vs.get("medium", {})
            out.append(R("Pixabay", "video", v.get("tags"), v.get("pageURL"), b.get("url"), b.get("thumbnail"), b.get("width"),
                         b.get("height"), v.get("duration"), "Pixabay License", v.get("user", "")))
        return out
    d = await j(cl, "https://pixabay.com/api/", params={"key": k, "q": q, "per_page": max(3, min(n, 50)), "image_type": "photo"})
    return [R("Pixabay", "image", x.get("tags"), x.get("pageURL"), x.get("largeImageURL"), x.get("webformatURL"),
              x.get("imageWidth"), x.get("imageHeight"), lic="Pixabay License", author=x.get("user", "")) for x in d.get("hits", [])]

async def s_unsplash(cl, q, kind, n):
    d = await j(cl, "https://api.unsplash.com/search/photos", params={"query": q, "per_page": min(n, 30), "client_id": KEYS["UNSPLASH_ACCESS_KEY"]})
    return [R("Unsplash", "image", x.get("alt_description"), (x.get("links") or {}).get("html"), (x.get("urls") or {}).get("full"),
              (x.get("urls") or {}).get("small"), x.get("width"), x.get("height"), lic="Unsplash License",
              author=(x.get("user") or {}).get("name", "")) for x in d.get("results", [])]

async def s_giphy(cl, q, kind, n):
    d = await j(cl, "https://api.giphy.com/v1/gifs/search", params={"api_key": KEYS["GIPHY_API_KEY"], "q": q, "limit": n})
    return [R("GIPHY", "gif", x.get("title"), x.get("url"), x["images"]["original"].get("mp4") or x["images"]["original"].get("url"),
              x["images"]["fixed_width"].get("url"), x["images"]["original"].get("width"), x["images"]["original"].get("height"),
              lic="GIPHY Terms") for x in d.get("data", [])]

# name -> (func, kinds, key-required)
SOURCES = {
 "pexels": (s_pexels, {"video", "image"}, "PEXELS_API_KEY"),
 "pixabay": (s_pixabay, {"video", "image"}, "PIXABAY_API_KEY"),
 "unsplash": (s_unsplash, {"image"}, "UNSPLASH_ACCESS_KEY"),
 "giphy": (s_giphy, {"gif"}, "GIPHY_API_KEY"),
 "wikimedia": (s_wikimedia, {"video", "image"}, None),
 "nasa": (s_nasa, {"video", "image"}, None),
 "archive": (s_archive, {"video"}, None),
 "europeana": (s_europeana, {"video", "image", "art"}, None),
 "openverse": (s_openverse, {"image"}, None),
 "smithsonian": (s_smithsonian, {"image", "art"}, None),
 "wellcome": (s_wellcome, {"image", "art"}, None),
 "aic": (s_aic, {"art"}, None),
 "cleveland": (s_cleveland, {"art"}, None),
 "polyhaven": (s_polyhaven, {"hdri", "texture", "3d"}, None),
 "ambientcg": (s_ambientcg, {"hdri", "texture"}, None),
 "iconify": (s_iconify, {"icon"}, None),
 "vam": (s_vam, {"art"}, None),
 "smk": (s_smk, {"art"}, None),
 "wallhaven": (s_wallhaven, {"wallpaper"}, None),
}

def cache_get(k, ttl):
    try:
        c = sqlite3.connect(DB); r = c.execute("select ts,data from cache where k=?", (k,)).fetchone()
        if r and time.time() - r[0] < ttl: return json.loads(r[1])
    except Exception: pass
    return None

def cache_put(k, data):
    try:
        c = sqlite3.connect(DB); c.execute("insert or replace into cache values(?,?,?)", (k, time.time(), json.dumps(data))); c.commit()
    except Exception: pass

async def run_search(q, kinds, n, only, timeout):
    jobs = []
    for name, (fn, sk, key) in SOURCES.items():
        if only and name not in only: continue
        if key and key not in KEYS: continue
        for k in kinds:
            if k in sk or (k == "art" and name in ("aic", "cleveland", "vam", "smk")):
                real = "image" if k == "art" else k
                jobs.append((name, real, fn))
    report = {}
    limits = httpx.Limits(max_connections=80, max_keepalive_connections=40)
    async with httpx.AsyncClient(headers={"User-Agent": UA}, timeout=timeout, follow_redirects=True, limits=limits) as cl:
        async def go(name, kind, fn):
            ck = f"s|{name}|{kind}|{q.lower()}|{n}"
            hit = cache_get(ck, 86400)
            if hit is not None:
                report[f"{name}:{kind}"] = f"cache {len(hit)}"; return hit
            t = time.perf_counter()
            try:
                res = await asyncio.wait_for(fn(cl, q, kind, n), timeout + 2)
                res = [r for r in res if r and (r.get("media_url") or r.get("page_url"))]
                cache_put(ck, res)
                report[f"{name}:{kind}"] = f"{len(res)} في {time.perf_counter()-t:.1f}s"; return res
            except Exception as e:
                report[f"{name}:{kind}"] = f"فشل ({type(e).__name__})"; return []
        lists = await asyncio.gather(*[go(*x) for x in jobs])
    return lists, report

def rank(lists, q, min_w, orient, limit):
    words = [w.lower() for w in re.findall(r"\w+", q)]
    seen, flat = set(), []
    for li, lst in enumerate(lists):
        for pos, r in enumerate(lst):
            key = r.get("media_url") or r.get("page_url")
            if key in seen: continue
            seen.add(key)
            w, h = r.get("width") or 0, r.get("height") or 0
            if min_w and w and max(w, h) < min_w: continue
            if orient == "portrait" and w and h and h <= w: continue
            if orient == "landscape" and w and h and w <= h: continue
            title = (r.get("title") or "").lower()
            s = pos * 1.0                                   # ترتيب المصدر نفسه
            s -= 2.0 * sum(wd in title for wd in words)     # تطابق العنوان
            s -= min(w * h / 8.3e6, 2.0) if w else 0        # الدقة (4K = -1)
            s -= 1.0 if re.search(r"cc0|public domain|pexels|pixabay|unsplash|cc by", (r.get("license") or "").lower()) else 0
            s -= 0.5 if r.get("media_url") else 0
            r["_s"] = s; flat.append(r)
    flat.sort(key=lambda r: r["_s"])
    picked, used = [], {}
    pool = flat[:]
    while pool and len(picked) < limit:      # تنويع: كل نتيجة من نفس المصدر عليها غرامة
        best = min(pool, key=lambda r: r["_s"] + 2.5 * used.get(r["source"].split("/")[0], 0))
        pool.remove(best); used[best["source"].split("/")[0]] = used.get(best["source"].split("/")[0], 0) + 1
        picked.append(best)
    for r in picked: r.pop("_s", None)
    return picked

def cmd_search(a):
    t0 = time.perf_counter()
    q, tr = translate_query(a.query)
    kinds = ["video", "image"] if a.type in (None, "any") else [a.type]
    only = set(a.sources.split(",")) if a.sources else None
    lists, report = asyncio.run(run_search(q, kinds, a.per_source, only, a.timeout))
    res = rank(lists, q, a.min_width, a.orientation, a.limit)
    json.dump({"query": q, "results": res}, open(LAST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dt = time.perf_counter() - t0
    if a.json:
        print(json.dumps({"query": q, "translated": tr, "seconds": round(dt, 2), "sources": report, "results": res}, ensure_ascii=False, indent=1)); return
    if tr: print(f"[ترجمة الطلب] {a.query} -> {q}")
    for i, r in enumerate(res, 1):
        dim = f"{r['width']}x{r['height']}" if r.get("width") else "?"
        dur = f" {r['duration']:.0f}s" if isinstance(r.get("duration"), (int, float)) else ""
        print(f"{i:>3}. [{r['kind']}] {r['title'][:70]} | {r['source']} | {dim}{dur} | {r['license'][:30]}\n     {r.get('media_url') or r['page_url']}")
    print(f"\n{len(res)} نتيجة من {len(report)} بحث متوازي في {dt:.1f}s")
    print("  " + " · ".join(f"{k}={v}" for k, v in report.items()))
    if any(k not in KEYS for k in ("PEXELS_API_KEY", "PIXABAY_API_KEY")):
        print("  (Pexels/Pixabay/Unsplash مقفولين لحد ما تضيف مفاتيح مجانية في keys.json — شوف: mh.py keys)")

def cmd_hunt(a):
    """البحث الحي + أنسب المواقع في رد JSON واحد (مخصص لـ Claude)."""
    t0 = time.perf_counter()
    q, tr = translate_query(a.query)
    kinds = ["video", "image"] if a.type in (None, "any") else [a.type]
    lists, report = asyncio.run(run_search(q, kinds, a.per_source, None, a.timeout))
    res = rank(lists, q, a.min_width, a.orientation, a.limit)
    json.dump({"query": q, "results": res}, open(LAST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sites = find_sites(a.query, a.type if a.type != "any" else None, a.free, a.sites)
    print(json.dumps({"query": q, "translated": tr, "seconds": round(time.perf_counter() - t0, 2), "sources": report,
                      "results": [dict(r, n=i) for i, r in enumerate(res, 1)],
                      "more_sites": [{k: x[k] for k in ("name", "category", "price", "quality", "search_url")} for x in sites]},
                     ensure_ascii=False, indent=1))

# ---------------------------------------------------------------- download
def cmd_get(a):
    data = json.load(open(LAST, encoding="utf-8")); res = data["results"]
    out = a.output or os.path.join(OUT_ROOT, "downloads"); os.makedirs(out, exist_ok=True)
    src_log = os.path.join(out, "sources.txt")
    with httpx.Client(headers={"User-Agent": UA}, follow_redirects=True, timeout=120) as cl:
        for i in a.ids:
            r = res[i - 1]; mu = r.get("media_url")
            try:
                if mu and mu.startswith("polyhaven:"):
                    aid = mu.split(":", 1)[1]; fl = cl.get(f"https://api.polyhaven.com/files/{aid}").json()
                    if "hdri" in fl:
                        res_k = a.res if a.res in fl["hdri"] else sorted(fl["hdri"], key=lambda s: int(s[:-1]))[-1]
                        mu = fl["hdri"][res_k]["hdr"]["url"]
                    else:
                        blend = fl.get("blend") or fl.get("gltf") or {}
                        res_k = a.res if a.res in blend else (sorted(blend, key=lambda s: int(s[:-1]))[-1] if blend else None)
                        mu = blend[res_k][next(iter(blend[res_k]))]["url"] if res_k else None
                if mu:
                    ext = os.path.splitext(urlparse(mu).path)[1].lower()
                    ext = ext if re.fullmatch(r"\.[a-z0-9]{2,5}", ext) else (".mp4" if r["kind"] == "video" else ".jpg")
                    name = (re.sub(r"[^\w\-]+", "_", r.get("title") or "")[:60].strip("_") or "item") + ext
                    path = os.path.join(out, f"{i:03d}_{name}")
                    with cl.stream("GET", mu) as s:
                        s.raise_for_status()
                        with open(path, "wb") as f:
                            for ch in s.iter_bytes(1 << 20): f.write(ch)
                else:
                    subprocess.run(["yt-dlp", "-f", "bv*+ba/b", "-o", os.path.join(out, f"{i:03d}_%(title).60s.%(ext)s"), r["page_url"]], check=True)
                    path = out
                with open(src_log, "a", encoding="utf-8") as f:
                    f.write(f"{os.path.basename(path)}\t{r['source']}\t{r['page_url']}\t{r['license']}\t{r.get('author','')}\n")
                print(f"OK {i}: {path}")
            except Exception as e:
                print(f"FAIL {i}: {type(e).__name__}: {e}")

def cmd_keys(a):
    for name, (_, kinds, key) in SOURCES.items():
        st = "بدون مفتاح ✓" if not key else ("مفعّل ✓" if key in KEYS else f"مقفول — حط {key} في keys.json")
        print(f"{name:12} {','.join(sorted(kinds)):22} {st}")
    print(f"\nملف المفاتيح: {os.path.join(HERE, 'keys.json')}  (مثال: keys.example.json)")

def cmd_sources(a):
    cmd_keys(a)

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("build")
    types = ["any", "video", "image", "art", "hdri", "texture", "3d", "icon", "gif", "font", "vfx", "ai"]
    for nm in ("sites", "links"):
        x = sp.add_parser(nm); x.add_argument("query"); x.add_argument("--type", choices=types); x.add_argument("--free", action="store_true")
        x.add_argument("--limit", type=int, default=25 if nm == "sites" else 0); x.add_argument("--json", action="store_true")
    x = sp.add_parser("search"); x.add_argument("query"); x.add_argument("--type", choices=types[:9] + ["wallpaper"], default="any")
    x.add_argument("--limit", type=int, default=40); x.add_argument("--per-source", type=int, default=15)
    x.add_argument("--min-width", type=int, default=0, help="مثلا 3840 لـ 4K"); x.add_argument("--orientation", choices=["portrait", "landscape"])
    x.add_argument("--sources", help="مثلا nasa,wikimedia"); x.add_argument("--timeout", type=float, default=8.0); x.add_argument("--json", action="store_true")
    x = sp.add_parser("hunt"); x.add_argument("query"); x.add_argument("--type", choices=types[:9] + ["wallpaper"], default="any")
    x.add_argument("--limit", type=int, default=30); x.add_argument("--per-source", type=int, default=15); x.add_argument("--sites", type=int, default=15)
    x.add_argument("--min-width", type=int, default=0); x.add_argument("--orientation", choices=["portrait", "landscape"])
    x.add_argument("--free", action="store_true"); x.add_argument("--timeout", type=float, default=8.0)
    x = sp.add_parser("get"); x.add_argument("ids", type=int, nargs="+"); x.add_argument("-o", "--output"); x.add_argument("--res", default="4k")
    sp.add_parser("keys"); sp.add_parser("sources")
    a = p.parse_args()
    if a.cmd != "build" and not os.path.exists(DB):
        import contextlib
        with contextlib.redirect_stdout(sys.stderr):  # keep --json stdout clean on first run
            cmd_build(a)
    {"build": cmd_build, "sites": cmd_sites, "links": cmd_links, "search": cmd_search, "hunt": cmd_hunt, "get": cmd_get,
     "keys": cmd_keys, "sources": cmd_sources}[a.cmd](a)

if __name__ == "__main__":
    main()
