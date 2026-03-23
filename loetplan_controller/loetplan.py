import graphviz

def erstelle_loetplan():
    # Setup des Graphen: 'ortho' sorgt für eckige, kabel-ähnliche Linien
    dot = graphviz.Digraph('Loetplan', filename='ESP32_Loetplan', format='png')
    dot.attr(rankdir='LR', splines='ortho', nodesep='1.0', ranksep='2.5')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 als detaillierte Tabelle (Die Zentrale)
    esp32_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="2" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V Input)</TD><TD PORT="g23">GPIO 23</TD></TR>
      <TR><TD PORT="3v3">3.3V (Output)</TD><TD PORT="g19">GPIO 19</TD></TR>
      <TR><TD PORT="gnd">GND (Masse)</TD><TD PORT="g18">GPIO 18</TD></TR>
      <TR><TD PORT="g4">GPIO 4</TD><TD PORT="g5">GPIO 5</TD></TR>
      <TR><TD PORT="g2">GPIO 2</TD><TD BGCOLOR="#f0f0f0"><I>Weitere Pins...</I></TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. MicroSD Modul
    sd_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#d3d3d3"><B>MicroSD (SPI)</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD><TD PORT="cs">CS</TD></TR>
      <TR><TD PORT="gnd">GND</TD><TD PORT="sck">SCK</TD></TR>
      <TR><TD PORT="miso">MISO</TD><TD PORT="mosi">MOSI</TD></TR>
    </TABLE>>'''
    dot.node('SD', label=sd_html)

    # 3. Temperatursensoren (DS18B20)
    temp_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="3" BGCOLOR="#ffffe0"><B>DS18B20 (Motor & ESC)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD><TD PORT="gnd">GND (Schwarz)</TD><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''
    dot.node('TEMP', label=temp_html)

    # 4. Hall Sensor (RPM)
    hall_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="3" BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B></TD></TR>
      <TR><TD PORT="vcc">VCC (Pin 1)</TD><TD PORT="gnd">GND (Pin 2)</TD><TD PORT="out">OUT (Pin 3)</TD></TR>
    </TABLE>>'''
    dot.node('HALL', label=hall_html)

    # 5. Hilfs-Bauteile
    dot.node('RC', shape='box', style='filled', fillcolor='#90ee90', label='RC-Empfänger\n(5V / 6V BEC)')
    dot.node('RES', shape='box', style='filled', fillcolor='white', label='4.7 kΩ\nWiderstand')

    # --- VERKABELUNG (LÖT-VERBINDUNGEN) ---

    # Stromversorgung Zentrale
    dot.edge('RC', 'ESP:vin', color='red', penwidth='2', label=' Plus (Rot)')
    dot.edge('RC', 'ESP:gnd', color='black', penwidth='2', label=' Minus (Schwarz)')

    # Stromversorgung Sensoren & SD (3.3V und GND)
    dot.edge('ESP:3v3', 'SD:vcc', color='red')
    dot.edge('ESP:3v3', 'TEMP:vcc', color='red')
    dot.edge('ESP:3v3', 'HALL:vcc', color='red')
    
    dot.edge('ESP:gnd', 'SD:gnd', color='black')
    dot.edge('ESP:gnd', 'TEMP:gnd', color='black')
    dot.edge('ESP:gnd', 'HALL:gnd', color='black')

    # SPI-Bus (MicroSD)
    dot.edge('ESP:g23', 'SD:mosi', color='blue', label=' MOSI')
    dot.edge('ESP:g19', 'SD:miso', color='blue', label=' MISO')
    dot.edge('ESP:g18', 'SD:sck', color='blue', label=' SCK')
    dot.edge('ESP:g5',  'SD:cs', color='blue', label=' CS')

    # Sensor-Datenleitungen
    dot.edge('ESP:g4', 'TEMP:dq', color='orange', label=' 1-Wire Data')
    dot.edge('ESP:g2', 'HALL:out', color='purple', label=' RPM Interrupt')

    # Der Pull-Up Widerstand (Spezialfall: Überbrückt 3.3V und Data)
    dot.edge('ESP:3v3', 'RES', color='red', style='dashed', label=' Lötbrücke 1')
    dot.edge('RES', 'ESP:g4', color='orange', style='dashed', label=' Lötbrücke 2')

    # Rendern ohne das Bild in Codespaces öffnen zu wollen
    dot.render(view=False)
    print("Der Lötplan wurde als 'ESP32_Loetplan.png' erfolgreich generiert!")

if __name__ == '__main__':
    erstelle_loetplan()
  
