from MT22Visitor import MT22Visitor
from MT22Parser import MT22Parser
from AST import *


class ASTGeneration(MT22Visitor):
    # program
    def visitProgram(self, ctx: MT22Parser.ProgramContext):
        return Program(self.visit(ctx.decllist()))

    # decllist
    def visitDecllist(self, ctx: MT22Parser.DecllistContext):
        # print('visitDecllist')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.decl())
        return self.visit(ctx.decl()) + self.visit(ctx.decllist())

    # decl
    def visitDecl(self, ctx: MT22Parser.DeclContext):
        # print("visitDecl")
        return self.visit(ctx.vardecl()) if ctx.vardecl() else self.visit(ctx.funcdecl())

    # vardecl
    def visitVardecl(self, ctx: MT22Parser.VardeclContext):
        # print('visitVardecl')
        return self.visit(ctx.vardeclnoinit()) if ctx.vardeclnoinit() else self.visit(ctx.vardeclinit())

    # vardeclnoinit
    def visitVardeclnoinit(self, ctx: MT22Parser.VardeclnoinitContext):
        # print('visitVardeclnoinit')
        return [VarDecl(x, self.visit(ctx.typ())) for x in self.visit(ctx.idlist())]

    # vardeclinit
    arrayIdVarDeclInit = []
    arrayExprVarDeclInit = []

    def visitVardeclinit(self, ctx: MT22Parser.VardeclinitContext):
        # print('visitVardeclinit')
        if ctx.typ():
            self.arrayIdVarDeclInit += [ctx.ID().getText()]
            self.arrayExprVarDeclInit += [self.visit(ctx.expr())]

            arrayIdVarDeclInit = self.arrayIdVarDeclInit
            arrayExprVarDeclInit = self.arrayExprVarDeclInit[::-1]

            assocArray = list(zip(arrayIdVarDeclInit, arrayExprVarDeclInit))

            self.arrayIdVarDeclInit.clear()
            self.arrayExprVarDeclInit.clear()

            return [VarDecl(x[0], self.visit(ctx.typ()), x[1]) for x in assocArray]
        self.arrayIdVarDeclInit += [ctx.ID().getText()]
        self.arrayExprVarDeclInit += [self.visit(ctx.expr())]
        return self.visit(ctx.vardeclinit())

    def visitFuncdecl(self, ctx: MT22Parser.FuncdeclContext):
        return self.visitChildren(ctx)

    def visitParamlist(self, ctx: MT22Parser.ParamlistContext):
        return self.visitChildren(ctx)

    def visitParams(self, ctx: MT22Parser.ParamsContext):
        return self.visitChildren(ctx)

    def visitParam(self, ctx: MT22Parser.ParamContext):
        return self.visitChildren(ctx)

    def visitFunctyp(self, ctx: MT22Parser.FunctypContext):
        return self.visitChildren(ctx)

    # EXPRESSION
    # expr
    def visitExpr(self, ctx: MT22Parser.ExprContext):
        print('visitExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.relationalExpr(0))
        return BinExpr(ctx.CONCATOP().getText(), self.visit(ctx.relationalExpr(0)), self.visit(ctx.relationalExpr(1)))

    # relationalExpr
    def visitRelationalExpr(self, ctx: MT22Parser.RelationalExprContext):
        print('visitRelationalExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.logicalExpr(0))
        return BinExpr(self.visit(ctx.relationalOpt()), self.visit(ctx.logicalExpr(0)), self.visit(ctx.logicalExpr(1)))

    # relationalOpt
    def visitRelationalOpt(self, ctx: MT22Parser.RelationalOptContext):
        print('visitRelationalOpt')
        if ctx.EQCOP():
            return ctx.EQCOP().getText()
        elif ctx.NOTEQOP():
            return ctx.NOTEQOP().getText()
        elif ctx.SMOP():
            return ctx.SMOP().getText()
        elif ctx.GTOP():
            return ctx.GTOP().getText()
        elif ctx.SMEOP():
            return ctx.SMEOP().getText()
        return ctx.GTEOP().getText()

    # logicalExpr
    def visitLogicalExpr(self, ctx: MT22Parser.LogicalExprContext):
        print('visitLogicalExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.addExpr())
        return BinExpr(self.visit(ctx.logicalOpt()), self.visit(ctx.logicalExpr()), self.visit(ctx.addExpr()))

    # logicalOpt
    def visitLogicalOpt(self, ctx: MT22Parser.LogicalOptContext):
        print('visitLogicalOpt')
        if ctx.ANDOP():
            return ctx.ANDOP().getText()
        return ctx.OROP.getText()

    # addExpr
    def visitAddExpr(self, ctx: MT22Parser.AddExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.multiExpr())
        return BinExpr(self.visit(ctx.addOpt()), self.visit(ctx.addExpr()), self.visit(ctx.multiExpr()))

    # addOpt
    def visitAddOpt(self, ctx: MT22Parser.AddOptContext):
        print('visitAddOpt')
        return ctx.ADDOP().getText() if ctx.ADDOP() else ctx.SUBOP().getText()

    # multiExpr
    def visitMultiExpr(self, ctx: MT22Parser.MultiExprContext):
        print('visistMultiExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.unaryLogicalExpr())
        return BinExpr(self.visit(ctx.multiOpt()), self.visit(ctx.multiExpr()), self.visit(ctx.unaryLogicalExpr()))

    # multiOpt
    def visitMultiOpt(self, ctx: MT22Parser.MultiOptContext):
        print('visitMultiOpt')
        if ctx.MULOP():
            return ctx.MULOP().getText()
        elif ctx.DIVOP():
            return ctx.DIVOP().getText()
        return ctx.MODOP().getText()

    # logicalExpr
    def visitUnaryLogicalExpr(self, ctx: MT22Parser.UnaryLogicalExprContext):
        print('visitUnaryLogicalExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.signExpr())
        return UnExpr(ctx.NOTOP().getText(), self.visit(ctx.unaryLogicalExpr()))

    # signExpr
    def visitSignExpr(self, ctx: MT22Parser.SignExprContext):
        print('visitSignExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.indexOptExpr())
        return UnExpr(ctx.SUBOP().getText(), self.visit(ctx.signExpr()))

    # indexOptExpr
    def visitIndexOptExpr(self, ctx: MT22Parser.IndexOptExprContext):
        print('visitIndexOptExpr')
        if ctx.getChildCount() == 1:
            return self.visit(ctx.subexpr())
        # ID LS nonnullexprlist RS
        return None

    # subexpr
    def visitSubexpr(self, ctx: MT22Parser.SubexprContext):
        print('visitSubexpr')
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.alllit():
            return self.visit(ctx.alllit())
        elif ctx.expr():
            return self.visit(ctx.expr())
        return self.visit(ctx.callexpr())

    def visitCallexpr(self, ctx: MT22Parser.CallexprContext):
        return self.visitChildren(ctx)

    def visitStmt(self, ctx: MT22Parser.StmtContext):
        return self.visitChildren(ctx)

    def visitAssignstmt(self, ctx: MT22Parser.AssignstmtContext):
        return self.visitChildren(ctx)

    def visitIfstmt(self, ctx: MT22Parser.IfstmtContext):
        return self.visitChildren(ctx)

    def visitForstmt(self, ctx: MT22Parser.ForstmtContext):
        return self.visitChildren(ctx)

    def visitInitexpr(self, ctx: MT22Parser.InitexprContext):
        return self.visitChildren(ctx)

    def visitConditionexpr(self, ctx: MT22Parser.ConditionexprContext):
        return self.visitChildren(ctx)

    def visitUpdateexpr(self, ctx: MT22Parser.UpdateexprContext):
        return self.visitChildren(ctx)

    def visitWhilestmt(self, ctx: MT22Parser.WhilestmtContext):
        return self.visitChildren(ctx)

    def visitDowhilestmt(self, ctx: MT22Parser.DowhilestmtContext):
        return self.visitChildren(ctx)

    def visitBreakstmt(self, ctx: MT22Parser.BreakstmtContext):
        return self.visitChildren(ctx)

    def visitContinuestmt(self, ctx: MT22Parser.ContinuestmtContext):
        return self.visitChildren(ctx)

    def visitReturnstmt(self, ctx: MT22Parser.ReturnstmtContext):
        return self.visitChildren(ctx)

    def visitCallstmt(self, ctx: MT22Parser.CallstmtContext):
        return self.visitChildren(ctx)

    def visitBlockstmt(self, ctx: MT22Parser.BlockstmtContext):
        return self.visitChildren(ctx)

    def visitBlockstmtbody(self, ctx: MT22Parser.BlockstmtbodyContext):
        return self.visitChildren(ctx)

    def visitDeclandstmts(self, ctx: MT22Parser.DeclandstmtsContext):
        return self.visitChildren(ctx)

    def visitDeclandstmt(self, ctx: MT22Parser.DeclandstmtContext):
        return self.visitChildren(ctx)

    def visitScalarvar(self, ctx: MT22Parser.ScalarvarContext):
        return self.visitChildren(ctx)

    def visitNonullexprlist(self, ctx: MT22Parser.NonullexprlistContext):
        return self.visitChildren(ctx)

    def visitNullexprlist(self, ctx: MT22Parser.NullexprlistContext):
        return self.visitChildren(ctx)

    # IDLIST & TYP
    # idlist
    def visitIdlist(self, ctx: MT22Parser.IdlistContext):
        # print('visitIdlist')
        if ctx.getChildCount() == 1:
            return [ctx.ID().getText()]
        return [ctx.ID().getText()] + self.visit(ctx.idlist())

    # typ
    def visitTyp(self, ctx: MT22Parser.TypContext):
        # print('visitTyp')
        if ctx.INT():
            return IntegerType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        elif ctx.BOOLEAN():
            return BooleanType()
        elif ctx.AUTO():
            return AutoType()
        return self.visit(ctx.arraytyp())

    # arrayTyp
    def visitArraytyp(self, ctx: MT22Parser.ArraytypContext):
        # print('visitArraytyp')
        return ArrayType(self.visit(ctx.intList()), self.visit(ctx.typ()))

    # intList
    def visitIntList(self, ctx: MT22Parser.IntListContext):
        # print('visitIntList')
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.intandexpr())]
        return [self.visit(ctx.intandexpr())] + self.visit(ctx.intList())

    # intandexpr
    def visitIntandexpr(self, ctx: MT22Parser.IntandexprContext):
        # print('visitIntandexpr')
        if ctx.INTLIT():
            return int(ctx.INTLIT().getText())
        return self.visit(ctx.expr())

    # alllit: INTLIT | STRINGLIT | FLOATLIT | TRUE | FALSE | arrayLit;
    def visitAlllit(self, ctx: MT22Parser.AlllitContext):
        print('visitAlllit')
        if ctx.INTLIT():
            return IntegerLit(int(ctx.INTLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLit(ctx.STRINGLIT().getText())
        elif ctx.FLOATLIT():
            return FloatLit(float(ctx.FLOATLIT().getText()))
        elif ctx.TRUE() or ctx.FALSE():
            return BooleanLit(True if ctx.TRUE() else False)
        return self.visit(ctx.arrayLit())

    def visitArrayLit(self, ctx: MT22Parser.ArrayLitContext):
        return self.visitChildren(ctx)

    def visitArrayElements(self, ctx: MT22Parser.ArrayElementsContext):
        return self.visitChildren(ctx)

    def visitAlllits(self, ctx: MT22Parser.AlllitsContext):
        return self.visitChildren(ctx)

    # SPECIAL FUNCTIONS
    def visitSpecialFunc(self, ctx: MT22Parser.SpecialFuncContext):
        return self.visitChildren(ctx)

    def visitReadInt(self, ctx: MT22Parser.ReadIntContext):
        return self.visitChildren(ctx)

    # # def visitPrintInt(self, ctx: MT22Parser.PrintIntContext):
        return self.visitChildren(ctx)

    def visitReadFloat(self, ctx: MT22Parser.ReadFloatContext):
        return self.visitChildren(ctx)

    def visitWriteFloat(self, ctx: MT22Parser.WriteFloatContext):
        return self.visitChildren(ctx)

    def visitReadBoolean(self, ctx: MT22Parser.ReadBooleanContext):
        return self.visitChildren(ctx)

    # # def visitPrintBoolean(self, ctx: MT22Parser.PrintBooleanContext):
        return self.visitChildren(ctx)

    def visitReadString(self, ctx: MT22Parser.ReadStringContext):
        return self.visitChildren(ctx)

    # # def visitPrintString(self, ctx: MT22Parser.PrintStringContext):
        return self.visitChildren(ctx)

    def visitSuperFunc(self, ctx: MT22Parser.SuperFuncContext):
        return self.visitChildren(ctx)

    def visitPreventDefault(self, ctx: MT22Parser.PreventDefaultContext):
        return self.visitChildren(ctx)
