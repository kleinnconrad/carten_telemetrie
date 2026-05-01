# ESP32 Sensor-Station & Gehäuselösung

Dieser Ordner enthält die 3D-Druck-Dateien (STL) für eine ESP32-basierte Sensor-Station. Das Projekt kombiniert ein Gehäuse für den Mikrocontroller mit einem eigens entwickelten Trägerboard für verschiedene Sensor- und Speichermodule.

## Enthaltene 3D-Modelle

| Dateiname | Beschreibung | Herkunft |
| :--- | :--- | :--- |
| `sensor_board.stl` | Maßgeschneiderte Trägerplatte zur sicheren Montage der Peripherie. Bietet dedizierten Platz für 2x Temperatur-Sensoren, 1x Micro-SD-Modul und 1x GPS-Modul. | Eigenentwicklung |
| `esp32-30pin-breakoutboard-case.stl` | Hauptgehäuse, passend für ein ESP32 Development Board (30 Pins) in Kombination mit einem Terminal-Breakout-Board. | Extern (Printables) |
| `esp32-30pin-breakoutboard-lid.stl` | Passgenauer Deckel (Snap-Fit) für das ESP32-Gehäuse. | Extern (Printables) |

## Unterstützte Hardware

Die Konstruktion ist für die Unterbringung der folgenden Hardware-Komponenten ausgelegt:

* **Mikrocontroller:** ESP32 Development Board (30-Pin Variante)
* **Erweiterung:** Terminal-Breakout-Board für den ESP32
* **Sensoren:** 2x Temperatur-Sensoren
* **Speicher:** 1x Micro-SD-Karten-Modul (zur Datenaufzeichnung/Logging)
* **Ortung:** 1x GPS-Modul

## 🔗 Quellen

Während das `sensor_board.stl` eine Eigenentwicklung für dieses spezifische Projekt ist, stammen die Gehäuseteile für den ESP32 (Case und Lid) aus der 3D-Druck-Community. 

Ein großer Dank geht an den ursprünglichen Designer des ESP32-Gehäuses:
* **Modell:** [ESP32 30-pin breakout board case + snap fit lid](https://www.printables.com/model/856471-esp32-30-pin-breakout-board-case-snap-fit-lid/files)
* **Ersteller:** [@Goofee_2018635 auf Printables](https://www.printables.com/@Goofee_2018635)
