from board import Board

class Solver:
    def __init__(self, sudoku:Board):
        self.sudoku = sudoku

    def solve(self):
        # Use backtracking algorithm and recursion to solve
        # Get first empty field and solver from there
        first_empty = self.next_empty((0,0))
        found_solution = self.solve_from(first_empty)
        

    # Returns true if was able to solve from (row, col)
    def solve_from(self, index:tuple) -> bool:
        if index == (-1, -1): # end of sudoku reached, completely solved
            assert(self.is_full())
            return True
                    
        row = index[0]
        col = index[1]

        # try all possibilities while not solution found
        for n in range(1,10): # numbers 1-9
            if self.is_valid(index, n):
                self.sudoku.board[row][col] = n

                # Get next cell and do recursive call
                next = self.next_empty((row, col))
                if self.solve_from(next):
                    return True
        
        # no option works -> backpropagate
        else:
            self.sudoku.board[row][col] = 0 # reset
            return False 
            

    # returns (row, col) of next empty field and (-1, -1) if full
    def next_empty(self, index:tuple) -> int:
        if self.is_full():
            return (-1, -1)

        row = index[0]
        col = index[1]    
        
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
    def is_valid(self, index:tuple, number:int) -> bool:
        assert(1 <= number <= 9)
        row = index[0]
        col = index[1]

        # check row
        for c in range(self.sudoku.n_cols):
            if self.sudoku.board[row][c] == number:
                return False

        # check column
        for r in range(self.sudoku.n_rows):
            if self.sudoku.board[r][col] == number:
                return False

        # check box
        box = self.get_box((row, col))
        for r in range(box[0] * 3, box[0] * 3 + 3):
            for c in range(box[1] * 3, box[1] * 3 + 3):
                if self.sudoku.board[r][c] == number:
                    return False

        return True

    # returns (r, c) indices of box corresponding to row and col
    def get_box(self, index:tuple) -> tuple:
        return (index[0] // 3, index[1] // 3)
        
