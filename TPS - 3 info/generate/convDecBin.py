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

conversioni = [
    # Difficoltà 1 (facili, numeri fino a 15 -> massimo 4 bit)
    [1, "2"],
    [1, "3"],
    [1, "4"],
    [1, "5"],
    [1, "6"],
    [1, "7"],
    [1, "8"],
    [1, "9"],
    [1, "10"],
    [1, "11"],
    [1, "12"],
    [1, "13"],
    [1, "14"],
    [1, "15"],
    [1, "20"],

    # Difficoltà 2 (media, numeri da 16 a 127 -> da 5 a 7 bit)
    [2, "18"],
    [2, "23"],
    [2, "35"],
    [2, "41"],
    [2, "52"],
    [2, "58"],
    [2, "67"],
    [2, "74"],
    [2, "77"],
    [2, "89"],
    [2, "96"],
    [2, "100"],
    [2, "111"],
    [2, "120"],
    [2, "127"],

    # Difficoltà 3 (difficili, numeri da 128 a 255 -> 8 bit)
    [3, "128"],
    [3, "141"],
    [3, "156"],
    [3, "164"],
    [3, "173"],
    [3, "176"],
    [3, "187"],
    [3, "199"],
    [3, "212"],
    [3, "219"],
    [3, "233"],
    [3, "240"],
    [3, "246"],
    [3, "250"],
    [3, "255"]
]

from Dec2Bin import generateLatex

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
