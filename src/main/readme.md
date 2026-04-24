# Firmware: RC Telemetrie (Cloud & Offline)

Diese Firmware verwandelt den ESP32 in einen autarken IoT-Edge-Client für RC-Fahrzeuge. Das Repository enthält zwei maßgeschneiderte Software-Varianten (`main_cloud` und `main_offline`), um hochfrequente Sensordaten (GPS, Doppler-Geschwindigkeit, Drehzahlen, Temperaturen) optimal zu erfassen.

## Die zwei Firmware-Varianten

* **`main_cloud` (Live-Streaming):** Baut über ein LTE-Modem (SIM7000) eine Verbindung zum Mobilfunknetz auf und streamt die Telemetriedaten in Echtzeit über das MQTT-Protokoll an eine Cloud-Infrastruktur. Zusätzlich werden die Daten als Fallback auf der SD-Karte gesichert (Dual-Storage).
* **`main_offline` (Batch-Logging):** Eine extrem schlanke, ressourcen- und gewichtsoptimierte Variante komplett ohne Mobilfunk-Stack. Sie speichert die JSON-Payloads blitzschnell im 2-Hz-Takt ausschließlich lokal auf der MicroSD-Karte. Perfekt für High-Speed-Runs, bei denen auf Zusatzakkus und Modems verzichtet wird.

## Kern-Features (Beide Varianten)

* **Non-Blocking Architecture:** Die Firmware ist extrem asynchron aufgebaut. Das Parsen von GPS-NMEA-Daten und das Warten auf Temperaturwandlungen (1-Wire) blockieren niemals den Main-Loop.
* **Hardware-Zähler (PCNT):** Die Pulse des Hall-Sensors werden nicht über fehleranfällige Software-Interrupts, sondern über den dedizierten PCNT-Hardware-Zähler des ESP32 verlustfrei im Hintergrund erfasst.
* **Anti-Jitter Mathematik:** Präzise `timeDelta`-Berechnungen garantieren exakte RPM-Werte, unabhängig von winzigen Latenzen durch SD-Schreibvorgänge oder Mobilfunk-Schwankungen.
* **Hardware UART Routing:** Das System nutzt die dedizierten Hardware-Serial-Schnittstellen des ESP32, um parallel mit dem GPS-Modul (`UART 2`) und – in der Cloud-Variante – mit dem LTE-Modem (`UART 1`) zu kommunizieren.

## Bibliotheken

Um den Code zu kompilieren (z. B. via PlatformIO oder Arduino IDE), müssen je nach Variante folgende externe Bibliotheken installiert sein:

**Basis-Bibliotheken (Für Cloud & Offline):**
* **`TinyGPSPlus`** (von Mikal Hart): Zum asynchronen Parsen der NMEA-Sätze des BN-220 GPS-Moduls.
* **`OneWire`** & **`DallasTemperature`**: Für den parallelen Auslese-Bus der Motor- und ESC-Sensoren.

**Zusätzliche Bibliotheken (Nur für `main_cloud`):**
* **`TinyGSM`** (von Volodymyr Shymanskyy): Für die AT-Kommunikation mit dem LTE-Modem.
* **`PubSubClient`** (von Nick O'Leary): Der schlanke Standard-Client für die MQTT-Cloud-Verbindung.

## Konfiguration (Nur Cloud-Variante!)

Während die `main_offline`-Variante absolutes "Plug & Play" ist, musst du vor dem Flashen der **Cloud-Firmware** deine netzwerk- und cloudspezifischen Daten im oberen Bereich der Datei eintragen:

```cpp
// 1. Mobilfunk-Provider (APN) - z.B. für 1NCE IoT Karten oft "iot.1nce.net"
const char apn[]      = "internet"; 
const char gprsUser[] = "";
const char gprsPass[] = "";

// 2. Cloud-Backend (MQTT Broker)
const char* mqttServer = "dein-mqtt-broker.com"; // IP oder URL deiner Cloud
const int   mqttPort   = 1883;                   // Standard-Port (1883 unverschlüsselt, 8883 TLS)
const char* mqttTopic  = "rc-car/telemetry/live";