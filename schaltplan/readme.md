# RC-Telemetrie-System

## Inhaltsverzeichnis
* [1. System-Architektur](#1-system-architektur)
* [2. Pin-Mapping](#2-pin-mapping)
  * [2.1 Variante A: Cloud (LTE)](#21-variante-a-cloud-lte)
  * [2.2 Variante B: Offline (Lokales Logging)](#22-variante-b-offline-lokales-logging)
* [3. Stromversorgung](#3-stromversorgung)
  * [3.1 Variante A: Cloud](#31-variante-a-cloud)
  * [3.2 Variante B: Offline](#32-variante-b-offline)
* [4. Schaltplan Generierung](#4-schaltplan-generierung)
* [5. Betrieb](#5-betrieb)
  * [5.1 Cloud-Workflow](#51-cloud-workflow)
  * [5.2 Offline-Workflow](#52-offline-workflow)

Dieses System erfasst Telemetriedaten (Geschwindigkeit, Drehzahl, Temperaturen) in einem RC-Fahrzeug. Es existieren zwei Varianten:
* Cloud-Version: Live-Streaming über Mobilfunk.
* Offline-Version: Lokales Data-Logging.

Beide Architekturen sind für den Betrieb in RC-Fahrzeugen ausgelegt.

## 1. System-Architektur
* Betriebsmodi:
  * Cloud-Modus: Datenübertragung als JSON-Payloads via MQTT über ein SIM7000G LTE-Modul.
  * Offline-Modus: Batch-Logging auf MicroSD-Karte.
* GPS-Tracking: Ein GPS-Modul liefert Geodaten und Geschwindigkeitswerte via NMEA-Protokoll (Hardware-UART).
* Logging: Die MicroSD-Karte dient als Fallback in der Cloud-Variante und als primärer Speicher in der Offline-Variante.
* Sensor-Auslesen: Die Erfassung erfolgt asynchron. Impulse des Hall-Sensors werden über einen Hardware-Zähler (PCNT) registriert.

## 2. Pin-Mapping
Alle Komponenten benötigen eine gemeinsame Masse (GND). Serielle Verbindungen erfordern gekreuzte Leitungen (TX an RX, RX an TX).

### 2.1 Variante A: Cloud (LTE)
| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| USB Powerbank | Power | `VIN` | 5V Out | Versorgung für ESP32 und LTE |
| LTE Modul | UART 1 | `GPIO 32` (RX1) | TX | VCC an 5V Powerbank |
| | | `GPIO 33` (TX1) | RX | |
| GPS Modul | UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| MicroSD-Modul | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | |
| DS18B20 (Motor)| 1-Wire | `GPIO 4` | DQ | 4.7kΩ Pull-Up an 3.3V |
| DS18B20 (ESC)| 1-Wire | `GPIO 4` | DQ | Parallelschaltung |
| A3144 Hall-Sensor| Digital Out | `GPIO 2` | DO | PCNT-Nutzung |

### 2.2 Variante B: Offline (Lokales Logging)
| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| RC-Empfänger | Power | `VIN` | 5V (Rot) | Versorgung über ESC/Empfänger |
| | | `GND` | GND (Schwarz)| Gemeinsame Masse |
| GPS Modul | UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| MicroSD-Modul | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | |
| DS18B20 (Motor)| 1-Wire | `GPIO 4` | DQ | 4.7kΩ Pull-Up an 3.3V |
| DS18B20 (ESC)| 1-Wire | `GPIO 4` | DQ | Parallelschaltung |
| A3144 Hall-Sensor| Digital Out | `GPIO 2` | DO | PCNT-Nutzung |

## 3. Stromversorgung
Die Stromversorgung variiert je nach Setup, um Spannungsabfälle des ESP32 zu vermeiden.

### 3.1 Variante A: Cloud
Das LTE-Modem erfordert Spitzenströme bis zu 2 Ampere. Eine parallele Schaltung über ein USB-Breakout-Board ist notwendig.
1. VCC (5V): Verlöten von zwei Kabeln am VCC-Pad des Breakout-Boards (zu ESP32 VIN und LTE-Modul VCC).
2. GND: Verlöten von zwei Kabeln am GND-Pad des Breakout-Boards (zu ESP32 und LTE-Modul).
3. Daten-Pins (D+ / D-) werden nicht belegt.

### 3.2 Variante B: Offline
ESP32 und Sensorik benötigen 150-250 mA. Die Versorgung erfolgt über den Motorregler (ESC) und Empfänger.
1. Anschluss eines Servokabels an den RC-Empfänger.
2. Rotes Kabel (5V) an den VIN-Pin des ESP32.
3. Schwarzes Kabel (GND) an den GND-Pin des ESP32.

## 4. Schaltplan Generierung
Der Schaltplan wird mit Python und `uv` erstellt.

1. System-Abhängigkeit (Alpine Linux):
   ```bash
   sudo apk add graphviz
   ```
2. Tool `uv` herunterladen:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```
3. Skript ausführen:
   ```bash
   uv run --with graphviz schaltplan.py
   ```

## 5. Betrieb

### 5.1 Cloud-Workflow
1. Boot: USB-Powerbank verbinden. Initialisierung der SD-Karte.
2. Connect: Einwahl ins LTE-Netz und Aufbau der TCP-Verbindung zum MQTT-Broker.
3. Stream: Kontinuierliche Erfassung und Übertragung der Sensordaten.
4. Analyse: Auswertung im Cloud-Frontend.

### 5.2 Offline-Workflow
1. Boot: Systemstart bei Einschalten des RC-Fahrzeugs.
2. Log: Speicherung der Sensordaten mit 2 Hz auf der MicroSD-Karte.
3. Analyse: Manuelles Einlesen der MicroSD-Karte.
