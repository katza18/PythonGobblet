import pickle
from models.game import Game
from models.ai import AI
import os

def move(piece_id, space_id):
    player = game.current_player

    # Check if piece and space are valid
    if piece_id not in player.pieces:
        print('Invalid piece.')
        return False
    if space_id not in game.board.spaces:
        print('Invalid space.')
        return False

    # Process the move
    if player.pieces[piece_id].move(space_id, game.board, game):
        game.board.print_state()
        if game.check_winner():
            # Create a new game
            game = Game()
            print(f'{player.color.capitalize()} wins!')
            return True

        # Switch players
        game.current_player = game.players[0] if game.current_player == game.players[1] else game.players[1]

        print(f"{game.current_player.color.capitalize()}'s turn")
        return True

    print('Invalid move.')
    return False

# Set whether to use supervised or self-play learning
supervised = True

# Create a new game and two AIs
game = Game()

# Load the AI (CHANGE THIS IF YOU WANT TO CREATE A NEW ONE)
if os.path.exists('ai1.pkl'):
    with open('ai1.pkl', 'rb') as f:
        ai1 = pickle.load(f)
else:
    ai1 = AI()
if not supervised:
    if os.path.exists('ai2.pkl'):
        with open('ai2.pkl', 'rb') as f:
            ai2 = pickle.load(f)
    else:
        ai2 = AI()

# Train the AI
if not supervised:
    for i in range(10000):  # Play 10,000 games
        while not game.is_over():
            # Get the current game state
            state = game.get_state()

            # Let the AI choose an action
            current_ai = ai1 if game.current_player.color == 'white' else ai2
            action = current_ai.choose_action(state)

            # Perform the action and get the reward
            reward = game.perform_action(action)

            # Get the new game state
            new_state = game.get_state()

            # Let the AI learn from the action
            ai.learn(state, action, reward, new_state)

        # Reset the game
        game = Game()
else:
    # Run a single game against the user
    game = Game()

    # Will need to rewrite a play method for this. It should prompt the user if player is white (user) and it should prompt the AI if they are black




# Store the AI (CHANGE THIS IF YOU WANT TO CREATE A NEW ONE)
with open('ai1.pkl', 'wb') as f:
    pickle.dump(ai1, f)
with open('ai2.pkl', 'wb') as f:
    pickle.dump(ai2, f)
