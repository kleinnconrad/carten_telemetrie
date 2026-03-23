import graphviz

def erstelle_schaltplan():
    # Erstelle einen gerichteten Graphen mit detaillierten Knoten (Records)
    dot = graphviz.Digraph(comment='RC Telemetrie Schaltplan')
    dot.attr(rankdir='LR', splines='polyline')
    dot.attr('node', shape='record', style='filled', fontname='Helvetica', fontsize='10')

    # Komponenten als Pin-genaue Records definieren
    dot.node('ESP', '{ ESP32 (NodeMCU) | { <vin> VIN (5V) | <gnd> GND | <3v3> 3.3V | <gpio23> GPIO 23 | <gpio19> GPIO 19 | <gpio18> GPIO 18 | <gpio5> GPIO 5 | <gpio4> GPIO 4 | <gpio2> GPIO 2 } }', fillcolor='lightblue')
    
    dot.node('RC', '{ RC-Empfänger | { <vcc> VCC (5V/6V) | <gnd> GND } }', fillcolor='lightgreen')
    
    dot.node('SD', '{ MicroSD-Modul (SPI) | { <vcc> VCC (3.3V) | <gnd> GND | <mosi> MOSI | <miso> MISO | <sck> SCK | <cs> CS } }', fillcolor='lightgrey')
    
    dot.node('T_MOT', '{ DS18B20 (Motor) | { <vdd> VDD (Rot) | <gnd> GND (Schwarz) | <dq> DQ (Daten) } }', fillcolor='lightyellow')
    dot.node('T_ESC', '{ DS18B20 (ESC) | { <vdd> VDD (Rot) | <gnd> GND (Schwarz) | <dq> DQ (Daten) } }', fillcolor='lightyellow')
    
    dot.node('HALL', '{ A3144 Hall-Sensor | { <vcc> VCC (1) | <gnd> GND (2) | <do> DO (3) } }', fillcolor='lightcoral')
    
    dot.node('R', '4.7 kΩ\nPull-Up Widerstand', fillcolor='white', shape='box')

    # Stromversorgung (Rot/Schwarz)
    dot.edge('RC:vcc', 'ESP:vin', color='red', label=' BEC Power')
    dot.edge('RC:gnd', 'ESP:gnd', color='black')

    # SD Card (SPI-Bus)
    dot.edge('ESP:3v3', 'SD:vcc', color='red')
    dot.edge('ESP:gnd', 'SD:gnd', color='black')
    dot.edge('ESP:gpio23', 'SD:mosi', color='blue', label=' SPI MOSI')
    dot.edge('ESP:gpio19', 'SD:miso', color='blue', label=' SPI MISO')
    dot.edge('ESP:gpio18', 'SD:sck', color='blue', label=' SPI CLK')
    dot.edge('ESP:gpio5', 'SD:cs', color='blue', label=' SPI CS')

    # Sensoren Power
    dot.edge('ESP:3v3', 'T_MOT:vdd', color='red')
    dot.edge('ESP:gnd', 'T_MOT:gnd', color='black')
    dot.edge('ESP:3v3', 'T_ESC:vdd', color='red')
    dot.edge('ESP:gnd', 'T_ESC:gnd', color='black')
    dot.edge('ESP:3v3', 'HALL:vcc', color='red')
    dot.edge('ESP:gnd', 'HALL:gnd', color='black')

    # Datenleitungen (Protokolle)
    dot.edge('ESP:gpio4', 'T_MOT:dq', color='orange', label=' 1-Wire Bus')
    dot.edge('ESP:gpio4', 'T_ESC:dq', color='orange', label=' 1-Wire Bus')
    dot.edge('ESP:gpio2', 'HALL:do', color='purple', label=' Hardware Interrupt')

    # Pull-Up Widerstand (1-Wire Spezifikation)
    dot.edge('ESP:3v3', 'R', color='red', style='dashed')
    dot.edge('R', 'T_MOT:dq', color='orange', style='dashed', label=' Pull-Up')

    # Rendern
    dot.render('RC_Telemetrie_Schaltplan_Pro', format='png', view=False)
    print("Professioneller Schaltplan generiert.")

if __name__ == '__main__':
    erstelle_schaltplan()
