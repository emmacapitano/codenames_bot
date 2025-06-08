import numpy as np
import gensim.downloader as api
wv = api.load('glove-twitter-200')

class Guesser:
    def __init__(self):
        ...
    def guess(self, word, n):
        ...


def word_similarity(word_1:str, word_2:str):
    # get the word vector indexes
    vector_1 = wv[word_1]
    vector_2 = wv[word_2]
    
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