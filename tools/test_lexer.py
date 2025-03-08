from typing import Dict, Set
from Automatons.DFA import DFA
from Lexical.DFALexer import DFALexer

# DFA for <regex>, <term>, <factor>
Q1 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}  # States for each character
Sigma1 = {'<', 'r', 'e', 'g', 'x', '>', 't', 'm', 'f', 'a'}  # Input alphabet
delta1 = {
    0: {'<': 1},
    1: {'r': 2, 't': 8, 'f': 10},
    2: {'e': 3},
    3: {'g': 4},
    4: {'e': 5},
    5: {'x': 16},
    8: {'e': 9},
    9: {'r': 10},
    10: {'m': 16},
    11: {'a': 12},
    12: {'c': 13},
    13: {'t': 14},
    14: {'o': 15},
    15: {'r': 16},
    16: {'>': 17},
    17: {},
}
q1 = 0  # Initial state
F1 = {17}  # Accepting states

dfa_regex = DFA(Q1, Sigma1, delta1, q1, F1, '<NON-TERMINAL>')

# DFA for * and +
Q2 = {0, 1, 2}  # States
Sigma2 = {'*', '+'}  # Input alphabet
delta2 = {
    0: {'*': 1, '+': 1},
    1: {},  # Accepting state for *
}
q2 = 0  # Initial state
F2 = {1}  # Accepting states

dfa_operators = DFA(Q2, Sigma2, delta2, q2, F2, 'OPERATOR')

# DFA for ( and )
Q3 = {0, 1, 2}  # States
Sigma3 = {'(', ')'}  # Input alphabet
delta3 = {
    0: {'(': 1, ')': 1},
    1: {},  # Accepting state for (
}
q3 = 0  # Initial state
F3 = {1}  # Accepting states

dfa_parentheses = DFA(Q3, Sigma3, delta3, q3, F3, 'PARANTHESES')

# DFA for 0 and 1
Q4 = {0, 1}  # States
Sigma4 = {'0', '1'}  # Input alphabet
delta4 = {
    0: {'0': 1, '1': 1},
    1: {},  # Accepting state for 0
}
q4 = 0  # Initial state
F4 = {1}  # Accepting states

dfa_zero_one = DFA(Q4, Sigma4, delta4, q4, F4, 'TERMINALS')






def test_lexer():
    # Create a list of DFAs
    dfas = [dfa_regex, dfa_operators, dfa_parentheses, dfa_zero_one]

    # Define multiple input strings to tokenize
    test_cases = [
        "0",                          # Single number
        "1",                          # Single number
        "0+1",                        # Simple addition
        "1+0",                        # Simple addition
        "0*1",                        # Simple multiplication
        "1*0",                        # Simple multiplication
        "(0)",                        # Parentheses with a number
        "(1)",                        # Parentheses with a number
        "0+1*1",                      # Mixed operations
        "1*(0+1)",                    # Nested operations
        "(0+1)*1",                    # Parentheses with addition
        "0*(1+0)",                    # Parentheses with multiplication
        "1+0*1",                      # Mixed operations
        "0*(1+0)+1",                  # Complex expression
        "1+(0*1)",                    # Nested operations
        "0+1+0",                      # Multiple additions
        "1*0+1",                      # Mixed operations
        "0*1+0*1",                    # Multiple multiplications
        "(0+1)*(1+0)",                # Nested parentheses
    ]

    for i, input_string in enumerate(test_cases):
        print(f"Test case {i + 1}: Input: '{input_string}'")
        lexer = DFALexer(dfas, input_string)
        try:
            lexer.tokenize()
            tokens = lexer.get_tokens()
            print("Tokens:", tokens)
        except Exception as e:
            print("Error:", e)
        print("-" * 40)

# Run the test cases
test_lexer()
