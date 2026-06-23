# Compilador JSS — Front-end

Front-end para a linguagem Java Script Simplificado (JSS), implementado em
Python com ANTLR 4.

Nesta versão são executadas as análises léxica e sintática exigidas para a
apresentação prévia da primeira etapa. O programa fonte é lido pela entrada
padrão e o resultado é escrito na saída padrão.

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

O compilador lê exclusivamente da entrada padrão:

```bash
python3 compilador.py < exemplos/sucesso.jss
```

Saída:

```text
Programa aceito: analise lexica e sintatica concluida com sucesso.
```

Também é possível usar um pipe:

```bash
printf 'function void main() {}' | python3 compilador.py
```

Quando existe um erro, são apresentados sua categoria, linha e coluna:

```bash
python3 compilador.py < exemplos/erro_lexico.jss
python3 compilador.py < exemplos/erro_sintatico.jss
```

Exemplo de diagnóstico:

```text
Linha 2, coluna 25: erro lexico: token recognition error at: '@'
Programa rejeitado.
```

O processo retorna código `0` para programas aceitos e `1` para programas
rejeitados.

## Recursos sintáticos reconhecidos

- tipos `int`, `real`, `str` e `bool`;
- variáveis, constantes, listas de identificadores, vetores
  multidimensionais e objetos;
- funções, parâmetros, chamadas e recursão;
- classes, atributos, construtores, métodos, `new`, `this` e `null`;
- atribuições simples e compostas;
- operadores aritméticos, relacionais e lógicos;
- `if`, `else if`, `else`, `while`, `for`, `break` e `return`;
- `input`, `console.log` e conversões entre tipos primitivos;
- comentários de linha iniciados por `//`.

## Regeneração do ANTLR

Após modificar `JSSimplificado.g4`, execute:

```bash
java -jar antlr-4.13.2-complete.jar \
  -Dlanguage=Python3 -visitor JSSimplificado.g4
```

Isso atualiza `JSSimplificadoLexer.py`, `JSSimplificadoParser.py`,
`JSSimplificadoListener.py`, `JSSimplificadoVisitor.py`, arquivos `.tokens` e
arquivos `.interp`.
