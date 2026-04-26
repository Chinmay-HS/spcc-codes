import re

temp_count = 1


def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t


# -------- INFIX TO POSTFIX --------
def precedence(op):
    return {'+':1, '-':1, '*':2, '/':2}.get(op, 0)


def infix_to_postfix(expr):
    stack = []
    output = []
    tokens = re.findall(r'[A-Za-z0-9]+|[\+\-\*/\(\)]', expr)

    for tok in tokens:
        if tok.isalnum():
            output.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(tok):
                output.append(stack.pop())
            stack.append(tok)

    while stack:
        output.append(stack.pop())

    return output


# -------- GENERATE TAC / QUAD / TRIPLE --------
def generate(expr):
    global temp_count
    temp_count = 1

    lhs, rhs = map(str.strip, expr.split("="))
    postfix = infix_to_postfix(rhs)

    stack = []
    tac = []
    quadruples = []
    triples = []

    for tok in postfix:
        if tok.isalnum():
            stack.append(tok)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = new_temp()

            # TAC
            tac.append(f"{temp} = {op1} {tok} {op2}")

            # Quadruple: (op, arg1, arg2, result)
            quadruples.append((tok, op1, op2, temp))

            # Triple: (op, arg1, arg2)
            triples.append((tok, op1, op2))

            stack.append(temp)

    # final assignment
    result = stack.pop()
    tac.append(f"{lhs} = {result}")
    quadruples.append(("=", result, "-", lhs))
    triples.append(("=", result, "-"))

    return tac, quadruples, triples


# -------- MAIN --------
expr = input("Enter expression (e.g., a = b + c * d): ")

tac, quads, triples = generate(expr)

# -------- OUTPUT --------
print("\n=== THREE ADDRESS CODE ===")
for line in tac:
    print(line)

print("\n=== QUADRUPLES ===")
print("Index\tOp\tArg1\tArg2\tResult")
for i, q in enumerate(quads):
    print(f"{i}\t{q[0]}\t{q[1]}\t{q[2]}\t{q[3]}")

print("\n=== TRIPLES ===")
print("Index\tOp\tArg1\tArg2")
for i, t in enumerate(triples):
    print(f"{i}\t{t[0]}\t{t[1]}\t{t[2]}")
