from llvmlite import ir
from antlr4 import FileStream, CommonTokenStream

from JSSimplificadoLexer import JSSimplificadoLexer
from JSSimplificadoParser import JSSimplificadoParser
from JSSimplificadoVisitor import JSSimplificadoVisitor

import os
import sys

from llvmlite import ir

class GeradorIR(JSSimplificadoVisitor):

    def __init__(self):
        self.module = ir.Module(name="jss")
        self.builder   = None   
        self.variaveis = {}    

        self.tipo_int = ir.IntType(32)
        self.tipo_real = ir.DoubleType()
        self.tipo_bool = ir.IntType(1)
        self.tipo_str  = ir.PointerType(ir.IntType(8))

    ##──────────── Retornamos o tipo identificado e registrado em nossa arquitetura ────────────

    def llvm_tipo(self, tipo_str):
        if(tipo_str == "int"):
            return self.tipo_int
        if(tipo_str == "real"):
            return self.tipo_real
        if(tipo_str == "bool"):
            return self.tipo_bool
        if tipo_str == 'str':  return self.tipo_str
        return self.tipo_int
    

    
    ##──────────── Visitando expressões literais ────────────
    ## ao visitar o nó ctx capturamos seu conteudo e devolvemos uma constante com uma tupla(tipo, valor)

    def visitExprBool(self,ctx):
        #convertemos true e false para 0 ou 1
        value = 1 if(ctx.getText() == "true") else 0
        return ir.Constant(self.tipo_bool, value)

    def visitExprInt(self,ctx):
        #convertemos o texto da expressao inteira em int
        value = int(ctx.getText())#getText é o conteudo da expressao
        return ir.Constant(self.tipo_int, value)

    def visitExprReal(self,ctx):
        value = float(ctx.getText())
        return ir.Constant(self.tipo_real, value)
    
    def visitExprStr(self,ctx):
        return None
    
    #visitamos o valor da expressão e idenficamos se o ID foi declarado antes
    def visitExprId(self,ctx):
        id_var = ctx.getText()
        if(id_var not in self.variaveis):
            print (f"Erro: variável '{id_var}' não declarada")
            return None

        #alloca é o endereço que a variável está armazenada
        #tipo_str é o tipo
        #o nome só importa para abstração do usuário
        alloca, tipo_str = self.variaveis[id_var]

        #retorna o valor armazenado no endereço alloca
        #cria a instrução e vai direto para o IR
        return self.builder.load(alloca, id_var)
    
    # retornamos um valor None de tipo str.
    def visitExprNull(self, ctx):
        return ir.Constant(self.tipo_str, None)
    
    ##──────────── trabalhando com operando ────────────

    def visitExprIncDec(self,ctx):

        ##incremento e decremento pre fixado.

        id_var = ctx.expr().getText()
        if(id_var not in self.variaveis):
            print(f"Erro: variável '{id_var}' não declarada")
            return None
        
        alloca,tipo = self.variaveis[id_var]
        value = self.builder.load(alloca,id_var)
        x = ir.Constant(self.llvm_tipo(tipo,1))
        
        if(ctx.op.text == "++"):
            new_value = self.builder.add(value,x)
        elif(ctx.op.text == "--"):
            new_value = self.builder.sub(value,x)

        self.builder.store(new_value,alloca)
        return new_value

    def visitExprUnary(self,ctx):

        value = self.visit(ctx.expr())
        operacao = ctx.op.text
        
        if(value is None):
            return None
        
        #nao vamos atualizar o valor da variavel pois ele so retorna o valor negativo ou o not
        if(operacao == "-"):
            return self.builder.neg(value)

        elif(operacao == "!"):
            return self.builder.not_(value)
        
        return value

    def visitExprPow(self,ctx):

        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))
        operacao = ctx.op.text

        if((value_x is None)or(value_y is None)):
            return None
        
        double_value_x = self.builder.sitofp(value_x, self.tipo_real)
        double_value_y = self.builder.sitofp(value_y, self.tipo_real)
        double_func = self.module.declare_intrinsic('llvm.pow', [self.tipo_real])

        return  self.builder.call(double_func, [double_value_x, double_value_y])
    
    def visitExprMulDiv(self,ctx):

        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))
        operador = ctx.op.text

        if((value_x is None) or (value_y is None)):
            return None
    
        if (operador == "*"):
            return self.builder.mul(value_x, value_y)
        if (operador == "/"):
            return self.builder.sdiv(value_x, value_y)
        if (operador == "%"):
            return self.builder.srem(value_x, value_y)

    def visitExprAddSub(self, ctx):
        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))
        operador = ctx.op.text

        if ((value_x is None) or (value_y is None)):
            return None
        
        if(operador == "+"):
            return self.builder.add(value_x, value_y)
        if(operador == '-'): 
            return self.builder.sub(value_x, value_y)

    def visitExprRel(self, ctx):

        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))
        operador = ctx.op.text

        if ((value_x is None) or (value_y is None)):
            return None
        
        relacionais = {'>':'>', '>=':'>=', '<':'<', '<=':"<="}

        return self.builder.icmp_signed(relacionais[operador], value_x, value_y)

    def visitExprEq(self, ctx):
        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))
        operador = ctx.op.text

        if ((value_x is None) or (value_y is None)):
            return None

        return self.builder.icmp_signed(operador, value_x, value_y)

    def visitExprAnd(self, ctx):
        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))

        if ((value_x is None) or (value_y is None)):
            return None

        return self.builder.and_(value_x, value_y)

    def visitExprOr(self, ctx):
        value_x = self.visit(ctx.expr(0))
        value_y = self.visit(ctx.expr(1))

        if ((value_x is None) or (value_y is None)):
            return None

        return self.builder.or_(value_x, value_y)

    def visitExprParen(self, ctx):
        return self.visit(ctx.expr())

    def visitExprAtrib(self, ctx):
        id_var = ctx.expr(0).getText()
        operador = ctx.op.text

        if (id_var not in self.variaveis):
            print(f"Erro: variável '{id_var}' não declarada.")
            return None

        alloca, tipo_str = self.variaveis[id_var]
        value_expr = self.visit(ctx.expr(1))

        if (value_expr is None):
            return None

        if (operador == '='):
            self.builder.store(value_expr, alloca)
            return value_expr

        value_atual = self.builder.load(alloca, id_var)

        if (operador == '+='):
            resultado = self.builder.add(value_atual, value_expr)
        elif (operador == '-='):
            resultado = self.builder.sub(value_atual, value_expr)
        elif (operador == '*='):
            resultado = self.builder.mul(value_atual, value_expr)
        elif (operador == '/='):
            resultado = self.builder.sdiv(value_atual, value_expr)
        elif (operador == '%='):
            resultado = self.builder.srem(value_atual, value_expr)

        self.builder.store(resultado, alloca)
        return resultado


        




