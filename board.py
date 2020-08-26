class Board:
    def __init__(self, board):

        if type(board) == str: #load board from file
            self.board = self.load_from_file(board)
        else:
            self.board = board

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
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                print(self.board[r][c], end=' ')
                if (c+1) % 3 == 0 and c != len(self.board[0])-1:
                    print('|', end=' ')
            
            if (r+1) % 3 == 0 and r != len(self.board)-1:
                print("\n---------------------") # new row
            else:
                print()



board = Board('board1.txt')
board.print()




