#############################
# NODES
#############################

from .validations.errors import InvalidSyntaxError
from .validations.parser_result import *
from .token_types import *
from .nodes.number_node import *
from .nodes.binary_operation_node import *
from .nodes.unary_operation_node import *
from .nodes.variable_access_node import *
from .nodes.variable_assignment_node import *
    
#############################
# PARSER
#############################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

        return self.current_tok
    
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "'Expected '+', '-', '*', '^' or '/'"))
        return res
    
    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            return res.success(VariableAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())

            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, '+', '-' or '("))

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())

            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register(self.advance())

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected an identifier"))

            variable_name = self.current_tok
            res.register(self.advance())

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))

            res.register(self.advance())
            expr = res.register(self.expr())

            if res.error: return res
            return res.success(VariableAssignmentNode(variable_name, expr))

        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a()) 
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func_b())

            if res.error: 
                return res

            left = BinOpNode(left, op_tok, right)

        return res.success(left)
