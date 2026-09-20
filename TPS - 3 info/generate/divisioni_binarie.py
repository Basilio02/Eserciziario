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

divisioni = [
    # Difficoltà 1 (divisioni esatte, numeri piccoli)
    [1, "12 : 3"],
    [1, "20 : 4"],
    [1, "18 : 2"],
    [1, "24 : 6"],
    [1, "30 : 5"],
    [1, "16 : 4"],
    [1, "21 : 7"],
    [1, "28 : 7"],
    [1, "36 : 6"],
    [1, "40 : 8"],
    
    # Difficoltà 2 (divisioni esatte, numeri medi)
    [2, "48 : 6"],
    [2, "56 : 7"],
    [2, "63 : 9"],
    [2, "72 : 8"],
    [2, "84 : 7"],
    [2, "90 : 9"],
    [2, "96 : 8"],
    [2, "108 : 9"],
    [2, "120 : 10"],
    [2, "132 : 11"],
    [2, "144 : 12"],
    [2, "150 : 15"],
    [2, "168 : 12"],
    [2, "192 : 16"],
    
    # Difficoltà 3 (divisioni con resto o numeri più grandi)
    [3, "234 : 13"],
    [3, "276 : 12"],
    [3, "315 : 15"],
    [3, "348 : 12"],
    [3, "390 : 13"],
    [3, "425 : 17"],
    [3, "468 : 18"],
    [3, "504 : 21"],
    [3, "540 : 18"],
    [3, "576 : 24"],
    [3, "612 : 17"],
    [3, "648 : 24"],
    [3, "684 : 19"],
    [3, "756 : 21"]
]


from DivisioneBinaria import generateLatex


if not args.soluzioni:
    print("""\\begin{multicols}{2}
""")

for s in divisioni:
    print("""\\begin{esercizio}[""" + str(s[0]) + """]
    """ + s[1])
    if args.soluzioni:
        print("\\solution")
        print("")
        print(generateLatex(s[1]) + "\n")

    print("""\\end{esercizio}
""")

if not args.soluzioni:
    print("""\\end{multicols}
""")
