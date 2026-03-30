#include <Arduino.h>
#include <HardwareSerial.h>

const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

HardwareSerial SerialGPS(2); // UART 2

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN); // 9600 ist Standard für GPS
  Serial.println("Warte auf GPS Rohdaten...");
}

void loop() {
  // Wenn das GPS-Modul Daten sendet, drucke sie sofort in den Monitor
  while (SerialGPS.available()) {
    char c = SerialGPS.read();
    Serial.print(c);
  }
}