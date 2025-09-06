# codenames_bot
Automate the 'Codenames' board-game

# Methods Paper
Please find detailed background and methods [here](https://docs.google.com/document/d/1Cqr0T-8HbaiBTdXBj7pRB2QCOx-cvMroH8v5ULgt0gs/edit?usp=sharing).

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

