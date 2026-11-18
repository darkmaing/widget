@echo off
cd /d "%~dp0"
taskkill /f /im DesktopWidget.exe >nul 2>&1
taskkill /f /im DesktopWidget.old.exe >nul 2>&1
if exist "%~dp0DesktopWidget.old.exe" del /f /q "%~dp0DesktopWidget.old.exe" >nul 2>&1
if exist "%~dp0DesktopWidget.exe" (
    start "" "%~dp0DesktopWidget.exe"
) else if exist "%~dp0dist\DesktopWidget.exe" (
    start "" "%~dp0dist\DesktopWidget.exe"
) else (
    start "" pythonw "%~dp0widget.py"
)
