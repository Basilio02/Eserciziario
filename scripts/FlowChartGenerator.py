from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# ============================================================
# AST
# ============================================================

@dataclass
class Declare:
    text: str

@dataclass
class Input:
    text: str

@dataclass
class Output:
    text: str

@dataclass
class Process:
    text: str

@dataclass
class If:
    condition: str
    true_branch: list[object] = field(default_factory=list)
    false_branch: list[object] = field(default_factory=list)

@dataclass
class While:
    condition: str
    body: list[object] = field(default_factory=list)

@dataclass
class DoWhile:
    condition: str
    body: list[object] = field(default_factory=list)

@dataclass
class For:
    init: str
    condition: str
    increment: str
    body: list[object] = field(default_factory=list)

class ParseError(ValueError):
    pass

# ============================================================
# PARSER
# ============================================================

def clean_lines(source: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for line_no, raw in enumerate(source.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        lines.append((line_no, line))
    return lines


def parse_algorithm(source: str) -> list[object]:
    lines = clean_lines(source)
    root: list[object] = []

    # Ogni elemento dello stack rappresenta un blocco aperto.
    # target e' la lista AST in cui aggiungere la prossima istruzione.
    stack: list[dict] = [
        {"kind": "ROOT", "target": root, "line": 0}
    ]

    def current_target(line_no: int) -> list[object]:
        target = stack[-1].get("target")
        if target is None:
            raise ParseError(
                f"Riga {line_no}: istruzione fuori da TRUE/FALSE. "
                "Dopo IF devi aprire TRUE oppure FALSE."
            )
        return target

    def fail(line_no: int, message: str) -> None:
        raise ParseError(f"Riga {line_no}: {message}")

    for line_no, line in lines:
        upper = line.upper()

        # ----------------------------------------------------
        # CHIUSURE: vanno controllate prima delle aperture.
        # In particolare END FOR non deve essere scambiato per
        # una riga ordinaria del corpo di un FOR.
        # ----------------------------------------------------
        if upper == "END IF":
            if stack[-1]["kind"] != "IF":
                fail(line_no, "END IF senza un IF aperto.")
            node: If = stack[-1]["node"]
            if not node.true_branch or not node.false_branch:
                fail(line_no, "IF richiede entrambi i rami TRUE e FALSE non vuoti.")
            stack.pop()
            continue

        if upper == "END WHILE":
            if stack[-1]["kind"] != "WHILE":
                fail(line_no, "END WHILE senza un WHILE aperto.")
            node: While = stack[-1]["node"]
            if not node.body:
                fail(line_no, "Il corpo di WHILE non può essere vuoto.")
            stack.pop()
            continue

        if upper == "END FOR":
            if stack[-1]["kind"] != "FOR":
                fail(
                    line_no,
                    f"END FOR senza un FOR aperto: blocco corrente = {stack[-1]['kind']}."
                )
            node: For = stack[-1]["node"]
            if not node.body:
                fail(line_no, "Il corpo di FOR non può essere vuoto.")
            stack.pop()
            continue

        if upper == "END TRUE" or upper == "END FALSE":
            if stack[-1]["kind"] != "IF":
                fail(line_no, f"{upper} senza un IF aperto.")
            stack[-1]["target"] = None
            stack[-1]["branch_open"] = None
            continue

        # ----------------------------------------------------
        # DO-WHILE: questa verifica DEVE venire prima del WHILE
        # normale, altrimenti 'WHILE valore != 0' aprirebbe un
        # WHILE invece di chiudere il DO.
        # ----------------------------------------------------
        if upper.startswith("WHILE ") and stack[-1]["kind"] == "DO":
            node: DoWhile = stack[-1]["node"]
            condition = line[6:].strip()
            if not condition:
                fail(line_no, "La riga WHILE finale di DO richiede una condizione.")
            if not node.body:
                fail(line_no, "Il corpo di DO non può essere vuoto.")
            node.condition = condition
            stack.pop()
            continue

        # ----------------------------------------------------
        # RAMI DELL'IF
        # ----------------------------------------------------
        if upper == "TRUE":
            if stack[-1]["kind"] != "IF":
                fail(line_no, "TRUE deve trovarsi direttamente dentro un IF.")
            if stack[-1].get("branch_open") is not None:
                fail(line_no, "Chiudi il ramo precedente con END TRUE o END FALSE.")
            node: If = stack[-1]["node"]
            stack[-1]["target"] = node.true_branch
            stack[-1]["branch_open"] = "TRUE"
            continue

        if upper == "FALSE":
            if stack[-1]["kind"] != "IF":
                fail(line_no, "FALSE deve trovarsi direttamente dentro un IF.")
            if stack[-1].get("branch_open") is not None:
                fail(line_no, "Chiudi il ramo precedente con END TRUE o END FALSE.")
            node: If = stack[-1]["node"]
            stack[-1]["target"] = node.false_branch
            stack[-1]["branch_open"] = "FALSE"
            continue

        # ----------------------------------------------------
        # ISTRUZIONI SEMPLICI
        # ----------------------------------------------------
        if upper.startswith("DECLARE "):
            current_target(line_no).append(Declare(line[8:].strip()))
            continue

        if upper.startswith("INPUT "):
            current_target(line_no).append(Input(line[6:].strip()))
            continue

        if upper.startswith("OUTPUT "):
            current_target(line_no).append(Output(line[7:].strip()))
            continue

        if upper.startswith("PROCESS "):
            current_target(line_no).append(Process(line[8:].strip()))
            continue

        # ----------------------------------------------------
        # APERTURE DI BLOCCHI
        # ----------------------------------------------------
        if upper.startswith("IF "):
            condition = line[3:].strip()
            if not condition:
                fail(line_no, "IF richiede una condizione.")
            node = If(condition)
            current_target(line_no).append(node)
            stack.append({
                "kind": "IF",
                "node": node,
                "target": None,
                "branch_open": None,
                "line": line_no,
            })
            continue

        if upper.startswith("FOR "):
            parts = [part.strip() for part in line[4:].split(";")]
            if len(parts) != 3 or not all(parts):
                fail(line_no, "FOR richiede: FOR init ; condizione ; incremento")
            node = For(parts[0], parts[1], parts[2])
            current_target(line_no).append(node)
            stack.append({
                "kind": "FOR",
                "node": node,
                "target": node.body,
                "line": line_no,
            })
            continue

        if upper.startswith("WHILE "):
            condition = line[6:].strip()
            if not condition:
                fail(line_no, "WHILE richiede una condizione.")
            node = While(condition)
            current_target(line_no).append(node)
            stack.append({
                "kind": "WHILE",
                "node": node,
                "target": node.body,
                "line": line_no,
            })
            continue

        if upper == "DO":
            node = DoWhile("")
            current_target(line_no).append(node)
            stack.append({
                "kind": "DO",
                "node": node,
                "target": node.body,
                "line": line_no,
            })
            continue

        fail(line_no, f"Istruzione non riconosciuta: {line}")

    if len(stack) != 1:
        opened = stack[-1]
        raise ParseError(
            f"Blocco {opened['kind']} aperto alla riga {opened['line']} e mai chiuso."
        )

    return root

# ============================================================
# MODELLO DEL DIAGRAMMA
# ============================================================

@dataclass
class Node:
    id: str
    kind: str
    text: str
    x: float
    y: float

@dataclass
class Edge:
    source: str
    target: str
    label: str = ""
    route: str = "direct"

@dataclass
class Fragment:
    entry: str
    exit: str
    center_x: float
    bottom_y: float

class Diagram:
    def __init__(self):
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self._id = 0

    def add_node(self, kind: str, text: str, x: float, y: float) -> str:
        self._id += 1
        node_id = f"n{self._id}"
        self.nodes.append(Node(node_id, kind, text, x, y))
        return node_id

    def add_edge(self, source: str, target: str, label: str = "", route: str = "direct") -> None:
        self.edges.append(Edge(source, target, label, route))

# ============================================================
# LAYOUT
# ============================================================

VERTICAL_STEP = 1.75
BRANCH_GAP = 4.80
JOIN_GAP = 1.35
LOOP_GAP = 4.20

def layout_sequence(diagram: Diagram, statements: list[object], x: float, y: float) -> Fragment:
    if not statements:
        raise ValueError("Blocco vuoto non ammesso nel flowchart.")

    first: Fragment | None = None
    previous: Fragment | None = None
    current_y = y

    for statement in statements:
        fragment = layout_statement(diagram, statement, x, current_y)
        if previous is not None:
            diagram.add_edge(previous.exit, fragment.entry)
        if first is None:
            first = fragment
        previous = fragment
        current_y = fragment.bottom_y - VERTICAL_STEP

    assert first is not None and previous is not None
    return Fragment(first.entry, previous.exit, x, previous.bottom_y)

def layout_statement(diagram: Diagram, stmt: object, x: float, y: float) -> Fragment:
    if isinstance(stmt, Declare):
        node = diagram.add_node("declare", stmt.text, x, y)
        return Fragment(node, node, x, y)
    if isinstance(stmt, Input):
        node = diagram.add_node("input", stmt.text, x, y)
        return Fragment(node, node, x, y)
    if isinstance(stmt, Output):
        node = diagram.add_node("output", stmt.text, x, y)
        return Fragment(node, node, x, y)
    if isinstance(stmt, Process):
        node = diagram.add_node("process", stmt.text, x, y)
        return Fragment(node, node, x, y)
    if isinstance(stmt, If):
        return layout_if(diagram, stmt, x, y)
    if isinstance(stmt, While):
        return layout_while(diagram, stmt, x, y)
    if isinstance(stmt, DoWhile):
        return layout_do_while(diagram, stmt, x, y)
    if isinstance(stmt, For):
        return layout_for(diagram, stmt, x, y)
    raise TypeError(f"Nodo AST non gestito: {type(stmt).__name__}")

def layout_if(diagram: Diagram, stmt: If, x: float, y: float) -> Fragment:
    decision = diagram.add_node("decision", stmt.condition, x, y)
    false_fragment = layout_sequence(diagram, stmt.false_branch, x - BRANCH_GAP, y - VERTICAL_STEP * 1.65)
    true_fragment = layout_sequence(diagram, stmt.true_branch, x + BRANCH_GAP, y - VERTICAL_STEP * 1.65)
    diagram.add_edge(decision, false_fragment.entry, "False", "branch_left")
    diagram.add_edge(decision, true_fragment.entry, "True", "branch_right")
    joint_y = min(false_fragment.bottom_y, true_fragment.bottom_y) - JOIN_GAP
    joint = diagram.add_node("joint", "", x, joint_y)
    diagram.add_edge(false_fragment.exit, joint, route="joint_left")
    diagram.add_edge(true_fragment.exit, joint, route="joint_right")
    return Fragment(decision, joint, x, joint_y)

def layout_while(diagram: Diagram, stmt: While, x: float, y: float) -> Fragment:
    head = diagram.add_node("loop", "\\textbf{While} " + f"{stmt.condition}", x, y)
    body = layout_sequence(diagram, stmt.body, x + LOOP_GAP, y - VERTICAL_STEP * 1.65)
    diagram.add_edge(head, body.entry, "True", "branch_right")
    diagram.add_edge(body.exit, head, "False", "while_back_right")
    exit_y = min(y - VERTICAL_STEP * 1.65, body.bottom_y) - JOIN_GAP
    exit_node = diagram.add_node("spacer", "", x, exit_y)
    diagram.add_edge(head, exit_node, "False", "while_spacer")
    return Fragment(head, exit_node, x, exit_y)

def layout_do_while(diagram: Diagram, stmt: DoWhile, x: float, y: float) -> Fragment:
    do_node = diagram.add_node("joint", "", x, y)
    body = layout_sequence(diagram, stmt.body, x, y - VERTICAL_STEP)
    diagram.add_edge(do_node, body.entry)
    test_y = body.bottom_y - VERTICAL_STEP
    test = diagram.add_node("loop", "\\textbf{While}\\\\"+ stmt.condition, x, test_y)
    diagram.add_edge(body.exit, test)
    diagram.add_edge(test, do_node, "True", "do_back_right")
    exit_y = test_y - VERTICAL_STEP
    exit_node = diagram.add_node("spacer", "", x, exit_y)
    diagram.add_edge(test, exit_node, "False", "while_spacer")
    return Fragment(do_node, exit_node, x, exit_y)

def layout_for(diagram: Diagram, stmt: For, x: float, y: float) -> Fragment:
    text = "\\textbf{For} " + stmt.init + "; \\\\" + f"{stmt.condition}; {stmt.increment}"
    head = diagram.add_node("loop", text, x, y)
    body = layout_sequence(diagram, stmt.body, x + LOOP_GAP, y - VERTICAL_STEP * 1.6)
    diagram.add_edge(head, body.entry, "True", "branch_right")
    diagram.add_edge(body.exit, head, route="for_back_right")
    exit_y = min(body.bottom_y, y - VERTICAL_STEP * 1.6) - JOIN_GAP
    exit_node = diagram.add_node("spacer", "", x, exit_y)
    diagram.add_edge(head, exit_node, "False", "while_spacer")
    return Fragment(head, exit_node, x, exit_y)

# ============================================================
# GENERATORE LaTeX/TIKZ
# ============================================================

def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text

def render_node(node: Node) -> str:
    return f"  \\node[{node.kind}] ({node.id}) at ({node.x:.2f},{node.y:.2f}) {{{node.text}}};"

def render_edge(edge: Edge) -> str:
    label = ""
    if edge.label:
        position = "right"
        if edge.route == "branch_left":
            position = "below=0.3cm, right=0.8cm"
        elif edge.route == "branch_right":
            position = "below=0.3cm, left=0.8cm"
        label = f" node[label,{position}] {{{latex_escape(edge.label)}}}"

    if edge.route == "branch_left":
        return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}.west) -|{label} ({edge.target}.north);"
    if edge.route == "branch_right":
        return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}.east) -|{label} ({edge.target}.north);"
    if edge.route in {"joint_left", "joint_right"}:
        return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}.south) |- ({edge.target});"
    if edge.route == "do_back_right":
        return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}.east) -- ++(1.1,0) |- ({edge.target}.east);"
    if edge.route == "while_back_right":
        return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}.east) -- ++(1.1,0) |- ({edge.target}.north east);"
    if edge.route == "for_back_right":
            return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}.south) -- ++(1.5,0) |- ({edge.target}.north east);"
    if edge.route == "while_spacer":
        return f"  \\draw[flow] ({edge.source}) --{label} ({edge.target}.south);"
    return f"  \\draw[flow, -{{Latex[length=1.7mm]}}] ({edge.source}) --{label} ({edge.target});"

