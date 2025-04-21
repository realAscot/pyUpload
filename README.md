# pyUpload (TKInter Version)

![pyUpload 1.0 Logo](./assets/logo-1.0-alpha.png)

## ⚠️ Projektstatus: Eingefroren – Nur noch Bugfixes  

Diese Version von **pyUpload** wird **nicht weiterentwickelt** und erhält nur noch Fehlerbehebungen.  
Die neue Version mit Flask-Backend ist **BALD** verfügbar unter:  

🔗 **<https://github.com/realAscot/pyUpload2>**

---

## pyUpload – Sicherer Datei-Upload-Server über HTTPS (lokal & offline)

Diese Version basiert auf **Tkinter (GUI + QR)** sowie einer optionalen **reinen CLI-Nutzung**.  
Sie ist vollständig lokal lauffähig – ganz ohne Installation von externen Tools oder komplexen Abhängigkeiten.

---

## 🛠 Features

- **HTTPS-gesicherter Datei-Upload**
- **Selbstsigniertes SSL-Zertifikat bei Bedarf**
- **QR-Code-basierte Verbindung für Smartphones**
- **Client-spezifische Verzeichnisse und Logs**
- **GUI und Konsolen-Modus verfügbar**
- **automatische Einrichtung von `.venv` und Abhängigkeiten**
- **kein Installationsskript mehr nötig – alles passiert beim Start von `main.py`**

---

## 🚀 Schnellstart

### ▶️ Für Windows:

1. Lade das Projekt herunter oder klone es:  

   ```sh

   git clone https://github.com/realAscot/pyUpload
   ```

2. Starte die App mit:  

   ```cmd
   start.cmd
   ```

   Alternativ in PowerShell:  

   ```powershell
   cmd /c start.cmd
   ```

   ⚠️ **Alternative 2 falls die Ausführung per Doppelklick auf .bat oder .cmd gesperrt ist:**  

   > Doppelklick auf -> `start.pyw`  

   Es ist möglich das beim ersten mal gefragt wird womit das Programm gestartet werden soll.
   Einfach die Python-Installation suchen und `python.exe` wählen.  

### 🐧 Für Linux / macOS:

1. Stelle sicher, dass Python 3.8+ installiert ist:

   ```bash
   python3 --version
   ```

2. Mache das Startscript ausführbar:

   ```bash
   chmod +x start.sh
   ```

3. Starte die App:

   ```bash
   ./start.sh
   ```

---

Beim ersten Start wird automatisch:

- eine virtuelle Umgebung `.venv/` im `app/`-Verzeichnis erzeugt
- `requirements.txt` installiert
- das Programm danach neu aus der Umgebung gestartet

---

## 🧩 Kommandozeilenoptionen

```sh
python app\main.py --nogui     # Start ohne GUI / QR
python app\main.py --port 9999 # Custom-Port verwenden
```

---

## 🌐 Zugriff im Browser

Sobald gestartet:

```https
https://<lokale-IP>:4443
```

Alternativ QR-Code scannen (GUI-Modus).  
Dateien werden im `upload/<Client-IP>/` gespeichert.

---

## 📁 Logs & Uploads

- **Uploads**: im Ordner `upload/` nach Client-IP
- **Zentrale Logs**: `logs/pyupload.log`
- **Pro-Client Logs**: `logs/<Client-IP>.log`

---

## 🔐 Hinweis zur SSL-Zertifikatswarnung

Beim ersten Aufruf im Browser erscheint eine Warnung wegen des selbstsignierten Zertifikats.  
Du kannst:

- auf **„Erweitert“ > „Trotzdem fortfahren“** klicken
- eigene Zertifikate in `cert.pem` und `key.pem` hinterlegen

---

## 👨‍💻 Autor

- **Adam Skotarczak**  
  Kontakt: [adam@skotarczak.net](mailto:adam@skotarczak.net)  
  GitHub: [realAscot](https://github.com/realAscot)

---

## 📝 Lizenz

- Proprietär, © 2025 Adam Skotarczak  
  **Keine Weitergabe ohne ausdrückliche Genehmigung**
