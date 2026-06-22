# Generated from JSSimplificado.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JSSimplificadoParser import JSSimplificadoParser
else:
    from JSSimplificadoParser import JSSimplificadoParser

# This class defines a complete generic visitor for a parse tree produced by JSSimplificadoParser.

class JSSimplificadoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JSSimplificadoParser#prog.
    def visitProg(self, ctx:JSSimplificadoParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#decl.
    def visitDecl(self, ctx:JSSimplificadoParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#VarSimples.
    def visitVarSimples(self, ctx:JSSimplificadoParser.VarSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#VarVetor.
    def visitVarVetor(self, ctx:JSSimplificadoParser.VarVetorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#VarObjeto.
    def visitVarObjeto(self, ctx:JSSimplificadoParser.VarObjetoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#funcDecl.
    def visitFuncDecl(self, ctx:JSSimplificadoParser.FuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#tipoRetorno.
    def visitTipoRetorno(self, ctx:JSSimplificadoParser.TipoRetornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#paramList.
    def visitParamList(self, ctx:JSSimplificadoParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#param.
    def visitParam(self, ctx:JSSimplificadoParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#classDecl.
    def visitClassDecl(self, ctx:JSSimplificadoParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#atributo.
    def visitAtributo(self, ctx:JSSimplificadoParser.AtributoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#constructorDecl.
    def visitConstructorDecl(self, ctx:JSSimplificadoParser.ConstructorDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#stmtConstructor.
    def visitStmtConstructor(self, ctx:JSSimplificadoParser.StmtConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#metodoDecl.
    def visitMetodoDecl(self, ctx:JSSimplificadoParser.MetodoDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#bloco.
    def visitBloco(self, ctx:JSSimplificadoParser.BlocoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtVarDecl.
    def visitStmtVarDecl(self, ctx:JSSimplificadoParser.StmtVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtAssign.
    def visitStmtAssign(self, ctx:JSSimplificadoParser.StmtAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtVetorAssign.
    def visitStmtVetorAssign(self, ctx:JSSimplificadoParser.StmtVetorAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtAtribObjeto.
    def visitStmtAtribObjeto(self, ctx:JSSimplificadoParser.StmtAtribObjetoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtIf.
    def visitStmtIf(self, ctx:JSSimplificadoParser.StmtIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtWhile.
    def visitStmtWhile(self, ctx:JSSimplificadoParser.StmtWhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtFor.
    def visitStmtFor(self, ctx:JSSimplificadoParser.StmtForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtBreak.
    def visitStmtBreak(self, ctx:JSSimplificadoParser.StmtBreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtReturn.
    def visitStmtReturn(self, ctx:JSSimplificadoParser.StmtReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtChamada.
    def visitStmtChamada(self, ctx:JSSimplificadoParser.StmtChamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtConsoleLog.
    def visitStmtConsoleLog(self, ctx:JSSimplificadoParser.StmtConsoleLogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtInput.
    def visitStmtInput(self, ctx:JSSimplificadoParser.StmtInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#StmtIncDec.
    def visitStmtIncDec(self, ctx:JSSimplificadoParser.StmtIncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#atribComp.
    def visitAtribComp(self, ctx:JSSimplificadoParser.AtribCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#forInit.
    def visitForInit(self, ctx:JSSimplificadoParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#forUpdate.
    def visitForUpdate(self, ctx:JSSimplificadoParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#chamadaFuncao.
    def visitChamadaFuncao(self, ctx:JSSimplificadoParser.ChamadaFuncaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#casting.
    def visitCasting(self, ctx:JSSimplificadoParser.CastingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#consolelog.
    def visitConsolelog(self, ctx:JSSimplificadoParser.ConsolelogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#inputStmt.
    def visitInputStmt(self, ctx:JSSimplificadoParser.InputStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#idList.
    def visitIdList(self, ctx:JSSimplificadoParser.IdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#exprList.
    def visitExprList(self, ctx:JSSimplificadoParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprParen.
    def visitExprParen(self, ctx:JSSimplificadoParser.ExprParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprInt.
    def visitExprInt(self, ctx:JSSimplificadoParser.ExprIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprAtrib.
    def visitExprAtrib(self, ctx:JSSimplificadoParser.ExprAtribContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprIncDec.
    def visitExprIncDec(self, ctx:JSSimplificadoParser.ExprIncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprStr.
    def visitExprStr(self, ctx:JSSimplificadoParser.ExprStrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprEq.
    def visitExprEq(self, ctx:JSSimplificadoParser.ExprEqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprAddSub.
    def visitExprAddSub(self, ctx:JSSimplificadoParser.ExprAddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprAnd.
    def visitExprAnd(self, ctx:JSSimplificadoParser.ExprAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprPow.
    def visitExprPow(self, ctx:JSSimplificadoParser.ExprPowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprAtribObjeto.
    def visitExprAtribObjeto(self, ctx:JSSimplificadoParser.ExprAtribObjetoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprChamada.
    def visitExprChamada(self, ctx:JSSimplificadoParser.ExprChamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprMulDiv.
    def visitExprMulDiv(self, ctx:JSSimplificadoParser.ExprMulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprRel.
    def visitExprRel(self, ctx:JSSimplificadoParser.ExprRelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprOr.
    def visitExprOr(self, ctx:JSSimplificadoParser.ExprOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprUnary.
    def visitExprUnary(self, ctx:JSSimplificadoParser.ExprUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprNew.
    def visitExprNew(self, ctx:JSSimplificadoParser.ExprNewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprReal.
    def visitExprReal(self, ctx:JSSimplificadoParser.ExprRealContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprNull.
    def visitExprNull(self, ctx:JSSimplificadoParser.ExprNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprBool.
    def visitExprBool(self, ctx:JSSimplificadoParser.ExprBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprId.
    def visitExprId(self, ctx:JSSimplificadoParser.ExprIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprVetor.
    def visitExprVetor(self, ctx:JSSimplificadoParser.ExprVetorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#ExprMod.
    def visitExprMod(self, ctx:JSSimplificadoParser.ExprModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JSSimplificadoParser#tipo.
    def visitTipo(self, ctx:JSSimplificadoParser.TipoContext):
        return self.visitChildren(ctx)



del JSSimplificadoParser