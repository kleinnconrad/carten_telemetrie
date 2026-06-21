# Firmware: RC Telemetrie

## Inhaltsverzeichnis
* [1. Architektur und Firmware-Variante](#1-architektur-und-firmware-variante)
* [2. Kern-Funktionen und Module](#2-kern-funktionen-und-module)
* [3. Datenstruktur und Speicherformat](#3-datenstruktur-und-speicherformat)
* [4. Hardware-Interrupts (PCNT)](#4-hardware-interrupts-pcnt)
* [5. Bibliotheken und Abhängigkeiten](#5-bibliotheken-und-abhängigkeiten)

Diese Firmware ist exklusiv für den ESP32 als lokales Data-Logging-System konzipiert. Sie erfasst zyklisch GPS-Daten, Drehzahlen und Systemtemperaturen.

## 1. Architektur und Firmware-Variante
* `main_offline`: Die Software arbeitet im Batch-Betrieb. Es findet keine drahtlose Kommunikation (weder WiFi noch Bluetooth oder LTE) statt. Der ESP32 fungiert als reiner Sensor-Hub und schreibt die ermittelten Payloads mit einer Frequenz von 2 Hz auf die angeschlossene MicroSD-Karte.
* **Main-Loop:** Die `loop()`-Schleife ist streng blockierungsfrei (non-blocking) implementiert. Verzögerungen durch `delay()` sind bis auf minimale Entprell-Logiken untersagt. Das Timing erfolgt über `millis()`-basierte Zustandsmaschinen.

## 2. Kern-Funktionen und Module
* **Asynchrone Sensorabfrage:** Das Parsen der NMEA-Datensätze des GPS-Moduls erfolgt zeichenweise asynchron. Temperaturmessungen des 1-Wire-Busses werden asynchron angefragt; der Bus blockiert während der Konvertierungszeit (ca. 750 ms für 12-Bit Auflösung) nicht die restliche Codeausführung.
* **Hardware UART:** Zur seriellen Kommunikation mit dem GPS-Modul wird zwingend die Hardware-Serial-Schnittstelle (`UART 2`) an den Pins `GPIO 16` und `17` verwendet. `SoftwareSerial` ist aus Leistungsgründen nicht zulässig.

## 3. Datenstruktur und Speicherformat
Die erhobenen Sensordaten werden formatiert auf der MicroSD-Karte abgelegt.
* **Dateisystem:** FAT32 (SDHC-Karten bis 32 GB empfohlen).
* **Format:** Jeder Log-Eintrag besteht wahlweise aus einem JSON-Objekt oder einer durch Kommata getrennten Zeile (CSV).
* **Metriken:** Timestamps (aus GPS-RTC bezogen), Motor-Temperatur (°C), ESC-Temperatur (°C), Drehzahl (RPM), GPS-Koordinaten (Lat/Lon), Satellitenanzahl (HDOP-Wert zur Genauigkeitsprüfung).

## 4. Hardware-Interrupts (PCNT)
Für die exakte Erfassung der Drehzahl über den A3144 Hall-Sensor wird das PCNT (Pulse Counter) Peripheriemodul des ESP32 genutzt. 
* Im Gegensatz zu softwarebasierten GPIO-Interrupts, die bei hohen Frequenzen zum Absturz des Schedulers führen können, zählt das PCNT-Modul Impulse autark auf der Hardware-Ebene. 
* Die Drehzahl (RPM) wird über eine `timeDelta`-Berechnung ermittelt: Anzahl der Impulse im Messintervall, skaliert auf eine Minute.

## 5. Bibliotheken und Abhängigkeiten
Folgende externe Bibliotheken sind für den Build-Prozess (Kompilierung über PlatformIO oder Arduino IDE) zwingend erforderlich:

* `TinyGPSPlus`: Effizientes Parsen der eingehenden NMEA-Rohdaten.
* `OneWire`: Protokoll-Ebene für den Bus der Temperatursensoren.
* `DallasTemperature`: Höherwertige Abstraktionsschicht zur Adressierung und Auslesung der DS18B20-ICs.
* `SPI` und `SD`: Core-Bibliotheken für den Dateizugriff auf das MicroSD-Modul.