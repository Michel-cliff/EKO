# main.py
import numpy as np
import time
from wakeword import WakeWordDetector
from speechtotext import transcribe_audio, record_command
from texttospeech import speak
from aicore import ask_mistral
from myqtt_client import UnityMQTTClient

fs = 16000  # sample rate

# Initialize MQTT client for Unity
try:
    mqtt_client = UnityMQTTClient(topic="/jarvis/commands")
    print("MQTT client initialized")
except Exception as e:
    print(f"Failed to initialize MQTT client: {e}")
    mqtt_client = None

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
            if mqtt_client:
                success = mqtt_client.send_command("render", {
                    "text": text,
                    "response": response
                })
                if not success:
                    print("Failed to send message to Unity")
            else:
                print("No MQTT client available")
    except KeyboardInterrupt:
        print("Conversation ended.")
    except Exception as e:
        print(f"Error in interaction: {e}")

# Initialize wake word detector
try:
    detector = WakeWordDetector(keyword="jarvis")
    detector.on_wake = start_interaction
    detector.listen()
except Exception as e:
    print(f"Failed to initialize wake word detector: {e}")

# Cleanup on exit
import atexit
atexit.register(lambda: mqtt_client.disconnect() if mqtt_client else None)