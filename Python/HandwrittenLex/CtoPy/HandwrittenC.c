#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 1000

// -------- PYTHON KEYWORDS --------
const char *keywords[] = {
    "def","return","if","else","elif","for","while","break","continue",
    "import","from","as","class","try","except","finally","with",
    "lambda","pass","yield","True","False","None","and","or","not","in","is"
};

int isKeyword(char *word) {
    int n = sizeof(keywords)/sizeof(keywords[0]);
    for(int i=0;i<n;i++)
        if(strcmp(word, keywords[i])==0)
            return 1;
    return 0;
}

int isOperator(char c) {
    return strchr("+-*/%=<>!", c) != NULL;
}

int isDelimiter(char c) {
    return strchr("(){}[],:.;", c) != NULL;
}

// -------- MAIN --------
int main() {
    FILE *fp = fopen("input.py", "r");
    if (!fp) {
        printf("File not found\n");
        return 1;
    }

    char ch, buffer[MAX];
    int i = 0;

    while ((ch = fgetc(fp)) != EOF) {

        // -------- IDENTIFIER / KEYWORD --------
        if (isalpha(ch) || ch == '_') {
            buffer[i++] = ch;

            while ((ch = fgetc(fp)) != EOF && (isalnum(ch) || ch == '_')) {
                buffer[i++] = ch;
            }

            buffer[i] = '\0';
            i = 0;

            if (isKeyword(buffer))
                printf("Keyword: %s\n", buffer);
            else
                printf("Identifier: %s\n", buffer);

            if (ch != EOF) ungetc(ch, fp);
        }

        // -------- NUMBER --------
        else if (isdigit(ch)) {
            buffer[i++] = ch;

            while ((ch = fgetc(fp)) != EOF && (isdigit(ch) || ch=='.')) {
                buffer[i++] = ch;
            }

            buffer[i] = '\0';
            i = 0;

            printf("Number: %s\n", buffer);

            if (ch != EOF) ungetc(ch, fp);
        }

        // -------- STRING --------
        else if (ch == '"' || ch == '\'') {
            char quote = ch;
            buffer[i++] = ch;

            while ((ch = fgetc(fp)) != EOF && ch != quote) {
                buffer[i++] = ch;
            }

            buffer[i++] = ch;
            buffer[i] = '\0';
            i = 0;

            printf("String: %s\n", buffer);
        }

        // -------- COMMENT --------
        else if (ch == '#') {
            buffer[i++] = ch;

            while ((ch = fgetc(fp)) != EOF && ch != '\n') {
                buffer[i++] = ch;
            }

            buffer[i] = '\0';
            i = 0;

            printf("Comment: %s\n", buffer);
        }

        // -------- OPERATOR --------
        else if (isOperator(ch)) {
            char next = fgetc(fp);

            if ((ch=='=' && next=='=') ||
                (ch=='!' && next=='=') ||
                (ch=='<' && next=='=') ||
                (ch=='>' && next=='=')) {

                printf("Operator: %c%c\n", ch, next);
            } else {
                printf("Operator: %c\n", ch);
                if (next != EOF) ungetc(next, fp);
            }
        }

        // -------- DELIMITER --------
        else if (isDelimiter(ch)) {
            printf("Delimiter: %c\n", ch);
        }

        // -------- IGNORE SPACE --------
        else if (isspace(ch)) {
            continue;
        }

        // -------- UNKNOWN --------
        else {
            printf("Unknown: %c\n", ch);
        }
    }

    fclose(fp);
    return 0;
}