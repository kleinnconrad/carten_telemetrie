#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <HardwareSerial.h>

// --- Neue Cloud & GPS Bibliotheken ---
#include <TinyGPS++.h>
#define TINY_GSM_MODEM_SIM7000
#include <TinyGsmClient.h>
#include <PubSubClient.h>

// --- Pin Definitionen (Gemäß neuem Schaltplan) ---
const int SD_CS_PIN = 5;
const int ONE_WIRE_BUS = 4;
const int HALL_PIN = 2;

// UART 1 (LTE Modem)
const int LTE_RX_PIN = 32;
const int LTE_TX_PIN = 33;

// UART 2 (GPS)
const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

// --- Netzwerk & Cloud Setup ---
const char apn[]      = "internet"; // Dein Provider APN (z.B. 1NCE)
const char gprsUser[] = "";
const char gprsPass[] = "";

const char* mqttServer = "dein-mqtt-broker.com"; // IP oder URL deiner Cloud
const int   mqttPort   = 1883;
const char* mqttTopic  = "rc-car/telemetry/live";

// --- Globale Objekte ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

TinyGPSPlus gps;
HardwareSerial SerialGPS(2); // Nutzt Hardware UART 2
HardwareSerial SerialLTE(1); // Nutzt Hardware UART 1

TinyGsm modem(SerialLTE);
TinyGsmClient client(modem);
PubSubClient mqtt(client);

// --- Timing & State Machine ---
unsigned long lastIngestionTime = 0;
const int ingestionInterval = 500; // 2 Hz Streaming-Rate

unsigned long lastTempRequest = 0;
const int tempConversionDelay = 800;
float currentTempMotor = 0.0;
float currentTempESC = 0.0;

volatile unsigned int pulseCount = 0;
int currentRPM = 0;

const char* fileName = "/telemetry.csv";

// --- Interrupt Service Routine ---
void IRAM_ATTR countPulse() {
  pulseCount++;
}

// --- Hilfsfunktionen ---
void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Verbinde mit MQTT...");
    // Nutze eine zufällige Client-ID
    String clientId = "RC-Car-ESP32-";
    clientId += String(random(0xffff), HEX);
    
    if (mqtt.connect(clientId.c_str())) {
      Serial.println(" Verbunden!");
    } else {
      Serial.print(" Fehler, rc=");
      Serial.print(mqtt.state());
      Serial.println(" Nächster Versuch in 5 Sekunden...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // Serielle Schnittstellen für Module starten
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
  SerialLTE.begin(115200, SERIAL_8N1, LTE_RX_PIN, LTE_TX_PIN);

  // Sensoren
  sensors.begin();
  sensors.setWaitForConversion(false); 
  sensors.requestTemperatures();
  lastTempRequest = millis();

  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);

  // SD-Karte
  if (SD.begin(SD_CS_PIN)) {
    File dataFile = SD.open(fileName, FILE_APPEND);
    if (dataFile) {
      dataFile.println("\n--- NEUE CLOUD FAHRT ---");
      dataFile.println("Timestamp,TempMot,TempESC,RPM,Lat,Lng,Speed_kmh");
      dataFile.close();
    }
  }

  // Modem Starten & Verbinden
  Serial.println("Initialisiere LTE Modem...");
  modem.restart();
  Serial.print("Verbinde mit Netzwerk: ");
  Serial.println(apn);
  if (!modem.gprsConnect(apn, gprsUser, gprsPass)) {
    Serial.println(" Netzwerkverbindung fehlgeschlagen!");
    // Hier kein blockierendes while(true), wir wollen auf SD weiter loggen!
  } else {
    Serial.println(" Netzwerk verbunden.");
  }

  mqtt.setServer(mqttServer, mqttPort);
}

void loop() {
  unsigned long currentMillis = millis();

  // 1. MQTT Verbindung am Leben halten & eingehende Pakete checken
  if (modem.isNetworkConnected()) {
    if (!mqtt.connected()) {
      connectMQTT();
    }
    mqtt.loop();
  }

  // 2. GPS Daten permanent und asynchron aus dem Puffer lesen
  while (SerialGPS.available() > 0) {
    gps.encode(SerialGPS.read());
  }

  // 3. Asynchroner Temperatur-Update-Zyklus
  if (currentMillis - lastTempRequest >= tempConversionDelay) {
    currentTempMotor = sensors.getTempCByIndex(0);
    currentTempESC = sensors.getTempCByIndex(1);
    sensors.requestTemperatures();
    lastTempRequest = currentMillis;
  }

  // 4. Data Ingestion Pipeline (2 Hz)
  if (currentMillis - lastIngestionTime >= ingestionInterval) {
    
    // RPM berechnen
    noInterrupts();
    unsigned int currentPulses = pulseCount;
    pulseCount = 0; 
    interrupts();
    currentRPM = currentPulses * (60000 / ingestionInterval);

    // GPS Werte sicher abholen
    float lat = gps.location.isValid() ? gps.location.lat() : 0.0;
    float lng = gps.location.isValid() ? gps.location.lng() : 0.0;
    float speed = gps.speed.isValid() ? gps.speed.kmph() : 0.0;

    // Payload als JSON formatieren (Für MQTT)
    char jsonPayload[256];
    snprintf(jsonPayload, sizeof(jsonPayload), 
             "{\"ts\":%lu,\"rpm\":%d,\"temp_mot\":%.2f,\"temp_esc\":%.2f,\"lat\":%.6f,\"lng\":%.6f,\"spd\":%.2f}",
             currentMillis, currentRPM, currentTempMotor, currentTempESC, lat, lng, speed);

    // CSV Format (Für SD Backup)
    char csvPayload[128];
    snprintf(csvPayload, sizeof(csvPayload), 
             "%lu,%.2f,%.2f,%d,%.6f,%.6f,%.2f",
             currentMillis, currentTempMotor, currentTempESC, currentRPM, lat, lng, speed);

    // Auf SD-Karte schreiben (lokales Backup)
    File dataFile = SD.open(fileName, FILE_APPEND);
    if (dataFile) {
      dataFile.println(csvPayload);
      dataFile.close();
    }

    // In die Cloud publishen
    if (mqtt.connected()) {
      mqtt.publish(mqttTopic, jsonPayload);
      Serial.println("-> Cloud Publish OK");
    }

    lastIngestionTime = currentMillis;
  }
}