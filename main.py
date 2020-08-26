from board import Board
from solver import Solver

def main():
    board = Board('board1.txt')
    board.print()

    solver = Solver(board)
    solver.solve()
    board.print()




if __name__ == "__main__":
    main()