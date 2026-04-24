# carten_telemetrie
Entwicklung einer Telemetrie-Lösung für einen Carten T410R [![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/kleinnconrad/RC100), um Temperatur (Motor, ESC), Drehzahl (Kardanwelle) und GPS-Daten (Geschwindigkeit, Position) hochfrequent zu erfassen.

Das System kann in zwei Architektur-Varianten aufgebaut werden: Als **Cloud-Version** (Live-Streaming via LTE) oder als gewichtsoptimierte und kostengünstige **Offline-Version** (Lokales Logging via RC-Empfänger).

## Inhaltsverzeichnis

* [Bauanleitung: DIY Telemetrie-System (Cloud & Offline)](#bauanleitung-diy-telemetrie-system-cloud--offline)
  * [1. Stückliste (Bill of Materials)](#1-stückliste-bill-of-materials)
  * [2. Schaltplan & Pin-Belegung](#2-schaltplan--pin-belegung)
    * [Variante A: Cloud (LTE)](#variante-a-cloud-lte)
    * [Variante B: Offline (Lokales Logging)](#variante-b-offline-lokales-logging)
  * [3. Schritt-für-Schritt Aufbau](#3-schritt-für-schritt-aufbau)
    * [Phase 1: Vorbereitung & Software](#phase-1-vorbereitung--software)
    * [Phase 2: Löten & Verkabeln (Power-Management)](#phase-2-löten--verkabeln-power-management)
    * [Phase 3: Mechanische Integration](#phase-3-mechanische-integration)
  * [4. Betrieb](#4-betrieb)
  * [5. Reddit-Feedback-Sync](#5-reddit-feedback-sync)

---

# Bauanleitung: DIY Telemetrie-System (Cloud & Offline)

Dieses Dokument beschreibt den Aufbau eines autarken IoT-Edge-Nodes für RC-Fahrzeuge. Die Sensordaten werden entweder live über das Mobilfunknetz an ein Cloud-Dashboard (via MQTT) gestreamt oder lokal als High-Speed-Batch auf einer MicroSD-Karte geloggt. 

---

## 1. Stückliste (Bill of Materials)

| Komponente | Spezifikation / Typ | Variante | Bemerkung |
| :--- | :--- | :--- | :--- |
| **Microcontroller** | ESP32 Dev Board (z.B. NodeMCU) | Beide | Zentraleinheit für Ingestion |
| **GPS-Modul** | BN-220 (u-blox) | Beide | Für Geodaten & Doppler-Geschwindigkeit |
| **Speichermodul** | MicroSD-Karten-Modul (SPI) | Beide | 3.3V-kompatibel |
| **Temperatursensor** | DS18B20 (Wasserdicht) | Beide | 2x Digitale 1-Wire Sensoren (Motor & ESC) |
| **Drehzahlsensor** | Hall-Sensor Modul (z.B. A3144) | Beide | Erfasst das Magnetfeld für RPM-Berechnung |
| **Magnet** | Neodym-Magnet (klein, z.B. 3x2mm) | Beide | Wird auf rotierende Kardanwelle geklebt |
| **Widerstand** | 4,7 kΩ (Kilo-Ohm) | Beide | Pull-Up-Widerstand für den 1-Wire Bus |
| **LTE-Modem** | SIM7000G Breakout-Board | Nur Cloud | Für die Cloud-Anbindung (inkl. SIM-Karte) |
| **Stromversorgung 1**| USB Powerbank (klein/leicht) | Nur Cloud | Isoliertes 5V Power-Management für LTE |
| **Stromversorgung 2**| 3-Pin Servokabel | Nur Offline | Abgriff der 5V vom RC-Empfänger (BEC) |

---

## 2. Schaltplan & Pin-Belegung

**WICHTIG:** Alle Komponenten teilen sich eine gemeinsame Masse (**GND**). Bei seriellen Verbindungen (UART) müssen die Leitungen zwingend überkreuzt werden (TX an RX, RX an TX).

### Variante A: Cloud (LTE)
Nutzt ein LTE-Modul und eine isolierte Powerbank, um Brownouts des ESP32 durch Stromspitzen (bis zu 2A) zu verhindern.

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| **USB Powerbank** | Power | `VIN` | 5V Out | Speist ESP32 und LTE parallel |
| **LTE Modul** | UART 1 | `GPIO 32` (RX1) | TX | VCC direkt an 5V Powerbank! |
| | | `GPIO 33` (TX1) | RX | |
| **GPS Modul**| UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V vom ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| **MicroSD-Modul** | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC an 3.3V vom ESP32 |
| **DS18B20 (Motor/ESC)** | 1-Wire | `GPIO 4` | DQ (Daten) | Parallel schalten, 4.7kΩ Pull-Up an 3.3V |
| **A3144 Hall-Sensor**| Dig. Out | `GPIO 2` | DO (Signal) | Nutzt ESP32 PCNT Hardware-Counter |

### Variante B: Offline (Lokales Logging)
Gewichtsoptimiert. Verzichtet auf Modem und Powerbank. Die Stromversorgung (ca. 200mA) erfolgt direkt über das RC-Auto.

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| **RC-Empfänger (BEC)**| Power | `VIN` | 5V (Rot) | Speist den ESP32 direkt über ESC/Empfänger |
| | | `GND` | GND (Schwarz)| Gemeinsame Masse |
| **GPS Modul**| UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V vom ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| **MicroSD-Modul** | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC an 3.3V vom ESP32 |
| **DS18B20 (Motor/ESC)** | 1-Wire | `GPIO 4` | DQ (Daten) | Parallel schalten, 4.7kΩ Pull-Up an 3.3V |
| **A3144 Hall-Sensor**| Dig. Out | `GPIO 2` | DO (Signal) | Nutzt ESP32 PCNT Hardware-Counter |

---

## 3. Schritt-für-Schritt Aufbau

### Phase 1: Vorbereitung & Software
1. **Abhängigkeiten installieren:** Öffne die Arduino IDE / PlatformIO und installiere folgende Bibliotheken: `TinyGPSPlus`, `OneWire` und `DallasTemperature`. *(Für die Cloud-Variante zusätzlich: `TinyGSM` und `PubSubClient`)*.
2. **Konfiguration:** Flashe die entsprechende Firmware auf den ESP32 (Cloud oder Offline Skript). 

### Phase 2: Löten & Verkabeln (Power-Management)
3. **Stromversorgung aufbauen:**
   * **Cloud-Variante:** Nutze ein USB-Breakout-Board als Y-Verteiler. Verlöte die 5V-Leitung so, dass sie sich splittet und isoliert zum ESP32 (`VIN`) und zum LTE-Modem (`VCC`) führt.
   * **Offline-Variante:** Verlöte ein Standard-Servokabel mit `VIN` (Rot) und `GND` (Schwarz) des ESP32, um es später in einen freien Kanal des RC-Empfängers zu stecken.
4. **Bus-Systeme verbinden:** Verlöte GPS, SD-Modul, Hall-Sensor und Temperatursensoren gemäß dem Pin-Mapping.
5. **Pull-Up integrieren:** Löte den 4,7 kΩ Widerstand zwischen die 3.3V-Leitung und die Datenleitung der Temperatursensoren.
6. **Isolieren:** Sichere alle offenen Lötstellen mit Schrumpfschlauch oder Heißkleber gegen Kurzschlüsse durch Vibrationen.

### Phase 3: Mechanische Integration
7. **Zentraleinheit platzieren:** Befestige die Elektronik geschützt im Carten T410R Chassis. Das **GPS-Modul** muss zwingend mit der Keramik-Antenne nach oben zeigen und darf nicht durch Carbon oder Metall verdeckt werden.
8. **Magnet montieren:** Klebe den Neodym-Magneten auf die Kardanwelle (Gegengewicht gegen Unwucht nicht vergessen!).
9. **Hall-Sensor ausrichten:** Montiere den Sensor starr so, dass der Magnet bei jeder Umdrehung in ca. 1-2 mm Abstand daran vorbeifliegt.
10. **Temperatursensoren:** Einen Sensor zwischen die Kühlrippen des ESC klemmen. Den zweiten an die Motor-Außenhülle anlegen und mit hitzebeständigem Kaptonband fixieren.

---

## 4. Betrieb

**Workflow Variante A (Cloud):**
1. **Einschalten:** Verbinde die USB-Powerbank. Der ESP32 fährt hoch, initialisiert die SD-Karte als Fallback und sucht nach einem GPS-Fix.
2. **Verbindungsaufbau:** Das System wählt sich automatisch ins LTE-Netz ein und verbindet sich mit der Cloud (MQTT-Broker).
3. **Fahrt:** Alle Daten (Position, Speed, RPM, Temps) werden mit 2 Hz als JSON-Payload in die Cloud gestreamt und in Echtzeit überwacht.

**Workflow Variante B (Offline):**
1. **Einschalten:** Das System startet automatisch mit dem Einschalten des RC-Autos (Power via ESC/Empfänger).
2. **Log:** Sensordaten werden mit 2 Hz kontinuierlich als strukturiertes JSON/CSV auf die MicroSD-Karte geschrieben.
3. **Analyse:** Nach der Fahrt wird die MicroSD-Karte entnommen und manuell am PC in die Data-Analytics-Plattform eingelesen (Batch-Ingestion).

---

## 5. Reddit-Feedback-Sync

Dieses Repository nutzt eine GitHub Action, um Community-Feedback zu dem Carten-Telemetrie Projekt aus dem zugehörigen [Reddit-Thread](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/) automatisch zu extrahieren und im Repository zu sichern. 

Da die reguläre Reddit-API und direkte JSON-Abfragen oftmals Cloud-Server (wie die von GitHub Actions) blockieren, nutzt dieses Setup den öffentlichen RSS-Feed des Posts als stabilen Workaround.

### Architektur & Funktionsweise
* **Skript (`scripts/fetch_reddit.py`):** Ein Python-Skript ruft den RSS-Feed des Posts ab (`feedparser`) und bereinigt den HTML-Code der Kommentare (`beautifulsoup4`), um reinen Text zu erhalten.
* **Automatisierung (`.github/workflows/reddit-sync.yml`):** Eine GitHub Action führt das Python-Skript automatisch jeden Tag um 08:00 UTC aus.
* **Output:** Neue Kommentare werden als Zitate in die Datei `reddit/reddit_feedback.md` geschrieben. Die Action erstellt bei Änderungen automatisch einen Commit und pusht diesen in den `main` Branch.

### Manueller Sync
Falls das Feedback außerhalb des täglichen Rhythmus sofort aktualisiert werden soll:
1. Im Repository auf den Reiter **Actions** wechseln.
2. In der linken Seitenleiste den Workflow **Fetch Reddit Feedback** auswählen.
3. Auf den Button **Run workflow** klicken und den `main` Branch bestätigen.
4. Nach Abschluss des Jobs ist die aktualisierte `reddit_feedback.md` im Ordner `docs/` zu finden.
