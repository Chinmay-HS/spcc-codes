%{
 #define Num 1
 #define Identifier 2
 #define Keyword 3
 #define Symbol 4
 #define Message 5
 #define Preprocessor 6
%}
%%
[0-9]+|[0-9]+\.[0-9]+ {return Num;}
[a-zA-Z_][a-zA-Z0-9_]* {
    if (strcmp(yytext, "if") == 0 || strcmp(yytext, "else") == 0 || strcmp(yytext, "while") == 0) 
        return Keyword;
    else 
        return Identifier;
}
[+\-*/=<>!&|^%] {return Symbol;}
\"[^\"]*\" {return Message;}
#[^\n]* {return Preprocessor;}
%%
#include <stdio.h>

int main(int argc, char *argv[]){
    int val;
    while (val = yylex()){
        switch(val){
            case 1:
                printf("\n%s Number : ", yytext);
                break;
            case 2:
                printf("\n%s Identifier : ", yytext);
                break;
            case 3:
                printf("\n%s Keyword : ", yytext);
                break;
            case 4:
                printf("\n%s Symbol : ", yytext);
                break;
            case 5:
                printf("\n%s Message : ", yytext);
                break;
            case 6:
                printf("\n%s Preprocessor Directive : ", yytext);
                break;
        }
    }
}

int yywrap(){
    return (1);
}

