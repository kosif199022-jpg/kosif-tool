# virtualcam — كاميرا افتراضية من ملف فيديو

<div dir="rtl">

مشروع المالك، منقول من مجلد العمل كما هو (قدرة APPX-59 في `kosif-superpowers`). يشغّل أي ملف فيديو عبر **OBS Virtual Camera** فيراه Zoom والمتصفح وTikTok Live Studio كأنه كاميرا ويب.

**التشغيل:** اسحب ملف الفيديو فوق `اسحب الفيديو هنا.bat`، أو:

</div>

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File start-virtualcam.ps1 C:\path\video.mp4
```

What the script does: writes an OBS profile `VirtualCam` (1280×720 @ 30 fps) and a scene collection with one looping `ffmpeg_source` (hardware decode), then starts `obs64.exe --startvirtualcam`.

- Needs OBS Studio 28+ at `C:\Program Files\obs-studio\bin\64bit`.
- **It closes any running OBS first** (`Stop-Process obs64`), so save your OBS work before running it.
- Without a path it plays `cam-video.mp4` next to the script (not committed: `*.mp4` is git-ignored).
- Status in the catalog: 📄 documented. It was not run in the session that imported it, because it would close OBS on the owner's machine.
