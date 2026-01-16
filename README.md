# Speech_2_Text_4_free

A lightweight, local speech-to-text assistant using OpenAI's Whisper model. Hold a hotkey to speak, release to transcribe, and the text is automatically copied to your clipboard.

## Features

- **Hold-to-record**: Press and hold Ctrl+Space to record audio
- **Auto-transcribe**: Release to transcribe using Whisper
- **Clipboard integration**: Transcribed text is automatically copied
- **Local processing**: All transcription happens on your machine
- **Background mode**: Run silently without a terminal window
- **System tray icon**: Visual status indicator with click-to-record
- **Audio feedback**: Sound cues for recording start, stop, and completion
- **Graceful exit**: Press Ctrl+Shift+ESC or right-click tray → Quit

## Requirements

- Python 3.x
- FFmpeg (must be installed and in PATH)
- Windows (uses `keyboard` library for global hotkeys)

## Installation

```bash
# Clone the repository
git clone https://github.com/AdrienSourdille/Speech_2_Text_4_free.git
cd Speech_2_Text_4_free

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install openai-whisper sounddevice keyboard pyperclip scipy numpy pystray pillow
```

## Usage

### With console (for debugging)
```bash
.venv\Scripts\activate
python hotkey_whisper.py
```

### Background mode (no window)
Double-click `start_silent.bat` or run it from command line.

### Controls
1. Wait for the Whisper model to load (tray icon appears green when ready)
2. Hold **Ctrl+Space** OR **click the tray icon** to start recording (icon turns red)
3. Release to transcribe (icon turns orange)
4. Text is copied to clipboard - paste anywhere with Ctrl+V (icon returns to green)
5. Press **Ctrl+Shift+ESC** or right-click tray icon → **Quit** to exit

### Tray Icon Colors
- **Gray**: Loading model
- **Green**: Ready
- **Red**: Recording
- **Orange**: Transcribing

## Configuration

Edit the config section in `hotkey_whisper.py`:

```python
MODEL_NAME = "medium"   # tiny, base, small, medium, large
SAMPLE_RATE = 16000     # Audio sample rate
HOTKEY = "ctrl+space"   # Record hotkey
EXIT_KEY = "ctrl+shift+esc"  # Exit hotkey
SOUND_ENABLED = True    # Enable/disable audio feedback
```

## License

MIT License
