import sys
# sys.path.append("../src")  # Adjust to the correct path
from Grammars.CFG import CFG
from typing import Dict, List, Set
from Syntax.Parsers.LL1 import LL1, remove_left_recursion

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

def check_LL1():

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

def check_left_recursion():

    cfg =  {
            "name": "Simple Regex Extension",
            "productions": {
                "R": ["T", "RT"],
                "T": ["F", "TF"],
                "F": ["0", "1", "(R)", "F*", "F+"]
            },
            "terminals": ["#", "0", "1", "(", ")", "*", "+"],
            "start_symbol": "R"
        }

    cfg = {
        "name": "Simple Regex Extension",
        "productions": {
            "<regex>": [
                ["<term>"],
                ["<regex>", "<term>"]
            ],
            "<term>": [
                ["<factor>"],
                ["<term>", "<factor>"]
            ],
            "<factor>": [
                ["0"],
                ["1"],
                ["(", "<regex>", ")"],
                ["<factor>", "*"],
                ["<factor>", "+"]
            ]
        },
        "terminals": ["#", "0", "1", "(", ")", "*", "+"],
        "start_symbol": "<regex>",
        "variables": ["<regex>", "<term>", "<factor>"]
    }

    left_recursive_cfg = CFG(cfg["name"], list(cfg["productions"].keys()), cfg["terminals"], cfg["productions"], cfg["start_symbol"])
    print("Before LR removal:")
    left_recursive_cfg.print_grammar()
    remove_left_recursion(left_recursive_cfg)
    print("After LR removal:")
    left_recursive_cfg.print_grammar()


# check_LL1()
check_left_recursion()