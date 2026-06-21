# Einkaufsliste

## Inhaltsverzeichnis
* [1. Variante A (Cloud / LTE)](#1-variante-a-cloud--lte)
* [2. Variante B (Offline / Lokales Logging)](#2-variante-b-offline--lokales-logging)

## 1. Variante A (Cloud / LTE)
Bauteile für das Setup mit Spannungsversorgung.

| Komponente | Typ | Anz. | Zweck |
| :--- | :--- | :--- | :--- |
| Microcontroller | Joy-IT ESP32 NodeMCU (38-Pin) | 1 | Zentraleinheit |
| Terminal Board | Joy-IT ESP32 Expansion Board (38-Pin) | 1 | Anschlüsse |
| LTE-Modem | Waveshare SIM7000G / SIM7600G | 1 | Cloud-Uplink |
| GPS-Modul | Joy-IT GPS Modul (u-blox) | 1 | Positionsdaten und Geschwindigkeitsdaten |
| Speichermodul | Joy-IT Micro-SD Card Reader Modul | 1 | Datenlogger |
| Temperatursensor | Joy-IT DS18B20 | 2 | Temperaturmessung Motor und Regler |
| Drehzahlsensor | Joy-IT Hall-Sensor Modul (KY-003) | 1 | Impulsgeber |
| Magnet | Neodym-Magnet (3x2mm) | 1 | Impulsgeber |
| Widerstand | 4,7 kΩ (0,25W) | 1 | Pull-Up für Temperatur-Bus |
| Powerbank | Intenso xs5000 / Voltcraft Mini Powerbank | 1 | Spannungsquelle |
| USB-Versorgung | USB-A Ladekabel | 1 | Anschluss |
| Netz-Verteiler | WAGO 221-415 (5-Leiter-Klemme) | 3 | Verteilung für 5V, GND und 3.3V |
| Verbindung | Jumper-Kabel (M/M, F/F) | 1 Set | Kabelbrücken |
| Werkzeug | Abisolierzange | 1 | Kabelbearbeitung |

## 2. Variante B (Offline / Lokales Logging)
Bauteile für das Setup ohne LTE-Modem. Spannungsversorgung über RC-Empfänger.

| Komponente | Typ | Anz. | Zweck |
| :--- | :--- | :--- | :--- |
| Microcontroller | Joy-IT ESP32 NodeMCU (38-Pin) | 1 | Zentraleinheit |
| Terminal Board | Joy-IT ESP32 Expansion Board (38-Pin) | 1 | Anschlüsse |
| GPS-Modul | Joy-IT GPS Modul (u-blox) | 1 | Positionsdaten und Geschwindigkeitsdaten |
| Speichermodul | Joy-IT Micro-SD Card Reader Modul | 1 | Datenlogger |
| Temperatursensor | Joy-IT DS18B20 | 2 | Temperaturmessung Motor und Regler |
| Drehzahlsensor | Joy-IT Hall-Sensor Modul (KY-003) | 1 | Impulsgeber |
| Magnet | Neodym-Magnet (3x2mm) | 1 | Impulsgeber |
| Widerstand | 4,7 kΩ (0,25W) | 1 | Pull-Up für Temperatur-Bus |
| Empfänger-Strom | Servo-Verlängerungskabel (JR-Stecker) | 1 | Anschluss vom RC-Empfänger |
| Netz-Verteiler | WAGO 221-415 (5-Leiter-Klemme) | 2 | Verteilung für GND und 3.3V |
| Verbindung | Jumper-Kabel (M/M, F/F) | 1 Set | Kabelbrücken |
| Werkzeug | Abisolierzange | 1 | Kabelbearbeitung |