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

set "APP=%~dp0AI_Tach_Phong.exe"
if not exist "%APP%" set "APP=%~dp0dist\AI_Tach_Phong\AI_Tach_Phong.exe"
if not exist "%APP%" (
    echo [LOI] Khong tim thay AI_Tach_Phong.exe.
    echo Hay chay BUILD_PORTABLE.bat hoac giai nen goi portable day du.
    pause
    exit /b 1
)

"%APP%" "%~1" --watch %2 %3 %4 %5 %6 %7 %8 %9
