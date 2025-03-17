from typing import Dict, List
from pprint import pprint

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
        :param P: Dictionary of production rules.
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
        pprint(self.P)

        print("Start Symbol:")
        pprint(self.S)
        print()


