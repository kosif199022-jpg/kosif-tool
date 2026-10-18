# قدرات التطبيقات المحللة — Analyzed app capabilities (APPX)

<div dir="rtl">

**من أين جاءت:** في 2026-10-18 حُللت ثلاثة مثبّتات وضعها المالك في مجلد العمل بأداة REA v6.7.0 وأداة `scripts/installer_triage.py`، بلا تشغيل أي منها: CapCut وCanva 1.126.1 وAdobe Premiere Pro. السجل الكامل في [proofs/windows-installers-rea](../proofs/windows-installers-rea/README.md). كل ميزة وجدناها صارت قدرة في عائلة [app-feature-transfer](powers/app-feature-transfer.md) (APPX-01…APPX-30)، ومعها وصفة مفتوحة تبنيها أنت.

**القاعدة:** نستلهم الميزة ولا ننسخ الكود. لا يدخل هذا المستودع أي سطر من كود Canva أو CapCut أو Adobe؛ نسجّل الحقيقة البنيوية (اسم نافذة، مرساة API، امتداد ملف) ثم نكتب تنفيذًا أصليًا بأدوات مفتوحة ونثبته باختبار قابل للقياس.

</div>

## 1. What each installer really is

| | CapCut | Canva 1.126.1 | Adobe Premiere Pro |
|---|---|---|---|
| File | 2.9 MB, signed Bytedance Pte. Ltd. | 213.6 MB, signed Canva | 3.4 MB, signed Adobe Inc. |
| Installer | NSIS-3 Unicode | NSIS-3 Unicode | UPX-packed "Creative Cloud Set-up" (Adobe Installer 2.14.0.43) |
| Payload | `res.zip` (installer skin, 23 languages) + `shell_downloader.dll`, `downloader_nsis_plugin.dll`, `BgWorker.dll` | `app-64.7z` + `app-32.7z` → Electron app, `resources/app.asar` (23 MB, 998 files) | none: the product is downloaded by Creative Cloud |
| What we can learn | installer architecture only | the whole desktop shell | installer architecture only |

So the **editor** features of CapCut and Premiere are *not* in these files. They are listed below from the vendors' public product documentation and marked as such; the open recipe that rebuilds each one was proved here on synthetic media ([proofs/app-feature-transfer](../proofs/app-feature-transfer/README.md), 17/17).

## 2. Video-editor features → proven open recipes

| Feature (app) | Power | Recipe in one line |
|---|---|---|
| Speed curve (CapCut) | APPX-01 ✅ | trim + `setpts` per segment + concat |
| Chroma key (CapCut, Premiere Ultra Key) | APPX-02 ✅ | `chromakey` + `overlay` |
| Auto reframe 9:16 (Premiere, CapCut) | APPX-03 ✅ | OpenCV subject centroid → smoothed crop → raw pipe to x264 |
| Scene edit detection (Premiere) | APPX-04 ✅ | `select='gt(scene,0.3)',showinfo` |
| Loudness −14 LUFS (both) | APPX-05 ✅ | `loudnorm` then `ebur128` check |
| Filters / Lumetri looks | APPX-06 ✅ | generated `.cube` + `lut3d` |
| Remove pauses (CapCut) | APPX-07 ✅ | `silencedetect` → `silenceremove` keeping a 0.5 s breath |
| Auto beat (CapCut) | APPX-08 ✅ | energy flux peaks → BPM |
| Keyframed punch-in (both) | APPX-10 ✅ | `zoompan` (+ EASE curves) |
| Auto ducking (both) | APPX-11 ✅ | `sidechaincompress` |
| Enhance Speech / reduce noise | APPX-12 ✅ | `afftdn` + high-pass (classic DSP, not Adobe's model) |
| Auto captions / Speech to Text | APPX-13 ✅ | faster-whisper word timestamps → SRT |
| Remove background (CapCut, Canva) | APPX-14 ✅ | GrabCut (rembg 📦 for hair) |
| EDL / project interchange (Premiere) | APPX-15 ✅ | CMX3600 writer + ffmpeg conform |
| Reverse + freeze (CapCut) | APPX-16 ✅ | `reverse` + `tpad=stop_mode=clone` |
| Cover suggestion (CapCut, Canva) | APPX-17 ✅ | Laplacian sharpness + colourfulness |

## 3. Canva desktop: evidence from its own bytes

From `installer_triage.py fingerprint`, REA `inspect-electron-fuses` and REA `analyze-javascript-application` (preload + package.json):

- **Three renderer windows**: `desktop_chrome_v2` (the editor shell), `desktop_recording` (pages `display_media_picker`, `mission_control`, `overlay`, `talking_head`) and `desktop_offline_fallback`. → APPX-09 ✅ camera bubble, APPX-18 📄 display picker, APPX-19 📄 control + overlay windows, APPX-20 📄 offline fallback.
- **RTL shipped as separate builds**: every page exists as `.ltr`/`.rtl` CSS and HTML. → APPX-21 📄 (directly useful for Arabic apps).
- **16 file associations** including HEIC and Apple Keynote/Numbers/Pages. → APPX-22 📄.
- **One bridge, two members**: `ElectronBridge {onPageBuildIdentityReady, requestMessagePort}`; the web app talks to the shell over a MessagePort. → APPX-23 📄.
- **Fuses** (REA): RunAsNode, NODE_OPTIONS and inspect arguments disabled; cookie encryption, embedded ASAR integrity and only-load-from-ASAR enabled. → APPX-24 ✅ (the check is proven here).
- **Shell services** (anchor counts in `dist/main.js`): electron-updater/autoUpdater (77), Sentry (150) + crashReporter (9), safeStorage, `setAsDefaultProtocolClient` and `canva://notification`, `protocol.handle`, Tray, Notification, nativeTheme, spell-check dictionary, utilityProcess, webRequest. → APPX-25…27 📄.

## 4. Installer architecture

- Dual-arch NSIS payload (Canva) → APPX-28 📄.
- Online bootstrapper (CapCut: libcurl + BoringSSL with `sha256//` public-key pinning, MD5 check, signature checker, background worker, 23 UI languages; Adobe: UPX-packed Creative Cloud setup) → APPX-29 📄.
- Signature first, then triage, never run → APPX-30 ✅.

## 5. How to use this family

1. `python scripts/powers.py suggest "<طلبك>"` — names like CapCut/كاب كات, Canva/كانفا, Premiere/بريمير route here.
2. Open the record (`powers.py show APPX-13`) and run its `how` line; `proofs/app-feature-transfer/smoke.py` holds a working version of every ✅ recipe.
3. For a new app: `installer_triage.py scan` → `unpack --authorized` → `fingerprint` → REA (`route` prints the commands) → add what you found as new APPX records with the lowest honest badge, and a proof before ✅.

**Limits:** anchor counts prove code presence, not that a feature runs; minified aliases can hide APIs (REA proved 0 Electron identities in Canva's 6.8 MB main bundle for exactly that reason). Vendor-documented features are listed as context; only the open recipes carry ✅.
