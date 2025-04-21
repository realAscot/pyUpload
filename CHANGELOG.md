# CHANGELOG

## pyUpload (TKInter-Version 1.0)




- 2025-04-21  

  - Geändert  
    - `main.py` übernimmt nun automatisch die Erstellung der virtuellen Umgebung `.venv` und die Installation der Abhängigkeiten aus `requirements.txt`  
    - Entfernt: `install.cmd` und `startUpload.cmd` wurden vollständig ersetzt durch neue Startlogik  
    - `start.cmd` wurde vereinfacht, prüft nun auf vorhandenes `python` und startet `main.py` über absoluten Pfad  
    - `main.py` setzt bei Start automatisch `os.chdir()` auf das eigene Verzeichnis, um relative Pfade sicher zu behandeln  

  - Hinzugefügt  
    - Neue plattformunabhängige `start.sh` für Linux/macOS  
    - Automatischer Restart nach Installation über `os.execv()` in `main.py`  
    - Neue Sicherheits- und Netzwerkinformationen in der `README.md`  
    - Erweiterung der `README.md` um Speicherort der Uploads und Projektstruktur  
    - Hinweis auf Projektstatus und neue Version unter <https://github.com/realAscot/pyUpload2>  
    - Neue LICENSE-Datei (proprietär, nicht zur Weitergabe)  
    - start.py hinzugefügt wenn auf manchen Systemen die Ausführung von .cmd und .bat gesperrt sind.

  - Fixes  
    - PowerShell-Inkompatibilitäten mit `set /p` entfernt  
    - `.cmd`-Startskripte reagieren jetzt korrekt auf STRG+C  
    - Mehrere Markdown-Korrekturen (Codeblöcke, Leerzeilen, Lesbarkeit)  
