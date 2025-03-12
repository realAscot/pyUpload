
## exe erstellen:

### pyinstaller

pip install pyinstaller
pyinstaller --onefile --add-data "template.html;." --add-data "success.html;." --add-data "favicon.ico;." --windowed --icon favicon.ico pyUpload.py
pyinstaller --add-data "template.html;." --add-data "success.html;." --add-data "favicon.ico;." --windowed --icon favicon.ico pyUpload.py

### nuitka

python setup.py build
nuitka --standalone --onefile --enable-plugin=tk-inter --windows-console-mode=disable --windows-icon-from-ico=favicon.ico pyUpload.py



## requirements.txt:

pipreqs . --force