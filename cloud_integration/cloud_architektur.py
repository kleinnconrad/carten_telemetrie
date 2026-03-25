import graphviz

def erstelle_cloud_architektur():
    dot = graphviz.Digraph('Azure_Serverless_Architecture', filename='Azure_Cloud_Pipeline', format='png')
    
    # Diagramm-Styling: LR (Left to Right) ist der Standard für Data-Pipelines
    dot.attr(rankdir='LR', splines='spline', nodesep='0.6', ranksep='1.2')
    dot.attr('node', shape='box', style='filled, rounded', fontname='Helvetica', fontsize='12', margin='0.2')

    # --- DIE KNOTEN (Nodes) ---
    
    # 1. Edge (Das Auto)
    dot.node('Edge', label='🚗 RC Carten T410R\nESP32 + SIM7000G LTE', fillcolor='#e1e1e1', fontcolor='black')
    
    # 2. Ingestion (Azure IoT Hub) - Azure Blau
    dot.node('IoTHub', label='☁️ Azure IoT Hub\n(Free Tier F1)\nMQTT Broker / Ingestion', fillcolor='#0078D4', fontcolor='white')
    
    # 3. Processing (Azure Function) - Azure Blau
    dot.node('Function', label='⚡ Azure Function\n(Consumption Plan)\nEvent-Driven Processing', fillcolor='#0078D4', fontcolor='white')
    
    # 4. Storage (Cosmos DB) - Cosmos Grün
    dot.node('CosmosDB', label='🗄️ Azure Cosmos DB\n(Serverless NoSQL)\nLangzeitspeicher (JSON)', fillcolor='#5CDA99', fontcolor='black')
    
    # 5. Dashboard (Power BI / Web) - Power BI Gelb
    dot.node('Dashboard', label='📊 Live Dashboard\n(Power BI / SignalR)\nEchtzeit-Telemetrie', fillcolor='#F2C811', fontcolor='black')

    # --- DER DATENFLUSS (Edges) ---
    
    # Auto funkt an IoT Hub
    dot.edge('Edge', 'IoTHub', label=' LTE / MQTT\n(2 Hz JSON Stream)', color='black', penwidth='2')
    
    # IoT Hub triggert Function
    dot.edge('IoTHub', 'Function', label=' Event Trigger', color='#0078D4', penwidth='2')
    
    # Function speichert in DB
    dot.edge('Function', 'CosmosDB', label=' Save Document\n(Cosmos DB SDK)', color='#5CDA99', penwidth='2')
    
    # Function pusht an Dashboard (Gleichermaßen aus der Function heraus)
    dot.edge('Function', 'Dashboard', label=' Live Push\n(REST / WebSockets)', color='#F2C811', penwidth='2')

    # Bild rendern
    dot.render(view=False)
    print("Cloud-Architektur-Diagramm generiert! Bitte öffne 'Azure_Cloud_Pipeline.png'.")

if __name__ == '__main__':
    erstelle_cloud_architektur()
