# Firmware: RC Telemetrie

## Inhaltsverzeichnis
* [1. Firmware-Variante](#1-firmware-variante)
* [2. Kern-Funktionen](#2-kern-funktionen)
* [3. Bibliotheken](#3-bibliotheken)

Diese Firmware ist für den ESP32 als IoT-Edge-Client konzipiert zur Erfassung von GPS-Daten, Drehzahlen und Temperaturen.

## 1. Firmware-Variante
* `main_offline`: Speichert JSON-Payloads mit 2 Hz auf der MicroSD-Karte.

## 2. Kern-Funktionen
* Asynchrone Architektur: Das Parsen von GPS-NMEA-Daten und Temperaturmessungen blockieren den Main-Loop nicht.
* Hardware-Zähler (PCNT): Erfassung der Hall-Sensor-Impulse über den PCNT-Hardware-Zähler des ESP32.
* Zeitberechnung: Verwendung von `timeDelta`-Berechnungen für die Drehzahlbestimmung.
* Hardware UART: Nutzung der Hardware-Serial-Schnittstellen für die Kommunikation mit GPS-Modul (`UART 2`).

## 3. Bibliotheken
Folgende Bibliotheken sind für die Kompilierung erforderlich:

* `TinyGPSPlus`: Parsen der NMEA-Sätze des GPS-Moduls.
* `OneWire` & `DallasTemperature`: Auslesen der Temperatursensoren.