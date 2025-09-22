# test_commands.py
from myqtt_client import UnityMQTTClient
import time

client = UnityMQTTClient(topic="/jarvis/commands")

# Test sequence
commands = [
    "create a cube",
    "rotate the cube around y axis",
    "make the cube red", 
    "create a sphere",
    "make sphere bigger",
    "rotate sphere forever"
]

for cmd in commands:
    client.send_command("voice_command", {"text": cmd})
    time.sleep(3)  # Wait between commands