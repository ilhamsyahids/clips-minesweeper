from tkinter import *
from functools import partial
from tkinter import ttk
from main import Board

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
        self.board = board
        self.master.title("Minesweeper")
        self.master.resizable(True, True)
        window_width = 960
        window_height = 480
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        # -- MENU --
        self.frame_menu = Frame(self.master)
        self.frame_menu.place(anchor="w", relx=0.01, rely=0.5, width=240, height=400)

        i_row = 0

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # BOARD SIZE
        self.label_board_size = Label(self.frame_menu, text="Board Size (NxN)", font=("Verdana", 10, "bold"))
        self.label_board_size.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_board_size = IntVar()
        self.var_board_size.set(8)
        self.scale_board_size = Scale(self.frame_menu, variable=self.var_board_size, from_=6, to=10, orient=HORIZONTAL)
        self.scale_board_size.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # START GAME
        self.button_start_game = Button(self.frame_menu, text="Start Game", font=("Verdana", 14, "bold"), bg=BLUE_GRAY,
                                        command=self.start_game)
        self.button_start_game.grid(row=i_row, column=0)

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
        self.board_size = self.var_board_size.get()
        self.list_bomb = []
        self.list_flag = []
        # self.test_game() # !!! TESTING !!!

        # BOARD FRAME
        self.frame_board = Frame(self.master)
        self.frame_board.place(anchor="center", relx=0.5, rely=0.5, width=400, height=400)
        self.frame_board.config(borderwidth=2, relief="solid")
        for i in range(self.board_size):
            self.frame_board.columnconfigure(i, weight=1)
            self.frame_board.rowconfigure(i, weight=1)
        
        self.tiles = [[None for i in range(self.board_size)] for i in range(self.board_size)]  # tile border
        self.tile_labels = [[None for i in range(self.board_size)] for i in range(self.board_size)]  # actual tile
        for i in range(self.board_size):
            for j in range(self.board_size):
                is_bomb = (i, j) in self.list_bomb
                is_flag = (i, j) in self.list_flag
                el = self.board[i][j]
                op = self.board_open[i][j]
                tile_color = TILE_COLORS[op]
                icon = u"\u25B8" if is_flag else ELEMENTS[el]
                color = LABEL_COLORS[el] if op else tile_color
                color = RED if is_flag else color
                self.tiles[i][j] = Frame(self.frame_board, bg=tile_color, borderwidth=BORDER_WIDTH[op], relief=BORDERS[op])
                self.tile_labels[i][j] = Label(self.tiles[i][j], bg=tile_color, bd=0, fg=color, text=icon,
                                               font=("Helvetica", int(34 - 1.6 * self.board_size), "bold"),
                                               anchor="center")
                self.tiles[i][j].grid(row=i, column=j, sticky="nesw")
                self.tile_labels[i][j].grid(row=0, column=0, sticky="nesw")
                self.tiles[i][j].grid_rowconfigure(0, weight=1)
                self.tiles[i][j].grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    size = int(input())

    list_bomb = []
    list_flag = []
    for i in range(int(input())):
        coor = tuple(map(int, input().split(', ')))
        list_bomb.append(coor)
        list_flag.append(coor)

    board = Board(size, list_bomb)

    app = Tk()
    Window = Window(app, board)
    app.mainloop()
    