import graphviz

def erstelle_perfekten_schaltplan():
    dot = graphviz.Digraph('Schaltplan', filename='Schaltplan_Perfekt', format='png')
    
    # splines='polyline' erzwingt, dass die Linien exakt an den definierten Pins andocken!
    dot.attr(rankdir='LR', splines='polyline', nodesep='0.8', ranksep='3.5')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 ALS ZWEISPALTIGE ZENTRALE
    esp32_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="3" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B> (Zentrale)</TD></TR>
      <TR><TD BGCOLOR="#d3d3d3"><B>Linke Pins</B></TD><TD BGCOLOR="#e0e0e0" ROWSPAN="8"> ESP32 <br/> Core </TD><TD BGCOLOR="#d3d3d3"><B>Rechte Pins</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V In)</TD><TD PORT="3v3_r">3.3V (Out)</TD></TR>
      <TR><TD PORT="3v3_l">3.3V (Out)</TD><TD PORT="gnd_r">GND (Masse)</TD></TR>
      <TR><TD PORT="gnd_l">GND (Masse)</TD><TD PORT="g4">GPIO 4 (1-Wire)</TD></TR>
      <TR><TD PORT="g23">GPIO 23 (MOSI)</TD><TD PORT="g2">GPIO 2 (Hall Interrupt)</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (MISO)</TD><TD>---</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (SCK)</TD><TD>---</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (CS)</TD><TD>---</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. KOMPONENTEN AUF DER LINKEN SEITE
    rc_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#90ee90"><B>RC-Empfänger</B></TD></TR>
      <TR><TD PORT="vin">5V Power</TD></TR>
      <TR><TD PORT="gnd">Masse</TD></TR>
    </TABLE>>'''
    
    # Reihenfolge exakt an ESP32 angepasst für 0 Überschneidungen
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

    # Subgraph erzwingt saubere vertikale Anordnung links
    with dot.subgraph() as s_left:
        s_left.attr(rank='same')
        s_left.node('RC', label=rc_html)
        s_left.node('SD', label=sd_html)
        s_left.edge('RC', 'SD', style='invis') # Unsichtbare Linie schiebt SD unter RC

    # 3. KOMPONENTEN AUF DER RECHTEN SEITE
    temp_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 Temp.</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''

    hall_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B></TD></TR>
      <TR><TD PORT="vcc">1: VCC (Power)</TD></TR>
      <TR><TD PORT="gnd">2: GND (Masse)</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD></TR>
    </TABLE>>'''

    # Widerstand mit zwei sauberen Pins
    res_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="white"><B>4.7 kΩ Pull-Up</B></TD></TR>
      <TR><TD PORT="p1">Zu 3.3V</TD><TD PORT="p2">Zu GPIO 4</TD></TR>
    </TABLE>>'''

    # Subgraph erzwingt saubere vertikale Anordnung rechts
    with dot.subgraph() as s_right:
        s_right.attr(rank='same')
        s_right.node('TEMP', label=temp_html)
        s_right.node('HALL', label=hall_html)
        s_right.node('RES', label=res_html)
        s_right.edge('TEMP', 'HALL', style='invis') # Schiebt Hall unter Temp
        s_right.edge('HALL', 'RES', style='invis')  # Schiebt Widerstand ganz nach unten

    # --- VERKABELUNG LINKE SEITE ---
    # :e und :w zwingen die Linien auf die exakte vertikale Mitte der Zelle!
    dot.edge('RC:vin:e', 'ESP:vin:w', color='red', penwidth='2', dir='none')
    dot.edge('RC:gnd:e', 'ESP:gnd_l:w', color='black', penwidth='2', dir='none')

    dot.edge('SD:vcc:e', 'ESP:3v3_l:w', color='red', penwidth='2', dir='none')
    dot.edge('SD:gnd:e', 'ESP:gnd_l:w', color='black', penwidth='2', dir='none')
    dot.edge('SD:mosi:e', 'ESP:g23:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:miso:e', 'ESP:g19:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:sck:e', 'ESP:g18:w', color='blue', penwidth='2', dir='none')
    dot.edge('SD:cs:e', 'ESP:g5:w', color='blue', penwidth='2', dir='none')

    # --- VERKABELUNG RECHTE SEITE ---
    dot.edge('ESP:3v3_r:e', 'TEMP:vcc:w', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'TEMP:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g4:e', 'TEMP:dq:w', color='orange', penwidth='2', dir='none')

    dot.edge('ESP:3v3_r:e', 'HALL:vcc:w', color='red', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'HALL:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:g2:e', 'HALL:out:w', color='purple', penwidth='2', dir='none')

    # --- PULL-UP WIDERSTAND ---
    dot.edge('ESP:3v3_r:e', 'RES:p1:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('RES:p2:w', 'ESP:g4:e', color='orange', style='dashed', penwidth='2', dir='none') 

    # Rendern
    dot.render(view=False)
    print("Makelloser Schaltplan generiert! Bitte öffne 'Schaltplan_Perfekt.png'.")

if __name__ == '__main__':
    erstelle_perfekten_schaltplan()