def render_latex(diagram: Diagram) -> str:
    node_lines = "\n".join(render_node(node) for node in diagram.nodes)
    edge_lines = "\n".join(render_edge(edge) for edge in diagram.edges)
    return rf"""
\begin{{tikzpicture}}[x=1cm,y=1cm, scale=0.7, transform shape]
{node_lines}

{edge_lines}
\end{{tikzpicture}}"""


    return rf"""\documentclass[a4paper,11pt]{{article}}

\usepackage[margin=1.5cm]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage[italian]{{babel}}
\usepackage{{xcolor}}
\usepackage{{tikz}}
\usetikzlibrary{{arrows.meta,shapes.geometric,shapes.misc,calc}}

\tikzset{{
  flow/.style={{-{{Latex[length=1.7mm]}}, thick}},
  startstop/.style={{circle, draw=black, fill=red!20, minimum size=8mm, inner sep=1pt, align=center, font=\sffamily\small}},
  declare/.style={{rectangle, draw=black, fill=yellow!25, minimum width=4.0cm, minimum height=10mm, text width=3.5cm, align=center, font=\sffamily\small,
    path picture={{\draw ([xshift=2mm]path picture bounding box.north west) -- ([xshift=2mm]path picture bounding box.south west);
                  \draw ([yshift=-2mm]path picture bounding box.north west) -- ([yshift=-2mm]path picture bounding box.north east);}}}},
  process/.style={{rectangle, draw=black, fill=yellow!15, minimum width=3.7cm, minimum height=8mm, text width=3.2cm, align=center, font=\sffamily\small}},
  input/.style={{trapezium, trapezium left angle=75, trapezium right angle=105, draw=black, fill=blue!20, minimum width=3.7cm, minimum height=8mm, text width=3.2cm, align=center, font=\sffamily\small}},
  output/.style={{trapezium, trapezium left angle=75, trapezium right angle=105, draw=black, fill=green!20, minimum width=3.7cm, minimum height=8mm, text width=3.2cm, align=center, font=\sffamily\small}},
  decision/.style={{diamond, draw=red!80!black, fill=red!25, minimum width=3.7cm, minimum height=1.35cm, text width=2.4cm, align=center, aspect=2, font=\sffamily\small}},
  loop/.style={{chamfered rectangle, draw=brown!70!black, fill=orange!25, minimum width=4.0cm, minimum height=10mm, text width=3.4cm, align=center, font=\sffamily\small}},
  joint/.style={{circle, draw=black, fill=red!20, minimum size=3.5mm, inner sep=0pt}},
  label/.style={{font=\sffamily\footnotesize, fill=white, inner sep=1pt}}
}}

\begin{{document}}
\section*{{{latex_escape(title)}}}
\begin{{center}}
\begin{{tikzpicture}}[x=1cm,y=1cm, scale=0.7, transform shape]
{node_lines}

{edge_lines}
\end{{tikzpicture}}
\end{{center}}
\end{{document}}
"""

