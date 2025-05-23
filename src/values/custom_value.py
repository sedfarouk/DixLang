from ..validations.runtime_result import RuntimeResult
from ..validations.errors import *

class CustomValue:
    def __init__(self):
        self.set_pos()
        self.set_context()
        
    def set_context(self, context=None):
        self.context = context
        return self

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def added_to(self, other):
        return None, self.illegal_operation(other)
        
    def subbed_by(self, other):
        return None, self.illegal_operation(other)
        
    def multed_by(self, other):
        return None, self.illegal_operation(other)
        
    def dived_by(self, other):
        return None, self.illegal_operation(other)
        
    def exp_by(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def copy(self):
        raise Exception('No copy method defined')
    
    def is_true(self):
        return False
    
    def execute(self, args):
        return RuntimeResult().failure(self.illegal_operation())      
    
    def illegal_operation(self, other=None):
        if not other: other = self
        
        return RuntimeErrorX(self.pos_start, other.pos_end,
                'Illegal operation', self.context)