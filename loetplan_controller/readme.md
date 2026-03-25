# RC-Telemetrie-System: Cloud Streaming & Architektur

Dieses System erfasst hochfrequente Telemetriedaten (Geschwindigkeit, Drehzahl, Temperaturen) in einem RC-Fahrzeug und streamt diese in Echtzeit über ein Mobilfunknetz (LTE) an ein Cloud-Backend (via MQTT). Die Architektur ist auf höchste Zuverlässigkeit und Systemsicherheit ausgelegt, inklusive einer vom RC-Antrieb komplett isolierten Stromversorgung.

![schaltplan2](https://github.com/kleinnconrad/carten_telemetrie/blob/main/loetplan_controller/Schaltplan_Cloud.png)

## 1. System-Architektur & Features

* **Isolierte Stromversorgung:** Die gesamte Telemetrie-Elektronik wird über eine autarke 5V USB-Powerbank versorgt. Stromspitzen des LTE-Modems (bis zu 2A) können so keinen Brownout des RC-Empfängers verursachen.
* **Live-Streaming (LTE & MQTT):** Daten werden asynchron als JSON-Payloads via MQTT über ein SIM7000G LTE-Modul an die Cloud gesendet.
* **GPS Tracking:** Ein dediziertes GPS-Modul liefert echte Geodaten und hochpräzise Geschwindigkeitswerte via NMEA-Protokoll (Hardware-UART).
* **Lokales Backup (Ringpuffer):** Die MicroSD-Karte fungiert über den SPI-Bus als Fallback. Bei Verbindungsabbrüchen im Mobilfunknetz gehen keine Speedrun-Daten verloren.
* **Asynchrones Sensor-Auslesen:** Zeitintensive Operationen (wie die 750ms Wandlungszeit der DS18B20 1-Wire Sensoren) blockieren niemals den Main-Loop.

## 2. Pin-Mapping (Verkabelung)

**WICHTIG:** Alle Komponenten müssen sich eine gemeinsame Masse (**GND**) teilen. RX- und TX-Leitungen bei seriellen Verbindungen müssen immer überkreuzt angeschlossen werden (TX an RX, RX an TX).

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| **USB Powerbank** | Power | `VIN` | 5V Out | Speist ESP32 und LTE parallel |
| **LTE Modul (SIM7000)** | UART 1 | `GPIO 32` (RX1) | TX | VCC direkt an 5V Powerbank! |
| | | `GPIO 33` (TX1) | RX | |
| **GPS Modul (BN-220)**| UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V vom ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| **MicroSD-Modul** | SPI | `GPIO 23` | MOSI | |
| | | `GPIO 19` | MISO | |
| | | `GPIO 18` | SCK | |
| | | `GPIO 5` | CS | |
| **DS18B20 (Motor)** | 1-Wire | `GPIO 4` | DQ (Daten) | Benötigt 4.7kΩ Pull-Up an 3.3V |
| **DS18B20 (ESC)** | 1-Wire | `GPIO 4` | DQ (Daten) | Parallel zum Motor-Sensor schalten |
| **A3144 Hall-Sensor**| Digital Out | `GPIO 2` | DO (Signal) | Nutzt Hardware-Interrupt (`FALLING`) |

## 3. Schaltplan generieren (mit `uv`)

Um den visuellen Lötplan als PNG zu generieren, nutzen wir Python und das Tool `uv`, um die Abhängigkeit (`graphviz`) nicht global im System installieren zu müssen.

**graphviz:**

1. System-Abhängigkeit installieren (Alpine Linux):
   ```bash
   sudo apk add graphviz
   ```

2. Tool `uv` herunterladen und Pfad laden:
   ```bash
   curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
   source $HOME/.local/bin/env
   ```

3. Skript ausführen:
   ```bash
   uv run --with graphviz loetplan.py
   ```

## 4. Betrieb & Datenfluss

1. **Boot:** Nach dem Verbinden der USB-Powerbank initialisiert der ESP32 die SD-Karte und wartet auf einen GPS-Fix.
2. **Connect:** Das Modem wählt sich ins LTE-Netz ein und baut die TCP-Verbindung zum MQTT-Broker der Cloud auf.
3. **Stream:** Sensordaten werden kontinuierlich erfasst und in Echtzeit an das Cloud-Dashboard gepusht. 
4. **Analyse:** Die Auswertung der Fahrt (Geschwindigkeitskurven, Temperatur-Warnungen) erfolgt live über das Cloud-Frontend (z.B. Grafana), ein lokaler Download der CSV ist nur im Fehlerfall nötig.
