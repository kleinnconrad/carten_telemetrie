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
const char* ssid = "RC-Telemetry";      // Name deines WLANs
const char* password = "password123";   // Passwort (mind. 8 Zeichen)
WebServer server(80);                   // Standard HTTP Port

// --- Sensor Setup ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// --- RPM & Timing Variablen ---
volatile unsigned int pulseCount = 0;
unsigned long lastTime = 0;
const int samplingInterval = 500; // 500ms (2 Hz)
int currentRPM = 0;

const char* fileName = "/telemetry.csv";

// --- Interrupt Service Routine (ISR) ---
void IRAM_ATTR countPulse() {
  pulseCount++;
}

// --- Webserver Routinen ---
void handleRoot() {
  // Eine einfache HTML-Seite mit einem Download-Button
  String html = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>";
  html += "<title>RC Telemetrie</title><style>body{font-family:sans-serif; text-align:center; padding:50px;}";
  html += "a{background-color:#4CAF50; color:white; padding:15px 25px; text-decoration:none; font-size:20px; border-radius:5px;}</style></head><body>";
  html += "<h1>RC Telemetrie Dashboard</h1>";
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
  // Sende die Datei als Anhang, damit der Browser den Download startet
  server.sendHeader("Content-Type", "text/csv");
  server.sendHeader("Content-Disposition", "attachment; filename=telemetry.csv");
  server.sendHeader("Connection", "close");
  
  size_t fileSize = downloadFile.size();
  server.streamFile(downloadFile, "text/csv");
  downloadFile.close();
}

void setup() {
  Serial.begin(115200);

  // 1. WLAN als Access Point starten
  Serial.println("Starte WLAN Access Point...");
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP-Adresse: ");
  Serial.println(IP);

  // 2. Webserver konfigurieren
  server.on("/", handleRoot);
  server.on("/download", HTTP_GET, handleDownload);
  server.begin();
  Serial.println("Webserver gestartet.");

  // 3. Sensoren initialisieren
  sensors.begin();
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);

  // 4. SD-Karte initialisieren
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("SD-Karte Fehlgeschlagen!");
    return; 
  }

  // 5. CSV-Header schreiben, falls Datei neu erstellt wird
  File dataFile = SD.open(fileName, FILE_APPEND);
  if (dataFile) {
    // Schreibe einen neuen Header als Trenner für eine neue Fahrt
    dataFile.println("\n--- NEUE FAHRT ---");
    dataFile.println("Timestamp_ms,Temp_Motor_C,Temp_ESC_C,RPM");
    dataFile.close();
  }
}

void loop() {
  // Webserver am Laufen halten (nimmt Anfragen entgegen)
  server.handleClient();

  unsigned long currentTime = millis();

  // Data Ingestion Cycle
  if (currentTime - lastTime >= samplingInterval) {
    
    noInterrupts();
    unsigned int currentPulses = pulseCount;
    pulseCount = 0; 
    interrupts();

    // RPM berechnen
    currentRPM = currentPulses * (60000 / samplingInterval);

    // Temperaturen lesen
    sensors.requestTemperatures();
    float tempMotor = sensors.getTempCByIndex(0);
    float tempESC = sensors.getTempCByIndex(1);

    // Payload bauen
    String payload = String(currentTime) + "," +
                     String(tempMotor) + "," +
                     String(tempESC) + "," +
                     String(currentRPM);

    // Auf SD-Karte schreiben
    File dataFile = SD.open(fileName, FILE_APPEND);
    if (dataFile) {
      dataFile.println(payload);
      dataFile.close();
    }
    
    lastTime = currentTime;
  }
}