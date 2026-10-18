@echo off
setlocal
title Install Photobooth Source Runtime
cd /d "%~dp0"

echo ==============================================
echo       CAI MOI TRUONG PHOTOBOOTH
echo ==============================================
echo.

set "BASE_PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%BASE_PYTHON%" set "BASE_PYTHON=python"

"%BASE_PYTHON%" -c "import sys,struct; raise SystemExit(0 if sys.version_info[:2]==(3,12) and struct.calcsize('P')==8 else 1)"
if errorlevel 1 (
    echo [LOI] Can Python 3.12 x64 trong PATH hoac duong dan mac dinh.
    echo Cai Python 3.12 x64 roi chay lai INSTALL.bat.
    pause
    exit /b 1
)

if not exist ".photobooth-env\Scripts\python.exe" (
    echo Tao moi truong Python rieng cho Photobooth...
    "%BASE_PYTHON%" -m venv .photobooth-env
    if errorlevel 1 goto :error
)

echo Cai thu vien vao .photobooth-env...
".photobooth-env\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".photobooth-env\Scripts\python.exe" -m pip install --only-binary=:all: pillow numpy onnxruntime-directml==1.24.4
if errorlevel 1 goto :error

echo.
echo CAI DAT XONG.
echo Chay RUN_PHOTOBOOTH_WATCH.bat voi duong dan thu muc anh.
echo Model se tu tai trong lan chay dau tien, can ket noi Internet.
echo Moi truong rieng: .photobooth-env
echo.
pause
exit /b 0

:error
echo.
echo [LOI] Cai dat that bai. Hay kiem tra ket noi Internet va loi phia tren.
pause
exit /b 1
