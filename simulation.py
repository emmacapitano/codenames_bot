from gamestate import GameState
from guesser import Guesser
from codemaster import Codemaster


def main():
    gamestate = GameState()
    guesser = Guesser()
    codemaster = Codemaster()

    game = True

    while game:

        codename, num_words = codemaster.codeguy(gamestate=gamestate, guesser=guesser)

        print(f'{codename}, {num_words}')

        guesses = guesser.guess(gamestate=gamestate, codename=codename, n=num_words)
        
        print(guesses)

        gamestate.view_board()

        red_words = (gamestate.assignment_board == 'r') * (gamestate.covered_words == False)
        red_words = gamestate.word_board[red_words]

        blue_words = (gamestate.assignment_board == 'b') * (gamestate.covered_words == False)
        blue_words = gamestate.word_board[blue_words]

        if len(red_words) == 0:
            game = False
            print("Red Team wins!")
        elif len(blue_words) == 0:
            game = False
            print("blue Team wins!")
        elif gamestate.assassin_word in guesses and gamestate.current_player == True:
            game = False
            print("GAME OVER!\nYou hit the assassin!\nBlue Team wins!")
        elif gamestate.assassin_word in guesses and gamestate.current_player == False:
            game = False
            print("GAME OVER!\nYou hit the assassin!\nRed Team wins!")

if __name__ == "__main__":
    main()



