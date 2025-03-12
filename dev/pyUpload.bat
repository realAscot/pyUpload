@echo off
setlocal
goto code

(C) 2025 Adam Scotarczak

options for pyUpload.py:

usage: pyUpload.py [-h] [--port PORT] [--nogui]

  -h, --help       show this help message and exit
  --port, -p PORT  Port, auf dem der Server lauscht (Standard: 4443)
  --nogui, -n      Ohne GUI & QR-Code im reinen CLI-Modus starten

:code
:: Prüfen, ob die virtuelle Umgebung existiert
if not exist .venv (
    echo Virtuelle Umgebung nicht gefunden! Bitte zuerst install.bat ausführen.
    pause
    exit /b
)

:: Aktivieren der virtuellen Umgebung
call .venv\Scripts\activate
echo "Virtuelle Umgebung gestartet!"

:: Starten des Upload-Servers mit Übergabe aller übergebenen Parameter
python pyUpload.py %*

:: Nach Beenden der Anwendung
deactivate

echo "Virtuelle Umgebung beendet!"
