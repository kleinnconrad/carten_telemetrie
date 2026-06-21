# Testverfahren und Verifikation

## Inhaltsverzeichnis
* [1. Methodik und Akzeptanzkriterien](#1-methodik-und-akzeptanzkriterien)
* [2. Allgemeine Vorbereitung](#2-allgemeine-vorbereitung)
* [3. Phase 1: Systemstart](#3-phase-1-systemstart)
* [4. Phase 2A: Temperatursensor](#4-phase-2a-temperatursensor)
* [5. Phase 2B: Hall-Sensor](#5-phase-2b-hall-sensor)
* [6. Phase 3: MicroSD-Karte](#6-phase-3-microsd-karte)
* [7. Phase 4: GPS-Modul](#7-phase-4-gps-modul)

## 1. Methodik und Akzeptanzkriterien
Die nachfolgenden Testroutinen dienen der isolierten Hardware-Verifikation (Unit-Tests der Peripherie). Jede Komponente muss zwingend einzeln geprüft werden, bevor die vollständige Firmware aufgespielt wird.
Ein Test gilt als bestanden, wenn die Ausgabe im Seriellen Monitor präzise den definierten Erwartungswerten entspricht und keine Hardware-Timeouts gemeldet werden.

## 2. Allgemeine Vorbereitung
1. Den ESP32 über ein Daten-USB-Kabel (zwingend mit intakten D+/D- Leitungen) mit dem PC verbinden.
2. Die Arduino IDE öffnen und den jeweiligen Testcode in den Editor einfügen.
3. Im Menü `Werkzeuge` -> `Board`: Die Vorgabe `ESP32 Dev Module` auswählen.
4. Im Menü `Werkzeuge` -> `Port`: Die Zuweisung des erkannten COM-Ports (Windows) bzw. `/dev/ttyUSB*` (Linux/macOS) vornehmen.
5. Die Upload-Schaltfläche betätigen. Falls der Verbindungsaufbau stagniert, den `BOOT`-Taster am ESP32 für zwei Sekunden gedrückt halten.
6. Den Seriellen Monitor öffnen und die Baudrate exakt auf `115200` einstellen.

## 3. Phase 1: Systemstart
**Ziel:** Prüfung der ESP32-Grundfunktion, des seriellen Interfaces und des Flash-Vorgangs.
**Akzeptanzkriterium:** Der serielle Monitor gibt abwechselnd im Sekunden-Takt "LED AN" und "LED AUS" aus. Die Onboard-LED blinkt synchron.

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

## 4. Phase 2A: Temperatursensor
**Ziel:** Verifikation der 1-Wire-Kommunikation. Anschluss des DS18B20-Sensors an Pin 4.
**Akzeptanzkriterium:** Die gemessene Temperatur wird in Celsius ausgegeben. Ein Auslesen des Werts `-127.00 C` indiziert einen Verbindungsabbruch oder Verdrahtungsfehler.

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

## 5. Phase 2B: Hall-Sensor
**Ziel:** Funktionsprüfung des Hardware-Interrupts am A3144 Hall-Sensor (Pin 2).
**Akzeptanzkriterium:** Bei manueller Annäherung des Neodym-Magneten an den Sensor wird exakt ein Impuls auf dem Seriellen Monitor registriert. Mehrfachauslösungen weisen auf Prellen hin (Bouncing).

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

## 6. Phase 3: MicroSD-Karte
**Ziel:** Verifikation des SPI-Busses und der Lese-/Schreibzyklen. Das Modul muss zwingend über 3.3V versorgt werden.
**Akzeptanzkriterium:** Ausgabe der Bestätigung "Schreibvorgang abgeschlossen". Die SD-Karte (FAT32) enthält anschließend eine Datei `test.txt` mit dem Text "SD-Test erfolgreich".

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

## 7. Phase 4: GPS-Modul
**Ziel:** Evaluierung des Hardware-UART-Empfangs von NMEA-Datensätzen des BN-220 Moduls (RX an Pin 16, TX an Pin 17).
**Akzeptanzkriterium:** Der Monitor zeigt rohe NMEA-Sätze (z.B. `$GPRMC...`) an. Diese müssen unter freiem Himmel valide Koordinaten enthalten, andernfalls verbleiben die Datenfelder leer.

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
