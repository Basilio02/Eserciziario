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

# Rappresentazione dei numeri interi in modulo e segno
conversioni = [
    # Difficolta 1 (numeri piccoli, pochi bit)
    [1, "2"],
    [1, "-3"],
    [1, "-5"],
    [1, "7"],
    [1, "-6"],
    [1, "8"],
    [1, "-11"],
    [1, "-15"],
    [1, "14"],

    # Difficolta 2 (numeri fino a 127)
    [2, "16"],
    [2, "-27"],
    [2, "45"],
    [2, "-58"],
    [2, "64"],
    [2, "-77"],
    [2, "100"],
    [2, "-111"],
    [2, "-96"],

    # Difficolta 3 (numeri a 8 bit e oltre)
    [3, "128"],
    [3, "-164"],
    [3, "187"],
    [3, "-212"],
    [3, "233"],
    [3, "-246"],
    [3, "240"],
    [3, "-255"],
    [3, "199"],
    [3, "-141"]
]

from Dec2BinMS import generateLatex

if not args.soluzioni:
    print("""\\begin{multicols}{2}
""")

for s in conversioni:
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
