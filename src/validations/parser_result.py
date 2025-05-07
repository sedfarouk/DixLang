#############################
# PARSER RESULT
#############################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self 