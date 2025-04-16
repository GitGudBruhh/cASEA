import sys
from typing import Dict, List, Set

from Grammars.CFG import CFG, ProdRule
from Syntax.Parsers.LL1 import LL1, remove_direct_left_recursion
from Syntax.Parsers.Parser import LL1Parser
from Grammars.Helpers.Factor import left_factor

# Function to convert production dictionary to list of ProdRuleCollection
def convert_productions(prod_dict):
    prod_rule_collections = {}
    for head, productions in prod_dict.items():
        prod_rules = []
        for production in productions:
            # Create a production rule for each production alternative
            prod_rules.append(ProdRule(head=head, tail=production))
        prod_rule_collections[head] = prod_rules
    return prod_rule_collections

def print_parse_table(parse_table, cfg):
    import pprint
    for row_sym, row in parse_table.items():
        print(f"!!!!!!!!{row_sym}!!!!!!!!!")
        pprint.pprint(row)


####################
#    MAIN CODE     #
####################
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

cfg = {
    "name": "Left Recursion Demo",
    "productions": {
        "<expr>": [
            ["<expr>", "+", "id"],
            ["<factor>"],
        ],
        "<factor>": [
            ["<factor>", "*", "id"],
            ["id"],
        ]
    },
    "terminals": ["+", "id", "*"],
    "start_symbol": "<expr>",
    "variables": ["<expr>", "<factor>"]
}

prod_rule_collections = convert_productions(cfg["productions"])
grammar = CFG(
    name=cfg["name"],
    V=cfg["variables"],
    T=cfg["terminals"],
    P=prod_rule_collections,
    S=cfg["start_symbol"]
)

left_rec_removed_grammar = remove_direct_left_recursion(grammar)
# left_rec_removed_grammar = grammar

parse_table = LL1(left_rec_removed_grammar)
print_parse_table(parse_table, left_rec_removed_grammar)

LL1Parser(parse_table, "dba")

# left_recursive_cfg = CFG(cfg["name"], list(cfg["productions"].keys()), cfg["terminals"], cfg["productions"], cfg["start_symbol"])
# print("Before LR removal:")
# left_recursive_cfg.print_grammar()
# remove_direct_left_recursion(left_recursive_cfg)
# print("After LR removal:")
# left_recursive_cfg.print_grammar()
