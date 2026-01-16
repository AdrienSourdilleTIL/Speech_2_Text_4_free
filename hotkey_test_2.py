import sounddevice as sd
import numpy as np
import whisper
import wavio
import tempfile
import keyboard

fs = 44100  # sample rate

model = whisper.load_model("small")

print("Press and hold Ctrl+Space to speak. Release to transcribe.")

while True:
    # Wait for hotkey press
    keyboard.wait('ctrl+space')
    print("Recording... Speak now!")

    recording = []

    # Record while key is held
    while keyboard.is_pressed('ctrl+space'):
        chunk = sd.rec(int(0.5 * fs), samplerate=fs, channels=1)  # 0.5s chunks
        sd.wait()
        recording.append(chunk)

    audio_data = np.concatenate(recording, axis=0)
    print("Recording stopped. Transcribing...")

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
        wavio.write(filename, audio_data, fs, sampwidth=2)

    # Transcribe
    result = model.transcribe(filename)
    print("Transcribed text:")
    print(result["text"])
    print("-" * 40)
