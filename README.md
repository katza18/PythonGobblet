# PythonGobblet

# Minimax implementation
When implementing minimax with alpha-beta pruning, I started by modeling a way to represent the state space of the board game. After multiple iterations, the simplest method seemed to be to represent the board as a 3D array where there are 4 rows and 4 columns of the board and stacks for each space on the board. Then, each player (the agent and the user) needed t0 each have 2 stacks at home (where the pieces start).

Pieces were initially represented as objects of a Piece class although this proved to be unnecesssary. The best way to represent the pieces is a tuple containing the initial stack ID of the piece and the size of the piece. To simplify things, instead of adding a third value to distinguish who the piece belongs to, I use a negative integer for the size of the agents pieces. Since this needs to be absolute valued for size comparison, it may be better to alter the initial position ID of the piece for the demarcation of pieces. We also use the initial position ID for indexing, so alteration would have to occur there as well. It may be fine in the end to just add a third value to represent who the piece belongs to. 

Movable pieces are also tracked for ease of determining valid moves. Each player's movable pieces are represented in a set() for better efficiency when removing pieces from the set.

In scoring states I track many variables of the state including: pieces covering other pieces, number of pieces per player showing on the board, winning states, losing states etc. After scoring a state, it's value is used in the minimax algorithm to determine the best move. This algorithm examines all possible moves in a state tree assuming that the agent would make a move to maximize the state score on it's turns and the player would do the opposite. 

Using alpha-beta pruning allows us to ignore uneccessary states and thus traverse to a lower depth with better computational efficiency. 

To adjust the difficulty of the agent we can adjust multiple variables such as the scoring weights or the depth of the minimax traversal. 

# Where to optimize
It seems that the best place to optimize this algorithm would be in the scoring of states and in eliminating non-unique moves when reporting valid moves. The agent iterates rows and columns of the board to score the board. If the method of scoring or the representation of pieces were adjusted, the agent may be able to score in a more efficient manner that does not require iteration (using numpy). Due to mirroring and rotation, there is potential for moves that produce duplicate states. Eliminating these could lead to an even more efficient agent.  

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
