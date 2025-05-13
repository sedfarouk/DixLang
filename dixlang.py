#############################
# IMPORTS
#############################

from src.storage.context import Context
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.storage.symbol_table import SymbolTable
from src.values.number import Number


#############################
# RUN
#############################


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0)) # By default, Null == 0 in DixLang
global_symbol_table.set("TRUE", Number(1))
global_symbol_table.set("FALSE", Number(0))


def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error