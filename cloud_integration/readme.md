# Cloud-Architektur in Azure

## Inhaltsverzeichnis
* [1. Architektur](#1-architektur)
* [2. Datenfluss](#2-datenfluss)
  * [2.1 Ingestion Layer: Azure IoT Hub](#21-ingestion-layer-azure-iot-hub)
  * [2.2 Processing Layer: Azure Functions](#22-processing-layer-azure-functions)
  * [2.3 Storage Layer: Azure Cosmos DB](#23-storage-layer-azure-cosmos-db)
  * [2.4 Presentation Layer](#24-presentation-layer)

## 1. Architektur
Das Projekt nutzt einen Serverless-Ansatz in Microsoft Azure. Es entstehen im Leerlauf keine Compute-Kosten. Die Pipeline verarbeitet Telemetriedaten und stellt sie bereit.

![pipeline](https://github.com/kleinnconrad/carten_telemetrie/blob/main/cloud_integration/Azure_Cloud_Pipeline.png)

## 2. Datenfluss

### 2.1 Ingestion Layer: Azure IoT Hub
* Aufgabe: Authentifizierung des ESP32 und Empfang der JSON-Payloads.
* Kosten: Free Tier.

### 2.2 Processing Layer: Azure Functions
* Trigger: Event-getriebenes Computing. Die Azure Function wird bei Dateneingang ausgelöst.
* Aufgabe: JSON-Verarbeitung, Datenprüfung, Timestamp-Konvertierung und Routing.
* Kosten: Consumption Plan.

### 2.3 Storage Layer: Azure Cosmos DB
* Setup: Serverless-Modus.
* Aufgabe: Speicherung der Telemetrie-Pakete als JSON-Dokumente.
* Kosten: Abrechnung nach Request Units.

### 2.4 Presentation Layer
* Option A (Power BI): Push-Dataset empfängt Daten via REST-API.
* Option B (Azure SignalR + Static Web App): Datenübertragung via WebSockets an eine Web-App.
