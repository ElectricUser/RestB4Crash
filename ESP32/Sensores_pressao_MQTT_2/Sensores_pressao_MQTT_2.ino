#include <WiFi.h>
#include <PubSubClient.h>
#include <string.h>
#include <time.h>

int fsrPin1 = 34;  // the FSR and 10K pulldown are connected to a1
int fsrReading1;   // the analog reading from the FSR resistor 1 divider

int fsrPin2 = 35;  // the FSR and 10K pulldown are connected to a2
int fsrReading2;   // the analog reading from the FSR resistor 2 divider

const char* ssid = "OnePlus 6";
const char* password = "12345678";
const char* mqtt_server = "broker.emqx.io";
const char* mqtt_topic2 = "/sensors/initialValues";

const char* mqtt_topic3 = "/sensors/3";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqtt_server, 1883);
}

void connectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client_pub")) {
      Serial.println("connected");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  sleep(18);

  int counter = 0;

  while (counter != 55) {

    client.loop();

    fsrReading1 = analogRead(fsrPin1);

    Serial.print("Analog reading 1 = ");
    Serial.print(fsrReading1);  // print the raw analog reading

    if (fsrReading1 < 10) {
      Serial.println(" - No pressure");
    } else if (fsrReading1 < 100) {
      Serial.println(" - Light touch");
    } else if (fsrReading1 < 230) {
      Serial.println(" - Light squeeze");
    } else if (fsrReading1 < 400) {
      Serial.println(" - Medium squeeze");
    } else {
      Serial.println(" - Big squeeze");
    }
    delay(1000);

    if( counter <= 30){
    String topic2 = "normal:" + String(fsrReading1);

    client.publish(mqtt_topic2, topic2.c_str());
    } else {
    String topic2 = "stress:" + String(fsrReading1);

    client.publish(mqtt_topic2, topic2.c_str());
    }
    
    if (!client.connected()) {
      connectMQTT();
    }

    counter = counter + 1;

    if (counter == 30) {
      sleep(10);
    }
  }
}