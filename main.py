# TODO: Lock board when game is over, make sure draw works
from flask import Flask, render_template, request, jsonify
from game_state import GameState

app = Flask(__name__)

# Create a new game and play
game = GameState()

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = GameState()
    return jsonify({'valid': True, 'message': f"{game.winner.capitalize()}'s turn"})

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.get_json()
    piece_id = data.get('pieceId')  # Format == 'xyz' where x is the player (0== player, 1== AI), y is the homestack number, z is the piece size (1-4)
    space_id = data.get('spaceId')  # Format == 'xy' where x is the row, y is the column
    depth = data.get('depth')  # Depth for the AI to search

    if piece_id[0] == '1':
        # User trying to move AI piece
        return jsonify({'valid': False, 'message': 'Invalid piece. Please move a white piece.', 'winner': game.winner})

    # Convert the string to a tuple
    piece_id = (int(piece_id[1]), int(piece_id[2]))
    space_id = (int(space_id[0]), int(space_id[1]))

    # Check if piece is movable
    if not game.is_movable(piece_id):
        return jsonify({'valid': False, 'message': 'Piece is not movable.', 'winner': game.winner})

    # Process the move
    if game.make_move(piece_id, space_id):
        if game.check_winner():
            # Create a new game
            message = jsonify({'valid': True, 'winner': game.winner, 'message': f'{game.winner.capitalize()} wins!'})
            game = GameState()
            return message

        # AI move
        (aiPiece, aiTargetLocation) = game.ai_move(depth=depth)

        if game.check_winner():
            # Create a new game
            message = jsonify({'valid': True, 'winner': game.winner, 'message': f'{game.winner.capitalize()} wins!'})
            game = GameState()
            return message

        return jsonify({'valid': True, 'message': f"", 'aiPiece': aiPiece, 'aiTargetLocation': aiTargetLocation, 'winner': game.winner})

    return jsonify({'valid': False, 'message': 'Invalid move.'})


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
