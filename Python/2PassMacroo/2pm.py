# -------- DATA STRUCTURES --------
MDT = []
MNT = {}
ALA = {}

# -------- MAIN --------
output = []
macro_def = False
mdt_index = 0

# -------- PASS 1 --------
with open("input.asm") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        if line == "MACRO":
            macro_def = True
            continue

        if macro_def:
            if line == "MEND":
                MDT.append("MEND")
                macro_def = False
                continue

            parts = line.split()

            # macro header
            if parts[0] not in MNT:
                MNT[parts[0]] = mdt_index

                params = parts[1].split(",")
                for i, p in enumerate(params):
                    ALA[p] = i

            # replace params with #index
            for arg in list(ALA.keys()):
                line = line.replace(arg, f"#{ALA[arg]}")

            MDT.append(line)
            mdt_index += 1

        else:
            output.append(line)

# -------- PRINT TABLES --------
print("\n=== MNT ===")
for k, v in MNT.items():
    print(f"{k} -> {v}")

print("\n=== MDT ===")
for i, val in enumerate(MDT):
    print(f"{i} : {val}")

print("\n=== ALA ===")
for k, v in ALA.items():
    print(f"{k} -> #{v}")

# -------- PASS 2 (EXPANSION) --------
print("\n=== EXPANDED CODE ===")

for l in output:
    parts = l.split()

    if parts[0] in MNT:
        ptr = MNT[parts[0]]
        actuals = parts[1].split(",")

        while MDT[ptr] != "MEND":
            temp = MDT[ptr]

            for i in range(len(actuals)):
                temp = temp.replace(f"#{i}", actuals[i])

            print(temp)
            ptr += 1
    else:
        print(l)
