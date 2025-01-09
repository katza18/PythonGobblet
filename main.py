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
    piece_id = data.get('pieceId')
    space_id = data.get('spaceId')
    depth = 4

    # TODO: PASS THIS FROM THE FRONT END
    # depth = data.get('difficulty')
    piece_id = (int(piece_id[1]), int(piece_id[2]))
    space_id = (int(space_id[0]), int(space_id[1]))

    # Check if piece is movable
    if not game.is_movable(piece_id):
        return jsonify({'valid': False, 'message': 'Invalid piece.'})

    # Process the move
    if game.make_move(piece_id, space_id):
        if game.check_winner():
            # Create a new game
            message = jsonify({'valid': True, 'winner': game.winner, 'message': f'{game.winner.capitalize()} wins!'})
            game = GameState()
            return message

    return jsonify({'valid': False, 'message': 'Invalid move.'})


@app.route('/ai-move', methods=['POST'])
def move_ai():
    global game
    move = game.ai_move(depth=3)
    return jsonify({'spaceId': move[1], 'previousSpaceId': move[2], 'winner': game.winner})


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
