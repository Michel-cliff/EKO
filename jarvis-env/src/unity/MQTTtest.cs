
using System;
using System.Text;
using System.Threading.Tasks;
using MQTTnet;
using MQTTnet.Client;
using UnityEngine;

public class MQTTTest : MonoBehaviour
{
    private IMqttClient client;

    async void Start()
    {
        Debug.Log("🚀 Starting MQTT test...");

        var factory = new MqttFactory();
        client = factory.CreateMqttClient();

        var options = new MqttClientOptionsBuilder()
            .WithTcpServer("127.0.0.1", 1883)
            .WithCleanSession()
            .Build();

        client.ApplicationMessageReceivedAsync += e =>
        {
            Debug.Log($"📩 Received: {Encoding.UTF8.GetString(e.ApplicationMessage.Payload)}");
            return Task.CompletedTask;
        };

        await client.ConnectAsync(options);
        Debug.Log("✅ Connected to MQTT broker!");

        await client.SubscribeAsync("unity/test");
        Debug.Log("📡 Subscribed to unity/test");

        // publish test
        var msg = new MqttApplicationMessageBuilder()
            .WithTopic("unity/test")
            .WithPayload("Hello from Unity!")
            .Build();

        await client.PublishAsync(msg);
    }
}
