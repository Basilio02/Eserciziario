def generateLatex(params):
    BASE = 2

    bits = str(params).strip().replace(" ", "")
    if bits.lower().startswith("0b"):
        bits = bits[2:]

    orig = bits
    n = len(bits)

    passaggi_potenze = []
    for i, bit in enumerate(bits):
        esponente = n - 1 - i
        valore = int(bit) * (BASE ** esponente)
        passaggi_potenze.append((bit, esponente, valore))

    totale = sum(valore for _, _, valore in passaggi_potenze)

    res = []
    res.append("{")
    res.append(f"${orig}_{{{BASE}}} = {totale}_{{10}}$")
    res.append("")

    for bit, esponente, valore in passaggi_potenze:
        res.append(f"${bit} \\cdot {BASE}^{{{esponente}}} = {valore}$")
        res.append("")

    somma = " + ".join(str(valore) for _, _, valore in passaggi_potenze)
    res.append(f"${somma} = {totale}$")
    res.append("")
    res.append("}")
    res.append("")
    res.append("")
    return "\n".join(res)

def main(params, spaces):
    print(generateLatex(params))

import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        num = sys.argv[1]
        main(num, 0)
