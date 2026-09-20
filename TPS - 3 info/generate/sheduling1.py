# Aggiunta dinamica degli scripts
import sys
from pathlib import Path
BATE_DIR = Path(__file__).resolve().parents[2]
TCRIPT_DIR = BATE_DIR / "scripts"
sys.path.insert(0, str(TCRIPT_DIR))

# Gestione del parametro --soluzioni
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--soluzioni", action="store_true")
args = parser.parse_args()

esercizi = [
    # =========================
    # Difficoltà 1
    # Pochi processi, qualche arrivo contemporaneo, differenze FCFS vs SJF/SRTF
    # =========================
    
    # 1. Arrivi contemporanei a t=0, burst diversi → SJF cambia ordine
    [1, """P1,0,6
P2,0,3
P3,0,2"""],
    
    # 2. Due arrivi a t=0, uno a t=1 → SJF migliore di FCFS
    [1, """P1,0,5
P2,0,2
P3,1,3"""],
    
    # 3. Arrivi scalari, ma un processo corto arriva dopo
    [1, """P1,0,6
P2,1,2
P3,2,3"""],
    
    # 4. Tutti arrivi a t=0, burst crescenti → FCFS pessimo, SJF ottimo
    [1, """P1,0,2
P2,0,4
P3,0,6
P4,0,8"""],
    
    # 5. Due processi uguali a t=0, uno corto a t=1
    [1, """P1,0,4
P2,0,4
P3,1,2"""],
    
    # 6. Arrivi a 0 e 1, burst molto diversi → SRTF preemption chiara
    [1, """P1,0,6
P2,1,2
P3,2,3"""],
    
    # 7. Tre processi, due con stesso arrivo, uno corto
    [1, """P1,0,5
P2,0,3
P3,1,2"""],
    
    # 8. Arrivi a 0,1,2 con burst decrescente → SJF/SRTF vantaggiosi
    [1, """P1,0,6
P2,1,4
P3,2,2"""],
    
    # 9. Due processi lunghi a t=0, uno corto a t=1
    [1, """P1,0,5
P2,0,6
P3,1,2"""],
    
    # 10. Quattro processi, due a t=0, due dopo
    [1, """P1,0,4
P2,0,3
P3,1,2
P4,2,3"""],
    
    # =========================
    # Difficoltà 2
    # Più processi, più arrivi contemporanei, situazioni più “subdole”
    # =========================
    
    # 11. Tre processi a t=0, altri due dopo → SJF/SRTF molto diversi da FCFS
    [2, """P1,0,6
P2,0,3
P3,0,2
P4,1,4
P5,2,3"""],
    
    # 12. Due lunghi a t=0, corti in arrivo a 1 e 2 → SRTF preemption multipla
    [2, """P1,0,7
P2,0,6
P3,1,2
P4,2,3"""],
    
    # 13. Arrivi a 0,0,1,1,2 → FCFS vs SJF evidente
    [2, """P1,0,5
P2,0,4
P3,1,2
P4,1,3
P5,2,4"""],
    
    # 14. Processo lungo a t=0, molti corti dopo → SRTF molto efficiente
    [2, """P1,0,8
P2,1,2
P3,2,3
P4,3,2
P5,4,3"""],
    
    # 15. Due “grandi” a t=0, tre medi a t=1,2,3
    [2, """P1,0,7
P2,0,6
P3,1,4
P4,2,3
P5,3,4"""],
    
    # 16. Arrivi a 0,0,0,1,2 → SJF cambia molto l’ordine
    [2, """P1,0,5
P2,0,4
P3,0,3
P4,1,2
P5,2,4"""],
    
    # 17. Processo lungo, poi due corti quasi simultanei
    [2, """P1,0,9
P2,1,2
P3,1,3
P4,3,4"""],
    
    # 18. Quattro processi, due a t=0, due a t=2
    [2, """P1,0,6
P2,0,4
P3,2,2
P4,2,3
P5,3,5"""],
    
    # 19. Tre a t=0, due a t=2, uno a t=4
    [2, """P1,0,5
P2,0,4
P3,0,3
P4,2,2
P5,2,4
P6,4,3"""],
    
    # 20. Lungo a t=0, corti ravvicinati tra 1 e 3
    [2, """P1,0,10
P2,1,2
P3,2,3
P4,3,2
P5,4,4"""],
    
    # 21. Due lunghi a t=0, tre corti a t=1,2,3
    [2, """P1,0,8
P2,0,7
P3,1,2
P4,2,3
P5,3,2"""],
    
    # 22. Tre a t=0, tre a t=2, burst vari
    [2, """P1,0,6
P2,0,4
P3,0,5
P4,2,2
P5,2,3
P6,2,4"""],
    
    # 23. Processo medio a t=0, molti piccoli dopo
    [2, """P1,0,7
P2,1,2
P3,2,2
P4,3,3
P5,4,2
P6,5,3"""],
    
    # 24. Due a t=0, quattro a t=2,3,4
    [2, """P1,0,6
P2,0,5
P3,2,2
P4,3,3
P5,4,2
P6,4,4"""],
    
    # 25. Tre a t=0, tre a t=1,2,3 (burst decrescenti nei secondi)
    [2, """P1,0,6
P2,0,5
P3,0,4
P4,1,3
P5,2,2
P6,3,2"""],
    
    # =========================
    # Difficoltà 3
    # Molti processi, arrivi contemporanei multipli, situazioni “nastie”
    # =========================
    
    # 26. Tre lunghi a t=0, tre corti a t=1,2,3 → SRTF molto diverso
    [3, """P1,0,8
P2,0,7
P3,0,6
P4,1,2
P5,2,3
P6,3,2"""],
    
    # 27. Quattro a t=0, due a t=2, due a t=4
    [3, """P1,0,6
P2,0,5
P3,0,4
P4,0,3
P5,2,2
P6,2,3
P7,4,4
P8,4,2"""],
    
    # 28. Lungo a t=0, molti corti ravvicinati 1–5
    [3, """P1,0,10
P2,1,2
P3,2,2
P4,3,3
P5,4,2
P6,5,3
P7,5,2"""],
    
    # 29. Due lunghi a t=0, quattro corti a t=1,2,3,4
    [3, """P1,0,9
P2,0,8
P3,1,2
P4,2,3
P5,3,2
P6,4,4"""],
    
    # 30. Tre a t=0, tre a t=1, tre a t=3
    [3, """P1,0,7
P2,0,5
P3,0,4
P4,1,3
P5,1,2
P6,1,4
P7,3,2
P8,3,3
P9,3,2"""],
    
    # 31. Quattro a t=0, quattro a t=2, burst molto vari
    [3, """P1,0,8
P2,0,6
P3,0,5
P4,0,4
P5,2,2
P6,2,3
P7,2,4
P8,2,5"""],
    
    # 32. Lungo a t=0, molti corti tra 1 e 6
    [3, """P1,0,12
P2,1,2
P3,2,3
P4,3,2
P5,4,2
P6,5,3
P7,6,2
P8,6,3"""],
    
    # 33. Tre medi a t=0, cinque corti a t=1..5
    [3, """P1,0,7
P2,0,6
P3,0,5
P4,1,2
P5,2,2
P6,3,3
P7,4,2
P8,5,2"""],
    
    # 34. Due lunghi a t=0, sei corti a t=1..6
    [3, """P1,0,10
P2,0,9
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2
P8,6,3"""],
    
    # 35. Quattro a t=0, tre a t=2, tre a t=4
    [3, """P1,0,7
P2,0,6
P3,0,5
P4,0,4
P5,2,2
P6,2,3
P7,2,4
P8,4,2
P9,4,3
P10,4,2"""],
    
    # 36. Tre a t=0, quattro a t=1, tre a t=3
    [3, """P1,0,8
P2,0,6
P3,0,5
P4,1,2
P5,1,3
P6,1,2
P7,1,4
P8,3,2
P9,3,3
P10,3,2"""],
    
    # 37. Due lunghi a t=0, molti corti 1..7
    [3, """P1,0,11
P2,0,10
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2
P8,6,3
P9,7,2"""],
    
    # 38. Quattro a t=0, quattro a t=2, quattro a t=4
    [3, """P1,0,7
P2,0,6
P3,0,5
P4,0,4
P5,2,2
P6,2,3
P7,2,4
P8,2,5
P9,4,2
P10,4,3
P11,4,2
P12,4,4"""],
    
    # 39. Tre a t=0, tre a t=1, tre a t=2, tre a t=4
    [3, """P1,0,7
P2,0,6
P3,0,5
P4,1,3
P5,1,2
P6,1,4
P7,2,2
P8,2,3
P9,2,2
P10,4,3
P11,4,2
P12,4,4"""],
    
    # 40. Lungo a t=0, molti corti 1..8
    [3, """P1,0,12
P2,1,2
P3,2,2
P4,3,3
P5,4,2
P6,5,2
P7,6,3
P8,7,2
P9,8,2"""],
    
    # 41. Due lunghi a t=0, otto corti 1..8
    [3, """P1,0,11
P2,0,10
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2
P8,6,3
P9,7,2
P10,8,2"""],
    
    # 42. Quattro a t=0, sei a t=2, due a t=5
    [3, """P1,0,8
P2,0,7
P3,0,6
P4,0,5
P5,2,2
P6,2,3
P7,2,2
P8,2,4
P9,2,3
P10,2,2
P11,5,3
P12,5,2"""],
    
    # 43. Tre a t=0, cinque a t=1, quattro a t=3
    [3, """P1,0,8
P2,0,7
P3,0,6
P4,1,2
P5,1,2
P6,1,3
P7,1,2
P8,1,4
P9,3,2
P10,3,3
P11,3,2
P12,3,4"""],
    
    # 44. Due lunghi a t=0, dieci corti 1..10
    [3, """P1,0,12
P2,0,11
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2
P8,6,3
P9,7,2
P10,8,2
P11,9,3
P12,10,2"""],
    
    # 45. Quattro a t=0, quattro a t=2, quattro a t=4, quattro a t=6
    [3, """P1,0,7
P2,0,6
P3,0,5
P4,0,4
P5,2,2
P6,2,3
P7,2,4
P8,2,5
P9,4,2
P10,4,3
P11,4,2
P12,4,4
P13,6,3
P14,6,2
P15,6,4
P16,6,2"""],
    
    # 46. Tre a t=0, tre a t=1, tre a t=2, tre a t=3, tre a t=5
    [3, """P1,0,7
P2,0,6
P3,0,5
P4,1,3
P5,1,2
P6,1,4
P7,2,2
P8,2,3
P9,2,2
P10,3,3
P11,3,2
P12,3,4
P13,5,2
P14,5,3
P15,5,2"""],
    
    # 47. Due lunghi a t=0, dodici corti 1..12
    [3, """P1,0,13
P2,0,12
P3,1,2
P4,2,2
P5,3,3
P6,4,2
P7,5,2
P8,6,3
P9,7,2
P10,8,2
P11,9,3
P12,10,2
P13,11,2
P14,12,3"""],
    
    # 48. Quattro a t=0, sei a t=2, sei a t=4
    [3, """P1,0,8
P2,0,7
P3,0,6
P4,0,5
P5,2,2
P6,2,3
P7,2,2
P8,2,4
P9,2,3
P10,2,2
P11,4,2
P12,4,3
P13,4,2
P14,4,4
P15,4,2
P16,4,3"""],
]

import sys
from pathlib import Path

# Aggiungi la cartella "scripts" al path, partendo da questo file
BASE_DIR = Path(__file__).resolve().parents[2]  # torna a project_root
SCRIPT_DIR = BASE_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

# Ora puoi importare ProcessTable
from ProcessTable import generateLatex

for es in esercizi:
    print("""\\begin{esercizio}[""" + str(es[0]) + """]
    """ + generateLatex(es[1]) + """
\\end{esercizio}
""")