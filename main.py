from board import Board
from gui import main_gui
import pygame

def main():
    board = Board('board1.txt')
    #board = Board('board2.txt')

    main_gui(board)
    pygame.quit()

    # Solve without animation
    # solver = Solver(board)
    # solver.solve()
    # board.print()

if __name__ == "__main__":
    main()