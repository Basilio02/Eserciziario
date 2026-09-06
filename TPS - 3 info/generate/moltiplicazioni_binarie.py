moltiplicazioni = [
    # Difficoltà 1 (tabelline e prodotti semplici)
    [1, "3 x 4"],
    [1, "5 x 6"],
    [1, "7 x 8"],
    [1, "9 x 2"],
    [1, "6 x 7"],
    [1, "8 x 5"],
    [1, "4 x 9"],
    [1, "10 x 3"],
    [1, "11 x 2"],
    [1, "12 x 4"],
    
    # Difficoltà 2 (prodotti a due cifre, senza o con riporto leggero)
    [2, "13 x 4"],
    [2, "15 x 6"],
    [2, "18 x 5"],
    [2, "22 x 3"],
    [2, "24 x 4"],
    [2, "16 x 7"],
    [2, "19 x 5"],
    [2, "21 x 6"],
    [2, "25 x 4"],
    [2, "28 x 3"],
    [2, "14 x 8"],
    [2, "17 x 6"],
    [2, "23 x 5"],
    [2, "26 x 4"],
    
    # Difficoltà 3 (prodotti più grandi, doppi riporti)
    [3, "34 x 12"],
    [3, "45 x 13"],
    [3, "56 x 14"],
    [3, "67 x 15"],
    [3, "78 x 12"],
    [3, "89 x 11"],
    [3, "92 x 13"],
    [3, "84 x 16"],
    [3, "73 x 18"],
    [3, "65 x 19"],
    [3, "58 x 17"],
    [3, "49 x 21"],
    [3, "37 x 24"],
    [3, "46 x 22"]
]

for s in moltiplicazioni:
    print("""\\begin{esercizio}[""" + str(s[0]) + """]
    """ + s[1] + """
\\end{esercizio}
""")