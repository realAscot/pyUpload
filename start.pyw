#!/usr/bin/env python3

import os
import sys
import subprocess

os.chdir(os.path.dirname(__file__))

# Zielpfad zur venv-Python
venv_python = os.path.join("app", ".venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("app", ".venv", "bin", "python")

# Verwende venv-Python, wenn vorhanden – sonst system-Python für initialen Aufbau
python_exec = venv_python if os.path.exists(venv_python) else sys.executable

# Starte main.py
subprocess.run([python_exec, "app/main.py"] + sys.argv[1:])
