import re
import time


class Instr:
    def __init__(self, id, line):
        self.id = id
        parts = line.split("=")
        self.lhs = parts[0].strip()
        self.rhs = parts[1].strip()

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"


# COST MODEL
def compute_cost(code):
    cost = 0
    for i in code:
        rhs = i.rhs
        if "*" in rhs:
            cost += 3
        elif "+" in rhs:
            cost += 2
        else:
            cost += 1
    return cost


# -------- MAIN --------
tac = []

# READ FROM FILE
with open("input.txt") as f:
    for idx, line in enumerate(f, 1):
        if line.strip():
            tac.append(Instr(idx, line.strip()))

# ORIGINAL
print("=== ORIGINAL CODE ===")
for i in tac:
    print(f"{i.id}: {i}")

original_cost = compute_cost(tac)

# COPY PROPAGATION
cp_start = time.time_ns()

mapping = {}

for i in tac:
    # replace variables using map
    for key in list(mapping.keys()):
        i.rhs = re.sub(rf"\b{key}\b", mapping[key], i.rhs)

    # detect simple copy (x = y)
    if not any(op in i.rhs for op in ["+", "*"]) and not i.rhs.isdigit():
        mapping[i.lhs] = mapping.get(i.rhs, i.rhs)

cp_end = time.time_ns()

print("\n=== AFTER COPY PROPAGATION ===")
for i in tac:
    print(f"{i.id}: {i}")

# DEAD CODE ELIMINATION
dce_start = time.time_ns()

used = {"x", "y", "z", "w"}  # final outputs
optimized = []

for inst in reversed(tac):
    if inst.lhs in used:
        optimized.insert(0, inst)

        tokens = re.split(r"[^a-zA-Z0-9]+", inst.rhs)
        for t in tokens:
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*", t):
                used.add(t)

dce_end = time.time_ns()

# FINAL OUTPUT
print("\n=== AFTER DEAD CODE ELIMINATION ===")
for idx, i in enumerate(optimized, 1):
    print(f"{idx}: {i}")

optimized_cost = compute_cost(optimized)

# TIMINGS
total_time = (cp_end - cp_start) + (dce_end - dce_start)

print("\n=== TIMINGS ===")
print(f"Copy Propagation: {cp_end - cp_start} ns")
print(f"Dead Code Elimination: {dce_end - dce_start} ns")
print(f"Total Optimization Time: {total_time} ns")

# COST COMPARISON
print("\n=== EXECUTION COST COMPARISON ===")
print(f"Original Cost: {original_cost}")
print(f"Optimized Cost: {optimized_cost}")

saved = original_cost - optimized_cost
print(f"Cost Reduction: {saved}")

percent = (saved * 100.0) / original_cost if original_cost else 0
print(f"Improvement: {percent:.2f}%")
