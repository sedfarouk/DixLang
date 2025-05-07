class VariableAccessNode:
    def __init__(self, variable_name_tok):
        self.variable_name_tok = variable_name_tok

        self.pos_start = self.variable_name_tok.pos_start
        self.pos_end = self.variable_name_tok.pos_end

