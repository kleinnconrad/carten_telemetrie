# Firmware: RC Cloud Telemetry (ESP32)

Diese Firmware verwandelt den ESP32 in einen autarken IoT-Edge-Client für RC-Fahrzeuge. Anstatt Daten nur lokal zu speichern, baut das System über ein LTE-Modem eine Verbindung zum Mobilfunknetz auf und streamt hochfrequente Sensordaten (GPS, Drehzahlen, Temperaturen) in Echtzeit über das MQTT-Protokoll an eine Cloud-Infrastruktur.

## 🚀 Kern-Features

* **Non-Blocking Architecture:** Die Firmware ist extrem asynchron aufgebaut. Das Parsen von GPS-NMEA-Daten (UART) und das Warten auf Temperaturwandlungen (1-Wire) blockieren niemals den Main-Loop. Dadurch geht kein einziger RPM-Interrupt verloren.
* **Hardware UART Routing:** Das System nutzt die dedizierten Hardware-Serial-Schnittstellen des ESP32, um parallel mit dem LTE-Modem (`UART 1`) und dem GPS-Modul (`UART 2`) zu kommunizieren.
* **Dual-Storage (Cloud + Edge):** Primär werden die Daten als JSON-Payload via MQTT in die Cloud gepusht. Parallel läuft ein Fallback-Ringpuffer, der die Daten im CSV-Format auf die lokale MicroSD-Karte schreibt, falls das Mobilfunknetz bei hohen Geschwindigkeiten kurzzeitig abreißt.

## 📦 Bibliotheken (Abhängigkeiten)

Um diesen Code zu kompilieren (z. B. via PlatformIO oder Arduino IDE), müssen folgende externe Bibliotheken installiert sein:

1. **`TinyGSM`** (von Volodymyr Shymanskyy): Für die AT-Kommunikation mit dem SIM7000G LTE-Modem.
2. **`TinyGPSPlus`** (von Mikal Hart): Zum asynchronen Parsen der NMEA-Sätze des BN-220 GPS-Moduls.
3. **`PubSubClient`** (von Nick O'Leary): Der schlanke Standard-Client für die MQTT-Cloud-Verbindung.
4. **`OneWire`** & **`DallasTemperature`**: Für den parallelen Auslese-Bus der Motor- und ESC-Sensoren.

## ⚙️ Konfiguration (Vor dem Flashen!)

Bevor du die Firmware auf den ESP32 lädst, musst du im oberen Bereich der `main.cpp` deine netzwerk- und cloudspezifischen Daten eintragen:

```cpp
// 1. Mobilfunk-Provider (APN) - z.B. für 1NCE IoT Karten oft "iot.1nce.net"
const char apn[]      = "internet"; 
const char gprsUser[] = "";
const char gprsPass[] = "";

// 2. Cloud-Backend (MQTT Broker)
const char* mqttServer = "dein-mqtt-broker.com"; // IP oder URL deiner Cloud
const int   mqttPort   = 1883;                   // Standard-Port (1883 unverschlüsselt, 8883 TLS)
const char* mqttTopic  = "rc-car/telemetry/live";