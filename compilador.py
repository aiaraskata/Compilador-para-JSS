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
    codigo = sys.stdin.read()
    diagnosticos = analisar_codigo(codigo)

    if diagnosticos:
        for diagnostico in diagnosticos:
            print(diagnostico.formatar())
        print("Programa rejeitado.")
        return 1

    print("Programa aceito: analises lexica, sintatica e semantica concluidas com sucesso.")
    return 0


if __name__ == "__main__":

    raise SystemExit(main())
