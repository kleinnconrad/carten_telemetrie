# Testprotokoll: In-Vehicle Integration

## Inhaltsverzeichnis
* [1. Beschreibung](#1-beschreibung)
* [2. Testergebnisse](#2-testergebnisse)
* [3. Status](#3-status)

## 1. Beschreibung
Ein Systemtest der Telemetrie-Einheit wurde im Fahrzeug durchgeführt. Die Stromversorgung des ESP32 erfolgte über den BEC-Port des RC-Empfängers (5V). Das Fahrzeug wurde stationär platziert, um GPS-Empfang zu ermöglichen. Die Testdauer betrug 3 Minuten.

## 2. Testergebnisse
* Stromversorgung: Die Versorgung über das BEC des Empfängers war stabil. Es traten keine Spannungsabfälle während der Initialisierung auf.
* Datenaufzeichnung: Das Batch-Logging auf die MicroSD-Karte verlief fehlerfrei.
* Sensordaten: Die aufgezeichneten Parameter (Temperatur, GPS) in der Datei `log.csv` wurden geprüft und sind plausibel.

## 3. Status
Der Test wurde erfolgreich abgeschlossen.

<img src="https://github.com/kleinnconrad/carten_telemetrie/blob/main/testrun/test_im_fahrzeug/PXL_20260518_144521252.jpg?raw=true" width="50%" alt="Test im Fahrzeug - Setup 1">
<img src="https://github.com/kleinnconrad/carten_telemetrie/blob/main/testrun/test_im_fahrzeug/PXL_20260518_144728325.jpg?raw=true" width="50%" alt="Test im Fahrzeug - Setup 2">
