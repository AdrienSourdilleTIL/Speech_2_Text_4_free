# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important

Always update README.md and CLAUDE.md when making significant changes to the codebase.

## Project Overview

Speech_2_Text_4_free is a hotkey-activated speech-to-text application using OpenAI's Whisper model. Users hold Ctrl+Space to record audio, release to transcribe, and the transcribed text is automatically copied to the clipboard.

## Running the Application

```bash
# With console (for debugging)
.venv\Scripts\activate
python hotkey_whisper.py

# Background mode (no window) - double-click or run:
start_silent.bat
```

## Dependencies

Key packages (installed in .venv):
- `openai-whisper` - Speech recognition model
- `sounddevice` - Audio recording
- `keyboard` - Global hotkey detection
- `pyperclip` - Clipboard operations
- `scipy` - WAV file handling
- `numpy` - Audio data processing
- `torch` - Whisper backend
- `pystray` - System tray icon
- `pillow` - Icon image generation

## Architecture

Single-file application ([hotkey_whisper.py](hotkey_whisper.py)):

- **Configuration** (lines 15-20): Model name, sample rate, hotkeys, sound toggle
- **Background mode detection** (line 23): Auto-detects if running with pythonw.exe
- **Sound feedback** (lines 31-71): Generated tones for recording start/stop, success, error
- **System tray icon** (lines 82-127): Color-coded status indicator with click-to-record
- **Audio recording**: Uses `sounddevice.InputStream` with callback pattern, stores chunks in `audio_buffer`
- **Transcription**: Writes audio to temp WAV file, calls Whisper's `transcribe()`, copies result to clipboard
- **Hotkey handling**: `keyboard` library binds Ctrl+Space (record toggle) and ESC (exit)

## Key Configuration Variables

```python
MODEL_NAME = "medium"   # Whisper model size (tiny, base, small, medium, large)
SAMPLE_RATE = 16000     # Audio sample rate in Hz
HOTKEY = "ctrl+space"   # Hold to record
EXIT_KEY = "ctrl+shift+esc"  # Exit application
SOUND_ENABLED = True    # Enable/disable audio feedback
```

## Usage Pattern

1. Script loads Whisper model on startup (takes several seconds)
2. System tray icon appears (green = ready)
3. Hold Ctrl+Space OR click tray icon to start recording (icon turns red)
4. Release to stop recording and trigger transcription (icon turns orange)
5. Transcribed text is copied to clipboard, icon returns to green
6. Press Ctrl+Shift+ESC or right-click tray → Quit to exit

**Tray Icon Colors:**
- Gray: Loading model
- Green: Ready
- Red: Recording
- Orange: Transcribing

**Sound Feedback:**
- Recording start: Rising tone
- Recording stop: Falling tone
- Transcription complete: Two-tone chime
- Error: Low buzz

## Project Goal

Create a lightweight, local, always-ready speech-to-text assistant ("SuperWhisperer") with silent background operation.

## Current Status

**Completed:**
- Ctrl+Space hold-to-record, release-to-transcribe
- Clipboard auto-copy of transcribed text
- Ctrl+Shift+ESC graceful exit
- Virtual environment with all dependencies
- FFmpeg installed and working
- Background/silent execution via `start_silent.bat`
- System tray icon with status colors and click-to-record
- Audio feedback (sound cues for recording/transcription states)

**Roadmap:**
1. ~~Basic recording + transcription~~ (done)
2. ~~Clipboard integration~~ (done)
3. ~~Graceful exit~~ (done)
4. ~~Background/silent execution~~ (done) - `start_silent.bat` uses pythonw.exe
5. ~~System tray icon~~ (done) - color status, click to record, right-click to quit
6. **Next: Standalone packaging** (PyInstaller) or global dependency install
7. Optional: Pre-roll listening, latency optimizations, logging
