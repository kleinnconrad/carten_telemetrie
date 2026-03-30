#include <Arduino.h>

// Beim ESP32 ist die interne blaue LED oft an Pin 2
const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ESP32 lebt und startet den Test!");
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // LED an
  Serial.println("LED AN");
  delay(1000);                 // 1 Sekunde warten
  
  digitalWrite(LED_PIN, LOW);  // LED aus
  Serial.println("LED AUS");
  delay(1000);
}