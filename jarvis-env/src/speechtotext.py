import whisper
import sounddevice as sd
import numpy as np
import torch

fs = 16000  # sample rate

# Automatically select device and fastest model
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# Model selection: tiny for speed, small if more accuracy desired
MODEL_NAME = "small" # options: tiny, base, small, medium, large
model = whisper.load_model(MODEL_NAME).to(DEVICE)
print(f"Loaded Whisper model: {MODEL_NAME}")

def transcribe_audio(audio_data: np.ndarray) -> str:
  # Whisper expects float32 PCM normalized to [-1, 1]
  audio_float = audio_data.astype(np.float32) / 32768.0
  result = model.transcribe(audio_float, fp16=False, language='en')
  return result["text"]

def record_command(duration=5):
    """Record voice command for given duration (seconds)."""
    print("🎤 Listening for your command...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    return audio.flatten()