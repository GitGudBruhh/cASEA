from typing import Dict, List

class CFG:
    """
    A class representing a Context-Free Grammar (CFG).

    Attributes:
        V (List[str]): Variables (non-terminals).
        T (List[str]): Terminals.
        P (Dict[str, List[str]]): Production rules.
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

    def __str__(self):
        return f"\nGrammar Name: {self.name}\nVariables: {self.V}\nTerminals: {self.T}\nProduction Rules: {self.P}\nStart Symbol: {self.S}"
