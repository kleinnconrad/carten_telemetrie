#include <Arduino.h>
#include <HardwareSerial.h>

const int LTE_RX_PIN = 32;
const int LTE_TX_PIN = 33;

HardwareSerial SerialLTE(1); // UART 1

void setup() {
  Serial.begin(115200);
  // Das SIM7000 spricht standardmäßig meist mit 115200 Baud
  SerialLTE.begin(115200, SERIAL_8N1, LTE_RX_PIN, LTE_TX_PIN); 
  
  Serial.println("Sende 'AT' an das Modem...");
  SerialLTE.println("AT"); // AT ist der universelle "Hallo bist du da?" Befehl
}

void loop() {
  // Alles was vom Modem kommt, im PC anzeigen
  if (SerialLTE.available()) {
    Serial.write(SerialLTE.read());
  }
  // Alles was du im Seriellen Monitor tippst, ans Modem schicken
  if (Serial.available()) {
    SerialLTE.write(Serial.read());
  }
}