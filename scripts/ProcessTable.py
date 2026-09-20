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

def generateLatex(params):
    processes = parse_csv(params)

    res = []
    res.append("{")
    res.append("\\begin{tabular}{|l|c|c|}")
    res.append("\\hline")
    res.append("\\textbf{Processo} & \\textbf{Arrivo} & \\textbf{Burst} \\\\")
    res.append("\\hline")
    for i in range(len(processes)):
        res.append(f"{processes[i].name} & {processes[i].arrival} & {processes[i].burst} \\\\")
    res.append("\\hline")
    res.append("\\end{tabular}")
    res.append("}")

    return "\n".join(res)

def main(params):
    print(generateLatex(params))

# main("""P1,0,6
# P2,1,4
# P3,2,2
# P4,2,5
# P5,5,3
# P6,5,5""")

import sys

# ha un parametro
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        nums = sys.argv[1]
        main(nums)