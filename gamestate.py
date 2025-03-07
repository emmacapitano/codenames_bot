import numpy as np
import sys

class GameState:
    def __init__(self):
        '''creates a 5x5 gameboard of words and identical assignment list of a mix of ['r', 'b', 'a', 'g'].
            Picks who is going first uses that to determine who wins in the end. 
            We retreive the index of the input that will match a word within the gameboard.
            We match that index to the same index in the assignment list.
            We say that input's value, prevent it from being guessed again, and switch to next player.
            If input's assignment is 'a', gameover.'''
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

    def place_card(self, guess):
        '''Check if guess matches the intance of assassin_word.
        Find the index of the guess in the instance of word_board.
        In covered_words, change the value in that index to True...'''
        if guess == self.assassin_word and self.current_player == True:
            sys.exit("GAME OVER!\nYou hit the assassin!\nBlue Team wins!")
        elif guess == self.assassin_word and self.current_player == False:
            sys.exit("GAME OVER!\nYou hit the assassin!\nRed Team wins!")
        #find index
        g_1, g_2 = self.find_index(self.word_board, guess)
        
        #This method will say if that word red, blue, grey, or assassin
        #Use assassin_word here
        
        #attach index to covered_words
        self.covered_words[g_1][g_2] = True
        return self.covered_words      

    def find_index(self, board_list, word) -> tuple:
        '''retrieves 2x1 index of a provided word in 
            the instance of the provided nested list'''
        for index_1 in range(len(board_list)):
            for index_2 in range(len(board_list[index_1])):
                if board_list[index_1][index_2] == word:
                    return (index_1, index_2)
    


