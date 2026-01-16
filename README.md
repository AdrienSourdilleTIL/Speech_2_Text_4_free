# Speech_2_Text_4_free

A lightweight, local speech-to-text assistant using OpenAI's Whisper model. Hold a hotkey to speak, release to transcribe, and the text is automatically copied to your clipboard.

## Features

- **Hold-to-record**: Press and hold Ctrl+Space to record audio
- **Auto-transcribe**: Release to transcribe using Whisper
- **Clipboard integration**: Transcribed text is automatically copied
- **Local processing**: All transcription happens on your machine
- **Background mode**: Run silently without a terminal window
- **Graceful exit**: Press ESC to quit

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
pip install openai-whisper sounddevice keyboard pyperclip scipy numpy
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
1. Wait for the Whisper model to load
2. Hold **Ctrl+Space** and speak
3. Release to transcribe
4. Text is copied to clipboard - paste anywhere with Ctrl+V
5. Press **ESC** to exit

To stop the background process, press ESC or use Task Manager.

## Configuration

Edit the config section in `hotkey_whisper.py`:

```python
MODEL_NAME = "medium"   # tiny, base, small, medium, large
SAMPLE_RATE = 16000     # Audio sample rate
HOTKEY = "ctrl+space"   # Record hotkey
EXIT_KEY = "esc"        # Exit hotkey
```

## License

MIT License
