import copy
import time
from Grammars.CFG import CFG

def remove_direct_left_recursion(cfg: CFG):
    """
    Remove direct left recursion from a context-free grammar (CFG).

    :param cfg: The CFG object from which to remove direct left recursion.
    :return: A new CFG object with direct left recursion removed.
    """

    # Make a copy of the object
    cfg_copy = CFG(cfg.name , copy.deepcopy(cfg.V), copy.deepcopy(cfg.T), {}, cfg.S)

    # Create a dummy non terminal to help in replacement
    replc_str = 'REPLACE'
    replc_idx = 1

    # Iterate over each rule
    for head, tails in cfg.P.items():
        rec_list = []
        not_rec_list = []

        # Create list of recursive and non-recursive tails
        for tail in tails:
            if tail[0] == head:
                rec_list.append(tail)
            else:
                not_rec_list.append(tail)

        # If there are no left recursions, dont change anything
        if not rec_list:
            cfg_copy.P[head] = not_rec_list
            continue

        # Dummy non terminal
        replc_non_term = '<' + replc_str + str(replc_idx) + '>'
        cfg_copy.P.setdefault(head, [])
        cfg_copy.P.setdefault(replc_non_term, [])

        # For each recursive tail, create two new rules
        # One for the actual variable, removing the recursion
        # One for the dummy variable

        # WITH LEFTREC: A -> Ax | b
        #
        # RMVD LEFTREC: A -> bS       (new_tail_1)
        #             : S -> xS | #   (new_tail_2)
        for rec in rec_list:
            for no_rec in not_rec_list:

                # Special case: Remove trailing '#' from no_rec if it exists
                while no_rec and no_rec[-1] == '#':
                    no_rec.pop()

                # Create new tails
                new_tail_1 = no_rec + [replc_non_term]
                new_tail_2 = rec[1:] + [replc_non_term]

                # Add new tails
                if new_tail_1 not in cfg_copy.P[head]:
                    cfg_copy.P[head].append(new_tail_1)

                if new_tail_2 not in cfg_copy.P[replc_non_term]:
                    cfg_copy.P[replc_non_term].append(new_tail_2)

                # Add new non terminal
                if replc_non_term not in cfg_copy.V:
                    cfg_copy.V.append(replc_non_term)

                # Add epsilon production
                if '#' not in cfg_copy.T:
                    cfg_copy.T.append('#')

                if '#' not in cfg_copy.P[replc_non_term]:
                    cfg_copy.P[replc_non_term].append('#')

        replc_idx += 1

    return cfg_copy


def remove_indirect_left_recursion(cfg: CFG):
    pass
