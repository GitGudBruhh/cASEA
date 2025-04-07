class TOYRISCGenerator:
    def __init__(self, dfa, initstate, acceptingstates, word):
        self.dfa = dfa
        self.initstate = initstate
        self.acceptingstates = acceptingstates
        self.nacceptingstates = len(self.acceptingstates)
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
            f"nacceptingstates: \n    {self.nacceptingstates}",
            f"nrows: \n    {self.nrows}",
            f"ncols:\n    {self.ncols}",
            "table:"
        ]

        for transition in self.table:
            self.code.append(f"    {transition}")

        self.code.append("acceptingstates:")
        for acceptingstate in self.acceptingstates:
            self.code.append(f"    {acceptingstate}")
        
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
            "    add %x0, %x0, %x6",           
            "    add %x0, %x0, %x7",           
            f"    load %x0, $ncols, %x3",      # ncols in x3
            f"    load %x0, $nrows, %x4",      # nrows in x4
            f"    load %x0, $nacceptingstates, %x28", # accepting state in x28
            f"    load %x0, $wordlen, %x29",    # wordlen in x29
            "loop:",
            "    beq %x2, %x29, exit",
            "    load %x2, $word, %x5",
            "    mul %x1, %x3, %x6",
            "    add %x6, %x5, %x6",
            "    load %x6, $table, %x1",
            "    addi %x2, 1, %x2",
            "    jmp loop",
            "exit:",
            "    beq %x7, %x28, reject",
            "    load %x7, $acceptingstates, %8",
            "    beq %x8, %x1, accept",
            "    addi %x7, 1, %x7", 
            "    jmp exit",
            "accept:",
            "    addi %x0, 1, %x10",   # storing 1 in %x1 if accepted
            "    end",
            "reject:",
            "    add %x0, %x0, %x10",   # storing 0 in %x1 if not accepted
            "    end"
        ])

        return self.code


dfa = {
    0: {0: 1, 1: 0, 2: 2},
    1: {0: 0, 1: 1, 2: 2},
    2: {0: 1, 1: 2, 2: 0}
}


toyriscgen = TOYRISCGenerator(dfa, 2, [0, 2], [0, 1, 2, 2, 0, 0, 2, 0])
toyriscgen.create_table()  
code = toyriscgen.generate_TOYRISC()

for line in code:
    print(line)
