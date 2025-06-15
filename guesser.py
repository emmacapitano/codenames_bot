import numpy as np
import gensim.downloader as api
from gamestate import GameState
import sys

class Guesser:
    def __init__(self):
        ...
    def guess(self, gamestate:GameState, codename:str, n:int) -> list: 
        flat_wb = gamestate.word_board.flatten()
        word_dict = {}
        for word in flat_wb:
            x, y = gamestate.find_index(gamestate.word_board, word)
            if not gamestate.covered_words[x, y]:
                cosine = word_similarity(codename, word)
                word_dict.update({word: cosine})
        sorted_words = sorted(word_dict.keys(), key=lambda x: word_dict[x])
        guesses = sorted_words[-n:]
        for word in guesses:
            gamestate.place_card(word)
        return sorted_words

def word_similarity(gamestate:GameState, word_1:str, word_2:str):
    # get the word vector indexes
    vector_1 = gamestate.wv[word_1.lower()]
    vector_2 = gamestate.wv[word_2.lower()]
    
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

