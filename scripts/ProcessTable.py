from dataclasses import dataclass

@dataclass
class Process:
    name: str
    arrival: int
    burst: int

def parse_csv(csv_string: str):
    processes = []
    for line in csv_string.strip().split("\n"):
        name, arrival, burst = line.split(",")
        processes.append(Process(name, int(arrival), int(burst)))
    return processes

def generateLatex(params, spaces=1):
    processes = parse_csv(params)

    res = []
    res.append("    " * spaces + "{")
    res.append("    " * (spaces + 1) + "\\begin{tabular}{|l|c|c|}")
    res.append("    " * (spaces + 2) + "\\hline")
    res.append("    " * (spaces + 2) + "\\textbf{Processo} & \\textbf{Arrivo} & \\textbf{Burst} \\\\")
    res.append("    " * (spaces + 2) + "\\hline")
    for i in range(len(processes)):
        res.append("    " * (spaces + 2) + f"{processes[i].name} & {processes[i].arrival} & {processes[i].burst} \\\\")
    res.append("    " * (spaces + 2) + "\\hline")
    res.append("    " * (spaces + 1) + "\\end{tabular}")
    res.append("    " * spaces + "}")

    return "\n".join(res)

def main(params, spaces = 1):
    print(generateLatex(params, spaces))

# main("""P1,0,6
# P2,1,4
# P3,2,2
# P4,2,5
# P5,5,3
# P6,5,5""", 2)

import sys

# ha un parametro
if len(sys.argv) >= 2:
    nums = sys.argv[1]
    main(nums, 0)