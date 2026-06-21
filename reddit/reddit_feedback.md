# Reddit Feedback: Telemetrie-System (RSS Sync)

## Inhaltsverzeichnis
* [1. Letzter Synchronisationszeitpunkt](#1-letzter-synchronisationszeitpunkt)
* [2. Kommentare](#2-kommentare)

## 1. Letzter Synchronisationszeitpunkt
03.04.2026 20:24:24

## 2. Kommentare

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/):
> Hallo r/esp32! Ich konstruiere derzeit ein RC-Fahrzeug (Carten T410R) im Maßstab 1:10 mit dem Ziel, Geschwindigkeiten von 100 km/h zu erreichen. Link: https://github.com/kleinnconrad/RC100.
> 
> Beruflich entwickle ich Datenanalyse-Plattformen. Daher ist die Erfassung von Live-Daten aus dem Fahrzeug ein Teil dieses Projekts. Ich besitze Erfahrung mit Datenplattformen, bin jedoch Anfänger im Bereich der eingebetteten Programmierung. Dies ist mein erstes Hardware/C++ Projekt.
> 
> Geplant ist der Einsatz eines ESP32 als IoT-Telemetriegerät im Fahrzeug. Ziel ist die Erfassung von Live-Daten während der Fahrten und deren Übertragung, um thermische Bedingungen und Leistungsgrenzen zu analysieren.
> 
> Da das ESP32-Ökosystem neu für mich ist, gehe ich von Fehlern in meinem ersten Entwurf aus.
> 
> Das Projekt ist auf GitHub veröffentlicht. Ich bitte um Überprüfung, Ratschläge oder Hinweise von erfahrenen Entwicklern.
> 
> Repository: https://github.com/kleinnconrad/carten_telemetrie
> 
> Die Dokumentation ist in deutscher Sprache verfasst.
> 
> Tipps zur Verarbeitung von Live-Datenströmen an einem bewegten Objekt bei 100 km/h sind willkommen.

**u/Plastic_Fig9225** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odnq4e3/):
> Der Code sollte in mehrere Tasks aufgeteilt werden, um Jitter bei der Datenerfassung zu vermeiden. MQTT kann unvorhersehbare Verzögerungen verursachen.
> Für die Drehzahlmessung empfiehlt sich die Nutzung des PCNT (Arduino) des ESP.
> Die Berechnung `int rpm = pulses * (60000 / ingestionInterval);` sollte zu `pulses * (60000 / (millis() - lastIngestionTime))` geändert werden, um zeitlichen Jitter zu berücksichtigen. Der Zeitstempel sollte so nah wie möglich am Auslesen der `pulses` genommen werden.
> Ein Timer kann genutzt werden, um die Datenerfassung in festen Intervallen durchzuführen, unabhängig vom Timing anderer Operationen.

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odobii2/):
> Danke für den Hinweis zur Berechnungslogik und zum Impulszähler. Der Code wurde entsprechend aktualisiert.

**u/Plastic_Fig9225** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odptjd2/):
> Beim PCNT ist zu beachten, dass der Zähler automatisch auf null zurückgesetzt wird, wenn er den oberen oder unteren Grenzwert überschreitet. Um keine Impulse zu verlieren, kann folgende Logik angewendet werden:
> [Codebeispiel zur Behandlung des PCNT-Überlaufs]

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odqkzd8/):
> Danke. Ich habe dies mit einem LLM diskutiert. Der Vorschlag wurde übernommen.

**u/Plastic_Fig9225** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/ods93c3/):
> Die Telemetriedaten enthalten keine Geschwindigkeit. Das GPS liefert eine genaue Geschwindigkeit über Grund, die präziser ist als eine Ableitung aus Positionsdaten. Dies sollte integriert werden.

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odtzz1m/):
> Danke für den Hinweis. Gemäß der Commit-Historie wurde dies nie implementiert.

**u/portugese_fruit** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoepnc/):
> Das System sieht gut aus.

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoftb5/):
> Zustimmung.

**u/portugese_fruit** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odov0on/):
> An welchen Orten wird das Fahrzeug bewegt? Sind 100 km/h auf der Straße möglich?

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odovbdp/):
> Parkplätze von großen Supermärkten außerhalb der Öffnungszeiten eignen sich dafür.

**u/jappiedoedelzak** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odohi8x/):
> Ein Blick auf ExpressRLS (https://www.expresslrs.org/) wird empfohlen. Es ist ein Open-Source-RC-System, das Telemetrie unterstützt.

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odohx37/):
> Danke. Das System wird geprüft.

**u/G-EDM** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odo9ijv/):
> Welche Fragen bestehen bezüglich Datenübertragung und Datenerfassung? PCNT eignet sich für die Impulszählung, I2S ADC für analoge Datenerfassung. Für die Übertragung sollten DMA-Puffer genutzt werden. Daten sollten komprimiert werden, z. B. durch Packen von vier 8-Bit-Werten in einen 32-Bit-Integer.

**u/Basic-You7791** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoesab/):
> Es ist geplant, Daten (GPS, Temperatur, Hall-Sensor) mit einer Abtastrate von 2 Hz zu erfassen und über LTE via MQTT in eine Cloud zu streamen. JSON-Payloads werden verwendet. I2S, DMA-Puffer und Bit-Packing sind für eine Rate von 2 Hz derzeit nicht erforderlich. Das Bit-Packing wird für mögliche Erweiterungen mit analogen Hochfrequenzsensoren vorgemerkt.

**u/G-EDM** [schrieb](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoofo8/):
> Für 2 Hz sind diese Methoden nicht zwingend erforderlich.
