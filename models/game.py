from models.board import Board
from models.player import Player

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player('white'), Player('black')]
        self.pieces = {**self.players[0].pieces, **self.players[1].pieces}
        self.in_progress = True
        self.current_player = self.players[0]

    # def play(self):
    #     while self.in_progress:
    #         for player in self.players:
    #             self.board.print_state()
    #             print(f"{player.color.capitalize()}'s turn")
    #             move = 'Invalid'
    #             while move == 'Invalid':
    #                 piece = 'Invalid'
    #                 position = 'Invalid'

    #                 # Get user input (move/piece)
    #                 while piece == 'Invalid':
    #                     piece = input('What piece would you like to move? ')
    #                     if piece not in player.pieces:
    #                         piece = 'Invalid'
    #                         print('Invalid piece. Please try again.')

    #                 while position == 'Invalid':
    #                     position = input('Where would you like to move it? ')
    #                     if position not in self.board.spaces:
    #                         position = 'Invalid'
    #                         print('Invalid board space. Please try again.')

    #                 # Process the move
    #                 if player.pieces[piece].move(position, self.board, self):
    #                     move = 'Valid'

    #                 # Check if the game is over
    #                 if self.check_winner():
    #                     break

    # def play_user_vs_ai(self):
    #     while self.in_progress:
    #         for player in self.players:
    #             self.board.print_state()
    #             print(f"{player.color.capitalize()}'s turn")
    #             move = 'Invalid'
    #             while move == 'Invalid':
    #                 piece = 'Invalid'
    #                 position = 'Invalid'

    #                 # If the current player is not AI
    #                 if player.color == 'white':
    #                     # Get user input (move/piece)
    #                     while piece == 'Invalid':
    #                         piece = input('What piece would you like to move? ')
    #                         if piece not in player.pieces:
    #                             piece = 'Invalid'
    #                             print('Invalid piece. Please try again.')

    #                     while position == 'Invalid':
    #                         position = input('Where would you like to move it? ')
    #                         if position not in self.board.spaces:
    #                             position = 'Invalid'
    #                             print('Invalid board space. Please try again.')

    #                     # Process the move
    #                     if player.pieces[piece].move(position, self.board, self):
    #                         move = 'Valid'

    #                     # Check if the game is over
    #                     if self.check_winner():
    #                         break
    #                 else:
    #                     # AI's turn

    #                     pass


    def check_winner(self):
        if len(self.board.pieces.keys()) < 4:
            # There can't be a winner yet
            return False

        # Check if a player has won
        if 'A1' in self.board.pieces and 'A2' in self.board.pieces and 'A3' in self.board.pieces and 'A4' in self.board.pieces:
            if self.board.pieces["A1"].color == self.board.pieces["A2"].color == self.board.pieces["A3"].color == self.board.pieces["A4"].color:
                print(f'{self.board.pieces["A1"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'B1' in self.board.pieces and 'B2' in self.board.pieces and 'B3' in self.board.pieces and 'B4' in self.board.pieces:
            if self.board.pieces["B1"].color == self.board.pieces["B2"].color == self.board.pieces["B3"].color == self.board.pieces["B4"].color:
                print(f'{self.board.pieces["B1"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'C1' in self.board.pieces and 'C2' in self.board.pieces and 'C3' in self.board.pieces and 'C4' in self.board.pieces:
            if self.board.pieces["C1"].color == self.board.pieces["C2"].color == self.board.pieces["C3"].color == self.board.pieces["C4"].color:
                print(f'{self.board.pieces["C1"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'D1' in self.board.pieces and 'D2' in self.board.pieces and 'D3' in self.board.pieces and 'D4' in self.board.pieces:
            if self.board.pieces["D1"].color == self.board.pieces["D2"].color == self.board.pieces["D3"].color == self.board.pieces["D4"].color:
                print(f'{self.board.pieces["D1"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'A1' in self.board.pieces and 'B1' in self.board.pieces and 'C1' in self.board.pieces and 'D1' in self.board.pieces:
            if self.board.pieces["A1"].color == self.board.pieces["B1"].color == self.board.pieces["C1"].color == self.board.pieces["D1"].color:
                print(f'{self.board.pieces["A1"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'A2' in self.board.pieces and 'B2' in self.board.pieces and 'C2' in self.board.pieces and 'D2' in self.board.pieces:
            if self.board.pieces["A2"].color == self.board.pieces["B2"].color == self.board.pieces["C2"].color == self.board.pieces["D2"].color:
                print(f'{self.board.pieces["A2"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'A3' in self.board.pieces and 'B3' in self.board.pieces and 'C3' in self.board.pieces and 'D3' in self.board.pieces:
            if self.board.pieces["A3"].color == self.board.pieces["B3"].color == self.board.pieces["C3"].color == self.board.pieces["D3"].color:
                print(f'{self.board.pieces["A3"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'A4' in self.board.pieces and 'B4' in self.board.pieces and 'C4' in self.board.pieces and 'D4' in self.board.pieces:
            if self.board.pieces["A4"].color == self.board.pieces["B4"].color == self.board.pieces["C4"].color == self.board.pieces["D4"].color:
                print(f'{self.board.pieces["A4"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'A1' in self.board.pieces and 'B2' in self.board.pieces and 'C3' in self.board.pieces and 'D4' in self.board.pieces:
            if self.board.pieces["A1"].color == self.board.pieces["B2"].color == self.board.pieces["C3"].color == self.board.pieces["D4"].color:
                print(f'{self.board.pieces["A1"].color.capitalize()} wins!')
                self.in_progress = False
                return True
        if 'A4' in self.board.pieces and 'B3' in self.board.pieces and 'C2' in self.board.pieces and 'D1' in self.board.pieces:
            if self.board.pieces["A4"].color == self.board.pieces["B3"].color == self.board.pieces["C2"].color == self.board.pieces["D1"].color:
                print(f'{self.board.pieces["A4"].color.capitalize()} wins!')
                self.in_progress = False
                return True

        # TODO: Check if the game is a draw, will need to have move memory here to see if the same board state has been reached 3 times

        return False
