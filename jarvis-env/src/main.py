# main.py
import numpy as np
import sounddevice as sd
import threading
import time
from wakeword import WakeWordDetector
from speechtotext import transcribe_audio, record_command
from texttospeech import speak
from aicore import ask_mistral
from myqtt_client import UnityMQTTClient
from queue import Queue

fs = 16000  # sample rate

# Initialize MQTT client for Unity
mqtt_client = UnityMQTTClient()

# Override wake-word callback
def start_interaction(audio_buffer):
    print("Wake word detected! Listening...")

    try:
        while True:
            # Convert raw buffer -> numpy array
            audio_np = record_command()
    
            # STT: real-time transcription
            text = transcribe_audio(audio_np)
            print("You said:", text)
    
            # Skip empty audio
            if np.max(np.abs(audio_np)) < 500:
                break
            
            if not text.strip():
                continue
                        
            # AI core
            response = ask_mistral(text)
            print("Jarvis:", response)
            
            # TTS
            speak(response)
            
            # Send to Unity
            mqtt_client.send_command("render", {
                "text": text,
                "response": response
            })
    except KeyboardInterrupt:
        print("Conversation ended.")

# Initialize wake word detector
detector = WakeWordDetector(keyword="jarvis")
detector.on_wake = start_interaction
detector.listen()
