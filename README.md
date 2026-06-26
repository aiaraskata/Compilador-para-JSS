# Compilador JSS — Front-end

Front-end para a linguagem Java Script Simplificado (JSS), implementado em
Python com ANTLR 4.

O projeto realiza análise léxica, sintática e semântica. O compilador recebe o
caminho de um arquivo `.jss`, lê o conteúdo com `open`, executa as análises e
informa se o programa foi aceito ou rejeitado. Em caso de erro, a saída indica
categoria, linha e coluna.

## Requisitos

- Python 3.10 ou superior
- Dependências de `requirements.txt`

Java só é necessário para regenerar os arquivos Python do ANTLR depois de
alterar a gramática.

## Instalação

Opcionalmente, crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale a dependência:

```bash
pip install -r requirements.txt
```

## Execução

Execute informando o caminho do arquivo de entrada:

```bash
python3 compilador.py testes/1_basics.jss
```

Saída para programa aceito:

```text
Programa aceito: analises lexica, sintatica e semantica concluidas com sucesso.
```

Saída para programa rejeitado:

```text
Linha 19, coluna 1: erro semantico: 'break' so pode ser usado dentro de laco 'while' ou 'for'.
Programa rejeitado.
```

O processo retorna código `0` para programas aceitos e `1` para programas
rejeitados.

## Como a entrada é lida

O compilador não lê mais o código-fonte pela entrada padrão. Ele recebe o nome
do arquivo pela linha de comando e abre o arquivo com `open`:

```python
with open(caminho, "r", encoding="utf-8") as arquivo:
    codigo = arquivo.read()
```

Depois disso, o conteúdo lido é entregue ao ANTLR por meio de `InputStream`.

## Etapas implementadas

### Análise léxica

Reconhece palavras reservadas, identificadores, literais, operadores,
delimitadores e comentários de linha. Erros léxicos são coletados e exibidos
com linha e coluna.

### Análise sintática

Usa a gramática `JSSimplificado.g4` para gerar a árvore sintática. A regra
inicial do programa é:

```antlr
prog
    : (decl | stmt)* EOF
    ;
```

Essa decisão permite tanto declarações quanto comandos soltos no escopo global,
aproximando o comportamento da sintaxe de JavaScript usada nos testes.

### Análise semântica

Percorre a árvore usando `JSSimplificadoVisitor` e valida regras como:

- identificador usado antes da declaração;
- redeclaração no mesmo escopo;
- escopos de blocos, funções, métodos e laços;
- constantes não podem ser reatribuídas;
- condições de `if`, `while` e `for` devem ser booleanas;
- `break` só pode aparecer dentro de `while` ou `for`;
- tipos em operações aritméticas, lógicas e relacionais;
- compatibilidade em atribuições;
- chamadas de funções/métodos com quantidade, tipo e dimensões corretas;
- funções e métodos não-`void` devem ter `return` com valor;
- funções `void` não devem retornar valor;
- uso de arrays e matrizes com quantidade correta de índices;
- uso básico de classes, objetos, atributos, métodos e `this`.

## Recursos reconhecidos

- tipos primitivos `int`, `real`, `str` e `bool`;
- variáveis e constantes com `let` e `const`;
- listas de identificadores, como `let int a, b, c;`;
- arrays e matrizes;
- arrays multidimensionais;
- arrays como parâmetro e retorno de função;
- classes, atributos, construtores, métodos, `new`, `this` e `null`;
- atributos de classe que podem ser arrays/matrizes;
- funções, parâmetros, chamadas e recursão;
- comandos soltos no escopo global;
- atribuições simples e compostas: `=`, `+=`, `-=`, `*=`, `/=`, `%=`;
- operadores aritméticos, relacionais e lógicos;
- `if`, `else if`, `else`, `while`, `for`, `break` e `return`;
- `input` e `console.log`;
- conversões explícitas entre tipos primitivos;
- comentários de linha iniciados por `//`.

## Casting

O casting é reconhecido pela gramática como uma chamada especial:

```antlr
casting
    : tipo LPAREN expr RPAREN
    ;
```

Exemplos aceitos:

```jss
let int x = int(3.14);
let real y = real(10);
let str texto = str(x);
let bool flag = bool(1);
```

Na análise semântica, a expressão interna é visitada para detectar possíveis
erros, e o tipo resultante passa a ser o tipo indicado no cast. Por exemplo,
`real(10)` é tratado como uma expressão de tipo `real`.

Decisão implementada: os casts seguem a proposta de conversão explícita entre
tipos primitivos da especificação. Conversões para `str` são aceitas para
valores primitivos, e conversões entre `int`, `real` e `bool` são tratadas como
intercambiáveis.

## Decisões de projeto além do PDF

Algumas escolhas foram feitas para atender aos testes e ao comportamento
esperado durante a apresentação:

- Comandos soltos no escopo global são aceitos, não apenas declarações globais.
- Arrays podem ter mais de uma dimensão.
- Funções podem receber arrays com dimensão fixa, por exemplo `int[5] arr`.
- Funções podem retornar arrays, por exemplo `function int[5] criarSequencia(...)`.
- Arrays podem ser inicializados por chamada de função, como
  `let int[5] sequencia = criarSequencia(100);`.
- Classes podem ter atributos que são arrays/matrizes.
- Constructors aceitam bloco comum de comandos, permitindo `for`, `while`,
  `console.log` etc.
- Acesso a array em atributo de objeto ou `this` é aceito, por exemplo
  `this.matriz[i][j]`.

Essas decisões tornam a linguagem um pouco mais permissiva que a descrição
mínima do PDF, mas preservam a ideia de JavaScript Simplificado usada nos testes.

## Exemplos de execução

Programas esperados como sucesso:

```bash
python3 compilador.py testes/1_basics.jss
python3 compilador.py testes/3_control_flow.jss
python3 compilador.py testes/4_strings_casts.jss
python3 compilador.py testes/5_classes.jss
python3 compilador.py testes/6_functions.jss
```

Programas esperados como erro:

```bash
python3 compilador.py testes/7_errors.jss
python3 compilador.py testes/8_erros_funcao.jss
```

## Regeneração do ANTLR

Após modificar `JSSimplificado.g4`, execute:

```bash
java -jar antlr-4.13.2-complete.jar \
  -Dlanguage=Python3 -visitor JSSimplificado.g4
```

Isso atualiza `JSSimplificadoLexer.py`, `JSSimplificadoParser.py`,
`JSSimplificadoListener.py`, `JSSimplificadoVisitor.py`, arquivos `.tokens` e
arquivos `.interp`.
