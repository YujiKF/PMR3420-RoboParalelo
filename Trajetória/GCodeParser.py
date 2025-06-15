# Generated from GCode.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,16,84,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,0,5,0,12,8,0,
        10,0,12,0,15,9,0,1,0,1,0,1,0,1,1,3,1,21,8,1,1,1,1,1,1,2,1,2,1,2,
        3,2,28,8,2,1,2,1,2,3,2,32,8,2,1,2,1,2,1,2,3,2,37,8,2,1,2,1,2,3,2,
        41,8,2,1,2,1,2,1,2,3,2,46,8,2,1,2,1,2,3,2,50,8,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,3,2,59,8,2,1,2,1,2,1,2,3,2,64,8,2,1,2,1,2,3,2,68,8,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,77,8,2,1,2,3,2,80,8,2,1,3,1,3,1,
        3,0,0,4,0,2,4,6,0,0,97,0,13,1,0,0,0,2,20,1,0,0,0,4,79,1,0,0,0,6,
        81,1,0,0,0,8,9,3,2,1,0,9,10,5,15,0,0,10,12,1,0,0,0,11,8,1,0,0,0,
        12,15,1,0,0,0,13,11,1,0,0,0,13,14,1,0,0,0,14,16,1,0,0,0,15,13,1,
        0,0,0,16,17,3,6,3,0,17,18,5,0,0,1,18,1,1,0,0,0,19,21,5,11,0,0,20,
        19,1,0,0,0,20,21,1,0,0,0,21,22,1,0,0,0,22,23,3,4,2,0,23,3,1,0,0,
        0,24,27,5,1,0,0,25,26,5,6,0,0,26,28,5,12,0,0,27,25,1,0,0,0,27,28,
        1,0,0,0,28,31,1,0,0,0,29,30,5,7,0,0,30,32,5,12,0,0,31,29,1,0,0,0,
        31,32,1,0,0,0,32,80,1,0,0,0,33,36,5,2,0,0,34,35,5,6,0,0,35,37,5,
        12,0,0,36,34,1,0,0,0,36,37,1,0,0,0,37,40,1,0,0,0,38,39,5,7,0,0,39,
        41,5,12,0,0,40,38,1,0,0,0,40,41,1,0,0,0,41,80,1,0,0,0,42,45,5,3,
        0,0,43,44,5,6,0,0,44,46,5,12,0,0,45,43,1,0,0,0,45,46,1,0,0,0,46,
        49,1,0,0,0,47,48,5,7,0,0,48,50,5,12,0,0,49,47,1,0,0,0,49,50,1,0,
        0,0,50,58,1,0,0,0,51,52,5,8,0,0,52,53,5,12,0,0,53,54,1,0,0,0,54,
        55,5,9,0,0,55,59,5,12,0,0,56,57,5,10,0,0,57,59,5,12,0,0,58,51,1,
        0,0,0,58,56,1,0,0,0,58,59,1,0,0,0,59,80,1,0,0,0,60,63,5,4,0,0,61,
        62,5,6,0,0,62,64,5,12,0,0,63,61,1,0,0,0,63,64,1,0,0,0,64,67,1,0,
        0,0,65,66,5,7,0,0,66,68,5,12,0,0,67,65,1,0,0,0,67,68,1,0,0,0,68,
        76,1,0,0,0,69,70,5,8,0,0,70,71,5,12,0,0,71,72,1,0,0,0,72,73,5,9,
        0,0,73,77,5,12,0,0,74,75,5,10,0,0,75,77,5,12,0,0,76,69,1,0,0,0,76,
        74,1,0,0,0,76,77,1,0,0,0,77,80,1,0,0,0,78,80,5,5,0,0,79,24,1,0,0,
        0,79,33,1,0,0,0,79,42,1,0,0,0,79,60,1,0,0,0,79,78,1,0,0,0,80,5,1,
        0,0,0,81,82,5,5,0,0,82,7,1,0,0,0,13,13,20,27,31,36,40,45,49,58,63,
        67,76,79
    ]

