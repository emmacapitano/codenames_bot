from gamestate import GameState
from guesser import Guesser
from guesser import word_similarity
import numpy as np
from typing import Tuple
from sklearn.cluster import KMeans
from math import ceil
import re
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


class Codemaster:
    """
    This is a class that creates a codeword as a hint for the guesser.
    """

    def __init__(self):
        # Store most recent attributes for post-hoc PCA visualization
        self.last_color = None
        self.last_available_words = None # 1xn np.array of strings
        self.last_num_clusters = None # int
        self.last_mod_centroids_wv = None # last_num_clusters x gamestate.wv.vector_size np.array


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

        # 1st get all available words for the team
        color = 'r' if gamestate.current_player else 'b'
        available_words = (gamestate.assignment_board == color) * (gamestate.covered_words == False) # 5x5 np.array of bools
        available_words = gamestate.word_board[available_words] # 1xn np.array of strings
        
        # Store for post-hoc vis
        self.last_color = color
        self.last_available_words = available_words
        
        # Set the number of clusters based on number of words left
        # Practical experience influences this formula
        # For example, being able to successfully associate >= 4 words in 1 turn is unlikely
        # There is probably a smarter way to do this
        num_clusters = ceil(len(available_words) / 3)
        self.last_num_clusters = num_clusters

        # Run word vec matching algos
        if len(available_words) == 1:
            num_words = 1
            codename = get_most_similar_word(gamestate=gamestate, 
                                             word=available_words[0])
        # TODO: In future iteration, could make a elif statement
        # with more intelligent decision making at len(available_words) == 2
        else:
            cluster_idx, num_words, mod_centroids_wv = repel_word_vector(gamestate=gamestate, 
                                                                         team_color=color, 
                                                                         num_clusters = num_clusters)
            codename = get_most_similar_word(gamestate=gamestate,
                                             word=mod_centroids_wv[cluster_idx])
            self.last_mod_centroids_wv = mod_centroids_wv

        return (codename, num_words)
    
    
    def display_pca(self, gamestate:GameState):

        available_words = (gamestate.assignment_board == self.last_color) * (gamestate.covered_words == False) # 5x5 np.array of bools
        available_wv = gamestate.word_vectors[available_words] # n x g.wv.vector_size

        # Find unsupervised cluster centroids
        k_means = KMeans(n_clusters=self.last_num_clusters, 
                        random_state=0, 
                        n_init="auto").fit(available_wv)
        
        cluster_centers_wv = k_means.cluster_centers_
        cluster_ids = k_means.labels_

        # colors
        color_map = {'b': 'blue', 'r': 'red', 'a': 'black', 'g': 'yellow'}
        game_colors = [color_map[a] for a in gamestate.assignment_board.flatten()]

        # Combine all word(vec)s on board with centroid word(vec)s
        words = gamestate.word_board.flatten()
        all_word_vectors = np.resize(gamestate.word_vectors, (25, gamestate.wv.vector_size))
        added_vec_idx = all_word_vectors.shape[0] + np.arange(cluster_centers_wv.shape[0])
        all_word_vectors = np.append(all_word_vectors, cluster_centers_wv, axis=0)
        words = np.append(words, ['centroid_word: ' + get_most_similar_word(gamestate, word=w) for w in cluster_centers_wv])
        word_colors = np.append(game_colors, ['green'] * cluster_centers_wv.shape[0])
        
        if self.last_mod_centroids_wv is not None:
            # Add to word_vectors to be PCAed but pass None and 'none' to matplotlib so they are not plotted
            added_vec_new_idx = all_word_vectors.shape[0] + np.arange(self.last_mod_centroids_wv.shape[0])
            all_word_vectors = np.append(all_word_vectors, self.last_mod_centroids_wv, axis=0)
            words = np.append(words, ['adjusted_word: ' + get_most_similar_word(gamestate, word=w) for w in self.last_mod_centroids_wv])
            word_colors = np.append(word_colors, ['none'] * self.last_mod_centroids_wv.shape[0])
            # word_colors = np.append(word_colors, ['purple'] * added_vec_new.shape[0])

        twodim = PCA().fit_transform(all_word_vectors)[:,:2]
        
        plt.figure(figsize=(6,6))
        plt.scatter(twodim[:,0], twodim[:,1], color=word_colors.flatten())
        for word, (x,y) in zip(words.flatten(), twodim):
            plt.text(x+0.05, y+0.05, word)

        for (og_added_idx, new_added_idx) in zip(added_vec_idx, added_vec_new_idx):
            x, y = twodim[og_added_idx]
            x_new, y_new = twodim[new_added_idx]
            plt.arrow(x, y, x_new - x, y_new - y, length_includes_head=True, head_width=0.05)


def get_most_similar_word(gamestate:GameState, word:str | np.ndarray) -> str:
    """
    Get most similar word that exists in the gamestate.wv model
    Constrain the model's returned words such that they
        - do not contain special characters
        - do not already exist on the board
    """
    # Get top 10 word similarity word tuples
    if type(word) is str:
        similar_words = gamestate.wv.similar_by_word(word)
    else:
        similar_words = gamestate.wv.similar_by_vector(word)
    similar_words = np.array([t[0] for t in similar_words])

    # Remove words that exist on the board
    board_words = gamestate.word_board.flatten()
    similar_words = [w for w in similar_words if (w not in board_words) and (not re.search('[^A-Za-z]', w))]

    return similar_words[0]


def repel_word_vector(gamestate:GameState, team_color:str, num_clusters:int) -> Tuple[int, int, np.array]:
    """
    Calculate Coulomb repulsion forces from all-other words on KMeans centroids
    based on words available to the current team (denoted by team_color).
    Then move centroids in the direction of the calculated repulsion forces weighted by word association.

    """
    available_words = (gamestate.assignment_board == team_color) * (gamestate.covered_words == False) # 5x5 np.array of bools
    available_wv = gamestate.word_vectors[available_words] # n x g.wv.vector_size

    # Bad words are any other word
    bad_words = (gamestate.assignment_board != team_color) * (gamestate.covered_words == False) # 5x5 np.array of bools
    bad_words_assignment = gamestate.assignment_board[bad_words]
    bad_wv = gamestate.word_vectors[bad_words] # m x g.wv.vector_size
    
    # Define the weight of the "repulsive" force
    weights = {'r': 10, 'b': 10, 'a': 20, 'g': 5}

    # Find unsupervised cluster centroids
    k_means = KMeans(n_clusters=num_clusters, 
                    random_state=0, 
                    n_init="auto").fit(available_wv)
    
    cluster_centers_wv = k_means.cluster_centers_
    cluster_ids = k_means.labels_

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

    modified_centroids_wv = cluster_centers_wv + f_repulse_12

    # Get largest cluster id
    unique_elements, counts = np.unique(cluster_ids, return_counts=True)
    max_count_index = np.argmax(counts)
    largest_cluster_idx = unique_elements[max_count_index]
    largest_cluster_size = np.max(counts)

    return (largest_cluster_idx, largest_cluster_size, modified_centroids_wv)