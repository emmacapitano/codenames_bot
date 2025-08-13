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
        
        if len(available_words) == 1:
            num_words = 1
            codename = get_most_similar_word(g=gamestate, word=available_words[0])
        elif len(available_words) == 2:
            ...
        else:
            ...


        # np.random returns an array, so in the return we only, want the 0th element
        return (codename, num_words)


def get_most_similar_word(g:GameState, word:str):
    # Get top 10 word similarity word tuples
    similar_words = g.uv.similar_by_word(word)
    similar_words = np.array([t[0] for t in similar_words])

    # Remove words that exist on the board
    board_words = g.word_board.flatten()
    similar_words = [w for w in similar_words if w not in board_words]

    return similar_words[0]