# ============================================================
# PROGRAMMA PRINCIPALE
# ============================================================

def build_diagram(ast: list[object]) -> Diagram:
    diagram = Diagram()
    start = diagram.add_node("startstop", "Start", 0, 0)
    body = layout_sequence(diagram, ast, 0, -VERTICAL_STEP)
    stop = diagram.add_node("startstop", "Stop", 0, body.bottom_y - VERTICAL_STEP)
    diagram.add_edge(start, body.entry)
    diagram.add_edge(body.exit, stop)
    return diagram

def generateLatex(code):
    ast = parse_algorithm(code)
    diagram = build_diagram(ast)
    latex = render_latex(diagram)
    output = Path("flowchart_generato.tex")
    output.write_text(latex, encoding="utf-8")
    return latex
    # print(f"Creato: {output.resolve()}")
    # print("Compila con: pdflatex flowchart_generato.tex")

def main(code):
    print(generateLatex(code))




# ============================================================
# INPUT DI ESEMPIO
# ============================================================
# Spazi iniziali, tab e righe vuote vengono ignorati.
#
# Istruzioni:
#   DECLARE testo
#   INPUT testo
#   OUTPUT testo
#   PROCESS testo
#
# Blocchi:
#   IF condizione
#       TRUE
#           ...
#       END TRUE
#       FALSE
#           ...
#       END FALSE
#   END IF
#
#   WHILE condizione
#       ...
#   END WHILE
#
#   DO
#       ...
#   WHILE condizione
#
#   FOR init ; condizione ; incremento
#       ...
#   END FOR
# ============================================================

EXAMPLE = r"""
DECLARE Integer i, j, n
INPUT Leggi n
PROCESS j <- 0

FOR i = 0 ; i < n ; i = i + 1
    IF i mod 2 = 0
        TRUE
            WHILE j < i
                PROCESS Elabora j
                PROCESS j <- j + 1
            END WHILE
            OUTPUT Numero pari
        END TRUE
        FALSE
            OUTPUT Numero dispari
        END FALSE
    END IF

    DO
        PROCESS Aggiorna valore
    WHILE valore != 0
END FOR

OUTPUT Fine algoritmo
"""


if __name__ == "__main__":
    main(EXAMPLE)
