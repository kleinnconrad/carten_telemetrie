# Cloud-Architektur: Serverless IoT Streaming (Azure)

Dieses Projekt nutzt einen zu 100 % Serverless-basierten Ansatz in der Microsoft Azure Cloud. Dadurch entstehen im Leerlauf (wenn das Auto nicht fährt) **keine laufenden Compute-Kosten**. Die Pipeline verarbeitet die JSON-Telemetriedaten in Echtzeit und stellt sie für Live-Dashboards bereit.

## Der Datenfluss (Pipeline)

### 1. Ingestion Layer: Azure IoT Hub (F1 Free Tier)
Das ist das physische Eingangstor für das RC-Car in die Azure-Cloud. Der IoT Hub agiert als verwalteter MQTT-Broker.
* **Aufgabe:** Sichere Authentifizierung des ESP32 und hochperformantes Entgegennehmen der JSON-Payloads (`ts`, `rpm`, `temp_mot`, `spd`, etc.).
* **Kosten:** 0,00 € (Das Free Tier erlaubt 8.000 Nachrichten pro Tag, ausreichend für RC-Speedruns).

### 2. Processing Layer: Azure Functions (Consumption Plan)
Anstatt einen teuren Databricks-Cluster 24/7 laufen zu lassen, nutzen wir Event-getriebenes Computing. Die Azure Function wacht nur auf, wenn Daten ankommen.
* **Trigger:** Gekoppelt über einen "IoT Hub Trigger". Sobald ein JSON-Paket vom Auto ankommt, feuert die Funktion in Millisekunden.
* **Aufgabe:** Entpacken des JSON, Plausibilitätsprüfung (z.B. GPS-Ausreißer filtern), Timestamp-Konvertierung und dynamisches Routing (Speicherung + Live-Push).
* **Kosten:** Die ersten 1 Million Ausführungen/Monat sind kostenlos (Praktisch 0,00 €).

### 3. Storage Layer: Azure Cosmos DB (Serverless Mode)
Eine NoSQL-Datenbank, die native JSON-Dokumente mit extrem niedriger Latenz wegschreibt und automatisch indiziert.
* **Setup:** Zwingend im **"Serverless"**-Modus anlegen, um stündliche Fixkosten zu vermeiden!
* **Aufgabe:** Langzeitspeicherung jedes validierten Telemetrie-Pakets als einzelnes Dokument für spätere Performance-Analysen.
* **Kosten:** Nur wenige Cent im Monat (Abrechnung erfolgt rein nach tatsächlichen Request Units (RUs) während der Fahrt).

### 4. Presentation Layer (Live-Dashboard)
Die Azure Function leitet den Datenstrom parallel zur Datenbank an ein Präsentations-Layer weiter:
* **Option A (Power BI):** Ein Push-Dataset empfängt die Daten via REST-API. Das Dashboard aktualisiert Tachos und Liniendiagramme ohne Browser-Refresh.
* **Option B (Azure SignalR + Static Web App):** Die Daten werden via WebSockets direkt in eine mobile Web-App gepusht (ideal für die Live-Ansicht auf dem Smartphone direkt an der Strecke).
