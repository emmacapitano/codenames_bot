import numpy as np

class GameState:
    def __init__(self):
        words = []
        with open('./codenames_words.txt') as file:
            for line in file:
                line = line.strip()
                words.append(line)    
        word_board = np.array((np.random.choice(words, size=25, replace=False)))
        word_board = np.resize(word_board, (5,5))
        self.word_board = word_board

gamestate = GameState()
print(gamestate.word_board)