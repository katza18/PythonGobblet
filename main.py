# TODO: Lock board when game is over, make sure draw works
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from game_state import GameState
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def get_game_state():
    if 'game' in session:
        return pickle.loads(session['game'])
    else:
        return GameState()

def save_game_state(game):
    session['game'] = pickle.dumps(game)

@app.route('/reset', methods=['POST'])
def reset():
    game = GameState()
    save_game_state(game)
    return jsonify({'valid': True, 'message': f"{game.winner.capitalize()}'s turn"})

@app.route('/move', methods=['POST'])
def move():
    game = get_game_state()
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
            save_game_state(game)
            message = jsonify({'valid': True, 'winner': game.winner, 'message': f'{game.winner.capitalize()} wins!'})
            return message

        # AI move
        (aiPiece, aiTargetLocation) = game.ai_move(depth=depth)

        save_game_state(game)

        if game.check_winner():
            # Create a new game
            message = jsonify({'valid': True, 'winner': game.winner, 'message': f'{game.winner.capitalize()} wins!'})
            return message

        return jsonify({'valid': True, 'message': f"", 'aiPiece': aiPiece, 'aiTargetLocation': aiTargetLocation, 'winner': game.winner})

    return jsonify({'valid': False, 'message': 'Invalid move.'})


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
