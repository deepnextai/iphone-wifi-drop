@echo off
title AirTransfer - iPhone to Windows Wi-Fi Transfer
chcp 65001 >nul
cd /d "C:\Users\aquib\.gemini\antigravity\scratch\ios_drop"
cls
echo ========================================================
echo   AirTransfer - Wireless File Sharing
echo ========================================================
python server.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to start AirTransfer server.
)
echo.
echo Press any key to stop the server...
pause
