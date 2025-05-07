#############################
# IMPORTS
#############################


from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

#############################
# RUN
#############################

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
    result = interpreter.visit(ast.node)

    return result.value, result.error