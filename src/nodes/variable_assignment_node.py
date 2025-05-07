class VariableAssignmentNode:
    def __init__(self, variable_name_tok, value_node):
        self.variable_name_tok = variable_name_tok
        self.value_node = value_node

        self.pos_start = self.variable_name_tok.pos_start
        self.pos_end = self.variable_name_tok.pos_end