from models.piece import Piece

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = {
            f'{color}-xl-1': Piece(color, 4, 1, 'home', None, f'{color}-l-1'),
            f'{color}-xl-2': Piece(color, 4, 2, 'home', None, f'{color}-l-2'),
            f'{color}-xl-3': Piece(color, 4, 3, 'home', None, f'{color}-l-3'),
            f'{color}-l-1': Piece(color, 3, 1, 'home', f'{color}-xl-1', f'{color}-m-1'),
            f'{color}-l-2': Piece(color, 3, 2, 'home', f'{color}-xl-2', f'{color}-m-2'),
            f'{color}-l-3': Piece(color, 3, 3, 'home', f'{color}-xl-3', f'{color}-m-3'),
            f'{color}-m-1': Piece(color, 2, 1, 'home', f'{color}-l-1', f'{color}-s-1'),
            f'{color}-m-2': Piece(color, 2, 2, 'home', f'{color}-l-2', f'{color}-s-2'),
            f'{color}-m-3': Piece(color, 2, 3, 'home', f'{color}-l-3', f'{color}-s-3'),
            f'{color}-s-1': Piece(color, 1, 1, 'home', f'{color}-m-1', None),
            f'{color}-s-2': Piece(color, 1, 2, 'home', f'{color}-m-2', None),
            f'{color}-s-3': Piece(color, 1, 3, 'home', f'{color}-m-3', None)
        }
        self.move_counter = 0
