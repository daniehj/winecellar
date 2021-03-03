#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define NTP_OFFSET   60 * 60      // In seconds
#define NTP_INTERVAL 60 * 1000    // In miliseconds
#define NTP_ADDRESS  "europe.pool.ntp.org"

#define ONE_WIRE_BUS 4


// Replace with your network credentials
const char* ssid     = "SSID";
const char* password = "PASSWORD";

// REPLACE with your Domain name and URL path or IP address with path
const char* serverName = "http://arctanconsulting.no:8000/records/";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_ADDRESS, NTP_OFFSET, NTP_INTERVAL);

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

uint8_t sensor1[8] = { 0x28, 0xD1, 0x8E, 0x24, 0x09, 0x00, 0x00, 0x74 };
uint8_t sensor2[8] = { 0x28, 0x89, 0x3E, 0x30, 0x09, 0x00, 0x00, 0x82 };
uint8_t sensor3[8] = { 0x28, 0x8B, 0x3F, 0x30, 0x09, 0x00, 0x00, 0x21 };
uint8_t sensor4[8] = { 0x28, 0xF0, 0x49, 0x30, 0x09, 0x00, 0x00, 0xB0 };
uint8_t sensor5[8] = { 0x28, 0x74, 0x40, 0x30, 0x09, 0x00, 0x00, 0x75 };
uint8_t sensor6[8] = { 0x28, 0x4D, 0x52, 0x30, 0x09, 0x00, 0x00, 0xF1 };

uint8_t* sensorArr[] = {sensor1,sensor2,sensor3,sensor4,sensor5,sensor6};
char* loc[] = {"N1","N2","N3","O1","O2","O3"};

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  timeClient.begin();
  sensors.begin();
  
}

void loop() {
  //Check WiFi connection status
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;

    timeClient.update();
    
    // Your Domain name with URL path or IP address with path
    http.begin(serverName);
    
    // Specify content-type header
    http.addHeader("Content-Type", "application/json");
    
    sensors.requestTemperatures();
    
    String formattedDate = timeClient.getFormattedDate();

    Serial.println("");
    Serial.println(formattedDate);
    
    float temp = 0;
    String httpRequestData = "[";
    for (int i = 0;i < 6;i++){
         temp = sensors.getTempC(sensorArr[i]);
         if(temp != -127.00) {
          
              httpRequestData += "{\"temperature\": " + String(temp,2) + ",\"loc\": \"" + loc[i] + "\",\"date\": \"" + formattedDate + "\"},"; 
            
              
            
         }
    }
    httpRequestData = httpRequestData.substring(0,httpRequestData.length() - 1);
    httpRequestData += "]";
    Serial.print("httpRequestData: ");
    Serial.println(httpRequestData);
    
    // Send HTTP POST request
    int httpResponseCode = http.POST(httpRequestData);
     
        
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  //Send an HTTP POST request every 30 seconds
  delay(30000);  
}
