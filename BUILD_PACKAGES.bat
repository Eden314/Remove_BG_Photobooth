@echo off
setlocal
title Build AI Tach Phong Packages
cd /d "%~dp0"

echo ==============================================
echo   BUILD 2 GOI PORTABLE DOC LAP - WINDOWS x64
echo ==============================================
echo.

set "BUILD_PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%BUILD_PYTHON%" set "BUILD_PYTHON=python"
"%BUILD_PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] May build can Python 3.12 x64.
    pause
    exit /b 1
)

"%BUILD_PYTHON%" -c "import sys,struct; raise SystemExit(0 if sys.version_info[:2]==(3,12) and struct.calcsize('P')==8 else 1)"
if errorlevel 1 (
    echo [LOI] Hay build bang Python 3.12 x64.
    pause
    exit /b 1
)

if not exist "%USERPROFILE%\.u2net\birefnet-general.onnx" (
    echo [LOI] Khong tim thay model: %USERPROFILE%\.u2net\birefnet-general.onnx
    echo Hay tai model birefnet-general truoc khi dong goi.
    pause
    exit /b 1
)

if not exist ".directml-build-env\Scripts\python.exe" (
    echo Tao moi truong build rieng...
    "%BUILD_PYTHON%" -m venv .directml-build-env
    if errorlevel 1 goto :error
)

echo Cai cong cu build vao moi truong rieng...
".directml-build-env\Scripts\python.exe" -m pip install --only-binary=:all: pyinstaller pillow numpy onnx==1.18.0 onnxruntime-directml==1.24.4
if errorlevel 1 goto :error

echo Tao hai goi portable DirectML. Can khoang 4 GB dung luong trong.
".directml-build-env\Scripts\python.exe" build_portable.py
if errorlevel 1 goto :error

echo.
echo DA TAO:
echo %CD%\dist\Remove_BG
echo %CD%\dist\Photobooth
echo Moi goi la doc lap va can giai nen day du tren may Windows x64.
echo.
pause
exit /b 0

:error
echo.
echo [LOI] Build that bai. Hay gui noi dung loi phia tren de kiem tra.
pause
exit /b 1
