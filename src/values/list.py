from .number import Number
from .custom_value import CustomValue
from ..validations.errors import RuntimeErrorX

class List(CustomValue):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
        
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        
        return new_list, None
    
    def multed_by(self, other):
        if isinstance(other, List):
            new_list= self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        
        return None, CustomValue.illegal_operation(self, other)
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RuntimeErrorX(other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is invalid',
                    self.context)
                
        else:
            return None, CustomValue.illegal_operation(self, other)
        
    def dived_by (self, other):
        if isinstance(other, Number):            
            try:
                return self.elements[other.value], None
            except:
                return None, RuntimeErrorX(other.pos_start, other.pos_end,
                    'Element at this index could not be accessed from list because index is invalid',
                    self.context)
                
        else:
            return None, CustomValue.illegal_operation(self, other)
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        
        return copy
    
    def __str__(self):
        return f"{", ".join([str(x) for x in self.elements])}"
    
    def __repr__(self):
        return f"[{", ".join([str(x) for x in self.elements])}]"