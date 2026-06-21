# Testverfahren

## Inhaltsverzeichnis
* [1. Allgemeine Vorbereitung](#1-allgemeine-vorbereitung)
* [2. Phase 1: Systemstart](#2-phase-1-systemstart)
* [3. Phase 2A: Temperatursensor](#3-phase-2a-temperatursensor)
* [4. Phase 2B: Hall-Sensor](#4-phase-2b-hall-sensor)
* [5. Phase 3: MicroSD-Karte](#5-phase-3-microsd-karte)
* [6. Phase 4: GPS-Modul](#6-phase-4-gps-modul)

## 1. Allgemeine Vorbereitung
1. ESP32 über ein Daten-USB-Kabel mit dem PC verbinden.
2. Arduino IDE öffnen und den jeweiligen Testcode in den Editor einfügen.
3. Menü `Werkzeuge` -> `Board`: `ESP32 Dev Module` auswählen.
4. Menü `Werkzeuge` -> `Port`: Zuweisung des COM-Ports.
5. Upload-Schaltfläche betätigen. Falls notwendig, den BOOT-Taster am ESP32 für zwei Sekunden drücken.
6. Seriellen Monitor öffnen und Baudrate auf 115200 einstellen.

## 2. Phase 1: Systemstart
Prüfung der ESP32-Grundfunktion und des Uploads. Es wird nur der ESP32 ohne Peripherie benötigt.

```cpp
#include <Arduino.h>

const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Systemstart");
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED AN");
  delay(1000);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED AUS");
  delay(1000);
}
```

## 3. Phase 2A: Temperatursensor
Prüfung des OneWire-Busses. Anschluss eines DS18B20-Sensors (Pin 4).

```cpp
#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 4;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Temperatur-Test");
}

void loop() {
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  
  Serial.print("Temperatur: ");
  Serial.print(temp);
  Serial.println(" C");
  
  delay(1000);
}
```

## 4. Phase 2B: Hall-Sensor
Prüfung des Interrupts. Anschluss des A3144 Hall-Sensors (Pin 2).

```cpp
#include <Arduino.h>

const int HALL_PIN = 2;
volatile int magnetErkannt = 0;

void IRAM_ATTR countPulse() {
  magnetErkannt++;
}

void setup() {
  Serial.begin(115200);
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);
  Serial.println("Bereit");
}

void loop() {
  if (magnetErkannt > 0) {
    Serial.print("Impulse: ");
    Serial.println(magnetErkannt);
    magnetErkannt = 0;
  }
  delay(100);
}
```

## 5. Phase 3: MicroSD-Karte
Prüfung des SPI-Busses und der Schreibfunktion. Anschluss des MicroSD-Moduls (CS an Pin 5) mit eingelegter FAT32-Karte.

```cpp
#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

const int SD_CS_PIN = 5;

void setup() {
  Serial.begin(115200);
  
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Fehler bei SD-Initialisierung");
    return;
  }
  
  File dataFile = SD.open("/test.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("SD-Test erfolgreich");
    dataFile.close();
    Serial.println("Schreibvorgang abgeschlossen");
  } else {
    Serial.println("Fehler beim Dateizugriff");
  }
}

void loop() {}
```

## 6. Phase 4: GPS-Modul
Empfang der NMEA-Rohdaten. Anschluss des BN-220 GPS-Moduls (RX an Pin 16, TX an Pin 17).

```cpp
#include <Arduino.h>
#include <HardwareSerial.h>

const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;
HardwareSerial SerialGPS(2);

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);
}

void loop() {
  while (SerialGPS.available()) {
    char c = SerialGPS.read();
    Serial.print(c);
  }
}
```
