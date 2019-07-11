# coding=utf-8
import random
import pygame


class pycolors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255, 45)
    BLUE = pygame.Color(149, 202, 255)
    PINK = pygame.Color(255, 192, 203)
    RED = pygame.Color(237, 41, 57)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# a sandpile is a GRID_SIZExGRID_SIZE grid with each cell containing a number
# from 0 to 3
# sandpile = [
#     [a, b, c],
#     [d, e, f],
#     [g, h, i],
# ]


# sandpile[row][column]
class Sandpiles:
    def __init__(self, size=3):
        self.GRID_SIZE = size

    def _GENERATOR(self, number):
        r = []
        for i in range(self.GRID_SIZE):
            m = []
            for j in range(self.GRID_SIZE):
                m.append(number)
            r.append(m)
        return r

    @property
    def ZERO(self):
        return self._GENERATOR(0)
        # return [[0, ] * self.GRID_SIZE, ] * self.GRID_SIZE

    @property
    def ONE(self):
        return self._GENERATOR(1)
        # return [[1, ] * self.GRID_SIZE, ] * self.GRID_SIZE

    @property
    def TWO(self):
        return self._GENERATOR(2)
        # return [[2, ] * self.GRID_SIZE, ] * self.GRID_SIZE

    @property
    def THREE(self):
        return self._GENERATOR(3)
        # return [[3, ] * self.GRID_SIZE, ] * self.GRID_SIZE

    def bigpile(self, size=100):
        big_pile = self.ZERO
        middle = self.GRID_SIZE // 2
        big_pile[middle][middle] = size
        return big_pile

    @property
    def RANDOM(self):
        random_sandpile = self.ZERO
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                random_sandpile[row][column] = random.randint(0, 3)

        return random_sandpile

    def pygame_print(self, s):
        pygame.init()
        CELL_SIZE = 2
        screen_x = self.GRID_SIZE * CELL_SIZE
        screen_y = self.GRID_SIZE * CELL_SIZE
        screen = pygame.display.set_mode((screen_x, screen_y))
        # screen.fill(pycolors.BLACK)
        # clock = pygame.time.Clock()
        # FPS = 50
        # clock.tick(FPS)
        colors = {
            0: pycolors.BLUE,
            1: pycolors.WHITE,
            2: pycolors.PINK,
            3: pycolors.RED,
        }

        for x, row in enumerate(s):
            for y, element in enumerate(row):
                color = colors[element]
                center_point = (x * CELL_SIZE, y * CELL_SIZE)
                radius = CELL_SIZE
                pygame.draw.circle(screen, color, center_point, radius, 0)
        pygame.display.flip()

    def normal_print(self, s):
        for row in s:
            print(row)

    def color_print(self, s):
        for row in s:
            row_to_print = ''
            for element in row:
                if element == 0:
                    color = bcolors.OKBLUE
                if element == 1:
                    color = bcolors.OKGREEN
                if element == 2:
                    color = bcolors.WARNING
                if element == 3:
                    color = bcolors.FAIL
                row_to_print += color + u"\u2588"
            print(row_to_print)
        print(bcolors.ENDC)

    # When adding, you add cell by cell. If a cell ends up with a number bigger
    # than 3, then it 'topples', meaning it loses a grain of salt for each of
    # the four major directions (up, down, left, right). If that direction
    # leads to outside of the sandpile, it vanishes. If it leads to another
    # cell, it gets added to whatever number it has. The cell that topples ends
    # up with four less grains of salt.
    # You repeat this until there's no cell with more than 3 grains of salt in
    # it
    def add(self, s1, s2):
        r = self.ZERO
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                r[row][column] = s1[row][column] + s2[row][column]

        return self.handle_toppling(r)

    def handle_toppling(self, r):
        toppling = True
        while toppling:
            toppling = False
            for row in range(self.GRID_SIZE):
                for column in range(self.GRID_SIZE):
                    if r[row][column] > 3:
                        toppling = True
                        r[row][column] -= 4
                        if row+1 < self.GRID_SIZE:
                            r[row+1][column] += 1
                        if row-1 >= 0:
                            r[row-1][column] += 1
                        if column+1 < self.GRID_SIZE:
                            r[row][column+1] += 1
                        if column-1 >= 0:
                            r[row][column-1] += 1

        return r


if __name__ == '__main__':
    sandpiles = Sandpiles(100)
    result = sandpiles.add(sandpiles.ZERO, sandpiles.bigpile(10000))
    # sandpiles.color_print(result)
    # sandpiles.normal_print(result)
    sandpiles.pygame_print(result)
