es = [
    # Difficoltà 1
    [1, "1, 2, 3, 4, 5", "A, B"],
    [1, "insieme dei primi cinque numeri naturali", "A, B"],
    [1, "insieme dei colori primari", "X, Y"],
    [1, "ALFA, BETA, GAMMA", "P, Q"],
    [1, "insieme delle prime tre lettere dell'alfabeto greco", "1, 2"],
    [1, "insieme dei numeri pari minori di 10", "M, N"],
    [1, "A, B, C, D, E", "1, 2"],
    [1, "insieme dei punti cardinali principali", "N, S"],
    [1, "\\rightarrow, \\leftarrow, \\uparrow, \\downarrow", "1, 2"],
    [1, "insieme delle frecce direzionali principali", "A, B"],

    # Difficoltà 2
    [2, "1, 2, 3, 4, 5, 6, 7", "A, B, C"],
    [2, "insieme dei giorni della settimana esclusa domenica", "G, H, I"],
    [2, "insieme dei colori del semaforo", "X, Y, Z"],
    [2, "10, 20, 30, 40, 50, 60", "M, N, O"],
    [2, "insieme delle prime sette lettere dell'alfabeto latino", "1, 2, 3"],
    [2, "\\alpha, \\beta, \\gamma, \\delta, \\varepsilon", "1, 2, 3"],
    [2, "insieme dei primi quattro numeri dispari", "A, B, C"],
    [2, "\\infty, \\emptyset, \\forall", "X, x"],
    [2, "insieme dei multipli di 2 minori di 12", "P, Q"],
    [2, "\\rightarrow, \\leftarrow, \\uparrow, \\downarrow, \\nearrow", "1, 2, 3"],
    [2, "insieme dei simboli logici di base", "A, B, C"],
    [2, "\\infty, \\emptyset, \\forall, \\exists", "X, Y, Z"],
    [2, "insieme dei risultati possibili di un dado", "1, 2, 3"],
    [2, "insieme delle vocali e delle prime due consonanti", "A, B, C"],

    # Difficoltà 3
    [3, "insieme dei colori dell'arcobaleno", "X, Y, Z, W"],
    [3, "insieme delle prime nove lettere dell'alfabeto latino", "1, 2, 3, 4"],
    [3, "\\alpha, \\beta, \\gamma, \\delta, \\varepsilon, \\zeta, \\eta", "1, 2, 3, 4"],
    [3, "insieme dei primi cinque numeri dispari", "A, B, C, D"],
    [3, "insieme dei mesi dell'anno", "X, Y, Z, W"],
    [3, "insieme dei numeri naturali minori di 10", "G, H, I, J"],
    [3, "insieme dei multipli di 3 minori di 25", "P, Q, R, S"],
    [3, "\\rightarrow, \\leftarrow, \\uparrow, \\downarrow, \\nearrow, \\searrow, \\swarrow", "1, 2, 3, 4"],
    [3, "\\infty, \\emptyset, \\forall, \\exists, \\neg, \\wedge", "X, Y, Z, W"],
    [3, "insieme di tutte le lettere dell'alfabeto italiano", "A, B, C, D"],
]

for s in es:
    print("""\\begin{esercizio}[""" + str(s[0]) + """]
    $T = \\{ """ + s[1].replace(' ', '\ ')  + """ \\} $ \\\\
    $E = \\{ """ + s[2]+ """ \\} $
\\end{esercizio}
""")