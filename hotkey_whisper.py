import threading
import keyboard
import sounddevice as sd
import numpy as np
import whisper
import time
import sys
import tempfile
import scipy.io.wavfile as wavfile
import pyperclip
import os
from PIL import Image, ImageDraw
import pystray
import winsound

# ---------------- CONFIG ----------------
MODEL_NAME = "medium"   # step 2: better accuracy
SAMPLE_RATE = 16000
HOTKEY = "ctrl+space"
EXIT_KEY = "ctrl+shift+esc"
SOUND_ENABLED = True    # Enable/disable audio feedback
# ----------------------------------------

# Detect if running in background mode (no console)
BACKGROUND_MODE = not sys.stdout or not sys.stdout.isatty()

def log(message):
    """Print only if console is available."""
    if not BACKGROUND_MODE:
        print(message)

# ---------------- SOUND FEEDBACK ----------------
SOUND_SAMPLE_RATE = 44100

def generate_tone(frequency, duration, volume=0.3):
    """Generate a simple sine wave tone."""
    t = np.linspace(0, duration, int(SOUND_SAMPLE_RATE * duration), False)
    tone = np.sin(2 * np.pi * frequency * t) * volume
    # Apply fade in/out to avoid clicks
    fade_samples = int(SOUND_SAMPLE_RATE * 0.01)
    tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
    tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return tone.astype(np.float32)

def play_sound(sound_type):
    """Play a sound based on type. Uses Windows system sounds."""
    if not SOUND_ENABLED:
        return

    try:
        if sound_type == 'recording_start':
            # Device connect sound
            winsound.PlaySound("DeviceConnect", winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif sound_type == 'recording_stop':
            # Device disconnect sound
            winsound.PlaySound("DeviceDisconnect", winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif sound_type == 'transcription_complete':
            # Notification sound (pleasant chime)
            winsound.PlaySound("Notification.Default", winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif sound_type == 'error':
            # System exclamation
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    except Exception:
        pass  # Silently fail if sound doesn't work

log("Loading Whisper model...")
model = whisper.load_model(MODEL_NAME)

running = True
recording = False
transcribing = False
audio_buffer = []
tray_icon = None

# ---------------- TRAY ICON ----------------
def create_icon(color):
    """Create a simple colored circle icon."""
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse([4, 4, size-4, size-4], fill=color)
    return image

def update_tray_icon(status):
    """Update tray icon based on status."""
    global tray_icon
    if tray_icon is None:
        return

    colors = {
        'loading': (128, 128, 128),   # Gray - loading
        'ready': (0, 200, 0),         # Green - ready
        'recording': (255, 0, 0),     # Red - recording
        'transcribing': (255, 165, 0) # Orange - transcribing
    }

    tooltips = {
        'loading': 'Speech2Text - Loading...',
        'ready': 'Speech2Text - Ready (Ctrl+Space or click)',
        'recording': 'Speech2Text - Recording...',
        'transcribing': 'Speech2Text - Transcribing...'
    }

    tray_icon.icon = create_icon(colors.get(status, (128, 128, 128)))
    tray_icon.title = tooltips.get(status, 'Speech2Text')

def on_tray_click(icon, item):
    """Handle tray icon click - toggle recording."""
    global recording
    if transcribing:
        return  # Don't start recording while transcribing

    if recording:
        recording = False
    else:
        on_hotkey_press()

def on_tray_quit(icon, item):
    """Handle quit from tray menu."""
    exit_program()


def audio_callback(indata, frames, time_info, status):
    if recording:
        audio_buffer.append(indata.copy())


def record_audio():
    global recording, audio_buffer

    audio_buffer = []
    recording = True
    update_tray_icon('recording')
    play_sound('recording_start')
    log("Recording... Speak now!")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback
    ):
        while recording and running:
            time.sleep(0.05)

    play_sound('recording_stop')
    log("Recording stopped. Transcribing...")
    process_audio()


def process_audio():
    global transcribing

    if not audio_buffer:
        log("No audio captured.")
        play_sound('error')
        update_tray_icon('ready')
        return

    transcribing = True
    update_tray_icon('transcribing')

    try:
        audio = np.concatenate(audio_buffer, axis=0)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wavfile.write(f.name, SAMPLE_RATE, audio)
            result = model.transcribe(
                f.name,
                language="en",
                temperature=0.0,
                fp16=False
            )

        text = result["text"].strip()
        pyperclip.copy(text)

        log("\nTranscribed text (copied to clipboard):")
        log(text)
        log("-" * 40)

        play_sound('transcription_complete')
    except Exception as e:
        log(f"Transcription error: {e}")
        play_sound('error')
    finally:
        transcribing = False
        update_tray_icon('ready')


def on_hotkey_press():
    if not recording and running:
        threading.Thread(target=record_audio, daemon=True).start()


def on_hotkey_release():
    global recording
    recording = False


def exit_program():
    global running, recording, tray_icon
    log("\nExiting cleanly...")
    running = False
    recording = False
    if tray_icon:
        tray_icon.stop()
    time.sleep(0.2)
    sys.exit(0)


# ---------------- HOTKEYS ----------------
keyboard.on_press_key("space", lambda e: on_hotkey_press() if keyboard.is_pressed("ctrl") else None)
keyboard.on_release_key("space", lambda e: on_hotkey_release())

keyboard.add_hotkey(EXIT_KEY, exit_program)

log("Hold Ctrl+Space to speak. Release to transcribe.")
log("Press Ctrl+Shift+ESC to exit.")

# ---------------- TRAY ICON SETUP ----------------
def setup_tray():
    global tray_icon

    menu = pystray.Menu(
        pystray.MenuItem("Quit", on_tray_quit)
    )

    tray_icon = pystray.Icon(
        "Speech2Text",
        create_icon((0, 200, 0)),  # Start green (ready)
        "Speech2Text - Ready",
        menu
    )

    # Left-click to toggle recording
    tray_icon.default_action = on_tray_click

    return tray_icon

# ---------------- MAIN ----------------
update_tray_icon('ready')
log("System tray icon active. Click to record, right-click for menu.")

icon = setup_tray()
icon.run()
