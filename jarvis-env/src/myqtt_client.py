import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT
import time

class UnityMQTTClient:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, topic="/jarvis/commands"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.connected = False
        self.client = mqtt.Client()
        
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        # Connect to broker
        self.connect()
        
    def connect(self):
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            # Start network loop
            self.client.loop_start()
            # Wait for connection
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.1)
                timeout -= 0.1
            if not self.connected:
                print("Connection timeout")
        except Exception as e:
            print(f"Connection failed: {e}")
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("✅ Connected to MQTT Broker!")
        else:
            print(f"❌ Failed to connect, return code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("⚠️ Disconnected from MQTT Broker")
        # Attempt to reconnect
        if rc != 0:
            print("Attempting to reconnect...")
            self.connect()
    
    def send_command(self, action, data):
        """Send a command to Unity via MQTT."""
        if not self.connected:
            print("Not connected to broker, attempting to reconnect...")
            self.connect()
            if not self.connected:
                print("Cannot send message: not connected")
                return False
        
        payload = {"action": action, "data": data}
        json_payload = json.dumps(payload)
        
        try:
            # Publish with QoS=1 for reliability
            result = self.client.publish(self.topic, json_payload, qos=1)
            
            # Check if publish was successful
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"✅ Sent to {self.topic}: {json_payload}")
                return True
            else:
                print(f"❌ Failed to send message: {result.rc}")
                return False
        except Exception as e:
            print(f"❌ Error publishing message: {e}")
            return False
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
        print("Disconnected from MQTT broker")