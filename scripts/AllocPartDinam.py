from dataclasses import dataclass

@dataclass
class Process:
    name: str
    start: int
    end: int
def parse_csv(csv_string: str):
    processes = []
    for line in csv_string.strip().split("\n"):
        name, start, end = line.split(",")
        processes.append(Process(name, int(start), int(end)))
    return processes

@dataclass
class ProcessToAllocate:
    name: str
    size: int | None # size = None ==> Processo da liberare
def parse_csv_to_allocate(csv_string: str):
    processes = []
    for line in csv_string.strip().split("\n"):
        name, size = line.split(",")
        if size == "FREE":
            processes.append(ProcessToAllocate(name, None))
        else:
            processes.append(ProcessToAllocate(name, int(size)))
    return processes

def build_memory_map(total_size: int, processes: list[Process]):
    processes = sorted(processes, key=lambda p: p.start)
    result = []
    cursor = 0

    for p in processes:
        if p.start > cursor:
            result.append(Process(name="FREE", start=cursor, end=p.start - 1))
        result.append(p)
        cursor = max(cursor, p.end + 1)

    if cursor < total_size:
        result.append(Process(name="FREE", start=cursor, end=total_size - 1))

    return result

def printMemory(memory, mem_size, spaces):
    res = []

    res.append("    " * (spaces + 1) + "\\begin{tikzpicture}[")
    res.append("    " * (spaces + 2) + "label/.style={font=\\tiny, anchor=west},")
    res.append("    " * (spaces + 2) + "proc/.style={fill=blue!30, draw=blue, thick, minimum width=2cm},")
    res.append("    " * (spaces + 2) + "free/.style={fill=gray!20, draw=gray, thick, minimum width=2cm}")
    res.append("    " * (spaces + 1) + "]")
    
    height_pet_unit = 8 / mem_size
    
    prev_node = None
    for i, b in enumerate(memory):
        size = b.end - b.start + 1
        h = size * height_pet_unit 
        if b.name == "FREE":
            style = "free"
            text = ""
            node_name = f"f{i}"
        else:
            style = "proc"
            text = b.name
            node_name = f"p{i}"

        if prev_node is None:
            res.append("    " * (spaces + 2) + f"\\node[{style}, minimum height={h:.3f}cm] ({node_name}) at (0,0,) {{{text}}};")
        else:
            res.append("    " * (spaces + 2) + f"\\node[{style}, minimum height={h:.3f}cm, below=0pt of {prev_node}] ({node_name}) {{{text}}};")
        
        prev_node = node_name

    res.append("    " * (spaces + 2) + "")
    
    # Etichette di indirizzo (solo inizio di ogni blocco)
    for i, b in enumerate(memory):
        node_name = f"f{i}" if b.name == "FREE" else f"p{i}"
        res.append("    " * (spaces + 2) + f"\\node[label] at ([xshift=1cm]{node_name}.north) {{{b.start}}};")
        if i == len(memory) - 1:
            res.append("    " * (spaces + 2) + f"\\node[label] at ([xshift=1cm]{node_name}.south) {{{mem_size}}};")
    
    res.append("    " * (spaces + 1) + "\\end{tikzpicture}")

    return "\n".join(res)

def merge_free_blocks(mem):
    """Fonde blocchi FREE consecutivi"""
    if not mem:
        return mem
    merged = [mem[0]]
    for b in mem[1:]:
        if merged[-1].name == "FREE" and b.name == "FREE" and merged[-1].end + 1 == b.start:
            merged[-1] = Process("FREE", merged[-1].start, b.end)
        else:
            merged.append(b)
    return merged

def free_process(mem, process_name):
    """Rimuove un processo e lo trasforma in FREE"""
    new_mem = []
    freed = False
    for b in mem:
        if b.name == process_name:
            new_mem.append(Process("FREE", b.start, b.end))
            freed = True
        else:
            new_mem.append(b)
    
    if not freed:
        return mem  # Non trovato, memoria invariata
    
    return merge_free_blocks(new_mem)

def split_and_insert(mem, i, p):
    """Split del blocco FREE e inserimento del processo"""
    b = mem[i]
    new_blocks = [Process(p.name, b.start, b.start + p.size - 1)]
    if b.start + p.size <= b.end:
        new_blocks.append(Process("FREE", b.start + p.size, b.end))
    return mem[:i] + new_blocks + mem[i+1:]

