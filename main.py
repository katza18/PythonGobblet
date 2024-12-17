# TODO: Lock board when game is over, make sure draw works. Add AI
from models.game import Game
from flask import Flask, render_template, request, jsonify
from game_state import GameState
from minimax import TreeNode

app = Flask(__name__)

# Create a new game and play
game = Game()

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = Game()
    return jsonify({'valid': True, 'message': f"{game.current_player.color.capitalize()}'s turn"})

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.get_json()
    piece_id = data.get('pieceId')
    space_id = data.get('spaceId')

    # TODO: PASS THIS FROM THE FRONT END
    ai_mode = data.get('ai_mode')
    depth = data.get('difficulty')

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
            return jsonify({'valid': True, 'winner': player.color, 'message': f'{player.color.capitalize()} wins!'})

        # Switch players
        game.current_player = game.players[0] if game.current_player == game.players[1] else game.players[1]

        # Return here if a multiplayer game
        if not ai_mode:
            return jsonify({'valid': True, 'message': f"{game.current_player.color.capitalize()}'s turn"})

        # If this is against AI, represent the state correctly and run minimax
        # TODO: fill in GameState constructor
        curr_state = GameState()

        # Create minimax Tree from curr_state with children as valid_states
        # TODO: We shouldn't use state in the tree, we should use move to get to the state, somehow we need to know what move to make
        mm_root = TreeNode(state=curr_state, move=None)

        # Build the tree of states, score the last depth level. Propogate the scores back up. Other scores shouldn't matter, so we won't compute them?
        value = mm_root.alpha_beta(depth=depth, alpha=float('-inf'), beta=float('inf'), agent=True)

        # Get the best move according to the returned value
        best_move = mm_root.get_best_move()

        # Have the agent make the move

    return jsonify({'valid': False, 'message': 'Invalid move.'})

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
