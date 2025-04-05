import sys
from typing import Dict, List, Set

from Grammars.CFG import CFG
from Syntax.Parsers.LL1 import LL1, remove_direct_left_recursion
from Syntax.Parsers.Parser import LL1Parser
from Grammars.Helpers.Factor import left_factor

def print_parse_table_old(parse_table, cfg):
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

def print_parse_table(parse_table, cfg):
    # Get the terminals and add the end-of-input symbol
    terminals = cfg.T + ["$"]

    # Calculate the width for formatting
    max_length = max(len(term) for term in terminals) + 2  # Add some padding
    lhs_length = max(len(lhs) for lhs in parse_table.keys()) + 2  # Add padding for LHS

    # Print the header
    print("Parse Table:")
    header = " " * lhs_length + " | " + " | ".join(f"{terminal:<{max_length}}" for terminal in terminals)
    print(header)
    print("-" * len(header))  # Print a separator line

    # Print each row of the parse table
    for lhs, cells in parse_table.items():
        row = f"{lhs:<{lhs_length}} | "
        for terminal in terminals:
            # Format the cell content
            cell_content = ', '.join(cells.get(terminal, set()))  # Join set elements for better readability
            row += f"{cell_content:<{max_length}} | "
        print(row)
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

    LL1Parser(parse_table, "dba")

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
    remove_direct_left_recursion(left_recursive_cfg)
    print("After LR removal:")
    left_recursive_cfg.print_grammar()


check_LL1()