#!/usr/bin/env python3

# © 2025 Adam Skotarczak (adam@skotarczak.net)
# Dieses Softwarepaket darf nicht ohne Genehmigung weiterverbreitet werden!
# Version 1.2.2 (05.03.2025)

import os
import sys
import ssl
import logging
import socket
import argparse
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# -------------------------------------------------------------------
# Globale Konfigurationen & Verzeichnisse
# -------------------------------------------------------------------
UPLOAD_DIR = 'upload'
LOG_DIR = 'logs'
CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'
CENTRAL_LOG_FILE = os.path.join(LOG_DIR, 'pyupload.log')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.FileHandler(CENTRAL_LOG_FILE), logging.StreamHandler()]
)

central_logger = logging.getLogger("central_logger")
client_loggers = {}

# -------------------------------------------------------------------
# HTTP-Request-Handler
# -------------------------------------------------------------------
class SecureHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Sammelt Log-Einträge in Client-spezifische Dateien und die Zentrale-Logdatei."""
        client_ip = self.client_address[0]
        message = format % args

        # Einmalig pro Client-IP einen dedizierten Logger anlegen.
        if client_ip not in client_loggers:
            logger = logging.getLogger(f'client_{client_ip}')
            logger.setLevel(logging.INFO)
            client_log_file = os.path.join(LOG_DIR, f"{client_ip}.log")
            handler = logging.FileHandler(client_log_file)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            logger.addHandler(handler)
            client_loggers[client_ip] = logger

        # In den Client-spezifischen Logger und in den zentralen Logger schreiben.
        client_loggers[client_ip].info(message)
        central_logger.info(f"{client_ip} - {message}")

    def send_html_response(self, filename):
        """Liefert eine HTML-Datei als HTTP-Response zurück."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(500, "HTML-Template nicht gefunden")

    def do_GET(self):
        """Ausliefern der Upload-Seite (template.html)."""
        if self.path == '/':
            self.send_html_response("template.html")
        else:
            self.send_error(404, "Seite nicht gefunden")
            self.log_message('404 Not Found: %s', self.path)

    def do_POST(self):
        """Behandelt Datei-Uploads (multipart/form-data) direkt als Stream."""
        try:
            content_type = self.headers.get('Content-Type')
            content_length = int(self.headers.get('Content-Length', 0))

            if not content_type or 'multipart/form-data' not in content_type:
                self.send_error(400, "Ungültiger Content-Type")
                self.log_message('400 Bad Request: Ungültiger Content-Type')
                return

            if content_length == 0:
                self.send_error(400, "Leere Anfrage erhalten")
                self.log_message('400 Bad Request: Leere Anfrage')
                return

            client_ip = self.client_address[0]
            client_upload_dir = os.path.join(UPLOAD_DIR, client_ip)
            os.makedirs(client_upload_dir, exist_ok=True)

            boundary = content_type.split("boundary=")[-1].encode()
            raw_data = self.rfile.read(content_length)
            parts = raw_data.split(b"--" + boundary)

            found_file = False

            for part in parts:
                if b"Content-Disposition" in part:
                    headers, file_data = part.split(b"\r\n\r\n", 1)
                    filename_start = headers.find(b'filename="') + 10
                    filename_end = headers.find(b'"', filename_start)
                    filename = headers[filename_start:filename_end].decode()

                    if filename:  # Falls tatsächlich ein Dateiname vorhanden ist
                        file_path = os.path.join(client_upload_dir, os.path.basename(filename))
                        with open(file_path, "wb") as f:
                            # Entferne das trailing CRLF oder "--"
                            f.write(file_data.rstrip(b"\r\n--"))
                        self.log_message(f"Datei {filename} erfolgreich hochgeladen.")
                        found_file = True

            if not found_file:
                self.send_error(400, "Keine Datei im Upload enthalten")
                self.log_message('400 Bad Request: Keine Datei übermittelt')
                return

            # Erfolgsseite senden
            self.send_html_response("success.html")

        except Exception as e:
            self.log_message(f"Fehler: {e}")
            self.send_error(500, "Interner Serverfehler")

# -------------------------------------------------------------------
# HTTPS-Server-Setup
# -------------------------------------------------------------------
def generate_self_signed_cert(cert_file, key_file):
    """Erzeugt ein selbstsigniertes SSL-Zertifikat, falls keines vorhanden ist."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "DE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Berlin"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Berlin"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ionivation.com"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost.lan"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False
        )
        .sign(key, hashes.SHA256())
    )

    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(key_file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def get_server_ip():
    """Bestimmt die lokale IP-Adresse, um sie z.B. für den QR-Code zu nutzen."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def create_https_server(port, handler_class=SecureHTTPRequestHandler):
    """Erzeugt ein HTTPS-Serverobjekt (aber startet ihn noch nicht)."""
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("SSL-Zertifikat nicht gefunden. Erstelle selbstsigniertes Zertifikat...")
        generate_self_signed_cert(CERT_FILE, KEY_FILE)
        print("Selbstsigniertes SSL-Zertifikat erstellt.")

    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    return httpd

