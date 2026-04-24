# RC-Telemetrie-System

Dieses System erfasst hochfrequente Telemetriedaten (Geschwindigkeit, Drehzahl, Temperaturen) in einem RC-Fahrzeug. Das Projekt kann in zwei Varianten aufgebaut werden: Als vernetzte **Cloud-Version** (Live-Streaming über Mobilfunk) oder als gewichtsoptimierte **Offline-Version** (lokales Data-Logging über den RC-Empfänger). 

Beide Architekturen sind auf höchste Zuverlässigkeit bei Fahrten mit bis zu 100 km/h ausgelegt.

## Schaltpläne

### Variante A: Cloud (LTE & Live-Streaming)
Nutzt ein LTE-Modul und eine isolierte Powerbank für Live-Metriken.
![Schaltplan Cloud](https://github.com/kleinnconrad/carten_telemetrie/blob/main/schaltplan/schaltplan.png)

### Variante B: Offline 30 PIN (Gewichtsoptimiert & Lokales Logging)
Verzichtet auf LTE und Powerbank. Stromversorgung erfolgt direkt über das RC-Auto.
![Schaltplan Offline](https://github.com/kleinnconrad/carten_telemetrie/blob/main/schaltplan/Schaltplan_Offline_30Pin.png)

---

## 1. System-Architektur

* **Zwei Betriebsmodi:** * *Cloud-Modus:* Daten werden asynchron als JSON-Payloads via MQTT über ein SIM7000G LTE-Modul an die Cloud gesendet.
  * *Offline-Modus:* Reines Batch-Logging auf die MicroSD-Karte. Massive Gewichtsersparnis durch Wegfall von Modem und Powerbank.
* **GPS Tracking:** Ein dediziertes GPS-Modul liefert echte Geodaten und hochpräzise Geschwindigkeitswerte (Doppler-Effekt) via NMEA-Protokoll (Hardware-UART).
* **Ausfallsicheres Logging:** Die MicroSD-Karte fungiert über den SPI-Bus in der Cloud-Variante als Fallback und in der Offline-Variante als primärer Datenspeicher.
* **Asynchrones Sensor-Auslesen:** Zeitintensive Operationen (wie die 750ms Wandlungszeit der DS18B20 1-Wire Sensoren) blockieren niemals den Main-Loop. Pulse des Hall-Sensors werden über einen dedizierten Hardware-Zähler (PCNT) verlustfrei erfasst.

## 2. Pin-Mapping (Verkabelung)

**WICHTIG:** Alle Komponenten müssen sich eine gemeinsame Masse (**GND**) teilen. RX- und TX-Leitungen bei seriellen Verbindungen müssen immer überkreuzt angeschlossen werden (TX an RX, RX an TX).

### Variante A: Cloud (LTE)
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
| **A3144 Hall-Sensor**| Digital Out | `GPIO 2` | DO (Signal) | Nutzt internen Pull-Up & PCNT |

### Variante B: Offline (Lokales Logging)
| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| **RC-Empfänger (BEC)**| Power | `VIN` | 5V (Rot) | Stromversorgung direkt über ESC/Empfänger |
| | | `GND` | GND (Schwarz)| Gemeinsame Masse |
| **GPS Modul (BN-220)**| UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V vom ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| **MicroSD-Modul** | SPI | `GPIO 23` | MOSI | |
| | | `GPIO 19` | MISO | |
| | | `GPIO 18` | SCK | |
| | | `GPIO 5` | CS | |
| **DS18B20 (Motor)** | 1-Wire | `GPIO 4` | DQ (Daten) | Benötigt 4.7kΩ Pull-Up an 3.3V |
| **DS18B20 (ESC)** | 1-Wire | `GPIO 4` | DQ (Daten) | Parallel zum Motor-Sensor schalten |
| **A3144 Hall-Sensor**| Digital Out | `GPIO 2` | DO (Signal) | Nutzt internen Pull-Up & PCNT |

## 3. Stromversorgung (Power-Management)

Abhängig von der gewählten Variante unterscheidet sich die Stromversorgung grundlegend, um Brownouts (Spannungsabfälle) des ESP32 zu verhindern.

### Variante A: Cloud (Isolierte Powerbank)
Das LTE-Modem benötigt beim Senden im Mobilfunknetz kurzzeitig Stromspitzen von **bis zu 2 Ampere**. Um den ESP32 zu schützen, nutzen wir eine isolierte Parallel-Schaltung mittels eines **USB Breakout-Boards**.
1. **VCC (5V Pluspol):** Zwei Kabel am `VCC`-Pad des Breakout-Boards verlöten. Ein Kabel führt zum `VIN` des ESP32, das andere direkt zum `VCC` des LTE-Moduls.
2. **GND (Gemeinsame Masse):** Zwei Kabel am `GND`-Pad des Breakout-Boards verlöten und an ESP32 und LTE-Modul verteilen.
3. *Daten-Pins (D+ / D-)* am Breakout-Board werden ignoriert.

### Variante B: Offline (RC-Empfänger / BEC)
In der Offline-Variante entfällt das stromhungrige LTE-Modul. Der ESP32 und die Sensorik verbrauchen zusammen nur ca. 150-250 mA. Dies kann problemlos vom Motorregler (ESC) über den Empfänger bereitgestellt werden.
1. Ein Standard-Servokabel in einen freien Kanal des RC-Empfängers stecken.
2. Das rote Kabel (5V) mit dem `VIN` Pin des ESP32 verbinden.
3. Das schwarze Kabel (GND) mit einem `GND` Pin des ESP32 verbinden.
4. *Vorteil:* Massive Gewichtsersparnis, da die schwere USB-Powerbank komplett entfällt.

## 4. Schaltplan generieren (mit `uv`)

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
   uv run --with graphviz schaltplan.py
   ```

## 5. Betrieb
### Cloud Workflow
1. **Boot:** Nach dem Verbinden der USB-Powerbank initialisiert der ESP32 die SD-Karte und wartet auf einen GPS-Fix.
2. **Connect:** Das Modem wählt sich ins LTE-Netz ein und baut die TCP-Verbindung zum MQTT-Broker der Cloud auf.
3. **Stream:** Sensordaten werden kontinuierlich erfasst und in Echtzeit an das Cloud-Dashboard gepusht. 
4. **Analyse:** Die Auswertung der Fahrt (Geschwindigkeitskurven, Temperatur-Warnungen) erfolgt live über das Cloud-Frontend (z.B. Grafana), ein lokaler Download der CSV ist nur im Fehlerfall nötig.

### Offline-Workflow:
1. **Boot:** Das System startet automatisch mit dem Einschalten des RC-Autos (ESC).
2. **Log:** Sensordaten werden mit 2 Hz kontinuierlich als JSON/CSV auf die MicroSD-Karte geschrieben.
3. **Analyse:** Nach der Fahrt wird die MicroSD-Karte entnommen und manuell am PC in die Data-Analytics-Plattform eingelesen (Batch-Ingestion).
