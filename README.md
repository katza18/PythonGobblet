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


# Structure

/templates/index.html -> html and javascript for producing


# TODO
1. Implement check_winner and improve state scoring, make game reset properly, add winner animation, add reset button



## REMOVED CODE:
function selectPiece(event, pieceId) {
    // TODO: Clean this up. We can make the size numeric and do a simple comparison
    event.stopPropagation();

    // Deselect any selected pieces
    var selectedPieces = document.getElementsByClassName('selected');

    // Check if another piece is selected and then check if that piece is smaller so it can be gobbled
    if (selectedPieces.length > 0 && selectedPieces[0].id != pieceId) {
        var selectedPiece = selectedPieces[0];
        var selectedPieceSize = selectedPiece.classList[1];
        var pieceToGobbleSize = document.getElementById(pieceId).classList[1];
        if (selectedPieceSize == 's-circle') {
            // Cannot gobble anything, do nothing OR select the new piece and clear selectedPieces
            return;
        }
        else if (selectedPieceSize == 'm-circle') {
            if (pieceToGobbleSize == 's-circle') {
                // This piece can be gobbled: Remove selected pieces, get the spaceID from piece to gobble, make the move, and return
                spaceId = document.getElementById(pieceId).parentElement.id;
                movePiece(spaceId);
                return;
            } else {
                // This piece cannot be gobbled
                return;
            }
        }
        else if (selectedPieceSize == 'l-circle') {
            if (pieceToGobbleSize == 's-circle' || pieceToGobbleSize == 'm-circle') {
                // This piece can be gobbled
                spaceId = document.getElementById(pieceId).parentElement.id;
                movePiece(spaceId);
                return;
            } else {
                // This piece cannot be gobbled
                return;
            }
        }
        else {
            if (pieceToGobbleSize != 'xl-circle') {
                // This piece can be gobbled
                spaceId = document.getElementById(pieceId).parentElement.id;
                movePiece(spaceId);
                return;
            } else {
                // This piece cannot be gobbled
                return;
            }
        }
    } else {
        // Select the new piece
        var piece = document.getElementById(pieceId);
        piece.classList.add('selected');
    }
}



// THIS GETS HANDLED IN BACKEND AFTER EVERY MOVE
        // function makeAIMove() {
        //     fetch('/ai-move', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json',
        //         }
        //     })
        //     .then(response => response.json())
        //     .then(data => {
        //         // Set message div text
        //         var messageDiv = document.getElementById('message');
        //         messageDiv.innerText = data.message;

        //         if (data.valid) {
        //             // Move the piece returned in data
        //             var targetSpace = document.getElementById(data.spaceId);
        //             var previousSpace = document.getElementById(data.previousSpaceId);
        //             var piece = previousSpace.lastChild; // Get the piece to move from the top of the stack
        //             targetSpace.appendChild(piece); // Move piece to target space
        //             previousSpace.removeChild(piece); // Remove selected piece from previous space
        //         }

        //         if (data.winner) {

        //         }
        //     });
        // }


<style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 95vh;
        }

        .gamespace {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .board {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(4, 1fr);
            gap: 10px;
            width: 400px;
            height: 400px;
            padding: 10px;
        }

        .white-circle.selected {
            border: solid 2px red;
        }
        .white-circle {
            background-color: white;
            border-radius: 50%;
            border: solid 1px black;
        }



        .black-circle {
            background-color: black;
            border-radius: 50%;
        }

        .tan-space > .white-circle, .tan-space > .black-circle {
            position: absolute;
        }

        .xl-circle {
            width: 80px;
            height: 80px;
            z-index: 4;
        }

        .l-circle {
            width: 70px;
            height: 70px;
            z-index: 3;
        }

        .m-circle {
            width: 60px;
            height: 60px;
            z-index: 2;
        }

        .s-circle {
            width: 50px;
            height: 50px;
            z-index: 1;
        }

        .tan-space {
            background-color: tan;
            border: solid 1px black;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .home-space {
            display: grid;
            grid-template: 1fr / 1fr;
            place-items: center;
        }

        .home-space > * {
            grid-column: 1 / 1;
            grid-row: 1 / 1;
        }
    </style>








    body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #2b5876, #4e4376);
    color: white;
    text-align: center;
    margin: 0;
    padding: 20px;
}

h1#message {
    font-size: 2rem;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

button {
    font-size: 1rem;
    padding: 10px 20px;
    background: #ff6f61;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}

button:hover {
    transform: scale(1.1);
    box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.4);
}

.gamespace {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 20px;
    gap: 20px;
}

.white-side, .black-space {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.home-space {
    display: grid;
    grid-template: 1fr / 1fr;
    place-items: center;
    background: rgba(255, 255, 255, 0.2);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
}

.home-space > * {
    grid-column: 1 / 1;
    grid-row: 1 / 1;
}

.board {
    display: grid;
    grid-template-columns: repeat(4, 60px);
    grid-template-rows: repeat(4, 60px);
    gap: 10px;
    background: rgba(255, 255, 255, 0.2);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
}

.tan-space {
    width: 60px;
    height: 60px;
    background: #deb887;
    border-radius: 5px;
    box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.tan-space:hover {
    transform: scale(1.1);
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
}

.tan-space > .white-circle, .tan-space > .black-circle {
    position: absolute;
}

.white-circle, .black-circle {
    border-radius: 50%;
    margin: auto;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.white-circle {
    background: radial-gradient(circle, #ffffff, #dddddd);
}

.black-circle {
    background: radial-gradient(circle, #000000, #333333);
}

.xl-circle {
    width: 50px;
    height: 50px;
    z-index: 4;
}

.l-circle {
    width: 40px;
    height: 40px;
    z-index: 3;
}

.m-circle {
    width: 30px;
    height: 30px;
    z-index: 2;
}

.s-circle {
    width: 20px;
    height: 20px;
    z-index: 1;
}

.white-circle:hover {
    transform: scale(1.2);
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4);
}

.white-circle.selected {
    border: solid 2px red;
}

.white-side, .black-space {
    flex-basis: 20%;
    padding: 10px;
}
