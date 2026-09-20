def generateLatex(expr):
    parts = expr.split('-')
    a = int(parts[0].strip())
    b = int(parts[1].strip())

    bin_a = bin(a)[2:]
    bin_b = bin(b)[2:]
    bin_s = bin(a - b)[2:]

    max_len = max(len(bin_a), len(bin_b))
    bin_a = bin_a.zfill(max_len)
    bin_b = bin_b.zfill(max_len)
    bin_s = bin_s.rjust(max_len)

    real_a = [""] * len(bin_a)
    carry_line = [""] * max_len
    carry = 0

    for i in range(max_len - 1, -1, -1):
        bit_a = int(bin_a[i])
        bit_b = int(bin_b[i])

        if bit_a >= bit_b + carry:

            real_a[i] =  bin_a[i]
        else:
            carry = 1
            carry_line[i - 1] = "1"
            real_a[i] = "$_{1}" + bin_a[i] + "$"


    res = []
    res.append("{")
    res.append("$" + str(a) + "_{10} = " + str(bin_a).strip() + "_{2} $\\\\")
    res.append("$" + str(b) + "_{10} = " + str(bin_b).strip() + "_{2} $\\\\")
    res.append("")
    res.append("\\begin{tabular}{" + "c" * max_len + "l}")
    res.append(" & ".join(real_a) + " & - " + "\\\\")
    res.append(" & ".join(carry_line) + " & prestito" + "\\\\")
    res.append(" & ".join(bin_b) + " & = " + "\\\\")
    res.append("\\hline")
    res.append(" & ".join(bin_s) + " & " + "\\\\")
    res.append("\\end{tabular}")
    res.append("}")
    res.append("")

    return "\n".join(res)

def main(expr):
    print(generateLatex(expr))

#main("8-7")

import sys

# ha un parametro
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        nums = sys.argv[1]
        main(nums)
