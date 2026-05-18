### Testprotokoll #02: In-Vehicle Integration & Statischer Test

**Beschreibung:**
Ein erster Systemtest der Telemetrie-Einheit wurde direkt im Fahrzeug durchgeführt. Die Stromversorgung des ESP32-Setups erfolgte dabei erfolgreich über den BEC-Port des RC-Empfängers (5V). Das Fahrzeug wurde für den Testzeitraum von ca. 3 Minuten stationär an einem Fenster platziert, um den GPS-Empfang zu ermöglichen, ohne das Chassis zu bewegen.

**Testergebnisse:**
- **Stromversorgung:** Die Versorgung über das BEC des Empfängers ist stabil, es traten keine Spannungsabfälle beim Initialisieren der SD-Karte auf.
- **Datenaufzeichnung:** Das Batch-Logging auf die MicroSD-Karte lief über die vollen 3 Minuten ohne Fehler oder Abbrüche durch.
- **Sensordaten (Plausibilität):** Die aufgezeichneten Temperatur- sowie die GPS-Daten (aus der Datei `log.csv`) wurden gesichtet und als korrekt und plausibel bewertet.

**Status:** Erfolgreich abgeschlossen.

<img src="https://github.com/kleinnconrad/carten_telemetrie/blob/main/testrun/test_im_fahrzeug/PXL_20260518_144521252.jpg?raw=true" width="50%" alt="Test im Fahrzeug - Setup 1">
<img src="https://github.com/kleinnconrad/carten_telemetrie/blob/main/testrun/test_im_fahrzeug/PXL_20260518_144728325.jpg?raw=true" width="50%" alt="Test im Fahrzeug - Setup 2">
