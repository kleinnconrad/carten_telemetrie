#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 4; // Dein Pin laut Schaltplan

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Temperatur-Test gestartet.");
}

void loop() {
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  
  Serial.print("Aktuelle Temperatur: ");
  Serial.print(temp);
  Serial.println(" °C");
  
  delay(1000);
}