#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

const int SD_CS_PIN = 5;

void setup() {
  Serial.begin(115200);
  Serial.println("Initialisiere SD-Karte...");

  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Fehler: SD-Karte nicht gefunden oder falsch verkabelt!");
    return;
  }
  Serial.println("SD-Karte gefunden.");

  // Test-Datei erstellen und schreiben
  File dataFile = SD.open("/test.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Hallo vom ESP32! Die Karte funktioniert.");
    dataFile.close();
    Serial.println("Erfolgreich in test.txt geschrieben.");
  } else {
    Serial.println("Fehler beim Oeffnen der Datei.");
  }
}

void loop() {
  // Hier passiert nichts weiter
}