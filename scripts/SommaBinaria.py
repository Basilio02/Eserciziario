def main(expr, spaces=1):
    parts = expr.split('+')
    a = int(parts[0].strip())
    b = int(parts[1].strip())

    bin_a = bin(a)[2:]
    bin_b = bin(b)[2:]
    bin_s = bin(a + b)[2:]

    max_len = max(len(bin_a), len(bin_b), len(bin_s)) 
    bin_a = bin_a.rjust(max_len)
    bin_b = bin_b.rjust(max_len)

    carry = 0
    result = []
    carry_line = []

    for i in range(max_len - 1, -1, -1):
        bit_a = int(bin_a[i]) if bin_a[i] != " " else 0
        bit_b = int(bin_b[i]) if bin_b[i] != " " else 0
        s = bit_a + bit_b + carry

        result_bit = s % 2
        carry = s // 2

        result.insert(0, str(result_bit))
        
        carry_line.insert(0, str(carry) if carry > 0 else " ")

    if carry:
        carry_line.insert(0, "1")
        bin_a = " " + bin_a
        bin_b = " " + bin_b
        result.insert(0, " ")

    print("    " * spaces + "{")
    print("    " * (spaces + 1) + "\\vspace{0.25cm}")
    print("    " * (spaces + 1) + "\\textbf{" + expr + "}")
    print("    " * (spaces + 1))
    print("    " * (spaces + 2) + "\\begin{tabular}{" + "c" * max_len + "l}")
    print("    " * (spaces + 3) + " & ".join(carry_line[1:]) + " & & carry" + "\\\\")
    print("    " * (spaces + 3) + " & ".join(bin_a) + " & + " + "\\\\")
    print("    " * (spaces + 3) + " & ".join(bin_b) + " & = " + "\\\\")
    print("    " * (spaces + 3) + "\\hline")
    print("    " * (spaces + 3) + " & ".join(result) + " & " + "\\\\")
    print("    " * (spaces + 2) + "\\end{tabular}")
    print("    " * spaces + "}")
    print("    " * spaces)

#main("11+21", spaces=2)

import sys

# ha un parametro
if len(sys.argv) >= 2:
    nums = sys.argv[1]
    main(nums, 0)