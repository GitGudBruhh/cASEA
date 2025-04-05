class ParseTreeNode:

    def __init__(self, symbol, value, rule, action):

        self.symbol = symbol
        self.value = value
        self.rule = rule
        self.action = action

        self.children = []
        self.parent : ParseTreeNode = None

        self._cur_child : int = -1

    def get_next_node_to_parse(self):

        #TODO: Move handling of _cur_child calculations to this class itself
        if self._cur_child > -1 and self._cur_child < len(self.children):
            next_child = self.children[self._cur_child]
            self._cur_child += 1
            return next_child
        else:
            if self.parent:
                return self.parent.get_next_node_to_parse()
            else:
                # If root node return None
                return None

    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return self.symbol

class ParseTree:    
    def __init__(self, root):
        self.root = root

    def printTree(self):

        def printTreeHelper(node, prefix, is_last):
            # Print the current node's symbol
            print(prefix + ("└── " if is_last else "├── ") + node.symbol)
            prefix += "    " if is_last else "│   "

            # Recursively print each child
            for i, child in enumerate(node.children):
                printTreeHelper(child, prefix, i == len(node.children) - 1)

        printTreeHelper(self.root, "", True)
