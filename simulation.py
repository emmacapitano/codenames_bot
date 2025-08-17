from gamestate import GameState
from guesser import Guesser
from codemaster import Codemaster
import gensim.downloader as api


def simulation(wv, toggle_viz:bool=True):

    gamestate = GameState(wv=wv)
    guesser = Guesser()
    codemaster = Codemaster()

    game = True

    while game:

        codename, num_words = codemaster.codeguy(gamestate=gamestate, guesser=guesser)
        codemaster.display_pca(gamestate=gamestate)

        print(f'{codename}, {num_words}')

        guesses = guesser.guess(gamestate=gamestate, codename=codename, n=num_words)
        
        print(guesses)

        if toggle_viz:
            gamestate.view_board()
        else:
            print(gamestate.assignment_board)

        red_words = (gamestate.assignment_board == 'r') * (gamestate.covered_words == False)
        red_words = gamestate.word_board[red_words]

        blue_words = (gamestate.assignment_board == 'b') * (gamestate.covered_words == False)
        blue_words = gamestate.word_board[blue_words]

        if len(red_words) == 0:
            game = False
            return("Red Team wins!")
        elif len(blue_words) == 0:
            game = False
            return("blue Team wins!")
        elif gamestate.assassin_word in guesses and gamestate.current_player == True:
            game = False
            return("GAME OVER!\nYou hit the assassin!\nBlue Team wins!")
        elif gamestate.assassin_word in guesses and gamestate.current_player == False:
            game = False
            return("GAME OVER!\nYou hit the assassin!\nRed Team wins!")
        

def main():
    wv = api.load('glove-twitter-25')
    print(simulation(wv))


if __name__ == "__main__":
    main()


