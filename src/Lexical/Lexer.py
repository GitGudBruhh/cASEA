from typing import List

class Lexer:
    """
    An abstract class representing a Lexer.

    Attributes:
        input_string (str): The input string to be tokenized.
        tokens (List[str]): A list to store the generated tokens.
        start (int): The starting position for the current token.
        current_position (int): The current position in the input string.
    """

    def __init__(self, input_string: str):
        """
        Initializes a Lexer instance.

        :param input_string: The input string to be tokenized.
        """
        self.input_string = input_string
        self.tokens = []
        self.start = 0
        self.current_position = 0

    def tokenize(self) -> None:
        """
        Tokenizes the input string using the provided method.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_tokens(self) -> List[str]:
        """
        Returns the list of tokens generated from the input string.

        :return: A list of tokens.
        """
        return self.tokens
