import graphviz

def erstelle_lte_gps_schaltplan():
    dot = graphviz.Digraph('Schaltplan', filename='Schaltplan_Cloud_Telemetry', format='png')
    
    # splines='polyline' für exaktes Andocken an den Pins
    dot.attr(rankdir='LR', splines='polyline', nodesep='0.8', ranksep='3.5')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 ZENTRALE (Erweitert um UART Pins für GPS und LTE)
    esp32_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="3" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B> (Zentrale)</TD></TR>
      <TR><TD BGCOLOR="#d3d3d3"><B>Linke Pins</B></TD><TD BGCOLOR="#e0e0e0" ROWSPAN="10"> ESP32 <br/> Core </TD><TD BGCOLOR="#d3d3d3"><B>Rechte Pins</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V In)</TD><TD PORT="3v3_r">3.3V (Out)</TD></TR>
      <TR><TD PORT="3v3_l">3.3V (Out)</TD><TD PORT="gnd_r">GND (Masse)</TD></TR>
      <TR><TD PORT="gnd_l">GND (Masse)</TD><TD PORT="g4">GPIO 4 (1-Wire Bus)</TD></TR>
      <TR><TD PORT="g23">GPIO 23 (SD MOSI)</TD><TD PORT="g2">GPIO 2 (Hall Interrupt)</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (SD MISO)</TD><TD PORT="g16">GPIO 16 (GPS RX2)</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (SD SCK)</TD><TD PORT="g17">GPIO 17 (GPS TX2)</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (SD CS)</TD><TD>---</TD></TR>
      <TR><TD PORT="g32">GPIO 32 (LTE RX1)</TD><TD>---</TD></TR>
      <TR><TD PORT="g33">GPIO 33 (LTE TX1)</TD><TD>---</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. KOMPONENTEN LINKE SEITE (Powerbank, SD, LTE)
    pb_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#90ee90"><B>USB Powerbank</B> (Autark)</TD></TR>
      <TR><TD PORT="5v">5V (VBUS / Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
    </TABLE>>'''
    
    sd_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
      <TR><TD BGCOLOR="#d3d3d3"><B>MicroSD (SPI Backup)</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD></TR>
      <TR><TD PORT="miso">MISO</TD></TR>
      <TR><TD PORT="sck">SCK</TD></TR>
      <TR><TD PORT="cs">CS</TD></TR>
    </TABLE>>'''

    lte_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
      <TR><TD BGCOLOR="#ffa07a"><B>LTE Modul</B> (z.B. SIM7000)</TD></TR>
      <TR><TD PORT="vcc">VCC (5V In!)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="tx">TX (Senden)</TD></TR>
      <TR><TD PORT="rx">RX (Empfangen)</TD></TR>
    </TABLE>>'''

    with dot.subgraph() as s_left:
        s_left.attr(rank='same')
        s_left.node('PB', label=pb_html)
        s_left.node('LTE', label=lte_html)
        s_left.node('SD', label=sd_html)
        s_left.edge('PB', 'LTE', style='invis')
        s_left.edge('LTE', 'SD', style='invis')

    # 3. KOMPONENTEN RECHTE SEITE (Sensoren & GPS)
    gps_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
      <TR><TD BGCOLOR="#87cefa"><B>GPS Modul</B> (z.B. BN-220)</TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="tx">TX (Senden)</TD></TR>
      <TR><TD PORT="rx">RX (Empfangen)</TD></TR>
    </TABLE>>'''

    temp_motor_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 (Motor)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''

    temp_esc_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 (ESC)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''

    hall_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B></TD></TR>
      <TR><TD PORT="vcc">1: VCC</TD></TR>
      <TR><TD PORT="gnd">2: GND</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD></TR>
    </TABLE>>'''

    res_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="2">
      <TR><TD COLSPAN="2" BGCOLOR="white"><B>4.7 kΩ Pull-Up</B></TD></TR>
      <TR><TD PORT="p1">Zu 3.3V</TD><TD PORT="p2">Zu GPIO 4</TD></TR>
    </TABLE>>'''

    with dot.subgraph() as s_right:
        s_right.attr(rank='same')
        s_right.node('GPS', label=gps_html)
        s_right.node('TEMP_MOT', label=temp_motor_html)
        s_right.node('TEMP_ESC', label=temp_esc_html)
        s_right.node('HALL', label=hall_html)
        s_right.node('RES', label=res_html)
        s_right.edge('GPS', 'TEMP_MOT', style='invis') 
        s_right.edge('TEMP_MOT', 'TEMP_ESC', style='invis') 
        s_right.edge('TEMP_ESC', 'HALL', style='invis')
        s_right.edge('HALL', 'RES', style='invis')  

    # --- VERKABELUNG LINKE SEITE ---
    
    # POWERBANK: Splittet 5V direkt an ESP32 und LTE Modul!
    dot.edge('PB:5v:e', 'ESP:vin:w', color='red', penwidth='3', dir='none', label=' 5V')
    dot.edge('PB:5v:e', 'LTE:vcc:w', color='red', penwidth='3', dir='none')
    dot.edge('PB:gnd:e', 'ESP:gnd_l:w', color='black', penwidth='3', dir='none', label=' GND')
    dot.edge('PB:gnd:e', 'LTE:gnd:w', color='black', penwidth='3', dir='none')

    # LTE UART (Überkreuzt: TX->RX, RX->TX)
    dot.edge('LTE:tx:e', 'ESP:g32:w', color='purple', penwidth='2', dir='none', label=' TX zu RX1')
    dot.edge('LTE:rx:e', 'ESP:g33:w', color='magenta', penwidth='2', dir='none', label=' RX zu TX1')

    # SD Karte (3.3V vom ESP32)
    dot.edge('ESP:3v3_l:w', 'SD:vcc:e', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_l:w', 'SD:gnd:e', color='black', penwidth='2', dir='none')
    dot.edge('SD:mosi:e', 'ESP:g23:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:miso:e', 'ESP:g19:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:sck:e', 'ESP:g18:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:cs:e', 'ESP:g5:w', color='blue', penwidth='2', dir='none')

    # --- VERKABELUNG RECHTE SEITE ---

    # GPS Modul (3.3V vom ESP32, UART Überkreuzt)
    dot.edge('ESP:3v3_r:e', 'GPS:vcc:w', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'GPS:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('GPS:tx:w', 'ESP:g16:e', color='purple', penwidth='2', dir='none', label=' TX zu RX2')
    dot.edge('GPS:rx:w', 'ESP:g17:e', color='magenta', penwidth='2', dir='none', label=' RX zu TX2')
    
    # 1-Wire Sensoren (Parallel)
    dot.edge('ESP:3v3_r:e', 'TEMP_MOT:vcc:w', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'TEMP_MOT:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g4:e', 'TEMP_MOT:dq:w', color='orange', penwidth='2', dir='none')

    dot.edge('ESP:3v3_r:e', 'TEMP_ESC:vcc:w', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'TEMP_ESC:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g4:e', 'TEMP_ESC:dq:w', color='orange', penwidth='2', dir='none')

    # Hall Sensor
    dot.edge('ESP:3v3_r:e', 'HALL:vcc:w', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'HALL:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g2:e', 'HALL:out:w', color='green', penwidth='2', dir='none')

    # Pull-Up Widerstand
    dot.edge('ESP:3v3_r:e', 'RES:p1:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('RES:p2:w', 'ESP:g4:e', color='orange', style='dashed', penwidth='2', dir='none') 

    # Rendern
    dot.render(view=False)
    print("Isolierter Cloud-Telemetry Schaltplan generiert! Bitte öffne 'Schaltplan_Cloud_Telemetry.png'.")

if __name__ == '__main__':
    erstelle_lte_gps_schaltplan()
