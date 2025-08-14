import numpy as np
from gamestate import GameState

class Guesser:
    """
    This is a class that guesses words from word board when given a codename and a number.
    """

    def __init__(self):
        ...

    def guess(self, gamestate:GameState, codename:str, n:int) -> list:
        """
        The function uses word similarity to sort the available words and choose the top n words.

        Parameters:
            gamestate: instances of GameState.
            codename (str): The codename the bot has provided.
            n (int): the number of words the bot wants the guesser to guess.
        """
        flat_wb = gamestate.word_board.flatten()
        word_dict = {}
        for word in flat_wb:
            x, y = gamestate.find_index(gamestate.word_board, word)
            if not gamestate.covered_words[x, y]:
                for w in word:
                    cosine = word_similarity(gamestate, codename, word)
                    word_dict.update({word: cosine})
        sorted_words = sorted(word_dict.keys(), key=lambda x: word_dict[x])
        guesses = sorted_words[-n:]
        gamestate.place_card(guesses)
        return guesses


def word_similarity(gamestate:GameState, word_1:str, word_2:str) -> float:
    """
    The function finds the cosine of 2 word vectors.

    Parameters:
        gamestate: instances of GameState.
        word_1 (str): The codename the bot has provided.
        word_2 (str): one of the available words in word_board.

    Returns: 
        cos (float): the cosine of the 2 word vectors.
    """
    try:
        # get the word vector indexes
        vector_1 = gamestate.wv[word_1.lower()]
        vector_2 = gamestate.wv[word_2.lower()]
    
    # word similarity model gives KeyError when it doesn't recognize word.
    except KeyError:
        return 0

    dot_product = 0
    magnitude_1 = 0
    magnitude_2 = 0
    for i in range(len(vector_1)):
        dot_product += vector_1[i] * vector_2[i]
        magnitude_1 += vector_1[i]**2
        magnitude_2 += vector_2[i]**2
    magnitude_1 = np.sqrt(magnitude_1)
    magnitude_2 = np.sqrt(magnitude_2)
    cos = dot_product / (magnitude_1 * magnitude_2)
    return cos

    

