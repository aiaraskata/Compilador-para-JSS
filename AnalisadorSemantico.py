from __future__ import annotations

import sys
from dataclasses import dataclass

from antlr4 import CommonTokenStream, FileStream

from JSSimplificadoLexer import JSSimplificadoLexer
from JSSimplificadoParser import JSSimplificadoParser
from JSSimplificadoVisitor import JSSimplificadoVisitor


@dataclass(frozen=True)
class DiagnosticoSemantico:
    linha: int
    coluna: int
    mensagem: str
    categoria: str = "semantico"

    def formatar(self) -> str:
        return (
            f"Linha {self.linha}, coluna {self.coluna + 1}: "
            f"erro {self.categoria}: {self.mensagem}"
        )


@dataclass(frozen=True)
class Simbolo:
    nome: str
    categoria: str
    tipo: str
    linha: int
    dimensoes: int = 0


class TabelaDeSimbolos:
    def __init__(self) -> None:
        self.escopos: list[dict[str, Simbolo]] = [{}]

    def abrir_escopo(self) -> None:
        self.escopos.append({})

    def fechar_escopo(self) -> None:
        if len(self.escopos) > 1:
            self.escopos.pop()

    def declarar(self, simbolo: Simbolo) -> Simbolo | None:
        escopo_atual = self.escopos[-1]
        existente = escopo_atual.get(simbolo.nome)

        if existente is None:
            escopo_atual[simbolo.nome] = simbolo

        return existente

    def buscar(self, nome: str) -> Simbolo | None:
        for escopo in reversed(self.escopos):
            simbolo = escopo.get(nome)
            if simbolo is not None:
                return simbolo
        return None


