from dataclasses import dataclass
from collections import deque

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

def calculate_metrics(schedule, original_processes):
    """Calcola tempi di completamento, attesa e turnaround per ogni processo"""
    proc_dict = {p.name: {'name': p.name, 'arrival': p.arrival, 'burst': p.burst, 'completion': None} 
                 for p in original_processes}
    
    # Trova il tempo di completamento massimo per ogni processo
    for name, start, end in schedule:
        if proc_dict[name]['completion'] is None or end > proc_dict[name]['completion']:
            proc_dict[name]['completion'] = end
    
    # Calcola turnaround e waiting time
    for name, data in proc_dict.items():
        data['turnaround'] = data['completion'] - data['arrival']
        data['waiting'] = data['turnaround'] - data['burst']
    
    # Calcola medie
    avg_waiting = sum(data['waiting'] for data in proc_dict.values()) / len(proc_dict)
    avg_turnaround = sum(data['turnaround'] for data in proc_dict.values()) / len(proc_dict)
    
    return proc_dict, avg_waiting, avg_turnaround

def fcfs(processes):
    time = 0
    schedule = []
    processes = sorted(processes, key=lambda p: p.arrival)
    for p in processes:
        start = max(time, p.arrival)
        end = start + p.burst
        schedule.append((p.name, start, end))
        time = end
    return schedule

def sjf(processes):
    time = 0
    completed = []
    ready = []
    processes = processes[:]
    while processes or ready:
        for p in processes[:]:
            if p.arrival <= time:
                ready.append(p)
                processes.remove(p)
        if ready:
            p = min(ready, key=lambda x: x.burst)
            ready.remove(p)
            start = time
            end = time + p.burst
            completed.append((p.name, start, end))
            time = end
        else:
            time += 1
    return completed

def srtf(processes):
    time = 0
    schedule = []
    remaining = {p.name: p.burst for p in processes}
    processes = sorted(processes, key=lambda p: p.arrival)
    ready = []
    current = None
    start_time = 0
    while remaining:
        for p in processes[:]:
            if p.arrival == time:
                ready.append(p)
                processes.remove(p)
        if ready:
            p = min(ready, key=lambda x: remaining[x.name])
            if current != p.name:
                if current is not None:
                    schedule.append((current, start_time, time))
                current = p.name
                start_time = time
            remaining[p.name] -= 1
            time += 1
            if remaining[p.name] == 0:
                schedule.append((p.name, start_time, time))
                if p in ready:
                    ready.remove(p)
                del remaining[p.name]
                current = None
        else:
            time += 1
    return schedule

def round_robin(processes, quantum):
    time = 0
    queue = deque()
    schedule = []
    remaining = {p.name: p.burst for p in processes}
    processes = sorted(processes, key=lambda p: p.arrival)
    i = 0
    while queue or i < len(processes):
        while i < len(processes) and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1
        if queue:
            p = queue.popleft()
            start = time
            exec_time = min(quantum, remaining[p.name])
            time += exec_time
            remaining[p.name] -= exec_time
            schedule.append((p.name, start, time))
            while i < len(processes) and processes[i].arrival <= time:
                queue.append(processes[i])
                i += 1
            if remaining[p.name] > 0:
                queue.append(p)
            else:
                del remaining[p.name]
        else:
            time += 1
    return schedule

