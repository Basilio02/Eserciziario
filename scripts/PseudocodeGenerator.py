def latex_listing_escape(text: str) -> str:
    return f"""\\begin{{lstlisting}}[
    style=pseudocodice
]
{text}
\\end{{lstlisting}}"""

# Parole chiave che aprono un blocco e fanno aumentare l'identazione.
BLOCK_OPENERS = ('IF', 'ELSE', 'FOR', 'WHILE', 'DO')

# Associazione fra la riga di chiusura e la parola chiave che apre il blocco.
BLOCK_CLOSERS = {
    'END IF': 'IF',
    'END FOR': 'FOR',
    'END WHILE': 'WHILE',
    'END DO': 'DO',
}

# Righe di servizio del pseudocodice che non devono comparire in output.
SKIPPED_LINES = ('TRUE', 'END TRUE', 'FALSE', 'END FALSE', 'END IF', 'END FOR', 'END WHILE')

# Marcatori dei rami di un IF: non aprono e non chiudono blocchi.
BRANCH_MARKERS = ('TRUE', 'END TRUE', 'FALSE', 'END FALSE')


def _pop_block(block_stack, stripped):
    """
    Toglie dalla pila il blocco chiuso dalla riga corrente.

    La chiusura viene applicata solo se coerente con il blocco aperto in cima
    alla pila, così le righe TRUE/FALSE (che non aprono blocchi reali) non
    possono alterare la pila stessa.
    """
    keyword = BLOCK_CLOSERS.get(stripped)
    if keyword is None or not block_stack:
        return
    if block_stack[-1] == keyword or (keyword == 'WHILE' and block_stack[-1] == 'DO'):
        block_stack.pop()


def _while_opens_loop(lines, index):
    """
    Indica se il WHILE alla riga `index` apre un ciclo vero, cioè chiuso da END WHILE.

    Un ciclo WHILE è sempre terminato da END WHILE, mentre il WHILE che chiude
    un DO-WHILE non ha alcuna riga di chiusura: si scorrono quindi le righe
    successive per verificare se il WHILE incontrato apre davvero un blocco.
    """
    level = 1  # il WHILE in esame è il blocco più interno
    for line in lines[index + 1:]:
        stripped = line.strip()
        if not stripped or stripped in BRANCH_MARKERS:
            continue  # i rami TRUE/FALSE non aprono né chiudono blocchi
        if stripped.startswith('END'):
            level -= 1
            if level == 0:
                # il blocco è stato chiuso: è davvero il WHILE in esame?
                return stripped == 'END WHILE'
        elif stripped.startswith('ELSE'):
            continue  # ELSE chiude un ramo IF e ne apre subito un altro
        elif stripped.startswith(BLOCK_OPENERS):
            level += 1
    return False


def preprocess_code(code: str) -> str:
    lines = code.split('\n')
    result = []
    indent_level = 0
    indent_size = 4
    # Pila dei blocchi aperti: serve a riconoscere il WHILE che chiude un DO-WHILE
    block_stack = []

    for index, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith('END') or stripped.startswith('ELSE'):
            indent_level = max(0, indent_level - 1)
            _pop_block(block_stack, stripped)

        if stripped in SKIPPED_LINES:
            continue

        if stripped.startswith('PROCESS'):
            stripped = stripped[8:]

        # Il WHILE che termina un DO-WHILE non apre un nuovo blocco: va
        # allineato al DO che lo ha aperto e non aumenta l'identazione.
        closes_do_while = (
            stripped.startswith('WHILE')
            and bool(block_stack)
            and block_stack[-1] == 'DO'
            and not _while_opens_loop(lines, index)
        )
        if closes_do_while:
            indent_level = max(0, indent_level - 1)
            block_stack.pop()

        if stripped:
            result.append(' ' * (indent_level * indent_size) + stripped)

        if closes_do_while:
            continue

        for keyword in BLOCK_OPENERS:
            if stripped.startswith(keyword):
                block_stack.append(keyword)
                indent_level += 1
                break
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