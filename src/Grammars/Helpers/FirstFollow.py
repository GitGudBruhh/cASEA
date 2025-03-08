from Grammars.CFG import CFG
from typing import Dict, List, Set

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,   # Set the log level
    format='%(message)s'  # Log message format
)

def first(cfg):
    """
    Calculate the FIRST sets for the given context-free grammar (CFG).

    :param cfg: A CFG object containing the variables (non-terminals), terminals, and production rules.
    :return: A dictionary mapping each variable to its corresponding FIRST set.
    """

    def initialize_non_terms(first_sets, cfg):
        """
        Initialize the FIRST sets for non-terminals based on their immediate terminal productions.

        This function populates the FIRST sets of non-terminals with terminals that appear
        as the first symbol in their production rules.

        :param first_sets: A dictionary mapping non-terminals to their FIRST sets.
        :param cfg: A CFG object containing the production rules.
        """
        for head, tails in cfg.P.items():
            for tail in tails:
                symbol = tail[0]
                if symbol in cfg.T:
                    first_sets[head].add(symbol)
                    logging.debug(f'[INIT] Added {symbol} to FIRST({head})')

    def _propagate_non_terms(first_sets, cfg, head, symb):
        """
        Propagate non-terminal FIRST sets to the FIRST set of the given head.

        :param first_sets: A dictionary mapping non-terminals to their FIRST sets.
        :param cfg: A CFG object containing the production rules.
        :param head: The non-terminal whose FIRST set is being updated.
        :param symb: The non-terminal or terminal being processed.
        :return: A tuple indicating if a terminal was added and if epsilon is possible.
        """
        is_terminal_added = False
        is_epsilon_possible = False

        if symb in cfg.V:
            for non_term in first_sets[symb]:
                if non_term == '#':
                    is_epsilon_possible = True
                elif non_term not in first_sets[head]:
                    first_sets[head].add(non_term)
                    logging.debug(f'[PRPG] Added {non_term} to FIRST({head})')
                    is_terminal_added = True

            logging.debug(f'returning {is_terminal_added, is_epsilon_possible}')

            return (is_terminal_added, is_epsilon_possible)

        elif symb in cfg.T:
            if symb in first_sets[head]:
                logging.debug(f'returning F, F')
                return (False, False)
            else:
                first_sets[head].add(symb)
                logging.debug(f'[PRPG] Added {symb} to FIRST({head})')
                logging.debug(f'returning T, F')
                return (True, False)

        else:
            raise Exception(f'Unknown symbol {symb}')

    def propagate(first_sets, cfg, head, tail):
        """
        Propagate the FIRST sets from the tail of a production rule to the head.

        :param first_sets: A dictionary mapping non-terminals to their FIRST sets.
        :param cfg: A CFG object containing the production rules.
        :param head: The non-terminal whose FIRST set is being updated.
        :param tail: The production rule's tail being processed.
        :return: A boolean indicating if any changes were made to the FIRST set.
        """
        running = False
        for idx, symb in enumerate(tail):
            is_t_add, is_eps = _propagate_non_terms(first_sets, cfg, head, symb)
            if is_t_add:
                running = True
            if not is_eps:
                break

        if idx == len(tail) - 1 and is_eps and '#' not in first_sets[head]:
            running = True
            first_sets[head].add('#')
            logging.debug(f'[PRPG] Added # to FIRST({head})')

        return running

    # Create empty FIRST sets for each non-terminal
    first_sets = {var: set() for var in cfg.V}

    # Initialize FIRST sets for non-terminals
    initialize_non_terms(first_sets, cfg)

    # Loop until no change in any FIRST set
    running = True
    while running:
        running = False
        for head, tails in cfg.P.items():
            for tail in tails:
                is_modified = propagate(first_sets, cfg, head, tail)
                if is_modified:
                    running = True

    return first_sets

def follow(cfg: CFG, first_sets: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    follow_sets = {var: set() for var in cfg.V}
    follow_sets[cfg.S].add('$')  # Start symbol follows with end of input

    def compute_follow(variable: str):
        for lhs, productions in cfg.P.items():
            for production in productions:
                symbols = production.split()
                if variable in symbols:
                    index = symbols.index(variable)
                    for sym in symbols[index + 1:]:
                        first_of_sym = first_sets[sym]
                        follow_sets[variable].update(first_of_sym - {'#'})
                        if '#' in first_of_sym:
                            continue
                        break
                    else:
                        if lhs != variable:  # Avoid adding FOLLOW of the same variable
                            compute_follow(lhs)

    for variable in cfg.V:
        compute_follow(variable)

    return follow_sets