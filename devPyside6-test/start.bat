@echo off
setlocal

:: Prüfen, ob die virtuelle Umgebung existiert
if not exist venv (
    echo Virtuelle Umgebung nicht gefunden! Bitte zuerst install.bat ausführen.
    pause
    exit /b
)

:: Aktivieren der virtuellen Umgebung
call venv\Scripts\activate

:: Starten des Upload-Servers
python pyUpload.py

:: Nach Beenden der Anwendung
deactivate
