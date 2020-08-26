from board import Board

class Solver:
    def __init__(self, sudoku:Board):
        self.sudoku = sudoku

    def solve(self):
        # Loop through empty fields and use backtracking algorithm
        pass

    # returns (row, col) of next empty field and (-1, -1) if full
    def next_empty(self, row:int, col:int) -> int:
        if self.is_full():
            return (-1, -1)
        
        # check if in same row
        for c in range(col + 1, self.sudoku.n_cols):
            if self.sudoku.board[row][c] == 0:
                return (row, c)

        # check remaining rows
        for r in range(row+1, self.sudoku.n_rows):
            for c in range(self.sudoku.n_cols):
                if self.sudoku.board[r][c] == 0:
                    return (r, c)

    # returns True if board is full
    def is_full(self):        
        for r in range(self.sudoku.n_rows):
            for c in range(self.sudoku.n_cols):
                if self.sudoku.board[r][c] == 0:
                    return False
        return True

    # returns True if number at (row, col) results in valid composition
    def is_valid(self, position:tuple, number:int) -> bool:
        assert(1 <= number <= 9)
        row = position[0]
        col = position[1]

        # check row
        for c in range(self.sudoku.n_cols):
            if self.sudoku.board[row][c] == number:
                print("1")
                return False

        # check column
        for r in range(self.sudoku.n_rows):
            if self.sudoku.board[r][col] == number:
                print("2")
                return False

        # check box
        box = self.get_box(row, col)
        for r in range(box[0] * 3, box[0] * 3 + 3):
            for c in range(box[1] * 3, box[1] * 3 + 3):
                if self.sudoku.board[r][c] == number:
                    print("1")
                    return False

        return True

    # returns (r, c) indices of box corresponding to row and col
    def get_box(self, row:int, col:int) -> tuple:
        return (row // 3, col // 3)
        
