@echo off
chcp 65001 >nul
title KOSIF Motion - install
cd /d "%~dp0"
echo [1/3] Python libraries...
python -m pip install -r requirements.txt
echo [2/3] Browser for frame capture (Edge is used when present)...
python -m playwright install chromium
echo [3/3] JavaScript libraries (three, gsap, esbuild, hyperframes)...
cd scripts
call npm install
cd ..
echo.
python scripts\kmotion.py doctor
echo.
echo Done. Double-click "KOSIF Motion.bat" (menu) or "KOSIF Motion Web.bat" (site).
pause
