class Piece:
    def __init__(self):
        self.position = (-1, -1)  # Let (-1, -1) represent a piece that is not on the board
        self.color = color
        self.movable = True

    def __str__(self):
        return f"Piece at ({self.x}, {self.y})"

    def __repr__(self):
        return f"Piece at ({self.x}, {self.y})"

    def move(self, x, y):
        self.x = x
        self.y = y

    def is_valid_move(self, x, y):
        raise NotImplementedError

    def is_valid_capture(self, x, y):
        raise NotImplementedError
