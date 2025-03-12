.PHONY: exe release clean

# Variablen
PYTHON = python3
SCRIPT = pyUpload.py
EXE_NAME = pyUpload
BUILD_DIR = build
DIST_DIR = release
REQ_FILE = requirements.txt

exe:
	@echo "Erzeuge ausführbare Datei..."
	@mkdir -p $(BUILD_DIR)
	pyinstaller --onefile --add-data "template.html;." --add-data "success.html;." --add-data "favicon.ico;." --windowed --icon favicon.ico --name $(EXE_NAME) $(SCRIPT)
	@mv dist/$(EXE_NAME) $(BUILD_DIR)/
	@echo "Erstellung abgeschlossen: $(BUILD_DIR)/$(EXE_NAME)"

release: exe
	@echo "Erstelle Release-Paket..."
	@mkdir -p $(DIST_DIR)
	@cp $(BUILD_DIR)/$(EXE_NAME) $(DIST_DIR)/
	@cp $(REQ_FILE) $(DIST_DIR)/
	@cp template.html success.html favicon.ico $(DIST_DIR)/
	@echo "Release-Paket bereit in $(DIST_DIR)"

zip: release
	@echo "Erstelle ZIP-Archiv..."
	@cd $(DIST_DIR) && zip -r ../$(ZIP_NAME) $(EXE_NAME) template.html success.html favicon.ico
	@echo "ZIP-Archiv erstellt: $(ZIP_NAME)"

clean:
	@echo "Bereinige Projektverzeichnis..."
	@rm -rf $(BUILD_DIR) $(DIST_DIR) build dist __pycache__ *.spec
	@echo "Bereinigung abgeschlossen."

