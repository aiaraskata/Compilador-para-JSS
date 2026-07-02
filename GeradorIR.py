from __future__ import annotations

import re
from dataclasses import dataclass

from antlr4 import CommonTokenStream, InputStream

from JSSimplificadoLexer import JSSimplificadoLexer
from JSSimplificadoParser import JSSimplificadoParser
from JSSimplificadoVisitor import JSSimplificadoVisitor


@dataclass(frozen=True)
class ValorIR:
    tipo: str


@dataclass(frozen=True)
class SimboloIR:
    tipo: str
    indice: int
    is_const: bool = False


class ErroGeracaoIR(Exception):
    pass


def nome_classe_valido(nome: str) -> str:
    nome = re.sub(r"[^a-zA-Z0-9_]", "_", nome)
    if not nome or nome[0].isdigit():
        nome = f"Programa_{nome}"
    return nome


def gerar_jasmin(codigo: str, nome_classe: str = "Programa") -> str:
    entrada = InputStream(codigo)
    lexer = JSSimplificadoLexer(entrada)
    tokens = CommonTokenStream(lexer)
    parser = JSSimplificadoParser(tokens)
    tree = parser.prog()

    gerador = GeradorIR(nome_classe_valido(nome_classe))
    return gerador.gerar(tree)


class GeradorIR(JSSimplificadoVisitor):
    def __init__(self, nome_classe: str) -> None:
        self.nome_classe = nome_classe
        self.codigo: list[str] = []
        self.escopos: list[dict[str, SimboloIR]] = [{}]
        self.proximo_local = 1
        self.stack_limit = 64

    def gerar(self, tree) -> str:
        self.emit(f".class public {self.nome_classe}")
        self.emit(".super java/lang/Object")
        self.emit("")
        self.emit_metodo_construtor_padrao()
        self.emit_metodo_main_inicio()
        self.visit(tree)
        self.emit("return")
        self.emit(".end method")
        self.emit("")
        return "\n".join(self.codigo)

    def emit_metodo_construtor_padrao(self) -> None:
        self.emit(".method public <init>()V")
        self.emit("aload_0")
        self.emit("invokespecial java/lang/Object/<init>()V")
        self.emit("return")
        self.emit(".end method")
        self.emit("")

    def emit_metodo_main_inicio(self) -> None:
        self.emit(".method public static main([Ljava/lang/String;)V")
        self.emit(f".limit stack {self.stack_limit}")
        self.emit(".limit locals 256")

    def emit(self, linha: str) -> None:
        self.codigo.append(linha)

    def abrir_escopo(self) -> None:
        self.escopos.append({})

    def fechar_escopo(self) -> None:
        if len(self.escopos) > 1:
            self.escopos.pop()

    def declarar_variavel(self, nome: str, tipo: str, is_const: bool = False) -> SimboloIR:
        escopo_atual = self.escopos[-1]
        if nome in escopo_atual:
            raise ErroGeracaoIR(f"Variavel '{nome}' redeclarada no mesmo escopo.")

        simbolo = SimboloIR(
            tipo=tipo,
            indice=self.novo_local(tipo),
            is_const=is_const,
        )
        escopo_atual[nome] = simbolo
        return simbolo

    def buscar_variavel(self, nome: str) -> SimboloIR | None:
        for escopo in reversed(self.escopos):
            simbolo = escopo.get(nome)
            if simbolo is not None:
                return simbolo
        return None

    def novo_local(self, tipo: str) -> int:
        indice = self.proximo_local
        self.proximo_local += 2 if tipo == "real" else 1
        return indice

    def instrucao_load(self, simbolo: SimboloIR) -> str:
        if simbolo.tipo == "real":
            return "dload"
        if simbolo.tipo == "str":
            return "aload"
        return "iload"

    def instrucao_store(self, simbolo: SimboloIR) -> str:
        if simbolo.tipo == "real":
            return "dstore"
        if simbolo.tipo == "str":
            return "astore"
        return "istore"

    def descritor_print(self, tipo: str) -> str:
        if tipo == "real":
            return "D"
        if tipo == "str":
            return "Ljava/lang/String;"
        if tipo == "bool":
            return "Z"
        return "I"

    def emitir_valor_padrao(self, tipo: str) -> None:
        if tipo == "real":
            self.emit("dconst_0")
        elif tipo == "str":
            self.emit('ldc ""')
        else:
            self.emit("iconst_0")

    def is_const_decl(self, ctx) -> bool:
        return ctx.CONST() is not None

    def visitProg(self, ctx: JSSimplificadoParser.ProgContext):
        for decl in ctx.decl():
            funcao = decl.funcDecl()
            if funcao is not None and funcao.ID().getText() == "main":
                self.visit(funcao.bloco())
            elif decl.varDecl() is not None:
                self.visit(decl.varDecl())

        for stmt in ctx.stmt():
            self.visit(stmt)

        return None

    def visitBloco(self, ctx: JSSimplificadoParser.BlocoContext):
        self.abrir_escopo()
        for stmt in ctx.stmt():
            self.visit(stmt)
        self.fechar_escopo()
        return None

    def visitStmtVarDecl(self, ctx: JSSimplificadoParser.StmtVarDeclContext):
        return self.visit(ctx.varDecl())

    def visitVarSimples(self, ctx: JSSimplificadoParser.VarSimplesContext):
        tipo = ctx.tipo().getText()
        ids = ctx.ID()
        is_const = self.is_const_decl(ctx)

        for token_id in ids:
            simbolo = self.declarar_variavel(token_id.getText(), tipo, is_const=is_const)
            if ctx.expr() is not None and token_id == ids[0]:
                self.visit(ctx.expr())
            else:
                self.emitir_valor_padrao(tipo)
            self.emit(f"{self.instrucao_store(simbolo)} {simbolo.indice}")

        return None

    def visitStmtAssign(self, ctx: JSSimplificadoParser.StmtAssignContext):
        nome = ctx.ID().getText()
        simbolo = self.buscar_variavel(nome)
        if simbolo is None:
            raise ErroGeracaoIR(f"Variavel '{nome}' nao declarada.")
        if simbolo.is_const:
            raise ErroGeracaoIR(f"Constante '{nome}' nao pode ser alterada.")

        self.visit(ctx.expr())
        self.emit(f"{self.instrucao_store(simbolo)} {simbolo.indice}")
        return None

    def visitStmtConsoleLog(self, ctx: JSSimplificadoParser.StmtConsoleLogContext):
        expr_list = ctx.consolelog().exprList()
        if expr_list is not None:
            for indice, expr in enumerate(expr_list.expr()):
                if indice > 0:
                    self.emit_print_constante(" ")
                self.emit("getstatic java/lang/System/out Ljava/io/PrintStream;")
                valor = self.visit(expr)
                tipo = valor.tipo if isinstance(valor, ValorIR) else "str"
                self.emit(
                    "invokevirtual java/io/PrintStream/print"
                    f"({self.descritor_print(tipo)})V"
                )

        self.emit("getstatic java/lang/System/out Ljava/io/PrintStream;")
        self.emit("invokevirtual java/io/PrintStream/println()V")
        return None

    def emit_print_constante(self, texto: str) -> None:
        self.emit("getstatic java/lang/System/out Ljava/io/PrintStream;")
        self.emit(f'ldc "{texto}"')
        self.emit("invokevirtual java/io/PrintStream/print(Ljava/lang/String;)V")

    def visitExprInt(self, ctx: JSSimplificadoParser.ExprIntContext):
        self.emit(f"ldc {ctx.getText()}")
        return ValorIR("int")

    def visitExprReal(self, ctx: JSSimplificadoParser.ExprRealContext):
        self.emit(f"ldc2_w {ctx.getText()}")
        return ValorIR("real")

    def visitExprStr(self, ctx: JSSimplificadoParser.ExprStrContext):
        self.emit(f"ldc {ctx.getText()}")
        return ValorIR("str")

    def visitExprBool(self, ctx: JSSimplificadoParser.ExprBoolContext):
        self.emit("iconst_1" if ctx.getText() == "true" else "iconst_0")
        return ValorIR("bool")

    def visitExprId(self, ctx: JSSimplificadoParser.ExprIdContext):
        nome = ctx.ID().getText()
        simbolo = self.buscar_variavel(nome)
        if simbolo is None:
            raise ErroGeracaoIR(f"Variavel '{nome}' nao declarada.")
        self.emit(f"{self.instrucao_load(simbolo)} {simbolo.indice}")
        return ValorIR(simbolo.tipo)

    def visitExprParen(self, ctx: JSSimplificadoParser.ExprParenContext):
        return self.visit(ctx.expr())

    def visitExprAddSub(self, ctx: JSSimplificadoParser.ExprAddSubContext):
        esquerdo = self.visit(ctx.expr(0))
        direito = self.visit(ctx.expr(1))
        tipo = self.tipo_numerico_resultante(esquerdo, direito)
        if tipo == "real":
            self.emit("dadd" if ctx.op.text == "+" else "dsub")
        else:
            self.emit("iadd" if ctx.op.text == "+" else "isub")
        return ValorIR(tipo)

    def visitExprMulDiv(self, ctx: JSSimplificadoParser.ExprMulDivContext):
        esquerdo = self.visit(ctx.expr(0))
        direito = self.visit(ctx.expr(1))
        tipo = self.tipo_numerico_resultante(esquerdo, direito)
        if tipo == "real":
            self.emit("dmul" if ctx.op.text == "*" else "ddiv")
        else:
            self.emit("imul" if ctx.op.text == "*" else "idiv")
        return ValorIR(tipo)

    def visitExprMod(self, ctx: JSSimplificadoParser.ExprModContext):
        self.visit(ctx.expr(0))
        self.visit(ctx.expr(1))
        self.emit("irem")
        return ValorIR("int")

    def visitExprUnary(self, ctx: JSSimplificadoParser.ExprUnaryContext):
        valor = self.visit(ctx.expr())
        if ctx.op.text == "-":
            self.emit("dneg" if valor.tipo == "real" else "ineg")
        return valor

    def tipo_numerico_resultante(self, esquerdo, direito) -> str:
        if isinstance(esquerdo, ValorIR) and esquerdo.tipo == "real":
            return "real"
        if isinstance(direito, ValorIR) and direito.tipo == "real":
            return "real"
        return "int"
