@echo off
chcp 65001 >nul
title KOSIF Motion Web
cd /d "%~dp0"
echo KOSIF Motion Web — http://127.0.0.1:8766/
python scripts\web\server.py --open %*
echo.
pause
