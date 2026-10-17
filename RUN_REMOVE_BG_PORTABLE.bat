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

set "APP=%~dp0AI_Tach_Phong.exe"
if not exist "%APP%" set "APP=%~dp0dist\AI_Tach_Phong\AI_Tach_Phong.exe"
if not exist "%APP%" (
    echo [LOI] Khong tim thay AI_Tach_Phong.exe.
    echo Hay chay BUILD_PORTABLE.bat hoac giai nen goi portable day du.
    pause
    exit /b 1
)

"%APP%" %*

if errorlevel 1 (
    echo.
    echo Xu ly that bai. Hay kiem tra loi phia tren.
    pause
)
