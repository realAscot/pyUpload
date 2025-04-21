import subprocess, os
os.chdir(os.path.dirname(__file__))
subprocess.run(["python", "app/main.py"])
