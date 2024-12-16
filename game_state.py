class GameState:
    '''
    Each game state has a pieces on the board and a player's turn
    '''

    def __init__(self):
        # Map spaces to stacks of pieces (since multiple pieces can be on the same space), use ndarray for faster access
        self.spaces = np.empty((4, 4), dtype=object)
        self.turn = 'white'
        self.empty = True
        self.stacks = {
            'black1', [],
            'black2', [],
            'black3', [],
            'white1', [],
            'white2', [],
            'white3', []
            'A1', [],
            'A2', [],
            'A3', [],
            'A4', [],
            'B1', [],
            'B2', [],
            'B3', [],
            'B4', [],
            'C1', [],
            'C2', [],
            'C3', [],
            'C4', [],
            'D1', [],
            'D2', [],
            'D3', [],
            'D4', []
        }

    def update_turn(self):
        # Update the turn to the next player
        self.turn = 'black' if self.turn == 'white' else 'white'


    def generate_valid_states(self):



    def get_valid_moves(self):
        # Get all valid moves for the current player
        valid_moves = []

        # If empty board, there are only 4 unique moves
        if self.empty:
            # -1 represents the piece is not on the board, L arge piece can be moved
            return [('L1', 'A1'), ('L1', 'A2'), ('L1', 'B1'), ('L1', 'B2')]

        # Otherwise we have to iterate movable pieces/board spaces


        # Iterate movable pieces and get their valid moves
        for piece in self.get_movable_pieces():
            valid_moves += piece.get_valid_moves()
        return valid_moves
