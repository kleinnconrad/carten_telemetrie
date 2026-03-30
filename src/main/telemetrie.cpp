#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <HardwareSerial.h>
#include <TinyGPS++.h>

#define TINY_GSM_MODEM_SIM7000
#include <TinyGsmClient.h>
#include <PubSubClient.h>

// Pins
const int SD_CS_PIN = 5;
const int ONE_WIRE_BUS = 4;
const int HALL_PIN = 2;
const int LTE_RX_PIN = 32;
const int LTE_TX_PIN = 33;
const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

// Config
const char apn[]      = "internet"; 
const char* mqttServer = "dein-mqtt-broker.com";
const int   mqttPort   = 1883;
const char* mqttTopic  = "rc-car/telemetry/live";

// Objekte
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
TinyGPSPlus gps;
HardwareSerial SerialGPS(2); 
HardwareSerial SerialLTE(1); 
TinyGsm modem(SerialLTE);
TinyGsmClient client(modem);
PubSubClient mqtt(client);

// States
unsigned long lastIngestionTime = 0;
const int ingestionInterval = 500; 
unsigned long lastTempRequest = 0;
unsigned long lastMqttRetry = 0; // Neu: Für nicht-blockierendes Reconnect
float currentTempMotor = 0.0;
float currentTempESC = 0.0;
volatile unsigned int pulseCount = 0;

void IRAM_ATTR countPulse() {
  pulseCount++;
}

// Optimierte Connect-Funktion (ohne Blockieren!)
void maintainMQTT() {
  if (!mqtt.connected()) {
    unsigned long now = millis();
    if (now - lastMqttRetry > 5000) { // Nur alle 5 Sek versuchen
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

  sensors.begin();
  sensors.setWaitForConversion(false);
  sensors.requestTemperatures();

  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);

  if (SD.begin(SD_CS_PIN)) {
    Serial.println("SD OK");
  }

  Serial.println("Starte Modem...");
  modem.restart();
  modem.gprsConnect(apn, "", "");
  mqtt.setServer(mqttServer, mqttPort);
}

void loop() {
  unsigned long currentMillis = millis();

  // 1. LTE/MQTT Check
  if (modem.isNetworkConnected()) {
    maintainMQTT();
  }

  // 2. GPS Stream
  while (SerialGPS.available() > 0) {
    gps.encode(SerialGPS.read());
  }

  // 3. Temperatur (Asynchron)
  if (currentMillis - lastTempRequest >= 800) {
    currentTempMotor = sensors.getTempCByIndex(0);
    currentTempESC = sensors.getTempCByIndex(1);
    sensors.requestTemperatures();
    lastTempRequest = currentMillis;
  }

  // 4. Data Pipeline
  if (currentMillis - lastIngestionTime >= ingestionInterval) {
    // RPM
    noInterrupts();
    unsigned int pulses = pulseCount;
    pulseCount = 0;
    interrupts();
    int rpm = pulses * (60000 / ingestionInterval);

    // Payload
    char json[256];
    snprintf(json, sizeof(json), "{\"rpm\":%d,\"t_m\":%.1f,\"t_e\":%.1f,\"lat\":%.6f,\"lng\":%.6f}",
             rpm, currentTempMotor, currentTempESC, gps.location.lat(), gps.location.lng());

    // SD Log
    File dataFile = SD.open("/log.csv", FILE_APPEND);
    if (dataFile) {
      dataFile.println(json);
      dataFile.close();
    }

    // Cloud Publish
    if (mqtt.connected()) {
      mqtt.publish(mqttTopic, json);
    }

    lastIngestionTime = currentMillis;
  }
}