def find_allocation_block(mem, p, alg, last_index=None):
    """Trova il blocco da usare per allocazione secondo l'algoritmo"""
    if alg == "FF":
        for i, b in enumerate(mem):
            if b.name == "FREE" and (b.end - b.start + 1) >= p.size:
                return i
    elif alg == "BF":
        best_i = None
        best_size = float('inf')
        for i, b in enumerate(mem):
            if b.name == "FREE":
                block_size = b.end - b.start + 1
                if block_size >= p.size and block_size < best_size:
                    best_size = block_size
                    best_i = i
        return best_i
    elif alg == "WF":
        worst_i = None
        worst_size = 0
        for i, b in enumerate(mem):
            if b.name == "FREE":
                block_size = b.end - b.start + 1
                if block_size >= p.size and block_size > worst_size:
                    worst_size = block_size
                    worst_i = i
        return worst_i
    elif alg == "NF":
        n = len(mem)
        if last_index is None:
            last_index = 0
        for step in range(n):
            i = (last_index + step) % n
            b = mem[i]
            if b.name == "FREE" and (b.end - b.start + 1) >= p.size:
                return i, i  # return anche il nuovo last_index
        return None
    return None

def apply_operations(initial_memory, operations, alg):
    """Applica sequenza di allocazioni e FREE"""
    states = [initial_memory.copy()]
    mem = initial_memory.copy()
    last_index = 0  # per NF

    for op in operations:
        if op.size is None:
            # FREE
            mem = free_process(mem, op.name)
        else:
            # ALLOC
            if alg == "NF":
                alloc_i, new_last_index = find_allocation_block(mem, op, alg, last_index)
                if alloc_i is not None:
                    mem = split_and_insert(mem, alloc_i, op)
                    last_index = new_last_index
            else:
                alloc_i = find_allocation_block(mem, op, alg)
                if alloc_i is not None:
                    mem = split_and_insert(mem, alloc_i, op)
        
        states.append(mem.copy())
    
    return states

def generateLatex(params, spaces = 1):
    p = params.split(";")

    alg, mem_size, sol = p[0].split(",")
    mem_size = int(mem_size)
    processes = parse_csv(p[1])
    operations = parse_csv_to_allocate(p[2])

    memory = build_memory_map(mem_size, processes)

    res = []
    if sol == "T":
        res.append("    " * spaces + "{")
        res.append("    " * (spaces + 2) + "\\begin{minipage}[t]{0.45\\textwidth}")
        res.append("    " * (spaces + 3) + "\\begin{itemize}")
        for o in operations:
            if o.size == None:
                res.append("    " * (spaces + 4) + f"\\item {o.name} esce")
                res.append("    " * (spaces + 4) + "\\vspace{0.1cm}")
            else:
                res.append("    " * (spaces + 4) + f"\\item {o.name} di dimensione {o.size}Kb")
                res.append("    " * (spaces + 4) + "\\vspace{0.1cm}")
        res.append("    " * (spaces + 3) + "\\end{itemize}")
        res.append("    " * (spaces + 2) + "\\end{minipage}")
        res.append("    " * (spaces + 2) + "\\hfill")
        res.append("    " * (spaces + 2) + "\\begin{minipage}[t]{0.45\\textwidth}")
        res.append("    " * (spaces + 3) + "\\vspace{-0.5cm}")
        res.append(printMemory(memory, mem_size, spaces + 3))
        res.append("    " * (spaces + 2) + "\\end{minipage}")
        res.append("    " * (spaces + 3) + "\\vspace{-0.5cm}")
        # res.append("    " * (spaces + 3) + "\\vspace{-0.5cm}")
        res.append("    " * spaces + "}")

    if sol == "S":
        evolution = apply_operations(memory, operations, alg)
    
        res.append("    " * spaces + "{")
        res.append("    " * (spaces + 1) + "\\vspace{0.25cm}")
        for m in evolution:
            res.append("    " * (spaces + 1) + "\\scalebox{0.8}{\\begin{minipage}{3cm}\\centering")
            res.append(printMemory(m, mem_size, spaces + 1))
            res.append("    " * (spaces + 1) + "\\end{minipage}}\\hspace{0.5cm}")
        res.append("    " * spaces + "}")

    return "\n".join(res)

def main(params, spaces = 1):
    print(generateLatex(params, spaces))


# ALLOCAZIONE A PARTIZIONI DINAMICHE
#
# ALG, DIM_MEMORIA, TESTO/SOLUZIONE (T/S);
# PROC_ALLOCATO1, INIZIO_ALLOCAZIONE, FINE_ALLOCAZIONE
# ...
# PROC_ALLOCATOn, INIZIO_ALLOCAZIONE, FINE_ALLOCAZIONE;
# PROC_DA_ALLOCARE1, SPAZIO_DA_ALLOCARE
# PROC_DA_ALLOCAREk, FREE
# ...
# PROC_DA_ALLOCAREn, SPAZIO_DA_ALLOCARE
    

# main("""FF,500,S;
# P1,0,20
# P2,50,100
# P3,150,200;
# P4,20
# P1,FREE
# P5,10
# P6,150
# """, 2)

import sys

# ha un parametro
if len(sys.argv) >= 2:
    nums = sys.argv[1]
    main(nums, 0)