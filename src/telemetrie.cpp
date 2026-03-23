#include <SPI.h>
#include <SD.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- Pin Definitionen ---
const int SD_CS_PIN = 5;
const int ONE_WIRE_BUS = 4;
const int HALL_PIN = 2;

// --- Sensor Setup ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// --- RPM & Timing Variablen ---
volatile unsigned int pulseCount = 0;
unsigned long lastTime = 0;
const int samplingInterval = 500; // Datenerfassung alle 500ms (2 Hz)
int currentRPM = 0;

// --- Dateisystem ---
File dataFile;
const char* fileName = "/telemetry.csv";

// --- Interrupt Service Routine (ISR) ---
// Wird hardwarenah ausgelöst, sobald der Magnet den Sensor passiert
void IRAM_ATTR countPulse() {
  pulseCount++;
}

void setup() {
  Serial.begin(115200);

  // 1. Sensoren initialisieren
  sensors.begin();
  pinMode(HALL_PIN, INPUT_PULLUP);
  // Interrupt an den Hall-Sensor Pin binden
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);

  // 2. SD-Karte initialisieren
  Serial.print("Initialisiere SD-Karte...");
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println(" Fehlgeschlagen! Überprüfe die Verkabelung.");
    return; // Stoppt hier, falls keine SD-Karte gefunden wird
  }
  Serial.println(" Erfolgreich.");

  // 3. CSV-Header schreiben (Das Daten-Schema)
  dataFile = SD.open(fileName, FILE_APPEND);
  if (dataFile) {
    dataFile.println("Timestamp_ms,Temp_Motor_C,Temp_ESC_C,RPM");
    dataFile.close();
    Serial.println("Pipeline bereit. Header geschrieben.");
  } else {
    Serial.println("Fehler beim Erstellen der CSV-Datei.");
  }
}

void loop() {
  unsigned long currentTime = millis();

  // Trigger für den nächsten Ingestion-Zyklus
  if (currentTime - lastTime >= samplingInterval) {
    
    // 1. Interrupts kurz pausieren, um den Zählerstand sicher zu kopieren
    noInterrupts();
    unsigned int currentPulses = pulseCount;
    pulseCount = 0; // Zähler für das nächste Intervall zurücksetzen
    interrupts();

    // 2. RPM berechnen: (Impulse pro Intervall) * (Intervalle pro Minute)
    // Bei 500ms Intervall = 120 Intervalle pro Minute
    currentRPM = currentPulses * (60000 / samplingInterval);

    // 3. Temperaturen abfragen
    sensors.requestTemperatures();
    // Index 0 ist der erste gefundene Sensor auf dem Bus, Index 1 der zweite
    float tempMotor = sensors.getTempCByIndex(0);
    float tempESC = sensors.getTempCByIndex(1);

    // 4. Payload formatieren (CSV-Zeile bauen)
    String payload = String(currentTime) + "," +
                     String(tempMotor) + "," +
                     String(tempESC) + "," +
                     String(currentRPM);

    // 5. Payload auf die SD-Karte schreiben (Storage)
    dataFile = SD.open(fileName, FILE_APPEND);
    if (dataFile) {
      dataFile.println(payload);
      dataFile.close();
      
      // Zur Kontrolle auch auf dem Seriellen Monitor ausgeben
      Serial.println(payload); 
    } else {
      Serial.println("Schreibfehler: Datei konnte nicht geöffnet werden.");
    }

    lastTime = currentTime;
  }
}