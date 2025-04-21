@echo off
setlocal
chcp 65001 >nul

:: Prüfen, ob python vorhanden ist
where python >nul 2>nul
if errorlevel 1 (
  echo [Fehler] Python wurde nicht gefunden.
  echo Bitte installiere Python 3.8 oder höher: https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

:: Verzeichnis von start.cmd ermitteln (robust, egal von wo gestartet)
set SCRIPT_DIR=%~dp0

:: Starte die Anwendung direkt aus app\
python "%SCRIPT_DIR%app\main.py" %*

