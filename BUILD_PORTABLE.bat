@echo off
setlocal
title Build AI Tach Phong Portable
cd /d "%~dp0"

echo ==============================================
echo    BUILD GOI PORTABLE - KHONG CAN PYTHON MAY DICH
echo ==============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [LOI] May build can Python 3.10 x64 va cac thu vien cua du an.
    pause
    exit /b 1
)

python -c "import sys,struct; raise SystemExit(0 if sys.version_info[:2]==(3,10) and struct.calcsize('P')==8 else 1)"
if errorlevel 1 (
    echo [LOI] Hay chay build bang Python 3.10 x64 va moi truong co Pillow, NumPy, ONNX Runtime GPU.
    pause
    exit /b 1
)

if not exist "%USERPROFILE%\.u2net\birefnet-general.onnx" (
    echo [LOI] Khong tim thay model da tai: %USERPROFILE%\.u2net\birefnet-general.onnx
    echo Hay chay ung dung Python voi model birefnet-general mot lan de tai model truoc.
    pause
    exit /b 1
)

if not exist ".portable-build-env\Scripts\python.exe" (
    echo Tao moi truong build rieng...
    python -m venv --system-site-packages .portable-build-env
    if errorlevel 1 goto :error
)

echo Cai PyInstaller va cong cu chuyen model FP16 vao moi truong build rieng...
".portable-build-env\Scripts\python.exe" -m pip install --only-binary=:all: pyinstaller onnx==1.18.0 onnxruntime-gpu==1.23.2
if errorlevel 1 goto :error

echo Tao goi portable. Qua trinh nay co the mat vai phut va can khoang 5 GB trong.
".portable-build-env\Scripts\python.exe" build_portable.py
if errorlevel 1 goto :error

echo.
echo BUILD THANH CONG:
echo %CD%\dist\AI_Tach_Phong
echo Hay nen ca thu muc AI_Tach_Phong de chuyen sang may Windows x64 khac.
echo.
pause
exit /b 0

:error
echo.
echo [LOI] Build that bai. Hay gui noi dung loi phia tren de kiem tra.
pause
exit /b 1
