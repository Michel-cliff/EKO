import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT

class UnityMQTTClient:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, topic="jarvis/commands"):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.topic = topic

    def send_command(self, action, data):
        """Send a command to Unity via MQTT."""
        payload = {"action": action, "data": data}
        self.client.publish(self.topic, json.dumps(payload))