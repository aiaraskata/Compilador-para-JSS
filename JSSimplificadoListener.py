# Generated from JSSimplificado.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JSSimplificadoParser import JSSimplificadoParser
else:
    from JSSimplificadoParser import JSSimplificadoParser

# This class defines a complete listener for a parse tree produced by JSSimplificadoParser.
class JSSimplificadoListener(ParseTreeListener):

    # Enter a parse tree produced by JSSimplificadoParser#prog.
    def enterProg(self, ctx:JSSimplificadoParser.ProgContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#prog.
    def exitProg(self, ctx:JSSimplificadoParser.ProgContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#decl.
    def enterDecl(self, ctx:JSSimplificadoParser.DeclContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#decl.
    def exitDecl(self, ctx:JSSimplificadoParser.DeclContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#VarSimples.
    def enterVarSimples(self, ctx:JSSimplificadoParser.VarSimplesContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#VarSimples.
    def exitVarSimples(self, ctx:JSSimplificadoParser.VarSimplesContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#VarVetor.
    def enterVarVetor(self, ctx:JSSimplificadoParser.VarVetorContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#VarVetor.
    def exitVarVetor(self, ctx:JSSimplificadoParser.VarVetorContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#VarObjeto.
    def enterVarObjeto(self, ctx:JSSimplificadoParser.VarObjetoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#VarObjeto.
    def exitVarObjeto(self, ctx:JSSimplificadoParser.VarObjetoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#funcDecl.
    def enterFuncDecl(self, ctx:JSSimplificadoParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#funcDecl.
    def exitFuncDecl(self, ctx:JSSimplificadoParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#tipoRetorno.
    def enterTipoRetorno(self, ctx:JSSimplificadoParser.TipoRetornoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#tipoRetorno.
    def exitTipoRetorno(self, ctx:JSSimplificadoParser.TipoRetornoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#paramList.
    def enterParamList(self, ctx:JSSimplificadoParser.ParamListContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#paramList.
    def exitParamList(self, ctx:JSSimplificadoParser.ParamListContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#param.
    def enterParam(self, ctx:JSSimplificadoParser.ParamContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#param.
    def exitParam(self, ctx:JSSimplificadoParser.ParamContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#classDecl.
    def enterClassDecl(self, ctx:JSSimplificadoParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#classDecl.
    def exitClassDecl(self, ctx:JSSimplificadoParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#atributo.
    def enterAtributo(self, ctx:JSSimplificadoParser.AtributoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#atributo.
    def exitAtributo(self, ctx:JSSimplificadoParser.AtributoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#constructorDecl.
    def enterConstructorDecl(self, ctx:JSSimplificadoParser.ConstructorDeclContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#constructorDecl.
    def exitConstructorDecl(self, ctx:JSSimplificadoParser.ConstructorDeclContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#stmtConstructor.
    def enterStmtConstructor(self, ctx:JSSimplificadoParser.StmtConstructorContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#stmtConstructor.
    def exitStmtConstructor(self, ctx:JSSimplificadoParser.StmtConstructorContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#metodoDecl.
    def enterMetodoDecl(self, ctx:JSSimplificadoParser.MetodoDeclContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#metodoDecl.
    def exitMetodoDecl(self, ctx:JSSimplificadoParser.MetodoDeclContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#bloco.
    def enterBloco(self, ctx:JSSimplificadoParser.BlocoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#bloco.
    def exitBloco(self, ctx:JSSimplificadoParser.BlocoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtVarDecl.
    def enterStmtVarDecl(self, ctx:JSSimplificadoParser.StmtVarDeclContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtVarDecl.
    def exitStmtVarDecl(self, ctx:JSSimplificadoParser.StmtVarDeclContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtAssign.
    def enterStmtAssign(self, ctx:JSSimplificadoParser.StmtAssignContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtAssign.
    def exitStmtAssign(self, ctx:JSSimplificadoParser.StmtAssignContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtVetorAssign.
    def enterStmtVetorAssign(self, ctx:JSSimplificadoParser.StmtVetorAssignContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtVetorAssign.
    def exitStmtVetorAssign(self, ctx:JSSimplificadoParser.StmtVetorAssignContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtAtribObjeto.
    def enterStmtAtribObjeto(self, ctx:JSSimplificadoParser.StmtAtribObjetoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtAtribObjeto.
    def exitStmtAtribObjeto(self, ctx:JSSimplificadoParser.StmtAtribObjetoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtIf.
    def enterStmtIf(self, ctx:JSSimplificadoParser.StmtIfContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtIf.
    def exitStmtIf(self, ctx:JSSimplificadoParser.StmtIfContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtWhile.
    def enterStmtWhile(self, ctx:JSSimplificadoParser.StmtWhileContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtWhile.
    def exitStmtWhile(self, ctx:JSSimplificadoParser.StmtWhileContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtFor.
    def enterStmtFor(self, ctx:JSSimplificadoParser.StmtForContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtFor.
    def exitStmtFor(self, ctx:JSSimplificadoParser.StmtForContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtBreak.
    def enterStmtBreak(self, ctx:JSSimplificadoParser.StmtBreakContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtBreak.
    def exitStmtBreak(self, ctx:JSSimplificadoParser.StmtBreakContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtReturn.
    def enterStmtReturn(self, ctx:JSSimplificadoParser.StmtReturnContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtReturn.
    def exitStmtReturn(self, ctx:JSSimplificadoParser.StmtReturnContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtChamada.
    def enterStmtChamada(self, ctx:JSSimplificadoParser.StmtChamadaContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtChamada.
    def exitStmtChamada(self, ctx:JSSimplificadoParser.StmtChamadaContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtConsoleLog.
    def enterStmtConsoleLog(self, ctx:JSSimplificadoParser.StmtConsoleLogContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtConsoleLog.
    def exitStmtConsoleLog(self, ctx:JSSimplificadoParser.StmtConsoleLogContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtInput.
    def enterStmtInput(self, ctx:JSSimplificadoParser.StmtInputContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtInput.
    def exitStmtInput(self, ctx:JSSimplificadoParser.StmtInputContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#StmtIncDec.
    def enterStmtIncDec(self, ctx:JSSimplificadoParser.StmtIncDecContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#StmtIncDec.
    def exitStmtIncDec(self, ctx:JSSimplificadoParser.StmtIncDecContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#atribComp.
    def enterAtribComp(self, ctx:JSSimplificadoParser.AtribCompContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#atribComp.
    def exitAtribComp(self, ctx:JSSimplificadoParser.AtribCompContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#forInit.
    def enterForInit(self, ctx:JSSimplificadoParser.ForInitContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#forInit.
    def exitForInit(self, ctx:JSSimplificadoParser.ForInitContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#forUpdate.
    def enterForUpdate(self, ctx:JSSimplificadoParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#forUpdate.
    def exitForUpdate(self, ctx:JSSimplificadoParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#chamadaFuncao.
    def enterChamadaFuncao(self, ctx:JSSimplificadoParser.ChamadaFuncaoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#chamadaFuncao.
    def exitChamadaFuncao(self, ctx:JSSimplificadoParser.ChamadaFuncaoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#casting.
    def enterCasting(self, ctx:JSSimplificadoParser.CastingContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#casting.
    def exitCasting(self, ctx:JSSimplificadoParser.CastingContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#consolelog.
    def enterConsolelog(self, ctx:JSSimplificadoParser.ConsolelogContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#consolelog.
    def exitConsolelog(self, ctx:JSSimplificadoParser.ConsolelogContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#inputStmt.
    def enterInputStmt(self, ctx:JSSimplificadoParser.InputStmtContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#inputStmt.
    def exitInputStmt(self, ctx:JSSimplificadoParser.InputStmtContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#idList.
    def enterIdList(self, ctx:JSSimplificadoParser.IdListContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#idList.
    def exitIdList(self, ctx:JSSimplificadoParser.IdListContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#exprList.
    def enterExprList(self, ctx:JSSimplificadoParser.ExprListContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#exprList.
    def exitExprList(self, ctx:JSSimplificadoParser.ExprListContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprParen.
    def enterExprParen(self, ctx:JSSimplificadoParser.ExprParenContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprParen.
    def exitExprParen(self, ctx:JSSimplificadoParser.ExprParenContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprInt.
    def enterExprInt(self, ctx:JSSimplificadoParser.ExprIntContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprInt.
    def exitExprInt(self, ctx:JSSimplificadoParser.ExprIntContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprAtrib.
    def enterExprAtrib(self, ctx:JSSimplificadoParser.ExprAtribContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprAtrib.
    def exitExprAtrib(self, ctx:JSSimplificadoParser.ExprAtribContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprIncDec.
    def enterExprIncDec(self, ctx:JSSimplificadoParser.ExprIncDecContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprIncDec.
    def exitExprIncDec(self, ctx:JSSimplificadoParser.ExprIncDecContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprStr.
    def enterExprStr(self, ctx:JSSimplificadoParser.ExprStrContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprStr.
    def exitExprStr(self, ctx:JSSimplificadoParser.ExprStrContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprEq.
    def enterExprEq(self, ctx:JSSimplificadoParser.ExprEqContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprEq.
    def exitExprEq(self, ctx:JSSimplificadoParser.ExprEqContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprAddSub.
    def enterExprAddSub(self, ctx:JSSimplificadoParser.ExprAddSubContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprAddSub.
    def exitExprAddSub(self, ctx:JSSimplificadoParser.ExprAddSubContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprAnd.
    def enterExprAnd(self, ctx:JSSimplificadoParser.ExprAndContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprAnd.
    def exitExprAnd(self, ctx:JSSimplificadoParser.ExprAndContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprPow.
    def enterExprPow(self, ctx:JSSimplificadoParser.ExprPowContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprPow.
    def exitExprPow(self, ctx:JSSimplificadoParser.ExprPowContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprAtribObjeto.
    def enterExprAtribObjeto(self, ctx:JSSimplificadoParser.ExprAtribObjetoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprAtribObjeto.
    def exitExprAtribObjeto(self, ctx:JSSimplificadoParser.ExprAtribObjetoContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprChamada.
    def enterExprChamada(self, ctx:JSSimplificadoParser.ExprChamadaContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprChamada.
    def exitExprChamada(self, ctx:JSSimplificadoParser.ExprChamadaContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprMulDiv.
    def enterExprMulDiv(self, ctx:JSSimplificadoParser.ExprMulDivContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprMulDiv.
    def exitExprMulDiv(self, ctx:JSSimplificadoParser.ExprMulDivContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprRel.
    def enterExprRel(self, ctx:JSSimplificadoParser.ExprRelContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprRel.
    def exitExprRel(self, ctx:JSSimplificadoParser.ExprRelContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprOr.
    def enterExprOr(self, ctx:JSSimplificadoParser.ExprOrContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprOr.
    def exitExprOr(self, ctx:JSSimplificadoParser.ExprOrContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprUnary.
    def enterExprUnary(self, ctx:JSSimplificadoParser.ExprUnaryContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprUnary.
    def exitExprUnary(self, ctx:JSSimplificadoParser.ExprUnaryContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprNew.
    def enterExprNew(self, ctx:JSSimplificadoParser.ExprNewContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprNew.
    def exitExprNew(self, ctx:JSSimplificadoParser.ExprNewContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprReal.
    def enterExprReal(self, ctx:JSSimplificadoParser.ExprRealContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprReal.
    def exitExprReal(self, ctx:JSSimplificadoParser.ExprRealContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprNull.
    def enterExprNull(self, ctx:JSSimplificadoParser.ExprNullContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprNull.
    def exitExprNull(self, ctx:JSSimplificadoParser.ExprNullContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprBool.
    def enterExprBool(self, ctx:JSSimplificadoParser.ExprBoolContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprBool.
    def exitExprBool(self, ctx:JSSimplificadoParser.ExprBoolContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprId.
    def enterExprId(self, ctx:JSSimplificadoParser.ExprIdContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprId.
    def exitExprId(self, ctx:JSSimplificadoParser.ExprIdContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprVetor.
    def enterExprVetor(self, ctx:JSSimplificadoParser.ExprVetorContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprVetor.
    def exitExprVetor(self, ctx:JSSimplificadoParser.ExprVetorContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#ExprMod.
    def enterExprMod(self, ctx:JSSimplificadoParser.ExprModContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#ExprMod.
    def exitExprMod(self, ctx:JSSimplificadoParser.ExprModContext):
        pass


    # Enter a parse tree produced by JSSimplificadoParser#tipo.
    def enterTipo(self, ctx:JSSimplificadoParser.TipoContext):
        pass

    # Exit a parse tree produced by JSSimplificadoParser#tipo.
    def exitTipo(self, ctx:JSSimplificadoParser.TipoContext):
        pass



del JSSimplificadoParser