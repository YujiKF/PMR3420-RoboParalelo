// GCode.g4
// Gramática ANTLR para um subconjunto de Código G

grammar GCode;

// --- Regras do Parser ---

// Regra inicial: um programa G-Code é uma sequência de sentenças e um final de programa
program : (statement EOL)* programEnd EOF;

// Uma sentença é uma linha de código G que pode ter um número de linha opcional
statement : (LINE_NUMBER)? gcodeCommand;

// Comandos G-Code
gcodeCommand
    : G00 (X VALUE)? (Y VALUE)?
    | G01 (X VALUE)? (Y VALUE)?
    | G02 (X VALUE)? (Y VALUE)? ((I VALUE) (J VALUE) | (R VALUE))? // G02/G03 podem ter I/J ou R
    | G03 (X VALUE)? (Y VALUE)? ((I VALUE) (J VALUE) | (R VALUE))?
    | M30
    ;

// Fim do programa
programEnd : M30;

// --- Regras do Lexer (Tokens) ---

// Tokens para os códigos de função G
G00 : 'G00';
G01 : 'G01';
G02 : 'G02';
G03 : 'G03';

// Token para o código de função M
M30 : 'M30';

// Tokens para as coordenadas e parâmetros
X : 'X';
Y : 'Y';
I : 'I';
J : 'J';
R : 'R';

// Número de linha (N seguido por dígitos)
LINE_NUMBER : 'N' DIGITS;

// Valor numérico: pode ser inteiro ou de ponto flutuante
VALUE : (SIGN)? DIGITS ('.' DIGITS)?;

// Caracteres auxiliares
SIGN : '+' | '-';
DIGITS : [0-9]+; // Um ou mais dígitos

// Fim de linha (Windows, Unix)
EOL : '\r'? '\n';

// Ignorar espaços em branco
WS : [ \t]+ -> skip;