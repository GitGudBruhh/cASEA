from typing import Dict, Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,   # Set the log level
    format='%(message)s'  # Log message format
)

class DFA:
    """
    A class representing a Deterministic Finite Automaton (DFA).

    Attributes:
        Q (Set[int]): A set of states in the DFA.
        Sigma (Set[str]): The input alphabet of the DFA.
        delta (Dict[int, Dict[str, int]]): The transition function mapping states and input symbols to next states.
        q0 (int): The initial state of the DFA.
        F (Set[int]): A set of accepting states.
        name (str): The name of the DFA.
        current_state (int): The current state of the DFA during processing.
        log_state_transition (bool): A flag to enable logging of state transitions.
    """

    def __init__(self, Q, Sigma, delta, q0, F, name):
        """
        Initializes a DFA instance.

        :param Q: Set of states.
        :param Sigma: Input alphabet.
        :param delta: Transition function.
        :param q0: Initial state.
        :param F: Set of accepting states.
        :param name: Name of the DFA.
        """
        self.Q = Q            # Set of states
        self.Sigma = Sigma    # Input alphabet
        self.delta = delta    # Transition function
        self.q0 = q0          # Initial state
        self.F = F            # Set of accepting states
        self.name = name
        self.current_state = self.q0

    def reset_to_start(self) -> None:
        """Resets the current state to the initial state."""
        self.current_state = self.q0

    def read_symbol(self, symbol) -> None:
        """
        Reads a single input symbol and transitions to the next state.

        :param symbol: The input symbol to read.
        :raises Exception: If the symbol is not in the alphabet or if there is no transition from the current state.
        """
        if not symbol in self.Sigma:
            raise Exception(f"{self.name} DFA says: {symbol} not in alphabet")
            return

        if symbol in self.delta[self.current_state].keys():
            next_state = self.delta[self.current_state][symbol]

            logging.debug(f"{self.name} DFA: {self.current_state} --- {symbol} ---> {next_state}")

            self.current_state = next_state
        else:
            raise Exception(f"{self.name} DFA says: No transition from {self.current_state} on reading {symbol}")

        return

    def read_word(self, word) -> bool:
        """
        Reads a string of input symbols and processes it through the DFA.

        :param word: The input string to read.
        :return: True if the final state is an accepting state, False otherwise.
        """
        for sym in word:
            try:
                self.read_symbol(sym)
            except Exception as e:
                print(f"{e}")

        return self.current_state in self.F
