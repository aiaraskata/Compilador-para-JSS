from __future__ import annotations

import sys
from dataclasses import dataclass

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from JSSimplificadoLexer import JSSimplificadoLexer
from JSSimplificadoParser import JSSimplificadoParser
from AnalisadorSemantico import analisar_arvore


@dataclass(frozen=True)
class Diagnostico:
    categoria: str
    linha: int
    coluna: int
    mensagem: str

    def formatar(self) -> str:
        return (
            f"Linha {self.linha}, coluna {self.coluna + 1}: "
            f"erro {self.categoria}: {self.mensagem}"
        )


class ColetorDeErros(ErrorListener):
    def __init__(self, categoria: str) -> None:
        super().__init__()
        self.categoria = categoria
        self.diagnosticos: list[Diagnostico] = []

    def syntaxError(
        self,
        recognizer,
        offendingSymbol,
        line: int,
        column: int,
        msg: str,
        e,
    ) -> None:
        self.diagnosticos.append(
            Diagnostico(
                categoria=self.categoria,
                linha=line,
                coluna=column,
                mensagem=msg,
            )
        )


def analisar_codigo(codigo: str) -> list[Diagnostico]:
    entrada = InputStream(codigo)
    return analisar_entrada(entrada)


def analisar_arquivo(caminho: str) -> list[Diagnostico]:
    with open(caminho, "r", encoding="utf-8") as arquivo:
        codigo = arquivo.read()
    return analisar_codigo(codigo)


def analisar_entrada(entrada) -> list[Diagnostico]:

    erros_lexicos = ColetorDeErros("lexico")
    lexer = JSSimplificadoLexer(entrada)
    lexer.removeErrorListeners()
    lexer.addErrorListener(erros_lexicos)

    tokens = CommonTokenStream(lexer)

    erros_sintaticos = ColetorDeErros("sintatico")
    parser = JSSimplificadoParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(erros_sintaticos)
    tree = parser.prog()

    diagnosticos = (
        erros_lexicos.diagnosticos + erros_sintaticos.diagnosticos
    )
    if not diagnosticos:
        diagnosticos.extend(analisar_arvore(tree))

    return sorted(
        diagnosticos,
        key=lambda erro: (erro.linha, erro.coluna, erro.categoria),
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python3 compilador.py <arquivo.jss>")
        return 1

    try:
        diagnosticos = analisar_arquivo(sys.argv[1])
    except FileNotFoundError:
        print(f"Erro: arquivo '{sys.argv[1]}' nao encontrado.")
        return 1

    if diagnosticos:
        for diagnostico in diagnosticos:
            print(diagnostico.formatar())
        print("Programa rejeitado.")
        return 1

    print("Programa aceito: analises lexica, sintatica e semantica concluidas com sucesso.")
    return 0


if __name__ == "__main__":

    raise SystemExit(main())
