from Grammars.CFG import CFG
from Syntax.Parsers.Parser import LL1Parser

cfg = {
    "name": "Simple Grammar",
    "productions": {
        "S": ["F", "(S+F)"], 
        "F": ["a"]            
    },
    "terminals": ["a", "+", "(", ")"],  
    "start_symbol": "S" 
}


parse_table = {
    'S': {
        'a': {'F'},        # When 'a' is encountered, we can derive S using F
        '(': {'(S+F)'},  # When '(' is encountered, we can derive S using (S + F)
        '+': set(),             # No production for '+'
        ')': set(),             # No production for ')'
        '$': set()              # No production for end of input
    },
    'F': {
        'a': {'a'},        # When 'a' is encountered, we can derive F using a
        '(': set(),             # No production for '('
        '+': set(),             # No production for '+'
        ')': set(),             # No production for ')'
        '$': set()              # No production for end of input
    }
}
# Use (a+a) for the above grammar

cfg = {
    "name": "Expression Grammar",
    "productions": {
        "S": ["TE"],          # S produces TE
        "E": ["+TE", "#"],    # E produces +TE or epsilon (represented by #)
        "T": ["FI"],          # T produces FI
        "I": ["*FI", "#"],     # I produces *FI or epsilon (represented by #)
        "F": ["(S)", "i"]    # F produces (S) or id
    },
    "terminals": ["+", "*", "(", ")", "i", "#"],  # Updated terminals
    "start_symbol": "S" 
}

parse_table = {
    'S': {
        'i': {'TE'},          # When 'id' is encountered, we can derive S using TE
        '(': {'TE'},           # When '(' is encountered, we can derive S using TE
        '$': set()             # No production for end of input
    },
    'E': {
        '+': {'+TE'},          # When '+' is encountered, we can derive E using +TE
        ')': {'#'},            # E can also produce epsilon (represented by #)
        '$': {"#"}
    },
    'T': {
        'i': {'FI'},          # When 'id' is encountered, we can derive T using FI
        '(': {'FI'},           # When '(' is encountered, we can derive T using FI
    },
    'I': {
        '*': {'*FI'},          # When '*' is encountered, we can derive I using *FI
        '+': {'#'},            # I can also produce epsilon (represented by #)
        ')': {'#'},
        '$': {'#'},
    },
    'F': {
        '(': {'(S)'},          # When '(' is encountered, we can derive F using (S)
        'i': {'i'},          # When 'id' is encountered, we can derive F using id
    }
}
# Use i+i*i for the above grammar


grammar = CFG(cfg["name"], list(cfg["productions"].keys()), cfg["terminals"], cfg["productions"], cfg["start_symbol"])

parser = LL1Parser(parse_table, grammar)
tree = parser.parse('i+i*i')

if tree:
    tree.printTree()