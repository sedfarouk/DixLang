from src.values.functions.base_function import BaseFunction
from ...validations.runtime_result import RuntimeResult

from src.constants.default_values import *


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return
        
    def execute(self, args):
        res = RuntimeResult()
        from ...main.interpreter import Interpreter # breaks circular dependency by deferring import until needed
        interpreter = Interpreter()
        
        new_context = self.gen_new_context()
        
        res.register(super().check_and_populate_args(self.arg_names, args, new_context))
            
        if res.should_return(): return res
            
        value = res.register(interpreter.visit(self.body_node, new_context)) 
        
        if res.should_return() and res.func_return_value == None: return res
        
        return_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null

        return res.success(return_value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"