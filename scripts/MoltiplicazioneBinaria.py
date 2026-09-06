def main(expr, spaces=1):
    parts = expr.split('x')
    a = int(parts[0].strip())
    b = int(parts[1].strip())

    bin_a = bin(a)[2:]
    
    bin_b = bin(b)[2:]
    bin_s = bin(a * b)[2:]
    
    blen = len(bin_b)
    
    max_len = max(len(bin_a), blen, len(bin_s)) 
    bin_b = bin_b.rjust(max_len)

    print("    " * spaces + "{")
    print("    " * (spaces + 1) + "\\vspace{0.25cm}")
    print("    " * (spaces + 1) + "\\textbf{" + expr + "}")
    print("    " * (spaces + 1))
    print("    " * (spaces + 2) + "\\begin{tabular}{" + "c" * max_len + "l}")
    print("    " * (spaces + 3) + " & ".join(bin_a.rjust(max_len)) + " & * " + "\\\\")
    print("    " * (spaces + 3) + " & ".join(bin_b) + " & = " + "\\\\")
    print("    " * (spaces + 3) + "\\hline")
    
    for i in range(blen):
        if bin_b[- i - 1] == "1":
            print("    " * (spaces + 3) + 
                " & " * (max_len - len(bin_a) - i) +
                " & ".join(bin_a) + 
                " & -" * i + " & " + "\\\\")
        else:
            print("    " * (spaces + 3) + 
                " & " * (max_len - len(bin_a) - i) +
                " & ".join("0" * len(bin_a)) + 
                " & -" * i + " & " + "\\\\")
    
    print("    " * (spaces + 3) + "\\hline")
    print("    " * (spaces + 3) + " & ".join(list(bin_s)) + " & " + "\\\\")
    print("    " * (spaces + 2) + "\\end{tabular}")
    print("    " * spaces + "}")
    print("    " * spaces)

# main("11x21", spaces=2)

import sys

# ha un parametro
if len(sys.argv) >= 2:
    nums = sys.argv[1]
    main(nums, 0)