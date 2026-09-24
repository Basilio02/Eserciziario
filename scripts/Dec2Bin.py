def generateLatex(params):
    BASE = 2
        
    n = int(params)
    orig = n

    passaggi_divisioni = []
    while n > 0:
        q, r = divmod(n, BASE)
        passaggi_divisioni.append((n, q, r))
        n = q

    valore = "".join(str(r) for _, _, r in reversed(passaggi_divisioni))
    res = []
    res.append("{")
    res.append(f"${orig}_{{10}} = {valore}_{{{BASE}}}$")
    res.append("")

    for dividendo, quoziente, resto in passaggi_divisioni:
        res.append(f"${dividendo} \\div {BASE} = {quoziente}$ con resto ${resto}$")
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
        num = int(sys.argv[1])
        main(num, 0)