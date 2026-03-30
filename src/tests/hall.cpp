#include <Arduino.h>

const int HALL_PIN = 2; // Dein Pin laut Schaltplan
volatile int magnetErkannt = 0;

// Diese Funktion wird in Millisekunden aufgerufen, wenn der Magnet vorbeifliegt
void IRAM_ATTR countPulse() {
  magnetErkannt++;
}

void setup() {
  Serial.begin(115200);
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);
  Serial.println("Warte auf Magneten...");
}

void loop() {
  if (magnetErkannt > 0) {
    Serial.print("Magnet erkannt! Zähler: ");
    Serial.println(magnetErkannt);
    magnetErkannt = 0; // Zähler zurücksetzen für den nächsten Durchlauf
  }
  delay(100);
}