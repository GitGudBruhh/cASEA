from Grammars.CFG import CFG
from typing import Dict, List, Set
import string
import copy
# from Grammars.Helpers.FirstFollow import first, follow #uncomment after first-follow implementation

# LL(1) parser:

def first(cfg):
    first_set = {
        "B": set(("a", "(")),
        "C": set(("d", "#")),
        "E": set(("d", "#", "b")),
        "A": set(("d", "#", "b", "a", "("))
    }
    return first_set

def follow(cfg):
    follow_set = {
        "B": set(("$")),
        "C": set(("b")),
        "E": set(("b", "a", "(")),
        "A": set(("$"))
    }
    return follow_set

def generate_new_alphabet(cfg, all_alphabets):
    remaining_alphabets = [alphabet for alphabet in all_alphabets if alphabet not in cfg.V]
    pass
def remove_left_recursion(cfg):
    all_possible_non_terminals = [x for x in string.ascii_uppercase]
    remaining_non_terminals = [alphabet for alphabet in all_possible_non_terminals if alphabet not in cfg.V]
    cfg_copy = CFG(cfg.name , copy.deepcopy(cfg.V), copy.deepcopy(cfg.T), copy.deepcopy(cfg.P), cfg.S)
    for P in cfg.P.items():
        lhs = P[0]
        replacement_alphabet = None
        for rhs in P[1]:
            if rhs[0] == lhs:
                if replacement_alphabet is None:
                    replacement_alphabet = remaining_non_terminals[0]
                    cfg_copy.V.append(replacement_alphabet)
                    cfg_copy.P[replacement_alphabet] = list()
                    remaining_non_terminals.pop(0)
                cfg_copy.P[replacement_alphabet].append(rhs[1:] + rhs[0])
                cfg_copy.P[lhs].remove(rhs)
        for rhs in P[1]:
            if rhs[0] != lhs and replacement_alphabet is not None:
                cfg_copy.P[lhs].remove(rhs)
                cfg_copy.P[lhs].append(rhs + replacement_alphabet)
    
    cfg.V = cfg_copy.V
    cfg.T = cfg_copy.T
    cfg.P = cfg_copy.P

def remove_left_factoring(cfg):
    pass


def LL1(cfg)->Dict:
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
    remove_left_recursion(cfg)
    remove_left_factoring(cfg)
    
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
