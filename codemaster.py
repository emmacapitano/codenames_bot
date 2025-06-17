from gamestate import GameState
from guesser import Guesser
from guesser import word_similarity
import numpy as np

class Codemaster:
    """
    This is a class that creates a codeword as a hint for the guesser.
    """

    def __init__(self):
        ...
    

    def codeguy(self, gamestate:GameState, guesser:Guesser) -> str|int:
        """
        This is a function that creates the code word and tells the 
        guesser how many words they need to guess.

        Parameters:
            gamestate:
            guesser:
        
        Returns:
            codename: the code word that connects the guessable words
            n: the number of words that need guessed
        """