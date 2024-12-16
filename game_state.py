class GameState:
    '''
    A class representing the game's state to be used by AI

    Attributes:
        ai_turn (int) = The AI's turn.
        empty (bool) = Represents whether or not there are pieces on the board
        board (list[list[Piece]]) = The stacks on each board space
        home_stacks (list[list[list[Piece]]]) = The stacks of player and ai's pieces OFF of the board (0 index is player, 1 is ai)
        self.movable (list[list[tuple(Piece, int)]]) = Movable pieces, index 0 is a list of player's movable pieces, index 1 is AI's movable pieces
    '''

    def __init__(self, ai_turn=0, empty=True, home_stacks=[[[],[],[]],[[],[],[]]], movable=[[],[]], board=[[],[],[],[],
                                                                                                                 [],[],[],[],
                                                                                                                 [],[],[],[],
                                                                                                                 [],[],[],[]]):
        '''
        Initializes a GameState object.
        '''
        self.ai_turn = ai_turn
        self.empty = True
        self.board = board
        self.home_stacks = home_stacks
        self.movable = movable  # TODO: Use a set for this to improve remove efficiency location == -1 = home stack 0, -2 == home stack 1, etc.


    def get_valid_moves(self):
        ''' 
        Gets all valid moves for the current player in this state.

        Returns:
            valid_moves (list[tuple(Piece, int, int)]): A list of tuples containing the piece object that can be moved and the the index of board_stacks to move to
        '''
        # Get all valid moves for the current player
        valid_moves = []

        # If empty board, there are only 4 unique moves (due to rotation/mirroring)
        if self.empty:
            valid_moves = [(-1, 0), (-1, 1), (-1, 4), (-1, 5)]
            return valid_moves

        # Otherwise we have to iterate movable pieces/board spaces
        # TODO: Optimize this by creating a unique_movable_pieces list. If there are two pieces with the same location, skip that piece (), otherwise keep track of size/location pairs already seen
        
        # Movable will be the ai movable pieces if it's the ai's turn
        movable = self.movable[self.ai_turn]
        
        for piece, curr_loc in movable:
            for target_loc, stack in enumerate(self.board):
                # Iterate stacks on the board
                if len(stack) == 0:
                    # Valid move here, it's an empty space
                    valid_moves.append((curr_loc, target_loc))
                else:
                    if stack[-1].size < piece.size:
                        # This is a valid move; stack the piece
                        valid_moves.append((curr_loc, target_loc))

        return valid_moves


    def generate_valid_states(self, valid_moves):
        '''
        Generates all valid next states based on the current state

        Parameters:
            valid_moves (list[tuples(int, int)]) = A list of possible moves represented as tuples where the first value is the current location and the second is the target 
        
        Returns:
            valid_states (list[GameState]) = A list of possible next states
        '''
        valid_states = []
        for curr_loc, target_loc in valid_moves:
            new_board = self.board.copy()
            new_movable = self.movable.copy()
            new_home_stacks = self.home_stacks.copy()
            
            # Remove current piece from its stack
            piece = new_board[curr_loc].pop() if curr_loc >= 0 else new_home_stacks[self.ai_turn][curr_loc].pop()

            # If we exposed a new piece, add it to movable
            if len(new_board[curr_loc]) > 0:
                if curr_loc >= 0:
                    exposed_piece = new_board[curr_loc][-1]
                else:
                    exposed_piece = new_home_stacks[self.ai_turn][curr_loc][-1]
                new_movable[exposed_piece.ai].append((exposed_piece, curr_loc))

            # If we covered a new piece, remove it from movable
            if len(new_board[target_loc]) > 0:
                covered_piece = new_board[target_loc][-1]
                new_movable[covered_piece.ai].remove((covered_piece, target_loc))

            # Move the piece to target location
            new_board[target_loc].append(piece)

            # Create the new game state and add to result vector
            new_state = GameState(ai_turn=int(not self.ai_turn), empty=False, home_stacks=new_home_stacks, movable=new_movable, board=new_board)
            valid_states.append(new_state)
        return valid_states