#############################
# NODES
#############################

from .validations.errors import InvalidSyntaxError
from .validations.parser_result import *
from .token_types import *
from .nodes.if_node import *
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
            res.register_with_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register_with_advancement()
            self.advance()
            return res.success(VariableAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_with_advancement()
            self.advance()
            expr = res.register(self.expr())

            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_with_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        
        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            
            if res.error: return res
            return res.success(if_expr)
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, identifier, '+', '-' or '("))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        
        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'IF'"))
            
        res.register_with_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        
        if res.error: return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"))
            
        res.register_with_advancement()
        self.advance()
        
        expr = res.register(self.expr())
        
        if res.error: return res
        
        cases.append((condition, expr))
        
        while self.current_tok.matches(TT_KEYWORD, 'EIF'):
            res.register_with_advancement()
            self.advance()
            
            condition = res.register(self.expr())
            
            if res.error: return res
            
            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected 'THEN'"))
                
            res.register_with_advancement()
            self.advance()
            
            expr = res.register(self.expr())
            
            if not res.error: return res
            
            cases.append((condition, expr))
            
        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_with_advancement()
            self.advance()
            
            else_case = res.register(self.expr())
            
            if res.error: return res
            
        return res.success(IfNode(cases, else_case))

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_with_advancement()
            self.advance()
            factor = res.register(self.factor())

            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_with_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, identifier, '+', '-', 'NOT' or '(")

        return res.success(node)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_with_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected an identifier"))

            variable_name = self.current_tok
            res.register_with_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))

            res.register_with_advancement()
            self.advance()
            expr = res.register(self.expr())

            if res.error: return res
            return res.success(VariableAssignmentNode(variable_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "AND"), (TT_KEYWORD, "OR"))))

        if res.error: return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, VAR, identifier, '+', '-' or '("))
        
        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a()) 
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_with_advancement()
            self.advance()
            right = res.register(func_b())

            if res.error: 
                return res

            left = BinOpNode(left, op_tok, right)

        return res.success(left)
