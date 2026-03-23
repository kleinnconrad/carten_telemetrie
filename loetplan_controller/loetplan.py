import graphviz

def erstelle_sauberen_schaltplan():
    # Setup des Graphen: 'ortho' sorgt für eckige, kabel-ähnliche Linien
    # splines='polyline' minimiert Überkreuzungen
    dot = graphviz.Digraph('Sauberer_Schaltplan', filename='Schaltplan_Detailliert', format='png')
    dot.attr(rankdir='LR', splines='polyline', nodesep='1.0', ranksep='2.5')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # Physisches Pin-Layout für NodeMCU ESP32 (DevKit V1, basierend auf image_7.png)
    # Die Tabelle zeigt exakt, welcher physische Pin welche Funktion hat.
    esp32_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="3" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B> (Zentraleinheit)</TD></TR>
      <TR><TD BGCOLOR="#d3d3d3">Pin-Name</TD><TD BGCOLOR="#d3d3d3">ESP32 GPIO</TD><TD BGCOLOR="#d3d3d3">Ziel</TD></TR>
      
      <TR><TD PORT="vin">VIN (5V Input)</TD><TD>1 (Oben Links)</TD><TD PORT="vin_t">RC-Empfänger</TD></TR>
      <TR><TD PORT="3v3">3.3V (Output)</TD><TD>2 (Oben Rechts)</TD><TD PORT="3v3_t">Sensoren & SD</TD></TR>
      <TR><TD PORT="gnd">GND (Masse)</TD><TD>3</TD><TD PORT="gnd_t">Gemeinsame Masse</TD></TR>

      <TR><TD PORT="g23">GPIO 23 (SPI MOSI)</TD><TD>15</TD><TD PORT="g23_t">SD: MOSI</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (SPI MISO)</TD><TD>13</TD><TD PORT="g19_t">SD: MISO</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (SPI CLK)</TD><TD>12</TD><TD PORT="g18_t">SD: SCK</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (SPI CS)</TD><TD>10</TD><TD PORT="g5_t">SD: CS</TD></TR>

      <TR><TD PORT="g4">GPIO 4 (1-Wire Temp)</TD><TD>9</TD><TD PORT="g4_t">Temp-Sensoren</TD></TR>
      <TR><TD PORT="g2">GPIO 2 (RPM Interrupt)</TD><TD>8</TD><TD PORT="g2_t">Hall-Sensor</TD></TR>
      
      <TR><TD BGCOLOR="#f0f0f0"><I>Weitere Pins...</I></TD><TD BGCOLOR="#f0f0f0">...</TD><TD BGCOLOR="#f0f0f0">...</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # Detailliertes Pinout für MicroSD Modul
    sd_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#d3d3d3"><B>MicroSD (SPI)</B></TD></TR>
      <TR><TD BGCOLOR="#f0f0f0">Sensor Pin</TD><TD BGCOLOR="#f0f0f0">Zweck</TD></TR>
      <TR><TD PORT="vcc">VCC</TD><TD>An ESP: 3.3V</TD></TR>
      <TR><TD PORT="gnd">GND</TD><TD>An ESP: GND</TD></TR>
      <TR><TD PORT="miso">MISO</TD><TD>An ESP: GPIO 19</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD><TD>An ESP: GPIO 23</TD></TR>
      <TR><TD PORT="sck">SCK</TD><TD>An ESP: GPIO 18</TD></TR>
      <TR><TD PORT="cs">CS</TD><TD>An ESP: GPIO 5</TD></TR>
    </TABLE>>'''
    dot.node('SD', label=sd_html)

    # Physisches Pinout für DS18B20 Temperatursensoren (Paralleler Bus)
    # Beide Sensoren werden exakt gleich und parallel angeschlossen.
    temp_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="3" BGCOLOR="#ffffe0"><B>DS18B20 Temperatur</B> (Motor & ESC)</TD></TR>
      <TR><TD BGCOLOR="#f0f0f0">Pin</TD><TD BGCOLOR="#f0f0f0">Kabel-Farbe</TD><TD BGCOLOR="#f0f0f0">Zweck</TD></TR>
      <TR><TD PORT="vcc">VDD</TD><TD>Rot</TD><TD>An ESP: 3.3V</TD></TR>
      <TR><TD PORT="gnd">GND</TD><TD>Schwarz</TD><TD>An ESP: GND</TD></TR>
      <TR><TD PORT="dq">Data</TD><TD>Gelb / Blau</TD><TD>An ESP: GPIO 4</TD></TR>
    </TABLE>>'''
    dot.node('TEMP', label=temp_html)

    # Physisches Pinout für A3144 Hall-Sensor (RPM)
    hall_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="3" BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B> (RPM)</TD></TR>
      <TR><TD BGCOLOR="#f0f0f0">Pin #</TD><TD BGCOLOR="#f0f0f0">Pin-Bezeichnung</TD><TD BGCOLOR="#f0f0f0">Zweck</TD></TR>
      <TR><TD PORT="vcc">1 (Links)</TD><TD>VCC (Power)</TD><TD>An ESP: 3.3V</TD></TR>
      <TR><TD PORT="gnd">2 (Mitte)</TD><TD>GND (Masse)</TD><TD>An ESP: GND</TD></TR>
      <TR><TD PORT="out">3 (Rechts)</TD><TD>DOUT (Signal)</TD><TD>An ESP: GPIO 2</TD></TR>
    </TABLE>>'''
    dot.node('HALL', label=hall_html)

    # Gemeinsame Masse und 3.3V Power visualisieren (Leif's Tipp)
    # Die Sensoren teilen sich diese Leitungen, d.h. sie werden parallel angeschlossen.
    dot.node('RC', shape='box', style='filled', fillcolor='#90ee90', label='RC-Empfänger\n(5V Power für ESP32)')
    dot.node('Widerstand', shape='box', style='filled', fillcolor='white', label='4.7 kΩ\nPull-Up Widerstand')

    # --- VERKABELUNG ---

    # Stromversorgung Zentrale (RC an ESP32 VIN)
    dot.edge('RC', 'ESP:vin', color='red', penwidth='2', label=' Plus (5V)')
    dot.edge('RC', 'ESP:gnd', color='black', penwidth='2', label=' Minus (Masse)')

    # Stromversorgung Sensoren & SD (Alle an denselben 3.3V / GND Pins)
    # Verwende eine kleine Lötplatine, um diese Kabel zusammenzuführen, anstatt zu versuchen, multiple dicke Kabel an einen winzigen Pin zu löten.
    dot.edge('ESP:3v3', 'SD:vcc', color='red')
    dot.edge('ESP:3v3', 'TEMP:vcc', color='red')
    dot.edge('ESP:3v3', 'HALL:vcc', color='red')
    dot.edge('ESP:3v3', 'Widerstand', color='red', style='dashed', label=' Pull-Up Power')
    
    dot.edge('ESP:gnd', 'SD:gnd', color='black')
    dot.edge('ESP:gnd', 'TEMP:gnd', color='black')
    dot.edge('ESP:gnd', 'HALL:gnd', color='black')

    # SPI-Bus (MicroSD)
    dot.edge('ESP:g23', 'SD:mosi', color='blue', label=' MOSI')
    dot.edge('ESP:g19', 'SD:miso', color='blue', label=' MISO')
    dot.edge('ESP:g18', 'SD:sck', color='blue', label=' SCK')
    dot.edge('ESP:g5',  'SD:cs', color='blue', label=' CS')

    # Sensor-Datenleitungen
    dot.edge('ESP:g4', 'TEMP:dq', color='orange', label=' 1-Wire DQ')
    dot.edge('ESP:g2', 'HALL:out', color='purple', label=' RPM (Interrupt)')

    # Der kritische Pull-Up Widerstand für 1-Wire (Muss zwischen 3.3V und Data (GPIO 4) gelötet werden)
    dot.edge('Widerstand', 'ESP:g4', color='orange', style='dashed', label=' Zieht "Data" auf High')

    # Rendern
    dot.render(view=False)
    print("Professioneller, detaillierter Schaltplan generiert. Bitte öffne 'Schaltplan_Detailliert.png' im Dateibaum links.")

if __name__ == '__main__':
    erstelle_sauberen_schaltplan()
