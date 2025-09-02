# codenames_bot
Automate the 'Codenames' board-game

# Codenames Simulation Program

## Overview

This Python program simulates the popular card/board game Codenames. Two AI-controlled teams (Red and Blue) alternate turns, with one AI acting as Codemaster (giving clues) and the other as Guesser (attempting to guess the correct words on the board).

The simulation:
- Uses NumPy arrays to represent the word board, team assignments, and covered words
- Relies on word embeddings (GloVe Twitter vectors) for semantic similarity in clue generation and guessing
- Uses Matplotlib to visualize the board state after each turn

Teams take turns generating clues and guessing until:
  - All words for one team are correctly guessed (that team wins), or
  - The "assassin" word is guessed (the opposing team wins)

## Program Flow

1. **Load Word Embeddings** - Uses gensim.downloader to load the "glove-twitter-25" pre-trained embedding model
2. **Initialize Game Components**
   - `GameState` → sets up the board, assigns words to teams, tracks guesses
   - `Codemaster` → chooses clue word and number of guesses
   - `Guesser` → selects board words based on clue and similarity scores
3. **Game Loop**
   - Codemaster generates a (clue, num_words) pair
   - Guesser makes num_words guesses from available board words
   - Board is updated and displayed
   - Win/lose conditions are checked

## Dependencies

- Python 3.11.13
- gensim
- matplotlib
- numpy
- scipy

## Usage Example

Run a single game:

```bash
python simulation.py
```

### simulation()

Loads pre-trained word embeddings and simulates the entire Codenames game.

```python
simulation(wv: gensim.models.KeyedVectors, toggle_viz: bool = True) -> str
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `wv` | `gensim.models.KeyedVectors` | Word embeddings model for clue generation and guessing |
| `toggle_viz` | `bool` | Whether to display the visual board (True) or text output only (False) |

**Returns:**
- `str`: Describes the outcome of the game

---

## GameState

The GameState class manages the state of the board, turn tracking, and visualization of the game.

```python
GameState(wv: gensim.models.KeyedVectors)
```

**Parameters:**
- `wv` (`gensim.models.KeyedVectors`): Gensim Word2Vec model for generating similarity-based clues

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `word_board` | `np.ndarray[str]` | 5×5 array of visible words in the current game |
| `assignment_board` | `np.ndarray[str]` | 5×5 array of role assignments: 'r', 'b', 'g', 'a' |
| `covered_words` | `np.ndarray[bool]` | 5×5 boolean array, True if a word is guessed/covered |
| `current_player` | `bool` | True → Red's turn; False → Blue's turn |
| `all_words` | `np.ndarray[str]` | Full list of available words from the source file |
| `assassin_word` | `str` | The assassin word for the current game |
| `word_vectors` | `np.ndarray[float]` | 5x5xn-dimensional word vector tensor |
| `wv` | `gensim.models.KeyedVectors` | Pre-trained Word2Vec model used for clue generation |

### Methods

#### find_index()

Searches for a word's coordinates within a nested numpy array.

```python
find_index(board_list: np.ndarray, word: str) -> tuple[int, int]
```

**Parameters:**
- `board_list` (`np.ndarray`): Board to search (usually word_board or assignment_board)
- `word` (`str`): Word to locate

**Returns:**
- `tuple[int, int]`: (row, col) representing the position

#### place_card()

Marks guessed words as covered and switches the turn to the other team.

```python
place_card(guess: list[str]) -> np.ndarray[bool]
```

**Parameters:**
- `guess` (`list[str]`): Words guessed in the current turn

#### view_board()

Displays the current game board using matplotlib.

```python
view_board() -> None
```

---

## Codemaster

The Codemaster uses the codeguy method to create the codename and decide the words and number of words to be guessed. The codeguy method stores the most recent relevant data as instance attributes to be used by the display_pca method for post-hoc visualization.

```python
Codemaster()
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `last_color` | `str` | Most recent team color |
| `last_available_words` | `np.ndarray[str]` | Team's most recent available words |
| `last_num_clusters` | `int` | Number of kmeans clusters used for code generation |
| `last_mod_centroids_wv` | `np.ndarray[float]` | Modified kmean centroids based on most recent available words. Has shape `self.last_num_clusters x gensim.models.KeyedVectors.vector_size` |

### Methods

#### codeguy()

Generates a clue word and a guess count for the Guesser based on adjusted Kmeans clustering.

```python
codeguy(gamestate: GameState, guesser: Guesser) -> tuple[str, int]
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `gamestate` | `GameState` | The current game state, including team assignments, covered words, and master word list |
| `guesser` | `Guesser` | The Guesser instance. (Currently unused inside the method, but included for possible future integration.) |

**Returns:**
- `codename` (`str`): The chosen clue word (not on the board)
- `num_words` (`int`): Number of guesses the Guesser should make this turn

#### display_pca()

2D PCA visualization of game board- and generated clue- word embeddings.

```python
display_pca(gamestate: GameState) -> None
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `gamestate` | `GameState` | The current game state, including team assignments, covered words, and master word list |

**Returns:**
- `None`

### Functions

#### get_most_similar_word()

Returns the most similar word compared to word indexed by the GameState.wv Word2Vec model by cosine similarity.

```python
get_most_similar_word(gamestate: GameState, word: str) -> str
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `gamestate` | `GameState` | The game state instance containing the Word2Vec model |
| `word` | `str` | Word to search by |

**Returns:**
- `str`: Most similar word that does not exist on the GameState.word_board

#### repel_word_vector()

Calculate Coulomb repulsion forces from all-other words on KMeans centroids based on words available to the current team (denoted by team_color). Then move centroids in the direction of the calculated repulsion forces weighted by word association.

```python
repel_word_vector(gamestate: GameState, team_color: str, num_clusters: int) -> tuple[int, int, np.array]
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `gamestate` | `GameState` | The game state instance containing the Word2Vec model |
| `team_color` | `str` | String denoting current turn: 'r' or 'b' |
| `n_clusters` | `int` | Number of clusters |

**Returns:**
A tuple containing the following:
- `int`: Index of the output array associated with the largest cluster
- `int`: Size of the largest cluster
- `np.array`: Vectors associated with adjusted cluster kmeans centroids. Has shape `num_clusters x gensim.models.KeyedVectors.vector_size`

---

## Guesser

The Guesser is the AI player responsible for selecting words on the board based on a clue word (codename) and a number provided by the Codemaster.

```python
Guesser()
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| (none) | — | The Guesser currently has no persistent instance attributes; it operates entirely based on input arguments and the GameState object |

### Methods

#### guess()

Selects the top n most semantically similar words to the given codename from the active board.

```python
guess(gamestate: GameState, codename: str, n: int) -> list[str]
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `gamestate` | `GameState` | The current game state, providing board data, covered word tracking, and the Word2Vec model |
| `codename` | `str` | The clue word provided by the Codemaster |
| `n` | `int` | The number of words to guess this turn |

**Returns:**
- `guesses` (`list[str]`): The words chosen to guess

---

## Functions

#### word_similarity()

Computes the cosine similarity between the vector representations of two words using the wv Word2Vec model stored in the GameState.

```python
word_similarity(gamestate: GameState, word_1: str, word_2: str) -> float
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `gamestate` | `GameState` | The game state instance containing the Word2Vec model |
| `word_1` | `str` | The first word (e.g., Codemaster's clue) |
| `word_2` | `str` | The second word (e.g., a candidate board word) |

**Returns:**
- `cos` (`float`): The cosine similarity between the two word vectors. Returns 0 if either word is not recognized by the Word2Vec model