import scanner

class Board:
    def __init__(self, board):

        if type(board) == str: #load board from file
            if board.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')): # image
                self.board = scanner.convert_image_to_board(board)
            else: # text file
                self.board = self.load_from_file(board)
        else:
            self.board = board

        # set dimensions
        self.n_rows = len(self.board)
        self.n_cols = len(self.board[0])

    def load_from_file(self, board:str) -> list:
        b = []
        with open(board) as reader:
            for line in reader:
                row = line.strip()
                b.append(row.split(' '))
        
        # convert to integers
        b = [list(map(int, r)) for r in b]
        return b

    def print(self):
        print()
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                print(self.board[r][c], end=' ')
                if (c+1) % 3 == 0 and c != self.n_cols-1:
                    print('|', end=' ')
            
            if (r+1) % 3 == 0 and r != self.n_rows-1:
                print("\n---------------------") # new row
            else:
                print()

    def copy(self):
        return Board([row[:] for row in self.board])



