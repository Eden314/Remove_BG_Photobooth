@echo off
setlocal EnableExtensions
title Cai dat AI Tach Phong - BiRefNet

echo ==============================================
echo       CAI DAT AI TACH PHONG - WINDOWS
echo ==============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python trong PATH.
    echo Hay cai Python 64-bit va tick "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo [1/4] Kiem tra Python...
python -c "import sys,struct; print('Python:',sys.version.split()[0]); print('Architecture:',struct.calcsize('P')*8,'bit')"

python -c "import struct; raise SystemExit(0 if struct.calcsize('P')*8==64 else 1)"
if errorlevel 1 (
    echo.
    echo [LOI] Python hien tai KHONG phai ban 64-bit.
    echo Hay cai Python 64-bit roi chay lai.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/4] Nang cap pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [LOI] Khong the nang cap pip.
    pause
    exit /b 1
)

echo.
echo [3/4] Cai cac thu vien AI...
echo.

python -m pip uninstall -y onnxruntime onnxruntime-gpu
if errorlevel 1 (
    echo [LOI] Khong the go ONNX Runtime cu.
    pause
    exit /b 1
)

python -m pip install --upgrade --only-binary=:all: pillow numpy "onnxruntime-gpu[cuda,cudnn]"
if errorlevel 1 (
    echo.
    echo ==============================================
    echo [LOI] CAI THU VIEN THAT BAI
    echo ==============================================
    echo.
    echo Khong tu dong bao cai dat thanh cong.
    echo Hay gui phan loi o tren cho ChatGPT.
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Kiem tra...
python -c "from PIL import Image; import numpy,onnxruntime; print('Pillow: OK'); print('NumPy:',numpy.__version__); print('ONNX Runtime:',onnxruntime.__version__); print('Providers:',onnxruntime.get_available_providers())"

if errorlevel 1 (
    echo.
    echo [LOI] Thu vien da cai nhung khong the import.
    echo.
    pause
    exit /b 1
)

echo.
echo ==============================================
echo       CAI DAT THANH CONG!
echo ==============================================
echo.
echo Bay gio ban co the keo thu muc anh vao:
echo RUN_REMOVE_BG.bat
echo Mo hinh birefnet-portrait se duoc tai trong lan xu ly dau tien.
echo.
echo ==============================================
pause
