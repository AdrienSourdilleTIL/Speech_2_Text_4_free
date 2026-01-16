import threading
import keyboard
import sounddevice as sd
import numpy as np
import whisper
import time
import sys
import tempfile
import scipy.io.wavfile as wavfile

# ---------------- CONFIG ----------------
MODEL_NAME = "medium"   # step 2: better accuracy
SAMPLE_RATE = 16000
HOTKEY = "ctrl+space"
EXIT_KEY = "esc"
# ----------------------------------------

print("Loading Whisper model...")
model = whisper.load_model(MODEL_NAME)

running = True
recording = False
audio_buffer = []


def audio_callback(indata, frames, time_info, status):
    if recording:
        audio_buffer.append(indata.copy())


def record_audio():
    global recording, audio_buffer

    audio_buffer = []
    recording = True
    print("Recording... Speak now!")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback
    ):
        while recording and running:
            time.sleep(0.05)

    print("Recording stopped. Transcribing...")
    process_audio()


def process_audio():
    if not audio_buffer:
        print("No audio captured.")
        return

    audio = np.concatenate(audio_buffer, axis=0)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavfile.write(f.name, SAMPLE_RATE, audio)
        result = model.transcribe(
            f.name,
            language="en",
            temperature=0.0,
            fp16=False
        )

    print("\nTranscribed text:")
    print(result["text"].strip())
    print("-" * 40)


def on_hotkey_press():
    if not recording and running:
        threading.Thread(target=record_audio, daemon=True).start()


def on_hotkey_release():
    global recording
    recording = False


def exit_program():
    global running, recording
    print("\nExiting cleanly...")
    running = False
    recording = False
    time.sleep(0.2)
    sys.exit(0)


# ---------------- HOTKEYS ----------------
keyboard.on_press_key("space", lambda e: on_hotkey_press() if keyboard.is_pressed("ctrl") else None)
keyboard.on_release_key("space", lambda e: on_hotkey_release())

keyboard.on_press_key(EXIT_KEY, lambda e: exit_program())

print("Hold Ctrl+Space to speak. Release to transcribe.")
print("Press ESC to exit.")

# ---------------- MAIN LOOP ----------------
while running:
    time.sleep(0.1)
