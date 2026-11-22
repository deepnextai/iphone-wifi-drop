@echo off
title Push to GitHub - deepnextai/iphone-wifi-drop
chcp 65001 >nul
cd /d "%~dp0"
cls
echo ========================================================
echo   🚀 Uploading AirTransfer to your GitHub repository...
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   🎉 SUCCESS! Code uploaded to:
    echo   https://github.com/deepnextai/iphone-wifi-drop
    echo ========================================================
) else (
    echo [INFO] Agar browser me authorization page khula ho to authorize karein.
)
echo.
pause
