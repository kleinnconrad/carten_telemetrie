### Testprotokoll #01: Hardware-Integration & SD-Logging

**Beschreibung:**
Beide Temperatursensoren (Motor/ESC), das GPS-Modul sowie das MicroSD-Modul wurden erfolgreich an den ESP32 angeschlossen. Der Hardware-Aufbau wurde auf dem Breakout-Board validiert. Auf die Integration des Hall-Sensors wird in dieser Phase aus Platzgründen innerhalb des Fahrzeug-Chassis vorerst verzichtet.

**Testergebnis:**
- **Initialisierung:** Erfolgreich ("SD OK" via Serial Monitor bestätigt).
- **Datenintegrität:** Die Datei `log.csv` wurde korrekt angelegt.
- **Plausibilität:** Die aufgezeichneten Temperatur- und GPS-Werte entsprechen den Erwartungen und sind konsistent.

**Status:** Erfogreich abgeschlossen.

<img src="[https://github.com/kleinnconrad/carten_telemetrie/blob/main/build/PXL_20260505_152613322.jpg?raw=true](https://github.com/kleinnconrad/carten_telemetrie/blob/main/build/PXL_20260505_152613322.jpg?raw=true)" width="50%" alt="Hardware Test Setup 1">
<img src="[https://github.com/kleinnconrad/carten_telemetrie/blob/main/build/PXL_20260505_152628893.jpg?raw=true](https://github.com/kleinnconrad/carten_telemetrie/blob/main/build/PXL_20260505_152628893.jpg?raw=true)" width="50%" alt="Hardware Test Setup 2">
