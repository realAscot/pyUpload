#!/usr/bin/env python3

# © 2025 Adam Skotarczak (adam@skotarczak.net)
# Dieses Softwarepaket darf nicht ohne Genehmigung weiterverbreitet werden!
#
# Version 1.0.2 (22.04.2025 - virtuelle Umgebung korrekt aktiviert)
# Manuel in z.B VS-Code: .\app\.venv\Scripts\activate

import os
import sys
import subprocess

# Pfade definieren
os.chdir(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, ".venv")
VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe") if os.name == "nt" else os.path.join(VENV_DIR, "bin", "python")
REQUIREMENTS_FILE = os.path.join(BASE_DIR, "requirements.txt")

# Wenn wir NICHT in der venv sind
if sys.prefix == sys.base_prefix:
    # venv erstellen falls nötig
    if not os.path.exists(VENV_DIR):
        print("[Setup] Virtuelle Umgebung wird erstellt...")
        subprocess.run([sys.executable, "-m", "venv", "--copies", VENV_DIR], check=True)

        print("[Setup] requirements.txt wird installiert...")
        subprocess.run([VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([VENV_PYTHON, "-m", "pip", "install", "-r", REQUIREMENTS_FILE], check=True)

    # unabhängig davon: Neustart innerhalb der venv
    print("[Setup] Starte erneut mit aktivierter Umgebung...")

    if os.name == "nt":
      subprocess.Popen([VENV_PYTHON] + sys.argv, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
      os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)
      sys.exit(0)

# Wir sind jetzt sicher in der richtigen Umgebung → Rest des Programms geht hier weiter:

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
# Virtuelle Umgebung aktivieren (wenn nicht aktiv)
# -------------------------------------------------------------------

def activate_venv():
    if sys.prefix != os.path.abspath(VENV_DIR):
        venv_path = os.path.join(os.path.dirname(__file__), VENV_DIR)
        if os.name == "nt":
            activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        else:
            activate_script = os.path.join(venv_path, "bin", "activate")
        if os.path.exists(activate_script):
            print(f"Aktiviere virtuelle Umgebung: {VENV_DIR}")
            os.system(f'"{activate_script}"')
        else:
            print(f"FEHLER: Virtuelle Umgebung nicht gefunden ({VENV_DIR}). Bitte zuerst install.cmd ausführen.")
            sys.exit(1)

# -------------------------------------------------------------------
# Globale Konfigurationen & Logging
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
# HTTP-Handler für Upload und Logging
# -------------------------------------------------------------------

class SecureHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        client_ip = self.client_address[0]
        message = format % args
        if client_ip not in client_loggers:
            logger = logging.getLogger(f'client_{client_ip}')
            logger.setLevel(logging.INFO)
            client_log_file = os.path.join(LOG_DIR, f"{client_ip}.log")
            handler = logging.FileHandler(client_log_file)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            logger.addHandler(handler)
            client_loggers[client_ip] = logger
        client_loggers[client_ip].info(message)
        central_logger.info(f"{client_ip} - {message}")

    def send_html_response(self, filename):
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
        if self.path == '/':
            self.send_html_response("template.html")
        else:
            self.send_error(404, "Seite nicht gefunden")
            self.log_message('404 Not Found: %s', self.path)

    def do_POST(self):
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
                    if filename:
                        file_path = os.path.join(client_upload_dir, os.path.basename(filename))
                        with open(file_path, "wb") as f:
                            f.write(file_data.rstrip(b"\r\n--"))
                        self.log_message(f"Datei {filename} erfolgreich hochgeladen.")
                        found_file = True
            if not found_file:
                self.send_error(400, "Keine Datei im Upload enthalten")
                self.log_message('400 Bad Request: Keine Datei übermittelt')
                return
            self.send_html_response("success.html")
        except Exception as e:
            self.log_message(f"Fehler: {e}")
            self.send_error(500, "Interner Serverfehler")

# -------------------------------------------------------------------
# HTTPS-Server mit selbstsigniertem Zertifikat
# -------------------------------------------------------------------

def generate_self_signed_cert(cert_file, key_file):
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
# Server starten (mit oder ohne GUI)
# -------------------------------------------------------------------

def run_server_nogui(port):
    httpd = create_https_server(port)
    server_ip = get_server_ip()
    try:
        print(f"Starte HTTPS-Server auf https://{server_ip}:{port}")
        print("Drücke STRG+C, um zu beenden.")
        print("warte auf Verbindungen ...")
        print(f"Öffne im Browser: https://{server_ip}:{port}")
        print("Du musst Dich im gleichen Netzwerk befinden (LAN/WLAN)")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSTRG+C erkannt. Fahre Server herunter...")
    except Exception as e:
        print(f"Fehler aufgetreten: {e}")
        logging.error("Serverfehler", exc_info=True)
    finally:
        httpd.server_close()
        logging.shutdown()
        print("Server wurde sauber beendet.")

def run_server_with_gui(port):
    import qrcode
    import webbrowser
    from PIL import Image, ImageTk
    import tkinter as tk

    httpd = create_https_server(port)
    server_ip = get_server_ip()
    url = f"https://{server_ip}:{port}"

    def server_thread():
        try:
            print(f"Starte HTTPS-Server auf {url}")
            httpd.serve_forever()
        except Exception as ex:
            print(f"Server-Thread-Exception: {ex}")
        finally:
            httpd.server_close()
            logging.shutdown()

    threading.Thread(target=server_thread, daemon=True).start()

    root = tk.Tk()
    root.title("pyUpload - Secure File Upload")

    try:
        root.iconbitmap("favicon.ico")
    except Exception as e:
        print(f"Konnte das Icon nicht setzen: {e}")

    labels = [
        tk.Label(root, text="HTTPS-Upload-Server läuft!", font=("Arial", 14)),
        tk.Label(root, text=f"IP-Adresse: {server_ip}", font=("Arial", 11)),
        tk.Label(root, text=f"Port: {port}", font=("Arial", 11)),
        tk.Label(root, text="Scanne den QR-Code:", font=("Arial", 11))
    ]

    max_width, total_height = 0, 20
    for label in labels:
        label.pack(pady=5)
        label.update_idletasks()
        max_width = max(max_width, label.winfo_reqwidth())
        total_height += label.winfo_reqheight() + 10

    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    img_tk = ImageTk.PhotoImage(img_qr)

    tk.Label(root, image=img_tk).pack()
    total_height += img_tk.height() + 20

    label_copyright = tk.Label(root, text="Adam Skotarczak (C) 2025", font=("Arial", 9), fg="gray")
    label_copyright.pack(pady=5)
    total_height += label_copyright.winfo_reqheight() + 10

    def open_browser(event):
        webbrowser.open("https://www.ionivation.com/pyUpload")

    link_label = tk.Label(root, text="Infos: www.ionivation.com/pyUpload", font=("Arial", 10), fg="blue", cursor="hand2")
    link_label.pack()
    link_label.bind("<Button-1>", open_browser)
    total_height += link_label.winfo_reqheight() + 10

    tk.Button(root, text="Beenden", command=root.destroy, font=("Arial", 10)).pack(pady=10)
    root.geometry(f"{max_width + 40}x{total_height + 50}")
    root.mainloop()

# -------------------------------------------------------------------
# Kommandozeilenparser & Einstiegspunkt
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
