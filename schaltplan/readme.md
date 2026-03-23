# RC-Telemetrie-System: Architektur & Aufbau

Dieses System erfasst Telemetriedaten in einem RC-Fahrzeug. Die Architektur ist auf Robustheit und asynchrone Datenerfassung ausgelegt, um Blockaden durch langsame Sensor-Auslesezeiten (DS18B20) oder SD-Karten-Schreibzyklen zu kompensieren.

![schaltplan](https://github.com/kleinnconrad/carten_telemetrie/blob/main/schaltplan/RC_Telemetrie_Schaltplan_Pro.png)

## 1. System-Architektur & Timing

* **Sampling-Rate:** Das System sampelt mit 2 Hz (alle 500 ms).
* **RPM-Erfassung (Realtime):** Der Hall-Sensor ist an GPIO 2 (Hardware-Interrupt) angebunden. Impulse werden asynchron in Echtzeit gezählt, unbeeinflusst vom Main-Loop-Timing.
* **Temperatur (1-Wire):** Die DS18B20 Sensoren teilen sich einen Bus an GPIO 4. Da die 12-bit Wandlung ca. 750 ms benötigt, werden die Werte asynchron zum RPM-Zähler abgefragt.
* **Storage (SPI):** Daten werden via SPI an das MicroSD-Modul gesendet (Append-Mode).

## 2. Pin-Mapping (Verkabelung)

Alle Komponenten teilen sich eine gemeinsame Masse (**GND**).

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| **RC-Empfänger** | Power | `VIN` | VCC | 5V/6V BEC Spannung |
| **MicroSD-Modul** | SPI | `GPIO 23` | MOSI | |
| | | `GPIO 19` | MISO | |
| | | `GPIO 18` | SCK | |
| | | `GPIO 5` | CS | |
| **DS18B20 (Motor)** | 1-Wire | `GPIO 4` | DQ (Daten) | Benötigt 4.7kΩ Pull-Up an 3.3V |
| **DS18B20 (ESC)** | 1-Wire | `GPIO 4` | DQ (Daten) | Parallel zum Motor-Sensor schalten |
| **A3144 Hall-Sensor**| Digital Out | `GPIO 2` | DO (Signal) | Nutzt Hardware-Interrupt (`FALLING`) |

## 3. Schaltplan generieren (mit `uv`)

Um den visuellen Schaltplan als PNG zu generieren, nutzen wir Python und das Tool `uv`, um die Abhängigkeit (`graphviz`) nicht global installieren zu müssen.

**graphviz:**

1. System-Abhängigkeit installieren:
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
   uv run --with graphviz schaltplan.py
   ```

## 4. Betrieb
Nach dem Einschalten des Fahrzeugs startet der ESP32 automatisch die Ingestion Pipeline. 
Nach der Fahrt:
1. Mit dem WLAN `RC-Telemetry` verbinden.
2. `http://192.168.4.1` aufrufen.
3. CSV herunterladen.
