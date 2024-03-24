size_num_to_str = {
    1: 's',
    2: 'm',
    3: 'l',
    4: 'xl'
}

class Piece:
    def __init__(self, color, size, number, position, under, on):
        self.color = color
        self.size = size  # 4 = xl, 3 = l, 2 = m, 1 = s
        self.number = number  # 1, 2, 3 (each player has 3 pieces of each size)
        self.position = position
        self.on = on
        self.under = under

    def move(self, new_position, board, game):
        # Make sure piece is movable
        if self.under != None:
            # Cannot move piece
            print('This piece is not movable because it is under another piece.')
            return False

        # If there is a piece at that position, check if it can be gobbled
        if new_position in board.pieces:
            if board.pieces[new_position].size < self.size:
                # Set old 'on' piece's under to None
                if self.on != None:
                    game.pieces[self.on].under = None

                # Gobble the piece
                gobbled_piece = f'{board.pieces[new_position].color}-{size_num_to_str[board.pieces[new_position].size]}-{board.pieces[new_position].number}'
                this_piece = f'{self.color}-{size_num_to_str[self.size]}-{self.number}'
                if self.position != 'home':
                    if self.position in board.pieces and self.on != None:
                        board.pieces[self.position] = game.pieces[self.on]
                    else:
                        del board.pieces[self.position]
                self.on = gobbled_piece
                board.pieces[new_position].under = this_piece
                board.pieces[new_position] = self
                self.position = new_position
                print(f'{self.color} {self.size} - {self.number} gobbled {board.pieces[new_position].color} {board.pieces[new_position].size} - {board.pieces[new_position].number} at {new_position}')

                return True
            else:
                # Cannot gobble
                print('This piece cannot be moved to that position because it is blocked by a larger piece.')
                return False
        else:
            # Move the piece to an empty space
            if self.on != None:
                # The piece that it was on, it no longer under anything
                game.pieces[self.on].under = None

            if self.position != 'home':
                if self.on != None:
                    board.pieces[self.position] = game.pieces[self.on]
                else:
                    del board.pieces[self.position]
            self.on = None
            board.pieces[new_position] = self
            self.position = new_position
            print(f'{self.color} {self.size} - {self.number} moved to {new_position}')
            return True

    def __str__(self):
        return f'{self.color} {self.size} - {self.number} at {self.position}'
