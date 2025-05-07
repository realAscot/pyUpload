# CHANGELOG

## pyUpload (TKInter-Version 1.0)

- **2025-05-07 - v1.2.1**
  - **Geändert:**  
    - [x] `main.py` übergibt beim Neustart unter Linux jetzt einen **absoluten Pfad**, um Doppelpunkte wie `app/app/main.py` zu vermeiden.  
    - [x] `start.pyw` berücksichtigt nun `venv`-Interpreter korrekt, wenn vorhanden, sonst fallback auf `sys.executable`.  
    - [x] Erkennung von fehlendem `ensurepip`, mit Hinweis zur Installation von `python3-venv` bei Bedarf.  
    - [x] Neue Warnung, wenn `tkinter` fehlt – ohne Abbruch, Upload-Server läuft dennoch im CLI-Modus weiter.  
    - [x] README.md ergänzt um Setup-Hinweise für Linux bzgl. `python3-venv` und `python3-tk`.  

---

- **2025-04-28 - v1.2.0**
  - **Geändert:**  
    - [x] `main.py` prüft nun zusätzlich, ob die virtuelle Umgebung auch funktioniert und nicht nur ob sie lediglich vorhanden ist.  

---

- **2025-04-25 - v1.1.0**
  - **Geändert:**  
    - [x] Lizenz auf __MIT__ mit Namensnennung umgestellt, siehe [LICENSE](./LICENSE)  
    - [x] `main.py` prüft nun zusätzlich, ob bereits mit `pythonw.exe` gestartet wurde, um doppelten 
           Start mit neuem Fenster zu vermeiden  
    - [x] `main.py` ruft nach `subprocess.Popen(...)` nun zuverlässig `sys.exit(0)` auf, um „leere“ Ursprungsfenster zu beenden  
    - [x] `start.cmd` verwendet jetzt `python.exe` statt `pythonw.exe`, wodurch nur noch **ein** Konsolenfenster erscheint – auch beim Setup  
    - [x] `start.sh` erkennt fehlendes `python3` und bricht mit Hinweis ab; Pfade werden sauber relativ berechnet

  - **Behoben:**  
    - [x] Mit diesen Änderungen behoben, dass unter Windows unnötige Consolenfenster gestartet werden und der Sprung nun sauber in die Virtuelle Umbebung `./app/.venv` erfolgt.

- **2025-04-22 - v1.0.2**

  - **Behoben:**  
    - [x] Wrapper-Skript `start.py` erkennt nun fehlende `.venv` und startet `main.py` beim Erststart korrekt mit System-Python, danach mit venv (`start.py`).
    - [x] `main.py` verwendet unter Windows statt `os.execv()` nun `subprocess.Popen(..., CREATE_NEW_CONSOLE)` für einen sauberen Neustart mit sichtbarer Konsole (`main.py`).

  - **Entfernt:**  
    -- [x] Nicht mehr benötigte Funktion `activate_venv()` entfernt (`main.py`).

- **2025-04-21 - v1.0.1**  

  - **Geändert:**  
    - [x] `main.py` übernimmt nun automatisch die Erstellung der virtuellen Umgebung `.venv` und die Installation der Abhängigkeiten aus `requirements.txt`  
    - [x] Entfernt: `install.cmd` und `startUpload.cmd` wurden vollständig ersetzt durch neue Startlogik  
    - [x] `start.cmd` wurde vereinfacht, prüft nun auf vorhandenes `python` und startet `main.py` über absoluten Pfad  
    - [x] `main.py` setzt bei Start automatisch `os.chdir()` auf das eigene Verzeichnis, um relative Pfade sicher zu behandeln  

  - **Hinzugefügt:**  
    - [x] Neue plattformunabhängige `start.sh` für Linux/macOS  
    - [x] Automatischer Restart nach Installation über `os.execv()` in `main.py`  
    - [x] Neue Sicherheits- und Netzwerkinformationen in der `README.md`  
    - [x] Erweiterung der `README.md` um Speicherort der Uploads und Projektstruktur  
    - [x] Hinweis auf Projektstatus und neue Version unter <https://github.com/realAscot/pyUpload2>  
    - [x] Neue LICENSE-Datei (proprietär, nicht zur Weitergabe)  
    - [x] start.py hinzugefügt wenn auf manchen Systemen die Ausführung von .cmd und .bat gesperrt sind.

  - **Fixes:**  
    - [x] PowerShell-Inkompatibilitäten mit `set /p` entfernt  
    - [x] `.cmd`-Startskripte reagieren jetzt korrekt auf STRG+C  
    - [x] Mehrere Markdown-Korrekturen (Codeblöcke, Leerzeilen, Lesbarkeit)  

- **2025-04-21 - v1.0.0**  
  - [x] release!  
