from src.values.functions.base_function import BaseFunction
from ...validations.runtime_result import RuntimeResult


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        
    def execute(self, args):
        res = RuntimeResult()
        from ...main.interpreter import Interpreter # breaks circular dependency by deferring import until needed
        interpreter = Interpreter()
        
        new_context = self.gen_new_context()
        
        res.register(self.check_and_populate(self.arg_names, args, new_context))
            
        if res.error: return res
            
        value = res.register(interpreter.visit(self.body_node, new_context)) 
        if res.error: return res
        
        return res.success(value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"