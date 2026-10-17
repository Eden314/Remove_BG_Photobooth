@echo off
setlocal
title AI Tach Phong - Photobooth Worker

if "%~1"=="" (
    echo.
    echo Cach dung: RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input"
    echo Thu muc se duoc theo doi. Anh moi duoc tach nen tu dong.
    echo Nhan Ctrl+C de dung worker.
    echo.
    pause
    exit /b 1
)

"%~dp0AI_Tach_Phong.exe" "%~1" --watch %2 %3 %4 %5 %6 %7 %8 %9
