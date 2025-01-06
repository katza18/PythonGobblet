# TODO: Store a hint_move or hint_state to offer hints to the user (their optimal move)
# TODO: Add build_tree function
class TreeNode:
    def __init__(self, state, move=None, value=0, terminal=False):
        '''
        Initializes a TreeNode object.

        Attributes:
            state (GameState) = The state for the given node.
            move (tuple) = The move required to get to this state. Can be None (this is the current game state).
        '''
        
        self.children = None
        self.state = state
        self.move = move
        self.terminal = False
        self.value = 0


    def add_child(self, child):
        '''
        Adds a child to the TreeNode.

        Parameters:
            child (TreeNode) = A child of the current node.
        '''
        self.children.append(child)


    def alpha_beta(self, depth, alpha, beta, agent):
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
            self.value = self.state.score_board
            return self.value
        
        if agent:
            value = float('-inf')
            for child in self.children:
                value = max(value, child.alpha_beta(depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if value >= beta:
                    break  # Beta cutoff
            self.value = value
        else:
            value = float('inf')
            for child in self.children:
                value = min(value, child.alpha_beta(depth-1, alpha, beta, True))
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
    