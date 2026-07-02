from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from JSSimplificadoLexer import JSSimplificadoLexer
from JSSimplificadoParser import JSSimplificadoParser
from AnalisadorSemantico import analisar_arvore
from GeradorIR import ErroGeracaoIR, gerar_jasmin


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
    if len(sys.argv) < 2:
        print("Uso: python3 compilador.py <arquivo.jss>")
        print("Uso: python3 compilador.py --jasmin <arquivo.jss> [saida.j]")
        return 1

    modo_jasmin = sys.argv[1] == "--jasmin"
    if (not modo_jasmin and len(sys.argv) != 2) or (modo_jasmin and len(sys.argv) not in (3, 4)):
        print("Uso: python3 compilador.py <arquivo.jss>")
        print("Uso: python3 compilador.py --jasmin <arquivo.jss> [saida.j]")
        return 1

    caminho_entrada = sys.argv[2] if modo_jasmin else sys.argv[1]

    try:
        with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
            codigo = arquivo.read()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_entrada}' nao encontrado.")
        return 1

    diagnosticos = analisar_codigo(codigo)

    if diagnosticos:
        for diagnostico in diagnosticos:
            print(diagnostico.formatar())
        print("Programa rejeitado.")
        return 1

    if modo_jasmin:
        caminho_fonte = Path(caminho_entrada)
        caminho_saida = (
            Path(sys.argv[3])
            if len(sys.argv) == 4
            else Path("codigo_intermediario") / f"{caminho_fonte.stem}.j"
        )
        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        try:
            codigo_jasmin = gerar_jasmin(codigo, caminho_fonte.stem)
        except ErroGeracaoIR as erro:
            print(f"Erro na geracao de IR: {erro}")
            return 1
        with open(caminho_saida, "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo_jasmin)
        print(f"Codigo Jasmin gerado em: {caminho_saida}")
        return 0

    print("Programa aceito: analises lexica, sintatica e semantica concluidas com sucesso.")
    return 0


if __name__ == "__main__":

    raise SystemExit(main())
