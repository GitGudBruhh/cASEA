from typing import List
from Automatons.DFA import DFA
from Lexical.Lexer import Lexer  # Adjust the import based on your project structure

class DFALexer(Lexer):
    """
    A class representing a Lexer that uses DFAs for tokenization.

    Attributes:
        dfas (List[DFA]): A list of DFAs used for tokenization.
    """

    def __init__(self, dfas: List[DFA], input_string: str):
        """
        Initializes a DFALexer instance.

        :param dfas: A list of DFAs used for tokenization.
        :param input_string: The input string to be tokenized.
        """
        super().__init__(input_string)  # Call the constructor of the Lexer class
        self.dfas = dfas

    def tokenize(self) -> None:
        """
        Tokenizes the input string using the provided DFAs.

        This method processes the input string character by character,
        using the DFAs to identify valid tokens. It raises exceptions
        for invalid symbols or ambiguity in token recognition.
        """
        for dfa in self.dfas:
            dfa.reset_to_start()
            # dfa.log_transitions(True)

        while self.current_position < len(self.input_string):
            current_symbol = self.input_string[self.current_position]
            final_states = []

            for dfa in self.dfas:
                # Read symbols until we can't read anymore or reach a final state
                try:
                    dfa.read_symbol(current_symbol)
                    if dfa.current_state in dfa.F:
                        final_states.append(dfa)
                except Exception as e:
                    dfa.reset_to_start()
                    continue

            # Check for final states
            if len(final_states) == 0:
                if all(dfa.current_state == dfa.q0 for dfa in self.dfas):
                    raise Exception(f"Invalid symbol: Could not read '{current_symbol}' at position {self.current_position}")

            elif len(final_states) > 1:
                raise Exception(f"Ambiguity detected at position {self.current_position}")

            elif len(final_states) == 1:
                accepted_dfa = final_states[0]
                self.tokens.append(self.input_string[self.start:self.current_position + 1])
                self.start = self.current_position + 1
                accepted_dfa.reset_to_start()

            # Move to the next symbol
            self.current_position += 1

    def get_tokens(self) -> List[str]:
        """
        Returns the list of tokens generated from the input string.

        :return: A list of tokens.
        """
        return self.tokens
