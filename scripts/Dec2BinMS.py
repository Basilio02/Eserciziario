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

    valore = segno + "\\hspace{0.05cm}" + valore_modulo

    # composizione del risultato
    res = []
    res.append("{")
    res.append(f"${params}_{{10}} = {valore}_2$")

    res.append("")

    for dividendo, quoziente, resto in passaggi_divisioni:
        res.append(f"${dividendo} \\div 2 = {quoziente}$ con resto ${resto}$")
        res.append("")

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