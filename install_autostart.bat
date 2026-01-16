@echo off
REM Creates a shortcut in the Windows Startup folder to auto-start Speech2Text

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SCRIPT_DIR=%~dp0"
set "SHORTCUT=%STARTUP%\Speech2Text.lnk"

REM Create VBS script to make shortcut (Windows doesn't have native shortcut creation)
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
echo Speech2Text has been added to Windows Startup.
echo It will now start automatically when you log in.
echo.
echo To remove, delete: %SHORTCUT%
echo Or run: remove_autostart.bat
echo.
pause
