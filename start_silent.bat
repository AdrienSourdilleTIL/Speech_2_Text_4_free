@echo off
REM Start Speech_2_Text_4_free in background mode (no console window)
REM Uses pythonw.exe from the virtual environment

cd /d "%~dp0"
start "" ".venv\Scripts\pythonw.exe" hotkey_whisper.py
