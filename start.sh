#!/bin/bash

# Verzeichnis dieser Datei bestimmen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python-Interpreter prüfen
if ! command -v python3 &> /dev/null; then
  echo "[Fehler] Python 3 ist nicht installiert."
  echo "Bitte installiere es über deine Paketverwaltung (z.B. apt, dnf, brew)."
  exit 1
fi

# Starte das Hauptskript
python3 "$SCRIPT_DIR/app/main.py" "$@"
