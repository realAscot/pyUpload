@echo off
setlocal

:: Prüfen, ob Python installiert ist
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Fehler: Python ist nicht installiert oder nicht im PATH!
    echo Bitte installiere Python und starte die Installation erneut.
    pause
    exit /b 1
)

:: Python-Version prüfen (Mindestversion 3.8)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    if %%a LSS 3 (
        echo Fehler: Python 3.8 oder höher ist erforderlich!
        pause
        exit /b 1
    )
    if %%a==3 if %%b LSS 8 (
        echo Fehler: Python 3.8 oder höher ist erforderlich!
        pause
        exit /b 1
    )
)

:: Virtuelle Umgebung erstellen, falls sie nicht existiert
if not exist .venv (
    echo Erstelle virtuelle Server-Umgebung ...
    python -m venv --copies .venv
    if %ERRORLEVEL% NEQ 0 (
        echo Fehler beim Erstellen der virtuellen Umgebung!
        pause
        exit /b 2
    )
)

:: Aktivieren der virtuellen Umgebung
call .venv\Scripts\activate

:: Installieren der Abhängigkeiten
echo Installiere Abhaengigkeiten aus dem Internet ...
pip install --no-warn-script-location --disable-pip-version-check -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Fehler beim Installieren der Abhaengigkeiten!
    pause
    exit /b 3
)

:: Erfolgsmeldung
echo.
echo Installation abgeschlossen.
timeout /t 3 >nul  & exit /b 0
