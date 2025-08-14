import numpy as np
import sys
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class GameState:
    """
    This is a class for a game that creates a word board and the user guesses words.

    Attributes:
        word_board (list of str): The words user sees and guesses from.
        assignment_board (list of str): Values of list are a mixture of ['r', 'b', 'a', 'g'].
        covered_words (list of bools): Values remain False until a word from the matching index in word_board is guessed.
        current_player (bool): A random bool that decides if red or blue team goes first.
        wv (models.word2vec): gensim model word2vec
    """


    def __init__(self, wv):
        """
        The constructor for the GameState class:
        """
        self.wv = wv
        # empty words list to put codenames wordlist in
        all_words = []
        # open file with wordlist
        with open('./codenames_words.txt') as file:
            for line in file:
                line = line.strip()
                # add each word to file
                all_words.append(line)
        self.all_words = np.array(all_words)
        
        # create a new array with 25 of the words from wordlist    
        word_board = np.array((np.random.choice(all_words, size=25, replace=False)))
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
        # when red is first word_board, there are 9 red words and 8 blue words
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

        assassin_1, assassin_2 = self.find_index(self.assignment_board, 'a')
        self.assassin_word = self.word_board[assassin_1][assassin_2]  

        # covered_words are guessed words that will not be taken into account when coming up with codenames
        self.covered_words = [False]*25
        # create 5x5 board of non-guessed words
        self.covered_words = np.resize(self.covered_words, (5,5))


    def place_card(self, guess:list) -> str:
        """
        The function to change the word_board and keep track of guessed words.

        Parameters:
            guess (str): User input of a word within word_board.

        Returns:
            ... : String that conveys the outcome of the guess to the user.
        """
        
        for g in guess:
            g_1, g_2 = self.find_index(self.word_board, g)
            self.covered_words[g_1][g_2] = True
            
        # team's turn changes
        self.current_player = not self.current_player
        return self.covered_words      


    def find_index(self, board_list:np.ndarray, word:str) -> tuple:
        """
        The function to index a nested list.
        
        Parameters:
            board_list (nested list): The word_board currently in use.
            word (str): The user input.

        Returns:
            (index_1, index_2): A tuple that represents word's location in the list.
        """
        for index_1 in range(len(board_list)):
            for index_2 in range(len(board_list[index_1])):
                if board_list[index_1][index_2] == word:
                    return (index_1, index_2)
    

    #this will move to the player class
    def view_board(self):
        color_codes = {'r':'red', 'b':'cyan', 'a':'black', 'g':'yellow'}

        fig, ax = plt.subplots(5,5, figsize=(5, 5))
        fig.subplots_adjust(hspace=0, wspace=0)

        for i in range(5):
            for j in range(5):
                ax[i, j].xaxis.set_major_locator(plt.NullLocator())
                ax[i, j].yaxis.set_major_locator(plt.NullLocator())
                word_board_str = self.word_board[i, j]
                color = self.assignment_board[i, j]
                ax[i, j].text(.5, .5, word_board_str, 
                        horizontalalignment='center', 
                        verticalalignment='center')
                if self.covered_words[i, j]:
                    ax[i, j].set_facecolor(color_codes[color])
        plt.show()

