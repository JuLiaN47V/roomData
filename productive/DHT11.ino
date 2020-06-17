#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char* ssid = "XXXX";
const char* password = "XXXX";
const uint16_t port = 8090;
const char * host = "XXXX";
String room = "XXXX";
#include "DHT.h"

#define DHTPIN 5
#define DHTTYPE DHT11
String type = "DHT11";


DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;


void setup() {
  Serial.begin(115200);
  
  delay(10);
  dht.begin();
  Serial.print("Connect to Wifi ");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  client.connect(host, port);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    if (client.connected() == true){
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      
      String typeData = "type " + type;
      delay(100);
      String roomData = " room " + room;
      delay(100);
      String tempData = " temp " + String(t);
      delay(100);
      String humData = " hum " + String(h);
      String data = typeData + roomData + tempData + humData;
      Serial.println(data);
      client.print(data);
      delay(1000);
    } else {
      client.connect(host, port);
    }
  }
}
