#############################
# NODES
#############################

from ..validations.errors import InvalidSyntaxError
from ..validations.parser_result import *

from ..constants.token_types import *

from ..nodes.break_node import BreakNode
from ..nodes.continue_node import ContinueNode
from ..nodes.return_node import ReturnNode
from ..nodes.list_node import ListNode
from ..nodes.while_node import WhileNode
from ..nodes.if_node import IfNode
from ..nodes.for_node import ForNode
from ..nodes.number_node import NumberNode
from ..nodes.binary_operation_node import BinOpNode
from ..nodes.unary_operation_node import UnaryOpNode
from ..nodes.variable_access_node import VariableAccessNode
from ..nodes.variable_assignment_node import VariableAssignmentNode
from ..nodes.func_def_node import FuncDefNode
from ..nodes.call_node import CallNode
from ..nodes.string_node import StringNode
    
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

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
    
    def parse(self):
        res = ParseResult()
        
        statements = res.register(self.statements())
        
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "'Expected '+', '-', '*', '^' or '/'"))
        return res.success(statements)
    
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()
        
        while self.current_tok.type == TT_NEWLINE:
            res.register_with_advancement()
            self.advance()
            
        statement = res.register(self.statement())    
        if res.error: return res
        statements.append(statement)

        more_statements = True
        while True:
            newline_cnt = 0

            while self.current_tok.type == TT_NEWLINE:
                res.register_with_advancement()
                self.advance()
                newline_cnt += 1

            if newline_cnt == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.statement())

            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue

            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))
    
    
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
    
        if self.current_tok.matches(TT_KEYWORD, 'RET'):
            res.register_with_advancement()
            self.advance()
            
            expr = res.try_register(self.expr())
            
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))           
    
        if self.current_tok.matches(TT_KEYWORD, 'CONT'):
            res.register_with_advancement()
            self.advance()
            
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))
        
        if self.current_tok.matches(TT_KEYWORD, 'BR'):
            res.register_with_advancement()
            self.advance()
            
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))
            
        expr = res.register(self.expr())
        
        if res.error: 
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'RET', 'CONT', 'BR', '[', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier or '('"
        ))
        
        return res.success(expr)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_with_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        if tok.type in (TT_STRING):
            res.register_with_advancement()
            self.advance()
            return res.success(StringNode(tok))
        
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
        
        elif tok.type == TT_LSQB:
           list_expr = res.register(self.list_expr())
           
           if res.error: return res
           
           return res.success(list_expr)
        
        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            
            if res.error: return res
            return res.success(if_expr)
        
        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            
            if res.error: return res
            return res.success(for_expr)
        
        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            
            if res.error: return res
            return res.success(while_expr)
        
        elif tok.matches(TT_KEYWORD, 'FN'):
            func_def = res.register(self.func_def())
            
            if res.error: return res
            return res.success(func_def)
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, identifier, '+', '-', '[', 'IF', 'FOR', 'WHILE', 'FN' or '("))


    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()
        
        if self.current_tok.type != TT_LSQB:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '['"))
        
        res.register_with_advancement()
        self.advance()
        
        if self.current_tok.type == TT_RSQB:
            res.register_with_advancement()
            self.advance()
            
        else:
            element_nodes.append(res.register(self.expr()))
                
            if res.error:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '[', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier or '('"))

            while self.current_tok.type == TT_COMMA:
                res.register_with_advancement()
                self.advance()
                
                element_nodes.append(res.register(self.expr()))
                
                if res.error: return res
            
            if self.current_tok.type != TT_RSQB:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ']'")) 
                
            res.register_with_advancement()
            self.advance()
            
        return res.success(ListNode(element_nodes, pos_start, 
                self.current_tok.pos_end.copy()))


    def func_def(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD, 'FN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'FN'"))
            
        res.register_with_advancement()
        self.advance()


        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            
            res.register_with_advancement()
            self.advance()
            
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"))

        else:
            var_name_tok = None
            
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"))
                
        res.register_with_advancement()
        self.advance()
        
        arg_name_toks = []
        
        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            
            res.register_with_advancement()
            self.advance()
            
            while self.current_tok.type == TT_COMMA:
                res.register_with_advancement()
                self.advance()
                
                if self.current_tok.type != TT_IDENTIFIER:
                       return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier"))  
                       
                arg_name_toks.append(self.current_tok) 
                res.register_with_advancement()
                self.advance() 
                
               
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"))
                
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"))
                
        res.register_with_advancement()
        self.advance()
        
        if self.current_tok.type == TT_ARROW:       
            res.register_with_advancement()
            self.advance()
            
            node_to_return = res.register(self.expr())
            
            if res.error: return res
            
            return res.success(FuncDefNode(var_name_tok, arg_name_toks, node_to_return, True))     
    
        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->' or NEWLINE"))

        res.register_with_advancement()
        self.advance()

        body = res.register(self.statements())

        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"))

        res.register_with_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok, arg_name_toks, body, False
        ))


    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('IF'))
        
        if res.error: return res
        cases, else_case = all_cases
        
        return res.success(IfNode(cases, else_case))
                
                
    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None
        
        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '{case_keyword}'"))
            
        res.register_with_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        
        if res.error: return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"))
            
        res.register_with_advancement()
        self.advance()
        
        if self.current_tok.type == TT_NEWLINE:
            res.register_with_advancement()
            self.advance()
            
            statements = res.register(self.statements())
            
            if res.error: return res
            
            cases.append((condition, statements, True))
            
            if self.current_tok.matches(TT_KEYWORD, 'END'):
                res.register_with_advancement()
                self.advance()
                  
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                
                if res.error: return res
                
                new_cases, else_case = all_cases
                cases.extend(new_cases)
                
        else:
            expr = res.register(self.statement())
            
            if res.error: return res
            
            cases.append((condition, expr, False))
            
            all_cases = res.register(self.if_expr_b_or_c())
            
            if res.error: return res
            
            new_cases, else_case = all_cases
            
            cases.extend(new_cases)

        return res.success((cases, else_case))


    def if_expr_b(self):
        return self.if_expr_cases('EIF')

    
    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_with_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_with_advancement()
                self.advance()

                statements = res.register(self.statements())

                if res.error: return res

                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, 'END'):
                    res.register_with_advancement()
                    self.advance()

                else:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'END'"))

            else:
                expr = res.register(self.statement())
                
                if res.error: return res

                else_case = (expr, False)

        return res.success(else_case)

    
    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'EIF'):
            all_cases = res.register(self.if_expr_b())

            if res.error: return res

            cases, else_case = all_cases
        
        else:
            else_case = res.register(self.if_expr_c())

            if res.error: return res

        return res.success((cases, else_case))


    def power(self):
        return self.bin_op(self.call, (TT_POW, ), self.factor)


    def call(self):
        res = ParseResult()
        
        atom = res.register(self.atom())
        
        if res.error: return res
        
        if self.current_tok.type == TT_LPAREN:
            res.register_with_advancement()
            self.advance()
            
            arg_nodes = []
            
            if self.current_tok.type == TT_RPAREN:
                res.register_with_advancement()
                self.advance()            

            else:
                arg_nodes.append(res.register(self.expr()))
                
                if res.error:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, '[', identifier or '('"))

                while self.current_tok.type == TT_COMMA:
                    res.register_with_advancement()
                    self.advance()
                    
                    arg_nodes.append(res.register(self.expr()))
                    
                    if res.error: return res
                
                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'")) 
                    
                res.register_with_advancement()
                self.advance()
            
            return res.success(CallNode(atom, arg_nodes)) 
        return res.success(atom)           
                       
                

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
    
    def for_expr(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'FOR'"))
            
        res.register_with_advancement()
        self.advance()
        
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier"))
            
        var_name = self.current_tok
        res.register_with_advancement()
        self.advance()
        
        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '='"))   
            
        res.register_with_advancement()
        self.advance()
        
        start_val = res.register(self.expr())
        
        if res.error: return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'TO'")) 
            
        res.register_with_advancement()
        self.advance()
        
        end_value = res.register(self.expr())
        
        if res.error: return res
        
        step_value = None
        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            res.register_with_advancement()
            self.advance()
            
            step_value = res.register(self.expr())
            
            if res.error: return res
            
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'THEN'"))
            
        res.register_with_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_with_advancement()
            self.advance()

            body = res.register(self.statements())

            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected 'END'"))

            res.register_with_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_val, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error: return res
        
        return res.success(ForNode(var_name, start_val, end_value, step_value, body, False))
    
    
    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'WHILE'"))
            
        res.register_with_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        
        if res.error: return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"))
            
        res.register_with_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_with_advancement()
            self.advance()

            body = res.register(self.statements())

            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected 'END'"))

            res.register_with_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))
        
        body = res.register(self.statement())
        
        if res.error: return res
        
        return res.success(WhileNode(condition, body, False))
    
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
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, identifier, '+', '-', '[', 'NOT' or '("))

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

        if res.error: return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, VAR, identifier, '+', '-', '[', 'IF', 'FOR', 'WHILE', 'FN' or '("))
        
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
