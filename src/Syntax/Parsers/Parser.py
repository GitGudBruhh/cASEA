from Grammars.CFG import CFG

from Syntax.ParseTree import ParseTree, ParseTreeNode

class Parser():
    def __init__(self, parse_table, grammar : CFG):

        self.parse_table = parse_table
        self.grammar = grammar

    def parse(self, word):
        pass


class LL1Parser(Parser):
    
    def __init__(self, parse_table, grammar : CFG):
        super().__init__(parse_table, grammar)

        self.stack = ['$']
    
    def parse(self, word):
        
        cur_node = ParseTreeNode(self.grammar.S, None, None, None)
        parse_tree = ParseTree(cur_node)

        # Add $ to the end of the word 
        word += '$'

        self.stack.append(self.grammar.S)
        look_ahead = 0

        # print(self.parse_table)

        while (len(self.stack) != 0 and (len(self.stack) < 10)):
            
            # print(self.stack, word[look_ahead])
            # if cur_node.parent:
                # print(f"{cur_node}\t{cur_node.parent}\t{cur_node.parent.children}")
            
            cur_sym = self.stack.pop()  

            if cur_sym == "#":
                cur_node = cur_node.get_next_node_to_parse()
                continue

            if word[look_ahead] == cur_sym:
                if cur_sym == '$':
                    # If both look_ahead and cur_sym is $ we can accept and return the parse tree
                    print("Accepted")
                    return parse_tree
                else:
                    look_ahead += 1
                    cur_node = cur_node.get_next_node_to_parse()
                    continue
            
            rhs_set = self.parse_table[cur_sym][word[look_ahead]]

            if len(rhs_set) != 1:
                print(f"ERROR: Invalid Grammar!\nFound rules for {cur_sym} & {word[look_ahead]} -> {rhs_set}")
                return None

            rhs = list(rhs_set)[0]

            for symbol in rhs[::-1]:

                new_node = ParseTreeNode(symbol, None, None, None)
                new_node.parent = cur_node
                cur_node.children.insert(0, new_node)
    
                self.stack.append(symbol)
            
            cur_node._cur_child = 0
            cur_node = cur_node.get_next_node_to_parse()