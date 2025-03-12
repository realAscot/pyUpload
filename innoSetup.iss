; Define AppVersion as a constant
#define AppVersion "1.0.0"
#define BasePath ".\dev"

; Source: "{#BasePath}\*"; DestDir: "{app}"; Flags: ignoreversion;


[Setup]
AppId={{832B3E5D-14BC-4823-A911-00C9B79AD040}
AppName=pyUpload
AppVersion={#AppVersion}
AppVerName=pyUpload {#AppVersion} (win)
AppPublisher=Adam Skotarczak (ionivation.com)
AppPublisherURL=https://www.ionivation.com/pyupload/
AppSupportURL=https://www.ionivation.com/pyupload/
AppUpdatesURL=https://www.ionivation.com/pyupload/
DefaultDirName={userappdata}\pyUpload
DisableProgramGroupPage=yes
LicenseFile={#BasePath}\LICENSE
PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=pyUpload-Setup-{#AppVersion}
SolidCompression=yes
WizardStyle=modern
SetupIconFile={#BasePath}\favicon.ico
DisableDirPage=yes

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#BasePath}\pyUpload.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#BasePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{app}\upload"; Flags: uninsalwaysuninstall

[Icons]
Name: "{autoprograms}\pyUpload"; Filename: "{app}\pyUpload.bat"; IconFilename: "{app}\favicon.ico";
Name: "{autodesktop}\pyUpload"; Filename: "{app}\pyUpload.bat"; IconFilename: "{app}\favicon.ico"; Tasks: desktopicon
Name: "{userdesktop}\pyUpload-Uploads"; Filename: "{app}\upload"; IconFilename: "{app}\favicon.ico"; Tasks: desktopicon


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\install.bat"; Parameters: ""; WorkingDir: "{app}\"; Flags: waituntilterminated
;Flags: runhidden

Filename: "{app}\pyUpload.bat"; Description: "{cm:LaunchProgram,pyUpload}"; Flags: shellexec postinstall skipifsilent

[Code]
function IsPythonInstalled(): Boolean;
var
  PythonPath: String;
  ResultCode: Integer;
begin
  // Prüfe Registry für alle möglichen Python-Versionen (dynamisch)
  if RegQueryStringValue(HKLM, 'SOFTWARE\Python\PythonCore', '', PythonPath) or
     RegQueryStringValue(HKLM, 'SOFTWARE\WOW6432Node\Python\PythonCore', '', PythonPath) then
  begin
    Result := True;
    Exit;
  end;

  // Prüfe mit python --version, falls kein Registry-Eintrag gefunden wurde
  Result := Exec('cmd.exe', '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

function InitializeSetup(): Boolean;
begin
  if not IsPythonInstalled() then
  begin
    MsgBox('Python ist nicht installiert oder nicht erreichbar! Bitte installiere Python.', mbError, MB_OK);
    Result := False;  // Installation abbrechen
  end
  else
  begin
    Result := True;
  end;
end;

