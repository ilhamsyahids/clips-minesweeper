from tkinter import *
from functools import partial
from tkinter import ttk
from main import Board
from clips import Environment

# COLORS
BLUE_GRAY = "#B0BEC5"
LIGHT_BLUE_GRAY = "#ECEFF1"
GRAY = "#BDBDBD"
LIGHT_GRAY = "#E0E0E0"
MAGENTA = "#880E4F"
YELLOW = "#ffe082"
BLUE = "#283593" #1
GREEN = "#2E7D32" #2
RED = "#C62828" #3
DARK_BLUE = "#1a237e" #4
DARK_RED = "#b71c1c" #5
TOSCA = "#006064" #6
DARK_GRAY = "#212121" #7
YELLOW_GREEN = "#827717" #8
BLACK = "#000000"

ELEMENTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '*']
BORDERS = ["raised", "solid", "raised"]
BORDER_WIDTH = [5, 1, 5]
TILE_COLORS = [BLUE_GRAY, LIGHT_GRAY, BLUE_GRAY]
LABEL_COLORS = [LIGHT_GRAY, BLUE, GREEN, RED, DARK_BLUE, DARK_RED, TOSCA, DARK_GRAY, YELLOW_GREEN, BLACK]

class Window(object):

    def __init__(self, master, board):
        # Setup main window
        self.master = master
        self.master.title('Minesweeper GUI by "NoCLIPS Mode"')
        self.master.resizable(True, True)
        window_width = 960
        window_height = 480
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        self.board_size = board.size
        self.list_bomb = board.list_bomb
        self.list_flag = board.list_flag
        self.board = board.board
        self.board_open = board.board_open

        # -- MENU --
        self.frame_menu = Frame(self.master)
        self.frame_menu.place(anchor="w", relx=0.01, rely=0.5, width=240, height=400)

        i_row = 0

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        self.start_game()

    def test_game(self):
        self.board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        self.board_open = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        
        for i in range(4):
            for j in range(2):
                self.board_open[i][j] = 1
        for i in range(2):
            for j in range(2,6):
                self.board_open[i][j] = 1
        
        self.board[1][1] = 1
        self.board[1][2] = 2
        self.board[1][3] = 2
        self.board[1][4] = 1
        self.board[1][5] = 1
        self.board[0][5] = 1
        self.board[2][1] = 1
        self.board[3][1] = 2
        self.board[3][0] = 1
        self.list_bomb = [(2,2), (2,3), (0,6)]
        self.list_flag = [(2,2), (2,3)]

    def start_game(self):
        # BOARD FRAME
        self.frame_board = Frame(self.master)
        self.frame_board.place(anchor="center", relx=0.5, rely=0.5, width=400, height=400)
        self.frame_board.config(borderwidth=2, relief="solid")
        for i in range(self.board_size):
            self.frame_board.columnconfigure(i, weight=1)
            self.frame_board.rowconfigure(i, weight=1)
        
        self.update_board()

    def update_board(self):
        self.tiles = [[None for i in range(self.board_size)] for i in range(self.board_size)]  # tile border
        self.tile_labels = [[None for i in range(self.board_size)] for i in range(self.board_size)]  # actual tile
        for i in range(self.board_size):
            for j in range(self.board_size):
                is_bomb = (i, j) in self.list_bomb
                el = self.board[i][j]
                op = self.board_open[i][j]
                is_flag = not op
                tile_color = TILE_COLORS[op]
                icon = u"\u25B2" if is_flag else ELEMENTS[el]
                color = LABEL_COLORS[el] if op else tile_color
                color = RED if is_flag else color
                self.tiles[i][j] = Frame(self.frame_board, bg=tile_color, borderwidth=BORDER_WIDTH[op], relief=BORDERS[op])
                self.tile_labels[i][j] = Label(self.tiles[i][j], bg=tile_color, bd=0, fg=color, text=icon,
                                               font=("Helvetica", int((25 if is_flag else 34) - 1.6 * self.board_size), "bold"),
                                               anchor="center")
                self.tiles[i][j].grid(row=i, column=j, sticky="nesw")
                self.tile_labels[i][j].grid(row=0, column=0, sticky="nesw")
                self.tiles[i][j].grid_rowconfigure(0, weight=1)
                self.tiles[i][j].grid_columnconfigure(0, weight=1)

    def click_tile_env(self, i, j):
        self.board.click_tile(i, j)
        if self.env is not None:
            self.board.assert_state(self.env)
        self.update_board()


if __name__ == "__main__":
    size = int(input())

    list_bomb = []
    list_flag = []
    for i in range(int(input())):
        coor = tuple(map(int, input().split(', ')))
        list_bomb.append(coor)
        list_flag.append(coor)

    board = Board(size, list_bomb)

    env = Environment()
    board.env = env
    env.load('minesweeper.clp')
    
    env.define_function(board.click_tile_env, 'click_tile')
    rule = """
    (defrule open-tile-program
        (aman ?x ?y)
        (not (siku ?x ?y))
        (not (open ?x ?y))
        (size ?n)
        (test (>= ?x 0))
        (test (< ?x ?n))
        (test (>= ?y 0))
        (test (< ?y ?n))
        (using-program)
        =>
        (printout t "(" ?x " , "  ?y ")" crlf)
        (click_tile ?x ?y)
    )
    """
    
    rule2 = """
    (defrule open-tile-program-non-flag
        (declare (salience -10))
        (inboard ?x ?y)
        (not (siku ?x ?y))
        (not (flag ?x ?y))
        (not (open ?x ?y))
        (size ?n)
        (test (>= ?x 0))
        (test (< ?x ?n))
        (test (>= ?y 0))
        (test (< ?y ?n))
        (using-program)
        =>
        (printout t "(" ?x " , "  ?y ")" crlf)
        (click_tile ?x ?y)
    )
    """

    env.reset()

    for i in range(size):
        for j in range(size):
            env.assert_string(f'(inboard {i} {j})')

    env.build(rule)
    env.build(rule2)

    env.assert_string('(using-program)')
    env.assert_string('(size {})'.format(size))
    env.run()

    app = Tk()
    Window = Window(app, board)
    app.mainloop()
