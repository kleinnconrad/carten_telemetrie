# RC Telemetrie Firmware (ESP32)

Dieses Repository enthält die C++ Firmware für ein ESP32-basiertes Edge-Device zur Erfassung von Telemetriedaten in einem RC-Fahrzeug. Das System liest hochfrequent Sensordaten (Temperatur und Drehzahl) aus, speichert diese lokal auf einer MicroSD-Karte und stellt sie im Nachgang über einen eigenen WLAN-Access-Point zum Download bereit.

## Kern-Features & Architektur

* **Asynchrone Datenerfassung:** Die 1-Wire-Temperatursensoren (DS18B20) benötigen bis zu 750ms für eine 12-Bit-Wandlung. Die Firmware nutzt `setWaitForConversion(false)`, um den Haupt-Loop nicht zu blockieren.
* **Echtzeit-Interrupts (ISR):** Die Erfassung der Drehzahlimpulse (Hall-Sensor) erfolgt komplett asynchron über Hardware-Interrupts an GPIO 2.
* **Hohe Ingestion-Rate:** Die Telemetriedaten werden mit **5 Hz (alle 200 ms)** auf die MicroSD-Karte geschrieben.
* **Integrierter Webserver:** Der ESP32 spannt ein eigenes WLAN auf (`RC-Telemetry`). Die gesammelten CSV-Daten können nach der Fahrt direkt über den Browser eines Smartphones heruntergeladen werden.

## 🔌 Pin-Mapping (Hardware Setup)

| Komponente | Pin am ESP32 | Protokoll / Funktion |
| :--- | :--- | :--- |
| **MicroSD CS** | `GPIO 5` | SPI (Chip Select) |
| **MicroSD MOSI** | `GPIO 23` | SPI |
| **MicroSD MISO** | `GPIO 19` | SPI |
| **MicroSD SCK** | `GPIO 18` | SPI |
| **Temp. Sensoren** | `GPIO 4` | 1-Wire Bus (DS18B20)* |
| **Hall-Sensor (RPM)** | `GPIO 2` | Digitaler Input (Hardware Interrupt) |

*\*Hinweis: Der 1-Wire Bus an GPIO 4 erfordert zwingend einen 4,7kΩ Pull-Up Widerstand gegen 3.3V.*

## Software Abhängigkeiten

Um dieses Projekt zu kompilieren (via Arduino IDE oder PlatformIO), werden folgende Bibliotheken benötigt:

1. `OneWire` (für das Protokoll der Temperatursensoren)
2. `DallasTemperature` (zur Auswertung der DS18B20 Sensoren)
3. Integrierte ESP32-Bibliotheken: `WiFi`, `WebServer`, `SPI`, `SD`

## Betrieb & Datenabruf

Sobald der ESP32 mit Strom versorgt wird, beginnt er automatisch mit der Aufzeichnung der Daten in die Datei `/telemetry.csv`. Bei jedem Neustart wird ein neuer Block (`--- NEUE FAHRT ---`) in der Datei angelegt.

**So lädst du die Daten nach der Fahrt herunter:**

1. Verbinde dein Smartphone/Laptop mit dem WLAN des RC-Autos:
   * **SSID:** `RC-Telemetry`
   * **Passwort:** `password123`
2. Öffne einen Webbrowser und navigiere zu:
   * **URL:** `http://192.168.4.1`
3. Klicke auf "CSV-Datei Herunterladen".

## Datenstruktur (CSV-Schema)

Die exportierte `telemetry.csv` ist wie folgt strukturiert:

```csv
Timestamp_ms,Temp_Motor_C,Temp_ESC_C,RPM
200,35.50,42.00,0
400,35.50,42.25,1200
600,36.00,42.50,2450
