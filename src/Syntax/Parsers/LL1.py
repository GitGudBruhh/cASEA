from Grammars.CFG import CFG
from Grammars.Helpers.FirstFollow import first, follow
from Grammars.Helpers.Recursions import remove_direct_left_recursion
from Syntax.Parsers import Parser

from typing import Dict, List, Set
import string
import copy

def LL1(cfg: CFG) -> Dict:
    '''
    Takes CFG as input, computes First & Follow for all non-terminals,
    insert them in a table (a Dict) according to the LL(1) parser algorithm
    returns accumulated parse table (Dict[T, Dict[str, Set(str)]])
    '''

    '''
    Parse table will contain V (non-terminals) number of rows
    Each non-terminal(V) will have 1 row containing T(terminals)+1($) number of cells.
    Each cell will have one or more entry of production rule (in case of ambiguous grammar)
    (in class, we just used to put numbers in table, but we gotta put the production rule).
    However, adding the lhs part of production rule in table is redundant. Thus, we will just add the rhs in each cell.
    Thus, each cell must be a Set.
    '''
    # Initializing empty parse table:
    row = {sym:set() for sym in cfg.T}
    row["$"] = set()
    parse_table = {var: row for var in cfg.V} # Dict[str, Dict[str, Set]]

    first_sets = first(cfg) # Dict[str, Set[str]]
    follow_sets = follow(cfg) # Dict[str, Set[str]]

    # update the cfg itself
    remove_direct_left_recursion(cfg)
    # remove_left_factoring(cfg)

    # cfg.P: Production rules. Dict[str, List[str]]
    # code for accumulating parse table:
    for P in cfg.P.items(): # Each production rule P is of type lhs -> rhs
        lhs = P[0]
        row = parse_table[lhs]
        for rhs in P[1]:
            if rhs[0] in cfg.T:
                row[rhs[0]].add(rhs)
            else:
                epsilon_possible = False
                for terminal in first_sets[rhs[0]]:
                    row[terminal].add(rhs)
                    if terminal == '#':
                        epsilon_possible = True
                if epsilon_possible:
                    for terminal in follow_sets[lhs]:
                        row[terminal].add(rhs)

    return parse_table


# testing:
