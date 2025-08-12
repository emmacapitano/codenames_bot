from gamestate import GameState
from guesser import Guesser
from guesser import word_similarity
import numpy as np
from typing import Tuple

class Codemaster:
    """
    This is a class that creates a codeword as a hint for the guesser.
    """

    def __init__(self):
        ...
    

    def codeguy(self, gamestate:GameState, guesser:Guesser) -> Tuple[str, int]:
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

        color = 'r' if gamestate.current_player else 'b'
        available_words = (gamestate.assignment_board == color) * (gamestate.covered_words == False) # 5x5 np.array of bools
        available_words = gamestate.word_board[available_words] # 1xn np.array of strings
        
        if len(available_words) <= 3:
            num_words = len(available_words)
        else:
            num_words = np.random.randint(1, 3)
            chosen_words = np.array((np.random.choice(available_words, size=num_words, replace=False)))

        all_words_minus_board = []
        for word in gamestate.all_words:
            if word not in gamestate.word_board:
                all_words_minus_board.append(word)

        codename = np.random.choice(all_words_minus_board, size=1, replace=False)

        # np.random returns an array, so in the return we only, want the 0th element
        return (codename[0], num_words)
