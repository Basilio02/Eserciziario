esercizi_partizioni = [
    # =========================
    # Difficoltà 1
    # Memoria piccola, pochi processi, poche operazioni
    # =========================
    
    [1, """FF,300,T;
P1,0,100
P2,100,200;
P3,50
P1,FREE
P4,80
"""],
    
    [1, """BF,300,T;
P1,0,150
P2,150,250;
P3,40
P2,FREE
P4,90
"""],
    
    [1, """WF,300,T;
P1,50,200
P2,200,300;
P3,30
P1,FREE
P4,120
"""],
    
    [1, """FF,400,T;
P1,0,100
P2,200,300;
P3,50
P4,80
P1,FREE
P5,90
"""],
    
    [1, """BF,400,T;
P1,0,150
P2,250,350;
P3,40
P4,60
P2,FREE
P5,80
"""],
    
    [1, """WF,400,T;
P1,50,250
P2,300,400;
P3,30
P4,50
P1,FREE
P5,150
"""],
    
    # =========================
    # Difficoltà 2
    # Memoria media, più processi, più operazioni e FREE strategici
    # =========================
    
    [2, """FF,500,T;
P1,0,100
P2,100,250
P3,250,350;
P4,50
P5,80
P1,FREE
P6,120
P2,FREE
P7,140
"""],
    
    [2, """BF,500,T;
P1,0,150
P2,150,300
P3,350,450;
P4,40
P5,60
P2,FREE
P6,130
P3,FREE
P7,90
"""],
    
    [2, """WF,500,T;
P1,50,200
P2,200,350
P3,400,500;
P4,30
P5,50
P1,FREE
P6,140
P3,FREE
P7,80
"""],
    
    [2, """FF,600,T;
P1,0,100
P2,100,250
P3,300,450
P4,450,550;
P5,40
P6,60
P1,FREE
P7,120
P3,FREE
P8,140
"""],
    
    [2, """BF,600,T;
P1,0,150
P2,200,350
P3,400,500
P4,500,600;
P5,30
P6,50
P2,FREE
P7,130
P4,FREE
P8,90
"""],
    
    [2, """WF,600,T;
P1,50,200
P2,250,400
P3,450,550
P4,550,600;
P5,40
P6,60
P1,FREE
P7,140
P3,FREE
P8,80
"""],
    
    [2, """FF,700,T;
P1,0,150
P2,150,300
P3,350,500
P4,500,650;
P5,50
P6,70
P1,FREE
P7,130
P3,FREE
P8,140
P2,FREE
P9,120
"""],
    
    # =========================
    # Difficoltà 3
    # Memoria grande, molti processi, sequenze più “nastie” e frammentazione
    # =========================
    
    [3, """FF,800,T;
P1,0,100
P2,100,250
P3,250,400
P4,450,600
P5,600,750;
P6,40
P7,60
P8,50
P1,FREE
P9,120
P3,FREE
P10,140
P5,FREE
P11,130
"""],
    
    [3, """BF,800,T;
P1,0,150
P2,150,300
P3,350,500
P4,500,650
P5,700,800;
P6,30
P7,50
P8,40
P2,FREE
P9,130
P4,FREE
P10,140
P1,FREE
P11,120
"""],
    
    [3, """WF,800,T;
P1,50,200
P2,200,350
P3,400,550
P4,550,700
P5,750,800;
P6,40
P7,60
P8,50
P1,FREE
P9,140
P3,FREE
P10,130
P5,FREE
P11,80
"""],
    
    [3, """FF,900,T;
P1,0,100
P2,100,250
P3,250,400
P4,450,600
P5,600,750
P6,750,900;
P7,40
P8,60
P9,50
P1,FREE
P10,120
P3,FREE
P11,140
P5,FREE
P12,130
P2,FREE
P13,110
"""],
    
    [3, """BF,900,T;
P1,0,150
P2,150,300
P3,350,500
P4,500,650
P5,700,850
P6,850,900;
P7,30
P8,50
P9,40
P2,FREE
P10,130
P4,FREE
P11,140
P1,FREE
P12,120
P5,FREE
P13,100
"""],
    
    [3, """WF,900,T;
P1,50,200
P2,200,350
P3,400,550
P4,550,700
P5,750,850
P6,850,900;
P7,40
P8,60
P9,50
P1,FREE
P10,140
P3,FREE
P11,130
P5,FREE
P12,80
P2,FREE
P13,120
"""],
    
    [3, """FF,1000,T;
P1,0,150
P2,150,300
P3,300,450
P4,500,650
P5,650,800
P6,800,950;
P7,50
P8,70
P9,60
P1,FREE
P10,130
P3,FREE
P11,140
P5,FREE
P12,130
P2,FREE
P13,120
P4,FREE
P14,110
"""]
]

import sys
from pathlib import Path

# Aggiungi la cartella "scripts" al path, partendo da questo file
BATE_DIR = Path(__file__).resolve().parents[2]  # torna a project_root
TCRIPT_DIR = BATE_DIR / "scripts"
sys.path.insert(0, str(TCRIPT_DIR))

# Ora puoi importare ProcessTable
from AllocPartDinam import generateLatex

for es in esercizi_partizioni:
    print("""\\begin{esercizio}[""" + str(es[0]) + """]
    """ + generateLatex(es[1]) + """
\\end{esercizio}
""")