# main.py
import numpy as np
import sounddevice as sd
from wakeword import WakeWordDetector
from speechtotext import transcribe_audio, record_command
from texttospeech import speak
from aicore import ask_mistral
# from mqtt_client import UnityMQTTClient

# mqtt_client = UnityMQTTClient()

# Override wake-word callback
def start_interaction(audio_buffer):
    print("Wake word detected! Listening...")

    # Convert raw buffer -> numpy array
    audio_np = record_command()
    # audio_np = np.frombuffer(audio_buffer, dtype=np.int16)

    # STT: real-time transcription
    text = transcribe_audio(audio_np)
    print("You said:", text)

    if text.strip():
        # AI core
        response = ask_mistral(text)
        print("Jarvis:", response)

        # TTS
        speak(response)

        # Send to Unity
        # mqtt_client.send_command("render", {
        #     "text": text,
        #     "response": response
        # })

# Initialize wake word detector
detector = WakeWordDetector(keyword="jarvis")
detector.on_wake = start_interaction
detector.listen()
