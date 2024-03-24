# TODO: Lock board when game is over, make sure draw works. Add AI
from models.game import Game
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Create a new game and play
game = Game()

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = Game()
    return jsonify({'valid': True, 'message': f"{game.current_player.color}'s turn"})

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.get_json()
    piece_id = data.get('pieceId')
    space_id = data.get('spaceId')

    player = game.current_player

    # Check if piece and space are valid
    if piece_id not in player.pieces:
        return jsonify({'valid': False, 'message': 'Invalid piece.'})
    if space_id not in game.board.spaces:
        return jsonify({'valid': False, 'message': 'Invalid space.'})

    # Process the move
    if player.pieces[piece_id].move(space_id, game.board, game):
        game.board.print_state()
        if game.check_winner():
            # Create a new game
            game = Game()
            return jsonify({'valid': True, 'winner': player.color, 'message': f'{player.color} wins!'})

        # Switch players
        game.current_player = game.players[0] if game.current_player == game.players[1] else game.players[1]

        return jsonify({'valid': True, 'message': f"{game.current_player.color}'s turn"})

    return jsonify({'valid': False, 'message': 'Invalid move.'})

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
