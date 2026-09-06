from dataclasses import dataclass

@dataclass
class Process:
    name: str
    partition: int
def parse_csv(csv_string: str):
    processes = []
    for line in csv_string.strip().split("\n"):
        name, partition = line.split(",")
        processes.append(Process(name, int(partition)))
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

def build_memory_map(partitions: int, processes: list[Process]):
    processes = sorted(processes, key=lambda p: p.partition)
    result = []
    
    for i in range(len(partitions)):
        result.append(Process("FREE", i))
    
    for p in processes:
        result[p.partition].name = p.name
    
    return result

def generateMemory(memory, partitions, spaces):

    res = []

    res.append("    " * (spaces + 1) + "\\begin{tikzpicture}[")
    res.append("    " * (spaces + 2) + "label/.style={font=\\tiny, anchor=west},")
    res.append("    " * (spaces + 2) + "proc/.style={fill=blue!30, draw=blue, thick, minimum width=2cm},")
    res.append("    " * (spaces + 2) + "free/.style={fill=gray!20, draw=gray, thick, minimum width=2cm}")
    res.append("    " * (spaces + 1) + "]")
    
    height_pet_unit = 8 / sum(partitions)
    
    prev_node = None
    for i, p in enumerate(memory):
        size = partitions[i]
        h = size * height_pet_unit 
        if p.name == "FREE":
            style = "free"
            text = ""
            node_name = f"f{i}"
        else:
            style = "proc"
            text = p.name
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
        size = partitions[i]
        
        res.append("    " * (spaces + 2) + f"\\node[label] at ({node_name}.east) {{{size}}};")
        
        if i == len(memory) - 1:
            res.append("    " * (spaces + 2) + f"\\node[label] at ([xshift=1cm]{node_name}.south) {{}};")
    
    res.append("    " * (spaces + 1) + "\\end{tikzpicture}")
    return "\n".join(res)

def free_process(mem, process_name):
    """Rimuove un processo e lo trasforma in FREE"""
    new_mem = []
    freed = False
    for b in mem:
        if b.name == process_name:
            new_mem.append(Process("FREE", b.partition))
            freed = True
        else:
            new_mem.append(b)
    
    if not freed:
        return mem  # Non trovato, memoria invariata
    
    return new_mem

def find_allocation_block(mem, partitions, process, alg, last_index=None):
    """Trova il blocco da usare per allocazione secondo l'algoritmo"""
    if alg == "FF":
        for i, b in enumerate(mem):
            if b.name == "FREE" and partitions[i] >= process.size:
                return i
    elif alg == "BF":
        best_i = None
        best_size = float('inf')
        for i, b in enumerate(mem):
            if b.name == "FREE":
                if partitions[i] >= process.size and partitions[i] < best_size:
                    best_size = partitions[i]
                    best_i = i
        return best_i
    elif alg == "WF":
        worst_i = None
        worst_size = 0
        for i, b in enumerate(mem):
            if b.name == "FREE":
                if partitions[i] >= process.size and partitions[i] > worst_size:
                    worst_size = partitions[i]
                    worst_i = i
        return worst_i
    elif alg == "NF":
        n = len(mem)
        if last_index is None:
            last_index = 0
        for step in range(n):
            i = (last_index + step) % n
            b = mem[i]
            if b.name == "FREE" and partitions[i] >= process.size:
                return i, i  # return anche il nuovo last_index
        return None
    return None

def apply_operations(initial_memory, partitions, operations, alg):
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
                alloc_i, new_last_index = find_allocation_block(mem, partitions, op, alg, last_index)
                if alloc_i is not None:
                    mem[alloc_i] = Process(op.name, alloc_i)
                    last_index = new_last_index
            else:
                alloc_i = find_allocation_block(mem, partitions, op, alg)
                if alloc_i is not None:
                    mem[alloc_i] = Process(op.name, alloc_i)
        
        states.append(mem.copy())
    
    return states

def generateLatex(params, spaces = 1):
    p = params.split(";")
    
    alg, num_part, sol = p[0].split(",")
    num_part = int(num_part)
    
    partitions = [int(x) for x in p[1].split(",")]
    
    processes = parse_csv(p[2])
    operations = parse_csv_to_allocate(p[3])

    memory = build_memory_map(partitions, processes)

    res = []
    if sol == "T":
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
        res.append(generateMemory(memory, partitions, spaces + 3))
        res.append("    " * (spaces + 2) + "\\end{minipage}")
        # res.append("    " * (spaces + 3) + "\\vspace{-0.5cm}")

    if sol == "S":
        evolution = apply_operations(memory, partitions, operations, alg)
        for m in evolution:
            res.append("    " * (spaces + 1) + "\\scalebox{0.8}{\\begin{minipage}{3cm}\\centering")
            res.append(generateMemory(m, partitions, spaces + 1))
            res.append("    " * (spaces + 1) + "\\end{minipage}}\\hspace{0.5cm}")
    return "\n".join(res)

def main(params, spaces = 1):
    print(generateLatex(params, spaces))



# ALLOCAZIONE A PARTIZIONI FISSE
#
# ALG, NUM_PARIZIONI, TESTO/SOLUZIONE (T/S);
# DIM_PARTIZIONE1, ..., DIM_PARTIZIONEn;
# PROC_ALLOCATO1, PARTIZIONE_ALLOCATA
# ...
# PROC_ALLOCATOn, PARTIZIONE_ALLOCATA;
# PROC_DA_ALLOCARE1, SPAZIO_DA_ALLOCARE
# PROC_DA_ALLOCAREk, FREE
# ...
# PROC_DA_ALLOCAREn, SPAZIO_DA_ALLOCARE

# main("""BF,5,S;
# 200,300,400,200,400;
# P1,0
# P2,1
# P3,3;
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