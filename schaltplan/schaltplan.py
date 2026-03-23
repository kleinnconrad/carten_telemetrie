import graphviz

def erstelle_schaltplan():
    # Erstelle einen gerichteten Graphen
    dot = graphviz.Digraph(comment='RC Telemetrie Schaltplan')
    dot.attr(rankdir='LR', splines='ortho')
    dot.attr('node', shape='box', style='filled', fontname='Helvetica')

    # Definiere die Hauptkomponenten (Nodes)
    dot.node('ESP', 'ESP32\n(Zentraleinheit)', fillcolor='lightblue')
    dot.node('RC', 'RC-Empfänger\n(Stromquelle 5V/6V)', fillcolor='lightgreen')
    dot.node('SD', 'MicroSD-Modul\n(SPI-Bus)', fillcolor='lightgrey')
    dot.node('T_MOT', 'Temp Motor\n(DS18B20)', fillcolor='lightyellow', shape='ellipse')
    dot.node('T_ESC', 'Temp ESC\n(DS18B20)', fillcolor='lightyellow', shape='ellipse')
    dot.node('HALL', 'Hall-Sensor\n(A3144)', fillcolor='lightcoral', shape='ellipse')
    dot.node('R', '4.7 kΩ\nWiderstand', fillcolor='white', shape='plaintext')

    # Stromversorgung (Rot/Schwarz)
    dot.edge('RC', 'ESP', label=' VCC (+5V) -> VIN\n GND (-) -> GND', color='red', fontcolor='red')
    
    # Verbindungen zum SD-Modul
    dot.edge('ESP', 'SD', label=' 3.3V -> VCC\n GND -> GND\n GPIO 23 -> MOSI\n GPIO 19 -> MISO\n GPIO 18 -> SCK\n GPIO 5 -> CS', color='blue', fontcolor='blue')

    # Verbindungen zu den Sensoren
    dot.edge('ESP', 'HALL', label=' 3.3V -> VCC\n GND -> GND\n GPIO 2 -> Signal', color='purple', fontcolor='purple')
    
    # 1-Wire Bus für Temperaturen
    dot.edge('ESP', 'T_MOT', label=' 3.3V -> VCC\n GND -> GND\n GPIO 4 -> Data', color='orange', fontcolor='orange')
    dot.edge('ESP', 'T_ESC', label=' (Parallel zu Motor)', color='orange', fontcolor='orange')
    
    # Pull-Up Widerstand visualisieren
    dot.edge('ESP', 'R', label='3.3V', arrowhead='none', style='dashed')
    dot.edge('R', 'T_MOT', label='Zieht "Data" auf High', arrowhead='none', style='dashed')

    # Rendern und speichern
    dot.render('RC_Telemetrie_Schaltplan', format='png', view=False)
    print("Schaltplan wurde als 'RC_Telemetrie_Schaltplan.png' erfolgreich generiert und geöffnet.")

if __name__ == '__main__':
    erstelle_schaltplan()
