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
class InfoParametro:
    nome: str
    tipo: str
    dimensoes: int = 0


@dataclass(frozen=True)
class InfoClasse:
    atributos: dict[str, str]
    metodos: dict[str, Simbolo]


def tipos_compativeis(esperado: str, obtido: str) -> bool:
    if esperado == obtido:
        return True
    if esperado == "real" and obtido == "int":
        return True
    return False


@dataclass(frozen=True)
class Simbolo:
    nome: str
    categoria: str
    tipo: str
    linha: int
    dimensoes: int = 0
    is_const: bool = False  # Rastreia se foi declarado com 'const' para proteger vetores/objetos
    parametros: tuple[InfoParametro, ...] | None = None


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
        self._pilha_contexto: list[str] = []
        self._classes: dict[str, InfoClasse] = {}

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

    def declarar(self, token, category: str, tipo: str, dimensoes: int = 0, is_const: bool = False, parametros: tuple[InfoParametro, ...] | None = None) -> None:
        nome = token.getText()
        existente = self.tabela.declarar(
            Simbolo(
                nome=nome,
                categoria=category,
                tipo=tipo,
                linha=token.symbol.line,
                dimensoes=dimensoes,
                is_const=is_const,
                parametros=parametros,
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

    def coletar_parametros(self, param_list_ctx: JSSimplificadoParser.ParamListContext | None) -> tuple[InfoParametro, ...]:
        if param_list_ctx is None:
            return ()
        resultado: list[InfoParametro] = []
        for param_ctx in param_list_ctx.param():
            ids = param_ctx.ID()
            nome = ids[-1].getText()
            tipo = self.texto_tipo_parametro(param_ctx)
            dims = self.quantidade_dimensoes(param_ctx.dimensoesVazias())
            resultado.append(InfoParametro(nome=nome, tipo=tipo, dimensoes=dims))
        return tuple(resultado)

    def tipo_expr(self, ctx) -> str | None:
        if ctx is None:
            return None
        resultado = self.visit(ctx)
        return resultado if isinstance(resultado, str) else None

    def _validar_argumentos(self, token, simbolo: Simbolo, args_info: list[tuple[str | None, int]]) -> None:
        if simbolo.parametros is None:
            return
        params = simbolo.parametros
        n_params = len(params)
        n_args = len(args_info)

        if n_args != n_params:
            self.erro(
                token,
                f"'{simbolo.nome}' espera {n_params} argumento(s), "
                f"mas {n_args} foram fornecidos.",
            )
            return

        for i, (param, (tipo_arg, dims_arg)) in enumerate(zip(params, args_info)):
            if tipo_arg is not None and not tipos_compativeis(param.tipo, tipo_arg):
                self.erro(
                    token,
                    f"argumento {i + 1} de '{simbolo.nome}': "
                    f"esperado '{param.tipo}', obtido '{tipo_arg}'.",
                )
            if param.dimensoes != dims_arg:
                self.erro(
                    token,
                    f"argumento {i + 1} de '{simbolo.nome}': "
                    f"esperado array com {param.dimensoes} dimensao(oes), "
                    f"mas foi passado com {dims_arg}.",
                )

    def _info_expr(self, ctx) -> tuple[str | None, int]:
        tipo = self.tipo_expr(ctx)
        dims = 0
        if isinstance(ctx, JSSimplificadoParser.ExprIdContext):
            simbolo = self.tabela.buscar(ctx.ID().getText())
            if simbolo is not None:
                dims = simbolo.dimensoes
        elif isinstance(ctx, JSSimplificadoParser.ExprVetorContext):
            simbolo = self.tabela.buscar(ctx.ID().getText())
            if simbolo is not None:
                num_indices = self.quantidade_dimensoes(ctx.indices())
                dims = simbolo.dimensoes - num_indices
        return tipo, dims

    def _verificar_index(self, ctx) -> None:
        for expr_ctx in ctx.expr():
            tipo = self.tipo_expr(expr_ctx)
            if tipo is not None and tipo != "int":
                self.erro(
                    expr_ctx.start,
                    f"indice de array deve ser 'int', obtido '{tipo}'.",
                )

    def _verificar_dim(self, ctx) -> None:
        for expr_ctx in ctx.expr():
            tipo = self.tipo_expr(expr_ctx)
            if tipo is not None and tipo != "int":
                self.erro(
                    expr_ctx.start,
                    f"tamanho de dimensao de array deve ser 'int', obtido '{tipo}'.",
                )

    def visitProg(self, ctx: JSSimplificadoParser.ProgContext):
        for decl in ctx.decl():
            funcao = decl.funcDecl()
            classe = decl.classDecl()

            if funcao is not None:
                tipo_ret = self.texto_tipo_retorno(funcao.tipoRetorno())
                nome_func = funcao.ID().getText()
                if "[" in tipo_ret or "]" in tipo_ret:
                    self.erro(funcao.ID().symbol, f"Funcao '{nome_func}' nao pode retornar um vetor.")
                params = self.coletar_parametros(funcao.paramList())
                if nome_func == "main" and len(params) > 0:
                    self.erro(funcao.ID().symbol, "A funcao 'main' nao deve possuir parametros.")
                self.declarar(
                    funcao.ID(),
                    "funcao",
                    tipo_ret,
                    parametros=params,
                )
            elif classe is not None:
                self.declarar(classe.ID(), "classe", classe.ID().getText())
        for decl in ctx.decl():
            self.visit(decl)
        return None

    def visitVarSimples(self, ctx: JSSimplificadoParser.VarSimplesContext):
        tipo = ctx.tipo().getText()
        is_const = ctx.parentCtx is not None and "const" in ctx.parentCtx.getText()
        for token_id in ctx.ID():
            self.declarar(token_id, "variavel", tipo, is_const=is_const)
        if ctx.expr() is not None:
            self.visit(ctx.expr())
        return None

    def visitVarVetor(self, ctx: JSSimplificadoParser.VarVetorContext):
        is_const = ctx.parentCtx is not None and "const" in ctx.parentCtx.getText()
        self.declarar(
            ctx.ID(),
            "variavel",
            ctx.tipo().getText(),
            self.quantidade_dimensoes(ctx.dimensoes()),
            is_const=is_const
        )
        self._verificar_dim(ctx.dimensoes())
        if ctx.inicializadorVetor() is not None:
            self.visit(ctx.inicializadorVetor())
        return None

    def visitVarObjeto(self, ctx: JSSimplificadoParser.VarObjetoContext):
        self.exigir_declarado(ctx.ID(0), {"classe"}, "classe")
        is_const = ctx.parentCtx is not None and "const" in ctx.parentCtx.getText()
        self.declarar(ctx.ID(1), "variavel", self.texto_tipo_var_objeto(ctx), is_const=is_const)
        if ctx.expr() is not None:
            self.visit(ctx.expr())
        return None

    def visitFuncDecl(self, ctx: JSSimplificadoParser.FuncDeclContext):
        self._pilha_contexto.append(self.texto_tipo_retorno(ctx.tipoRetorno()))
        self.tabela.abrir_escopo()
        if ctx.paramList() is not None:
            self.visit(ctx.paramList())

        if ctx.bloco() is not None:
            self.visit(ctx.bloco())
            
        self.tabela.fechar_escopo()
        self._pilha_contexto.pop()  
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
        nome_classe = ctx.ID().getText()
        self.tabela.abrir_escopo()

        atributos: dict[str, str] = {}
        for atributo in ctx.atributo():
            self.visit(atributo)
            ids = atributo.ID()
            if atributo.tipo() is not None:
                atributos[ids[0].getText()] = atributo.tipo().getText()
            elif len(ids) >= 2:
                atributos[ids[1].getText()] = ids[0].getText()

        self.visit(ctx.constructorDecl())

        metodos: dict[str, Simbolo] = {}
        for metodo in ctx.metodoDecl():
            tipo_ret = self.texto_tipo_retorno(metodo.tipoRetorno())
            if "[" in tipo_ret or "]" in tipo_ret:
                self.erro(metodo.ID().symbol, f"Metodo '{metodo.ID().getText()}' nao pode retornar um vetor.")
            self.visit(metodo)
            nome_metodo = metodo.ID().getText()
            simbolo = self.tabela.buscar(nome_metodo)
            if simbolo is not None:
                metodos[nome_metodo] = simbolo

        self._classes[nome_classe] = InfoClasse(atributos=atributos, metodos=metodos)
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
        params = self.coletar_parametros(ctx.paramList())
        self.declarar(
            ctx.ID(),
            "metodo",
            self.texto_tipo_retorno(ctx.tipoRetorno()),
            parametros=params,
        )
        self._pilha_contexto.append(self.texto_tipo_retorno(ctx.tipoRetorno()))
        self.tabela.abrir_escopo()
        if ctx.paramList() is not None:
            self.visit(ctx.paramList())
        self.visit(ctx.bloco())
        self.tabela.fechar_escopo()
        self._pilha_contexto.pop()
        return None
    
    def visitStmtReturn(self, ctx: JSSimplificadoParser.StmtReturnContext):
        tipo = self._pilha_contexto[-1] if self._pilha_contexto else "void"
        if ctx.expr() is not None:
            current_tipo = self.tipo_expr(ctx.expr())
            if tipo == "void":
                self.erro(ctx.start, "funcao 'void' nao deve retornar um valor.")
            elif current_tipo is not None and not tipos_compativeis(tipo, current_tipo):
                self.erro(ctx.start, f"retorno incompativel: esperado '{tipo}', obtido '{current_tipo}'.")
        else:
            if tipo != "void":
                self.erro(ctx.start, f"funcao deve retornar '{tipo}', mas 'return' sem valor foi encontrado.")
        return None

    def visitExprInt(self, ctx: JSSimplificadoParser.ExprIntContext):
        return "int"

    def visitExprReal(self, ctx: JSSimplificadoParser.ExprRealContext):
        return "real"

    def visitExprStr(self, ctx: JSSimplificadoParser.ExprStrContext):
        return "str"

    def visitExprBool(self, ctx: JSSimplificadoParser.ExprBoolContext):
        return "bool"

    # ---------------------------------------------------------
    # OPERAÇÕES ARITMÉTICAS COM TRATAMENTO DE COERÇÃO E STR
    # ---------------------------------------------------------
    def visitExprAddSub(self, ctx: JSSimplificadoParser.ExprAddSubContext) -> str | None:
        tipo_esq = self.tipo_expr(ctx.expr(0))
        tipo_dir = self.tipo_expr(ctx.expr(1))

        if tipo_esq is None or tipo_dir is None:
            return None

        # Regra III / Tabela 1: Concatenação de string caso um operando seja str
        if ctx.op.text == "+":
            if tipo_esq == "str" or tipo_dir == "str":
                return "str"

        if tipo_esq not in ["int", "real"] or tipo_dir not in ["int", "real"]:
            self.erro(ctx.op, f"operacao aritmetica '{ctx.op.text}' exige operandos numericos, obtidos '{tipo_esq}' e '{tipo_dir}'.")
            return None

        return "real" if "real" in (tipo_esq, tipo_dir) else "int"

    def visitExprMulDiv(self, ctx: JSSimplificadoParser.ExprMulDivContext) -> str | None:
        tipo_esq = self.tipo_expr(ctx.expr(0))
        tipo_dir = self.tipo_expr(ctx.expr(1))

        if tipo_esq is None or tipo_dir is None:
            return None

        if tipo_esq not in ["int", "real"] or tipo_dir not in ["int", "real"]:
            self.erro(ctx.op, f"operacao '{ctx.op.text}' exige operandos numericos, obtidos '{tipo_esq}' e '{tipo_dir}'.")
            return None

        return "real" if "real" in (tipo_esq, tipo_dir) else "int"

    def visitExprMod(self, ctx: JSSimplificadoParser.ExprModContext) -> str | None:
        tipo_esq = self.tipo_expr(ctx.expr(0))
        tipo_dir = self.tipo_expr(ctx.expr(1))

        if tipo_esq is None or tipo_dir is None:
            return None

        if tipo_esq != "int" or tipo_dir != "int":
            self.erro(ctx.op, f"operacao de resto '%' exige inteiros, obtidos '{tipo_esq}' e '{tipo_dir}'.")
            return None
        return "int"

    def visitExprPow(self, ctx: JSSimplificadoParser.ExprPowContext) -> str | None:
        tipo_esq = self.tipo_expr(ctx.expr(0))
        tipo_dir = self.tipo_expr(ctx.expr(1))
        if tipo_esq is None or tipo_dir is None:
            return None
        # Tabela 1: Operador ** aplica-se somente a inteiros e retorna inteiro
        if tipo_esq != "int" or tipo_dir != "int":
            self.erro(ctx.op, f"operacao de potencia '**' exige inteiros, obtidos '{tipo_esq}' e '{tipo_dir}'.")
            return None
        return "int"

    def visitExprUnary(self, ctx: JSSimplificadoParser.ExprUnaryContext) -> str | None:
        tipo = self.tipo_expr(ctx.expr())
        if tipo is None:
            return None
        operador = ctx.op.text
        if operador in ["-", "+"]:
            if tipo not in ["int", "real"]:
                self.erro(ctx.op, f"operador unario '{operador}' exige numerico, obtido '{tipo}'.")
                return None
            return tipo
        elif operador == "!":
            if tipo != "bool":
                self.erro(ctx.op, f"operador unario '!' exige 'bool', obtido '{tipo}'.")
                return None
            return "bool"
        return tipo

    def visitExprIncDec(self, ctx: JSSimplificadoParser.ExprIncDecContext) -> str | None:
        tipo = self.tipo_expr(ctx.expr())
        if tipo is not None and tipo not in ["int", "real"]:
            self.erro(ctx.op, f"operador '{ctx.op.text}' exige operando numerico, obtido '{tipo}'.")
        return tipo

    # ---------------------------------------------------------
    # OPERAÇÕES RELACIONAIS CONFORME REQUISITOS DO PDF
    # ---------------------------------------------------------
    def visitExprRel(self, ctx: JSSimplificadoParser.ExprRelContext) -> str | None:
        tipo_esq, dims_esq = self._info_expr(ctx.expr(0))
        tipo_dir, dims_dir = self._info_expr(ctx.expr(1))

        if tipo_esq is None or tipo_dir is None:
            return "bool"

        # Tabela 1: Relacionais operam em todos os primitivos, exceto vetor (dimensoes > 0)
        if dims_esq > 0 or dims_dir > 0:
            self.erro(ctx.op, f"operador '{ctx.op.text}' nao pode ser aplicado a vetores.")
        return "bool"

    def visitExprEq(self, ctx: JSSimplificadoParser.ExprEqContext) -> str | None:
        tipo_esq = self.tipo_expr(ctx.expr(0))
        tipo_dir = self.tipo_expr(ctx.expr(1))

        if tipo_esq is not None and tipo_dir is not None:
            if not tipos_compativeis(tipo_esq, tipo_dir) and not tipos_compativeis(tipo_dir, tipo_esq):
                self.erro(ctx.op, f"comparacao '{ctx.op.text}' entre tipos incompativeis: '{tipo_esq}' e '{tipo_dir}'.")
        return "bool"

    def visitExprAnd(self, ctx: JSSimplificadoParser.ExprAndContext) -> str | None:
        tipo_esq = self.tipo_expr(ctx.expr(0))
        tipo_dir = self.tipo_expr(ctx.expr(1))
        if tipo_esq is not None and tipo_esq != "bool":
            self.erro(ctx.op, f"operador '&&' exige lado esquerdo 'bool', obtido '{tipo_esq}'.")
        if tipo_dir is not None and tipo_dir != "bool":
            self.erro(ctx.op, f"operador '&&' exige lado direito 'bool', obtido '{tipo_dir}'.")
        return "bool"

    def visitExprOr(self, ctx: JSSimplificadoParser.ExprOrContext) -> str | None:
        self.tipo_expr(ctx.expr(0))
        self.tipo_expr(ctx.expr(1))
        return "bool"

    def visitExprParen(self, ctx: JSSimplificadoParser.ExprParenContext) -> str | None:
        return self.tipo_expr(ctx.expr())

    def visitBloco(self, ctx: JSSimplificadoParser.BlocoContext):
        self.tabela.abrir_escopo()
        for stmt in ctx.stmt():
            self.visit(stmt)
        self.tabela.fechar_escopo()
        return None

    # ---------------------------------------------------------
    # VALIDAÇÃO DE COMANDOS, CONSTANTES E INPUT
    # ---------------------------------------------------------
    def visitStmtAssign(self, ctx: JSSimplificadoParser.StmtAssignContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        tipo_valor = self.tipo_expr(ctx.expr())
        op_texto = ctx.atribComp().getText()
        if simbolo is not None:
            # Regra 4.1: Proibir reatribuicao direta em constantes
            if simbolo.is_const:
                self.erro(ctx.ID().symbol, f"Identificador '{simbolo.nome}' e constante e nao pode ser alterado.")
                return None
            if tipo_valor is not None:
                if op_texto != "=":
                    if simbolo.tipo not in ["int", "real"] or tipo_valor not in ["int", "real"]:
                        self.erro(ctx.ID().symbol, f"atribuicao composta '{op_texto}' exige tipos numericos.")
                        return None
                if not tipos_compativeis(simbolo.tipo, tipo_valor):
                    self.erro(ctx.ID().symbol, f"atribuicao incompativel: esperado '{simbolo.tipo}', obtido '{tipo_valor}'.")
        return None

    def visitStmtVetorAssign(self, ctx: JSSimplificadoParser.StmtVetorAssignContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        self._verificar_index(ctx.indices())

        if simbolo is not None:
            # Regra 4.2.2: Vetores constantes nao podem ter seus valores alterados
            if simbolo.is_const:
                self.erro(ctx.ID().symbol, f"Vetor '{simbolo.nome}' e constante e nao pode ser modificado.")
                return None
            num_indices = self.quantidade_dimensoes(ctx.indices())
            if simbolo.dimensoes == 0:
                self.erro(ctx.ID().symbol, f"'{simbolo.nome}' nao e um array.")
            elif num_indices != simbolo.dimensoes:
                self.erro(ctx.ID().symbol, f"'{simbolo.nome}' tem {simbolo.dimensoes} dimensoes, obtido {num_indices}.")
            else:
                tipo_valor = self.tipo_expr(ctx.expr())
                if tipo_valor is not None and not tipos_compativeis(simbolo.tipo, tipo_valor):
                    self.erro(ctx.ID().symbol, f"atribuicao incompativel em vetor: esperado '{simbolo.tipo}', obtido '{tipo_valor}'.")
        return None

    def visitStmtAtribObjeto(self, ctx: JSSimplificadoParser.StmtAtribObjetoContext):
        if ctx.THIS() is None:
            simbolo = self.exigir_declarado(ctx.ID(0), {"variavel", "parametro", "atributo"})
            # Regra 4.2.2: Objeto constante nao pode ter seus atributos alterados
            if simbolo is not None and simbolo.is_const:
                self.erro(ctx.ID(0).symbol, f"Objeto '{simbolo.nome}' e constante e nao pode ter seus atributos modificados.")
        self.visit(ctx.expr())
        return None

    def visitStmtIf(self, ctx: JSSimplificadoParser.StmtIfContext):
        for expr in ctx.expr():
            tipo_cond = self.tipo_expr(expr)
            if tipo_cond is not None and tipo_cond != "bool":
                self.erro(expr.start, f"condicao do 'if' deve ser 'bool', obtido '{tipo_cond}'.")
        for bloco in ctx.bloco():
            self.visit(bloco)
        return None

    def visitStmtWhile(self, ctx: JSSimplificadoParser.StmtWhileContext):
        tipo_cond = self.tipo_expr(ctx.expr())
        if tipo_cond is not None and tipo_cond != "bool":
            self.erro(ctx.expr().start, f"condicao do 'while' deve ser 'bool', obtido '{tipo_cond}'.")
        self.visit(ctx.bloco())
        return None

    def visitStmtFor(self, ctx: JSSimplificadoParser.StmtForContext):
        self.tabela.abrir_escopo()
        if ctx.forInit() is not None:
            self.visit(ctx.forInit())
        if ctx.expr() is not None:
            tipo_cond = self.tipo_expr(ctx.expr())
            if tipo_cond is not None and tipo_cond != "bool":
                self.erro(ctx.expr().start, f"condicao do 'for' deve ser 'bool', obtido '{tipo_cond}'.")
        if ctx.forUpdate() is not None:
            self.visit(ctx.forUpdate())
        self.visit(ctx.bloco())
        self.tabela.fechar_escopo()
        return None

    def visitStmtConsoleLog(self, ctx: JSSimplificadoParser.StmtConsoleLogContext):
        if ctx.consolelog() is not None and ctx.consolelog().exprList() is not None:
            for expr_ctx in ctx.consolelog().exprList().expr():
                self.tipo_expr(expr_ctx)
        return None

    def visitForInit(self, ctx: JSSimplificadoParser.ForInitContext):
        ids = ctx.ID()
        is_const = ctx.CONST() is not None
        if ctx.LET() is not None or ctx.CONST() is not None:
            if ctx.tipo() is not None:
                tipo = ctx.tipo().getText()
                for token_id in ids:
                    self.declarar(token_id, "variavel", tipo, self.quantidade_dimensoes(ctx.dimensoes()), is_const=is_const)
            elif len(ids) >= 2:
                self.exigir_declarado(ids[0], {"classe"}, "classe")
                self.declarar(ids[1], "variavel", ids[0].getText(), is_const=is_const)
        elif ids:
            simbolo = self.exigir_declarado(ids[0], {"variavel", "parametro", "atributo"})
            if simbolo is not None and simbolo.is_const:
                self.erro(ids[0].symbol, f"Nao e possivel reatribuir a constante '{simbolo.nome}' no inicializador do 'for'.")
        if ctx.expr() is not None:
            self.visit(ctx.expr())
        if ctx.dimensoes() is not None:
            self.visit(ctx.dimensoes())
        if ctx.inicializadorVetor() is not None:
            self.visit(ctx.inicializadorVetor())
        return None

    def visitForUpdate(self, ctx: JSSimplificadoParser.ForUpdateContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        if simbolo is not None and simbolo.is_const:
            self.erro(ctx.ID().symbol, f"Nao e permitido modificar a constante '{simbolo.nome}' no update do 'for'.")
        if ctx.expr() is not None:
            self.visit(ctx.expr())
        return None

    def visitStmtIncDec(self, ctx: JSSimplificadoParser.StmtIncDecContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        if simbolo is not None and simbolo.is_const:
            self.erro(ctx.ID().symbol, f"Nao e permitido aplicar incremento/decremento na constante '{simbolo.nome}'.")
        return None

    def visitInputStmt(self, ctx: JSSimplificadoParser.InputStmtContext):
        for token_id in ctx.idList().ID():
            simbolo = self.exigir_declarado(token_id, {"variavel", "parametro", "atributo"})
            if simbolo is not None:
                if simbolo.is_const:
                    self.erro(token_id.symbol, f"O comando 'input' nao pode ler dados para a constante '{simbolo.nome}'.")
                if simbolo.tipo not in ["int", "real", "str"]:
                    self.erro(token_id.symbol, f"O comando 'input' suporta apenas int, real e str. Variavel '{simbolo.nome}' e do tipo '{simbolo.tipo}'.")
                if simbolo.dimensoes > 0:
                    self.erro(token_id.symbol, f"O comando 'input' nao pode ler diretamente para o vetor '{simbolo.nome}'.")
        return None

    def visitChamadaFuncao(self, ctx: JSSimplificadoParser.ChamadaFuncaoContext):
        if ctx.casting() is not None:
            return self.visit(ctx.casting())

        if ctx.DOT() is not None:
            if ctx.THIS() is None:
                simbolo_obj = self.exigir_declarado(ctx.ID(0), {"variavel", "parametro", "atributo"}, "objeto")
                if simbolo_obj is not None:
                    nome_classe = simbolo_obj.tipo
                    nome_metodo = ctx.ID(1).getText()
                    info = self._classes.get(nome_classe)

                    if info is None:
                        self.erro(ctx.ID(1).symbol, f"classe '{nome_classe}' nao possui informacoes registradas.")
                    elif nome_metodo not in info.metodos:
                        self.erro(ctx.ID(1).symbol, f"metodo '{nome_metodo}' nao existe na classe '{nome_classe}'.")
                    else:
                        simbolo_metodo = info.metodos[nome_metodo]
                        args_info: list[tuple[str | None, int]] = []  
                        if ctx.exprList() is not None:
                            args_info = [self._info_expr(e) for e in ctx.exprList().expr()]  
                        self._validar_argumentos(ctx.ID(1).symbol, simbolo_metodo, args_info)  
                        return simbolo_metodo.tipo
            if ctx.exprList() is not None:
                self.visit(ctx.exprList())
            return None

        simbolo = self.exigir_declarado(ctx.ID(0), {"funcao"}, "funcao")
        args_info: list[tuple[str | None, int]] = []
        if ctx.exprList() is not None:
            args_info = [self._info_expr(e) for e in ctx.exprList().expr()] 

        if simbolo is not None:
            self._validar_argumentos(ctx.ID(0).symbol, simbolo, args_info)  
            return simbolo.tipo
        return None
    
    def visitCasting(self, ctx: JSSimplificadoParser.CastingContext) -> str | None:
        # Avalia a expressão interna para garantir que não tenha erros em seu conteúdo
        self.tipo_expr(ctx.expr())
        # O casting forçará o retorno para o tipo primitivo escrito antes dos parênteses
        return ctx.tipo().getText()
    
    def visitExprId(self, ctx: JSSimplificadoParser.ExprIdContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        if simbolo is not None:
            return simbolo.tipo
        return None

    def visitExprVetor(self, ctx: JSSimplificadoParser.ExprVetorContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        self._verificar_index(ctx.indices())

        if simbolo is not None:
            num_indices = self.quantidade_dimensoes(ctx.indices())
            if simbolo.dimensoes == 0:
                self.erro(ctx.ID().symbol, f"'{simbolo.nome}' nao e um array.")
            elif num_indices != simbolo.dimensoes:
                self.erro(ctx.ID().symbol, f"'{simbolo.nome}' tem {simbolo.dimensoes} dimensoes, obtido {num_indices}.")
                return None
            return simbolo.tipo
        return None

    def visitExprAtribObjeto(self, ctx: JSSimplificadoParser.ExprAtribObjetoContext):
        if ctx.THIS() is None:
            simbolo_obj = self.exigir_declarado(ctx.ID(0), {"variavel", "parametro", "atributo"}, "objeto")
            if simbolo_obj is not None:
                nome_classe = simbolo_obj.tipo
                nome_atributo = ctx.ID(1).getText()
                info = self._classes.get(nome_classe)

                if info is None:
                    self.erro(ctx.ID(1).symbol, f"classe '{nome_classe}' nao possui informacoes registradas.")
                elif nome_atributo not in info.atributos:
                    self.erro(ctx.ID(1).symbol, f"atributo '{nome_atributo}' nao existe na classe '{nome_classe}'.")
                else:
                    return info.atributos[nome_atributo]
        return None

    def visitExprNew(self, ctx: JSSimplificadoParser.ExprNewContext):
        self.exigir_declarado(ctx.ID(), {"classe"}, "classe")
        if ctx.exprList() is not None:
            self.visit(ctx.exprList())
        return ctx.ID().getText()


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