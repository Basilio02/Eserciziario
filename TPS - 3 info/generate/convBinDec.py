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
    # Difficoltà 1 (facili, numeri da 2 a 4 bit)
    [1, "10"],
    [1, "11"],
    [1, "100"],
    [1, "101"],
    [1, "110"],
    [1, "111"],
    [1, "1000"],
    [1, "1001"],
    [1, "1010"],
    [1, "1011"],
    [1, "1100"],
    [1, "1101"],
    [1, "1110"],
    [1, "1111"],

    # Difficoltà 2 (media, numeri da 5 a 6 bit)
    [2, "10000"],
    [2, "10001"],
    [2, "10011"],
    [2, "10101"],
    [2, "10110"],
    [2, "11000"],
    [2, "11010"],
    [2, "11100"],
    [2, "11111"],
    [2, "100000"],
    [2, "100101"],
    [2, "101010"],
    [2, "101101"],
    [2, "110011"],
    [2, "111000"],

    # Difficoltà 3 (difficili, numeri da 7 a 8 bit)
    [3, "1000000"],
    [3, "1010101"],
    [3, "1011010"],
    [3, "1100110"],
    [3, "1101101"],
    [3, "1110111"],
    [3, "1111000"],
    [3, "10000001"],
    [3, "10011001"],
    [3, "10101010"],
    [3, "10110011"],
    [3, "11001100"],
    [3, "11010101"],
    [3, "11100011"],
    [3, "11110000"],
    [3, "11111111"]
]

from Bin2Dec import generateLatex

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
