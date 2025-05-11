class ForNode:
    def __init__(self, var_name_tok, start_val_node, end_val_node, step_val_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_val_node = start_val_node
        self.end_val_node = end_val_node
        self.step_val_node = step_val_node
        self.body_node = body_node
        
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end