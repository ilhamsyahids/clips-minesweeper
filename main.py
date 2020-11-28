from clips import Environment


class Board:
    def __init__(self, size, list_bomb):
        self.env = None
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]
        self.board_open = [[0 for i in range(size)] for j in range(size)]
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

    def create_numbers(self):
        for coor in self.list_bomb:
            self.board[coor[0]][coor[1]] = -1
        n = self.size
        for coor in self.list_bomb:
            i = coor[0]
            j = coor[1]
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if ((i + x >= 0) and (i + x < n) and (j + y >= 0) and (j + y < n)):
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
        print('Click tile ({}, {})'.format(i,j))
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
                if ((i + x >= 0) and (i + x < self.size) and (j + y >= 0) and (j + y < self.size)):
                    if (not self.board_open[i+x][j+y]):
                        self.click_tile(i + x, j + y, False)
        if base:
            print(self)
            if self.env is not None:
                self.assert_state(self.env)

    def assert_state(self, env):
        for i in range(self.size):
            for j in range(self.size):
                if self.board_open[i][j] == 1:
                    env.assert_string("(open {} {})".format(i, j))
                    env.assert_string(
                        '(value {} {} {})'.format(i, j, self.board[i][j]))


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
    board.click_tile(0, 0)
    # board.mark_tile((0, 6))
    # board.unmark_tile((0, 6))

    env = Environment()
    board.env = env
    env.define_function(board.click_tile, 'click_tile')
    env.load('minesweeper.clp')
    board.assert_state(env)
    env.reset()
    env.run()
    for fact in env.facts():
        print(fact)
    print(board)
