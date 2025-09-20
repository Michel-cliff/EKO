import paho.mqtt.client as mqtt
import json

class UnityMQTTClient:
    def __init__(self, broker="localhost", port=1883, topic="/jarvis/render"):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.topic = topic

    def send_command(self, command_type, payload):
        message = json.dumps({"cmd": command_type, "payload": payload})
        self.client.publish(self.topic, message)