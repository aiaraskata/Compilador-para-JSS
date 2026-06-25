grammar JSSimplificado;

// ============================================================================
// REGRAS SINTATICAS
// ============================================================================

// Um programa JSS pode conter declaracoes globais e comandos soltos no escopo
// global. A funcao main e facultativa, portanto nao aparece como obrigatoria.
prog
    : (decl | stmt)* EOF
    ;

decl
    : varDecl
    | funcDecl
    | classDecl
    ;

// Declaracoes primitivas, vetores e objetos.
//
// A alternativa VarSimples tambem reconhece a declaracao de uma lista de
// identificadores, por exemplo: let int a, b, c;
varDecl
    : (LET | CONST) tipo ID (ASSIGN expr | (COMMA ID)*) SEMI
                                                                # VarSimples
    | (LET | CONST) tipo dimensoes ID
        (ASSIGN (inicializadorVetor | expr))? SEMI
                                                                # VarVetor
    | (LET | CONST) ID ID (ASSIGN expr)? SEMI                    # VarObjeto
    ;

funcDecl
    : FUNCTION tipoRetorno ID LPAREN paramList? RPAREN bloco
    ;

tipoRetorno
    : tipo dimensoes?
    | ID
    | VOID
    ;

paramList
    : param (COMMA param)*
    ;

param
    : tipo (dimensoes | dimensoesVazias)? ID
    | ID ID
    ;

// Vetores podem possuir uma ou mais dimensoes. Na declaracao, cada dimensao
// informa seu tamanho; nos parametros, somente a quantidade de dimensoes.
dimensoes
    : (LBRACK expr RBRACK)+
    ;

dimensoesVazias
    : (LBRACK RBRACK)+
    ;

// Inicializadores podem ser aninhados para representar vetores
// multidimensionais, por exemplo: [[1, 2], [3, 4]].
inicializadorVetor
    : LBRACK (elementoVetor (COMMA elementoVetor)*)? RBRACK
    ;

elementoVetor
    : expr
    | inicializadorVetor
    ;

// Classes possuem atributos antes do construtor e dos metodos.
classDecl
    : CLASS ID LBRACE atributo* constructorDecl metodoDecl* RBRACE
    ;

atributo
    : tipo dimensoes? ID SEMI
    | ID ID SEMI
    ;

constructorDecl
    : ID CONSTRUCTOR LPAREN paramList? RPAREN bloco
    ;

stmtConstructor
    : THIS DOT ID ASSIGN expr SEMI
    ;

metodoDecl
    : tipoRetorno ID LPAREN paramList? RPAREN bloco
    ;

bloco
    : LBRACE stmt* RBRACE
    ;

stmt
    : varDecl                                                     # StmtVarDecl
    | ID atribComp expr SEMI                                      # StmtAssign
    | ID indices atribComp expr SEMI                              # StmtVetorAssign
    | (ID | THIS) DOT ID indices atribComp expr SEMI              # StmtVetorObjetoAssign
    | (ID | THIS) DOT ID atribComp expr SEMI                      # StmtAtribObjeto
    | IF LPAREN expr RPAREN bloco
        (ELSE IF LPAREN expr RPAREN bloco)*
        (ELSE bloco)?                                             # StmtIf
    | WHILE LPAREN expr RPAREN bloco                              # StmtWhile
    | FOR LPAREN forInit? SEMI expr? SEMI forUpdate? RPAREN bloco # StmtFor
    | BREAK SEMI                                                  # StmtBreak
    | RETURN expr? SEMI                                           # StmtReturn
    | chamadaFuncao SEMI                                          # StmtChamada
    | consolelog SEMI                                             # StmtConsoleLog
    | inputStmt SEMI                                              # StmtInput
    | op=(INC | DEC) ID SEMI                                      # StmtIncDec
    ;

atribComp
    : ASSIGN
    | MAIS_IG
    | MENOS_IG
    | MULT_IG
    | DIV_IG
    | MOD_IG
    ;

// No cabecalho do for a declaracao nao consome o primeiro ponto e virgula.
forInit
    : (LET | CONST) tipo ID (ASSIGN expr | (COMMA ID)*)
    | (LET | CONST) tipo dimensoes ID
        (ASSIGN (inicializadorVetor | expr))?
    | (LET | CONST) ID ID (ASSIGN expr)?
    | ID atribComp expr
    ;

forUpdate
    : ID atribComp expr
    | op=(INC | DEC) ID
    ;

indices
    : (LBRACK expr RBRACK)+
    ;

