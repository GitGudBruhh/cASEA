from typing import Dict, Set, Tuple, List
from Automatons.DFA import DFA
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,   # Set the log level
    format='%(message)s'  # Log message format
)


class DFST(DFA):
    def __init__(self, Q: Set[int],
                 Sigma: Set[str],
                 Gamma: Set[str],  # Output alphabet
                 delta: Dict[int, Dict[str, Tuple[int, str]]],
                 q0: int,
                 F: Set[int],
                 name: str
    ):
        super().__init__(Q, Sigma, delta, q0, F, name)
        self.Gamma = Gamma
        self.output = []

    def read_symbol(self, symbol: str):
        if not symbol in self.Sigma:
            raise Exception(f"{self.name} DFST says: {symbol} not in alphabet")
            return

        if symbol in self.delta[self.current_state].keys():
            next_state, output_symbol = self.delta[self.current_state][symbol]

            logging.debug(f"{self.name} DFST: {self.current_state} --- {symbol} ---> {next_state} | Output: {output_symbol}")

            self.current_state = next_state
            self.output.append(output_symbol)  # Collect the output

        else:
            raise Exception(f"{self.name} DFST says: No transition from {self.current_state} on reading {symbol}")

        return

    def read_word(self, word: str):
        self.output = []  # Reset output for new word
        for sym in word:
            try:
                self.read_symbol(sym)
            except Exception as e:
                print(f"{e}")

        if self.current_state in self.F:
            return True
        else:
            return False

    def get_output(self) -> str:
        return ''.join(self.output)  # Return the output as a concatenated string
