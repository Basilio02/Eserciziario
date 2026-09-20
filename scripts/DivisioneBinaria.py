def binary_long_division_steps(a, b):
    A = bin(a)[2:]
    B = bin(b)[2:]

    steps = []
    current = ""
    Q = ""

    for i, bit in enumerate(A):
        current += bit
        start = i - (len(current) - 1)  # indice della prima cifra di `current` in A

        if int(current, 2) < b:
            Q += "0"
            steps.append((start, current, None))
        else:
            Q += "1"
            diff_val = int(current, 2) - b
            diff_bin = bin(diff_val)[2:] if diff_val != 0 else "0"
            steps.append((start, current, diff_bin))
            current = diff_bin  # il resto parziale diventa la nuova "current"

    R = current if current != "" else "0"
    return A, B, Q, R, steps

def generateLatex(expr):

    parts = expr.split(':')
    a = int(parts[0].strip())
    b = int(parts[1].strip())


    A, B, Q, R, steps = binary_long_division_steps(a, b)

    la = len(A)
    lb = len(B)
    lq = len(Q)

    # parte sinistra ha tante colonne quante cifre del dividendo
    left_cols = la
    # parte destra avrà colonne pari al massimo tra divisore e quoziente
    right_cols = max(lb, lq)
    lines = []
    lines.append("{")

    lines.append("$" + str(a) + "_{10} = " + str(A).strip() + "_{2} $\\\\")
    lines.append("$" + str(b) + "_{10} = " + str(B).strip() + "_{2} $\\\\")

    lines.append("\\begin{tabular}{" + "c" * left_cols + "|" + "c" * right_cols + "}")

    # --- PRIMA RIGA: dividendo | divisore (divisore right-justified nella parte destra) ---
    left_row = list(A)  # direttamente una cella per cifra del dividendo
    # right: right-justify B in right_cols
    right_row = list(B) + [""] * (right_cols - lb)
    lines.append(" & ".join(left_row) + " & " + " & ".join(right_row) + " \\\\")
    lines.append("\\hline")
    lines.append("\\hline")

    # --- PASSI: per ogni step mostro il blocco corrente e, se sottrazione,
    #     la riga con il divisore allineata allo stesso start ---
    for start, cur, diff in steps:
        # riga con current (posizionato a partire da `start`)
        row = [""] * left_cols
        for j, ch in enumerate(cur):
            pos = start + j
            if 0 <= pos < left_cols:
                row[pos] = ch
        # nella parte destra non mostriamo nulla (è la zona del divisore/quoziente)
        right_empty = [""] * right_cols
        lines.append(" & ".join(row) + " & " + " & ".join(right_empty) + " \\\\")
        # se c'è stata sottrazione, mostro il divisore posizionato sotto lo stesso start
        if diff is not None:
            row_b = [""] * left_cols
            for j, ch in enumerate(B):
                pos = start + j + len(cur) - len(B)
                if 0 <= pos < left_cols:
                    row_b[pos] = ch
            lines.append(" & ".join(row_b) + " & " + " & ".join(right_empty) + " \\\\")
            lines.append("\\hline")

    # --- LINEA FINALE: resto | quoziente
    # resto: right-justify in left_cols
    rest_row = [""] * (left_cols - len(R)) + list(R)
    # quoziente: right-justify in right_cols (così è vicino alla barra)
    quot_row = [""] * (right_cols - len(Q)) + list(Q)
    lines.append("\\hline")
    lines.append(" & ".join(rest_row) + " & " + " & ".join(quot_row) + " \\\\")
    lines.append("\\end{tabular}")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)

def main(expr):
    print(generateLatex(expr))

# main("11:21")

import sys

# ha un parametro
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        nums = sys.argv[1]
        main(nums)
