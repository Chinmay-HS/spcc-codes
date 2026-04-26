import re

# -------- DEFINITIONS --------
keywords = {
    "int","float","char","double","if","else","while","for","return",
    "void","break","continue","switch","case","default","do","sizeof",
    "struct","union","typedef","enum","const","unsigned","signed","long","short"
}

operators = {
    "+","-","*","/","%","=","==","!=","<",">","<=",">=",
    "&&","||","!","++","--","+=","-=","*=","/=","%="
}

delimiters = {'(', ')', '{', '}', '[', ']', ';', ',', '#', '.'}


# -------- TOKEN STORAGE --------
tokens = {
    "Preprocessor": [],
    "Keyword": [],
    "Identifier": [],
    "Operator": [],
    "Delimiter": [],
    "Number": [],
    "String": [],
    "Unknown": []
}


# -------- HELPER FUNCTIONS --------
def is_identifier(token):
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token)

def is_number(token):
    return re.match(r'^\d+(\.\d+)?$', token)


# -------- MAIN ANALYZER --------
def analyze(code):

    lines = code.split("\n")

    for line in lines:

        # PREPROCESSOR
        if line.strip().startswith("#"):
            tokens["Preprocessor"].append(line.strip())
            continue

        # HANDLE STRINGS
        strings = re.findall(r'\".*?\"|\'.*?\'', line)
        for s in strings:
            tokens["String"].append(s)
            line = line.replace(s, " ")

        # TOKENIZE
        parts = re.split(r'(\W)', line)

        for tok in parts:
            tok = tok.strip()
            if not tok:
                continue

            if tok in keywords:
                tokens["Keyword"].append(tok)

            elif tok in operators:
                tokens["Operator"].append(tok)

            elif tok in delimiters:
                tokens["Delimiter"].append(tok)

            elif is_number(tok):
                tokens["Number"].append(tok)

            elif is_identifier(tok):
                tokens["Identifier"].append(tok)

            else:
                tokens["Unknown"].append(tok)


# -------- READ FILE --------
with open("input.c") as f:
    code = f.read()

analyze(code)


# -------- OUTPUT --------
for category, vals in tokens.items():
    print(f"\n=== {category.upper()} ===")
    for v in sorted(set(vals)):
        print(v)
