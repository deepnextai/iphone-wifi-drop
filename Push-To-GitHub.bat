@echo off
title Push to GitHub - deepnextai/iphone-wifi-drop
cd /d "C:\Users\aquib\.gemini\antigravity\scratch\ios_drop"
cls
echo ========================================================
echo   Pushing AirTransfer to GitHub: deepnextai/iphone-wifi-drop
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   SUCCESS: Code uploaded to https://github.com/deepnextai/iphone-wifi-drop
    echo ========================================================
) else (
    echo ========================================================
    echo   Push failed or pending authentication.
    echo ========================================================
)
echo.
pause
