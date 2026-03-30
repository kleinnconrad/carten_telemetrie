# RC-Telemetrie-System

Dieses System erfasst hochfrequente Telemetriedaten (Geschwindigkeit, Drehzahl, Temperaturen) in einem RC-Fahrzeug und streamt diese in Echtzeit über ein Mobilfunknetz (LTE) an ein Cloud-Backend (via MQTT). Die Architektur ist auf höchste Zuverlässigkeit und Systemsicherheit ausgelegt, inklusive einer vom RC-Antrieb komplett isolierten Stromversorgung.

![schaltplan2](https://github.com/kleinnconrad/carten_telemetrie/blob/main/schaltplan/schaltplan.png)

## 1. System-Architektur

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

## 3. Autarke Stromversorgung (Power-Management)

Die zuverlässige Stromversorgung ist der kritischste Punkt dieses Cloud-Telemetrie-Systems. Das LTE-Modem (SIM7000) benötigt beim Senden im Mobilfunknetz kurzzeitig Stromspitzen von **bis zu 2 Ampere**. Würde man das Modem direkt an den 5V-Ausgang des ESP32 anschließen, käme es sofort zu einem Spannungsabfall (Brownout) und der Controller würde unkontrolliert neu starten. 

Um dies zu verhindern, nutzen wir eine isolierte Parallel-Schaltung mittels eines **USB Breakout-Boards**. 

### Benötigte Komponenten
* 1x Standard USB-Powerbank (5V, min. 2.1A Output)
* 1x USB Breakout-Board (Passend zum Anschluss der Powerbank, meist USB-A oder USB-C)
* Kupferlitze (Empfehlung: AWG 22 für das LTE-Modul, um Kabelwiderstände zu minimieren)

### Physischer Aufbau (Die 5V-Weiche)

Das Breakout-Board fungiert als Y-Verteiler, der den ESP32 und das LTE-Modem unabhängig voneinander aus derselben Quelle speist:

1. **VCC (5V Pluspol):**
   * Nimm zwei rote Kabel (ein dickeres für LTE, ein Standard-Kabel für den ESP32).
   * Verzwirble die blanken Kupferenden beider Kabel miteinander.
   * Stecke die verzwirbelten Enden gemeinsam durch das Pad mit der Aufschrift `VCC` (oder `5V`) auf dem Breakout-Board und verlöte sie großzügig.
   * Führe das eine Kabel an den `VIN` (oder 5V) Pin des ESP32 und das andere an den `VCC` (5V In) Pin des LTE-Moduls.

2. **GND (Gemeinsame Masse):**
   * Wiederhole den exakt gleichen Vorgang mit zwei schwarzen Kabeln am `GND`-Pad des Breakout-Boards.
   * Führe ein Kabel an einen `GND` Pin des ESP32 und das andere an den `GND` Pin des LTE-Moduls. 
   * *Wichtig: Alle Komponenten des Systems (Sensoren, GPS, SD-Karte) müssen zwingend über den ESP32 mit diesem GND verbunden sein (Common Ground), da sonst die serielle Datenübertragung fehlschlägt.*

3. **Daten-Pins (D+ / D-):**
   * Diese Pins auf dem Breakout-Board werden komplett ignoriert, da die USB-Verbindung rein der Stromversorgung dient.

Sobald das Breakout-Board in die Powerbank gesteckt wird, fahren beide Module parallel hoch, ohne sich bei Stromspitzen gegenseitig zu beeinflussen.

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

1. **Boot:** Nach dem Verbinden der USB-Powerbank initialisiert der ESP32 die SD-Karte und wartet auf einen GPS-Fix.
2. **Connect:** Das Modem wählt sich ins LTE-Netz ein und baut die TCP-Verbindung zum MQTT-Broker der Cloud auf.
3. **Stream:** Sensordaten werden kontinuierlich erfasst und in Echtzeit an das Cloud-Dashboard gepusht. 
4. **Analyse:** Die Auswertung der Fahrt (Geschwindigkeitskurven, Temperatur-Warnungen) erfolgt live über das Cloud-Frontend (z.B. Grafana), ein lokaler Download der CSV ist nur im Fehlerfall nötig.
