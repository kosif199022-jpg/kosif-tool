@echo off
chcp 65001 >nul
title KOSIF Motion
cd /d "%~dp0"
python scripts\kmotion.py %*
echo.
pause
