import numpy as np
np.random.seed(7)

class GameState:
    def __init__(self):
        # empty words list to put codenames wordlist in
        words = []
        # open file with wordlist
        with open('./codenames_words.txt') as file:
            for line in file:
                line = line.strip()
                # add each word to file
                words.append(line)
        # create a new array with 25 of the words from wordlist    
        word_board = np.array((np.random.choice(words, size=25, replace=False)))
        # make array a 5x5 nested list
        word_board = np.resize(word_board, (5,5))
        # making word_board an instance attribute
        self.word_board = word_board

        # list of lables for red words, blue words, grey words, and assassin
        assignment_board = ['a'] + ['g']*7
        # find out if red is first by having a random choice of T or F
        current_player = np.random.choice([True, False], size=1)
        # red is going first when current_player == True
        current_player = current_player[0]
        # when red is first, there are 9 red words and 8 blue words
        if current_player:
            r = ['r']*9
            b = ['b']*8
        # when red isn't first, there are 8 red wrods and 9 blue words
        else:
            r = ['r']*8
            b = ['b']*9
        # add r and b to the assignment board list. We now have 25 lables in the list
        assignment_board += r + b
        # shuffle them around to get a unique gameboard
        np.random.shuffle(assignment_board)
        # order it in a 5x5 nested list
        assignment_board = np.resize(assignment_board, (5,5))
        # making assignment_board an instance attribute
        self.assignment_board = assignment_board
        self.current_player = current_player

        for word_list in range(len(word_board)):
            for word in range(len(word_board[word_list])):
                if word_board[word_list][word] == 'PIT':
                    index_word = (word_list, word)
        self.index_word = index_word