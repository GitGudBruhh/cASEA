class TOYRISCGenerator:
    def __init__(self, dfa, initstate, acceptstate, word):
        self.dfa = dfa
        self.initstate = initstate
        self.acceptstate = acceptstate
        self.word = word
        self.table = []
        self.wordlen = len(word)

    def create_table(self):
        states = sorted(self.dfa.keys())
        input_symbols = sorted(next(iter(self.dfa.values())).keys())
        self.ncols = len(input_symbols)
        self.nrows = len(states)
    
        for state in states:
            for symbol in input_symbols:
                self.table.append(self.dfa[state].get(symbol, None))

        return self.table

    def generate_TOYRISC(self):
        self.code = [
            ".data",
            f"initstate: \n    {self.initstate}",
            f"acceptstate:\n    {self.acceptstate}",
            f"nrows: \n    {self.nrows}",
            f"ncols:\n    {self.ncols}",
            "table:"
        ]

        for transition in self.table:
            self.code.append(f"    {transition}")
        
        self.code.extend([
            f"wordlen: \n    {self.wordlen}",
            "word:",
        ])

        for symbol in self.word:
            self.code.append(f"    {symbol}")

        self.code.extend([
            ".text",
            "main:",
            f"    load %x0, $initstate, %x1",  # current state in x1
            "    add %x0, %x0, %x2",           # index of symbol in x2
            f"    load %x0, $ncols, %x3",      # ncols in x3
            f"    load %x0, $nrows, %x4",      # nrows in x4
            f"    load %x0, $acceptstate, %x28", # accepting state in x28
            f"    load %x0, $wordlen, %x29",    # wordlen in x29
            "loop:",
            "    beq %x2, %x29, exit",
            "    load %x2, $word, %x3",
            "    mul %x1, %x3, %x6",
            "    add %x6, %x3, %x1",
            "    addi %x2, 1, %x2",
            "    jmp loop",
            "exit:",
            "    beq %x28, %x1, accept",
            "    add %x0, %x0, %x1",  # storing 0 in %x1 if not accepted
            "    end",
            "accept:",
            "    addi %x0, 1, %x1",   # storing 1 in %x1 if accepted
            "    end"
        ])

        return self.code


dfa = {
    0: {0: 1, 1: 0, 2: 0},
    1: {0: 1, 1: 0, 2: 1}
}

toyriscgen = TOYRISCGenerator(dfa, 0, 1, [0, 1,0,1,0,1])
toyriscgen.create_table()  
code = toyriscgen.generate_TOYRISC()

for line in code:
    print(line)
