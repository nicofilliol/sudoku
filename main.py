from board import Board
from solver import Solver

def main():
    board = Board('board1.txt')
    board.print()

    solver = Solver(board)
    solver.solve()

    print(solver.is_valid((0, 1), 6))
    print(solver.is_valid((0, 1), 7))



if __name__ == "__main__":
    main()