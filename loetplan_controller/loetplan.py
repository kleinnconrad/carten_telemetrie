import graphviz

def erstelle_sauberen_schaltplan():
    dot = graphviz.Digraph('Sauberer_Schaltplan', filename='Schaltplan_Detailliert', format='png')
    dot.attr(rankdir='LR', splines='polyline', nodesep='1.0', ranksep='2.0')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. Zentraleinheit ESP32 (bereinigtes HTML)
    esp32_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="2" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B> (DevKit V1)</TD></TR>
      <TR><TD BGCOLOR="#d3d3d3">Pin / Funktion</TD><TD BGCOLOR="#d3d3d3">ESP32 Pin</TD></TR>
      
      <TR><TD PORT="vin">VIN (5V Input)</TD><TD>1 (Oben Links)</TD></TR>
      <TR><TD PORT="3v3">3.3V (Output)</TD><TD>2 (Oben Rechts)</TD></TR>
      <TR><TD PORT="gnd">GND (Masse)</TD><TD>3</TD></TR>

      <TR><TD PORT="g23">GPIO 23 (MOSI)</TD><TD>15</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (MISO)</TD><TD>13</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (CLK)</TD><TD>12</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (CS)</TD><TD>10</TD></TR>

      <TR><TD PORT="g4">GPIO 4 (1-Wire)</TD><TD>9</TD></TR>
      <TR><TD PORT="g2">GPIO 2 (Interrupt)</TD><TD>8</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. MicroSD Modul
    sd_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#d3d3d3"><B>MicroSD Modul</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="miso">MISO</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD></TR>
      <TR><TD PORT="sck">SCK</TD></TR>
      <TR><TD PORT="cs">CS</TD></TR>
    </TABLE>>'''
    dot.node('SD', label=sd_html)

    # 3. Temperatursensoren
    temp_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#ffffe0"><B>DS18B20 Temp.</B> (Motor &amp; ESC)</TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''
    dot.node('TEMP', label=temp_html)

    # 4. Hall Sensor
    hall_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B></TD></TR>
      <TR><TD PORT="vcc">1: VCC (Power)</TD></TR>
      <TR><TD PORT="gnd">2: GND (Masse)</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD></TR>
    </TABLE>>'''
    dot.node('HALL', label=hall_html)

    # 5. Externe Komponenten
    dot.node('RC', shape='box', style='filled', fillcolor='#90ee90', label='RC-Empfänger\n(5V Power)')
    dot.node('Widerstand', shape='box', style='filled', fillcolor='white', label='4.7 kΩ\nPull-Up Widerstand')

    # --- VERKABELUNG ---
    
    # Power vom Empfänger
    dot.edge('RC', 'ESP:vin', color='red', penwidth='2', label=' Plus (5V)')
    dot.edge('RC', 'ESP:gnd', color='black', penwidth='2', label=' Minus')

    # 3.3V Versorgung
    dot.edge('ESP:3v3', 'SD:vcc', color='red')
    dot.edge('ESP:3v3', 'TEMP:vcc', color='red')
    dot.edge('ESP:3v3', 'HALL:vcc', color='red')
    dot.edge('ESP:3v3', 'Widerstand', color='red', style='dashed')
    
    # GND Versorgung
    dot.edge('ESP:gnd', 'SD:gnd', color='black')
    dot.edge('ESP:gnd', 'TEMP:gnd', color='black')
    dot.edge('ESP:gnd', 'HALL:gnd', color='black')

    # SPI Leitungen
    dot.edge('ESP:g23', 'SD:mosi', color='blue', label=' MOSI')
    dot.edge('ESP:g19', 'SD:miso', color='blue', label=' MISO')
    dot.edge('ESP:g18', 'SD:sck', color='blue', label=' SCK')
    dot.edge('ESP:g5',  'SD:cs', color='blue', label=' CS')

    # Datenleitungen Sensoren
    dot.edge('ESP:g4', 'TEMP:dq', color='orange', label=' 1-Wire DQ')
    dot.edge('ESP:g2', 'HALL:out', color='purple', label=' RPM Signal')

    # Pull-Up Lötbrücke
    dot.edge('Widerstand', 'ESP:g4', color='orange', style='dashed', label=' Pull-Up (High)')

    # Rendern
    dot.render(view=False)
    print("Schaltplan erfolgreich repariert und generiert!")

if __name__ == '__main__':
    erstelle_sauberen_schaltplan()
