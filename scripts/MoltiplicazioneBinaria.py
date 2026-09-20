def generateLatex(expr):
    parts = expr.split('x')
    a = int(parts[0].strip())
    b = int(parts[1].strip())

    bin_a = bin(a)[2:]

    bin_b = bin(b)[2:]
    bin_s = bin(a * b)[2:]

    blen = len(bin_b)

    max_len = max(len(bin_a), blen, len(bin_s))
    bin_b = bin_b.rjust(max_len)

    res = []
    res.append("{")
    res.append("$" + str(a) + "_{10} = " + str(bin_a).strip() + "_{2} $\\\\")
    res.append("$" + str(b) + "_{10} = " + str(bin_b).strip() + "_{2} $\\\\")
    res.append("")
    res.append("\\begin{tabular}{" + "c" * max_len + "l}")
    res.append(" & ".join(bin_a.rjust(max_len)) + " & * " + "\\\\")
    res.append(" & ".join(bin_b) + " & = " + "\\\\")
    res.append("\\hline")

    for i in range(blen):
        if bin_b[- i - 1] == "1":
            res.append(" & " * (max_len - len(bin_a) - i) +
                " & ".join(bin_a) +
                " & -" * i + " & " + "\\\\")
        else:
            res.append(" & " * (max_len - len(bin_a) - i) +
                " & ".join("0" * len(bin_a)) +
                " & -" * i + " & " + "\\\\")

    res.append("\\hline")
    res.append(" & ".join(list(bin_s)) + " & " + "\\\\")
    res.append("\\end{tabular}")
    res.append("}")
    res.append("")

    return "\n".join(res)

def main(expr):
    print(generateLatex(expr))

# main("11x21")

import sys

# ha un parametro
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        nums = sys.argv[1]
        main(nums)
