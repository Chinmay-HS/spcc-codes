mot = {"L": "58", "A": "5A", "ST": "50"}
symtab = {}
lc = 0

lines = open("input.txt").readlines()

def parse(line):
    has_label = line[0] not in (' ', '\t')
    words = line.split()
    if not words: return None, None, None
    if has_label:
        label  = words[0]
        opcode = words[1] if len(words) > 1 else "-"
        operand = " ".join(words[2:]) if len(words) > 2 else "-"
    else:
        label   = "-"
        opcode  = words[0]
        operand = " ".join(words[1:]) if len(words) > 1 else "-"
    return label, opcode, operand

# ===== PASS 1 =====
print("\n===== PASS 1 =====\n")
print(f"{'LC':<6}{'LABEL':<10}{'OPCODE':<10}OPERAND")
print("-" * 40)

for line in lines:
    if not line.strip(): continue
    label, opcode, operand = parse(line)

    if opcode == "START":
        lc = int(operand)
        print(f"{lc:<6}{label:<10}{opcode:<10}{operand}")
        continue
    if opcode == "USING":
        print(f"{lc:<6}{label:<10}{opcode:<10}{operand}")
        continue
    if opcode == "END":
        print(f"{lc:<6}{label:<10}{opcode:<10}{operand}")
        break

    if label != "-":
        symtab[label] = lc

    print(f"{lc:<6}{label:<10}{opcode:<10}{operand}")
    lc += 1

# Symbol Table
print("\nSymbol Table:")
print(f"{'Index':<8}{'Symbol':<10}Address")
print("-" * 25)
for i, (k, v) in enumerate(symtab.items(), 1):
    print(f"{i:<8}{k:<10}{v}")

# ===== PASS 2 =====
print("\n===== PASS 2 =====\n")
print(f"{'LC':<6}{'OPCODE':<10}{'REG':<6}ADDR")
print("-" * 30)
lc = 0

for line in lines:
    if not line.strip(): continue
    label, opcode, operand = parse(line)
    if opcode in ("START", "USING", "END", "DC", "DS"): continue

    if opcode in mot:
        reg, sym = operand.split(",")
        sym  = sym.strip()
        addr = symtab.get(sym, "?")
        print(f"{lc:<6}{mot[opcode]:<10}{reg.strip():<6}{addr}")
        lc += 1