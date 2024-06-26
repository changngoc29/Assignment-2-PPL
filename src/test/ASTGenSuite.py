import unittest
from TestUtils import TestAST
from AST import *


class ASTGenSuite(unittest.TestCase):
    def test_short_vardecl(self):
        input = """x: integer;"""
        expect = str(Program([VarDecl("x", IntegerType())]))
        # print(expect)
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_full_vardecl(self):
        input = """x, y, z: integer = 1, 2, 3;"""
        expect = """Program([
	VarDecl(x, IntegerType, IntegerLit(1))
	VarDecl(y, IntegerType, IntegerLit(2))
	VarDecl(z, IntegerType, IntegerLit(3))
])"""
        self.assertTrue(TestAST.test(input, expect, 301))

    def test_vardecls(self):
        input = """x, y, z: integer = 1, 2, 3;
        a, b: float;"""
        expect = """Program([
	VarDecl(x, IntegerType, IntegerLit(1))
	VarDecl(y, IntegerType, IntegerLit(2))
	VarDecl(z, IntegerType, IntegerLit(3))
	VarDecl(a, FloatType)
	VarDecl(b, FloatType)
])"""
        self.assertTrue(TestAST.test(input, expect, 302))

    def test_simple_program(self):
        """Simple program"""
        input = """main: function void () {
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 303))

    def test_more_complex_program(self):
        """More complex program"""
        input = """main: function void () {
            printInteger(4);
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(printInteger, IntegerLit(4))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 304))

    def testcase5(self):
        # test vardecl with no init of array
        input = """x: array[2,3] of integer;"""
        expect = str(Program([
            VarDecl("x", ArrayType([2, 3], IntegerType()))
        ]))
        self.assertTrue(TestAST.test(input, expect, 305))

    def testcase6(self):
        # test vardecl with init of expression
        input = """x, y: integer = 1*2, 2+3;
                    a: string = "abc" :: "def";"""
        expect = """Program([
	VarDecl(x, IntegerType, BinExpr(*, IntegerLit(1), IntegerLit(2)))
	VarDecl(y, IntegerType, BinExpr(+, IntegerLit(2), IntegerLit(3)))
	VarDecl(a, StringType, BinExpr(::, StringLit(abc), StringLit(def)))
])"""
        self.assertTrue(TestAST.test(input, expect, 306))

    def testcase7(self):
        # test vardecl with init of expression
        input = """x, y: integer = 1*2, 2+3;
                    a: string = "abc" :: "def";
                    a: integer = a[1+2, 1*5];"""
        expect = """Program([
	VarDecl(x, IntegerType, BinExpr(*, IntegerLit(1), IntegerLit(2)))
	VarDecl(y, IntegerType, BinExpr(+, IntegerLit(2), IntegerLit(3)))
	VarDecl(a, StringType, BinExpr(::, StringLit(abc), StringLit(def)))
	VarDecl(a, IntegerType, ArrayCell(a, [BinExpr(+, IntegerLit(1), IntegerLit(2)), BinExpr(*, IntegerLit(1), IntegerLit(5))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 307))

    def testcase8(self):
        # test vardecl with init of expression
        input = """x, y: integer = 1*2, 2+3;
                    a: string = "abc" :: "def";
                    d: integer = a[1+2, 1*5];
                    c: string = a(1, f("abc"));"""
        expect = """Program([
	VarDecl(x, IntegerType, BinExpr(*, IntegerLit(1), IntegerLit(2)))
	VarDecl(y, IntegerType, BinExpr(+, IntegerLit(2), IntegerLit(3)))
	VarDecl(a, StringType, BinExpr(::, StringLit(abc), StringLit(def)))
	VarDecl(d, IntegerType, ArrayCell(a, [BinExpr(+, IntegerLit(1), IntegerLit(2)), BinExpr(*, IntegerLit(1), IntegerLit(5))]))
	VarDecl(c, StringType, FuncCall(a, [IntegerLit(1), FuncCall(f, [StringLit(abc)])]))
])"""
        self.assertTrue(TestAST.test(input, expect, 308))

    def testcase9(self):
        # test vardecl with no init of array
        input = """x: array[2,3] of integer = {1,2,3};"""
        expect = """Program([
	VarDecl(x, ArrayType([2, 3], IntegerType), ArrayLit([IntegerLit(1), IntegerLit(2), IntegerLit(3)]))
])"""
        self.assertTrue(TestAST.test(input, expect, 309))

    def testcase10(self):
        # test basic funcdecls
        input = """
    foo: function void (inherit a: integer, inherit out b: float) inherit bar {}

    main: function void () {
        printInteger(4);
}"""
        expect = """Program([
	FuncDecl(foo, VoidType, [InheritParam(a, IntegerType), InheritOutParam(b, FloatType)], bar, BlockStmt([]))
	FuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(printInteger, IntegerLit(4))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 310))

    def testcase11(self):
        # test funcdecls
        input = """main: function void () {
        x: integer;
        x = (3+4)*2;
        b: array [2] of float;
        b[0] = 4.5;
        preventDefault();
}"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([VarDecl(x, IntegerType), AssignStmt(Id(x), BinExpr(*, BinExpr(+, IntegerLit(3), IntegerLit(4)), IntegerLit(2))), VarDecl(b, ArrayType([2], FloatType)), AssignStmt(ArrayCell(b, [IntegerLit(0)]), FloatLit(4.5)), CallStmt(preventDefault, )]))
])"""
        self.assertTrue(TestAST.test(input, expect, 311))

    def testcase12(self):
        # ifstmt without blockstmt and else
        input = """
    main: function void () {
        if (3 > 4 + 5) a[0] = "hello world";
}"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, IntegerLit(3), BinExpr(+, IntegerLit(4), IntegerLit(5))), AssignStmt(ArrayCell(a, [IntegerLit(0)]), StringLit(hello world)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 312))

    def testcase13(self):
        # ifstmt without blockstmt but have else
        input = """
    main: function void () {
        if (3 > 4 + 5) a[0] = "hello world";
        else a[0] = "hello world in else";
}"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, IntegerLit(3), BinExpr(+, IntegerLit(4), IntegerLit(5))), AssignStmt(ArrayCell(a, [IntegerLit(0)]), StringLit(hello world)), AssignStmt(ArrayCell(a, [IntegerLit(0)]), StringLit(hello world in else)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 313))

    def testcase14(self):
        # forstmt without block
        input = """
    a,b,c : array [2] of integer = {1,1}, {2,2}, {3,5-4};
    main: function void () {
        for (i=1,i<100,i+1) break;
}"""
        expect = """Program([
	VarDecl(a, ArrayType([2], IntegerType), ArrayLit([IntegerLit(1), IntegerLit(1)]))
	VarDecl(b, ArrayType([2], IntegerType), ArrayLit([IntegerLit(2), IntegerLit(2)]))
	VarDecl(c, ArrayType([2], IntegerType), ArrayLit([IntegerLit(3), BinExpr(-, IntegerLit(5), IntegerLit(4))]))
	FuncDecl(main, VoidType, [], None, BlockStmt([ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), IntegerLit(100)), BinExpr(+, Id(i), IntegerLit(1)), BreakStmt())]))
])"""
        self.assertTrue(TestAST.test(input, expect, 314))

    def testcase15(self):
        # forstmt with block
        input = """
    main: function void () {
        for (i=1,i<100,i+1) {
            if (a<1) continue;
            a: boolean = false;
        }
}"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), IntegerLit(100)), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([IfStmt(BinExpr(<, Id(a), IntegerLit(1)), ContinueStmt()), VarDecl(a, BooleanType, BooleanLit(False))]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 315))

    def testcase16(self):
        # whilestmt without block
        input = """
    testfunc: function integer (a: integer) {
        while (a < 10) a = a + 1;
        return a + 3;
    }
    main: function void () {
        testfunc();
}"""
        expect = """Program([
	FuncDecl(testfunc, IntegerType, [Param(a, IntegerType)], None, BlockStmt([WhileStmt(BinExpr(<, Id(a), IntegerLit(10)), AssignStmt(Id(a), BinExpr(+, Id(a), IntegerLit(1)))), ReturnStmt(BinExpr(+, Id(a), IntegerLit(3)))]))
	FuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(testfunc, )]))
])"""
        self.assertTrue(TestAST.test(input, expect, 316))

    def testcase17(self):
        # whilestmt with block
        input = """
    testfunc: function integer (a: integer) {
        while (a < 10) {
            for (i=1,i<10,i+1) a = a + 1;
        }
        readBoolean(a==10);
        return a + 3;
    }
    main: function void () {
        testfunc();
}"""
        expect = """Program([
	FuncDecl(testfunc, IntegerType, [Param(a, IntegerType)], None, BlockStmt([WhileStmt(BinExpr(<, Id(a), IntegerLit(10)), BlockStmt([ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), IntegerLit(10)), BinExpr(+, Id(i), IntegerLit(1)), AssignStmt(Id(a), BinExpr(+, Id(a), IntegerLit(1))))])), CallStmt(readBoolean, BinExpr(==, Id(a), IntegerLit(10))), ReturnStmt(BinExpr(+, Id(a), IntegerLit(3)))]))
	FuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(testfunc, )]))
])"""
        self.assertTrue(TestAST.test(input, expect, 317))

    def testcase18(self):
        # dowhile
        input = """
    testfunc: function integer (c: string) {
        do {
            readString("abc");
            c = c :: "abc";
            printString(c);
        } while (c != "" );
        return 1;
    }
    main: function void () {
        testfunc();
}"""
        expect = """Program([
	FuncDecl(testfunc, IntegerType, [Param(c, StringType)], None, BlockStmt([DoWhileStmt(BinExpr(!=, Id(c), StringLit()), BlockStmt([CallStmt(readString, StringLit(abc)), AssignStmt(Id(c), BinExpr(::, Id(c), StringLit(abc))), CallStmt(printString, Id(c))])), ReturnStmt(IntegerLit(1))]))
	FuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(testfunc, )]))
])"""
        self.assertTrue(TestAST.test(input, expect, 318))

    def testcase19(self):
        input = """
    testfunc: function auto (a: boolean) {
        while (a < 10) {
            {
                a = a + 1;
            }
        }
    }
