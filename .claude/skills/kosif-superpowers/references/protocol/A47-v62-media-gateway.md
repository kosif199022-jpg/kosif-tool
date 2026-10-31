# A47 — KOSIF Media Gateway (Render Free) وحالته المقيسة

> **متى تقرأه / when to read:** فيديو من رابط وأنا مش على جهازي، أو `list_uploads` / `kosif-send`، أو قبل ما تقول إن السحابة تقدر تنزّل يوتيوب · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

**الخدمة:** `services/kosif-media-gateway/` في المستودع (دُمجت في PR #184)، شغالة على Render Free:
`https://kosif-media-gateway-free-20261030.onrender.com` · أدوات MCP: `gateway_status`، `list_uploads`، `probe_youtube`، `download_permitted_video`.
**القاعدة:** الجيتواي **صندوق بريد وتنزيل من مصادر مسموحة**، مش طريق ليوتيوب.

## 1. اللي اتقاس (31-10-2026، 11:49 UTC، من غير توكن)

الدليل الخام: `evidence/A47-gateway-health-20261031.json` (بجانب هذا الملف). إعادة القياس 16:53 UTC بنفس النتيجة، ومعاها حكم النسخة المنشورة (القسم 6): `evidence/A47-deploy-check-20261031.json`.

| السؤال | النتيجة |
|---|---|
| `/health` | `alive: true`، الإصدار 0.2.0، yt-dlp 2026.10.26، ffmpeg 5.1.9 بـ libx264، deno موجود |
| المصادر المسموحة غير يوتيوب | `archive.org`، `commons.wikimedia.org`، `upload.wikimedia.org`، `vimeo.com`، `player.vimeo.com` |
| `/health?deep=1` (الفيديو الثابت `dYrEeavC3cw`) | `ok: false` و`YOUTUBE_LOGIN_REQUIRED` («Sign in to confirm you're not a bot») |
| `youtube_download_verified` | `false` (صفر تنزيلات متحققة من يوتيوب). من 0.3.0 تنزيل archive.org أو Wikimedia أو Vimeo ما بيقلبهاش؛ قبلها كان أي تنزيل متحقق بيقلبها، فـ `true` من نسخة 0.2.0 مش دليل على يوتيوب |

**الحكم:** يوتيوب من Render = **BLOCKED** (درجة إثبات E3: قياس حي من الخدمة نفسها). نفس نتيجة sandbox السحابة في A45. يوتيوب بيحجب عناوين مراكز البيانات، والجيتواي مش بيلف حوالين الحجب ده (لا كوكيز، لا بروكسي، لا كابتشا) ولا هيلف.

**مش مقيس لسه:** تنزيل حقيقي متحقق من `archive.org` على Render (محتاج التوكن). أسهل طريق: سر المستودع `KOSIF_GATEWAY_TOKEN` ثم workflow **KOSIF Media Gateway live check**، وهو بيرفع `live-report.json` من غير التوكن.

## 2. التوجيه (مين ينزّل إيه)

| المصدر | الطريق | ليه |
|---|---|---|
| يوتيوب على الآيفون | Cinema C: `c "<url>"` (A45) | اتنزّل فعلًا من اتصال الموبايل (30-10-2026) |
| يوتيوب على ماك/PC | `yt_get.sh` أو Zajil (A45) | اتصال البيت مش محجوب |
| يوتيوب و Claude في السحابة | **`kosif-send "<url>"` من a-Shell** ← الملف يترفع للجيتواي ← Claude يجيبه بـ `list_uploads` أو `_media_gateway.py pull` | الموبايل بينزّل، والجيتواي بيوصّل بس |
| archive.org / Wikimedia / Vimeo | `download_permitted_video` أو `fetch_video.py URL --gateway <rights>` | مصادر مسموحة، والملف بيتفحص بديكودر حقيقي |
| أي حاجة تانية | الجهاز، أو ملف أنا أرفعه | الجيتواي بيرفض أي host مش في القايمة (حماية SSRF) |

ما تقولش «نزّلته» إلا لما يرجع `verified: true` ومعاه SHA-256. `/health` سليم أو probe ناجح **مش** إثبات تنزيل.

## 3. التوصيل (مرة واحدة)

- **Claude Code:** `claude mcp add --transport http kosif-media <URL>/mcp --header "Authorization: Bearer $KOSIF_GATEWAY_TOKEN"`.
- **الآيفون:** `curl -fsSL <URL>/kosif-send.sh -o ~/Documents/bin/kosif-send` ثم `kosif-send --setup` (التوكن بيتحفظ بصلاحية 600) ثم `kosif-send --check`. ومن زرار المشاركة: Shortcut بيشغّل Execute Command في a-Shell بـ `kosif-send "<Shortcut Input>"`.
- التوكن عمره ما يتكتب في محادثة أو commit أو سجل.

## 4. الحدود

- Render Free بينام بعد ~15 دقيقة، فأول طلب ممكن ياخد دقيقة.
- 45MB للتنزيل، 150MB للرفع، 3 محاولات في الساعة، تنزيل واحد في المرة، والملفات بتتمسح بعد 10 دقايق (الرفع بعد ساعة).
- بعد أي `LOGIN_REQUIRED` / 429 / 403 من يوتيوب، الجيتواي بيوقف طلبات يوتيوب 30 دقيقة (`cooldown_seconds`). من v6.2، `/health?deep=1` بيعرض النتيجة والتهدئة في نفس الرد.
- الخطة Free. أي ترقية بإذني.

## 5. Gate

PASS = `download_permitted_video` أو `pull` رجع ملف بـ `verified: true` و`sha256` وحجم أكبر من صفر ومدة قريبة من المصدر.
BLOCKED = أي كود من `YOUTUBE_*` أو `ACCESS_RESTRICTED` أو `DRM_PROTECTED`: قوله بالكود، واقترح الطريق اللي في جدول 2، وما تعيدش المحاولة.

## 6. هل Render شغال بآخر كود؟ (v6.3)

كل تعديل في `server.py` بيرفع `VERSION`، و`/health` من 0.3.0 فيه `build.commit` و`build.branch` (من متغيرات Render نفسها).

```
python3 services/kosif-media-gateway/deploy_check.py --json
```

| الحكم | المعنى | تعمل إيه |
|---|---|---|
| `FRESH` | النسخة المنشورة = المستودع | كمّل |
| `STALE` | Render شغال بكود أقدم | قولها بالكود، وما تقولش إن إصلاح وصل. الحل عندي أنا: Render ← الخدمة ← **Manual Deploy ← Deploy latest commit** (أو شغّل Auto-Deploy على `main`) |
| `UNREACHABLE` | `/health` ما ردّش | Render Free ممكن يكون نايم، جرّب مرة كمان بعد دقيقة، مرة واحدة بس |

**اتقاس 31-10-2026 16:53 UTC:** `STALE` (المنشور 0.2.0، والمستودع 0.3.0). وحتى قبل 0.3.0 كان باين إنه قديم: `/health?deep=1` رجّع `public_probe` فاشل جنب `last_result: null`، وده سلوك ما قبل إصلاح v6.2.
workflow **KOSIF Media Gateway live check** فيه job اسمه `deploy` من غير توكن، بيشتغل كل يوم 06:17 UTC وبيطلع تحذير لو `STALE`.
