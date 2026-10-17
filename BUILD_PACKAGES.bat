@echo off
setlocal
title Build AI Tach Phong Packages
cd /d "%~dp0"

echo ==============================================
echo   BUILD 2 GOI PORTABLE DOC LAP - WINDOWS x64
echo ==============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [LOI] May build can Python 3.10 x64.
    pause
    exit /b 1
)

python -c "import sys,struct; raise SystemExit(0 if sys.version_info[:2]==(3,10) and struct.calcsize('P')==8 else 1)"
if errorlevel 1 (
    echo [LOI] Hay build bang Python 3.10 x64.
    pause
    exit /b 1
)

if not exist "%USERPROFILE%\.u2net\birefnet-general.onnx" (
    echo [LOI] Khong tim thay model: %USERPROFILE%\.u2net\birefnet-general.onnx
    echo Hay tai model birefnet-general truoc khi dong goi.
    pause
    exit /b 1
)

if not exist ".portable-build-env\Scripts\python.exe" (
    echo Tao moi truong build rieng...
    python -m venv --system-site-packages .portable-build-env
    if errorlevel 1 goto :error
)

echo Cai cong cu build vao moi truong rieng...
".portable-build-env\Scripts\python.exe" -m pip install --only-binary=:all: pyinstaller onnx==1.18.0 onnxruntime-gpu==1.23.2
if errorlevel 1 goto :error

echo Tao hai goi portable. Can khoang 10 GB dung luong trong.
".portable-build-env\Scripts\python.exe" build_portable.py
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
