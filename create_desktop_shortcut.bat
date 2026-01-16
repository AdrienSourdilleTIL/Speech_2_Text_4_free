@echo off
REM Creates a desktop shortcut for Speech2Text

set "DESKTOP=%USERPROFILE%\Desktop"
set "SCRIPT_DIR=%~dp0"
set "SHORTCUT=%DESKTOP%\Speech2Text.lnk"

REM Create VBS script to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\createshortcut.vbs"
echo sLinkFile = "%SHORTCUT%" >> "%TEMP%\createshortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\createshortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_DIR%start_silent.bat" >> "%TEMP%\createshortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\createshortcut.vbs"
echo oLink.Description = "Speech to Text Assistant" >> "%TEMP%\createshortcut.vbs"
echo oLink.Save >> "%TEMP%\createshortcut.vbs"

cscript //nologo "%TEMP%\createshortcut.vbs"
del "%TEMP%\createshortcut.vbs"

echo.
echo Desktop shortcut created: %SHORTCUT%
echo.
echo TIP: Right-click the shortcut, go to Properties, and set a
echo "Shortcut key" (e.g., Ctrl+Alt+S) to launch with keyboard!
echo.
pause
