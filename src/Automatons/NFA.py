from typing import Dict, Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,   # Set the log level
    format='%(message)s'  # Log message format
)

class NFA:
    """
    A class representing a Non-Deterministic Finite Automaton (NFA).

    Attributes:
        Q (Set[int]): A set of states in the NFA.
        Sigma (Set[str]): The input alphabet of the NFA.
        delta (Dict[int, Dict[str, List[int]]]): The transition function mapping states and input symbols to next states.
        q0 (int): The initial state of the NFA.
        F (Set[int]): A set of accepting states.
        name (str): The name of the NFA.
        current_states (Set[int]): The current state of the NFA during processing.
        log_state_transition (bool): A flag to enable logging of state transitions.
    """

    def __init__(self, Q, Sigma, delta, q0, F, name):
        """
        Initializes a NFA instance.

        :param Q: Set of states.
        :param Sigma: Input alphabet.
        :param delta: Transition function.
        :param q0: Initial state.
        :param F: Set of accepting states.
        :param name: Name of the NFA.
        """
        self.Q = Q            # Set of states
        self.Sigma = Sigma    # Input alphabet
        self.delta = delta    # Transition function
        self.q0 = q0          # Initial state
        self.F = F            # Set of accepting states
        self.name = name
        self.current_states = {q0}
        self._expand_consuming_epsilon()

    def _expand_consuming_epsilon(self):
        """
        Covers states by consuming epsilons.
        """

        expanded = True
        while expanded:

            # Assume not expanded
            expanded = False

            # Iterate overe very current state
            for state in self.current_states:

                # Check if an epsilon transition is possible
                if '#' not in self.delta[state].keys():
                    continue

                # Iterate over the next states on an epsilon transition
                next_states = set(self.delta[state]['#'])
                for next_state in next_state:

                    # Add the possible states into current state
                    if next_state not in self.current_states:
                        # Set if expanded by at least one state
                        self.current_states.add(next_state)
                        expanded = True

    def reset_to_start(self) -> None:
        """Resets the current state to the initial states."""
        self.current_states = {self.q0}
        self._expand_consuming_epsilon()

    def read_symbol(self, symbol) -> None:
        """
        Reads a single input symbol and transitions to the next states.

        :param symbol: The input symbol to read.
        :raises Exception: If the symbol is not in the alphabet or if there is no transition from the current states.
        """
        if not symbol in self.Sigma:
            raise Exception(f"{self.name} NFA says: {symbol} not in alphabet")
            return

        new_states = set()

        for cur_state in self.current_states:
            # Check all next states possible
            _next_state = self.delta[cur_state][symbol]

            logging.debug(f"{self.name} NFA: {cur_state} --- {symbol} ---> {_next_state}")

            # Update new states and remove current state
            new_states.update(_next_state)
            self.current_states - cur_state

        if len(new_states) == 0:
            raise Exception(f"{self.name} NFA says: No transition from {self.current_states} on reading {symbol}")

        self.current_states = new_states

        return

    def read_word(self, word) -> bool:
        """
        Reads a string of input symbols and processes it through the NFA.

        :param word: The input string to read.
        :return: True if the final state is an accepting state, False otherwise.
        """
        for sym in word:
            try:
                self.read_symbol(sym)
            except Exception as e:
                print(f"{e}")

        return self.current_state in self.F
