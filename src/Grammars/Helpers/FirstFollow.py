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

    def initialize_non_terms_FIRST(first_sets, cfg):
        """
        Initialize the FIRST sets for non-terminals based on their immediate terminal productions.

        This function populates the FIRST sets of non-terminals with terminals that appear
        as the first symbol in their production rules.

        :param first_sets: A dictionary mapping non-terminals to their FIRST sets.
        :param cfg: A CFG object containing the production rules.
        """
        for head, list_of_rules in cfg.P.items():
            tails = [rule.tail for rule in list_of_rules]

            for tail_string in tails:
                symbol = tail_string[0]
                if symbol in cfg.T:
                    first_sets[head].add(symbol)
                    logging.debug(f'[INIT] Added {symbol} to FIRST({head})')

    def _propagate_non_terms_FIRST(first_sets, cfg, head, symb):
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

            return (is_terminal_added, is_epsilon_possible)

        elif symb in cfg.T:
            if symb in first_sets[head]:
                return (False, False)
            else:
                first_sets[head].add(symb)
                logging.debug(f'[PRPG] Added {symb} to FIRST({head})')
                return (True, False)

        else:
            raise Exception(f'Unknown symbol {symb}')

    def propagate_FIRST(first_sets, cfg, head, tail):
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
            is_t_add, is_eps = _propagate_non_terms_FIRST(first_sets, cfg, head, symb)
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
    initialize_non_terms_FIRST(first_sets, cfg)

    # Loop until no change in any FIRST set
    running = True
    while running:
        running = False
        for head, list_of_rules in cfg.P.items():

            tails = [rule.tail for rule in list_of_rules]

            for tail in tails:
                is_modified = propagate_FIRST(first_sets, cfg, head, tail)
                if is_modified:
                    running = True

    return first_sets

def follow(cfg: CFG) -> Dict[str, Set[str]]:
    def initialize_non_terms_FOLLOW(follow_sets, first_sets, cfg):
        """
        Initialize the FOLLOW sets for non-terminals based on their immediate terminal productions.

        This function populates the FOLLOW sets of non-terminals with terminals that appear
        as the FOLLOW symbol in their production rules.

        :param follow_sets: A dictionary mapping non-terminals to their FOLLOW sets.
        :param first_sets: A dictionary mapping non-terminals to their FIRST sets.
        :param cfg: A CFG object containing the production rules.
        """
        for head, list_of_rules in cfg.P.items():

            tails = [rule.tail for rule in list_of_rules]

            for tail_string in tails:
                for idx in range(0, len(tail_string) - 1):
                    curr_sym = tail_string[idx]
                    next_sym = tail_string[idx + 1]

                    if curr_sym in cfg.V and next_sym in cfg.T:
                        follow_sets[curr_sym].add(next_sym)
                        logging.debug(f'[INIT] Added {next_sym} to FOLLOW({curr_sym})')

                    elif curr_sym in cfg.V and next_sym in cfg.V:
                        next_idx = idx + 1
                        while next_idx != len(tail_string):
                            is_epsilon_possible = False
                            if '#' in first_sets[next_sym]:
                                is_epsilon_possible = True

                            tmp_no_eps = first_sets[next_sym] - {'#'}
                            follow_sets[curr_sym] = follow_sets[curr_sym].union(tmp_no_eps)

                            logging.debug(f'[INIT] Added FIRST({next_sym}) to FOLLOW({curr_sym})')

                            if is_epsilon_possible:
                                next_idx += 1
                            else:
                                break

    def propagate_FOLLOW(follow_sets, cfg, head, tail):
        """
        TODO: Write description

        :param follow_sets: A dictionary mapping non-terminals to their FOLLOW sets.
        :param first_sets: A dictionary mapping non-terminals to their FIRST sets.
        :param cfg: A CFG object containing the production rules.
        """
        is_terminal_added = False

        last_symbol = tail[-1]
        if last_symbol in cfg.V:
            if head != last_symbol:
                for symb in follow_sets[head]:
                    if symb not in follow_sets[last_symbol]:
                        follow_sets[last_symbol].add(symb)
                        is_terminal_added = True

        return is_terminal_added

    # Create empty FOLLOW sets for each non-terminal (add $)
    follow_sets = {var: set() for var in cfg.V}
    follow_sets[cfg.S].add('$')

    # Create first sets
    first_sets = first(cfg)

    # Initialize by adding direct terminals
    # and also FIRST of non-terminals
    initialize_non_terms_FOLLOW(follow_sets, first_sets, cfg)

    running = True
    while running:
        running = False
        for head, list_of_rules in cfg.P.items():

            tails = [rule.tail for rule in list_of_rules]

            for tail in tails:
                is_modified = propagate_FOLLOW(follow_sets, cfg, head, tail)
                if is_modified:
                    running = True

    return follow_sets
