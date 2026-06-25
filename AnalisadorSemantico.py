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

#dataclass InfoParametro define as informacoes que um parametro deve ter.
@dataclass(frozen=True)
class InfoParametro:
    nome: str
    tipo: str
    dimensoes: int = 0

#define o objeto classe, tendo atributos e metodos
@dataclass(frozen=True)
class InfoClasse:
    atributos: dict[str, str]
    metodos: dict[str, Simbolo]

# tipos compativeis retornam cast implicito
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

    parametros: tuple[InfoParametro, ...] | None = None #informa os parametros


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

    def declarar(self, token, categoria: str, tipo: str, dimensoes: int = 0, parametros: tuple[InfoParametro, ...] | None = None) -> None:
        nome = token.getText()
        existente = self.tabela.declarar(
            Simbolo(
                nome=nome,
                categoria=categoria,
                tipo=tipo,
                linha=token.symbol.line,
                dimensoes=dimensoes,
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
    

    #antes dos visit vamos definir um metodo auxiliar:
    #esse metodo captura a lista de parametros e retorna uma tupla contendo informações de parametro.
    #retorna nome, tipo e dimensoes capturadas do parametro atual.

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
    
    #validamos se os argumentos recebidos sao validos
    #se o numero de argumentos é o mesmo de parametros ou se os tipos não são compatíveis
    def _validar_argumentos(self,token,simbolo: Simbolo,args_info: list[tuple[str | None, int]],) -> None:
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

    #metodo que retorna o tipo e dimensoes de uma expressao
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

    #verificar se o index é int
    def _verificar_index(self, ctx) -> None:
        for expr_ctx in ctx.expr():
            tipo = self.tipo_expr(expr_ctx)
            if tipo is not None and tipo != "int":
                self.erro(
                    expr_ctx.start,
                    f"indice de array deve ser 'int', obtido '{tipo}'.",
                )
    #verificar se as dimensoes sao index
    def _verificar_dim(self, ctx) -> None:
        for expr_ctx in ctx.expr():
            tipo = self.tipo_expr(expr_ctx)
            if tipo is not None and tipo != "int":
                self.erro(
                    expr_ctx.start,
                    f"tamanho de dimensao de array deve ser 'int', obtido '{tipo}'.",
                )
    #Ao declarar a funcao agora também recebe os parametros para
    #Ser identificadas durante a varredura de declarações globais
    def visitProg(self, ctx: JSSimplificadoParser.ProgContext):
        for decl in ctx.decl():
            funcao = decl.funcDecl()
            classe = decl.classDecl()

            if funcao is not None:
                params = self.coletar_parametros(funcao.paramList())
                self.declarar(
                    funcao.ID(),
                    "funcao",
                    self.texto_tipo_retorno(funcao.tipoRetorno()),
                    parametros=params,
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
        self._verificar_dim(ctx.dimensoes())

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
        self._pilha_contexto.append(self.texto_tipo_retorno(ctx.tipoRetorno()))
        self.tabela.abrir_escopo()

        if ctx.paramList() is not None:
            self.visit(ctx.paramList())

        self.visit(ctx.bloco())
        self.tabela.fechar_escopo()
        # retirando da pilha
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
        params = self.coletar_parametros(ctx.paramList())  # <-- novo
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
    
    #adicao de um novo visitor para verificar o retorno  
    def visitStmtReturn(self, ctx: JSSimplificadoParser.StmtReturnContext):
        
        tipo = self._pilha_contexto[-1] if self._pilha_contexto else "void"

        if ctx.expr() is not None:
            current_tipo = self.tipo_expr(ctx.expr())

            if tipo == "void":
                self.erro(
                    ctx.start,
                    "funcao 'void' nao deve retornar um valor.",
                )
            elif current_tipo is not None and not tipos_compativeis(tipo, current_tipo):
                self.erro(
                    ctx.start,
                    f"retorno incompativel: esperado '{tipo}', obtido '{current_tipo}'.",
                )
        else:
            if tipo != "void":
                self.erro(
                    ctx.start,
                    f"funcao deve retornar '{tipo}', mas 'return' sem valor foi encontrado.",
                )

        return None
    #visitors para literais
    def visitExprInt(self, ctx: JSSimplificadoParser.ExprIntContext):
        return "int"

    def visitExprReal(self, ctx: JSSimplificadoParser.ExprRealContext):
        return "real"

    def visitExprStr(self, ctx: JSSimplificadoParser.ExprStrContext):
        return "str"

    def visitExprBool(self, ctx: JSSimplificadoParser.ExprBoolContext):
        return "bool"
    def visitBloco(self, ctx: JSSimplificadoParser.BlocoContext):
        self.tabela.abrir_escopo()

        for stmt in ctx.stmt():
            self.visit(stmt)

        self.tabela.fechar_escopo()
        return None

    def visitStmtAssign(self, ctx: JSSimplificadoParser.StmtAssignContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})
        tipo_valor = self.tipo_expr(ctx.expr())

        if simbolo is not None and tipo_valor is not None:
            if not tipos_compativeis(simbolo.tipo, tipo_valor):
                self.erro(
                    ctx.ID().symbol,
                    f"atribuicao incompativel: esperado '{simbolo.tipo}', obtido '{tipo_valor}'.",
                )

        return None

    def visitStmtVetorAssign(self, ctx: JSSimplificadoParser.StmtVetorAssignContext):
        simbolo = self.exigir_declarado(ctx.ID(), {"variavel", "parametro", "atributo"})

        self._verificar_index(ctx.indices())

        if simbolo is not None:
            num_indices = self.quantidade_dimensoes(ctx.indices())

            if simbolo.dimensoes == 0:
                self.erro(
                    ctx.ID().symbol,
                    f"'{simbolo.nome}' nao e um array, mas esta sendo indexado.",
                )
            elif num_indices != simbolo.dimensoes:
                self.erro(
                    ctx.ID().symbol,
                    f"'{simbolo.nome}' tem {simbolo.dimensoes} dimensoes, "
                    f"mas {num_indices} indice(s) foram usados.",
                )
            else:
                tipo_valor = self.tipo_expr(ctx.expr())
                if tipo_valor is not None and not tipos_compativeis(simbolo.tipo, tipo_valor):
                    self.erro(
                        ctx.ID().symbol,
                        f"atribuicao em array '{simbolo.nome}': "
                        f"esperado '{simbolo.tipo}', obtido '{tipo_valor}'.",
                    )
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

    #No VisitChamadaFuncao coletamos os tipos dos argumentos e fazemos a verificacao
    #Os tipos devem ser compataveis, e o numero de argumentos também.

    def visitChamadaFuncao(self, ctx: JSSimplificadoParser.ChamadaFuncaoContext):
        if ctx.casting() is not None:
            self.visit(ctx.casting())
            return None

        if ctx.DOT() is not None:
            if ctx.THIS() is None:
                simbolo_obj = self.exigir_declarado(
                    ctx.ID(0),
                    {"variavel", "parametro", "atributo"},
                    "objeto",
                )
                if simbolo_obj is not None:
                    nome_classe = simbolo_obj.tipo
                    nome_metodo = ctx.ID(1).getText()
                    info = self._classes.get(nome_classe)

                    if info is None:
                        self.erro(
                            ctx.ID(1).symbol,
                            f"classe '{nome_classe}' nao possui informacoes registradas.",
                        )
                    elif nome_metodo not in info.metodos:
                        self.erro(
                            ctx.ID(1).symbol,
                            f"metodo '{nome_metodo}' nao existe na classe '{nome_classe}'.",
                        )
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
                self.erro(
                    ctx.ID().symbol,
                    f"'{simbolo.nome}' nao e um array, mas esta sendo indexado.",
                )
            elif num_indices != simbolo.dimensoes:
                self.erro(
                    ctx.ID().symbol,
                    f"'{simbolo.nome}' tem {simbolo.dimensoes} dimensoes, "
                    f"mas {num_indices} indice(s) foram usados.",
                )
                return None

            return simbolo.tipo

        return None

    def visitExprAtribObjeto(self, ctx: JSSimplificadoParser.ExprAtribObjetoContext):
        if ctx.THIS() is None:
            simbolo_obj = self.exigir_declarado(
                ctx.ID(0),
                {"variavel", "parametro", "atributo"},
                "objeto",
            )
            if simbolo_obj is not None:
                nome_classe = simbolo_obj.tipo
                nome_atributo = ctx.ID(1).getText()
                info = self._classes.get(nome_classe)

                if info is None:
                    self.erro(
                        ctx.ID(1).symbol,
                        f"classe '{nome_classe}' nao possui informacoes registradas.",
                    )
                elif nome_atributo not in info.atributos:
                    self.erro(
                        ctx.ID(1).symbol,
                        f"atributo '{nome_atributo}' nao existe na classe '{nome_classe}'.",
                    )
                else:
                    return info.atributos[nome_atributo]
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
