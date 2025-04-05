from typing import Dict, List
from pprint import pprint

class ProdRule:
    """
    Represents a single production rule.

    Attributes:
        head (str): The non-terminal on the left-hand side.
        tail (List[str]): The sequence of symbols on the right-hand side.
        action (callable): The semantic action function for this production.
    """

    def __init__(self, head, tail, action_function=None, is_literal=False):
        self.head = head
        self.tail = tail
        self.action = action_function
        self.is_literal = is_literal

class CFG:
    """
    A class representing a Context-Free Grammar (CFG).

    Attributes:
        V (List[str]): Variables (non-terminals).
        T (List[str]): Terminals.
        P (Dict[str, List[List[str]]): Production rules.
        S (str): Start symbol.
        name (str): Name of the grammar.
    """

    def __init__(self, name, V, T, P, S):
        """
        Initializes a CFG instance.

        :param name: Name of the grammar.
        :param V: List of variables (non-terminals).
        :param T: List of terminals.
        :param P: List of ProdRules.
        :param S: Start symbol.
        """
        self.name = name
        self.V = V
        self.T = T
        self.P = P
        self.S = S

    def print_grammar(self):
        print()
        print("Grammar Name:")
        pprint(self.name)

        print("Variables:")
        pprint(self.V)

        print("Terminals:")
        pprint(self.T)

        print("Production Rules:")
        for head, prod_rules in self.P.items():
            print(head, ":", [pr.tail for pr in prod_rules])

        print("Start Symbol:")
        pprint(self.S)
        print()