class AnalisadorSemantico(JSSimplificadoVisitor):
    def __init__(self) -> None:
        self.tabela = TabelaDeSimbolos()
        self.diagnosticos: list[DiagnosticoSemantico] = []

    @property
    def erros(self) -> int:
        return len(self.diagnosticos)

    def erro(self, token, mensagem: str) -> None:
        self.diagnosticos.append(
            DiagnosticoSemantico(
                linha=token.line,
                coluna=token.column,
                mensagem=mensagem,
            )
        )

    def declarar(self, token, categoria: str, tipo: str, dimensoes: int = 0) -> None:
        nome = token.getText()
        existente = self.tabela.declarar(
            Simbolo(
                nome=nome,
                categoria=categoria,
                tipo=tipo,
                linha=token.symbol.line,
                dimensoes=dimensoes,
            )
        )

        if existente is not None:
            self.erro(
                token.symbol,
                (
                    f"'{nome}' ja foi declarado neste escopo "
                    f"como {existente.categoria} na linha {existente.linha}."
                ),
            )

    def exigir_declarado(
        self,
        token,
        categorias: set[str] | None = None,
        descricao: str = "identificador",
    ) -> Simbolo | None:
        nome = token.getText()
        simbolo = self.tabela.buscar(nome)

        if simbolo is None:
            self.erro(token.symbol, f"{descricao} '{nome}' nao foi declarado.")
            return None

        if categorias is not None and simbolo.categoria not in categorias:
            categorias_validas = ", ".join(sorted(categorias))
            self.erro(
                token.symbol,
                (
                    f"'{nome}' foi declarado como {simbolo.categoria}, "
                    f"mas aqui era esperado: {categorias_validas}."
                ),
            )

        return simbolo

    def texto_tipo_retorno(self, ctx: JSSimplificadoParser.TipoRetornoContext) -> str:
        return ctx.getText()

    def texto_tipo_parametro(self, ctx: JSSimplificadoParser.ParamContext) -> str:
        if ctx.tipo() is not None:
            return ctx.tipo().getText()
        return ctx.ID(0).getText()

    def texto_tipo_var_objeto(self, ctx: JSSimplificadoParser.VarObjetoContext) -> str:
        return ctx.ID(0).getText()

    def quantidade_dimensoes(self, ctx) -> int:
        if ctx is None:
            return 0
        return len(ctx.LBRACK())

    def visitProg(self, ctx: JSSimplificadoParser.ProgContext):
        for decl in ctx.decl():
            funcao = decl.funcDecl()
            classe = decl.classDecl()

            if funcao is not None:
                self.declarar(
                    funcao.ID(),
                    "funcao",
                    self.texto_tipo_retorno(funcao.tipoRetorno()),
                )
            elif classe is not None:
                self.declarar(classe.ID(), "classe", classe.ID().getText())

        for decl in ctx.decl():
            self.visit(decl)

        return None

    def visitVarSimples(self, ctx: JSSimplificadoParser.VarSimplesContext):
        tipo = ctx.tipo().getText()
        ids = ctx.ID()

        for token_id in ids:
            self.declarar(token_id, "variavel", tipo)

        if ctx.expr() is not None:
            self.visit(ctx.expr())

        return None

    def visitVarVetor(self, ctx: JSSimplificadoParser.VarVetorContext):
        self.declarar(
            ctx.ID(),
            "variavel",
            ctx.tipo().getText(),
            self.quantidade_dimensoes(ctx.dimensoes()),
        )
        self.visit(ctx.dimensoes())

        if ctx.inicializadorVetor() is not None:
            self.visit(ctx.inicializadorVetor())

        return None

    def visitVarObjeto(self, ctx: JSSimplificadoParser.VarObjetoContext):
        self.exigir_declarado(ctx.ID(0), {"classe"}, "classe")
        self.declarar(ctx.ID(1), "variavel", self.texto_tipo_var_objeto(ctx))

        if ctx.expr() is not None:
            self.visit(ctx.expr())

        return None

    def visitFuncDecl(self, ctx: JSSimplificadoParser.FuncDeclContext):
        self.tabela.abrir_escopo()

        if ctx.paramList() is not None:
            self.visit(ctx.paramList())

        self.visit(ctx.bloco())
        self.tabela.fechar_escopo()
        return None

    def visitParam(self, ctx: JSSimplificadoParser.ParamContext):
        ids = ctx.ID()
        nome = ids[-1]
        tipo = self.texto_tipo_parametro(ctx)

        if ctx.tipo() is None and len(ids) >= 2:
            self.exigir_declarado(ids[0], {"classe"}, "classe")

        self.declarar(
            nome,
            "parametro",
            tipo,
            self.quantidade_dimensoes(ctx.dimensoesVazias()),
        )
        return None

    def visitClassDecl(self, ctx: JSSimplificadoParser.ClassDeclContext):
        self.tabela.abrir_escopo()

        for atributo in ctx.atributo():
            self.visit(atributo)

        self.visit(ctx.constructorDecl())

        for metodo in ctx.metodoDecl():
            self.visit(metodo)

        self.tabela.fechar_escopo()
        return None

    def visitAtributo(self, ctx: JSSimplificadoParser.AtributoContext):
        ids = ctx.ID()

        if ctx.tipo() is not None:
            tipo = ctx.tipo().getText()
            nome = ids[0]
        else:
            self.exigir_declarado(ids[0], {"classe"}, "classe")
            tipo = ids[0].getText()
            nome = ids[1]

        self.declarar(nome, "atributo", tipo)
        return None

    def visitConstructorDecl(self, ctx: JSSimplificadoParser.ConstructorDeclContext):
        self.tabela.abrir_escopo()

        if ctx.paramList() is not None:
            self.visit(ctx.paramList())

        for stmt in ctx.stmtConstructor():
            self.visit(stmt)

        self.tabela.fechar_escopo()
        return None

    def visitMetodoDecl(self, ctx: JSSimplificadoParser.MetodoDeclContext):
        self.declarar(
            ctx.ID(),
            "metodo",
            self.texto_tipo_retorno(ctx.tipoRetorno()),
        )
        self.tabela.abrir_escopo()

        if ctx.paramList() is not None:
            self.visit(ctx.paramList())

        self.visit(ctx.bloco())
        self.tabela.fechar_escopo()
        return None

    def visitBloco(self, ctx: JSSimplificadoParser.BlocoContext):
        self.tabela.abrir_escopo()

        for stmt in ctx.stmt():
            self.visit(stmt)

        self.tabela.fechar_escopo()
        return None

    def visitStmtAssign(self, ctx: JSSimplificadoParser.StmtAssignContext):
        self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        self.visit(ctx.expr())
        return None

    def visitStmtVetorAssign(self, ctx: JSSimplificadoParser.StmtVetorAssignContext):
        self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        self.visit(ctx.indices())
        self.visit(ctx.expr())
        return None

    def visitStmtAtribObjeto(self, ctx: JSSimplificadoParser.StmtAtribObjetoContext):
        if ctx.THIS() is None:
            self.exigir_declarado(ctx.ID(0), {"variavel", "parametro", "atributo"})
        self.visit(ctx.expr())
        return None

    def visitStmtIf(self, ctx: JSSimplificadoParser.StmtIfContext):
        for expr in ctx.expr():
            self.visit(expr)

        for bloco in ctx.bloco():
            self.visit(bloco)

        return None

    def visitStmtWhile(self, ctx: JSSimplificadoParser.StmtWhileContext):
        self.visit(ctx.expr())
        self.visit(ctx.bloco())
        return None

    def visitStmtFor(self, ctx: JSSimplificadoParser.StmtForContext):
        self.tabela.abrir_escopo()

        if ctx.forInit() is not None:
            self.visit(ctx.forInit())
        if ctx.expr() is not None:
            self.visit(ctx.expr())
        if ctx.forUpdate() is not None:
            self.visit(ctx.forUpdate())

        self.visit(ctx.bloco())
        self.tabela.fechar_escopo()
        return None

    def visitForInit(self, ctx: JSSimplificadoParser.ForInitContext):
        ids = ctx.ID()

        if ctx.LET() is not None or ctx.CONST() is not None:
            if ctx.tipo() is not None:
                tipo = ctx.tipo().getText()
                for token_id in ids:
                    self.declarar(
                        token_id,
                        "variavel",
                        tipo,
                        self.quantidade_dimensoes(ctx.dimensoes()),
                    )
            elif len(ids) >= 2:
                self.exigir_declarado(ids[0], {"classe"}, "classe")
                self.declarar(ids[1], "variavel", ids[0].getText())
        elif ids:
            self.exigir_declarado(ids[0], {"variavel", "parametro", "atributo"})

        if ctx.expr() is not None:
            self.visit(ctx.expr())
        if ctx.dimensoes() is not None:
            self.visit(ctx.dimensoes())
        if ctx.inicializadorVetor() is not None:
            self.visit(ctx.inicializadorVetor())

        return None

    def visitForUpdate(self, ctx: JSSimplificadoParser.ForUpdateContext):
        self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})

        if ctx.expr() is not None:
            self.visit(ctx.expr())

        return None

    def visitStmtIncDec(self, ctx: JSSimplificadoParser.StmtIncDecContext):
        self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        return None

    def visitInputStmt(self, ctx: JSSimplificadoParser.InputStmtContext):
        for token_id in ctx.idList().ID():
            self.exigir_declarado(token_id, {"variavel", "parametro", "atributo"})
        return None

    def visitChamadaFuncao(self, ctx: JSSimplificadoParser.ChamadaFuncaoContext):
        if ctx.casting() is not None:
            self.visit(ctx.casting())
            return None

        if ctx.DOT() is not None:
            if ctx.THIS() is None:
                self.exigir_declarado(
                    ctx.ID(0),
                    {"variavel", "parametro", "atributo"},
                    "objeto",
                )
        else:
            self.exigir_declarado(ctx.ID(0), {"funcao"}, "funcao")

        if ctx.exprList() is not None:
            self.visit(ctx.exprList())

        return None

    def visitExprId(self, ctx: JSSimplificadoParser.ExprIdContext):
        self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        return None

    def visitExprVetor(self, ctx: JSSimplificadoParser.ExprVetorContext):
        self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        self.visit(ctx.indices())
        return None

    def visitExprAtribObjeto(self, ctx: JSSimplificadoParser.ExprAtribObjetoContext):
        if ctx.THIS() is None:
            self.exigir_declarado(
                ctx.ID(0),
                {"variavel", "parametro", "atributo"},
                "objeto",
            )
        return None

    def visitExprNew(self, ctx: JSSimplificadoParser.ExprNewContext):
        self.exigir_declarado(ctx.ID(), {"classe"}, "classe")

        if ctx.exprList() is not None:
            self.visit(ctx.exprList())

        return None


def analisar_arvore(tree) -> list[DiagnosticoSemantico]:
    analisador = AnalisadorSemantico()
    analisador.visit(tree)
    return sorted(
        analisador.diagnosticos,
        key=lambda erro: (erro.linha, erro.coluna, erro.categoria),
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python ./AnalisadorSemantico.py <arquivo.jss>")
        return 1

    entrada = FileStream(sys.argv[1], encoding="utf-8")
    lexer = JSSimplificadoLexer(entrada)
    tokens = CommonTokenStream(lexer)
    parser = JSSimplificadoParser(tokens)
    tree = parser.prog()

    diagnosticos = analisar_arvore(tree)

    if diagnosticos:
        for diagnostico in diagnosticos:
            print(diagnostico.formatar())
        print("Programa rejeitado.")
        return 1

    print("Programa aceito: analise semantica concluida com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
