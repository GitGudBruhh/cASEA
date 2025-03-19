import sys
# sys.path.append("../src")  # Adjust to the correct path
from Grammars.CFG import CFG
from typing import Dict, List, Set
from Syntax.Parsers.LL1 import LL1

def print_parse_table(parse_table, cfg):
    print("Parse Table:")
    print(" ", end="\t")
    terminals = cfg.T
    terminals.append("$")
    for x in terminals:
        print(x,end="\t\t")
    print("\n")

    for lhs, cells in parse_table.items():
        print(lhs, end="\t")
        for terminal in terminals:
            print(cells[terminal], end="\t\t")
        print("\n")

cfg = {
    "name": "Simple Regex Extension",
        "productions": {
            "A": ["EB"],
            "B": ["a", "(e)"],
            "C": ["d", "E"],
            "E": ["Cb", "#"]
        },
        "terminals": ["a", "(", ")", "b", "d", "e", "#"],
        "start_symbol": "A"
}

grammar = CFG(cfg["name"], list(cfg["productions"].keys()), cfg["terminals"], cfg["productions"], cfg["start_symbol"])
print(f"{grammar}")
parse_table = LL1(grammar)
print_parse_table(parse_table, grammar)