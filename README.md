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

- Python 3.8+
- FFmpeg
- Windows 10/11

## Installation

### 1. Install FFmpeg

FFmpeg is required for audio processing. Choose one method:

**Option A: Using winget (recommended)**
```bash
winget install FFmpeg
```

**Option B: Using Chocolatey**
```bash
choco install ffmpeg
```

**Option C: Manual installation**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH

Verify installation:
```bash
ffmpeg -version
```

### 2. Install Speech2Text

```bash
# Clone the repository
git clone https://github.com/AdrienSourdille/Speech_2_Text_4_free.git
cd Speech_2_Text_4_free

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
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

### Auto-start with Windows

To start Speech2Text automatically when you log in:
```bash
install_autostart.bat
```

To remove from startup:
```bash
remove_autostart.bat
```

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
