#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <HardwareSerial.h>
#include <TinyGPS++.h>
#include <driver/pcnt.h> // Die ESP32 Hardware-Zähler Bibliothek

#define TINY_GSM_MODEM_SIM7000
#include <TinyGsmClient.h>
#include <PubSubClient.h>

// --- Pin Definitionen ---
const int SD_CS_PIN = 5;
const int ONE_WIRE_BUS = 4;
const int HALL_PIN = 2;
const int LTE_RX_PIN = 32;
const int LTE_TX_PIN = 33;
const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

// --- Config ---
const char apn[]       = "internet"; // Dein Provider APN
const char* mqttServer = "dein-mqtt-broker.com"; // Deine Cloud/Broker IP
const int   mqttPort   = 1883;
const char* mqttTopic  = "rc-car/telemetry/live";

// --- Objekte ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
TinyGPSPlus gps;
HardwareSerial SerialGPS(2); 
HardwareSerial SerialLTE(1); 
TinyGsm modem(SerialLTE);
TinyGsmClient client(modem);
PubSubClient mqtt(client);

// --- States & Timing ---
unsigned long lastIngestionTime = 0;
const int ingestionInterval = 500; // 2 Hz Streaming-Rate
unsigned long lastTempRequest = 0;
unsigned long lastMqttRetry = 0;
float currentTempMotor = 0.0;
float currentTempESC = 0.0;

// --- PCNT Hardware Zähler States ---
pcnt_unit_t pcnt_unit = PCNT_UNIT_0;
int16_t prevPulses = 0; 
const int16_t COUNTER_HIGH_LIMIT = 30000;

// --- Setup PCNT Hardware-Zähler ---
void setupPCNT() {
  pcnt_config_t pcnt_config = {
    .pulse_gpio_num = HALL_PIN,
    .ctrl_gpio_num = PCNT_PIN_NOT_USED,
    .lctrl_mode = PCNT_MODE_KEEP,
    .hctrl_mode = PCNT_MODE_KEEP,
    .pos_mode = PCNT_COUNT_DIS,   // Ignorieren, wenn der Magnet kommt (HIGH)
    .neg_mode = PCNT_COUNT_INC,   // Zählen, wenn das Signal abfällt (FALLING)
    .counter_h_lim = COUNTER_HIGH_LIMIT,
    .counter_l_lim = -1,
    .unit = pcnt_unit,
    .channel = PCNT_CHANNEL_0,
  };
  
  pcnt_unit_config(&pcnt_config);
  
  // Hardware-Filter gegen Störsignale/Vibrationen aktivieren
  pcnt_set_filter_value(pcnt_unit, 100); 
  pcnt_filter_enable(pcnt_unit);
  
  pcnt_counter_pause(pcnt_unit);
  pcnt_counter_clear(pcnt_unit);
  pcnt_counter_resume(pcnt_unit);
}

// --- Hilfsfunktion: Nicht-blockierender MQTT Reconnect ---
void maintainMQTT() {
  if (!mqtt.connected()) {
    unsigned long now = millis();
    if (now - lastMqttRetry > 5000) { 
      lastMqttRetry = now;
      Serial.println("MQTT Reconnect Versuch...");
      String clientId = "RC-Car-" + String(random(0xffff), HEX);
      if (mqtt.connect(clientId.c_str())) {
        Serial.println("Cloud verbunden!");
      }
    }
  } else {
    mqtt.loop();
  }
}

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
  SerialLTE.begin(115200, SERIAL_8N1, LTE_RX_PIN, LTE_TX_PIN);

  // Sensoren starten
  sensors.begin();
  sensors.setWaitForConversion(false);
  sensors.requestTemperatures();

  // Den PCNT Hardware-Assistenten starten
  setupPCNT();

  // SD-Karte initialisieren
  if (SD.begin(SD_CS_PIN)) {
    Serial.println("SD OK");
  } else {
    Serial.println("SD Fehler!");
  }

  // Modem Starten & Verbinden
  Serial.println("Starte Modem...");
  modem.restart();
  modem.gprsConnect(apn, "", "");
  mqtt.setServer(mqttServer, mqttPort);
  
  lastIngestionTime = millis();
}

void loop() {
  unsigned long currentMillis = millis();

  // 1. LTE/MQTT Check am Leben halten
  if (modem.isNetworkConnected()) {
    maintainMQTT();
  }

  // 2. GPS Stream asynchron lesen
  while (SerialGPS.available() > 0) {
    gps.encode(SerialGPS.read());
  }

  // 3. Temperatur-Update-Zyklus (Asynchron)
  if (currentMillis - lastTempRequest >= 800) {
    currentTempMotor = sensors.getTempCByIndex(0);
    currentTempESC = sensors.getTempCByIndex(1);
    sensors.requestTemperatures();
    lastTempRequest = currentMillis;
  }

  // 4. Data Ingestion Pipeline
  unsigned long timeDelta = currentMillis - lastIngestionTime; 
  if (timeDelta >= ingestionInterval) {
    
    // Pulse abfragen (ohne den Zähler zu löschen!)
    int16_t currentPulses = 0;
    pcnt_get_counter_value(pcnt_unit, &currentPulses);
    
    // Delta berechnen
    int16_t deltaPulses = currentPulses - prevPulses;
    prevPulses = currentPulses; 
    
    // Overflow abfangen
    if (deltaPulses < 0) {
      deltaPulses = deltaPulses + COUNTER_HIGH_LIMIT;
    }

    // RPM mit Anti-Jitter Mathematik berechnen
    int rpm = deltaPulses * (60000.0 / timeDelta);

    // Payload schnüren (mit sicheren GPS Werten)
    float lat = gps.location.isValid() ? gps.location.lat() : 0.0;
    float lng = gps.location.isValid() ? gps.location.lng() : 0.0;
    
    // --- FEHLENDER WERT HINZUGEFÜGT ---
    float speed = gps.speed.isValid() ? gps.speed.kmph() : 0.0; 
    
    char json[256];
    snprintf(json, sizeof(json), "{\"rpm\":%d,\"t_m\":%.1f,\"t_e\":%.1f,\"lat\":%.6f,\"lng\":%.6f,\"spd\":%.2f}",
             rpm, currentTempMotor, currentTempESC, lat, lng, speed);

    // Lokales Backup auf SD-Karte
    File dataFile = SD.open("/log.csv", FILE_APPEND);
    if (dataFile) {
      dataFile.println(json);
      dataFile.close();
    }

    // In die Cloud publishen
    if (mqtt.connected()) {
      mqtt.publish(mqttTopic, json);
    }

    lastIngestionTime = currentMillis;
  }
}
