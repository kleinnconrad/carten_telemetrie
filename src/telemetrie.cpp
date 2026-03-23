#include <WiFi.h>
#include <WebServer.h>
#include <SPI.h>
#include <SD.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- Pin Definitionen ---
const int SD_CS_PIN = 5;
const int ONE_WIRE_BUS = 4;
const int HALL_PIN = 2;

// --- WLAN & Webserver Setup ---
const char* ssid = "RC-Telemetry";
const char* password = "password123";
WebServer server(80);

// --- Sensor Setup ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// --- Timing & State Machine Variablen ---
// 1. Data Ingestion Pipeline (z.B. 5 Hz für detailliertere RPM-Kurven)
unsigned long lastIngestionTime = 0;
const int ingestionInterval = 200; 

// 2. Asynchroner Temperatur-Zyklus
unsigned long lastTempRequest = 0;
const int tempConversionDelay = 800; // Muss > 750ms für 12-bit DS18B20 sein
float currentTempMotor = 0.0;
float currentTempESC = 0.0;

// RPM Zähler
volatile unsigned int pulseCount = 0;
int currentRPM = 0;

const char* fileName = "/telemetry.csv";

// --- Interrupt Service Routine (ISR) ---
void IRAM_ATTR countPulse() {
  pulseCount++;
}

// --- Webserver Routinen ---
void handleRoot() {
  String html = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
  html += "<title>RC Telemetrie Dashboard</title><style>body{font-family:sans-serif; text-align:center; padding:50px;}";
  html += "a{background-color:#0056b3; color:white; padding:15px 25px; text-decoration:none; font-size:20px; border-radius:5px;}</style></head><body>";
  html += "<h1>RC Telemetrie</h1>";
  html += "<p>Lade hier deine aufgezeichneten Daten herunter:</p><br>";
  html += "<a href=\"/download\">CSV-Datei Herunterladen</a>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleDownload() {
  File downloadFile = SD.open(fileName, FILE_READ);
  if (!downloadFile) {
    server.send(404, "text/plain", "Datei nicht gefunden.");
    return;
  }
  server.sendHeader("Content-Type", "text/csv");
  server.sendHeader("Content-Disposition", "attachment; filename=telemetry.csv");
  server.sendHeader("Connection", "close");
  
  server.streamFile(downloadFile, "text/csv");
  downloadFile.close();
}

void setup() {
  Serial.begin(115200);

  // WLAN & Webserver starten
  WiFi.softAP(ssid, password);
  server.on("/", handleRoot);
  server.on("/download", HTTP_GET, handleDownload);
  server.begin();

  // Sensoren initialisieren
  sensors.begin();
  
  // WICHTIG: Den blockierenden Modus deaktivieren!
  sensors.setWaitForConversion(false); 
  
  // Ersten Temperatur-Request anstoßen
  sensors.requestTemperatures();
  lastTempRequest = millis();

  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);

  // SD-Karte initialisieren
  if (SD.begin(SD_CS_PIN)) {
    File dataFile = SD.open(fileName, FILE_APPEND);
    if (dataFile) {
      dataFile.println("\n--- NEUE FAHRT ---");
      dataFile.println("Timestamp_ms,Temp_Motor_C,Temp_ESC_C,RPM");
      dataFile.close();
    }
  }
}

void loop() {
  // 1. Webserver bedienen (darf nicht blockiert werden!)
  server.handleClient();

  unsigned long currentMillis = millis();

  // 2. Asynchroner Temperatur-Update-Zyklus
  if (currentMillis - lastTempRequest >= tempConversionDelay) {
    // Werte abholen (dauert jetzt nur Mikrosekunden, da die Konvertierung fertig ist)
    currentTempMotor = sensors.getTempCByIndex(0);
    currentTempESC = sensors.getTempCByIndex(1);

    // Direkt die nächste Konvertierung beim Sensor in Auftrag geben
    sensors.requestTemperatures();
    lastTempRequest = currentMillis;
  }

  // 3. Data Ingestion Pipeline (Alle 200ms = 5 Hz)
  if (currentMillis - lastIngestionTime >= ingestionInterval) {
    
    // RPM sicher auslesen und zurücksetzen
    noInterrupts();
    unsigned int currentPulses = pulseCount;
    pulseCount = 0; 
    interrupts();

    // RPM hochrechnen
    currentRPM = currentPulses * (60000 / ingestionInterval);

    // Payload formatieren (nutzt die jeweils aktuellsten verfügbaren Temperaturwerte)
    String payload = String(currentMillis) + "," +
                     String(currentTempMotor) + "," +
                     String(currentTempESC) + "," +
                     String(currentRPM);

    // Auf SD-Karte schreiben
    File dataFile = SD.open(fileName, FILE_APPEND);
    if (dataFile) {
      dataFile.println(payload);
      dataFile.close();
    }
    
    lastIngestionTime = currentMillis;
  }
}
