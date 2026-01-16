import sounddevice as sd
import numpy as np
import whisper
import tempfile
import wavio

# 1. Set recording parameters
duration = 5  # seconds
fs = 44100    # sample rate

print("Recording for 5 seconds... Speak now!")

# 2. Record audio
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished

print("Recording complete!")

# 3. Save to temporary WAV file
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
    filename = f.name
    wavio.write(filename, audio, fs, sampwidth=2)

# 4. Load Whisper model
model = whisper.load_model("small")  # "small" is fast; "base" or "medium" are other options

# 5. Transcribe audio
result = model.transcribe(filename)

# 6. Print the transcription
print("Transcribed text:")
print(result["text"])