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

set "APP=%~dp0Photobooth.exe"
if exist "%APP%" goto :run_portable

set "APP=%~dp0dist\Photobooth\Photobooth.exe"
if exist "%APP%" goto :run_portable

set "PYTHON=%~dp0.photobooth-env\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"
"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python hoac moi truong Photobooth.
    echo Hay cai Python 3.12 x64 va chay INSTALL.bat truoc.
    pause
    exit /b 1
)
if not exist "%~dp0src\photobooth_worker.py" (
    echo [LOI] Khong tim thay ma nguon Photobooth hoac Photobooth.exe.
    pause
    exit /b 1
)

"%PYTHON%" -u "%~dp0src\photobooth_worker.py" "%~1" %2 %3 %4 %5 %6 %7 %8 %9
goto :finished

:run_portable
"%APP%" "%~1" --watch %2 %3 %4 %5 %6 %7 %8 %9

:finished
if errorlevel 1 (
    echo.
    echo Xu ly that bai. Hay kiem tra loi phia tren.
    pause
)
