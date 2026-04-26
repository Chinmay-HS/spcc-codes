class NonTerminal:
    def __init__(self, name):
        self.name = name
        self.rules = []

    def add_rule(self, r):
        self.rules.append(r)

    def __str__(self):
        return f"{self.name} -> {' | '.join(self.rules)}"


class Grammar:
    def __init__(self):
        self.nts = []

    def add_rule(self, line):
        name, rhs = map(str.strip, line.split("->"))
        nt = NonTerminal(name)
        for r in rhs.split("|"):
            nt.add_rule(r.strip())
        self.nts.append(nt)

    def solve_indirect(self, A, B):
        new_rules = []
        for r in A.rules:
            if r.startswith(B.name):
                for br in B.rules:
                    new_rules.append(br + r[len(B.name):])
            else:
                new_rules.append(r)
        A.rules = new_rules

    def solve_direct(self, A):
        alpha, beta = [], []

        for r in A.rules:
            (alpha if r.startswith(A.name) else beta).append(
                r[len(A.name):] if r.startswith(A.name) else r
            )

        if not alpha:
            return

        new_name = A.name + "'"
        A1 = NonTerminal(new_name)

        A.rules = [b + new_name for b in beta]
        A1.rules = [a + new_name for a in alpha] + ["ε"]

        self.nts.append(A1)

    def apply(self):
        for i in range(len(self.nts)):
            for j in range(i):
                self.solve_indirect(self.nts[i], self.nts[j])
            self.solve_direct(self.nts[i])

    def print(self):
        for nt in self.nts:
            print(nt)


# -------- MAIN --------
g = Grammar()
n = int(input("Enter number of productions: "))

for _ in range(n):
    line = input("Enter rule: ")
    g.add_rule(line)

g.apply()

print("\nAfter removing left recursion:")
g.print()