"""
        expect = """Program([
	FuncDecl(testfunc, AutoType, [Param(a, BooleanType)], None, BlockStmt([WhileStmt(BinExpr(<, Id(a), IntegerLit(10)), BlockStmt([BlockStmt([AssignStmt(Id(a), BinExpr(+, Id(a), IntegerLit(1)))])]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 319))

    def testcase20(self):
        input = """
    testfunc: function string (a: boolean) {
        x: float = 1.5e-10 + x + y;
    }
"""
        expect = """Program([
	FuncDecl(testfunc, StringType, [Param(a, BooleanType)], None, BlockStmt([VarDecl(x, FloatType, BinExpr(+, BinExpr(+, FloatLit(1.5e-10), Id(x)), Id(y)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 320))

    def testcase21(self):
        input = """
    testfunc: function void (inherit out a: array[1] of boolean) {
        if(a[1, 2] == "true")
            super(printInteger(a[1*2, 3+4]), x%2);
    }
"""
        expect = """Program([
	FuncDecl(testfunc, VoidType, [InheritOutParam(a, ArrayType([1], BooleanType))], None, BlockStmt([IfStmt(BinExpr(==, ArrayCell(a, [IntegerLit(1), IntegerLit(2)]), StringLit(true)), CallStmt(super, FuncCall(printInteger, [ArrayCell(a, [BinExpr(*, IntegerLit(1), IntegerLit(2)), BinExpr(+, IntegerLit(3), IntegerLit(4))])]), BinExpr(%, Id(x), IntegerLit(2))))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 321))

    def testcase23(self):
        input = """
    testfunc: function void (inherit out a: array[2, 3] of boolean) inherit foo {
        if(a[a[1, 2], 2] == "true") {
            {
                {
                    a[a[a[1, 2], 3], 2] = "false";
                }
            }
        }
            
    }
"""
        expect = """Program([
	FuncDecl(testfunc, VoidType, [InheritOutParam(a, ArrayType([2, 3], BooleanType))], foo, BlockStmt([IfStmt(BinExpr(==, ArrayCell(a, [ArrayCell(a, [IntegerLit(1), IntegerLit(2)]), IntegerLit(2)]), StringLit(true)), BlockStmt([BlockStmt([BlockStmt([AssignStmt(ArrayCell(a, [ArrayCell(a, [ArrayCell(a, [IntegerLit(1), IntegerLit(2)]), IntegerLit(3)]), IntegerLit(2)]), StringLit(false))])])]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 323))

    def testcase25(self):
        prog = """dd: integer;"""
        expect = str(Program([VarDecl("dd", typ=IntegerType())]))
        self.assertTrue(TestAST.test(prog, expect, 325))

    def testcase26(self):
        prog = """a, b, c, d, e, f, g, h: integer;"""
        expect = str(
            Program(
                [
                    VarDecl("a", typ=IntegerType()),
                    VarDecl("b", typ=IntegerType()),
                    VarDecl("c", typ=IntegerType()),
                    VarDecl("d", typ=IntegerType()),
                    VarDecl("e", typ=IntegerType()),
                    VarDecl("f", typ=IntegerType()),
                    VarDecl("g", typ=IntegerType()),
                    VarDecl("h", typ=IntegerType()),
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 326))

    def testcase27(self):
        prog = """a: integer = 2023;"""
        expect = str(
            Program([VarDecl("a", typ=IntegerType(), init=IntegerLit(2023))]))
        self.assertTrue(TestAST.test(prog, expect, 327))

    def testcase28(self):
        prog = "a: auto = arr[1, foo(), three, 2*2];"
        expect = str(
            Program(
                [
                    VarDecl(
                        "a",
                        AutoType(),
                        ArrayCell(
                            "arr",
                            [
                                IntegerLit(1),
                                FuncCall("foo", []),
                                Id("three"),
                                BinExpr("*", IntegerLit(2), IntegerLit(2)),
                            ],
                        ),
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 328), f"Correct {expect}")

    def testcase329(self):
        prog = """a: integer = -404;
b: boolean = !true;"""
        expect = str(
            Program(
                [
                    VarDecl("a", typ=IntegerType(),
                            init=UnExpr("-", IntegerLit(404))),
                    VarDecl("b", typ=BooleanType(),
                            init=UnExpr("!", BooleanLit(True))),
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 329),
                        f"Correct: \n{expect}")

    def testcase330(self):
        prog = """a: integer = -101 * -4;"""
        expect = str(
            Program(
                [
                    VarDecl(
                        "a",
                        typ=IntegerType(),
                        init=BinExpr(
                            "*", UnExpr("-", IntegerLit(101)
                                        ), UnExpr("-", IntegerLit(4))
                        ),
                    ),
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 330),
                        f"Correct: \n{expect}")

    def testcase331(self):
        prog = "lol: integer = 11 + - 2;"
        expect = str(
            Program(
                [
                    VarDecl(
                        name="lol",
                        typ=IntegerType(),
                        init=BinExpr(
                            op="+",
                            left=IntegerLit(11),
                            right=UnExpr(op="-", val=IntegerLit(2)),
                        ),
                    ),
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 331), f"Correct {expect}")

    def testcase332(self):
        prog = "a: integer = 100 + 100 * -100 - 100 / 100 + 100 % 100;"
        expect = str(
            Program(
                [
                    VarDecl(
                        "a",
                        IntegerType(),
                        init=BinExpr(
                            op="+",
                            left=BinExpr(
                                op="-",
                                left=BinExpr(
                                    op="+",
                                    left=IntegerLit(100),
                                    right=BinExpr(
                                        op="*",
                                        left=IntegerLit(100),
                                        right=UnExpr(
                                            op="-", val=IntegerLit(100)),
                                    ),
                                ),
                                right=BinExpr(
                                    op="/", left=IntegerLit(100), right=IntegerLit(100)
                                ),
                            ),
                            right=BinExpr(
                                op="%", left=IntegerLit(100), right=IntegerLit(100)
                            ),
                        ),
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 332), f"Correct: {expect}")

    def testcase333(self):
        prog = "a: integer = two() || three;"
        expect = str(
            Program(
                [
                    VarDecl(
                        name="a",
                        typ=IntegerType(),
                        init=BinExpr(
                            op="||", left=FuncCall("two", []), right=Id("three")
                        ),
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 324), f"Correct {expect}")

    def testcase334(self):
        prog = "a: auto = two() != three;"
        expect = str(
            Program(
                [
                    VarDecl(
                        "a",
                        AutoType(),
                        init=BinExpr("!=", FuncCall("two", []), Id("three")),
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 334), f"Correct {expect}")

    def testcase335(self):
        prog = """main: function void() {
callFunc(1, "String", foo());
}"""
        expect = str(
            Program(
                [
                    FuncDecl(
                        "main",
                        VoidType(),
                        [],
                        None,
                        BlockStmt(
                            [
                                CallStmt(
                                    "callFunc",
                                    [
                                        IntegerLit(1),
                                        StringLit("String"),
                                        FuncCall("foo", []),
                                    ],
                                )
                            ]
                        ),
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(prog, expect, 335), f"Correct {expect}")

    def testcase336(self):
        prog = """main: function void() {
    if (foo == barz)
        if (barz == bar)
            call();
        else
            dontCall();
    else
        callAPI();
}"""

        expect = str(
            Program(
                [
                    FuncDecl(
                        "main",
                        VoidType(),
                        [],
                        None,
                        BlockStmt(
                            [
                                IfStmt(
                                    BinExpr("==", Id("foo"), Id("barz")),
                                    IfStmt(
                                        BinExpr("==", Id("barz"), Id("bar")),
                                        CallStmt("call", []),
                                        CallStmt("dontCall", []),
                                    ),
                                    CallStmt("callAPI", []),
                                )
                            ]
                        ),
                    )
                ]
            )
        )

        self.assertTrue(TestAST.test(prog, expect, 336), f"Correct {expect}")
