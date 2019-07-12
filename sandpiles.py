# coding=utf-8
import copy
import random
import pygame


class pycolors:
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255, 45)
    BLUE = pygame.Color(149, 202, 255)
    PINK = pygame.Color(255, 192, 203)
    RED = pygame.Color(237, 41, 57)

    def get_gradient(color_from, color_to, steps):
        if steps == 0:
            return []
        r_from, g_from, b_from, a_from = color_from
        r_to, g_to, b_to, a_to = color_to

        r_step = (r_to - r_from) / steps
        g_step = (g_to - g_from) / steps
        b_step = (b_to - b_from) / steps
        a_step = (a_to - a_from) / steps

        gradient = []
        for i in range(steps + 1):
            r = int(r_from + i * r_step)
            g = int(g_from + i * g_step)
            b = int(b_from + i * b_step)
            a = int(a_from + i * a_step)
            color = pygame.Color(r, g, b, a)
            gradient.append(color)
        return gradient


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
    def __init__(self, size=3, animated=False, max_value=3):
        self.GRID_SIZE = size
        self.animated = animated
        self.MAX_VALUE = max_value
        if self.animated:
            self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        self.CELL_SIZE = 5
        screen_x = self.GRID_SIZE * self.CELL_SIZE
        screen_y = self.GRID_SIZE * self.CELL_SIZE
        self.screen = pygame.display.set_mode((screen_x, screen_y))
        self.screen.fill(pycolors.BLACK)
        self.font = pygame.font.SysFont('Arial', 25)
        self.clock = pygame.time.Clock()
        self.FPS = 50
        self.color_gradient = pycolors.get_gradient(
            pycolors.BLUE, pycolors.PINK, self.MAX_VALUE
        )

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
                random_sandpile[row][column] = random.randint(
                    0, self.MAX_VALUE
                )

        return random_sandpile

    def _get_overflow_gradient(self, s):
        max_value = max([max(row) for row in s])
        gradient = pycolors.get_gradient(
            pycolors.PINK, pycolors.RED, max_value - self.MAX_VALUE
        )
        return gradient

    def pygame_draw(self, s):
        if not self.animated:
            return

        for x, row in enumerate(s):
            for y, element in enumerate(row):
                overflow_gradient = self._get_overflow_gradient(s)
                color_gradient = self.color_gradient + overflow_gradient
                color = color_gradient[element]
                radius = self.CELL_SIZE // 2
                center_point = (
                    x * self.CELL_SIZE + radius,
                    y * self.CELL_SIZE + radius,
                )
                pygame.draw.circle(self.screen, color, center_point, radius, 0)
                text = self.font.render(str(element), True, pycolors.WHITE)
                text_rect = text.get_rect()
                text_width = text_rect.width
                text_height = text_rect.height
                text_center_point = (
                    center_point[0] - text_width // 2,
                    center_point[1] - text_height // 2
                )
                self.screen.blit(text, text_center_point)
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def pygame_print(self, s):
        pygame.init()
        CELL_SIZE = 5
        screen_x = self.GRID_SIZE * CELL_SIZE
        screen_y = self.GRID_SIZE * CELL_SIZE
        screen = pygame.display.set_mode((screen_x, screen_y))
        # screen.fill(pycolors.BLACK)
        color_gradient = pycolors.get_gradient(
            pycolors.BLUE, pycolors.RED, self.MAX_VALUE
        )

        for x, row in enumerate(s):
            for y, element in enumerate(row):
                color = color_gradient[element]
                radius = CELL_SIZE // 2
                center_point = (x * CELL_SIZE + radius, y * CELL_SIZE + radius)
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
    # You repeat this until there's no cell with more than MAX_VALUE grains of
    # sand in it
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
            if self.animated:
                new_r = copy.deepcopy(r)
            else:
                new_r = r
            for row in range(self.GRID_SIZE):
                for column in range(self.GRID_SIZE):
                    if r[row][column] > self.MAX_VALUE:
                        toppling = True
                        new_r[row][column] -= 4
                        if row+1 < self.GRID_SIZE:
                            new_r[row+1][column] += 1
                        if row-1 >= 0:
                            new_r[row-1][column] += 1
                        if column+1 < self.GRID_SIZE:
                            new_r[row][column+1] += 1
                        if column-1 >= 0:
                            new_r[row][column-1] += 1
            r = new_r

            if self.animated:
                self.pygame_draw(r)
        return r


if __name__ == '__main__':
    BIG_VALUE = 10000
    sandpiles = Sandpiles(200, animated=False)
    result = sandpiles.add(sandpiles.ZERO, sandpiles.bigpile(BIG_VALUE))
    # sandpiles.color_print(result)
    # sandpiles.normal_print(result)
    sandpiles.pygame_print(result)
    input("Press enter to finish...")
