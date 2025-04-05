

class Parser():
    def __init__(self, parse_table, word):

        self.parse_table = parse_table
        self.word = word


class LL1Parser(Parser):
    
    def __init__(self, parse_table, word):
        super().__init__(parse_table, word)

        print(parse_table['A'])