# -------------------------------------------------------------------
# Startfunktionen (GUI / no-GUI)
# -------------------------------------------------------------------
def run_server_nogui(port):
    httpd = create_https_server(port)
    server_ip = get_server_ip()

    try:
        print(f"Starte HTTPS-Server auf https://{server_ip}:{port}")
        print("Drücke STRG+C, um zu beenden.")
        print("warte auf Verbindungen ... \n")
        print(f"Öffne im Browser: https://{server_ip}:{port}")
        print("Du musst Dich im gleichen Netzwerk befinden (Lan/ Wlan)")
        httpd.serve_forever()

    except KeyboardInterrupt:
        # Nur eine kurze Meldung ausgeben und dann sauber herunterfahren
        print("\nSTRG+C erkannt. Fahre Server herunter...")

    except Exception as e:
        print(f"Fehler aufgetreten: {e}")
        logging.error("Serverfehler", exc_info=True)

    finally:
        httpd.server_close()
        logging.shutdown()
        print("Server wurde sauber beendet.")


def run_server_with_gui(port):
    # Nur für QR-Code und GUI benötigt:
    import qrcode
    import webbrowser
    from PIL import Image, ImageTk
    import tkinter as tk

    """Startet den Server in einem Hintergrund-Thread und öffnet eine tkinter-GUI mit QR-Code."""
    # 1) Erzeuge den Server (aber noch kein serve_forever).
    httpd = create_https_server(port)
    server_ip = get_server_ip()
    url = f"https://{server_ip}:{port}"

    # 2) Hintergrund-Thread starten
    def server_thread():
        try:
            print(f"Starte HTTPS-Server auf {url}")
            httpd.serve_forever()
        except Exception as ex:
            print(f"Server-Thread-Exception: {ex}")
        finally:
            httpd.server_close()
            logging.shutdown()

    t = threading.Thread(target=server_thread, daemon=True)
    t.start()

    # 3) tkinter-GUI aufbauen
    root = tk.Tk()
    root.title("pyUpload - Secure File Upload")

    # Favicon setzen (nur unter Windows direkt mit .ico möglich)
    try:
        root.iconbitmap("favicon.ico")
    except Exception as e:
        print(f"Konnte das Icon nicht setzen: {e}")

    # Labels erzeugen
    labels = [
        tk.Label(root, text="HTTPS-Upload-Server läuft!", font=("Arial", 14)),
        tk.Label(root, text=f"IP-Adresse: {server_ip}", font=("Arial", 11)),
        tk.Label(root, text=f"Port: {port}", font=("Arial", 11)),
        tk.Label(root, text="Scanne den QR-Code:", font=("Arial", 11))
    ]

    # Alle Labels packen und größte Breite ermitteln
    max_width = 0
    total_height = 20  # Grundhöhe als Puffer für Abstände
    for label in labels:
        label.pack(pady=5)
        label.update_idletasks()  # Breite und Höhe berechnen
        max_width = max(max_width, label.winfo_reqwidth())
        total_height += label.winfo_reqheight() + 10  # Höhe sammeln

    # QR-Code generieren
    url = f"https://{server_ip}:{port}"
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")

    # QR-Code als Tkinter-Image einbinden
    img_tk = ImageTk.PhotoImage(img_qr)
    label_qr = tk.Label(root, image=img_tk)
    label_qr.pack()
    total_height += img_tk.height() + 20

    # Copyright-Vermerk
    label_copyright = tk.Label(root, text="Adam Skotarczak (C) 2025", font=("Arial", 9), fg="gray")
    label_copyright.pack(pady=5)
    total_height += label_copyright.winfo_reqheight() + 10

    # Funktion für klickbaren Link
    def open_browser(event):
        webbrowser.open("https://www.ionivation.com/pyUpload")

    # Klickbarer Link unter Copyright
    link_label = tk.Label(root, text="Infos: www.ionivation.com/pyUpload", font=("Arial", 10), fg="blue", cursor="hand2")
    link_label.pack()
    link_label.bind("<Button-1>", open_browser)
    total_height += link_label.winfo_reqheight() + 10

    # Funktion zum Beenden
    def on_quit():
        root.destroy()

    # Beenden-Button
    btn_quit = tk.Button(root, text="Beenden", command=on_quit, font=("Arial", 10))
    btn_quit.pack(pady=10)
    total_height += btn_quit.winfo_reqheight() + 20

    # Endgültige Fenstergröße setzen
    root.geometry(f"{max_width + 40}x{total_height + 50}")

    # 4) GUI-Loop starten
    root.mainloop()

# -------------------------------------------------------------------
# Hauptprogramm mit CLI
# -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Secure file upload server with optional GUI/QR-Code.")
    parser.add_argument("--port", "-p", type=int, default=4443, help="Port, auf dem der Server lauscht (Standard: 4443)")
    parser.add_argument("--nogui", "-n", action="store_true", help="Ohne GUI & QR-Code im reinen CLI-Modus starten")
    
    args = parser.parse_args()
    print(f"Gestartet mit Port {args.port}, GUI: {not args.nogui}")

    if args.nogui:
        run_server_nogui(args.port)
    else:
        run_server_with_gui(args.port)

if __name__ == "__main__":
    main()
