esercizi_partizioni = [
    # =========================
    # Difficoltà 1
    # Poche partizioni, poche operazioni
    # =========================
    
    [1, """BF,3,T;
200,300,400;
P1,0
P2,1;
P3,150
P4,250
P1,FREE
P5,180
"""],
    
    [1, """FF,3,T;
200,300,400;
P1,0
P2,2;
P3,180
P1,FREE
P4,190
"""],
    
    [1, """WF,3,T;
200,300,400;
P2,1
P3,2;
P1,150
P4,250
P2,FREE
"""],
    
    [1, """BF,4,T;
100,200,300,400;
P1,0
P2,2;
P3,150
P4,250
P1,FREE
P5,90
"""],
    
    [1, """FF,4,T;
100,200,300,400;
P1,1
P2,3;
P3,180
P4,90
P2,FREE
P5,190
"""],
    
    
    # =========================
    # Difficoltà 2
    # Più partizioni, più operazioni, qualche FREE strategico
    # =========================
    
    [2, """BF,4,T;
200,300,400,500;
P1,0
P2,2
P3,3;
P4,180
P5,250
P1,FREE
P6,190
P2,FREE
P7,280
"""],
    
    [2, """FF,4,T;
200,300,400,500;
P1,1
P2,2
P3,3;
P4,150
P5,250
P1,FREE
P6,190
P3,FREE
P7,350
"""],
    
    [2, """WF,4,T;
200,300,400,500;
P1,0
P2,1
P3,3;
P4,200
P5,300
P2,FREE
P6,250
P1,FREE
P7,450
"""],
    
    [2, """BF,5,T;
100,200,300,400,500;
P1,0
P2,2
P3,4;
P4,150
P5,250
P1,FREE
P6,180
P3,FREE
P7,350
"""],
    
    [2, """FF,5,T;
100,200,300,400,500;
P1,1
P2,2
P3,3
P4,4;
P5,180
P6,250
P2,FREE
P7,190
P4,FREE
P8,380
"""],
    
    [2, """WF,5,T;
100,200,300,400,500;
P1,0
P2,1
P3,3
P4,4;
P5,150
P6,250
P1,FREE
P7,280
P3,FREE
P8,450
"""],
    
    # =========================
    # Difficoltà 3
    # Più partizioni, più processi, sequenze più “nastie”
    # =========================
    
    [3, """BF,5,T;
200,300,400,500,600;
P1,0
P2,1
P3,3
P4,4;
P5,180
P6,250
P7,350
P1,FREE
P8,280
P3,FREE
P9,480
P2,FREE
P10,190
"""],
    
    [3, """FF,5,T;
200,300,400,500,600;
P1,0
P2,2
P3,3
P4,4;
P5,150
P6,250
P7,350
P2,FREE
P8,280
P4,FREE
P9,450
P1,FREE
P10,190
"""],
    
    [3, """WF,5,T;
200,300,400,500,600;
P1,1
P2,2
P3,3
P4,4;
P5,200
P6,300
P7,400
P1,FREE
P8,250
P3,FREE
P9,550
P2,FREE
P10,350
"""],
    
    [3, """BF,6,T;
100,200,300,400,500,600;
P1,0
P2,2
P3,3
P4,5;
P5,150
P6,250
P7,350
P8,450
P1,FREE
P9,180
P3,FREE
P10,380
P2,FREE
P11,280
"""],
    
    [3, """FF,6,T;
100,200,300,400,500,600;
P1,1
P2,2
P3,4
P4,5;
P5,180
P6,280
P7,380
P8,480
P2,FREE
P9,190
P4,FREE
P10,450
P1,FREE
P11,90
"""],
    
    [3, """WF,6,T;
100,200,300,400,500,600;
P1,0
P2,1
P3,3
P4,4
P5,5;
P6,150
P7,250
P8,350
P9,450
P1,FREE
P10,280
P3,FREE
P11,550
P5,FREE
P12,580
"""]
]

import sys
from pathlib import Path

# Aggiungi la cartella "scripts" al path, partendo da questo file
BASE_DIR = Path(__file__).resolve().parents[2]  # torna a project_root
SCRIPT_DIR = BASE_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

# Ora puoi importare ProcessTable
from AllocPartFiss import generateLatex

for es in esercizi_partizioni:
    print("""\\begin{esercizio}[""" + str(es[0]) + """]
    """ + generateLatex(es[1]) + """
\\end{esercizio}
""")