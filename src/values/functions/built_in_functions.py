import os

from src.validations.runtime_result import RuntimeResult
from src.values.functions.base_function import BaseFunction
from src.values.list import List
from src.values.string import String

from ...constants.default_values import *


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
        
    def execute(self, args):
        res = RuntimeResult()
        exec_ctx = self.gen_new_context()
        
        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)
        
        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        
        if res.should_return(): return res
        
        return_value = res.register(method(exec_ctx))
        
        if res.should_return(): return res
        
        return res.success(return_value)
                
    
    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')
    
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        
        return copy
    
    def __repr__(self):
        return f"<built-in function {self.name}>"
    
    
    def execute_write(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        
        return RuntimeResult().success(Number.null)
    execute_write.arg_names = ['value']
    
    def execute_write_return(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        
        return RuntimeResult().success(String(exec_ctx.symbol_table.get('value')))
    execute_write_return.arg_names = ['value']
    
    def execute_input(self, exec_ctx):
        txt = input()
        
        return RuntimeResult().success(String(txt))
    execute_input.arg_names = []
    
    def execute_input_int(self, exec_ctx):        
        while True:
            txt = input()
            try:
                number = int(txt)
                break
            except ValueError:
                return RuntimeResult().failure(self.pos_start, self.pos_end, f"'{txt}' must be an integer. Try again!",
                        exec_ctx)
        
        return RuntimeResult().success(String(number))
        
    execute_input_int.arg_names = [] 
    
    def execute_clear(self, exec_ctx):
        # On Mac and Linux -> 'clear', on Windows -> 'cls'
        os.system('cls' if os.name == 'nt' else 'clear')
        
        return RuntimeResult().success(Number.null)
    execute_clear.arg_names = []
    
    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get('value'), Number)

        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ['value']
    
    def execute_is_string(self, exec_ctx):
        is_string = isinstance(exec_ctx.symbol_table.get('value'), String)

        return RuntimeResult().success(Number.true if is_string else Number.false)
    execute_is_number.arg_names = ['value']
    
    def execute_is_list(self, exec_ctx):
        is_list = isinstance(exec_ctx.symbol_table.get('value'), List)

        return RuntimeResult().success(Number.true if is_list else Number.false)
    execute_is_list.arg_names = ['value']
    
    def execute_is_function(self, exec_ctx):
        is_function = isinstance(exec_ctx.symbol_table.get('value'), BaseFunction)

        return RuntimeResult().success(Number.true if is_function else Number.false)
    execute_is_function.arg_names = ['value']
    
    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")
        
        if not isinstance(list_, List):
            return RuntimeResult().failure(RuntimeError(self.pos_start, self.pos_end, 
                "First argument must be list",
                exec_ctx))
            
        list_.elements.append(value)
        
        return RuntimeResult().success(Number.null)
        
    execute_append.arg_names = ['list', 'value']
    
    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")
        
        if not isinstance(list_, List):
            return RuntimeResult().failure(RuntimeError(self.pos_start, self.pos_end, 
                "First argument must be a list",
                exec_ctx))
            
        if not isinstance(index, Number):
            return RuntimeResult().failure(RuntimeError(self.pos_start, self.pos_end, 
                "Second argument must be a number",
                exec_ctx))
            
        try:
            element = list_.elements.pop(index.value)
        except:
            return RuntimeResult().failure(RuntimeError(self.pos_start, self.pos_end, 
                "Element at this index could not be removed from list because the index is out of range",
                exec_ctx))
        
        return RuntimeResult().success(element)        
    execute_pop.arg_names = ['list', 'index']
    
    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")
        
        if not isinstance(listA, List):
            return RuntimeResult().failure(RuntimeError(self.pos_start, self.pos_end, 
                "First argument must be a list",
                exec_ctx))
            
        if not isinstance(listB, List):
            return RuntimeResult().failure(RuntimeError(self.pos_start, self.pos_end, 
                "Second argument must be a list",
                exec_ctx))
            
        listA.elements.extend(listB.elements) 
        
        return RuntimeResult().success(Number.null)       
    execute_extend.arg_names = ['listA', 'listB']
   
# To refactor later to use Enums 
BuiltInFunction.write       = BuiltInFunction("write")
BuiltInFunction.write_ret   = BuiltInFunction("write_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")
    