# TODO: Store a hint_move or hint_state to offer hints to the user (their optimal move)
class TreeNode:
    def __init__(self, state, move=None, value=0, terminal=False):
        '''
        Initializes a TreeNode object.

        Attributes:
            state (GameState) = The state for the given node.
            move (tuple) = The move required to get to this state. Can be None (this is the current game state).
        '''

        self.children = []
        self.state = state
        self.move = move
        self.terminal = False
        self.value = 0


    def build_tree(self, depth):
        '''
        Recursively builds the tree to the specified depth.

        TODO: Needs to be optimized such that pieces of the same size at home are regarded as the same piece.

        Parameters:
            depth (int) = The depth of the tree to build.
        '''

        # SOMETHING WRONG HERE. There should only be at maximum 45 nodes for depth 1.

        if depth == 0:
            return

        # Get valid moves. Format == [(piece_id, space_id), ...] where piece_id and space_id are (home_stack, piece_size) and (row, column) respectively.
        valid_moves = self.state.get_valid_moves()
        for move in valid_moves:
            new_state = self.state.copy()

            if new_state.make_move(move[0], move[1]):
                child = TreeNode(new_state, move)

                # Score the board and set value
                child.value = new_state.score_board

                self.children.append(child)
                child.build_tree(depth-1)


    def alpha_beta(self, depth, alpha=float('-inf'), beta=float('inf'), agent=True):
        '''
        Implementation of the minimax algorithm with alpha-beta pruning.

        Parameters:
            node (TreeNode) = The current state (node) we are at in the tree.
            depth (int) = The depth of the tree that we will traverse to.
            alpha (float)
            beta (float)
            agent (bool) = Whether or not it is the Agent's turn (maximizing)

        Returns:
            value (float) = The value propogated up by the minimax/alpha-beta pruning algorithm.
        '''

        if depth == 0 or self.terminal:
            # Score the board here
            self.value = self.state.score_board()
            return self.value

        if agent:
            value = float('-inf')
            for child in self.children:
                child_val = child.alpha_beta(depth-1, alpha, beta, False)
                value = max(value, child_val)
                alpha = max(alpha, value)
                if value >= beta:
                    break  # Beta cutoff
            self.value = value
        else:
            value = float('inf')
            for child in self.children:
                child_val = child.alpha_beta(depth-1, alpha, beta, True)
                value = min(value, child_val)
                beta = min(beta, value)
                if value <= alpha:
                    break  # Alpha cutoff
            self.value = value

        return value


    def get_best_move(self):
        '''
        Used to retrieve the best move after alpha-beta is run. This is meant to be run on the root (current state) after alpha_beta.

        Returns:
            best_move (tuple) = The best move according to ab pruned minimax.
        '''
        for child in self.children:
            if child.value == self.value:
                return child.move
        return None
