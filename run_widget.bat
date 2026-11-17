@echo off
cd /d "%~dp0"
if exist "%~dp0DesktopWidget.exe" (
    start "" "%~dp0DesktopWidget.exe"
) else if exist "%~dp0dist\DesktopWidget.exe" (
    start "" "%~dp0dist\DesktopWidget.exe"
) else (
    start "" pythonw "%~dp0widget.py"
)
