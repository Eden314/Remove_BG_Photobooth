@echo off
setlocal
title AI Tach Phong - Portable

if "%~1"=="" (
    echo.
    echo Ke mot tep anh hoac thu muc anh vao file nay.
    echo.
    pause
    exit /b 0
)

"%~dp0AI_Tach_Phong.exe" %*

if errorlevel 1 (
    echo.
    echo Xu ly that bai. Hay kiem tra loi phia tren.
    pause
)
