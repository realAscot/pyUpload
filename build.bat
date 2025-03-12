@echo off
setlocal

:: Variablen
set SCRIPT=pyUpload.py
set EXE_NAME=pyUpload.exe
set BUILD_DIR=build
set DIST_DIR=release
set ZIP_NAME=pyUpload.zip
set REQ_FILE=requirements.txt

:: Liste von Dateien/Ordnern, die beim "clean" entfernt werden sollen
set DELETE_LIST=build dist __pycache__ *.spec *.zip temp_* logs\* cache\* pyUpload.build\* pyUpload.dist\* upload\* *.pem

:: Menü anzeigen
echo Wähle eine Option:
echo 1 - Erstelle ausführbare Datei (exe 1) 
echo 2 - Erstelle Release-Paket (release 1+2)
echo 3 - Erstelle ZIP-Archiv (zip 1+2+3)
echo 4 - Aufraeumen (clean)
set /p CHOICE=Eingabe (1-4): 

if "%CHOICE%"=="1" goto exe
if "%CHOICE%"=="2" goto release
if "%CHOICE%"=="3" goto zip
if "%CHOICE%"=="4" goto clean
echo Ungültige Eingabe!
exit /b

:exe
echo Erzeuge ausführbare Datei...
mkdir %BUILD_DIR% 2>nul
pyinstaller --onefile --add-data "template.html;." --add-data "success.html;." --add-data "favicon.ico;." --windowed --icon favicon.ico --name %EXE_NAME% %SCRIPT%
move dist\%EXE_NAME% %BUILD_DIR%\
echo Erstellung abgeschlossen: %BUILD_DIR%\%EXE_NAME%
exit /b

:release
call :exe
echo Erstelle Release-Paket...
mkdir %DIST_DIR% 2>nul
copy %BUILD_DIR%\%EXE_NAME% %DIST_DIR%\
copy %REQ_FILE% %DIST_DIR%\
copy template.html success.html favicon.ico %DIST_DIR%\
echo Release-Paket bereit in %DIST_DIR%
exit /b

:zip
call :release
echo Erstelle ZIP-Archiv...
powershell Compress-Archive -Path "%DIST_DIR%\%EXE_NAME%", "%DIST_DIR%\template.html", "%DIST_DIR%\success.html", "%DIST_DIR%\favicon.ico" -DestinationPath "%ZIP_NAME%"
echo ZIP-Archiv erstellt: %ZIP_NAME%
exit /b

:clean
echo Bereinige Projektverzeichnis...

:: Durchläuft alle Dateien/Ordner in DELETE_LIST
for %%F in (%DELETE_LIST%) do (
    if exist %%F (
        echo Entferne: %%F
        rmdir /s /q %%F 2>nul || del /q %%F 2>nul
    )
)

echo Bereinigung abgeschlossen.
exit /b
