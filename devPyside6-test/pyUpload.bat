@echo off
setlocal

:: Prüfen, ob die virtuelle Umgebung existiert
if not exist venv (
    echo Fehler: Die virtuelle Umgebung existiert nicht!
    echo Führe zuerst "install.bat" aus.
    pause
    exit /b
)

:: Aktivieren der virtuellen Umgebung
call venv\Scripts\activate

:: Starte den Upload-Server
python pyUpload.py
