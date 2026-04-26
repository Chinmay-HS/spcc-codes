import re

keywords = {
    "int","float","char","double","if","else","while","for","return",
    "void","break","continue","switch","case","default","do","sizeof",
    "struct","union","typedef","enum","const","unsigned","signed","long","short"
}

operators = {"+","-","*","/","%","=","==","!=","<",">","<=",">=",
             "&&","||","!","++","--","+=","-=","*=","/=","%="}

delimiters = {'(', ')', '{', '}', '[', ']', ';', ',', '#', '.'}


def get_type(tok):
    if tok in keywords: return "KEYWORD"
    if tok in operators: return "OPERATOR"
    if tok in delimiters: return "DELIMITER"
    if re.match(r'^\d+(\.\d+)?$', tok): return "NUMBER"
    if re.match(r'^[A-Za-z_]\w*$', tok): return "IDENTIFIER"
    return "UNKNOWN"


# -------- MAIN --------
with open("input.c") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        print(f"\nLINE: {line}")

        # Preprocessor
        if line.startswith("#"):
            print(f"  {line} -> PREPROCESSOR")
            continue

        # Extract strings
        strings = re.findall(r'\".*?\"|\'.*?\'', line)
        for s in strings:
            print(f"  {s} -> STRING")
            line = line.replace(s, " ")

        # Tokenize
        tokens = re.findall(r'[A-Za-z_]\w*|\d+\.\d+|\d+|==|!=|<=|>=|\+\+|--|\+=|-=|\*=|/=|%=|&&|\|\||\S', line)

        for tok in tokens:
            print(f"  {tok} -> {get_type(tok)}")
