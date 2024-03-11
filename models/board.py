size_num_to_str = {
    1: 's',
    2: 'm',
    3: 'l',
    4: 'xl'
}

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
