# Testprotokoll: In-Vehicle Integration

## Inhaltsverzeichnis
* [1. Testaufbau und Spezifikationen](#1-testaufbau-und-spezifikationen)
* [2. Prüfverfahren und Methodik](#2-prüfverfahren-und-methodik)
* [3. Testergebnisse und Validierung](#3-testergebnisse-und-validierung)
* [4. Visuelle Dokumentation](#4-visuelle-dokumentation)

## 1. Testaufbau und Spezifikationen
Der Integrationstest der Telemetrie-Einheit wurde im montierten Zustand im Fahrzeug-Chassis vollzogen.
* **Stromversorgung:** Die Energieversorgung des ESP32 erfolgte ausschließlich parasitär über den BEC-Port (Battery Eliminator Circuit) des RC-Empfängers bei einer nominalen Spannung von 5.0 V.
* **Datenspeicher:** Eine 16 GB SDHC-Karte (FAT32, Clustergröße 32 KB) wurde für das Logging verwendet.
* **Umgebung:** Das Fahrzeug wurde stationär unter freiem Himmel positioniert, um eine ungestörte Line-of-Sight für den Fix der Satelliten des GPS-Moduls zu garantieren.
* **Testdauer:** Der Testlauf dauerte exakt 180 Sekunden.

## 2. Prüfverfahren und Methodik
Der Test fokussierte sich auf die Verifikation von Systemstabilität und Datenintegrität unter realen mechanischen Integrationsbedingungen.
* Es wurde kontrolliert, ob der Einschaltstrom (Inrush Current) des ESP32 zu einem Reset oder einem Spannungsabfall ("Brownout") des Empfängers führt.
* Der Datendurchsatz auf dem SPI-Bus zum SD-Modul wurde im 2 Hz-Takt überwacht.
* Es wurde eine Störfestigkeitsprüfung bezüglich elektromagnetischer Interferenzen (EMI) zwischen dem Fahrtregler (ESC) und dem GPS-Modul durchgeführt.

## 3. Testergebnisse und Validierung
* **Stromversorgung:** Der Test war erfolgreich. Das BEC des Empfängers lieferte ausreichend Strom (Spitzen bis 250 mA) für den Bootvorgang. Brownout-Erkennungen des ESP32 blieben aus.
* **Datenaufzeichnung:** Das Logging auf die MicroSD-Karte verlief vollständig fehlerfrei. Es wurden keine verlorenen Schreibzyklen (Dropped Frames) verzeichnet.
* **Sensordaten:** Die in der Datei `log.csv` erfassten Parameter (Temperaturwerte in °C, GPS-Koordinaten) wurden einer Plausibilitätsprüfung unterzogen. Die Temperaturwerte lagen stabil im Umgebungsspektrum (ca. 22 °C), und der GPS-Fix erreichte eine akzeptable HDOP (Horizontal Dilution of Precision).
