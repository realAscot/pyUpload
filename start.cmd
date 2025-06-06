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

:: Verzeichnis von start.cmd ermitteln
set SCRIPT_DIR=%~dp0

:: Starte den Python-Wrapper, der .venv erkennt
if exist app\.venv\Scripts\python.exe (
    python.exe "%SCRIPT_DIR%start.pyw" %*
) else (
    echo Erste Initialisierung erforderlich.
    echo Starte Setup-Konsole...
    start cmd /k python.exe "%SCRIPT_DIR%start.pyw" %*
)