chamadaFuncao
    : ID LPAREN exprList? RPAREN
    | (ID | THIS) DOT ID LPAREN exprList? RPAREN
    | casting
    ;

casting
    : tipo LPAREN expr RPAREN
    ;

consolelog
    : CONSOLE DOT LOG LPAREN exprList? RPAREN
    ;

inputStmt
    : INPUT LPAREN idList RPAREN
    ;

idList
    : ID (COMMA ID)*
    ;

exprList
    : expr (COMMA expr)*
    ;

// A ordem das alternativas recursivas define a precedencia. Exponenciacao e
// atribuicao sao associativas a direita; os demais operadores binarios sao
// associativos a esquerda.
expr
    : op=(INC | DEC) expr                                         # ExprIncDec
    | op=(NOT | PLUS | MINUS) expr                                # ExprUnary
    | LPAREN expr RPAREN                                          # ExprParen
    | NEW ID LPAREN exprList? RPAREN                              # ExprNew
    | chamadaFuncao                                               # ExprChamada
    | ID indices                                                 # ExprVetor
    | (ID | THIS) DOT ID indices                                 # ExprVetorObjeto
    | (ID | THIS) DOT ID                                         # ExprAtribObjeto
    | INT_LIT                                                     # ExprInt
    | REAL_LIT                                                    # ExprReal
    | STR_LIT                                                     # ExprStr
    | BOOL_LIT                                                    # ExprBool
    | NULL                                                        # ExprNull
    | ID                                                          # ExprId
    | <assoc=right> expr op=POW expr                              # ExprPow
    | expr op=(MULT | DIV) expr                                   # ExprMulDiv
    | expr op=MOD expr                                            # ExprMod
    | expr op=(PLUS | MINUS) expr                                 # ExprAddSub
    | expr op=(GT | GTE | LT | LTE) expr                          # ExprRel
    | expr op=(EQ | NEQ) expr                                     # ExprEq
    | expr op=AND expr                                            # ExprAnd
    | expr op=OR expr                                             # ExprOr
    | <assoc=right> expr op=(ASSIGN | MAIS_IG | MENOS_IG
        | MULT_IG | DIV_IG | MOD_IG) expr                         # ExprAtrib
    ;

tipo
    : INT_TYPE
    | REAL_TYPE
    | STR_TYPE
    | BOOL_TYPE
    ;


// ============================================================================
// REGRAS LEXICAS
// ============================================================================

// Tipos primitivos
INT_TYPE  : 'int';
REAL_TYPE : 'real';
STR_TYPE  : 'str';
BOOL_TYPE : 'bool';

// Palavras reservadas
LET         : 'let';
CONST       : 'const';
FUNCTION    : 'function';
RETURN      : 'return';
IF          : 'if';
ELSE        : 'else';
WHILE       : 'while';
FOR         : 'for';
BREAK       : 'break';
CLASS       : 'class';
NEW         : 'new';
THIS        : 'this';
CONSTRUCTOR : 'constructor';
VOID        : 'void';
NULL        : 'null';
CONSOLE     : 'console';
LOG         : 'log';
INPUT       : 'input';

// Literais
BOOL_LIT : 'true' | 'false';
REAL_LIT : DIGIT+ '.' DIGIT+ ([eE] [+-]? DIGIT+)?;
INT_LIT  : DIGIT+;
STR_LIT  : '"' (ESC_SEQ | ~["\\\r\n])* '"';

// Operadores. Os compostos aparecem antes dos seus prefixos simples.
INC      : '++';
DEC      : '--';
POW      : '**';
MAIS_IG  : '+=';
MENOS_IG : '-=';
MULT_IG  : '*=';
DIV_IG   : '/=';
MOD_IG   : '%=';
EQ       : '==';
NEQ      : '!=';
GTE      : '>=';
LTE      : '<=';
AND      : '&&';
OR       : '||';
GT       : '>';
LT       : '<';
NOT      : '!';
PLUS     : '+';
MINUS    : '-';
MULT     : '*';
DIV      : '/';
MOD      : '%';
ASSIGN   : '=';

// Delimitadores
SEMI   : ';';
COMMA  : ',';
DOT    : '.';
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
LBRACK : '[';
RBRACK : ']';

// Identificadores sao case-sensitive e nao podem comecar com digito.
ID : [a-zA-Z_] [a-zA-Z0-9_]*;

// A especificacao admite apenas comentarios de linha.
LINE_COMMENT : '//' ~[\r\n]* -> skip;
WS           : [ \t\r\n]+ -> skip;

fragment DIGIT   : [0-9];
fragment ESC_SEQ : '\\' .;
