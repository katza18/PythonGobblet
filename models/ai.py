class AI:
    def __init__(self):
        self.weights = {}
        self.learning_rate = 0.1
        self.epsilon = 0.1
        self.discount = 0.9

    def move(self, game):
        state = game.get_state()

        possible_moves = game.get_possible_moves()

        if random.random() < self.epsilon:
            move = random.choice(possible_moves)
        else:
            move = max(possible_moves, key=lambda move: self.weights.get((state, move)))

        reward = game.perform_action(move)

        new_state = game.get_state()

        self.experiences.append((state, move, reward, new_state))

        return move
