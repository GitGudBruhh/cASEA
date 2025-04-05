class ParseTreeNode:

    def __init__(self, symbol, value, rule, action):

        self.symbol = symbol
        self.value = value
        self.rule = rule
        self.action = action

        self.children = ()
        self.parent = None

class ParseTree:
    pass