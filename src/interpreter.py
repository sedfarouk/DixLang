#############################
# INTERPRETER
#############################

from .token_types import *
from .number import Number

class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)

        return method(node)
    
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        # print('Found number node')
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinOpNode(self, node):
        # print('Found binary operator node')
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == TT_PLUS:
            result = left.added_to(right)

        elif node.op_tok.type == TT_MINUS:
            result = left.subbed_by(right)

        elif node.op_tok.type == TT_MUL:
            result = left.multed_by(right)

        elif node.op_tok.type == TT_DIV:
            result = left.dived_by(right)

        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOpNode(self, node):
        # print('Found unary operator node')
        number = self.visit(node.node)

        if node.op_tok.type == TT_MINUS:
            number = number.multed_by(Number(-1))
        
        return number
