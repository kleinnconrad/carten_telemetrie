import graphviz

def erstelle_perfekten_cloud_loetplan():
    dot = graphviz.Digraph('Cloud_Schaltplan', filename='Schaltplan_Cloud_Perfekt', format='png')
    
    # rankdir='LR' erzwingt den horizontalen Fluss.
    dot.attr(rankdir='LR', splines='polyline', nodesep='1.0', ranksep='4.0')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 ZENTRALE
    esp32_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="3" BGCOLOR="#add8e6"><B>NodeMCU ESP32 (Hub)</B></TD></TR>
      <TR><TD BGCOLOR="#d3d3d3"><B>Linke Pins</B></TD><TD BGCOLOR="#e0e0e0" ROWSPAN="11"> ESP32 <br/> Core </TD><TD BGCOLOR="#d3d3d3"><B>Rechte Pins</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V In)</TD><TD PORT="3v3_r1">3.3V (Out)</TD></TR>
      <TR><TD PORT="gnd_l1">GND (Masse)</TD><TD PORT="gnd_r1">GND (Masse)</TD></TR>
      <TR><TD PORT="g32">GPIO 32 (RX1)</TD><TD PORT="g16">GPIO 16 (RX2)</TD></TR>
      <TR><TD PORT="g33">GPIO 33 (TX1)</TD><TD PORT="g17">GPIO 17 (TX2)</TD></TR>
      <TR><TD PORT="3v3_l">3.3V (Out)</TD><TD PORT="3v3_r2">3.3V (Out)</TD></TR>
      <TR><TD PORT="gnd_l2">GND (Masse)</TD><TD PORT="gnd_r2">GND (Masse)</TD></TR>
      <TR><TD PORT="g23">GPIO 23 (MOSI)</TD><TD PORT="g4">GPIO 4 (1-Wire)</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (MISO)</TD><TD PORT="g2">GPIO 2 (Interrupt)</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (SCK)</TD><TD>---</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (CS)</TD><TD>---</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. KOMPONENTEN LINKE SEITE
    pb_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#90ee90"><B>USB Powerbank</B></TD></TR>
      <TR><TD PORT="v5">5V (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
    </TABLE>>'''
    
    lte_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffa07a"><B>SIM7000 LTE Modul</B></TD></TR>
      <TR><TD PORT="vcc">VCC (5V In)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="tx">TX (Senden)</TD></TR>
      <TR><TD PORT="rx">RX (Empfang)</TD></TR>
    </TABLE>>'''

    sd_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#d3d3d3"><B>MicroSD (SPI)</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD></TR>
      <TR><TD PORT="miso">MISO</TD></TR>
      <TR><TD PORT="sck">SCK</TD></TR>
      <TR><TD PORT="cs">CS</TD></TR>
    </TABLE>>'''

    with dot.subgraph() as s_left:
        s_left.attr(rank='same')
        s_left.node('PB', label=pb_html)
        s_left.node('LTE', label=lte_html)
        s_left.node('SD', label=sd_html)
        s_left.edge('PB', 'LTE', style='invis')
        s_left.edge('LTE', 'SD', style='invis')

    # 3. KOMPONENTEN RECHTE SEITE
    gps_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#87cefa"><B>GPS BN-220</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="tx">TX (Senden)</TD></TR>
      <TR><TD PORT="rx">RX (Empfang)</TD></TR>
    </TABLE>>'''

    temp_mot_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 (Motor)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''

    temp_esc_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 (ESC)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''

    hall_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B></TD></TR>
      <TR><TD PORT="vcc">1: VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">2: GND</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD></TR>
    </TABLE>>'''

    res_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="white"><B>4.7 kΩ Pull-Up</B></TD></TR>
      <TR><TD PORT="p1">Zu 3.3V</TD><TD PORT="p2">Zu GPIO 4</TD></TR>
    </TABLE>>'''

    with dot.subgraph() as s_right:
        s_right.attr(rank='same')
        s_right.node('GPS', label=gps_html)
        s_right.node('TEMP_MOT', label=temp_mot_html)
        s_right.node('TEMP_ESC', label=temp_esc_html)
        s_right.node('HALL', label=hall_html)
        s_right.node('RES', label=res_html)
        s_right.edge('GPS', 'TEMP_MOT', style='invis')
        s_right.edge('TEMP_MOT', 'TEMP_ESC', style='invis')
        s_right.edge('TEMP_ESC', 'HALL', style='invis')
        s_right.edge('HALL', 'RES', style='invis')

    # --- VERKABELUNG ---

    # LINKE SEITE -> Andocken an ESP Linke Pins (:w)
    
    # 1. POWERBANK SPLITTER
    # Powerbank -> ESP32 (Nach Rechts)
    dot.edge('PB:v5:e', 'ESP:vin:w', color='red', penwidth='3', dir='none')
    dot.edge('PB:gnd:e', 'ESP:gnd_l1:w', color='black', penwidth='3', dir='none')
    
    # Powerbank -> LTE Modul (Nach Links! Führung über die Außenseite, isoliert vom ESP)
    dot.edge('PB:v5:w', 'LTE:vcc:w', color='red', penwidth='3', dir='none')
    dot.edge('PB:gnd:w', 'LTE:gnd:w', color='black', penwidth='3', dir='none')

    # LTE UART (Überkreuzt)
    dot.edge('LTE:tx:e', 'ESP:g32:w', color='purple', penwidth='2', dir='none')
    dot.edge('LTE:rx:e', 'ESP:g33:w', color='magenta', penwidth='2', dir='none')

    # SD Karte (3.3V gestrichelt vom ESP!)
    dot.edge('SD:vcc:e', 'ESP:3v3_l:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('SD:gnd:e', 'ESP:gnd_l2:w', color='black', penwidth='2', dir='none')
    dot.edge('SD:mosi:e', 'ESP:g23:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:miso:e', 'ESP:g19:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:sck:e', 'ESP:g18:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:cs:e', 'ESP:g5:w', color='blue', penwidth='2', dir='none')

    # RECHTE SEITE -> Andocken an ESP Rechte Pins (:e)

    # GPS (UART Überkreuzt)
    dot.edge('ESP:3v3_r1:e', 'GPS:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r1:e', 'GPS:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g16:e', 'GPS:tx:w', color='magenta', penwidth='2', dir='none') 
    dot.edge('ESP:g17:e', 'GPS:rx:w', color='purple', penwidth='2', dir='none')  

    # Motor Temp
    dot.edge('ESP:3v3_r2:e', 'TEMP_MOT:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r2:e', 'TEMP_MOT:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g4:e', 'TEMP_MOT:dq:w', color='orange', penwidth='2', dir='none')

    # ESC Temp
    dot.edge('ESP:3v3_r2:e', 'TEMP_ESC:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r2:e', 'TEMP_ESC:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g4:e', 'TEMP_ESC:dq:w', color='orange', penwidth='2', dir='none')

    # Hall Sensor
    dot.edge('ESP:3v3_r2:e', 'HALL:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r2:e', 'HALL:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g2:e', 'HALL:out:w', color='green', penwidth='2', dir='none')

    # Pull-Up Widerstand
    dot.edge('ESP:3v3_r2:e', 'RES:p1:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('RES:p2:w', 'ESP:g4:e', color='orange', style='dashed', penwidth='2', dir='none')

    dot.render(view=False)
    print("Makelloser, zentrierter Cloud-Lötplan (mit korrigiertem Strom-Routing) generiert!")

if __name__ == '__main__':
    erstelle_perfekten_cloud_loetplan()
