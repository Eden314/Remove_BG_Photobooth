@echo off
title AI Tach Phong Anh

if "%~1"=="" (
    echo.
    echo KE THU MUC ANH VAO FILE NAY.
    echo.
    pause
    exit /b
)

python "%~dp0remove_background.py" "%~1" %2 %3 %4 %5

if errorlevel 1 (
    echo.
    echo Co loi. Hay chay INSTALL.bat truoc.
    pause
)
