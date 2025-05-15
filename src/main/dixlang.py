#############################
# IMPORTS
#############################

from src.context import Context
from src.main.lexer import Lexer
from src.main.parser import Parser
from src.main.interpreter import Interpreter
from src.symbol_table import SymbolTable
from src.values.number import Number
from src.constants.default_values import *
from src.values.functions.built_in_functions import BuiltInFunction

#############################
# RUN
#############################


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null) # By default, Null == 0 in DixLang
global_symbol_table.set("TRUE", Number.false)
global_symbol_table.set("FALSE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)
global_symbol_table.set("WRITE", BuiltInFunction.write)
global_symbol_table.set("WRITE_RET", BuiltInFunction.write_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("CLS", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FN", BuiltInFunction.is_function)
global_symbol_table.set("APPEND", BuiltInFunction.append)
global_symbol_table.set("POP", BuiltInFunction.pop)
global_symbol_table.set("EXTEND", BuiltInFunction.extend)
global_symbol_table.set("LENGTH", BuiltInFunction.length)
global_symbol_table.set("RUN", BuiltInFunction.run)


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