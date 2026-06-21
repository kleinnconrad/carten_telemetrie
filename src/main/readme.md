# Firmware: RC Telemetrie

## Inhaltsverzeichnis
* [1. Firmware-Varianten](#1-firmware-varianten)
* [2. Kern-Funktionen](#2-kern-funktionen)
* [3. Bibliotheken](#3-bibliotheken)
* [4. Konfiguration](#4-konfiguration)

Diese Firmware ist für den ESP32 als IoT-Edge-Client konzipiert. Es existieren zwei Varianten (`main_cloud` und `main_offline`) zur Erfassung von GPS-Daten, Drehzahlen und Temperaturen.

## 1. Firmware-Varianten
* `main_cloud`: Baut eine Verbindung zum Mobilfunknetz auf und überträgt Telemetriedaten über MQTT. Die Daten werden zusätzlich auf der SD-Karte gesichert.
* `main_offline`: Variante ohne Mobilfunk-Stack. Speichert JSON-Payloads mit 2 Hz auf der MicroSD-Karte.

## 2. Kern-Funktionen
* Asynchrone Architektur: Das Parsen von GPS-NMEA-Daten und Temperaturmessungen blockieren den Main-Loop nicht.
* Hardware-Zähler (PCNT): Erfassung der Hall-Sensor-Impulse über den PCNT-Hardware-Zähler des ESP32.
* Zeitberechnung: Verwendung von `timeDelta`-Berechnungen für die Drehzahlbestimmung.
* Hardware UART: Nutzung der Hardware-Serial-Schnittstellen für die Kommunikation mit GPS-Modul (`UART 2`) und LTE-Modem (`UART 1`).

## 3. Bibliotheken
Folgende Bibliotheken sind für die Kompilierung erforderlich:

Basis-Bibliotheken (Beide Varianten):
* `TinyGPSPlus`: Parsen der NMEA-Sätze des GPS-Moduls.
* `OneWire` & `DallasTemperature`: Auslesen der Temperatursensoren.

Zusätzliche Bibliotheken (`main_cloud`):
* `TinyGSM`: AT-Kommunikation mit dem LTE-Modem.
* `PubSubClient`: MQTT-Verbindung.

## 4. Konfiguration
In der Cloud-Variante müssen netzwerk- und cloudspezifische Parameter im Quellcode konfiguriert werden:

```cpp
// 1. Mobilfunk-Provider (APN)
const char apn[]      = "internet"; 
const char gprsUser[] = "";
const char gprsPass[] = "";

// 2. Cloud-Backend (MQTT Broker)
const char* mqttServer = "dein-mqtt-broker.com";
const int   mqttPort   = 1883;
const char* mqttTopic  = "rc-car/telemetry/live";
```