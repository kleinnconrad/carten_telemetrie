# Carten Telemetrie

## Inhaltsverzeichnis
* [1. Projektbeschreibung](#1-projektbeschreibung)
* [2. Stückliste (Bill of Materials)](#2-stueckliste-bill-of-materials)
* [3. Schaltplan und Pin-Belegung](#3-schaltplan-und-pin-belegung)
  * [3.1 Variante A: Cloud (LTE)](#31-variante-a-cloud-lte)
  * [3.2 Variante B: Offline (Lokales Logging)](#32-variante-b-offline-lokales-logging)
* [4. Aufbau](#4-aufbau)
  * [4.1 Vorbereitung und Software](#41-vorbereitung-und-software)
  * [4.2 Verkabelung und Energieversorgung](#42-verkabelung-und-energieversorgung)
  * [4.3 Mechanische Integration](#43-mechanische-integration)
* [5. Betrieb](#5-betrieb)
* [6. Reddit-Feedback-Synchronisation](#6-reddit-feedback-synchronisation)

## 1. Projektbeschreibung
Entwicklung eines Telemetriesystems für das Modell Carten T410R [![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/kleinnconrad/RC100). Erfasste Parameter:
* Temperatur (Motor, ESC)
* Drehzahl (Kardanwelle)
* GPS-Daten (Geschwindigkeit, Position)

Architektur-Varianten:
* Cloud-Version: Live-Streaming über LTE (MQTT)
* Offline-Version: Lokales Logging auf MicroSD-Karte

## 2. Stückliste (Bill of Materials)
| Komponente | Spezifikation / Typ | Variante | Funktion |
| :--- | :--- | :--- | :--- |
| Microcontroller | ESP32 Dev Board (z.B. NodeMCU) | Beide | Ingestion |
| GPS-Modul | BN-220 (u-blox) | Beide | Geodaten und Geschwindigkeit |
| Speichermodul | MicroSD-Karten-Modul (SPI) | Beide | Datenspeicher (3.3V) |
| Temperatursensor | DS18B20 | Beide | 2x 1-Wire Sensoren (Motor, ESC) |
| Drehzahlsensor | Hall-Sensor Modul (A3144) | Beide | Erfassung des Magnetfelds |
| Magnet | Neodym-Magnet (3x2mm) | Beide | Montage an Kardanwelle |
| Widerstand | 4,7 kΩ | Beide | Pull-Up für 1-Wire Bus |
| LTE-Modem | SIM7000G Breakout-Board | Cloud | Cloud-Anbindung |
| Stromversorgung 1| USB Powerbank | Cloud | 5V Spannungsversorgung |
| Stromversorgung 2| 3-Pin Servokabel | Offline | 5V Spannungsversorgung über RC-Empfänger |

## 3. Schaltplan und Pin-Belegung
Alle Komponenten nutzen eine gemeinsame Masse (GND). Serielle Verbindungen (UART) erfordern gekreuzte Leitungen (TX an RX, RX an TX).

### 3.1 Variante A: Cloud (LTE)
Verwendung eines LTE-Moduls und einer separaten Spannungsquelle zur Vermeidung von Spannungsabfällen am ESP32.

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| USB Powerbank | Power | `VIN` | 5V Out | Parallele Versorgung von ESP32 und LTE |
| LTE Modul | UART 1 | `GPIO 32` (RX1) | TX | VCC an 5V Powerbank |
| | | `GPIO 33` (TX1) | RX | |
| GPS Modul| UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| MicroSD-Modul | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC an 3.3V ESP32 |
| DS18B20 | 1-Wire | `GPIO 4` | DQ (Daten) | Parallelschaltung, 4.7kΩ Pull-Up an 3.3V |
| A3144 Hall-Sensor| Dig. Out | `GPIO 2` | DO (Signal) | ESP32 PCNT Hardware-Counter |

### 3.2 Variante B: Offline (Lokales Logging)
Verzicht auf Modem und separate Spannungsquelle. Stromversorgung über das RC-Fahrzeug.

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| RC-Empfänger| Power | `VIN` | 5V (Rot) | Versorgung über ESC/Empfänger |
| | | `GND` | GND (Schwarz)| Gemeinsame Masse |
| GPS Modul| UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| MicroSD-Modul | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC an 3.3V ESP32 |
| DS18B20 | 1-Wire | `GPIO 4` | DQ (Daten) | Parallelschaltung, 4.7kΩ Pull-Up an 3.3V |
| A3144 Hall-Sensor| Dig. Out | `GPIO 2` | DO (Signal) | ESP32 PCNT Hardware-Counter |

## 4. Aufbau

### 4.1 Vorbereitung und Software
* Installation der Bibliotheken in Arduino IDE / PlatformIO: `TinyGPSPlus`, `OneWire`, `DallasTemperature`. Für die Cloud-Variante zusätzlich: `TinyGSM`, `PubSubClient`.
* Flash-Vorgang der Firmware auf den ESP32.

### 4.2 Verkabelung und Energieversorgung
* Cloud-Variante: USB-Breakout-Board als Y-Verteiler nutzen. 5V-Leitung isoliert zu ESP32 (`VIN`) und LTE-Modem (`VCC`) verlegen.
* Offline-Variante: Servokabel mit `VIN` und `GND` des ESP32 verlöten. Anschluss an freien Kanal des RC-Empfängers.
* Verbindung von GPS, SD-Modul, Hall-Sensor und Temperatursensoren gemäß Pin-Mapping.
* Einbau des 4,7 kΩ Widerstands zwischen 3.3V-Leitung und Datenleitung der Temperatursensoren.
* Isolierung der Lötstellen.

### 4.3 Mechanische Integration
* Befestigung der Elektronik im Chassis. Das GPS-Modul muss mit der Keramik-Antenne nach oben zeigen.
* Montage des Neodym-Magneten auf der Kardanwelle. Gegengewicht anbringen.
* Montage des Hall-Sensors am rotierenden Magneten.
* Montage der Temperatursensoren am ESC und Motor.

## 5. Betrieb

### Variante A (Cloud)
* Verbinden der USB-Powerbank. Initialisierung der SD-Karte und GPS-Fix-Suche.
* Automatischer Verbindungsaufbau zum LTE-Netz und zur Cloud (MQTT-Broker).
* Übertragung der Daten mit 2 Hz als JSON-Payload.

### Variante B (Offline)
* Systemstart bei Einschalten des RC-Fahrzeugs.
* Aufzeichnung der Sensordaten mit 2 Hz als JSON/CSV auf die MicroSD-Karte.
* Manuelles Einlesen der MicroSD-Karte zur Datenauswertung.

## 6. Reddit-Feedback-Synchronisation
Eine GitHub Action extrahiert Feedback aus dem Reddit-Thread und speichert es im Repository. Es wird der RSS-Feed genutzt.

### Architektur
* Skript (`scripts/fetch_reddit.py`): Abruf des RSS-Feeds und HTML-Bereinigung.
* Automatisierung (`.github/workflows/reddit-sync.yml`): Tägliche Ausführung um 08:00 UTC.
* Output: Speicherung neuer Kommentare in `reddit/reddit_feedback.md`. Automatischer Commit im `main` Branch.

### Manueller Sync
* GitHub Actions aufrufen.
* Workflow "Fetch Reddit Feedback" auswählen.
* Ausführung bestätigen. Die Datei `reddit_feedback.md` wird aktualisiert.
