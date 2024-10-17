#include <WiFi.h>
#include <PubSubClient.h>

const char *ssid = "123_home";
const char *password = NULL; // secret password

const char *mqtt_broker = "10.100.9.197";
const char *topic = "temperature";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void on_message(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("--------------------");
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to 123_home!");

  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(on_message);
  while (!client.connected()) {
    String client_id = "esp32-client-";
    client_id += String(WiFi.macAddress());
    if (client.connect(client_id.c_str())) {
      Serial.println("Connected to RasPi MQTT broker");
    } else {
      Serial.print("Failed to connect to RasPi MQTT broker with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  client.subscribe(topic);
  client.publish(topic, "Hello from ESP32!");
}

void loop() {
  client.loop();
}
