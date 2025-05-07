#############################
# INTERPRETER
#############################

class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)

        return method(node)
    
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        print('Found number node')

    def visit_BinOpNode(self, node):
        print('Found binary operator node')
        self.visit(node.left_node)
        self.visit(node.right_node)

    def visit_UnaryOpNode(self, node):
        print('Found unary operator node')
        self.visit(node.node)
