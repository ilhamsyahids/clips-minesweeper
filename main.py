from clips import Environment


class Board:
    def __init__(self, size, list_bomb):
        self.env = None
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]
        self.board_open = [[0 for i in range(size)] for j in range(size)]
        self.board_open_asserted = [[False for i in range(size)] for j in range(size)]
        self.list_bomb = list_bomb
        self.list_flag = []
        self.create_numbers()

    def __str__(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                if self.board_open[i][j] == 1:
                    s += str(self.board[i][j]
                             ) if self.board[i][j] != -1 else '*'
                elif self.board_open[i][j] == -1:
                    s += 'X'
                else:
                    s += '?'
                s += ' '
            s = s.strip()
            s += '\n'
        return s.strip()

    def is_in_board(self, i, j):
        return i>=0 and i<self.size and j>=0 and j<self.size

    def create_numbers(self):
        for coor in self.list_bomb:
            self.board[coor[0]][coor[1]] = -1
        for coor in self.list_bomb:
            i = coor[0]
            j = coor[1]
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if self.is_in_board(i + x, j + y):
                        if (self.board[i + x][j + y] != -1):
                            self.board[i + x][j + y] += 1

    def mark_tile(self, t: tuple):
        i = t[0]
        j = t[1]
        if self.board_open[i][j] == 1:
            return
        if self.board_open[i][j] == -1:
            self.unmark_tile(t)
            return
        self.board_open[i][j] = -1

    def unmark_tile(self, t: tuple):
        i = t[0]
        j = t[1]
        if self.board_open[i][j] != -1:
            return
        self.board_open[i][j] = 0

    def click_tile(self, i, j, base=True):
        if base:
            print('Click tile ({}, {})'.format(i,j))
        if not self.is_in_board(i, j):
            print('[ERROR] click outside board')
            return

        if base and self.board[i][j] == -1:
            print('Game Over')
            exit(1)
            return
        if self.board_open[i][j] != 0:
            return
        self.board_open[i][j] = 1
        if self.board[i][j] != 0:
            return
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self.is_in_board(i + x, j + y):
                    if (not self.board_open[i+x][j+y]):
                        self.click_tile(i + x, j + y, False)

    def click_tile_env(self, i, j):
        self.click_tile(i, j)
        print(self)
        if self.env is not None:
            self.assert_state(self.env)

    def assert_state(self, env):
        for i in range(self.size):
            for j in range(self.size):
                if self.board_open[i][j] == 1 and not self.board_open_asserted[i][j]:
                    env.assert_string("(open {} {})".format(i, j))
                    env.assert_string(
                        '(value {} {} {})'.format(i, j, self.board[i][j]))
                    self.board_open_asserted[i][j] = True


if __name__ == "__main__":
    size = int(input())

    list_bomb = []
    list_flag = []
    for i in range(int(input())):
        coor = tuple(map(int, input().split(', ')))
        list_bomb.append(coor)
        list_flag.append(coor)

    board = Board(size, list_bomb)
    print(board)
    print()
    # board.click_tile(0,6)
    # board.click_tile(0, 0)
    # board.mark_tile((0, 6))
    # board.unmark_tile((0, 6))

    env = Environment()
    board.env = env
    env.load('minesweeper.clp')
    
    env.define_function(board.click_tile_env, 'click_tile')
    rule = """
    (defrule open-tile-program
        (aman ?x ?y)
        (not (open ?x ?y))
        (using-program)
        =>
        (printout t "(" ?x " , "  ?y ")" crlf)
        (click_tile ?x ?y)
    )
    """
    
    env.reset()
    env.build(rule)
    env.assert_string('(using-program)')
    env.assert_string('(size {})'.format(size))
    env.run()
    # for fact in env.facts():
    #     print(fact)
    # print(board)
