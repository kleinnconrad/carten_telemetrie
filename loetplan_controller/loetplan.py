import graphviz

def erstelle_perfekten_schaltplan():
    dot = graphviz.Digraph('Schaltplan', filename='Schaltplan_Perfekt', format='png')
    
    # rankdir=LR zeichnet streng von links nach rechts. 
    # splines=ortho macht schöne 90-Grad "Kabel"-Verläufe.
    dot.attr(rankdir='LR', splines='ortho', nodesep='1.0', ranksep='3.0')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 ALS ZWEISPALTIGE ZENTRALE
    esp32_html = '''<
    <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8">
      <TR><TD COLSPAN="3" BGCOLOR="#add8e6"><B>NodeMCU ESP32</B> (Zentrale)</TD></TR>
      <TR><TD BGCOLOR="#d3d3d3"><B>Linke Pins</B></TD><TD BGCOLOR="#e0e0e0" ROWSPAN="7"> ESP32 <br/> Core </TD><TD BGCOLOR="#d3d3d3"><B>Rechte Pins</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V In)</TD><TD PORT="3v3_r">3.3V (Out)</TD></TR>
      <TR><TD PORT="3v3_l">3.3V (Out)</TD><TD PORT="gnd_r">GND (Masse)</TD></TR>
      <TR><TD PORT="gnd_l">GND (Masse)</TD><TD PORT="g4">GPIO 4 (1-Wire)</TD></TR>
      <TR><TD PORT="g23">GPIO 23 (MOSI)</TD><TD PORT="g2">GPIO 2 (Interrupt)</TD></TR>
      <TR><TD PORT="g19">GPIO 19 (MISO)</TD><TD>---</TD></TR>
      <TR><TD PORT="g18">GPIO 18 (SCK)</TD><TD>---</TD></TR>
      <TR><TD PORT="g5">GPIO 5 (CS)</TD><TD>---</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. KOMPONENTEN AUF DER LINKEN SEITE
    dot.node('RC', shape='box', style='filled', fillcolor='#90ee90', label='RC-Empfänger\n(5V Batterie)')
    
    sd_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#d3d3d3"><B>MicroSD (SPI)</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="miso">MISO</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD></TR>
      <TR><TD PORT="sck">SCK</TD></TR>
      <TR><TD PORT="cs">CS</TD></TR>
    </TABLE>>'''
    dot.node('SD', label=sd_html)

    # 3. KOMPONENTEN AUF DER RECHTEN SEITE
    temp_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#ffffe0"><B>DS18B20 Temp.</B></TD></TR>
      <TR><TD PORT="vcc">VDD (Rot)</TD></TR>
      <TR><TD PORT="gnd">GND (Schwarz)</TD></TR>
      <TR><TD PORT="dq">Data (Gelb/Blau)</TD></TR>
    </TABLE>>'''
    dot.node('TEMP', label=temp_html)

    hall_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
      <TR><TD COLSPAN="2" BGCOLOR="#ffb6c1"><B>A3144 Hall-Sensor</B></TD></TR>
      <TR><TD PORT="vcc">1: VCC (Power)</TD></TR>
      <TR><TD PORT="gnd">2: GND (Masse)</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD></TR>
    </TABLE>>'''
    dot.node('HALL', label=hall_html)

    dot.node('RES', shape='box', style='filled', fillcolor='white', label='4.7 kΩ\nPull-Up')

    # --- VERKABELUNG LINKE SEITE (RC & SD) ---
    # Damit Graphviz diese links platziert, ziehen wir die Linie VON der Komponente ZUM ESP.
    # Mit dir="back" drehen wir den Pfeil optisch um, falls er vom ESP zur Komponente fließen soll.
    
    dot.edge('RC', 'ESP:vin', color='red', penwidth='2')
    dot.edge('RC', 'ESP:gnd_l', color='black', penwidth='2')

    # SD Karte an linke Pins des ESP
    dot.edge('SD:vcc', 'ESP:3v3_l', color='red', dir='back')
    dot.edge('SD:gnd', 'ESP:gnd_l', color='black', dir='back')
    dot.edge('SD:mosi', 'ESP:g23', color='blue', dir='back')
    dot.edge('SD:miso', 'ESP:g19', color='blue', dir='forward') # MISO sendet Daten ZUM ESP
    dot.edge('SD:sck', 'ESP:g18', color='blue', dir='back')
    dot.edge('SD:cs', 'ESP:g5', color='blue', dir='back')

    # --- VERKABELUNG RECHTE SEITE (Sensoren) ---
    # Linie vom ESP zu den Sensoren zwingt diese auf die rechte Seite.
    
    dot.edge('ESP:3v3_r', 'TEMP:vcc', color='red')
    dot.edge('ESP:gnd_r', 'TEMP:gnd', color='black')
    dot.edge('ESP:g4', 'TEMP:dq', color='orange')

    dot.edge('ESP:3v3_r', 'HALL:vcc', color='red')
    dot.edge('ESP:gnd_r', 'HALL:gnd', color='black')
    dot.edge('ESP:g2', 'HALL:out', color='purple')

    # Pull-Up Widerstand
    dot.edge('ESP:3v3_r', 'RES', color='red', style='dashed')
    dot.edge('RES', 'ESP:g4', color='orange', style='dashed')

    # Bild rendern
    dot.render(view=False)
    print("Perfekter, aufgeteilter Schaltplan generiert! Bitte öffne 'Schaltplan_Perfekt.png'.")

if __name__ == '__main__':
    erstelle_perfekten_schaltplan()
