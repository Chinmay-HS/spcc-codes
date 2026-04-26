import re, time

class Instr:
    def __init__(self, i, line):
        self.id = i
        self.lhs, self.rhs = map(str.strip, line.split("="))
    def __str__(self): return f"{self.lhs} = {self.rhs}"


def cost(code):
    return sum(3 if "*" in i.rhs else 2 if "+" in i.rhs else 1 for i in code)


# READ FILE
tac = [Instr(i, l.strip()) for i, l in enumerate(open("input.txt"), 1) if l.strip()]

print("=== ORIGINAL CODE ===")
for i in tac: print(f"{i.id}: {i}")
orig = cost(tac)


# COPY PROPAGATION
cp_s = time.time_ns()
mp = {}

for i in tac:
    for k in list(mp):
        i.rhs = re.sub(rf"\b{k}\b", mp[k], i.rhs)

    if not any(op in i.rhs for op in "+*") and not i.rhs.isdigit():
        mp[i.lhs] = mp.get(i.rhs, i.rhs)

cp_e = time.time_ns()

print("\n=== AFTER COPY PROPAGATION ===")
for i in tac: print(f"{i.id}: {i}")


# DEAD CODE ELIMINATION
dce_s = time.time_ns()
used, opt = {"x","y","z","w"}, []

for i in tac[::-1]:
    if i.lhs in used:
        opt.insert(0, i)
        used |= {t for t in re.split(r"\W+", i.rhs)
                 if re.match(r"[A-Za-z]\w*", t)}

dce_e = time.time_ns()

print("\n=== AFTER DEAD CODE ELIMINATION ===")
for i, v in enumerate(opt, 1): print(f"{i}: {v}")

opt_cost = cost(opt)


# TIMINGS
tot = (cp_e - cp_s) + (dce_e - dce_s)

print("\n=== TIMINGS ===")
print(f"Copy Propagation: {cp_e - cp_s} ns")
print(f"Dead Code Elimination: {dce_e - dce_s} ns")
print(f"Total Optimization Time: {tot} ns")


# COST
print("\n=== EXECUTION COST COMPARISON ===")
print(f"Original Cost: {orig}")
print(f"Optimized Cost: {opt_cost}")

saved = orig - opt_cost
print(f"Cost Reduction: {saved}")
print(f"Improvement: {(saved*100/orig if orig else 0):.2f}%")
