import os
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
PICO_VOICE=os.getenv("PICO_VOICE")
MQTT_BROKER="127.0.0.1"
MQTT_PORT=1883