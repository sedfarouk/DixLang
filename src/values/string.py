from src.values.number import Number
from .custom_value import CustomValue

class String(CustomValue):
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        if isinstance(other, Number):
            return String(self.value + str(other.value)).set_context(self.context), None
        return None, super().illegal_operation(other)
    
    def multed_by(self, other):
        if isinstance(other, String):
            return String(self.value * other.value).set_context(self.context), None
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        return None, super().illegal_operation(other)
        
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        
        return copy
    
    def __repr__(self):
        return f"{self.value}"
    