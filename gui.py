from solver import Solver
import pygame
from board import Board
import threading


class Sudoku:
    width = 540
    height = 540

    def __init__(self, board:Board):
        self.given = board.copy()
        self.board = board # contains filled board
        self.n_rows = board.n_rows
        self.n_cols = board.n_cols
        self.update_fields()

    def update_fields(self):
        self.fields = []
        for r in range(self.n_rows):
            for c in range(self.n_rows):
                self.fields.append(Field(self.board.board[r][c], (r,c), self.given.board[r][c] != 0))

    def draw(self, win):
        self.update_fields()

        # Calculate field width and height
        f_width = Sudoku.width // self.n_cols
        f_height = Sudoku.height // self.n_rows
        w, _ = pygame.display.get_surface().get_size()
        border = (w - f_width * self.n_cols) // 2

        # Draw Grid Lines
        for i in range(self.n_rows+1):
            if i % 3 == 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0,0,0), (border, border + i*f_height), (border + Sudoku.width, border + i*f_height), thickness)
            pygame.draw.line(win, (0,0,0), (border + i*f_width, border), (border + i*f_width, border + Sudoku.height), thickness)

            # Loop through fields and draw
        for field in self.fields:
            field.draw(win, f_width, f_height, border)


class Field:
    def __init__(self, value:int, index:tuple, given=False):
        self.row = index[0]
        self.col = index[1]

        self.value = value
        self.given = given

    def draw(self, win, width:int, height:int, border:int):
        x = self.col * width + border
        y = self.row * height + border

        if self.given == True:
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (width/2 - text.get_width()/2), y + (height/2 - text.get_height()/2)))
        elif self.given == False and self.value != 0:
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(str(self.value), 1, (65,105,225))
            win.blit(text, (x + (width/2 - text.get_width()/2), y + (height/2 - text.get_height()/2)))
        else:
            pass # empty


        #pygame.draw.rect(win, (255,0,0), (x, y, width, height), 3)


    def __repr__(self):
        return f"Field({self.value})"

def redraw_window(win, sudoku:Sudoku):
    win.fill((255,255,255))
    sudoku.draw(win)

def main_gui(board:Board):
    sudoku = Sudoku(board)
    win = pygame.display.set_mode((580,580))
    pygame.display.set_caption("Sudoku")
    pygame.font.init()

    # Draw window for first time
    redraw_window(win, sudoku)
    pygame.display.update()
    
    # Start solver in seperate thread
    print("before new thread")

    solver = Solver(sudoku.board)
    thread = threading.Thread(target = solver.solve)
    thread.setDaemon(True)
    thread.start()
    print("started solver")

    # Update GUI in main thread
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window(win, sudoku)
        pygame.display.update()
