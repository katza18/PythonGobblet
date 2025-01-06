# PythonGobblet

# Game State Representation
Game pieces - each player has 3 large, 3 med-large, 3 med-small, 3 small
    Represent sizes numerically for simple computation (4, 3, 2, 1)

Game board - 4x4 grid

Valid moves - any piece to any open space, any piece to any space with a piece smaller than it

Invalid moves - smaller piece to space with a larger piece on it

Terminal States - 4 colors in a row

# Future considerations

It would be great to design an agent implemented with ChatGPT to allow a user to provide game instructions which will then be interpretted into a universal class representation of a game state space. The agent could then play any board game using minimax. Agent difficulty would be set based on minimax depth.

Represent various different types of board game states to see where the crossover occurs and where interpretation needs to occur.


# Structure

/templates/index.html -> html and javascript for producing
