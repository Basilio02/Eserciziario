def main(params, spaces):
    BASE = 2
	
    n = int(params)
    orig = n

    passaggi_divisioni = []
    while n > 0:
        q, r = divmod(n, BASE)
        passaggi_divisioni.append((n, q, r))
        n = q

    valore = "".join(str(r) for _, _, r in reversed(passaggi_divisioni))
    print("    " * spaces + "{")
    print("    " * (spaces + 1) + f"${orig}_{{10}} = {valore}_{{{BASE}}}$")
    print("")

    for dividendo, quoziente, resto in passaggi_divisioni:
        print("    " * (spaces + 1) + f"${dividendo} \\div {BASE} = {quoziente}$ con resto ${resto}$")
        print("")
		
    print("    " * spaces + "}")
    print("    " * spaces)
    print("    " * spaces)

import sys

# ha un parametro
if len(sys.argv) >= 2:
    num = int(sys.argv[1])
    main(num, 0)