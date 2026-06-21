# RC-Telemetrie-System

## Inhaltsverzeichnis
* [1. System-Architektur](#1-system-architektur)
* [2. Schaltplan](#2-schaltplan)
* [3. Pin-Mapping](#3-pin-mapping)
* [4. Stromversorgung](#4-stromversorgung)
* [5. Schaltplan Generierung](#5-schaltplan-generierung)
* [6. Betrieb](#6-betrieb)

Dieses System erfasst Telemetriedaten (Geschwindigkeit, Drehzahl, Temperaturen) in einem RC-Fahrzeug als lokales Data-Logging.

## 1. System-Architektur
* Betriebsmodus: Batch-Logging auf MicroSD-Karte.
* GPS-Tracking: Ein GPS-Modul liefert Geodaten und Geschwindigkeitswerte via NMEA-Protokoll (Hardware-UART).
* Logging: Die MicroSD-Karte dient als primärer Speicher.
* Sensor-Auslesen: Die Erfassung erfolgt asynchron. Impulse des Hall-Sensors werden über einen Hardware-Zähler (PCNT) registriert.

## 2. Schaltplan

![Schaltplan Offline](Schaltplan_Offline_30Pin.png)

### Mermaid Diagramm

```mermaid
graph LR
    subgraph "RC Empfänger"
        v5[5V Rot]
        gnd_rx[GND Schwarz]
    end

    subgraph "ESP32"
        vin[VIN 5V In]
        v33[3V3 Out]
        gnd_esp[GND]
        d2[D2]
        d4[D4]
        d5[D5]
        d18[D18]
        d19[D19]
        d23[D23]
        rx2[RX2]
        tx2[TX2]
    end

    subgraph "MicroSD"
        sd_vcc[VCC]
        sd_gnd[GND]
        sd_mosi[MOSI]
        sd_miso[MISO]
        sd_sck[SCK]
        sd_cs[CS]
    end

    subgraph "GPS BN-220"
        gps_vcc[VCC]
        gps_gnd[GND]
        gps_tx[TX]
        gps_rx[RX]
    end

    subgraph "Sensoren"
        mot_vcc[Motor Temp VDD]
        mot_gnd[Motor Temp GND]
        mot_dq[Motor Temp Data]
        esc_vcc[ESC Temp VDD]
        esc_gnd[ESC Temp GND]
        esc_dq[ESC Temp Data]
        hall_vcc[Hall VCC]
        hall_gnd[Hall GND]
        hall_do[Hall DOUT]
    end

    v5 -->|Stromversorgung| vin
    gnd_rx -->|Masse| gnd_esp

    v33 -->|3.3V| sd_vcc
    gnd_esp -->|Masse| sd_gnd
    d23 -->|MOSI| sd_mosi
    d19 -->|MISO| sd_miso
    d18 -->|SCK| sd_sck
    d5 -->|CS| sd_cs

    v33 -->|3.3V| gps_vcc
    gnd_esp -->|Masse| gps_gnd
    rx2 -->|RX| gps_tx
    tx2 -->|TX| gps_rx

    v33 -->|3.3V| mot_vcc
    gnd_esp -->|Masse| mot_gnd
    d4 -->|1-Wire| mot_dq

    v33 -->|3.3V| esc_vcc
    gnd_esp -->|Masse| esc_gnd
    d4 -->|1-Wire| esc_dq

    v33 -->|3.3V| hall_vcc
    gnd_esp -->|Masse| hall_gnd
    d2 -->|Signal| hall_do
```

## 3. Pin-Mapping
Alle Komponenten benötigen eine gemeinsame Masse (GND). Serielle Verbindungen erfordern gekreuzte Leitungen (TX an RX, RX an TX).

| Komponente | Interface | ESP32 Pin | Sensor Pin | Bemerkung |
| :--- | :--- | :--- | :--- | :--- |
| RC-Empfänger | Power | `VIN` | 5V (Rot) | Versorgung über ESC/Empfänger |
| | | `GND` | GND (Schwarz)| Gemeinsame Masse |
| GPS Modul | UART 2 | `GPIO 16` (RX2) | TX | VCC an 3.3V ESP32 |
| | | `GPIO 17` (TX2) | RX | |
| MicroSD-Modul | SPI | `GPIO 23`, `19`, `18`, `5` | MOSI, MISO, SCK, CS | VCC an 3.3V ESP32 |
| DS18B20 (Motor)| 1-Wire | `GPIO 4` | DQ | |
| DS18B20 (ESC)| 1-Wire | `GPIO 4` | DQ | Parallelschaltung |
| A3144 Hall-Sensor| Digital Out | `GPIO 2` | DO | PCNT-Nutzung |

## 4. Stromversorgung
ESP32 und Sensorik benötigen 150-250 mA. Die Versorgung erfolgt über den Motorregler (ESC) und Empfänger.
1. Anschluss eines Servokabels an den RC-Empfänger.
2. Rotes Kabel (5V) an den VIN-Pin des ESP32.
3. Schwarzes Kabel (GND) an den GND-Pin des ESP32.

## 5. Schaltplan Generierung
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

## 6. Betrieb
1. Boot: Systemstart bei Einschalten des RC-Fahrzeugs.
2. Log: Speicherung der Sensordaten mit 2 Hz auf der MicroSD-Karte.
3. Analyse: Manuelles Einlesen der MicroSD-Karte.
