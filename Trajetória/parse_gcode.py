# parse_gcode.py

from antlr4 import *
from GCodeLexer import GCodeLexer
from GCodeParser import GCodeParser
from GCodeVisitor import GCodeVisitor

# -----------------------------------------------------------------------------
# Implementação do Visitor para extrair os dados do G-Code
# -----------------------------------------------------------------------------

class GCodeDataExtractor(GCodeVisitor):
    def __init__(self):
        self.commands = []

    # Visita a regra 'program'
    def visitProgram(self, ctx:GCodeParser.ProgramContext):
        # Chama o visit para cada 'statement' no programa
        self.visitChildren(ctx)
        return self.commands

    # Visita a regra 'statement'
    def visitStatement(self, ctx:GCodeParser.StatementContext):
        # A informação principal está no gcodeCommand
        # Garante que o número da linha é opcional, mas não é armazenado diretamente
        # apenas para manter o foco nos comandos de movimento
        return self.visit(ctx.gcodeCommand())

    # Visita a regra 'gcodeCommand'
    def visitGcodeCommand(self, ctx:GCodeParser.GcodeCommandContext):
        command_info = {}

        # Verifica qual tipo de comando G é
        if ctx.G00():
            command_info['type'] = 'G00'
        elif ctx.G01():
            command_info['type'] = 'G01'
        elif ctx.G02():
            command_info['type'] = 'G02'
        elif ctx.G03():
            command_info['type'] = 'G03'
        elif ctx.M30():
            command_info['type'] = 'M30'
            self.commands.append(command_info) # M30 é o fim, adiciona e retorna
            return command_info

        # Extrai os valores X, Y, I, J, R se existirem
        # O ANTLR ordena os tokens com base na ordem em que aparecem na regra.
        # Precisamos verificar cada um explicitamente.
        # ctx.X() retorna uma lista de contextos X.
        # ctx.VALUE() retorna uma lista de contextos VALUE.
        # Associamos pelo índice, mas é mais seguro verificar o tipo do token.

        # Pega todos os tokens de valor e seus tipos associados
        # Um pouco mais robusto do que iterar por ctx.VALUE() diretamente sem checagem de tipo
        for i, child in enumerate(ctx.children):
            if isinstance(child, TerminalNode):
                token_text = child.getText()
                if token_text == 'X' and i + 1 < len(ctx.children):
                    value_ctx = ctx.children[i+1]
                    if hasattr(value_ctx, 'getText'): # Verifica se é um nó de valor real
                        command_info['X'] = float(value_ctx.getText())
                elif token_text == 'Y' and i + 1 < len(ctx.children):
                    value_ctx = ctx.children[i+1]
                    if hasattr(value_ctx, 'getText'):
                        command_info['Y'] = float(value_ctx.getText())
                elif token_text == 'I' and i + 1 < len(ctx.children):
                    value_ctx = ctx.children[i+1]
                    if hasattr(value_ctx, 'getText'):
                        command_info['I'] = float(value_ctx.getText())
                elif token_text == 'J' and i + 1 < len(ctx.children):
                    value_ctx = ctx.children[i+1]
                    if hasattr(value_ctx, 'getText'):
                        command_info['J'] = float(value_ctx.getText())
                elif token_text == 'R' and i + 1 < len(ctx.children):
                    value_ctx = ctx.children[i+1]
                    if hasattr(value_ctx, 'getText'):
                        command_info['R'] = float(value_ctx.getText())

        self.commands.append(command_info)
        return command_info

# -----------------------------------------------------------------------------
# Função principal para parsear um arquivo G-Code
# -----------------------------------------------------------------------------

def parse_gcode_file(file_path):
    """
    Parseia um arquivo G-Code e extrai os comandos em uma lista de dicionários.
    """
    try:
        # Cria um stream de entrada a partir do arquivo
        input_stream = FileStream(file_path)

        # Cria um lexer (analisador léxico) a partir do stream de entrada
        lexer = GCodeLexer(input_stream)
        # Cria um stream de tokens a partir do lexer
        token_stream = CommonTokenStream(lexer)
        # Cria um parser (analisador sintático) a partir do stream de tokens
        parser = GCodeParser(token_stream)

        # Opcional: Adicionar listener para erros de sintaxe (para melhor feedback)
        # class GCodeErrorListener(ErrorListener):
        #     def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        #         print(f"Erro de sintaxe na linha {line}, coluna {column}: {msg}")
        # parser.removeErrorListeners() # Remove o default
        # parser.addErrorListener(GCodeErrorListener())

        # Inicia o processo de parsing a partir da regra 'program'
        tree = parser.program()

        # Cria uma instância do nosso visitor customizado
        extractor = GCodeDataExtractor()
        # Visita a árvore de análise sintática para extrair os dados
        extracted_data = extractor.visit(tree)

        return extracted_data

    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro durante o parsing: {e}")
        return None

# -----------------------------------------------------------------------------
# Exemplo de uso (apenas para testar este arquivo isoladamente)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Este bloco é para testar parse_gcode.py isoladamente.
    # No uso normal com trajectory_generator.py, este bloco não é executado.
    sample_gcode_content = """
G21
G90
G00 X0 Y400 F2000
G00 X190 Y200 F2000
G02 X190 Y200 I-40 J0 F1600
G00 X150 Y100 F2000
G01 F1100
G01 X120 Y50
G01 X180 Y50
G01 X150 Y100
M30
"""
    with open("temp_example.gcode", "w") as f:
        f.write(sample_gcode_content.strip())

    print("--- Testando parse_gcode.py diretamente ---")
    parsed = parse_gcode_file("temp_example.gcode")
    if parsed:
        for cmd in parsed:
            print(cmd)
    import os
    os.remove("temp_example.gcode") # Limpa o arquivo temporário