#############################
# INTERPRETER
#############################

from .validations.runtime_result import RuntimeResult
from .validations.errors import *
from .token_types import *
from .number import Number

class Interpreter:
    def __init__(self):
        pass

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)

        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node, context):
        # print('Found number node')
        res = RuntimeResult()

        return res.success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end).set_pos(node.pos_start, node.pos_end))

    def visit_VariableAccessNode(self, node, context):
        res = RuntimeResult()

        variable_name = node.variable_name_tok.value
        value = context.symbol_table.get(variable_name)

        if not value:
            return res.failure(RuntimeErrorX(node.pos_start, node.pos_end, f"'{variable_name}' is not defined", context))

        return res.success(value)

    def visit_VariableAssignmentNode(self, node, context):
        res = RuntimeResult()

        variable_name = node.variable_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.error: return res

        context.symbol_table.set(variable_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        # print('Found binary operator node')
        res = RuntimeResult()

        left = res.register(self.visit(node.left_node, context))
        if res.error: return res

        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)

        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)

        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)

        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)

        elif node.op_tok.type == TT_POW:
            result, error = left.exp_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        # print('Found unary operator node')
        res = RuntimeResult()

        number = res.register(self.visit(node.node, context))

        if res.error: return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
