using UnityEngine;
public class MQTTTester : MonoBehaviour
{
    // Reference to the MQTT client script
    public MQTTClientUnity mqttClient;

    // Topic to publish to
    public string testTopic = "/jarvis/commands";

    void Start()
    {
        // Ensure we have a reference
        if (mqttClient == null)
        {
            // Try to find it in the scene
            mqttClient = FindObjectOfType<MQTTClientUnity>();
            if (mqttClient == null)
            {
                Debug.LogError("MQTTClientUnity not found in scene!");
                return;
            }
        }

        // Simulate a test message after a delay
        Invoke("SendTestMessage", 2.0f);
    }

    void SendTestMessage()
    {
        string testMessage = "{\"action\": \"test\", \"value\": 567}";
        mqttClient.PublishMessage(testTopic, testMessage);
        Debug.Log("Test message sent: " + testMessage);
    }

    // Optional: Handle incoming messages (if subscribed)
    public void OnMQTTMessageReceived(string topic, string message)
    {
        Debug.Log($"Received message on {topic}: {message}");
    }
}