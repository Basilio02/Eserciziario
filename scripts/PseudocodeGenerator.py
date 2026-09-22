def latex_listing_escape(text: str) -> str:
    return f"""\\begin{{lstlisting}}[
    style=pseudocodice
]
{text}
\\end{{lstlisting}}"""

def preprocess_code(code: str) -> str:
    lines = code.split('\n')
    result = []
    indent_level = 0
    indent_size = 4
    
    for line in lines:
        stripped = line.strip()

        if stripped.startswith('END') or stripped.startswith('ELSE'):
            indent_level = max(0, indent_level - 1)
        
        if stripped in ('TRUE', 'END TRUE', 'FALSE', 'END FALSE', 'END IF', 'END FOR', 'END WHILE'):
            continue

        if stripped.startswith('PROCESS'):
            stripped = stripped[8:]
        
        if stripped:
            result.append(' ' * (indent_level * indent_size) + stripped)
        
        if any(stripped.startswith(kw) for kw in ('IF', 'ELSE', 'FOR', 'WHILE', 'DO')):
            indent_level += 1
    return '\n'.join(result)

def generatePseudocodeLatex(code):
    processed = preprocess_code(code)
    return latex_listing_escape(processed.strip())

def main(code):
    print(generatePseudocodeLatex(code))

# main("""
# DECLARE Integer i, j, n
# INPUT Leggi n
# PROCESS j <- 0
# FOR i = 0 ; i < n ; i = i + 1
#     IF i mod 2 = 0
#         TRUE
#             WHILE j < i
#                 PROCESS Elabora j
#                 PROCESS j <- j + 1
#             END WHILE
#             OUTPUT Numero pari
#         END TRUE
#         FALSE
#             OUTPUT Numero dispari
#         END FALSE
#     END IF
#     DO
#         PROCESS Aggiorna valore
#     WHILE valore != 0
# END FOR
# OUTPUT Fine algoritmo
# """)

import sys
import argparse

def read_algorithm(args):
    """
    Legge l'algoritmo:
    - da file se è stata usata l'opzione -f;
    - direttamente dalla riga di comando altrimenti.
    """
    if args.file:
        try:
            with open(args.input, "r", encoding="utf-8") as file:
                return file.read()
        except OSError as error:
            raise SystemExit(
            f"Errore nell'apertura del file '{args.input}': {error}"
        )
    return args.input


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Genera codice LaTeX per un flow chart."
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="interpreta l'argomento input come nome di file"
    )
    parser.add_argument(
        "input",
        help="algoritmo da elaborare oppure nome del file se si usa -f"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    algorithm = read_algorithm(args)
    main(algorithm)