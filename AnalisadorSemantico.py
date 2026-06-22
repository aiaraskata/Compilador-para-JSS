import sys
from antlr4 import FileStream, CommonTokenStream
from SemanticaLexer   import SemanticaLexer
from SemanticaParser  import SemanticaParser
from SemanticaVisitor import SemanticaVisitor


class AnalisadorSemantico(SemanticaVisitor):
    def __init__(self):
        self.tabela_simbolos = {}
        self.erros = 0

    def visitDecl(self, ctx: SemanticaParser.DeclContext):
        tipo = ctx.tipo().getText()
        nome = ctx.ID().getText()

        if nome in self.tabela_simbolos:
            print(f"Linha {ctx.start.line}: Declaracao dupla: '{nome}' ja foi declarada antes.")
            self.erros += 1
        else:
            self.tabela_simbolos[nome] = tipo
        return None

    def visitAssign(self, ctx: SemanticaParser.AssignContext):
        nome = ctx.ID().getText()

        if nome not in self.tabela_simbolos:
            print(f"Linha {ctx.start.line}: Variavel nao declarada: '{nome}' nunca foi declarada.")
            self.erros += 1
            self.visit(ctx.expr())
            return None

        tipo_var  = self.tabela_simbolos[nome]
        tipo_expr = self.visit(ctx.expr())

        if tipo_expr is not None and tipo_expr != tipo_var:
            print(f"Linha {ctx.start.line}: Erro de tipo: tentou atribuir '{tipo_expr}' na variavel '{nome}' (tipo {tipo_var}).")
            self.erros += 1
        return None

    def visitIfStat(self, ctx: SemanticaParser.IfStatContext):
        tipo_cond = self.visit(ctx.expr())

        if tipo_cond is not None and tipo_cond != 'bool':
            print(f"Linha {ctx.start.line}: Erro de tipo: condicao do 'if' e '{tipo_cond}', mas precisa ser 'bool'.")
            self.erros += 1

        for stat in ctx.stat():
            self.visit(stat)
        return None

    def visitExprArith(self, ctx: SemanticaParser.ExprArithContext):
        op = ctx.op.text
        t1 = self.visit(ctx.expr(0))
        t2 = self.visit(ctx.expr(1))

        if t1 is not None and t1 != 'int':
            print(f"Linha {ctx.start.line}: Erro de tipo: lado esquerdo de '{op}' e '{t1}', mas precisa ser 'int'.")
            self.erros += 1
        if t2 is not None and t2 != 'int':
            print(f"Linha {ctx.start.line}: Erro de tipo: lado direito de '{op}' e '{t2}', mas precisa ser 'int'.")
            self.erros += 1
        return 'int'

    def visitExprRel(self, ctx: SemanticaParser.ExprRelContext):
        op = ctx.op.text
        t1 = self.visit(ctx.expr(0))
        t2 = self.visit(ctx.expr(1))

        if t1 is not None and t2 is not None and t1 != t2:
            print(f"Linha {ctx.start.line}: Erro de tipo: '{op}' compara '{t1}' com '{t2}', os dois lados precisam ter o mesmo tipo.")
            self.erros += 1
        return 'bool'

    def visitExprUnary(self, ctx: SemanticaParser.ExprUnaryContext):
        op  = ctx.op.text
        tip = self.visit(ctx.expr())

        if op == '!':
            if tip is not None and tip != 'bool':
                print(f"Linha {ctx.start.line}: Erro de tipo: operador '!' recebeu '{tip}', mas precisa de 'bool'.")
                self.erros += 1
            return 'bool'
        else:
            if tip is not None and tip != 'int':
                print(f"Linha {ctx.start.line}: Erro de tipo: operador '{op}' recebeu '{tip}', mas precisa de 'int'.")
                self.erros += 1
            return 'int'

    def visitExprParen(self, ctx: SemanticaParser.ExprParenContext):
        return self.visit(ctx.expr())

    def visitExprInt(self, ctx: SemanticaParser.ExprIntContext):
        return 'int'

    def visitExprBool(self, ctx: SemanticaParser.ExprBoolContext):
        return 'bool'

    def visitExprId(self, ctx: SemanticaParser.ExprIdContext):
        nome = ctx.ID().getText()

        if nome not in self.tabela_simbolos:
            print(f"Linha {ctx.start.line}: Variavel nao declarada: '{nome}' usada sem ser declarada.")
            self.erros += 1
            return None
        return self.tabela_simbolos[nome]


def main():
    if len(sys.argv) != 2:
        print("Uso: python ./AnalisadorSemantico.py <arquivo.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    print(f"Iniciando Analise Semantica no arquivo: '{filename}'\n")

    try:
        input_stream = FileStream(filename, encoding='utf-8')
        lexer  = SemanticaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SemanticaParser(stream)

        tree = parser.prog()

        analisador = AnalisadorSemantico()
        analisador.visit(tree)

        if analisador.erros == 0:
            print("aceito")
        else:
            print("\nerro")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' nao encontrado.")
        sys.exit(1)


if __name__ == '__main__':
    main()