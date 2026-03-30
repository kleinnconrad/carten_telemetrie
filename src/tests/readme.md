1. **Verkabeln:** Verbinde deinen ESP32 mit einem Daten-USB-Kabel (kein reines Ladekabel!) mit dem PC.
2. **IDE vorbereiten:** Öffne die Arduino IDE. Kopiere den Code für den jeweiligen Schritt in das große weiße Textfeld (lösche vorher alles, was dort steht).
3. **Board auswählen:** Gehe oben im Menü auf `Werkzeuge` -> `Board` -> `esp32` und wähle **ESP32 Dev Module** (oder NodeMCU-32S).
4. **Port auswählen:** Gehe auf `Werkzeuge` -> `Port` und wähle den COM-Port aus, an dem dein ESP32 hängt (z.B. COM3 oder COM4).
5. **Hochladen:** Klicke oben links auf den runden Button mit dem **Pfeil nach rechts** (Upload). 
6. *Achtung:* Wenn unten im Terminal `Connecting...` steht, musst du bei manchen ESP32-Boards für 2 Sekunden den kleinen Knopf mit der Aufschrift **"BOOT"** auf dem Board gedrückt halten, damit er den Code annimmt!
7. **Ergebnis prüfen:** Klicke oben rechts auf das Lupe-Symbol (**Serieller Monitor**) und stelle die Baudrate unten rechts auf **115200**, um zu lesen, was dein ESP32 dir mitteilt.

---

### Phase 1: Das Fundament (Der Herzschlag)
**Ziel:** Prüfen, ob der ESP32 lebt und der Upload funktioniert.
**Hardware:** Nur der ESP32 per USB am PC. Nichts weiter anschließen.

```cpp
#include <Arduino.h>

// Beim ESP32 ist die interne blaue LED oft an Pin 2
const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ESP32 lebt und startet den Test!");
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // LED an
  Serial.println("LED AN");
  delay(1000);                 // 1 Sekunde warten
  
  digitalWrite(LED_PIN, LOW);  // LED aus
  Serial.println("LED AUS");
  delay(1000);
}
```

---

### Phase 2A: Temperatursensor
**Ziel:** Testen, ob der OneWire-Bus funktioniert.
**Hardware:** Verbinde *nur* den DS18B20 Temperatursensor. Rot an 3.3V, Schwarz an GND, Gelb/Blau an Pin 4. (Denke an den 4.7k Ohm Widerstand zwischen VCC und Data, falls du kein fertiges Modul nutzt!).

```cpp
#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 4; // Dein Pin laut Schaltplan

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Temperatur-Test gestartet.");
}

void loop() {
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  
  Serial.print("Aktuelle Temperatur: ");
  Serial.print(temp);
  Serial.println(" °C");
  
  delay(1000);
}
```

---

### Phase 2B: Hall-Sensor
**Ziel:** Testen, ob der Interrupt für die Motor-RPM klappt.
**Hardware:** Dallas-Sensor abstecken. *Nur* den A3144 Hall-Sensor anschließen (Signal an Pin 2). Führe einen Magneten am Sensor vorbei.

```cpp
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
```

---

### Phase 3: Lokales Backup (MicroSD-Karte)
**Ziel:** Beweisen, dass das SPI-Bussystem Daten auf die Karte schreiben kann.
**Hardware:** Schließe das MicroSD-Modul exakt gem. Schaltplan an (CS an Pin 5). Lege eine FAT32-formatierte SD-Karte ein.

```cpp
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
```

---

### Phase 4A: GPS UART
**Ziel:** Die NMEA-Rohdaten des GPS-Moduls empfangen.
**Hardware:** Schließe *nur* das BN-220 GPS an (RX an Pin 16, TX an Pin 17). **Gehe ins Freie oder ans Fenster!**

```cpp
#include <Arduino.h>
#include <HardwareSerial.h>

const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

HardwareSerial SerialGPS(2); // UART 2

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN); // 9600 ist Standard für GPS
  Serial.println("Warte auf GPS Rohdaten...");
}

void loop() {
  // Wenn das GPS-Modul Daten sendet, drucke sie sofort in den Monitor
  while (SerialGPS.available()) {
    char c = SerialGPS.read();
    Serial.print(c);
  }
}
```

---

### Phase 4B: LTE Modem
**Ziel:** Testen, ob der ESP32 mit dem SIM7000 Modem sprechen kann (AT-Befehle).
**Hardware:** Verbinde das SIM7000 Modul (RX an 32, TX an 33). Stromversorgung muss hier stabil sein (ggf. Powerbank).

```cpp
#include <Arduino.h>
#include <HardwareSerial.h>

const int LTE_RX_PIN = 32;
const int LTE_TX_PIN = 33;

HardwareSerial SerialLTE(1); // UART 1

void setup() {
  Serial.begin(115200);
  // Das SIM7000 spricht standardmäßig meist mit 115200 Baud
  SerialLTE.begin(115200, SERIAL_8N1, LTE_RX_PIN, LTE_TX_PIN); 
  
  Serial.println("Sende 'AT' an das Modem...");
  SerialLTE.println("AT"); // AT ist der universelle "Hallo bist du da?" Befehl
}

void loop() {
  // Alles was vom Modem kommt, im PC anzeigen
  if (SerialLTE.available()) {
    Serial.write(SerialLTE.read());
  }
  // Alles was du im Seriellen Monitor tippst, ans Modem schicken
  if (Serial.available()) {
    SerialLTE.write(Serial.read());
  }
}
```

---
