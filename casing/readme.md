# Gehäuse Abbildungen und Integration

## Inhaltsverzeichnis
* [1. Visuelle Dokumentation](#1-visuelle-dokumentation)
* [2. Anordnung der Komponenten](#2-anordnung-der-komponenten)
* [3. Thermische Aspekte](#3-thermische-aspekte)

## 1. Visuelle Dokumentation

Nachfolgend sind die fotografischen Nachweise der Gehäusekomponenten sowie deren Assemblierung aufgeführt.

![case1](https://github.com/kleinnconrad/carten_telemetrie/blob/main/casing/PXL_20260519_062427438.jpg)
![case2](https://github.com/kleinnconrad/carten_telemetrie/blob/main/casing/PXL_20260519_062433621.jpg)
![case3](https://github.com/kleinnconrad/carten_telemetrie/blob/main/casing/PXL_20260519_062444870.jpg)

## 2. Anordnung der Komponenten
Die physische Anordnung innerhalb des Gehäuses folgt diesen Konstruktionsprinzipien:
* **Terminal-Breakout-Board:** Dient als Basis. Der ESP32 wird in die Stiftleisten gesteckt. Dies ermöglicht einen werkzeuglosen Wechsel des Mikrocontrollers im Falle eines Hardwaredefekts.
* **Klemmen:** Alle Kabelverbindungen (Sensoren, Stromversorgung, SPI-Bus) werden in die Schraubklemmen des Breakout-Boards geführt. Lötverbindungen direkt am ESP32 sind untersagt, um die Modularität zu wahren.
* **Zugänglichkeit:** Der MicroSD-Kartenslot muss am montierten Gehäuse frei zugänglich bleiben, um die Daten nach dem Betrieb manuell entnehmen zu können, ohne das Gehäuse zu öffnen.

## 3. Thermische Aspekte
Der ESP32 erzeugt im Betrieb Verlustleistung. Zudem herrschen im RC-Chassis (insbesondere unter einer geschlossenen Karosserie) erhöhte Umgebungstemperaturen.
* **Belüftung:** Das Gehäusedesign beinhaltet minimale Toleranzspalten, die als passive Entlüftung dienen.
* **Positionierung:** Das Gehäuse ist im Fahrzeug so zu platzieren, dass es weder dem direkten Luftstrom des Motor-Kühlers ausgesetzt ist (Messverfälschung der Umgebungstemperatur), noch direkt an wärmeabstrahlenden Bauteilen (ESC-Kühlkörper) anliegt.
