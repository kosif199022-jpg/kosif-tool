# windows-installers-rea — REA على مثبّتات Windows حقيقية (2026-10-18)

<div dir="rtl">

## بالعربية

**ماذا يثبت:** شُغّل REA v6.7.0 فعليًا على Windows 11 على ثلاثة مثبّتات وضعها المالك في مجلد العمل: CapCut وCanva 1.126.1 وAdobe Premiere Pro (ملف الإعداد). لم يُشغَّل أي مثبّت؛ كل الفحص قراءة بايتات واستخراج بـ 7-Zip إلى مجلد جديد. السجل الكامل في `runs.json` (معرّفات الأدلة وبصمات SHA-256 فقط، بلا كود مملوك).

**ما وجدناه عن REA نفسه:**

| الملاحظة | الدليل | ما أضفناه |
|---|---|---|
| `inspect-artifact` يرى المثبّت ملف PE واحدًا «بلا عناصر حاوية» فلا يصل إلى التطبيق داخله | 3 من 3 مثبّتات | `scripts/installer_triage.py scan/unpack` يكشف NSIS/Inno/UPX/7z/MSI ويستخرج الحمولة بلا تشغيل |
| `inspect-pe-resources` يرفض ملف Adobe: «PE section raw bytes overlap headers» | الملف مضغوط بـ UPX (أقسام UPX0/UPX1) | الفرز يكشف UPX ويقول: فك الضغط على نسخة قبل الفحص العميق |
| `inspect-managed-artifact` يرفض مثبّت Canva (213 MB) لميزانية 128 MiB | `resource_constraint` | الفرز يوجّه فحص .NET إلى ملفات DLL المستخرجة فقط |
| تحليل app.asar كاملًا انتهت مهلته عند 300 ث على ملف vendor (368/804) | `provider_timeout` | التوجيه يبدأ بـ `--source-path` للملف الرئيسي والـ preload |
| main.js (6.77 MB): 2,199 وحدة و906,298 عقدة AST و6,436 نتيجة، لكن صفر هويات Electron مثبتة | الأسماء المصغّرة تخفي `require('electron')` | `installer_triage.py fingerprint` يعدّ مراسي واجهات Electron: 17 قدرة في 12 ثانية |
| `rea_bridge.py` لم يعمل على Windows: `python3` غير موجود، و`rea.cmd` يمرّر الوسائط عبر cmd.exe، ومهلة 120 ث قصيرة | تشغيل فعلي | المشغّل صار `node rea.mjs` بلا shell، ومتغيّر `REA_BIN`، و`--timeout` افتراضيه 600، و`--source-path` |

**ما لا يثبته:** لا يثبت أن أي ميزة تعمل وقت التشغيل (الفحص ساكن)، ولا يحوي أو يعيد نشر كود Canva أو CapCut أو Adobe. ملفا CapCut وAdobe مثبّتان «تمهيديان» ينزّلان البرنامج وقت التثبيت، فمزايا المحرر نفسه غير موجودة فيهما؛ ما نُسب إليهما من مزايا تحرير موثّق من البائع، لا من هذه البايتات.

</div>

## English

**What it proves:** REA v6.7.0 was actually run on Windows 11 against three installers the owner placed in the working folder (CapCut, Canva 1.126.1, Adobe Premiere Pro setup). No installer was executed: everything is byte reading plus 7-Zip extraction into a fresh folder. `runs.json` keeps evidence ids and SHA-256 digests only, never proprietary code.

| Target | Triage (`installer_triage.py scan`) | REA result |
|---|---|---|
| CapCut installer, 2.9 MB, signed Bytedance | NSIS-3 Unicode; overlay 2.56 MB; payload = `res.zip` (UI skin, 23 languages) + `shell_downloader.dll`, `downloader_nsis_plugin.dll`, `BgWorker.dll` → **online bootstrapper** | artifact: root PE, no children; PE resources ok; not managed |
| Canva 1.126.1, 213.6 MB, signed Canva | NSIS-3 Unicode; `app-64.7z` + `app-32.7z` (dual-arch) → Electron app, `resources/app.asar` 23 MB, 998 files | fuses read (7 hardening states); JS graph for preload + main; whole asar timed out at 300 s |
| Adobe Premiere Pro setup, 3.4 MB, signed Adobe | UPX0/UPX1 sections; version info "Adobe Installer 2.14.0.43", manifest "Creative Cloud Set-up" → **packed bootstrapper** | artifact ok; PE resources refused (UPX overlap); not managed |

Canva findings used by the APPX family (from `fingerprint`, REA fuses and REA preload graph):
renderer windows `desktop_chrome_v2`, `desktop_recording` (pages: display_media_picker, mission_control, overlay, talking_head), `desktop_offline_fallback`; every page shipped as `.ltr`/`.rtl` pairs; 16 file associations (avi gif heic jpeg jpg key mkv mov mp4 mpeg numbers pages png svg webm webp); one context-bridge API `ElectronBridge` with two members (`onPageBuildIdentityReady`, `requestMessagePort`) — the web app talks to the shell through a MessagePort instead of many IPC channels; anchors for desktopCapturer, autoUpdater/electron-updater, crashReporter + Sentry, safeStorage, setAsDefaultProtocolClient, protocol.handle, Tray, Notification, nativeTheme, spellcheck dictionary, utilityProcess, webRequest, offline.

**Rerun:**

```bash
python scripts/installer_triage.py scan "<folder with installers>"
python scripts/installer_triage.py unpack canva-1-126-1.exe --to ./canva-unpacked --authorized
python scripts/installer_triage.py fingerprint "./canva-unpacked/$PLUGINSDIR/app-64.7z.d/resources/app.asar"
python scripts/installer_triage.py route "./canva-unpacked/$PLUGINSDIR/app-64.7z.d"
REA_BIN=/path/to/node_modules/.bin/rea.cmd python scripts/rea_bridge.py run electron-fuses ./canva-unpacked/.../Canva.exe --authorized --output fuses.json
```

**What it does not prove:** runtime behaviour (all of this is static), or anything about the editors inside the two bootstrappers. Feature claims for CapCut and Premiere come from the vendors' own documentation; the open-tool recipes that rebuild them are proved separately in [../app-feature-transfer](../app-feature-transfer/README.md).