class GCodeParser ( Parser ):

    grammarFileName = "GCode.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'G00'", "'G01'", "'G02'", "'G03'", "'M30'", 
                     "'X'", "'Y'", "'I'", "'J'", "'R'" ]

    symbolicNames = [ "<INVALID>", "G00", "G01", "G02", "G03", "M30", "X", 
                      "Y", "I", "J", "R", "LINE_NUMBER", "VALUE", "SIGN", 
                      "DIGITS", "EOL", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_gcodeCommand = 2
    RULE_programEnd = 3

    ruleNames =  [ "program", "statement", "gcodeCommand", "programEnd" ]

    EOF = Token.EOF
    G00=1
    G01=2
    G02=3
    G03=4
    M30=5
    X=6
    Y=7
    I=8
    J=9
    R=10
    LINE_NUMBER=11
    VALUE=12
    SIGN=13
    DIGITS=14
    EOL=15
    WS=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def programEnd(self):
            return self.getTypedRuleContext(GCodeParser.ProgramEndContext,0)


        def EOF(self):
            return self.getToken(GCodeParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.StatementContext)
            else:
                return self.getTypedRuleContext(GCodeParser.StatementContext,i)


        def EOL(self, i:int=None):
            if i is None:
                return self.getTokens(GCodeParser.EOL)
            else:
                return self.getToken(GCodeParser.EOL, i)

        def getRuleIndex(self):
            return GCodeParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = GCodeParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 8
                    self.statement()
                    self.state = 9
                    self.match(GCodeParser.EOL) 
                self.state = 15
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 16
            self.programEnd()
            self.state = 17
            self.match(GCodeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def gcodeCommand(self):
            return self.getTypedRuleContext(GCodeParser.GcodeCommandContext,0)


        def LINE_NUMBER(self):
            return self.getToken(GCodeParser.LINE_NUMBER, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = GCodeParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 19
                self.match(GCodeParser.LINE_NUMBER)


            self.state = 22
            self.gcodeCommand()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GcodeCommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def G00(self):
            return self.getToken(GCodeParser.G00, 0)

        def X(self):
            return self.getToken(GCodeParser.X, 0)

        def VALUE(self, i:int=None):
            if i is None:
                return self.getTokens(GCodeParser.VALUE)
            else:
                return self.getToken(GCodeParser.VALUE, i)

        def Y(self):
            return self.getToken(GCodeParser.Y, 0)

        def G01(self):
            return self.getToken(GCodeParser.G01, 0)

        def G02(self):
            return self.getToken(GCodeParser.G02, 0)

        def I(self):
            return self.getToken(GCodeParser.I, 0)

        def J(self):
            return self.getToken(GCodeParser.J, 0)

        def R(self):
            return self.getToken(GCodeParser.R, 0)

        def G03(self):
            return self.getToken(GCodeParser.G03, 0)

        def M30(self):
            return self.getToken(GCodeParser.M30, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_gcodeCommand

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGcodeCommand" ):
                listener.enterGcodeCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGcodeCommand" ):
                listener.exitGcodeCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGcodeCommand" ):
                return visitor.visitGcodeCommand(self)
            else:
                return visitor.visitChildren(self)




    def gcodeCommand(self):

        localctx = GCodeParser.GcodeCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_gcodeCommand)
        self._la = 0 # Token type
        try:
            self.state = 79
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 24
                self.match(GCodeParser.G00)
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 25
                    self.match(GCodeParser.X)
                    self.state = 26
                    self.match(GCodeParser.VALUE)


                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 29
                    self.match(GCodeParser.Y)
                    self.state = 30
                    self.match(GCodeParser.VALUE)


                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 33
                self.match(GCodeParser.G01)
                self.state = 36
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 34
                    self.match(GCodeParser.X)
                    self.state = 35
                    self.match(GCodeParser.VALUE)


                self.state = 40
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 38
                    self.match(GCodeParser.Y)
                    self.state = 39
                    self.match(GCodeParser.VALUE)


                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 42
                self.match(GCodeParser.G02)
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 43
                    self.match(GCodeParser.X)
                    self.state = 44
                    self.match(GCodeParser.VALUE)


                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 47
                    self.match(GCodeParser.Y)
                    self.state = 48
                    self.match(GCodeParser.VALUE)


                self.state = 58
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [8]:
                    self.state = 51
                    self.match(GCodeParser.I)
                    self.state = 52
                    self.match(GCodeParser.VALUE)

                    self.state = 54
                    self.match(GCodeParser.J)
                    self.state = 55
                    self.match(GCodeParser.VALUE)
                    pass
                elif token in [10]:
                    self.state = 56
                    self.match(GCodeParser.R)
                    self.state = 57
                    self.match(GCodeParser.VALUE)
                    pass
                elif token in [15]:
                    pass
                else:
                    pass
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 60
                self.match(GCodeParser.G03)
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 61
                    self.match(GCodeParser.X)
                    self.state = 62
                    self.match(GCodeParser.VALUE)


                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 65
                    self.match(GCodeParser.Y)
                    self.state = 66
                    self.match(GCodeParser.VALUE)


                self.state = 76
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [8]:
                    self.state = 69
                    self.match(GCodeParser.I)
                    self.state = 70
                    self.match(GCodeParser.VALUE)

                    self.state = 72
                    self.match(GCodeParser.J)
                    self.state = 73
                    self.match(GCodeParser.VALUE)
                    pass
                elif token in [10]:
                    self.state = 74
                    self.match(GCodeParser.R)
                    self.state = 75
                    self.match(GCodeParser.VALUE)
                    pass
                elif token in [15]:
                    pass
                else:
                    pass
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 5)
                self.state = 78
                self.match(GCodeParser.M30)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramEndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def M30(self):
            return self.getToken(GCodeParser.M30, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_programEnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgramEnd" ):
                listener.enterProgramEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgramEnd" ):
                listener.exitProgramEnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgramEnd" ):
                return visitor.visitProgramEnd(self)
            else:
                return visitor.visitChildren(self)




    def programEnd(self):

        localctx = GCodeParser.ProgramEndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_programEnd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(GCodeParser.M30)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