def printLatex(algo, schedule, spaces, original_processes):
    proc_dict, avg_wait, avg_turn = calculate_metrics(schedule, original_processes)
    
    # Metriche
    names = [data['name'] for data in proc_dict.values()]
    arrivals = [str(data['arrival']) for data in proc_dict.values()]
    bursts = [str(data['burst']) for data in proc_dict.values()]
    waits = [str(data['waiting']) for data in proc_dict.values()]
    turns = [str(data['turnaround']) for data in proc_dict.values()]
    
    totalLen = int(schedule[-1][2])
    
    
    # Tabella con diagramma
    print("    " * spaces + "{")
    print("    " * (spaces + 1) + "\\vspace{0.25cm}")
    print("    " * (spaces + 1) + "\\textbf{" + algo + "}")
    print("    " * (spaces + 1) + "\\vspace{0.15cm}")
    print("    " * (spaces + 1))
    print("    " * (spaces + 1) + "\\newcolumntype{T}{>{\\tiny\\scalebox{0.8}}p{0.025cm}}")
    print("    " * (spaces + 1))
    print("    " * (spaces + 1) + "\\begin{tabular}{|l|c|c|" + "|*{5}T" * (totalLen // 5) + "T" * (totalLen % 5) + "||c|c|}")
    print("    " * (spaces + 2) + "\\hline")
    print("    " * (spaces + 2) + "\\textbf{P} & \\textbf{A} & \\textbf{D}" + "&" * totalLen + "& T. Att. & T. Compl." + "\\\\")
    print("    " * (spaces + 2) + "\\hline")
    
    for i in range(len(names)):
        print("    " * (spaces + 2) + f"{names[i]} & {arrivals[i]} & {bursts[i]}", end="")
    
        t = 1
        a = int(arrivals[i])
        
        for j in range(len(schedule)):
            s = schedule[j]
            futureSchedule = any(obj[0] == names[i] for obj in schedule[j+1:])
            
            if s[0] == names[i]:
                print("& \\cellcolor{blue!30} " * (s[2]-s[1]), end="")
                t += s[2] - s[1]
            else:
                d = s[2] - s[1]
                for k in range(d):
                    if a >= t + k:
                        print("& ", end="")
                    elif futureSchedule:
                        print("& - ", end="")
                    else:
                        print("& ", end="")
                        
                t += s[2] - s[1]
        
        print(f" & {waits[i]} & {turns[i]} \\\\")
        
    print("    " * (spaces + 2) + "\\hline")
    print("    " * (spaces + 2) + "& & " + "&" * totalLen + f"& {avg_wait:.2f} & {avg_turn:.2f}" + "\\\\")
    print("    " * (spaces + 2) + "\\hline")
    
    print("    " * (spaces + 1) + "\\end{tabular}")
    print("    " * (spaces + 1) + "\\vspace{0.25cm}")
    print("    " * spaces + "}")
    
    # Tabelle metriche
    # print("    " * (spaces + 1))
    # print("    " * spaces + "{")
    # print("    " * (spaces + 1) + "\\begin{tabular}{|l|c|c|c|c|}")
    # print("    " * (spaces + 2) + "\\hline")
    # print("    " * (spaces + 2) + "\\textbf{Processo} & \\textbf{Arrivo} & \\textbf{Burst} & \\textbf{Attesa} & \\textbf{Turnaround} \\\\")
    # print("    " * (spaces + 2) + "\\hline")
    # for i in range(len(names)):
    #     print("    " * (spaces + 2) + f"{names[i]} & {arrivals[i]} & {bursts[i]} & {waits[i]} & {turns[i]} \\\\")
    # print("    " * (spaces + 2) + "\\hline")
    # print("    " * (spaces + 2) + f"\\textbf{{Media}} & & & {avg_wait:.2f} & {avg_turn:.2f} \\\\")
    # print("    " * (spaces + 2) + "\\hline")
    # print("    " * (spaces + 1) + "\\end{tabular}")
    # print("    " * spaces + "}")

def main(params, spaces = 1):
    alg = params.split(";")[0]
    processes = parse_csv(params.split(";")[1])
    schedule = []
    
    if alg == "FCFS":
        schedule = fcfs(processes)
    elif alg == "SJF":
        schedule = sjf(processes)
    elif alg == "SRTF":
        schedule = srtf(processes)
    elif alg.startswith("RR"):
        q = int(alg[2:])
        schedule = round_robin(processes, q)
    
    printLatex(alg, schedule, spaces, processes)
    
    
# main("""RR2;
# P1,0,6
# P2,1,4
# P3,2,2
# P4,2,5
# P5,5,3
# P6,5,5""", 2)