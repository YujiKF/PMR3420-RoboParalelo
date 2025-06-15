# Generated from GCode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GCodeParser import GCodeParser
else:
    from GCodeParser import GCodeParser

# This class defines a complete listener for a parse tree produced by GCodeParser.
class GCodeListener(ParseTreeListener):

    # Enter a parse tree produced by GCodeParser#program.
    def enterProgram(self, ctx:GCodeParser.ProgramContext):
        pass

    # Exit a parse tree produced by GCodeParser#program.
    def exitProgram(self, ctx:GCodeParser.ProgramContext):
        pass


    # Enter a parse tree produced by GCodeParser#statement.
    def enterStatement(self, ctx:GCodeParser.StatementContext):
        pass

    # Exit a parse tree produced by GCodeParser#statement.
    def exitStatement(self, ctx:GCodeParser.StatementContext):
        pass


    # Enter a parse tree produced by GCodeParser#gcodeCommand.
    def enterGcodeCommand(self, ctx:GCodeParser.GcodeCommandContext):
        pass

    # Exit a parse tree produced by GCodeParser#gcodeCommand.
    def exitGcodeCommand(self, ctx:GCodeParser.GcodeCommandContext):
        pass


    # Enter a parse tree produced by GCodeParser#programEnd.
    def enterProgramEnd(self, ctx:GCodeParser.ProgramEndContext):
        pass

    # Exit a parse tree produced by GCodeParser#programEnd.
    def exitProgramEnd(self, ctx:GCodeParser.ProgramEndContext):
        pass



del GCodeParser