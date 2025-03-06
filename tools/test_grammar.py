# test_cfgs.py

from Grammars.CFG import CFG
from Grammars.Helpers.FirstFollow import first

cfgs = [
    {
        "name": "Simple Regex Extension",
        "productions": {
            "R": ["T", "RT"],
            "T": ["F", "TF"],
            "F": ["0", "1", "(R)", "F*", "F+"]
        },
        "terminals": ["0", "1", "(", ")", "*", "+"],
        "start_symbol": "R"
    },
    {
        "name": "Arithmetic Expressions",
        "productions": {
            "E": ["E+T", "E-T", "T", "#"],
            "T": ["T*F", "T/F", "F"],
            "F": ["(E)", "i"]
        },
        "terminals": ["+", "-", "*", "/", "(", ")", "i"],
        "start_symbol": "E"
    },
    {
        "name": "Boolean Expressions",
        "productions": {
            "B": ["B&A", "B|A", "A", "#"],
            "A": ["!F", "F"],
            "F": ["T", "F", "(B)"]
        },
        "terminals": ["&", "|", "!", "T", "F", "(", ")"],
        "start_symbol": "B"
    },
    {
        "name": "Simple Statements",
        "productions": {
            "S": ["iEtS", "iEtSeS", "pE", "#"],
            "E": ["i", "n"]
        },
        "terminals": ["i", "n", "t", "e", "p"],
        "start_symbol": "S"
    },
    {
        "name": "List Comprehensions",
        "productions": {
            "L": ["[EfiR]", "#"],
            "R": ["i", "R,i"],
            "E": ["i", "n"]
        },
        "terminals": ["[", "]", "f", "i", ",", "n"],
        "start_symbol": "L"
    },
    {
        "name": "Optional Elements",
        "productions": {
            "A": ["B", "B#"],
            "B": ["C", "C#"],
            "C": ["D", "D#"],
            "D": ["d", "e"]
        },
        "terminals": ["d", "e"],
        "start_symbol": "A"
    },
    {
        "name": "Nested Structures",
        "productions": {
            "X": ["Y", "Y#"],
            "Y": ["(X)", "X)"],
            "Z": ["z", "Z#"]
        },
        "terminals": ["(", ")", "z"],
        "start_symbol": "X"
    },
    {
        "name": "Simple Choices",
        "productions": {
            "C": ["A|B", "#"],
            "A": ["a"],
            "B": ["b"]
        },
        "terminals": ["a", "b", "|"],
        "start_symbol": "C"
    },
    {
        "name": "Repetitions",
        "productions": {
            "R": ["A*", "A#"],
            "A": ["a", "b"]
        },
        "terminals": ["a", "b", "*"],
        "start_symbol": "R"
    },
    {
        "name": "Complex Expressions",
        "productions": {
            "E": ["E+E", "E*E", "E#"],
            "T": ["(E)", "i"]
        },
        "terminals": ["+", "*", "(", ")", "i"],
        "start_symbol": "E"
    }
]


for cfg in cfgs:
    grammar = CFG(cfg["name"], list(cfg["productions"].keys()), cfg["terminals"], cfg["productions"], cfg["start_symbol"])
    print(f"{grammar}")
    first_sets = first(grammar)
    print("FIRST sets:")
    for var, first_set in first_sets.items():
        print(f"{var}: {first_set}")
