# TODO: BREAK UP CLASSES INTO SEPARATE FILES, FIX GOBBLE LOGIC, ADD AI
# TODO: When you move a piece on the board, remove it from the boards position list and add it to the new position
size_num_to_str = {
    1: 's',
    2: 'm',
    3: 'l',
    4: 'xl'
}

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player('white'), Player('black')]
        self.pieces = {**self.players[0].pieces, **self.players[1].pieces}
        self.in_progress = True

    def check_winner(self):
        if len(self.board.pieces.keys()) < 4:
            # There can't be a winner yet
            return False

        # Check if a player has won
        if 'A1' in self.board.pieces and 'A2' in self.board.pieces and 'A3' in self.board.pieces and 'A4' in self.board.pieces:
            if self.board.pieces["A1"].color == self.board.pieces["A2"].color == self.board.pieces["A3"].color == self.board.pieces["A4"].color:
                print(f'{self.board.pieces["A1"].color} wins!')
                self.in_progress = False
                return True
        if 'B1' in self.board.pieces and 'B2' in self.board.pieces and 'B3' in self.board.pieces and 'B4' in self.board.pieces:
            if self.board.pieces["B1"].color == self.board.pieces["B2"].color == self.board.pieces["B3"].color == self.board.pieces["B4"].color:
                print(f'{self.board.pieces["B1"].color} wins!')
                self.in_progress = False
                return True
        if 'C1' in self.board.pieces and 'C2' in self.board.pieces and 'C3' in self.board.pieces and 'C4' in self.board.pieces:
            if self.board.pieces["C1"].color == self.board.pieces["C2"].color == self.board.pieces["C3"].color == self.board.pieces["C4"].color:
                print(f'{self.board.pieces["C1"].color} wins!')
                self.in_progress = False
                return True
        if 'D1' in self.board.pieces and 'D2' in self.board.pieces and 'D3' in self.board.pieces and 'D4' in self.board.pieces:
            if self.board.pieces["D1"].color == self.board.pieces["D2"].color == self.board.pieces["D3"].color == self.board.pieces["D4"].color:
                print(f'{self.board.pieces["D1"].color} wins!')
                self.in_progress = False
                return True
        if 'A1' in self.board.pieces and 'B1' in self.board.pieces and 'C1' in self.board.pieces and 'D1' in self.board.pieces:
            if self.board.pieces["A1"].color == self.board.pieces["B1"].color == self.board.pieces["C1"].color == self.board.pieces["D1"].color:
                print(f'{self.board.pieces["A1"].color} wins!')
                self.in_progress = False
                return True
        if 'A2' in self.board.pieces and 'B2' in self.board.pieces and 'C2' in self.board.pieces and 'D2' in self.board.pieces:
            if self.board.pieces["A2"].color == self.board.pieces["B2"].color == self.board.pieces["C2"].color == self.board.pieces["D2"].color:
                print(f'{self.board.pieces["A2"].color} wins!')
                self.in_progress = False
                return True
        if 'A3' in self.board.pieces and 'B3' in self.board.pieces and 'C3' in self.board.pieces and 'D3' in self.board.pieces:
            if self.board.pieces["A3"].color == self.board.pieces["B3"].color == self.board.pieces["C3"].color == self.board.pieces["D3"].color:
                print(f'{self.board.pieces["A3"].color} wins!')
                self.in_progress = False
                return True
        if 'A4' in self.board.pieces and 'B4' in self.board.pieces and 'C4' in self.board.pieces and 'D4' in self.board.pieces:
            if self.board.pieces["A4"].color == self.board.pieces["B4"].color == self.board.pieces["C4"].color == self.board.pieces["D4"].color:
                print(f'{self.board.pieces["A4"].color} wins!')
                self.in_progress = False
                return True
        if 'A1' in self.board.pieces and 'B2' in self.board.pieces and 'C3' in self.board.pieces and 'D4' in self.board.pieces:
            if self.board.pieces["A1"].color == self.board.pieces["B2"].color == self.board.pieces["C3"].color == self.board.pieces["D4"].color:
                print(f'{self.board.pieces["A1"].color} wins!')
                self.in_progress = False
                return True
        if 'A4' in self.board.pieces and 'B3' in self.board.pieces and 'C2' in self.board.pieces and 'D1' in self.board.pieces:
            if self.board.pieces["A4"].color == self.board.pieces["B3"].color == self.board.pieces["C2"].color == self.board.pieces["D1"].color:
                print(f'{self.board.pieces["A4"].color} wins!')
                self.in_progress = False
                return True

        # TODO: Check if the game is a draw, will need to have move memory here to see if the same board state has been reached 3 times

        return False

class Board:
    def __init__(self):
        self.pieces = {}
        self.spaces = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4', 'D1', 'D2', 'D3', 'D4']

    def print_state(self):
        print('     1    2    3    4')  # Print column numbers
        print('  ---------------------')  # Print top border
        for i in range(4):
            print(chr(65 + i), end=' |')  # Print row letters
            for j in range(4):
                space = chr(65 + i) + str(j + 1)  # Convert i to a letter from 'A' to 'D' and add j + 1
                if space in self.pieces:
                    print(f'{self.pieces[space].color[0]}-{size_num_to_str[self.pieces[space].size]}', end='|')
                else:
                    print('    ', end='|')
            print()  # Print a newline at the end of each row
            print('  ---------------------')  # Print a divider after each row

class Piece:
    def __init__(self, color, size, number, position, under, on):
        self.color = color
        self.size = size  # 4 = xl, 3 = l, 2 = m, 1 = s
        self.number = number  # 1, 2, 3 (each player has 3 pieces of each size)
        self.position = position
        self.on = on
        self.under = under

    # TODO: If the piece is on top of another piece, update the board pieces when it is moved
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
                game.pieces[self.on].under = None
                if self.position != 'home':
                    if self.position in board.pieces:
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

def main():
    # Create a new game
    game = Game()

    # Create game loop
    while game.in_progress:
        for player in game.players:
            game.board.print_state()
            print(f"{player.color}'s turn")
            move = 'Invalid'
            while move == 'Invalid':
                piece = 'Invalid'
                position = 'Invalid'

                # Get user input (move/piece)
                while piece == 'Invalid':
                    piece = input('What piece would you like to move? ')
                    if piece not in player.pieces:
                        piece = 'Invalid'
                        print('Invalid piece. Please try again.')

                while position == 'Invalid':
                    position = input('Where would you like to move it? ')
                    if position not in game.board.spaces:
                        position = 'Invalid'
                        print('Invalid board space. Please try again.')

                # Process the move
                if player.pieces[piece].move(position, game.board, game):
                    move = 'Valid'

                # Check if the game is over
                if game.check_winner():
                    break

    pass

if __name__ == "__main__":
    main()
