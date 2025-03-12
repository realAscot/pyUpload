import sys
import os
import threading
import socket
import ssl
import qrcode
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import ImageQt


# --- HTTPS Server Klasse ---
class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>pyUpload Server</h1><p>Upload-Seite</p></body></html>")
        else:
            self.send_error(404)


def get_local_ip():
    """Ermittelt die lokale IP-Adresse"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def run_server(port):
    """Startet den HTTPS-Server in einem eigenen Thread"""
    server_address = ("", port)
    httpd = HTTPServer(server_address, SecureHTTPRequestHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Server läuft auf https://{get_local_ip()}:{port}")
    httpd.serve_forever()


# --- PySide6 GUI ---
class UploadGUI(QWidget):
    def __init__(self, server_ip, port):
        super().__init__()
        self.setWindowTitle("pyUpload - Secure File Upload")
        self.setGeometry(100, 100, 400, 500)

        # Info Label
        label_info = QLabel("HTTPS-Upload-Server läuft!", self)
        label_info.setAlignment(Qt.AlignCenter)
        
        label_ip = QLabel(f"IP-Adresse: {server_ip}", self)
        label_ip.setAlignment(Qt.AlignCenter)

        label_port = QLabel(f"Port: {port}", self)
        label_port.setAlignment(Qt.AlignCenter)

        label_hint = QLabel("Scanne den QR-Code:", self)
        label_hint.setAlignment(Qt.AlignCenter)

        # QR-Code generieren
        url = f"https://{server_ip}:{port}"
        qr = qrcode.make(url)
        qr = qr.convert("RGB")  # FIX: Konvertiere das Bild in ein gültiges Format für ImageQt
        qr_img = ImageQt.ImageQt(qr)
        pixmap = QPixmap.fromImage(qr_img)
        qr_label = QLabel(self)
        qr_label.setPixmap(pixmap)
        qr_label.setAlignment(Qt.AlignCenter)


        # Link Label (klickbar)
        link_label = QLabel(f'<a href="{url}">{url}</a>', self)
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignCenter)

        # Beenden Button
        btn_quit = QPushButton("Beenden", self)
        btn_quit.clicked.connect(self.close)

        # Layout setzen
        layout = QVBoxLayout()
        layout.addWidget(label_info)
        layout.addWidget(label_ip)
        layout.addWidget(label_port)
        layout.addWidget(label_hint)
        layout.addWidget(qr_label)
        layout.addWidget(link_label)
        layout.addWidget(btn_quit)

        self.setLayout(layout)


# --- Start der Anwendung ---
if __name__ == "__main__":
    port = 4443
    server_ip = get_local_ip()

    # HTTPS-Server in eigenem Thread starten
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    # Qt-Anwendung starten
    app = QApplication(sys.argv)
    window = UploadGUI(server_ip, port)
    window.show()
    sys.exit(app.exec())
