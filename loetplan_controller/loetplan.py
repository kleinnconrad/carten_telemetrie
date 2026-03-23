import graphviz

def erstelle_detaillierten_loetplan():
    # Setup des Graphen: 'ortho' sorgt für eckige, kabel-ähnliche Linien
    dot = graphviz.Digraph('Loetplan', filename='RC_Telemetry_ESP32_Detaillierter_Loetplan', format='png')
    dot.attr(rankdir='LR', splines='ortho', nodesep='1.5', ranksep='2.5')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 als detaillierte Tabelle (Physisches Pinout)
    # Die Pins sind so angeordnet, wie sie auf dem NodeMCU 32S DevKit V1 physisch liegen.
    esp32_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="2" BGCOLOR="#add8e6"><B>NodeMCU ESP32 (DevKit V1)</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V/6V)</TD><TD PORT="3v3">3.3V (Output)</TD></TR>
      <TR><TD PORT="gnd1">GND</TD><TD PORT="gnd2">GND</TD></TR>
      <TR><TD PORT="g13">D13</TD><TD PORT="g23">D23</TD></TR>
      <TR><TD PORT="g12">D12</TD><TD PORT="g22">D22</TD></TR>
      <TR><TD PORT="g14">D14</TD><TD PORT="g21">D21</TD></TR>
      <TR><TD PORT="g27">D27</TD><TD PORT="tx0">TX0</TD></TR>
      <TR><TD PORT="g26">D26</TD><TD PORT="rx0">RX0</TD></TR>
      <TR><TD PORT="g25">D25</TD><TD PORT="g19">D19</TD></TR>
      <TR><TD PORT="g33">D33</TD><TD PORT="g18">D18</TD></TR>
      <TR><TD PORT="g32">D32</TD><TD PORT="g5">D5</TD></TR>
      <TR><TD PORT="g35">D35</TD><TD PORT="g17">D17</TD></TR>
      <TR><TD PORT="g34">D34</TD><TD PORT="g16">D16</TD></TR>
      <TR><TD PORT="vn">VN</TD><TD PORT="g4">D4</TD></TR>
      <TR><TD PORT="vp">VP</TD><TD PORT="g2">D2</TD></TR>
      <TR><TD PORT="en">EN</TD><TD PORT="g15">D15</TD></TR>
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
    dot.node('RC', shape='box', style='filled', fillcolor='#90ee90', label='RC-Empfänger\n(5V BEC Power)')
    dot.node('RES', shape='box', style='filled', fillcolor='white', label='4.7 kΩ\nPull-Up Widerstand')

    # --- VERKABELUNG (LÖT-VERBINDUNGEN) ---

    # Stromversorgung Zentrale (VIN an VIN, GND an GND1)
    dot.edge('RC', 'ESP:vin', color='red', penwidth='2', label=' Plus (Rot)')
    dot.edge('RC', 'ESP:gnd1', color='black', penwidth='2', label=' Minus (Schwarz)')

    # Stromversorgung Sensoren & SD (Alle an 3.3V und GND2)
    # Tipp: Verwende eine kleine Platine, um diese Kabel zusammenzuführen, anstatt zu versuchen, multiple dicke Kabel an einen winzigen Pin zu löten.
    dot.edge('ESP:3v3', 'SD:vcc', color='red')
    dot.edge('ESP:3v3', 'TEMP:vcc', color='red')
    dot.edge('ESP:3v3', 'HALL:vcc', color='red')
    
    dot.edge('ESP:gnd2', 'SD:gnd', color='black')
    dot.edge('ESP:gnd2', 'TEMP:gnd', color='black')
    dot.edge('ESP:gnd2', 'HALL:gnd', color='black')

    # SPI-Bus (MicroSD) - Entspricht C++ Code Pin-Definition
    dot.edge('ESP:g23', 'SD:mosi', color='blue', label=' SPI MOSI (-> D23)')
    dot.edge('ESP:g19', 'SD:miso', color='blue', label=' SPI MISO (-> D19)')
    dot.edge('ESP:g18', 'SD:sck', color='blue', label=' SPI CLK (-> D18)')
    dot.edge('ESP:g5',  'SD:cs', color='blue', label=' SPI CS (-> D5, C++ CS)')

    # Sensor-Datenleitungen
    dot.edge('ESP:g4', 'TEMP:dq', color='orange', label=' 1-Wire DQ (-> D4, C++ Temp)')
    dot.edge('ESP:g2', 'HALL:out', color='purple', label=' RPM (-> D2, C++ Hall)')

    # Der Pull-Up Widerstand (MUSS zwischen 3.3V und Data (GPIO 4) gelötet werden)
    # Dies ist am besten direkt auf der kleinen Sensor-Anschlussplatine zu lösen.
    dot.edge('ESP:3v3', 'RES', color='red', style='dashed', label=' Lötbrücke 1')
    dot.edge('RES', 'ESP:g4', color='orange', style='dashed', label=' Lötbrücke 2')

    # Rendern ohne das Bild in Codespaces öffnen zu wollen
    dot.render(view=False)
    print("Detaillierter Lötplan generiert. Bitte öffne 'RC_Telemetry_ESP32_Detaillierter_Loetplan.png' im Dateibaum.")

if __name__ == '__main__':
    erstelle_detaillierten_loetplan()
