from Grammars.CFG import CFG
from typing import List
import copy

def find_factor(tails: List[List[str]]):

    # Return if there exists only one tail
    if len(tails) <= 1:
        return None

    # Get min length of all tail
    lengths = [len(tail) for tail in tails]
    min_len_of_tail = min(lengths)
    common_prefix = []
    window_idx = 0

    # Find the maximal factor
    while window_idx < min_len_of_tail:
        current_sym = tails[0][window_idx]
        if all(tail[window_idx] == current_sym for tail in tails):
            common_prefix.append(current_sym)
            window_idx += 1
        else:
            break

    return common_prefix


def left_factor(cfg: CFG):
    """
    Left factor the tails from a context-free grammar (CFG).

    :param cfg: The CFG object to modify.
    :return: A new CFG object after left factoring.
    """

    # Make a copy of the object
    cfg_copy = CFG(cfg.name , copy.deepcopy(cfg.V), copy.deepcopy(cfg.T), {}, cfg.S)

    # Create a dummy non terminal to help in replacement
    replc_str = 'LEFT-FACTOR-DUMMY'
    replc_idx = 1

    # Iterate over each rule
    for head, tails in cfg.P.items():
        common_prefix = find_factor(tails)

        # Check if a common prefix exists
        if common_prefix is not None and len(common_prefix) > 0:

            # Dummy non terminal
            replc_non_term = '<' + replc_str + str(replc_idx) + '>'
            cfg_copy.P.setdefault(replc_non_term, [])

            # Replace the tails of the head
            cfg_copy.P[head] = common_prefix + [replc_non_term]

            # Add the tails of a new dummy head
            for tail in tails:
                new_tail = tail[len(common_prefix):]

                # Special case for epsilon
                if new_tail == []:
                    cfg_copy.P[replc_non_term].append(['#'])
                else:
                    cfg_copy.P[replc_non_term].append(new_tail)


    return cfg_copy
