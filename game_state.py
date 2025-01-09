import numpy as np

class GameState:
    '''
    A class representing the game's state to be used by AI

    * NOTE: Pieces should be represented as an int in the range [-4,4] this will allow us to distinguish teams, do simple heuristic math, and save memory, use absolute difference for size comparison

    Attributes:
        ai_turn (int) = The AI's turn.
        empty (bool) = Represents whether or not there are pieces on the board
        board (list[list[Piece]]) = The stacks on each board space
        home_stacks (list[list[list[Piece]]]) = The stacks of player and ai's pieces OFF of the board (0 index is player, 1 is ai)
        self.movable (list[set[tuple(Piece, int)]]) = Movable pieces, index 0 is a list of player's movable pieces, index 1 is AI's movable pieces; use a set for .remove() efficiency
    '''

    def __init__(self,
                 ai_turn=0,
                 empty=True,
                 home_stacks= [[[(1,1),(1,2),(1,3),(1,4)],[(2,1),(2,2),(2,3),(2,4)],[(3,1),(3,2),(3,3),(3,4)]],
                               [[(1,-1),(1,-2),(1,-3),(1,-4)],[(2,-1),(2,-2),(2,-3),(2,-4)],[(3,-1),(3,-2),(3,-3),(3,-4)]]],
                 movable=[set([(1,4),(2,4),(3,4)]),set([(1,-4),(2,-4),(3,-4)])],
                 board=[[[],[],[],[]],
                        [[],[],[],[]],
                        [[],[],[],[]],
                        [[],[],[],[]]]):
        '''
        Initializes a GameState object.
        '''
        self.ai_turn = ai_turn
        self.empty = empty
        self.board = np.array(board)
        self.home_stacks = home_stacks
        self.winner = ''
        self.movable = movable  # Use a set for this to improve remove efficiency location == -1 = home stack 0, -2 == home stack 1, etc.

        # Initialize movable pieces

    def is_movable(self, piece):
        print(self.movable[self.ai_turn])
        print(piece)
        if piece in self.movable[self.ai_turn]:
            return True


    def __get_valid_moves(self):
        '''
        Gets all valid moves for the current player in this state. Private function. Meant to be used by AI agent.

        Returns:
            valid_moves (list[tuple(int, int)]): A list of tuples containing the location to move from and to (1D index of the board)
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
            piece_size = abs(piece[1])
            for r, row in enumerate(self.board):
                for c, stack in enumerate(row):
                    target_loc = (r, c)
                    if len(stack) == 0:
                        # Valid move here, it's an empty space
                        valid_moves.append((curr_loc, target_loc))
                    else:
                        target_piece_size = abs(stack[-1][1])
                        if target_piece_size < piece_size:
                            # This is a valid move; stack the piece
                            valid_moves.append((curr_loc, target_loc))

        return valid_moves


    def generate_valid_states(self):
        '''
        Generates all valid next states based on the current state. Meant to be used by AI agent.

        Returns:
            valid_states (list[GameState]) = A list of possible next states
        '''

        valid_states = []
        valid_moves = self.__get_valid_moves()
        for curr_loc, target_loc in valid_moves:
            new_board = self.board.copy()
            new_movable = self.movable.copy()
            new_home_stacks = self.home_stacks.copy()

            # Remove current piece from its stack
            home = type(curr_loc) is not tuple
            piece = new_board[curr_loc[0], curr_loc[1]].pop() if not home else new_home_stacks[self.ai_turn][curr_loc].pop()

            # TODO: Clean this up
            # If we exposed a new piece, add it to movable
            if not home:
                if len(new_board[curr_loc]) > 0:
                    exposed_piece = new_board[curr_loc][-1]
                    exposed_piece_is_agent = int(exposed_piece[1] < 0)
                    new_movable[exposed_piece_is_agent].add((exposed_piece, curr_loc))
            else:
                if len(new_home_stacks[self.ai_turn][curr_loc]) > 0:
                    exposed_piece = new_home_stacks[self.ai_turn][curr_loc][-1]
                    exposed_piece_is_agent = int(exposed_piece[1] < 0)
                    new_movable[exposed_piece_is_agent].add((exposed_piece, curr_loc))

            # If we covered a new piece, remove it from movable
            if len(new_board[target_loc]) > 0:
                covered_piece = new_board[target_loc][-1]
                covered_piece_is_agent = int(covered_piece[1] < 0)
                new_movable[covered_piece_is_agent].remove((covered_piece, target_loc))

            # Move the piece to target location
            print(target_loc)
            np.append(new_board[target_loc[0], target_loc[1]], piece)

            # Update movable
            piece_is_agent = int(piece[1] < 0)
            new_movable[piece_is_agent].remove((piece, curr_loc))
            new_movable[piece_is_agent].add((piece, target_loc))

            # Create the new game state and add to result vector
            new_state = GameState(ai_turn=int(not self.ai_turn), empty=False, home_stacks=new_home_stacks, movable=new_movable, board=new_board)
            valid_states.append(new_state)
        return valid_states


    def __heuristic_func(win=0, loss=0, own_pieces=0, opp_pieces=0, own_4_on_1=0, own_4_on_2=0, own_4_on_3=0, own_3_on_1=0, own_3_on_2=0, own_2_on_1=0, opp_covers=0):
        '''
        Heuristic function for scoring rows/cols/diagonals of a state. Private Function.
        '''
        # Input just a win/loss to terminate scoring early
        # Adjust scores for agent difficulty
        own_pieces_weight = 1  # Should really only consider pieces at the top of a stack
        opp_pieces_weight = -1
        own_3s_weight = 10  # Added weight for 3 pieces in row/col/diag
        opp_3s_weight = -10
        own_2s_weight = 5 # Added weight for 2 pieces in row/col/diag
        opp_2s_weight = -5
        win_weight = 1000
        loss_weight = -1000
        own_4_on_1_weight = 2
        own_4_on_2_weight = 3
        own_4_on_3_weight = 4  # Encourage the agent to cover pieces one size smaller
        own_3_on_1_weight = 3
        own_3_on_2_weight = 4
        own_2_on_1_weight = 4
        opp_covers_weight = 3  # Opponent covering one of your pieces (equally bad?)
        own_controlled_weight = 10  # Fully controlled rows/cols/diags (no piece of the opposite color); this has beginning of game implications
        opp_controlled_weight = 10  # Fully controlled by opp
        # Consider rewarding: blocking, movable pieces,

        # Compute derivables
        own_3s, opp_3s = int(own_pieces == 3), int(opp_pieces == 3)
        own_2s, opp_2s = int(own_pieces == 2), int(opp_pieces == 2)
        own_controlled, opp_controlled = int(opp_pieces == 0 and own_pieces > 0), int(own_pieces == 0 and opp_pieces > 0)

        return win * win_weight + loss * loss_weight + own_pieces * own_pieces_weight + opp_pieces * opp_pieces_weight + own_3s_weight * own_3s + own_2s_weight * own_2s + own_4_on_1_weight * own_4_on_1 + own_4_on_2_weight * own_4_on_2 + own_4_on_3_weight * own_4_on_3 + own_3_on_1_weight * own_3_on_1 + own_3_on_2_weight * own_3_on_2 + own_2_on_1_weight * own_2_on_1 + own_controlled_weight * own_controlled + opp_3s_weight * opp_3s + opp_2s_weight * opp_2s + opp_covers_weight * opp_covers + opp_controlled_weight * opp_controlled


    def __score_row_col_diag(self, rcd):
        '''
        Computes the score for a row/col/diagonal of the board. Private Function.

        Parameters:
            rcd (list[list[tuple(int,int)]]) = A row/col/diagonal from the board containing pieces

        Returns:
            score (int) = Score for the row/col/diagonal
        '''
        own_pieces = 0
        opp_pieces = 0
        own_4_on_3 = 0
        own_4_on_2 = 0
        own_4_on_1 = 0
        own_3_on_2 = 0
        own_3_on_1 = 0
        own_2_on_1 = 0
        opp_covers = 0
        for stack in rcd:
            own = 0  # Flag designating whether this is the Agent's piece
            if len(stack) > 0:
                if stack[-1][1] < 0:
                    # It's an AI piece
                    own_pieces += 1
                    own = 1
                else:
                    opp_pieces += 1

            if len(stack) > 1:
                if own:
                    player_size, agent_size = stack[-2][1], stack[-1][1]
                    if player_size > 0:
                        # Agent's pieces is on a player's piece, Subtract the player piece size from the ai piece size
                        size_diff = abs(agent_size) - player_size
                        if size_diff == 1:
                            if agent_size == 4:
                                own_4_on_3 += 1
                            elif agent_size == 3:
                                own_3_on_2 += 1
                            else:
                                own_2_on_1 += 1
                        elif size_diff == 2:
                            if agent_size == 4:
                                own_4_on_2 += 1
                            else:
                                own_3_on_1 += 1
                        else:
                            own_4_on_1 += 1
                else:
                    # Player's piece is stacked
                    player_size, agent_size = stack[-1][1], stack[-2][1]
                    if agent_size < 0:
                        # Player piece covering an agent's piece
                        opp_covers += 1

        return self.__heuristic_func(win=(own_pieces == 4), loss=(opp_pieces == 4), own_pieces=own_pieces, opp_pieces=opp_pieces, own_4_on_3=own_4_on_3, own_4_on_2=own_4_on_2, own_4_on_1=own_4_on_1, own_3_on_2=own_3_on_2, own_3_on_1=own_3_on_1, own_2_on_1=own_2_on_1, opp_covers=opp_covers)


    def score_board(self):
        '''
        Scores a board for minimax algorithm.

        Returns:
            score (int) = A board's score
        '''

        '''
        Need to score both offensive and defensive moves

        +1: Covering the other player's piece that's 3 sizes smaller
        +2: Covering the other player's piece that's 2 sizes smaller
        +3: Covering the other player's piece that's 1 size smaller; it's generally best not to waste a piece by covering it wrong

        +1: Placing one piece in an empty row
        +1: Placing one piece in an empty col
        +1: Placing one piece in an empty diagonal

        +2: Placing a piece in a row/col/diag with 1 other of the same color
        +3: Placing a piece in a row/col/diag with 2 other of the same color

        +1: Placing one piece in a row/col/diag with the opponent's piece in it

        -100: Allowing the opponent to complete a row/col/diag
        +100: Completing a row/col/diag

        Heuristic Function = +inf * win + -inf * loss + w1 * 3 in a rows + w2 * 2 in a rows + w3 * 1 in a rows + w4 * opp 3 in a rows + w5 * opp 2 in a rows + w6 * opp 1 in a rows + w7 * covering pieces + w8 * opp covering pieces + w9 * controlled rows/cols/diags + w10 * opp controlled rows/cols/diags

        Strategically the best scenario to be in beside a win is a 2 + 2 where we can place 1 large piece to get two threes in a row

        Need to weight larger pieces higher since they can't be captured? Maybe not since future states should account for that
            Likely shouldn't do this because it isn't always best to put the largest pieces down first, use other weights to account for this in future states
        '''

        total = 0

        for row in self.board:
            # NOTE: We may just want to compute coverings based on the most recently moved piece
            total += self.__score_row_col_diag(row)

        for col in self.board.T:
            # calculate score of that col and add to total
            total += self.__score_row_col_diag(col)

        # Compute diagonals
        total += self.__score_row_col_diag(np.diagonal(self.board))
        total += self.__score_row_col_diag(np.diagonal(np.fliplr(self.board)))

        return total


    def make_move(self, piece, target_loc):
        '''
        Makes a move for the current player.

        Parameters:
            piece (tuple): The piece to move.
            target_loc (tuple): The target location to move the piece to.

        Returns:
            bool: True if the move was successful, False otherwise.
        '''
        # TODO: curr_loc is set incorrectly
        curr_loc = None
        for loc, stack in np.ndenumerate(self.board):
            if piece in stack:
                curr_loc = loc
                break
        if curr_loc is None:
            for i, stack in enumerate(self.home_stacks[self.ai_turn]):
                if piece in stack:
                    curr_loc = i
                    break
        if curr_loc is None:
            return False

        new_board = self.board.copy()
        new_movable = self.movable.copy()
        new_home_stacks = self.home_stacks.copy()

        # Remove current piece from its stack
        home = type(curr_loc) is not tuple
        piece = new_board[curr_loc[0], curr_loc[1]].pop() if not home else new_home_stacks[self.ai_turn][curr_loc].pop()

        # If we exposed a new piece, add it to movable
        if not home:
            if len(new_board[curr_loc]) > 0:
                exposed_piece = new_board[curr_loc][-1]
                exposed_piece_is_agent = int(exposed_piece[1] < 0)
                new_movable[exposed_piece_is_agent].add((exposed_piece, curr_loc))
        else:
            if len(new_home_stacks[self.ai_turn][curr_loc]) > 0:
                exposed_piece = new_home_stacks[self.ai_turn][curr_loc][-1]
                exposed_piece_is_agent = int(exposed_piece[1] < 0)
                new_movable[exposed_piece_is_agent].add((exposed_piece, curr_loc))

        # If we covered a new piece, remove it from movable
        if len(new_board[target_loc]) > 0:
            covered_piece = new_board[target_loc][-1]
            covered_piece_is_agent = int(covered_piece[1] < 0)
            new_movable[covered_piece_is_agent].remove((covered_piece, target_loc))

        # Move the piece to target location
        print(piece)
        np.append(new_board[target_loc[0], target_loc[1]], piece)

        # Update movable
        piece_is_agent = int(piece[1] < 0)
        new_movable[piece_is_agent].remove((piece, curr_loc))
        new_movable[piece_is_agent].add((piece, target_loc))

        # Update the state
        self.board = new_board
        self.movable = new_movable
        self.home_stacks = new_home_stacks
        self.ai_turn = int(not self.ai_turn)
        self.empty = False
        self.winner = None

        return True


    def ai_move(self, depth):
        '''
        Makes a move for the AI using the minimax algorithm with alpha-beta pruning.

        Parameters:
            location (int): The location on the board to move the piece
            piece (int): The piece to move

        Returns:
            tuple(int, int): The move made by the AI containing piece and location.
        '''
        from minimax import TreeNode

        self.ai_turn = 1

        # Create minimax Tree from current state with children as valid_states
        mm_root = TreeNode(state=self, move=None)

        # Build the tree of states, score the last depth level. Propagate the scores back up.
        value = mm_root.alpha_beta(depth=depth)

        # Get the best move according to the returned value
        best_move = mm_root.get_best_move()

        # Make the move
        self.make_move(best_move[0], best_move[1])

        # Return the pieceId, spaceId, and previousSpaceId formatted for the front end
