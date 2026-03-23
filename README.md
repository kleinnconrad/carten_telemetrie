# carten_telemetrie
Entwicklung einer Telemetrie Lösung für einen Carten T410R [![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/kleinnconrad/RC100), um die Temperatur von Motor und ESC zu messen. Ebenfalls soll die Drehzahl der Kardanwelle gemessen werden.

# Bauanleitung: DIY RC-Telemetrie-System (ESP32)

Dieses Dokument beschreibt den Aufbau eines Edge-Sensor-Nodes zur Erfassung von Telemetriedaten (Motor-Temperatur, ESC-Temperatur und Drehzahl) in einem RC-Fahrzeug. Die Daten werden lokal auf einer MicroSD-Karte gespeichert und per WLAN-Access-Point bereitgestellt.

---

## 1. Stückliste (Bill of Materials)

| Komponente | Spezifikation / Typ | Anzahl | Bemerkung |
| :--- | :--- | :--- | :--- |
| **Microcontroller** | ESP32 Development Board (z.B. NodeMCU 32S) | 1 | Zentraleinheit für Ingestion & Webserver |
| **Speichermodul** | MicroSD-Karten-Modul (SPI) | 1 | 3.3V-kompatibel |
| **Speicherkarte** | MicroSD-Karte (FAT32 formatiert) | 1 | 8 GB oder 16 GB ausreichend |
| **Temperatursensor** | DS18B20 (Wasserdicht) | 2 | Digitale 1-Wire Sensoren für Motor & ESC |
| **Drehzahlsensor** | Hall-Sensor Modul (z.B. A3144) | 1 | Erfasst das Magnetfeld für RPM-Berechnung |
| **Magnet** | Neodym-Magnet (klein, z.B. 3x2mm) | 1 | Wird auf rotierende Welle geklebt |
| **Widerstand** | 4,7 kΩ (Kilo-Ohm) | 1 | Pull-up-Widerstand für den 1-Wire Bus |
| **Kabel & Stecker** | Jumper-Kabel (Dupont), Servostecker | Div. | Verbindungskomponenten |
| **Befestigung** | Wärmeleitkleber, Kabelbinder, Tape | Div. | Mechanische Montage im Chassis |

---

## 2. Schaltplan & Pin-Belegung

Alle Komponenten teilen sich eine gemeinsame Masse (**GND**).

### Stromversorgung (vom RC-Empfänger)
* **VCC (Rot):** Vom Empfänger (5V/6V BEC) an den **VIN** (oder 5V) Pin des ESP32.
* **GND (Schwarz/Braun):** Vom Empfänger an einen **GND** Pin des ESP32.

### MicroSD-Karten-Modul (SPI-Bus)
* **VCC:** an **3.3V** des ESP32
* **GND:** an **GND** des ESP32
* **MOSI:** an **GPIO 23**
* **MISO:** an **GPIO 19**
* **SCK / CLK:** an **GPIO 18**
* **CS / SS:** an **GPIO 5**

### Temperatursensoren (DS18B20)
*Beide Sensoren werden parallel angeschlossen.*
* **VCC (Rot):** an **3.3V** des ESP32
* **GND (Schwarz):** an **GND** des ESP32
* **Data (Gelb/Blau):** an **GPIO 4** des ESP32
* **WICHTIG:** Ein **4,7 kΩ Widerstand** muss als Brücke zwischen den 3.3V-Pin und den Data-Pin (GPIO 4) geschaltet werden.

### Hall-Sensor (RPM)
* **VCC:** an **3.3V** des ESP32
* **GND:** an **GND** des ESP32
* **Signal / DO:** an **GPIO 2** des ESP32

---

## 3. Schritt-für-Schritt Aufbau

### Phase 1: Vorbereitung & Software
1. **Speicher vorbereiten:** Formatiere die MicroSD-Karte am PC im **FAT32** Format und lege sie in das Modul ein.
2. **Bibliotheken installieren:** Öffne die Arduino IDE und installiere die Bibliotheken `OneWire` (Paul Stoffregen) und `DallasTemperature` (Miles Burton).
3. **Flashen:** Verbinde den ESP32 per USB, lade den C++ Code hoch und prüfe im Seriellen Monitor (Baudrate 115200), ob die SD-Karte erfolgreich initialisiert wird.

### Phase 2: Löten & Verkabeln
4. **Stromversorgung konfektionieren:** Löte oder crimpe ein Kabel mit einem Servostecker, das in einen freien Kanal des RC-Empfängers passt. Führe Plus an `VIN` und Minus an `GND` des ESP32.
5. **Bus-Systeme verbinden:** Verlöte das SD-Modul, den Hall-Sensor und die Temperatursensoren gemäß dem obigen Pin-Mapping.
6. **Pull-up integrieren:** Löte den 4,7 kΩ Widerstand zwischen die 3.3V-Leitung und die Datenleitung der Temperatursensoren.
7. **Isolieren:** Sichere alle offenen Lötstellen mit Schrumpfschlauch oder Heißkleber gegen Kurzschlüsse durch Vibrationen oder Feuchtigkeit.

### Phase 3: Mechanische Integration
8. **Zentraleinheit platzieren:** Befestige den ESP32 und das SD-Modul geschützt im Chassis (z. B. in der Empfängerbox oder mit Klettband auf dem Top-Deck).
9. **Magnet montieren:** Klebe den Neodym-Magneten mit Sekundenkleber/Epoxy auf das Hauptzahnrad (Spur Gear) oder die Antriebswelle. (Tipp: Gegenüberliegend einen Tropfen Kleber als Gegengewicht gegen Unwucht anbringen).
10. **Hall-Sensor ausrichten:** Montiere den Sensor starr so, dass der Magnet bei jeder Umdrehung in ca. 1-2 mm Abstand daran vorbeifliegt.
11. **Sensoren anbringen:** * *ESC:* Einen Sensor mit wärmeleitendem Kleber zwischen die Kühlrippen des Fahrtenreglers klemmen.
    * *Motor:* Den zweiten Sensor an die Außenhülle des Brushless-Motors anlegen und mit hitzebeständigem Kaptonband oder einem Kabelbinder fixieren.

---

## 4. Betrieb & Datenabruf
1. Schalte das RC-Auto ein. Der ESP32 startet automatisch die Datenaufzeichnung auf die SD-Karte und spannt das WLAN `RC-Telemetry` auf.
2. Verbinde dich nach der Fahrt mit dem Smartphone in dieses WLAN (Passwort: `password123`).
3. Öffne im Browser die IP `http://192.168.4.1` und lade die CSV-Datei herunter.
