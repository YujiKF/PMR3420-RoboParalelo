# Generated from GCode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GCodeParser import GCodeParser
else:
    from GCodeParser import GCodeParser

# This class defines a complete generic visitor for a parse tree produced by GCodeParser.

class GCodeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GCodeParser#program.
    def visitProgram(self, ctx:GCodeParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GCodeParser#statement.
    def visitStatement(self, ctx:GCodeParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GCodeParser#gcodeCommand.
    def visitGcodeCommand(self, ctx:GCodeParser.GcodeCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GCodeParser#programEnd.
    def visitProgramEnd(self, ctx:GCodeParser.ProgramEndContext):
        return self.visitChildren(ctx)



del GCodeParser