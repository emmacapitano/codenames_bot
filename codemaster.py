from gamestate import GameState
from guesser import Guesser
from guesser import word_similarity
import numpy as np
from typing import Tuple
from sklearn.cluster import KMeans


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
            # When 2 words are left, be conservative
            # If the 2 words are closer to each other than all other team's 
            ...

        else:
            ...


        # np.random returns an array, so in the return we only, want the 0th element
        return (codename, num_words)


def get_most_similar_word(gamestate:GameState, word:str) -> str:
    # Get top 10 word similarity word tuples
    similar_words = gamestate.wv.similar_by_word(word)
    similar_words = np.array([t[0] for t in similar_words])

    # Remove words that exist on the board
    board_words = gamestate.word_board.flatten()
    similar_words = [w for w in similar_words if w not in board_words]

    return similar_words[0]


def get_cluster_centroids(word_vectors:np.array, n_clusters=4) -> np.array:
    """
    Uses K-means to find centroids of unsupervised clusters
    """
    k_means = KMeans(n_clusters=n_clusters, 
                    random_state=0, 
                    n_init="auto").fit(word_vectors)
    
    return(k_means.cluster_centers_)


def repel_word_vector(g:GameState, team_color:str, num_clusters:int):
    """
    Moves word vectors further away other team's word vectors
    Inspired by Coulomb's law to "repel" away from undesirable words
    """
    available_words = (g.assignment_board == team_color) * (g.covered_words == False) # 5x5 np.array of bools
    available_wv = g.word_vectors[available_words] # n x g.wv.vector_size
    
    # Bad words are any other word
    bad_words = (g.assignment_board != team_color) * (g.covered_words == False) # 5x5 np.array of bools
    bad_words_assignment = g.assignment_board[bad_words]
    bad_wv = g.word_vectors[bad_words] # m x g.wv.vector_size
    
    # Define the weight of the "repulsive" force
    weights = {'r': 10, 'b': 10, 'a': 20, 'g': 5}

    # Find unsupervised cluster centroids
    cluster_centers_wv = get_cluster_centroids(word_vectors=available_wv, 
                          n_clusters=num_clusters)

    # Calculate the Coulomb repulsion forces from the bad words on the available words
    # Weight the repulsive force by weights
    f_repulse_12 = []
    for r_2_i, bwa in zip(bad_wv, bad_words_assignment):
        q = weights[bwa] # int
        r_12 = cluster_centers_wv - r_2_i # num_clusters x 25
        mag_repulse = np.linalg.norm(r_12, axis=1) 
        mag_repulse = np.resize(mag_repulse, (mag_repulse.shape[0], 1)) # 25 x 1
        repulse =  q * r_12 / (mag_repulse ** 3) # num_clusters x 25
        f_repulse_12.append(repulse)
    
    f_repulse_12 = np.array(f_repulse_12) # num_other_ix x num_clusters x 25
    f_repulse_12 = np.sum(f_repulse_12, axis=0) / f_repulse_12.shape[0] # num_clusters x 25

    return cluster_centers_wv + f_repulse_12