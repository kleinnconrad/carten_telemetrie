# carten_telemetrie
Entwicklung einer Cloud-Telemetrie-Lösung für einen Carten T410R [![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/kleinnconrad/RC100), um Temperatur (Motor, ESC), Drehzahl (Kardanwelle) und GPS-Daten (Geschwindigkeit, Position) in Echtzeit zu erfassen.

## Inhaltsverzeichnis

* [Bauanleitung: DIY Cloud-Telemetrie-System (ESP32 via LTE)](#bauanleitung-diy-cloud-telemetrie-system-esp32-via-lte)
  * [1. Stückliste (Bill of Materials)](#1-stückliste-bill-of-materials)
  * [2. Schaltplan & Pin-Belegung](#2-schaltplan--pin-belegung)
    * [Stromversorgung (Isoliert via Powerbank)](#stromversorgung-isoliert-via-powerbank)
    * [LTE-Modem (UART 1)](#lte-modem-uart-1)
    * [GPS-Modul (UART 2)](#gps-modul-uart-2)
    * [MicroSD-Karten-Modul (SPI-Bus)](#microsd-karten-modul-spi-bus)
    * [Temperatursensoren (DS18B20)](#temperatursensoren-ds18b20)
    * [Hall-Sensor (RPM)](#hall-sensor-rpm)
  * [3. Schritt-für-Schritt Aufbau](#3-schritt-für-schritt-aufbau)
    * [Phase 1: Vorbereitung & Software](#phase-1-vorbereitung--software)
    * [Phase 2: Löten & Verkabeln](#phase-2-löten--verkabeln)
    * [Phase 3: Mechanische Integration](#phase-3-mechanische-integration)
  * [4. Betrieb & Live-Streaming](#4-betrieb--live-streaming)
  * [5. Reddit-Feedback-Sync](#5-reddit-feedback-sync)

# Bauanleitung: DIY Cloud-Telemetrie-System (ESP32 via LTE)

Dieses Dokument beschreibt den Aufbau eines autarken IoT-Edge-Nodes für RC-Fahrzeuge. Die Sensordaten werden live über das Mobilfunknetz an ein Cloud-Dashboard (via MQTT) gestreamt. Eine MicroSD-Karte dient als ausfallsicheres, lokales Backup-System. Die Stromversorgung ist zum Schutz vor Brownouts komplett von der RC-Elektronik isoliert.

---

## 1. Stückliste (Bill of Materials)

| Komponente | Spezifikation / Typ | Anzahl | Bemerkung |
| :--- | :--- | :--- | :--- |
| **Microcontroller** | ESP32 Dev Board (z.B. NodeMCU) | 1 | Zentraleinheit für Ingestion & Streaming |
| **Stromversorgung** | USB Powerbank (klein/leicht) | 1 | Isoliertes 5V Power-Management |
| **LTE-Modem** | SIM7000G Breakout-Board | 1 | Für die Cloud-Anbindung (inkl. SIM-Karte) |
| **GPS-Modul** | BN-220 (u-blox) | 1 | Für Geodaten & exakte Geschwindigkeit |
| **Speichermodul** | MicroSD-Karten-Modul (SPI) | 1 | Lokaler Ringpuffer (3.3V-kompatibel) |
| **Temperatursensor** | DS18B20 (Wasserdicht) | 2 | Digitale 1-Wire Sensoren für Motor & ESC |
| **Drehzahlsensor** | Hall-Sensor Modul (z.B. A3144) | 1 | Erfasst das Magnetfeld für RPM-Berechnung |
| **Magnet** | Neodym-Magnet (klein, z.B. 3x2mm) | 1 | Wird auf rotierende Welle geklebt |
| **Widerstand** | 4,7 kΩ (Kilo-Ohm) | 1 | Pull-Up-Widerstand für den 1-Wire Bus |
| **Terminal/Breakout Board** | Anzahl der Pins muss passen | 1 | - |

---

## 2. Schaltplan & Pin-Belegung

**WICHTIG:** Alle Komponenten teilen sich eine gemeinsame Masse (**GND**). Bei seriellen Verbindungen (UART) müssen die Leitungen zwingend überkreuzt werden (TX an RX, RX an TX).

### Stromversorgung (Isoliert via Powerbank)
* Das 5V-Kabel (Rot) der Powerbank splittet sich und geht an **VIN** des ESP32 **UND** an **VCC** des LTE-Modems.
* Das GND-Kabel (Schwarz) geht an **GND** des ESP32 **UND** an **GND** des LTE-Modems.

### LTE-Modem (UART 1)
* **VCC & GND:** Direkt an die 5V Powerbank!
* **TX (Senden):** an **GPIO 32** (RX1 am ESP32)
* **RX (Empfangen):** an **GPIO 33** (TX1 am ESP32)

### GPS-Modul (UART 2)
* **VCC & GND:** an **3.3V** und **GND** des ESP32
* **TX (Senden):** an **GPIO 16** (RX2 am ESP32)
* **RX (Empfangen):** an **GPIO 17** (TX2 am ESP32)

### MicroSD-Karten-Modul (SPI-Bus)
* **VCC & GND:** an **3.3V** und **GND** des ESP32
* **MOSI:** an **GPIO 23**
* **MISO:** an **GPIO 19**
* **SCK / CLK:** an **GPIO 18**
* **CS / SS:** an **GPIO 5**

### Temperatursensoren (DS18B20)
*Beide Sensoren werden exakt parallel angeschlossen.*
* **VCC (Rot) & GND (Schwarz):** an **3.3V** und **GND** des ESP32
* **Data (Gelb/Blau):** an **GPIO 4** des ESP32
* **WICHTIG:** Ein **4,7 kΩ Widerstand** muss als Brücke zwischen den 3.3V-Pin und den Data-Pin (GPIO 4) geschaltet werden.

### Hall-Sensor (RPM)
* **VCC & GND:** an **3.3V** und **GND** des ESP32
* **Signal / DO:** an **GPIO 2** des ESP32

---

## 3. Schritt-für-Schritt Aufbau

### Phase 1: Vorbereitung & Software
1. **Abhängigkeiten installieren:** Öffne die Arduino IDE / PlatformIO und installiere folgende Bibliotheken: `TinyGSM`, `TinyGPSPlus`, `PubSubClient`, `OneWire` und `DallasTemperature`.
2. **Zugangsdaten eintragen:** Trage vor dem Flashen deine SIM-Karten-APN und die Zugangsdaten deines MQTT-Brokers im oberen Bereich der `main.cpp` ein.
3. **Flashen:** Verbinde den ESP32 per USB, lade den C++ Code hoch und prüfe im Seriellen Monitor, ob das LTE-Modem erfolgreich initialisiert wird.

### Phase 2: Löten & Verkabeln
4. **Isolierte Stromversorgung:** Opfere ein altes USB-Kabel, um die 5V-Leitung der Powerbank direkt an das LTE-Modem und den ESP32 anzulöten.
5. **Bus-Systeme verbinden:** Verlöte GPS, SD-Modul, Hall-Sensor und Temperatursensoren gemäß dem Pin-Mapping. Achte auf die UART-Kreuzungen (TX->RX).
6. **Pull-Up integrieren:** Löte den 4,7 kΩ Widerstand zwischen die 3.3V-Leitung und die Datenleitung der Temperatursensoren.
7. **Isolieren:** Sichere alle offenen Lötstellen mit Schrumpfschlauch oder Heißkleber gegen Kurzschlüsse durch Vibrationen.

### Phase 3: Mechanische Integration
8. **Zentraleinheit platzieren:** Befestige die Elektronik geschützt im Carten T410R Chassis. Das **GPS-Modul** muss zwingend mit der Keramik-Antenne nach oben zeigen und darf nicht durch Carbon oder Metall verdeckt werden.
9. **Magnet montieren:** Klebe den Neodym-Magneten auf die Kardanwelle (Gegengewicht gegen Unwucht nicht vergessen!).
10. **Hall-Sensor ausrichten:** Montiere den Sensor starr so, dass der Magnet bei jeder Umdrehung in ca. 1-2 mm Abstand daran vorbeifliegt.
11. **Temperatursensoren:** Einen Sensor zwischen die Kühlrippen des ESC klemmen. Den zweiten an die Motor-Außenhülle anlegen und mit hitzebeständigem Kaptonband fixieren.

---

## 4. Betrieb & Live-Streaming

1. **Einschalten:** Verbinde die USB-Powerbank. Der ESP32 fährt hoch, initialisiert die SD-Karte als Fallback und sucht nach einem GPS-Fix.
2. **Verbindungsaufbau:** Das System wählt sich automatisch ins LTE-Netz ein und verbindet sich mit der Cloud (MQTT-Broker).
3. **Fahrt & Analyse:** Das Auto ist bereit. Alle Daten (Position, Speed, RPM, Temps) werden mit 2 Hz als JSON-Payload in die Cloud gestreamt und können dort in Echtzeit (z.B. über Grafana) überwacht werden. Die CSV-Datei auf der SD-Karte dient lediglich als Backup.

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
