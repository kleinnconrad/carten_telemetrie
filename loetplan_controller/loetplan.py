import graphviz

def erstelle_sauberen_schaltplan():
    # Setup des Graphen. TB (Top-to-Bottom) ist die zentrale Hub-and-Spoke-Architektur.
    # splines='spline' für sanfte, klare Linien.
    # nodesep/ranksep sind riesig, um die Kabel zu entflechten.
    dot = graphviz.Digraph('Sauberer_Schaltplan', filename='Schaltplan_Detailliert', format='png')
    dot.attr(rankdir='TB', splines='spline', nodesep='3.5', ranksep='6.0', overlap='false', compound='true')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='14')
    dot.attr('edge', headport='c', tailport='c') # Verbindungen an Zellenmitte

    # Ein Diagramm-Titel hinzufügen
    dot.attr(label="RC Telemetrie ESP32 Wiring Diagram", labelloc="t", fontsize="24")

    # --- Z E N T R A L E (Hub) ---

    # 1. Detailliertes Pin-Layout für NodeMCU ESP32 (DevKit V1, basierend auf image_7.png)
    # Die Tabelle zeigt exakt, welcher physische Pin welche Funktion hat.
    esp32_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8">
      <TR><TD COLSPAN="2" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B> (DevKit V1 Hub)</TD></TR>
      <TR><TD BGCOLOR="#d3d3d3">Pin-Name</TD><TD BGCOLOR="#d3d3d3">Funktion / GPIO</TD></TR>
      
      <TR><TD PORT="vin">VIN (5V Input)</TD><TD>1 (Oben Links)</TD></TR>
      <TR><TD PORT="3v3">3.3V (Output)</TD><TD>2 (Oben Rechts)</TD></TR>
      <TR><TD PORT="gnd">GND (Masse)</TD><TD>3</TD></TR>

      <TR><TD PORT="g23">GPIO 23 (SPI MOSI)</TD><TD>15</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (SPI MISO)</TD><TD>13</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (SPI CLK)</TD><TD>12</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (SPI CS)</TD><TD>10</TD></TR>

      <TR><TD PORT="g4">GPIO 4 (1-Wire DQ)</TD><TD>9</TD></TR>
      <TR><TD PORT="g2">GPIO 2 (Interrupt)</TD><TD>8</TD></TR>
      
      <TR><TD BGCOLOR="#f0f0f0"><I>Weitere Pins...</I></TD><TD BGCOLOR="#f0f0f0">...</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # --- P E R I P H E R I E (Rund um den Hub) ---

    # Power Source (Oben-Links)
    dot.node('RC', shape='box', style='filled', fillcolor='#90ee90', label='RC-Empfänger\n(5V Power Source)')

    # MicroSD Modul (Unten-Rechts, hochwire count)
    sd_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="2" BGCOLOR="#d3d3d3"><B>MicroSD (SPI)</B></TD></TR>
      <TR><TD BGCOLOR="#f0f0f0">Modul Pin</TD><TD BGCOLOR="#f0f0f0">Verbindung zu ESP</TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD><TD>Pin 2 (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD><TD>Pin 3 (GND)</TD></TR>
      <TR><TD PORT="miso">MISO</TD><TD>Pin 13 (GPIO 19)</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD><TD>Pin 15 (GPIO 23)</TD></TR>
      <TR><TD PORT="sck">SCK</TD><TD>Pin 12 (GPIO 18)</TD></TR>
      <TR><TD PORT="cs">CS</TD><TD>Pin 10 (GPIO 5)</TD></TR>
    </TABLE>>'''
    dot.node('SD', label=sd_html)

    # Hall Sensor (RPM, Oben-Rechts)
    hall_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="2" BGCOLOR="#ffb6c1"><B>A3144 Hall (RPM)</B></TD></TR>
      <TR><TD BGCOLOR="#f0f0f0">Sensor Pin</TD><TD BGCOLOR="#f0f0f0">Zweck</TD></TR>
      <TR><TD PORT="vcc">1: VCC (3.3V)</TD><TD>An ESP: 3.3V</TD></TR>
      <TR><TD PORT="gnd">2: GND</TD><TD>An ESP: GND</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD><TD>An ESP: GPIO 2</TD></TR>
    </TABLE>>'''
    dot.node('HALL', label=hall_html)

    # DS18B20 Temperatursensoren (Paralleler Bus, Center-Rechts)
    temp_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="3" BGCOLOR="#ffffe0"><B>DS18B20 Temp.</B> (Motor &amp; ESC)</TD></TR>
      <TR><TD BGCOLOR="#f0f0f0">Pin (Kabel)</TD><TD BGCOLOR="#f0f0f0">Zweck</TD><TD BGCOLOR="#f0f0f0">An ESP</TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD><TD>Power (3.3V)</TD><TD>Pin 2 (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD><TD>Masse</TD><TD>Pin 3 (GND)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD><TD>1-Wire Data</TD><TD>Pin 9 (GPIO 4)</TD></TR>
    </TABLE>>'''
    dot.node('TEMP', label=temp_html)

    # Pull-Up Widerstand (nahe Temp und ESP4, Mitte-Unten)
    dot.node('WIDERSTAND', shape='box', style='filled', fillcolor='white', label='4.7 kΩ\nPull-Up Widerstand')

    # --- VERKABELUNG (Sternschaltung) ---

    # 1. STROMVERSORGUNG (RC an ESP VIN, dicke Leitungen)
    dot.edge('RC', 'ESP:vin', color='red', penwidth='3', label=' Plus (5V BEC)')
    dot.edge('RC', 'ESP:gnd', color='black', penwidth='3', label=' Minus (GND)')

    # 2. SENSOR-BUSSE (Strom & GND, farbkodiert)
    # Power (ESP 3.3V an alle)
    dot.edge('ESP:3v3', 'SD:vcc', color='red', penwidth='1.5')
    dot.edge('ESP:3v3', 'TEMP:vcc', color='red', penwidth='1.5')
    dot.edge('ESP:3v3', 'HALL:vcc', color='red', penwidth='1.5')
    # Masse (ESP GND an alle)
    dot.edge('ESP:gnd', 'SD:gnd', color='black', penwidth='1.5')
    dot.edge('ESP:gnd', 'TEMP:gnd', color='black', penwidth='1.5')
    dot.edge('ESP:gnd', 'HALL:gnd', color='black', penwidth='1.5')

    # 3. SPI BUS (MicroSD, color-coded, distinct colors)
    dot.edge('ESP:g23', 'SD:mosi', color='blue', label=' SPI MOSI (-> D23)')
    dot.edge('ESP:g19', 'SD:miso', color='blue', label=' SPI MISO (-> D19)')
    dot.edge('ESP:g18', 'SD:sck', color='blue', label=' SPI CLK (-> D18)')
    dot.edge('ESP:g5',  'SD:cs', color='blue', label=' SPI CS (-> D5)')

    # 4. SENSOR DATEN (color-coded, distinct colors)
    dot.edge('ESP:g4', 'TEMP:dq', color='orange', label=' 1-Wire DQ Data (-> D4)')
    dot.edge('ESP:g2', 'HALL:out', color='purple', label=' RPM Signal Interrupt (-> D2)')

    # 5. DER KRITISCHE WIDERSTAND (Dash-Lines für Spezialverbindungen)
    # Verbindet eine Seite mit 3.3V Power Bus
    dot.edge('ESP:3v3', 'WIDERSTAND', color='red', style='dashed', label=' Pull-Up Power')
    # Verbindet andere Seite mit DQ Data Bus (GPIO 4)
    dot.edge('WIDERSTAND', 'ESP:g4', color='orange', style='dashed', label=' Pull-Up (DQ High)')

    # Rendern
    dot.render(view=False)
    print("Detaillierter, Stern-Schaltplan generiert. Bitte öffne die PNG-Datei links.")

if __name__ == '__main__':
    erstelle_sauberen_schaltplan()
