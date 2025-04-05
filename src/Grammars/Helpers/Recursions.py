import copy
import time
from Grammars.CFG import CFG, ProdRule

def remove_direct_left_recursion(cfg: CFG):
    """
    Remove direct left recursion from a context-free grammar (CFG).

    :param cfg: The CFG object from which to remove direct left recursion.
    :return: A new CFG object with direct left recursion removed.
    """

    # Make a copy of the object
    cfg_copy = CFG(cfg.name , copy.deepcopy(cfg.V), copy.deepcopy(cfg.T), {}, cfg.S)

    # Create a dummy non terminal to help in replacement
    replc_str = 'LEFT-REC-DUMMY'
    replc_idx = 1

    # Iterate over each rule
    for head, list_of_rules in cfg.P.items():
        tails = [rule.tail for rule in list_of_rules]

        rec_rule_list = []
        not_rec_rule_list = []

        # Create list of recursive and non-recursive tails
        for tail in tails:
            if tail[0] == head:
                rec_rule_list.append(ProdRule(head=head, tail=tail))
            else:
                not_rec_rule_list.append(ProdRule(head=head, tail=tail))

        # If there are no left recursions, dont change anything
        if not rec_rule_list:
            cfg_copy.P[head] = not_rec_rule_list
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
        for rec_rule in rec_rule_list:

            rec = copy.copy(rec_rule.tail)

            for no_rec_rule in not_rec_rule_list:

                no_rec = copy.copy(no_rec_rule.tail)

                # Special case: Remove trailing '#' from no_rec if it exists
                while no_rec and no_rec[-1] == '#':
                    no_rec.pop()

                # Create new tails
                new_tail_1 = no_rec + [replc_non_term]
                new_tail_2 = rec[1:] + [replc_non_term]

                # Add new rules
                if all(new_tail_1 != rule.tail for rule in cfg_copy.P[head]):
                    cfg_copy.P[head].append(ProdRule(head=head, tail=new_tail_1))

                if all(new_tail_2 != rule.tail for rule in cfg_copy.P[replc_non_term]):
                    cfg_copy.P[replc_non_term].append(ProdRule(head=replc_non_term, tail=new_tail_2))

                # Add new non terminal
                if replc_non_term not in cfg_copy.V:
                    cfg_copy.V.append(replc_non_term)

                # Add epsilon production
                if '#' not in cfg_copy.T:
                    cfg_copy.T.append('#')

                if all(['#'] != rule.tail for rule in cfg_copy.P[replc_non_term]):
                    cfg_copy.P[replc_non_term].append(ProdRule(head=replc_non_term, tail='#'))

        replc_idx += 1

    return cfg_copy


def remove_indirect_left_recursion(cfg: CFG):
    raise NotImplementedError('Indirect Left Recursion removal')

    # GPT GENERATED - DO NOT USE DIRECTLY
    # """
    # Remove indirect left recursion from a context-free grammar (CFG).
    #
    # :param cfg: The CFG object from which to remove indirect left recursion.
    # :return: A new CFG object with indirect left recursion removed.
    # """
    # # Create a copy of the original CFG
    # cfg_copy = CFG(cfg.name, copy.deepcopy(cfg.V), copy.deepcopy(cfg.T), {}, cfg.S)
    #
    # # Iterate over each non-terminal in the grammar
    # for i in range(len(cfg_copy.V)):
    #     A = cfg_copy.V[i]
    #
    #     # Check for indirect left recursion with all previous non-terminals
    #     for j in range(i):
    #         B = cfg_copy.V[j]
    #         # Check if B can lead to A
    #         if B in cfg_copy.P:
    #             for production in cfg_copy.P[B]:
    #                 if production[0] == A:  # Found indirect left recursion
    #                     # Replace productions of A that lead to B
    #                     new_productions = []
    #                     for prod in cfg_copy.P[A]:
    #                         new_productions.append(prod + production[1:])  # Append the rest of B's production
    #                     cfg_copy.P[A].extend(new_productions)
    #
    # return cfg_copy
