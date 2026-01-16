@echo off
REM Removes Speech2Text from Windows Startup

set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Speech2Text.lnk"

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo Speech2Text has been removed from Windows Startup.
) else (
    echo Speech2Text was not found in Windows Startup.
)
echo.
pause
