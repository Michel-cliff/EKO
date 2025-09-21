# test_publisher.py
from myqtt_client import UnityMQTTClient
import time

client = UnityMQTTClient(topic="/jarvis/commands")
time.sleep(1)  # Wait for connection

# Send a test message
client.send_command("test", {"message": "Hello Unity!"})