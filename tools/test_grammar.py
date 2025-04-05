# test_cfgs.py

from Grammars.CFG import CFG, ProdRule
from Grammars.Helpers.FirstFollow import first, follow
from Grammars.Helpers.Recursions import remove_direct_left_recursion
from Grammars.Helpers.Factor import left_factor
from pprint import pprint

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


test_cases = [
    {
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
    },
    {
        "name": "Arithmetic Expressions",
        "productions": {
            "<expr>": [
                ["<expr>", "+", "<term>"],
                ["<expr>", "-", "<term>"],
                ["<term>"],
                ["#"]
            ],
            "<term>": [
                ["<term>", "*", "<factor>"],
                ["<term>", "/", "<factor>"],
                ["<factor>"]
            ],
            "<factor>": [
                ["(", "<expr>", ")"],
                ["i"]
            ]
        },
        "terminals": ["#", "+", "-", "*", "/", "(", ")", "i"],
        "start_symbol": "<expr>",
        "variables": ["<expr>", "<term>", "<factor>"]
    },
    {
        "name": "Boolean Expressions",
        "productions": {
            "<bool>": [
                ["<bool>", "&", "<bool>"],
                ["<bool>", "|", "<bool>"],
                ["!", "<bool>"],
                ["(", "<bool>",  ")"],
                ["T"],
                ["F"]
            ],
        },
        "terminals": ["&", "|", "!", "T", "F", "(", ")"],
        "start_symbol": "<bool>",
        "variables": ["<bool>"]
    },
    {
        "name": "Simple Statements",
        "productions": {
            "<stmt>": [
                ["i", "E", "t", "<stmt>"],
                ["i", "E", "t", "e", "<stmt>"],
                ["p", "<expr>"],
                ["#"]
            ],
            "<expr>": [
                ["i"],
                ["n"]
            ]
        },
        "terminals": ["#", "i", "n", "t", "e", "p"],
        "start_symbol": "<stmt>",
        "variables": ["<stmt>", "<expr>"]
    },
    {
        "name": "List Comprehensions",
        "productions": {
            "<list>": [
                ["[", "<expr>", "f", "<rest>", "]"],
                ["#"]
            ],
            "<rest>": [
                ["i"],
                ["<rest>", ",", "i"]
            ],
            "<expr>": [
                ["i"],
                ["n"]
            ]
        },
        "terminals": ["#", "[", "]", "f", "i", ",", "n"],
        "start_symbol": "<list>",
        "variables": ["<list>", "<rest>", "<expr>"]
    },
    {
        "name": "Optional Elements",
        "productions": {
            "<opt>": [
                ["<base>"],
                ["<base>", "#"]
            ],
            "<base>": [
                ["<choice>"],
                ["<choice>", "#"]
            ],
            "<choice>": [
                ["<element>"],
                ["<element>", "#"]
            ],
            "<element>": [
                ["d"],
                ["e"]
            ]
        },
        "terminals": ["#", "d", "e"],
        "start_symbol": "<opt>",
        "variables": ["<opt>", "<base>", "<choice>", "<element>"]
    },
    {
        "name": "Nested Structures",
        "productions": {
            "<nest>": [
                ["<inner>"],
                ["<inner>", "#"]
            ],
            "<inner>": [
                ["(", "<nest>", ")"],
                ["<nest>", ")"]
            ],
            "<leaf>": [
                ["z"],
                ["<leaf>", "#"]
            ]
        },
        "terminals": ["#", "(", ")", "z"],
        "start_symbol": "<nest>",
        "variables": ["<nest>", "<inner>", "<leaf>"]
    },
    {
        "name": "Simple Choices",
        "productions": {
            "<choice>": [
                ["<optionA>", "|", "<optionB>"],
                ["#"]
            ],
            "<optionA>": [
                ["a"]
            ],
            "<optionB>": [
                ["b"]
            ]
        },
        "terminals": ["#", "a", "b", "|"],
        "start_symbol": "<choice>",
        "variables": ["<choice>", "<optionA>", "<optionB>"]
    },
    {
        "name": "Repetitions",
        "productions": {
            "<repeat>": [
                ["<element>", "*"],
                ["<element>", "#"]
            ],
            "<element>": [
                ["a"],
                ["b"]
            ]
        },
        "terminals": ["#", "a", "b", "*"],
        "start_symbol": "<repeat>",
        "variables": ["<repeat>", "<element>"]
    },
    {
        "name": "Complex Expressions",
        "productions": {
            "<expr>": [
                ["<expr>", "+", "<expr>"],
                ["<expr>", "*", "<expr>"],
                ["#"]
            ],
            "<term>": [
                ["(", "<expr>", ")"],
                ["i"]
            ]
        },
        "terminals": ["#", "+", "*", "(", ")", "i"],
        "start_symbol": "<expr>",
        "variables": ["<expr>", "<term>"]
    },
    {
        "name": "All Epsilon",
        "productions": {
            "<expr>": [
                ["<A>", "<B>", "<C>"],
            ],
            "<A>": [
                ["<A>", "<X>"],
                ["a"],
                ["#"]
            ],
            "<B>": [
                ["<B>", "<X>"],
                ["b"],
                ["#"]
            ],
            "<C>": [
                ["<C>", "<X>"],
                ["c"],
                ["#"]
            ],
            "<X>": [
                ["<X>", "<X>"],
                ["x"],
                ["#"]
            ]
        },
        "terminals": ["#", "a", "b", "c", "x"],
        "start_symbol": "<expr>",
        "variables": ["<expr>", "<A>", "<B>", "<C>", "<X>"]
    },
    {
        "name": "Left Factor Test",
        "productions": {
            "<expr>": [
                ["<A>", "<B>", "+"],
                ["<A>", "<B>", "-"],
                ["<A>", "<B>", "*"],
            ],
            "<A>": [
                ["x"]
            ],
            "<B>": [
                ["y"]
            ],
        },
        "terminals": ["*", "-", "+", "y", "x"],
        "start_symbol": "<expr>",
        "variables": ["<expr>", "<A>", "<B>"]
    }
]

# For this example, let's pick a single test case (for example, the last one)
cfgs = [test_cases[1]]

for cfg in cfgs:
    # Convert the productions dictionary to a list of ProdRuleCollection objects.
    prod_rule_collections = convert_productions(cfg["productions"])

    # Build the CFG using the productions as RuleCollections (ProdRuleCollection)
    grammar = CFG(
        name=cfg["name"],
        V=cfg["variables"],         # use provided variables list
        T=cfg["terminals"],
        P=prod_rule_collections,
        S=cfg["start_symbol"]
    )

    print("Original Grammar:")
    grammar.print_grammar()

    # first_sets = first(grammar)
    # follow_sets = follow(grammar)
    #
    # print("FIRST sets:")
    # for var, first_set in first_sets.items():
    #     print(f"    {var}: {first_set}")
    #
    # print("FOLLOW sets:")
    # for var, follow_set in follow_sets.items():
    #     print(f"    {var}: {follow_set}")


    # The following parts are commented out. Uncomment them if you have implemented these helpers.
    # d_l_rec_removed = remove_direct_left_recursion(grammar)
    # d_l_rec_removed.print_grammar()

    # ind_l_rec_removed = remove_indirect_left_recursion(d_l_rec_removed)
    # ind_l_rec_removed.print_grammar()

    # Left factoring example (assuming left_factor returns a new CFG)
    # left_factored = left_factor(grammar)
    # print("Left Factored Grammar:")
    # left_factored.print_grammar()

