def generateLatex(params):

    n = int(params)
    segno = "1" if n < 0 else "0"
    n = abs(n)  # lavora solo sul modulo

    passaggi_divisioni = []
    while n > 0:
        q, r = divmod(n, 2)
        passaggi_divisioni.append((n, q, r))
        n = q

    valore_modulo = "".join(str(r) for _, _, r in reversed(passaggi_divisioni))

    inv = "".join("1" if b == "0" else "0" for b in valore_modulo)
    nbit = len(inv)
    comp2 = bin(int(inv, 2) + 1)[2:].zfill(nbit)
    comp2 = comp2[-nbit:]

    # composizione del risultato
    res = []
    res.append("{")
    if segno == "1":
        # TO INVERT
        valore = "1 \\hspace{0.05cm}" + comp2
        res.append(f"${params}_{{10}} = {valore}_2$")
    else:
        valore = "0 \\hspace{0.05cm}" + valore_modulo
        res.append(f"${params}_{{10}} = {valore}_2$")

    res.append("")

    for dividendo, quoziente, resto in passaggi_divisioni:
        res.append(f"${dividendo} \\div 2 = {quoziente}$ con resto ${resto}$")
        res.append("")

    if segno == "1":
        res.append(f"${valore_modulo}$")
        res.append("")
        res.append(f"${inv}$")
        res.append("")
        res.append(f"${comp2}$")

    res.append("}")
    res.append("")
    res.append("")
    return "\n".join(res)

def main(params):
    print(generateLatex(params))

import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])