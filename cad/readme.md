# ESP32 Sensor-Station und Gehäuse

## Inhaltsverzeichnis
* [1. Übersicht](#1-übersicht)
* [2. Dateiliste](#2-dateiliste)
* [3. Hardware-Komponenten](#3-hardware-komponenten)
* [4. Druckparameter und Material](#4-druckparameter-und-material)
* [5. Montagehinweise](#5-montagehinweise)
* [6. Quellen](#6-quellen)

## 1. Übersicht
Dieser Ordner enthält die 3D-Druck-Dateien (STL) für die Fertigung der ESP32-Sensor-Station. Das mechanische Konzept besteht aus einem Schutzgehäuse für den Mikrocontroller und einem passgenauen Trägerboard zur Montage der Sensor- und Speichermodule innerhalb des RC-Chassis. Ziel ist der Schutz vor mechanischen Stößen, Staub und Spritzwasser sowie die Zugentlastung der Kabel.

## 2. Dateiliste

| Dateiname | Beschreibung | Herkunft |
| :--- | :--- | :--- |
| `sensor_board_.stl` | Trägerplatte für die Peripherie. Enthält dedizierte Montageplätze für zwei Temperatursensoren (DS18B20), das Micro-SD-Modul und das GPS-Modul. | Eigenentwicklung |
| `esp32-30pin-breakoutboard-case.stl` | Unteres Gehäuseelement für das ESP32 Development Board (30-Pin Variante) inklusive des Terminal-Breakout-Boards. | Extern |
| `esp32-30pin-breakoutboard-lid.stl` | Deckel für das ESP32-Gehäuse mit Snap-Fit-Mechanismus (Einrast-Verschluss). | Extern |

## 3. Hardware-Komponenten
Die CAD-Konstruktion ist maßlich exakt auf folgende Hardware ausgelegt:
* Mikrocontroller: ESP32 Development Board (30 Pins, z.B. Freenove oder NodeMCU)
* Erweiterung: Terminal-Breakout-Board für 30-Pin ESP32 (Schraubklemmen)
* Sensoren: 2x DS18B20 (TO-92 Bauform oder vorkonfektioniert)
* Speicher: 1x MicroSD-Karten-Modul (Standard-SPI-Modul)
* Ortung: 1x GPS-Modul (BN-220, Maße: 22x20x6 mm)

## 4. Druckparameter und Material
Aufgrund der thermischen Belastung im RC-Fahrzeug (Nähe zu Motor und ESC) sowie der mechanischen Vibrationen gelten folgende Vorgaben für die additive Fertigung:

* **Material:** PETG, ASA oder ABS (PLA ist wegen der niedrigen Glasübergangstemperatur von ca. 60°C nicht zulässig).
* **Schichthöhe (Layer Height):** 0.20 mm für ein optimales Verhältnis aus Stabilität und Druckzeit.
* **Fülldichte (Infill):** Mindestens 30% (Gyroid oder Cubic Pattern), um strukturelle Integrität bei Stößen zu gewährleisten.
* **Wandlinien (Perimeters):** 3 bis 4 Linien zur Erhöhung der Biegesteifigkeit.
* **Toleranzen:** Das Modell beinhaltet ein Spaltmaß von 0.2 mm für den Snap-Fit-Deckel. Bei Überextrusion muss der Fluss (Flow Rate) im Slicer kalibriert werden.

## 5. Montagehinweise
* Die Platinen (GPS, SD-Modul) werden mit M2- oder M2.5-Schrauben auf der Trägerplatte `sensor_board_.stl` fixiert. Bei Bedarf sind Heiß-Einpressmuttern (Threaded Inserts) zu verwenden.
* Die Antenne des BN-220 GPS-Moduls (keramische Oberseite) muss zwingend nach oben zeigen und darf nicht durch Carbon- oder Metallbauteile des Chassis verdeckt werden.
* Kabeldurchführungen am Gehäuse müssen nach Abschluss der Verkabelung zur Zugentlastung mit einem Tropfen Schmelzklebstoff gesichert werden.

## 6. Quellen
* Modell: [ESP32 30-pin breakout board case + snap fit lid](https://www.printables.com/model/856471-esp32-30-pin-breakout-board-case-snap-fit-lid/files)
* Ersteller: [@Goofee_2018635 auf Printables](https://www.printables.com/@Goofee_2018635)
