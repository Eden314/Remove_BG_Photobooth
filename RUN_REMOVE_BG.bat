@echo off
title AI Tach Phong Anh

if "%~1"=="" (
    echo.
    echo KE THU MUC ANH VAO FILE NAY.
    echo.
    pause
    exit /b
)

python -u "%~dp0remove_background.py" "%~1" %2 %3 %4 %5 %6 %7 %8 %9

if errorlevel 1 (
    echo.
    echo Co loi. Hay chay INSTALL.bat truoc.
    pause
)
